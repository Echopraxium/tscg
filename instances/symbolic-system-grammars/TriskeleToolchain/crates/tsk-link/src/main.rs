// tsk-link/src/main.rs
// Author: Echopraxium with the collaboration of Claude AI
// Version: 0.3.0
//
// tsk-link — TriskeleVM linker: .tobj × N → .tvmx
//
// Usage:
//   tsk-link file1.tobj file2.tobj -o output.tvmx
//   tsk-link file1.tobj file2.tobj -o output.tvmx --entry main
//   tsk-link file1.tobj --dump-symbols
//
// Pipeline:
//   1. Load all .tobj files → parse code + data + symtab sections
//   2. Build global symbol table (name → file + offset)
//   3. Lay out final binary: concatenate code sections, then data sections
//   4. Patch F_CALL / F_JMP placeholders with final addresses
//   5. Emit .tvmx via TvmBuilder

use std::collections::HashMap;
use std::path::PathBuf;
use anyhow::{anyhow, bail, Result};
use clap::Parser;
use triskele_common::tvm::{TvmFile, TvmBuilder, SectionType};
use triskele_common::isa::Opcode;
use triskele_common::instr::{encode_r, encode_i};
use triskele_common::libc_symbols::libc_sym_addr;

// ─────────────────────────────────────────────────────────────────────────────
// CLI
// ─────────────────────────────────────────────────────────────────────────────

#[derive(Parser, Debug)]
#[clap(
    name    = "tsk-link",
    version = "0.3.0",
    about   = "TriskeleVM linker — .tobj × N → .tvmx"
)]
struct Args {
    /// Input object files (.tobj)
    #[clap(required = true)]
    inputs: Vec<PathBuf>,

    /// Output executable (.tvmx). Default: a.tvmx
    #[clap(short = 'o', long, default_value = "a.tvmx")]
    output: PathBuf,

    /// Entry point symbol name (default: first function in first .tobj)
    #[clap(long, default_value = "")]
    entry: String,

    /// Dump symbol tables of all input files
    #[clap(long)]
    dump_symbols: bool,

    /// Verbose output
    #[clap(short, long)]
    verbose: bool,
}

// ─────────────────────────────────────────────────────────────────────────────
// Object file representation
// ─────────────────────────────────────────────────────────────────────────────

struct ObjectFile {
    #[allow(dead_code)] path: PathBuf,
    code:     Vec<u8>,
    data:     Vec<u8>,
    /// symbols: name → byte offset within this object's code section
    symbols:  HashMap<String, u32>,
    /// relocations: (local_code_offset, symbol_name) — unresolved call targets
    relocs:   Vec<(u32, String)>,
    /// entry offset within this object's code (first function)
    entry:    u32,
}

impl ObjectFile {
    fn load(path: &PathBuf) -> Result<Self> {
        let bytes = std::fs::read(path)?;
        let tvm   = TvmFile::load_from_reader(&mut std::io::Cursor::new(&bytes))
            .map_err(|e| anyhow!("{}: {}", path.display(), e))?;

        let code = tvm.find_section(SectionType::Code)
            .map(|s| s.data.clone())
            .unwrap_or_default();

        let data = tvm.find_section(SectionType::Data)
            .map(|s| s.data.clone())
            .unwrap_or_default();

        // Parse symbol table: null-terminated name + u32 offset (little-endian)
        let symbols = if let Some(sym_sec) = tvm.find_section(SectionType::Symtab) {
            parse_symtab(&sym_sec.data)
        } else {
            HashMap::new()
        };

        let entry = tvm.entry_offset();

        // Parse relocation table: [u32 offset][name\0] repeated
        let relocs = if let Some(rel_sec) = tvm.find_section(SectionType::Reltab) {
            parse_reltab(&rel_sec.data)
        } else {
            Vec::new()
        };

        Ok(Self { path: path.clone(), code, data, symbols, relocs, entry })
    }
}

/// Parse relocation table: [u32 code_offset][null-terminated symbol name] repeated
fn parse_reltab(data: &[u8]) -> Vec<(u32, String)> {
    let mut relocs = Vec::new();
    let mut i = 0;
    while i + 4 < data.len() {
        let offset = u32::from_le_bytes(data[i..i+4].try_into().unwrap());
        i += 4;
        let start = i;
        while i < data.len() && data[i] != 0 { i += 1; }
        let name = String::from_utf8_lossy(&data[start..i]).to_string();
        if i < data.len() { i += 1; } // skip null
        if !name.is_empty() {
            relocs.push((offset, name));
        }
    }
    relocs
}

