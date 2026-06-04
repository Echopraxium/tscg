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
        self.data_base = self.code_base + code_offset;
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
                    eprintln!("[tsk-link] reloc sym='{}' base='{}' off={} known_syms={:?}",
                        sym_name, base_name, const_off,
                        self.global_syms.keys().collect::<Vec<_>>());
                    let sym_addr = self.global_syms.get(base_name).copied()
                        .unwrap_or_else(|| {
                            eprintln!("[tsk-link] ERROR: symbol @{} not found in symtab!", base_name);
                            0
                        }) + const_off;
                    eprintln!("[tsk-link] resolved @{} → 0x{:X}", sym_name, sym_addr);

                    match op {
                        // D_MOV_I placeholder → patch 19-bit imm with symbol address
                        // Used for global data addresses (tilemap etc.)
                        // Note: only low 19 bits fit — linker warns if address is too large
                        Opcode::D_MovI => {
                            let dst = (word >> 19) & 0x1F;
                            if sym_addr > 0x0007_FFFF {
                                log::warn!("reloc: @{} addr 0x{:X} truncated to 19 bits",
                                    sym_name, sym_addr);
                            }
                            let patched = ((opcode_byte as u32) << 24)
                                | (dst << 19)
                                | ((sym_addr as u32) & 0x0007_FFFF);
                            code[abs_code_off..abs_code_off+4]
                                .copy_from_slice(&patched.to_le_bytes());
                            log::debug!("patched D_MOV_I @{} → 0x{:X} at offset 0x{:X}",
                                sym_name, sym_addr, abs_code_off);
                        }
                        // F_CALL placeholder → patch 24-bit relative offset
                        Opcode::F_Call => {
                            let instr_vm = obj_base + abs_code_off as u64;
                            let delta = sym_addr as i64 - instr_vm as i64;
                            if delta.abs() > 0x7F_FFFF {
                                log::warn!("F_CALL to @{} exceeds ±8MB range", sym_name);
                            }
                            let patched = ((Opcode::F_Call as u32) << 24)
                                | ((delta as u32) & 0x00FF_FFFF);
                            code[abs_code_off..abs_code_off+4]
                                .copy_from_slice(&patched.to_le_bytes());
                            log::debug!("patched F_CALL @{} delta={:+} at offset 0x{:X}",
                                sym_name, delta, abs_code_off);
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

        // ── Phase 3: concatenate data sections ────────────────────────────────
        let mut final_data: Vec<u8> = Vec::new();
        for obj in &self.objects {
            final_data.extend_from_slice(&obj.data);
            while final_data.len() % 8 != 0 { final_data.push(0); }
        }

        // ── Phase 4: determine entry point ────────────────────────────────────
        let entry_addr: u64 = if !entry_name.is_empty() {
            *self.global_syms.get(entry_name)
                .ok_or_else(|| anyhow!("entry symbol @{} not found", entry_name))?
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
        let code = vec![
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
}