/// Parse the flat symtab format written by tsk-cc:
/// [name\0][u32 offset] repeated
fn parse_symtab(data: &[u8]) -> HashMap<String, u32> {
    let mut map = HashMap::new();
    let mut i = 0;
    while i < data.len() {
        // Read null-terminated name
        let start = i;
        while i < data.len() && data[i] != 0 { i += 1; }
        if i >= data.len() { break; }
        let name = String::from_utf8_lossy(&data[start..i]).to_string();
        i += 1; // skip null

        // Read u32 offset
        if i + 4 > data.len() { break; }
        let offset = u32::from_le_bytes(data[i..i+4].try_into().unwrap());
        i += 4;

        if !name.is_empty() {
            map.insert(name, offset);
        }
    }
    map
}

// ─────────────────────────────────────────────────────────────────────────────
// Linker
// ─────────────────────────────────────────────────────────────────────────────

struct Linker {
    objects: Vec<ObjectFile>,
    /// global symbol → absolute VM address in final binary
    global_syms: HashMap<String, u64>,
    /// base VM address for code (after null page)
    code_base: u64,
    /// base VM address for data (after code)
    data_base: u64,
}

const NULL_PAGE_END: u64 = 0x1000;

impl Linker {
    fn new(objects: Vec<ObjectFile>) -> Self {
        Self {
            objects,
            global_syms: HashMap::new(),
            code_base: NULL_PAGE_END,
            data_base: 0,
        }
    }

    fn link(&mut self, entry_name: &str, verbose: bool) -> Result<Vec<u8>> {
        // ── Phase 0: pre-populate tsk-libc symbols ───────────────────────────
        // These are always available at fixed addresses in the libc segment.
        // Doing this first lets .tobj symbols override them if needed.
        use triskele_common::libc_symbols::LIBC_SYMBOLS;
        for sym in LIBC_SYMBOLS {
            self.global_syms.insert(sym.name.to_string(), sym.stub_addr());
        }

        // ── Phase 0b: pre-scan relocations for far F_CALLs ───────────────────
        // Count how many trampolines will be needed so that data_base can be
        // set correctly in Phase 1 BEFORE D_MovI data-pointer patching in Phase 2.
        // A far call is any relocation whose target is in the libc range (≥0xE0000000).
        // Each trampoline is 6 instructions = 24 bytes.
        const TRAMPOLINE_BYTES: u64 = 24; // 6 × 4-byte instructions
        let mut n_far_calls: u64 = 0;
        for obj in &self.objects {
            for (local_off, sym_name) in &obj.relocs {
                let (base_name, _) = if let Some(plus) = sym_name.find('+') {
                    (&sym_name[..plus], ())
                } else {
                    (sym_name.as_str(), ())
                };
                // Check if this symbol resolves to a far (libc) address
                if let Some(&addr) = self.global_syms.get(base_name) {
                    if addr >= 0xE000_0000 {
                        // Check if the instruction is F_CALL (will need trampoline)
                        let off = *local_off as usize;
                        if off + 4 <= obj.code.len() {
                            let word = u32::from_le_bytes(
                                obj.code[off..off+4].try_into().unwrap_or([0;4])
                            );
                            let op = (word >> 24) as u8;
                            if op == Opcode::F_Call as u8 {
                                n_far_calls += 1;
                            }
                        }
                    }
                }
            }
        }
        let trampoline_reservation: u64 = n_far_calls * TRAMPOLINE_BYTES;
        log::debug!("pre-scan: {} far F_CALLs → {} bytes trampoline reservation",
            n_far_calls, trampoline_reservation);

        // ── Phase 1: layout — assign absolute addresses to all symbols ────────
        let mut code_offset: u64 = 0;
        let mut obj_code_bases = Vec::new();

        for obj in &self.objects {
            obj_code_bases.push(code_offset);
            // Register CODE symbols (flag bit 31 = 0)
            for (name, local_off) in &obj.symbols {
                if *local_off & 0x8000_0000 != 0 { continue; } // skip data symbols
                let abs_addr = self.code_base + code_offset + *local_off as u64;
                if verbose {
                    eprintln!("[tsk-link] code sym @{} → 0x{:08X}", name, abs_addr);
                }
                if self.global_syms.contains_key(name) {
                    eprintln!("[tsk-link] WARNING: duplicate symbol @{}", name);
                }
                self.global_syms.insert(name.clone(), abs_addr);
            }
            // Advance code pointer (align to 4)
            code_offset += obj.code.len() as u64;
            while code_offset % 4 != 0 { code_offset += 1; }
        }

        // Data section follows code
        self.data_base = self.code_base + code_offset + trampoline_reservation;
        let mut data_offset: u64 = 0;
        let mut obj_data_bases = Vec::new();

        for obj in &self.objects {
            obj_data_bases.push(data_offset);
            // Register DATA symbols (flag bit 31 = 1)
            for (name, local_off) in &obj.symbols {
                if *local_off & 0x8000_0000 == 0 { continue; } // skip code symbols
                let data_local = (*local_off & 0x7FFF_FFFF) as u64;
                let abs_addr = self.data_base + data_offset + data_local;
                if verbose {
                    eprintln!("[tsk-link] data sym @{} → 0x{:08X}", name, abs_addr);
                }
                self.global_syms.insert(name.clone(), abs_addr);
            }
            data_offset += obj.data.len() as u64;
            while data_offset % 8 != 0 { data_offset += 1; }
        }

        // ── Phase 2: concatenate code + patch call placeholders ───────────────
        // far_trampolines: (sym_name, [words]) — trampolines for out-of-range F_CALL
        // far_call_fixups: (fcall_vm_addr, trampoline_index) — F_CALLs needing Phase 3 fixup
        let mut far_trampolines: Vec<(String, Vec<u32>)> = Vec::new();
        let mut far_call_fixups: Vec<(u64, u32)> = Vec::new();
        let mut final_code: Vec<u8> = Vec::new();

        for (i, obj) in self.objects.iter().enumerate() {
            let obj_base = self.code_base + obj_code_bases[i];
            let mut code = obj.code.clone();

            // Apply relocations from .reltab
            for (local_off, sym_name) in &obj.relocs {
                let abs_code_off = *local_off as usize;
                if abs_code_off + 4 > code.len() {
                    log::warn!("reloc out of bounds: {} at 0x{:X}", sym_name, abs_code_off);
                    continue;
                }

                let word = u32::from_le_bytes(code[abs_code_off..abs_code_off+4].try_into().unwrap());
                let opcode_byte = (word >> 24) as u8;

                if let Some(op) = Opcode::from_byte(opcode_byte) {
                    // Look up symbol address — handle "name+offset" for inline GEP
                    let (base_name, const_off) = if let Some(plus) = sym_name.find('+') {
                        let off = sym_name[plus+1..].parse::<u64>().unwrap_or(0);
                        (&sym_name[..plus], off)
                    } else {
                        (sym_name.as_str(), 0u64)
                    };
                    let sym_addr = self.global_syms.get(base_name).copied()
                        .or_else(|| libc_sym_addr(base_name))
                        .unwrap_or_else(|| {
                            log::warn!("reloc: symbol @{} not found (unresolved)", base_name);
                            0
                        }) + const_off;

                    match op {
                        // D_MOV_I placeholder: patch with symbol address.
                        // If address fits imm19 (<= 0x3FFFF): patch in place (1 instr).
                        // Otherwise: expand to 5-instr sequence using the 20-byte slot
                        // that tsk-cc pre-allocates via split_const32 for large constants.
                        //   D_MovI dst, hi16
                        //   D_MovI R24, 16
                        //   D_Shl  dst, dst, R24
                        //   D_MovI R24, lo16
                        //   D_Or   dst, dst, R24
                        Opcode::D_MovI => {
                            let dst = (word >> 19) & 0x1F;
                            let addr = sym_addr as u32;
                            if addr <= 0x0003_FFFF {
                                // Fits in imm19 — simple patch
                                let patched = ((opcode_byte as u32) << 24)
                                    | (dst << 19)
                                    | (addr & 0x0007_FFFF);
                                code[abs_code_off..abs_code_off+4]
                                    .copy_from_slice(&patched.to_le_bytes());
                                log::debug!("patched D_MovI @{} → 0x{:X} at 0x{:X}",
                                    sym_name, addr, abs_code_off);
                            } else {
                                // Large address: 5-instruction sequence
                                let hi = (addr >> 16) as u32;
                                let lo = addr & 0xFFFF;
                                let scratch: u32 = 24; // REG_SCRATCH
                                let d_movi: u32 = 0x41; // D_MovI
                                let d_shl:  u32 = 0x4C; // D_Shl (Type R)
                                let d_or:   u32 = 0x46; // D_Or  (Type R)
                                // 0: D_MovI dst, hi
                                let w0 = (d_movi << 24) | (dst << 19) | (hi & 0x7FFFF);
                                // 1: D_MovI R24, 16
                                let w1 = (d_movi << 24) | (scratch << 19) | 16u32;
                                // 2: D_Shl dst, dst, R24
                                let w2 = (d_shl << 24) | (dst << 19) | (dst << 14) | (scratch << 9);
                                // 3: D_MovI R24, lo
                                let w3 = (d_movi << 24) | (scratch << 19) | (lo & 0x7FFFF);
                                // 4: D_Or dst, dst, R24
                                let w4 = (d_or << 24) | (dst << 19) | (dst << 14) | (scratch << 9);
                                let end = abs_code_off + 20;
                                if end <= code.len() {
                                    code[abs_code_off     ..abs_code_off +  4].copy_from_slice(&w0.to_le_bytes());
                                    code[abs_code_off +  4..abs_code_off +  8].copy_from_slice(&w1.to_le_bytes());
                                    code[abs_code_off +  8..abs_code_off + 12].copy_from_slice(&w2.to_le_bytes());
                                    code[abs_code_off + 12..abs_code_off + 16].copy_from_slice(&w3.to_le_bytes());
                                    code[abs_code_off + 16..abs_code_off + 20].copy_from_slice(&w4.to_le_bytes());
                                    log::debug!("patched D_MovI (large) @{} → 0x{:X} hi={} lo={} at 0x{:X}",
                                        sym_name, addr, hi, lo, abs_code_off);
                                } else {
                                    log::warn!("reloc large @{}: need 20 bytes at 0x{:X}, have {}",
                                        sym_name, abs_code_off, code.len() - abs_code_off);
                                    // Truncated fallback
                                    let patched = (d_movi << 24) | (dst << 19) | (addr & 0x7FFFF);
                                    code[abs_code_off..abs_code_off+4].copy_from_slice(&patched.to_le_bytes());
                                }
                            }
                        }
                        // F_CALL placeholder → patch 24-bit relative offset
                        // If target is out of ±8MB range (e.g. libc at 0xE000_0000),
                        // emit a trampoline and patch to call the trampoline instead.
                        Opcode::F_Call => {
                            let instr_vm = obj_base + abs_code_off as u64;
                            let delta = sym_addr as i64 - instr_vm as i64;
                            if delta.abs() > 0x7F_FFFF {
                                // Out of range — emit trampoline into far_trampolines
                                // Trampoline: D_MovI R24, hi16
                                //             D_Shl  R24, 16   (D_MovI R25,16 + D_SHL R24,R25)
                                //             D_Or   R24, lo16
                                //             Im_CallR R24
                                // (16 bytes, 4 instructions)
                                let hi16 = ((sym_addr >> 16) & 0xFFFF) as u32;
                                let lo16 = (sym_addr & 0xFFFF) as u32;
                                let r_scratch: u8 = 24; // REG_SCRATCH
                                // D_MovI R24, hi16
                                let w0 = encode_i(Opcode::D_MovI as u8, r_scratch, hi16 as i32);
                                // D_MovI R25, 16  (shift amount)
                                let w1 = encode_i(Opcode::D_MovI as u8, 25, 16);
                                // D_Shl R24, R24, R25
                                let w2 = encode_r(Opcode::D_Shl as u8, r_scratch, r_scratch, 25, 0);
                                // D_Or R24, R24, lo16  (via D_MovI R25, lo16; D_Or R24, R24, R25)
                                let w3 = encode_i(Opcode::D_MovI as u8, 25, lo16 as i32);
                                let w4 = encode_r(Opcode::D_Or as u8, r_scratch, r_scratch, 25, 0);
                                // Im_CallR R24 (Type R: op | d=0 | s1=24 | s2=0 | flags=0)
                                let w5 = encode_r(Opcode::Im_CbInvoke as u8, 0, r_scratch, 0, 0);
                                // Record trampoline (will be appended after all objects)
                                let tramp_words = vec![w0, w1, w2, w3, w4, w5];
                                far_trampolines.push((sym_name.clone(), tramp_words));
                                // Patch F_CALL to trampoline (address TBD — use placeholder reloc)
                                // We store the trampoline index in the offset field for now.
                                // Phase 3 will fix up the actual delta.
                                let tramp_idx = (far_trampolines.len() - 1) as u32;
                                let placeholder = ((Opcode::F_Call as u32) << 24) | tramp_idx;
                                code[abs_code_off..abs_code_off+4]
                                    .copy_from_slice(&placeholder.to_le_bytes());
                                // Record this reloc for Phase 3 fixup
                                far_call_fixups.push((
                                    obj_base + abs_code_off as u64,  // absolute VM addr of F_CALL
                                    tramp_idx,                        // trampoline index
                                ));
                                log::debug!("F_CALL @{} → trampoline[{}] (far: 0x{:X})",
                                    sym_name, tramp_idx, sym_addr);
                            } else {
                                let patched = ((Opcode::F_Call as u32) << 24)
                                    | ((delta as u32) & 0x00FF_FFFF);
                                code[abs_code_off..abs_code_off+4]
                                    .copy_from_slice(&patched.to_le_bytes());
                                log::debug!("patched F_CALL @{} delta={:+} at offset 0x{:X}",
                                    sym_name, delta, abs_code_off);
                            }
                        }
                        _ => {
                            log::debug!("reloc: ignoring op 0x{:02X} at 0x{:X}",
                                opcode_byte, abs_code_off);
                        }
                    }
                }
            }

            // Pad to 4-byte alignment
            while code.len() % 4 != 0 { code.push(0); }
            final_code.extend_from_slice(&code);
        }

        // ── Phase 3: append trampolines + fix up far F_CALLs ─────────────────
        // Trampolines sit at the end of the code section, within F_CALL range of
        // all compiled code (code is at LOAD_BASE ≈ 0x1000; trampolines immediately
        // after at LOAD_BASE + code_size — always within ±8MB).
        eprintln!("[tsk-link] DEBUG Phase3: final_code.len()={} code_offset={} n_trampolines={}",
            final_code.len(), code_offset, far_trampolines.len());
        if !far_trampolines.is_empty() {
            // Append trampolines and record their VM addresses
            let mut tramp_addrs: Vec<u64> = Vec::new();
            for (sym_name, words) in &far_trampolines {
                let tramp_vm_addr = self.code_base + final_code.len() as u64;
                tramp_addrs.push(tramp_vm_addr);
                log::debug!("trampoline @{} at 0x{:X}", sym_name, tramp_vm_addr);
                for w in words {
                    final_code.extend_from_slice(&w.to_le_bytes());
                }
            }
            // Fix up all far F_CALLs to point to their trampoline
            for (fcall_vm_addr, tramp_idx) in &far_call_fixups {
                let tramp_addr = tramp_addrs[*tramp_idx as usize];
                let delta = tramp_addr as i64 - *fcall_vm_addr as i64;
                let off = (*fcall_vm_addr - self.code_base) as usize;
                let patched = ((Opcode::F_Call as u32) << 24)
                    | ((delta as u32) & 0x00FF_FFFF);
                final_code[off..off+4].copy_from_slice(&patched.to_le_bytes());
                log::debug!("fixed far F_CALL at 0x{:X} → trampoline[{}] delta={:+}",
                    fcall_vm_addr, tramp_idx, delta);
            }

            // data_base was pre-computed in Phase 0b with trampoline_reservation
            // to avoid overlap. Verify the reservation was accurate.
            let actual_data_base = self.code_base + final_code.len() as u64;
            if actual_data_base != self.data_base {
                log::warn!("trampoline reservation mismatch: expected data_base=0x{:X}                             but trampolines end at 0x{:X} (diff={})",
                    self.data_base, actual_data_base,
                    actual_data_base as i64 - self.data_base as i64);
            }
        }

        // ── Phase 4a: concatenate data sections ───────────────────────────────
        let mut final_data: Vec<u8> = Vec::new();
        for obj in &self.objects {
            final_data.extend_from_slice(&obj.data);
            while final_data.len() % 8 != 0 { final_data.push(0); }
        }

        // ── Phase 4b: determine entry point ────────────────────────────────────
        let entry_addr: u64 = if !entry_name.is_empty() {
            *self.global_syms.get(entry_name)
                .ok_or_else(|| anyhow!("entry symbol @{} not found", entry_name))?
        } else if let Some(&addr) = self.global_syms.get("main") {
            // Auto-detect: use @main if present and no --entry specified
            log::debug!("entry: auto-selected @main at 0x{:X}", addr);
            addr
        } else {
            // Default: first function of first object
            let first_obj = &self.objects[0];
            let base = self.code_base + obj_code_bases[0];
            base + first_obj.entry as u64
        };

        let entry_offset = (entry_addr - self.code_base) as u32;

        if verbose {
            eprintln!("[tsk-link] entry = 0x{:08X} (offset 0x{:X})",
                entry_addr, entry_offset);
            eprintln!("[tsk-link] code  = {} bytes at 0x{:X}",
                final_code.len(), self.code_base);
            eprintln!("[tsk-link] data  = {} bytes at 0x{:X}",
                final_data.len(), self.data_base);
        }

        // ── Phase 5: emit .tvmx ───────────────────────────────────────────────
        // Build merged symbol table
        let mut merged_symtab: Vec<u8> = Vec::new();
        for (name, addr) in &self.global_syms {
            merged_symtab.extend_from_slice(name.as_bytes());
            merged_symtab.push(0);
            // Store absolute address as u32 (consistent with parse_symtab)
            merged_symtab.extend_from_slice(&(*addr as u32).to_le_bytes());
        }

        let mut builder = TvmBuilder::new()
            .entry(entry_offset)
            .add_section(SectionType::Code, 0x02, final_code);

        if !final_data.is_empty() {
            builder = builder.add_section(SectionType::Data, 0x01, final_data);
        }
        if !merged_symtab.is_empty() {
            builder = builder.add_section(SectionType::Symtab, 0x0E, merged_symtab);
        }

        Ok(builder.build())
    }
}

// ─────────────────────────────────────────────────────────────────────────────
// Main
// ─────────────────────────────────────────────────────────────────────────────

fn main() {
    env_logger::init();
    let args = Args::parse();

    if let Err(e) = run(args) {
        eprintln!("tsk-link error: {}", e);
        std::process::exit(1);
    }
}

fn run(args: Args) -> Result<()> {
    // Load all object files
    let mut objects = Vec::new();
    for path in &args.inputs {
        if !path.exists() {
            bail!("input file not found: {}", path.display());
        }
        let obj = ObjectFile::load(path)?;
        if args.verbose || args.dump_symbols {
            eprintln!("[tsk-link] loaded {} — {} bytes code, {} bytes data, {} symbols",
                path.display(), obj.code.len(), obj.data.len(), obj.symbols.len());
            if args.dump_symbols {
                let mut syms: Vec<_> = obj.symbols.iter().collect();
                syms.sort_by_key(|(_, &o)| o);
                for (name, off) in syms {
                    eprintln!("  @{:<20} offset 0x{:08X}", name, off);
                }
            }
        }
        objects.push(obj);
    }

    if objects.is_empty() {
        bail!("no input files");
    }

    // Link
    let mut linker = Linker::new(objects);
    let tvmx = linker.link(&args.entry, args.verbose)?;

    // Write output
    std::fs::write(&args.output, &tvmx)?;
    eprintln!("[tsk-link] {} input(s) → {}  ({} bytes)",
        args.inputs.len(), args.output.display(), tvmx.len());

    // Print symbol map
    if args.verbose {
        let mut syms: Vec<_> = linker.global_syms.iter().collect();
        syms.sort_by_key(|(_, &a)| a);
        eprintln!("[tsk-link] Symbol map:");
        for (name, addr) in syms {
            eprintln!("  0x{:08X}  @{}", addr, name);
        }
    }

    Ok(())
}

// ─────────────────────────────────────────────────────────────────────────────
// Tests
// ─────────────────────────────────────────────────────────────────────────────

#[cfg(test)]
mod tests {
    use super::*;
    use triskele_common::tvm::TvmBuilder;

    /// Build a minimal .tobj with one function and one symbol
    fn make_tobj(func_name: &str, code: Vec<u8>) -> Vec<u8> {
        // Symbol table
        let mut symtab = Vec::new();
        symtab.extend_from_slice(func_name.as_bytes());
        symtab.push(0);
        symtab.extend_from_slice(&0u32.to_le_bytes());  // offset 0

        TvmBuilder::new()
            .entry(0)
            .add_section(SectionType::Code,   0x02, code)
            .add_section(SectionType::Symtab, 0x0E, symtab)
            .build()
    }

    #[test]
    fn test_single_object_link() {
        use triskele_common::isa::Opcode;
        // Simple: D_MOV_I R0, 42 + F_RET
        let _code = vec![
            // D_MOV_I R0, 42
            0x00u8 | ((Opcode::D_MovI as u8)), 0x00, 0x00, 42,
            // F_RET
            Opcode::F_Ret as u8, 0x00, 0x00, 0x00,
        ];
        // Fix encoding: enc_i format
        let enc_movi = ((Opcode::D_MovI as u32) << 24) | 42u32;
        let enc_ret  = (Opcode::F_Ret  as u32) << 24;
        let code = [
            enc_movi.to_le_bytes(),
            enc_ret .to_le_bytes(),
        ].concat();

        let tobj = make_tobj("test_func", code);
        let tmp = std::env::temp_dir().join("test_single.tobj");
        std::fs::write(&tmp, &tobj).unwrap();

        let obj = ObjectFile::load(&tmp).unwrap();
        assert_eq!(obj.symbols.get("test_func"), Some(&0u32));
        assert_eq!(obj.code.len(), 8);

        let mut linker = Linker::new(vec![obj]);
        let tvmx = linker.link("test_func", false).unwrap();
        assert!(!tvmx.is_empty());

        let loaded = TvmFile::load_from_reader(&mut std::io::Cursor::new(&tvmx)).unwrap();
        let code_sec = loaded.find_section(SectionType::Code).unwrap();
        assert_eq!(code_sec.data.len(), 8);
    }

    #[test]
    fn test_two_object_link() {
        // Two objects — check symbol table merging
        let enc_ret = ((Opcode::F_Ret as u32) << 24).to_le_bytes().to_vec();

        let tobj1 = make_tobj("func_a", enc_ret.clone());
        let tobj2 = make_tobj("func_b", enc_ret.clone());

        let tmp1 = std::env::temp_dir().join("test_link_a.tobj");
        let tmp2 = std::env::temp_dir().join("test_link_b.tobj");
        std::fs::write(&tmp1, &tobj1).unwrap();
        std::fs::write(&tmp2, &tobj2).unwrap();

        let obj1 = ObjectFile::load(&tmp1).unwrap();
        let obj2 = ObjectFile::load(&tmp2).unwrap();

        let mut linker = Linker::new(vec![obj1, obj2]);
        let tvmx = linker.link("func_a", false).unwrap();
        assert!(!tvmx.is_empty());

        // Both symbols should be resolved
        assert!(linker.global_syms.contains_key("func_a"));
        assert!(linker.global_syms.contains_key("func_b"));

        // func_b must be at a higher address than func_a
        assert!(linker.global_syms["func_b"] > linker.global_syms["func_a"]);
    }

    #[test]
    fn test_symtab_parse() {
        let mut data = Vec::new();
        for (name, off) in [("foo", 0u32), ("bar", 16u32), ("baz", 32u32)] {
            data.extend_from_slice(name.as_bytes());
            data.push(0);
            data.extend_from_slice(&off.to_le_bytes());
        }
        let syms = parse_symtab(&data);
        assert_eq!(syms["foo"], 0);
        assert_eq!(syms["bar"], 16);
        assert_eq!(syms["baz"], 32);
    }

    // ── libc symbol resolution ────────────────────────────────────────────────

    #[test]
    fn test_libc_symbols_pre_populated() {
        // After link(), all libc symbols must be resolved to 0xE000_xxxx addresses
        use triskele_common::instr::encode_j;
        use triskele_common::isa::Opcode;
        // Object with a single F_CALL to @printf + F_Ret
        let f_call = encode_j(Opcode::F_Call as u8, 0).to_le_bytes();
        let f_ret  = encode_j(Opcode::F_Ret  as u8, 0).to_le_bytes();
        let mut code = Vec::new();
        code.extend_from_slice(&f_call);
        code.extend_from_slice(&f_ret);
        // Relocation: offset 0, symbol "printf"
        let mut reltab = Vec::new();
        reltab.extend_from_slice(&0u32.to_le_bytes());
        reltab.extend_from_slice(b"printf\0");
        let obj_bytes = TvmBuilder::new()
            .entry(0)
            .add_section(SectionType::Code,   0x02, code)
            .add_section(SectionType::Symtab, 0x0E,
                { let mut s = b"main\0".to_vec(); s.extend_from_slice(&0u32.to_le_bytes()); s })
            .add_section(SectionType::Reltab, 0x0F, reltab)
            .build();
        let tmp = tempfile::NamedTempFile::new().unwrap();
        std::fs::write(tmp.path(), &obj_bytes).unwrap();
        let obj = ObjectFile::load(&tmp.path().to_path_buf()).unwrap();
        let mut linker = Linker::new(vec![obj]);
        linker.link("main", false).unwrap();
        // @printf must resolve to libc base area
        let printf_addr = linker.global_syms.get("printf").copied().unwrap_or(0);
        assert!(printf_addr >= 0xE000_0000,
            "@printf must resolve to libc area, got 0x{:X}", printf_addr);
        assert_eq!(printf_addr, 0xE000_0000 + 0x40 * 8,
            "@printf must be at LIBC_BASE + Printf_id * STUB_SIZE");
    }

    // ── trampoline / data section non-overlap ─────────────────────────────────

    /// Build a minimal .tobj that makes N far calls to @printf.
    fn make_tobj_with_far_calls(n_calls: usize) -> Vec<u8> {
        use triskele_common::instr::encode_j;
        use triskele_common::isa::Opcode;
        let f_call = encode_j(Opcode::F_Call as u8, 0).to_le_bytes();
        let f_ret  = encode_j(Opcode::F_Ret  as u8, 0).to_le_bytes();
        let mut code = Vec::new();
        let mut reltab = Vec::new();
        for i in 0..n_calls {
            let off = (i * 4) as u32;
            code.extend_from_slice(&f_call);
            reltab.extend_from_slice(&off.to_le_bytes());
            reltab.extend_from_slice(b"printf\0");
        }
        code.extend_from_slice(&f_ret);
        // Data section: a small string
        let data = b"test\0\0\0\0".to_vec(); // 8 bytes
        // Data symbol at offset 0 (flag bit 31 set = data symbol)
        let mut symtab = b"main\0".to_vec();
        symtab.extend_from_slice(&0u32.to_le_bytes());
        symtab.extend_from_slice(b"str\0".as_ref());
        symtab.extend_from_slice(&0x8000_0000u32.to_le_bytes()); // data symbol
        TvmBuilder::new()
            .entry(0)
            .add_section(SectionType::Code,   0x02, code)
            .add_section(SectionType::Data,   0x01, data)
            .add_section(SectionType::Symtab, 0x0E, symtab)
            .add_section(SectionType::Reltab, 0x0F, reltab)
            .build()
    }

    #[test]
    fn test_trampolines_do_not_overlap_data_1_call() {
        trampolines_no_overlap_check(1);
    }

    #[test]
    fn test_trampolines_do_not_overlap_data_3_calls() {
        trampolines_no_overlap_check(3);
    }

    #[test]
    fn test_trampolines_do_not_overlap_data_7_calls() {
        trampolines_no_overlap_check(7);
    }

    fn trampolines_no_overlap_check(n_calls: usize) {
        let obj_bytes = make_tobj_with_far_calls(n_calls);
        let tmp = tempfile::NamedTempFile::new().unwrap();
        std::fs::write(tmp.path(), &obj_bytes).unwrap();
        let obj = ObjectFile::load(&tmp.path().to_path_buf()).unwrap();
        let code_len = obj.code.len() as u64;

        let mut linker = Linker::new(vec![obj]);
        linker.link("main", false).unwrap();

        // Trampolines: each is 24 bytes, starts at LOAD_BASE + code_len
        let tramp_start = linker.code_base + code_len;
        let tramp_end   = tramp_start + n_calls as u64 * 24;

        // Data: must start at or after tramp_end
        let data_base = linker.data_base;
        assert!(data_base >= tramp_end,
            "data_base 0x{:X} overlaps trampolines (end=0x{:X}) for {} calls",
            data_base, tramp_end, n_calls);

        // Data symbol @str must be at data_base + 0 (offset 0)
        let str_addr = linker.global_syms.get("str").copied().unwrap_or(0);
        assert_eq!(str_addr, data_base,
            "@str must be at data_base=0x{:X}, got 0x{:X}", data_base, str_addr);

        // str_addr must NOT fall inside trampoline range
        assert!(str_addr >= tramp_end,
            "@str at 0x{:X} falls inside trampolines [0x{:X}..0x{:X}]",
            str_addr, tramp_start, tramp_end);
    }
}
