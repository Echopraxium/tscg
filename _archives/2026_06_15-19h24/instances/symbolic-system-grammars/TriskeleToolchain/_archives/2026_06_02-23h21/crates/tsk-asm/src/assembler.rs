// tsk-asm/src/assembler.rs
// Author: Echopraxium with the collaboration of Claude AI
// Version: 0.3.0
//
// One-pass assembler with label fixup.
// Supports multiple sections (.code, .rodata, .data, .bss).
// .rodata is laid out before .code in memory; labels are resolved across sections.

use std::collections::HashMap;
use anyhow::{anyhow, bail};
use triskele_common::isa::Opcode;
use crate::lexer::{Token, Spanned};
use crate::encoder::{encode_r, encode_i, encode_j, is_jump_mnemonic, is_immediate_mnemonic};

// ─────────────────────────────────────────────────────────────────────────────
// Output
// ─────────────────────────────────────────────────────────────────────────────

pub struct AsmOutput {
    pub code:         Vec<u8>,    // .code section bytes
    pub rodata:       Vec<u8>,    // .rodata section bytes
    pub entry_offset: u32,        // offset of entry point within .code
    pub module_name:  String,
    /// All labels with their VM byte address (for --emit-symbols)
    pub symbol_table: HashMap<String, u64>,
}

// ─────────────────────────────────────────────────────────────────────────────
// Active section
// ─────────────────────────────────────────────────────────────────────────────

#[derive(Debug, Clone, Copy, PartialEq)]
enum Section { Code, Rodata, Data, Bss }

// ─────────────────────────────────────────────────────────────────────────────
// Relocation types
// ─────────────────────────────────────────────────────────────────────────────

#[derive(Debug)]
enum RelocKind {
    // Jump/branch — 24-bit signed offset relative to instruction address
    Jump,
    // LEA to rodata label — stores label name; resolved as absolute VM address
    // packed into two Type I instructions (hi/lo 32-bit halves)
    LeaRodata,
}

struct Reloc {
    code_offset: usize,     // byte offset in .code where placeholder lives
    label:       String,    // target label
    kind:        RelocKind,
    line:        usize,
}

// ─────────────────────────────────────────────────────────────────────────────
// Assembler
// ─────────────────────────────────────────────────────────────────────────────

pub struct Assembler {
    tokens:       Vec<Spanned>,
    pos:          usize,
    code:         Vec<u8>,
    rodata:       Vec<u8>,
    current:      Section,
    labels:       HashMap<String, (Section, usize)>,  // label → (section, offset)
    relocs:       Vec<Reloc>,
    defines:      HashMap<String, i64>,
    module_name:  String,
    entry_label:  String,
    entry_offset: u32,
}

impl Assembler {
    pub fn new(tokens: Vec<Spanned>) -> Self {
        Self {
            tokens,
            pos: 0,
            code:    Vec::new(),
            rodata:  Vec::new(),
            current: Section::Code,
            labels:  HashMap::new(),
            relocs:  Vec::new(),
            defines: HashMap::new(),
            module_name:  String::from("unnamed"),
            entry_label:  String::new(),
            entry_offset: 0,
        }
    }

    pub fn assemble(mut self) -> anyhow::Result<AsmOutput> {
        self.skip_newlines();
        while !self.at_eof() {
            self.parse_line()?;
            self.skip_newlines();
        }
        self.fixup_labels()?;
        if !self.entry_label.is_empty() {
            let (sec, off) = self.labels.get(&self.entry_label)
                .ok_or_else(|| anyhow!("entry label '{}' not defined", self.entry_label))?;
            if *sec != Section::Code {
                bail!("entry label '{}' must be in .code section", self.entry_label);
            }
            self.entry_offset = *off as u32;
        }
        // Build symbol table: resolve each label to its VM byte address
        let rodata_size = self.rodata.len();
        let code_base   = ((rodata_size + 3) & !3) as u64;
        let mut symbol_table: HashMap<String, u64> = HashMap::new();
        for (label, (sec, offset)) in &self.labels {
            let addr = match sec {
                Section::Rodata | Section::Data => *offset as u64,
                Section::Code | Section::Bss    => code_base + *offset as u64,
            };
            symbol_table.insert(label.clone(), addr);
        }

        Ok(AsmOutput {
            code:         self.code,
            rodata:       self.rodata,
            entry_offset: self.entry_offset,
            module_name:  self.module_name,
            symbol_table,
        })
    }

    // ─────────────────────────────────────────────────────────────────────────
    // Active section helpers
    // ─────────────────────────────────────────────────────────────────────────

    fn active_buf(&mut self) -> &mut Vec<u8> {
        match self.current {
            Section::Rodata | Section::Data => &mut self.rodata,
            _ => &mut self.code,
        }
    }

    fn active_offset(&self) -> usize {
        match self.current {
            Section::Rodata | Section::Data => self.rodata.len(),
            _ => self.code.len(),
        }
    }

    // ─────────────────────────────────────────────────────────────────────────
    // Line parsing
    // ─────────────────────────────────────────────────────────────────────────

    fn parse_line(&mut self) -> anyhow::Result<()> {
        let tok = self.peek().clone();
        match &tok {
            Token::Label(name) => {
                let name = name.clone();
                let offset = self.active_offset();
                let section = self.current;
                if self.labels.insert(name.clone(), (section, offset)).is_some() {
                    bail!("duplicate label: '{}'", name);
                }
                self.advance();
                self.skip_newlines();
                if !self.at_eof() && !matches!(self.peek(), Token::Newline) {
                    self.parse_line()?;
                }
            }
            Token::Directive(name) => {
                let name = name.clone();
                self.advance();
                self.parse_directive(&name)?;
                self.expect_newline()?;
            }
            Token::Define => {
                self.advance();
                self.parse_define()?;
                self.expect_newline()?;
            }
            Token::Ifdef | Token::Ifndef | Token::Endif | Token::Undef | Token::Include => {
                self.advance();
                self.skip_to_newline();
            }
            Token::Ident(mnemonic) => {
                let mnemonic = mnemonic.clone();
                let line = self.current_line();
                self.advance();
                self.parse_instruction(&mnemonic, line)?;
                self.expect_newline()?;
            }
            Token::Newline | Token::Eof => {}
            _ => bail!("unexpected token: {:?}", tok),
        }
        Ok(())
    }

    // ─────────────────────────────────────────────────────────────────────────
    // Directives
    // ─────────────────────────────────────────────────────────────────────────

    fn parse_directive(&mut self, name: &str) -> anyhow::Result<()> {
        match name {
            "module" => { self.module_name = self.expect_ident()?; }
            "type"   => { let _ = self.expect_ident()?; }
            "entry"  => { self.entry_label = self.expect_ident()?; }
            "section" => {
                let sec_name = self.expect_ident()?;
                self.current = match sec_name.as_str() {
                    "code"   | ".code"   => Section::Code,
                    "rodata" | ".rodata" => Section::Rodata,
                    "data"   | ".data"   => Section::Data,
                    "bss"    | ".bss"    => Section::Bss,
                    other => bail!("unknown section: '{}'", other),
                };
            }
            // Data directives — emit raw bytes into active section
            "byte" => {
                let v = self.parse_expr()? as u8;
                self.active_buf().push(v);
            }
            "word" => {
                let v = self.parse_expr()? as u16;
                let bytes = v.to_le_bytes();
                self.active_buf().extend_from_slice(&bytes);
            }
            "dword" => {
                let v = self.parse_expr()? as u32;
                let bytes = v.to_le_bytes();
                self.active_buf().extend_from_slice(&bytes);
            }
            "qword" => {
                let v = self.parse_expr()? as u64;
                let bytes = v.to_le_bytes();
                self.active_buf().extend_from_slice(&bytes);
            }
            "string" => {
                // .string "hello\n"  → bytes + \0
                match self.peek().clone() {
                    Token::StringLit(s) => {
                        self.advance();
                        let buf = self.active_buf();
                        buf.extend_from_slice(s.as_bytes());
                        buf.push(0); // null terminator
                    }
                    tok => bail!("expected string literal after .string, got {:?}", tok),
                }
            }
            "ascii" => {
                // .ascii "hello"  → bytes WITHOUT \0
                match self.peek().clone() {
                    Token::StringLit(s) => {
                        self.advance();
                        self.active_buf().extend_from_slice(s.as_bytes());
                    }
                    tok => bail!("expected string literal after .ascii, got {:?}", tok),
                }
            }
            "align" => {
                let align = self.parse_expr()? as usize;
                let len = self.active_offset();
                let pad = (align - (len % align)) % align;
                let buf = self.active_buf();
                for _ in 0..pad { buf.push(0); }
            }
            "export" | "extern" | "import" | "tscg" => { self.skip_to_newline(); }
            _ => { self.skip_to_newline(); }
        }
        Ok(())
    }

    fn parse_define(&mut self) -> anyhow::Result<()> {
        let name = self.expect_ident()?;
        if !matches!(self.peek(), Token::Newline | Token::Eof) {
            if let Ok(val) = self.parse_expr() {
                self.defines.insert(name, val);
            } else {
                self.skip_to_newline();
            }
        } else {
            self.defines.insert(name, 1);
        }
        Ok(())
    }

    // ─────────────────────────────────────────────────────────────────────────
    // Instruction parsing
    // ─────────────────────────────────────────────────────────────────────────

    fn parse_instruction(&mut self, mnemonic: &str, line: usize) -> anyhow::Result<()> {
        // Special pseudo-instructions
        match mnemonic {
            // PRINT "string"  →  auto-allocates string in .rodata, then O_LOG_S
            // Uses R25 (VM internal scratch) as string pointer register
            "PRINT" => {
                match self.peek().clone() {
                    Token::StringLit(s) => {
                        self.advance();
                        // 1. Allocate string in .rodata with auto-generated label
                        let str_label = format!("__str_{}", self.labels.len());
                        let rodata_offset = self.rodata.len();
                        self.labels.insert(str_label.clone(), (Section::Rodata, rodata_offset));
                        self.rodata.extend_from_slice(s.as_bytes());
                        self.rodata.push(0); // null terminator
                        // 2. Emit L_LEA R25, __str_N  (R25 = VM scratch)
                        let code_offset = self.code.len();
                        self.emit_u32(encode_i(Opcode::D_MovI, 25, 0)); // placeholder
                        self.relocs.push(Reloc {
                            code_offset,
                            label: str_label,
                            kind: RelocKind::LeaRodata,
                            line,
                        });
                        // 3. Emit O_LOG_S R25
                        self.emit_u32(encode_r(Opcode::O_LogS, 25, 0, 0, 0));
                    }
                    tok => bail!("line {}: PRINT expects a string literal, got {:?}", line, tok),
                }
                return Ok(());
            }
            // D_MUL Rdst, Ra, Rb  →  R_FIXMUL (fixed 16.16 multiply)
            "D_MUL" | "D_FIXMUL" => {
                let dst  = self.expect_register()?;
                self.expect_comma()?;
                let src1 = self.expect_register()?;
                self.expect_comma()?;
                let src2 = self.expect_register()?;
                self.emit_u32(encode_r(Opcode::R_FixMul, dst, src1, src2, 0));
                return Ok(());
            }
            // D_DIV Rdst, Ra, Rb  →  R_FIXDIV (fixed 16.16 divide)
            "D_DIV" | "D_FIXDIV" => {
                let dst  = self.expect_register()?;
                self.expect_comma()?;
                let src1 = self.expect_register()?;
                self.expect_comma()?;
                let src2 = self.expect_register()?;
                self.emit_u32(encode_r(Opcode::R_FixDiv, dst, src1, src2, 0));
                return Ok(());
            }
            // D_IMUL/D_IDIV/D_IREM Rdst, Ra, Rb — integer multiply/divide/remainder
            "D_IMUL" => {
                let dst  = self.expect_register()?;
                self.expect_comma()?;
                let src1 = self.expect_register()?;
                self.expect_comma()?;
                let src2 = self.expect_register()?;
                self.emit_u32(encode_r(Opcode::D_Mul, dst, src1, src2, 0));
                return Ok(());
            }
            "D_IDIV" => {
                let dst  = self.expect_register()?;
                self.expect_comma()?;
                let src1 = self.expect_register()?;
                self.expect_comma()?;
                let src2 = self.expect_register()?;
                self.emit_u32(encode_r(Opcode::D_Div, dst, src1, src2, 0));
                return Ok(());
            }
            "D_IREM" => {
                let dst  = self.expect_register()?;
                self.expect_comma()?;
                let src1 = self.expect_register()?;
                self.expect_comma()?;
                let src2 = self.expect_register()?;
                self.emit_u32(encode_r(Opcode::D_Rem, dst, src1, src2, 0));
                return Ok(());
            }
            // D_AND Rdst, Ra, Rb  →  D_And opcode (0x34)
            "D_AND" => {
                let dst  = self.expect_register()?;
                self.expect_comma()?;
                let src1 = self.expect_register()?;
                self.expect_comma()?;
                let src2 = self.expect_register()?;
                self.emit_u32(encode_r(Opcode::D_And, dst, src1, src2, 0));
                return Ok(());
            }
            // D_OR Rdst, Ra, Rb
            "D_OR" => {
                let dst  = self.expect_register()?;
                self.expect_comma()?;
                let src1 = self.expect_register()?;
                self.expect_comma()?;
                let src2 = self.expect_register()?;
                self.emit_u32(encode_r(Opcode::D_Or, dst, src1, src2, 0));
                return Ok(());
            }
            // D_XOR Rdst, Ra, Rb
            "D_XOR" => {
                let dst  = self.expect_register()?;
                self.expect_comma()?;
                let src1 = self.expect_register()?;
                self.expect_comma()?;
                let src2 = self.expect_register()?;
                self.emit_u32(encode_r(Opcode::D_Xor, dst, src1, src2, 0));
                return Ok(());
            }
            // D_SHL Rdst, Rsrc, imm  →  D_Shl (imm in flags[4:0])
            "D_SHL" => {
                let dst = self.expect_register()?;
                self.expect_comma()?;
                let src = self.expect_register()?;
                self.expect_comma()?;
                let imm = self.parse_expr()? as u16 & 0x1F;
                self.emit_u32(encode_r(Opcode::D_Shl, dst, src, 0, imm));
                return Ok(());
            }
            // D_SHR Rdst, Rsrc, imm  →  D_Shr (arithmetic, imm in flags[4:0])
            "D_SHR" => {
                let dst = self.expect_register()?;
                self.expect_comma()?;
                let src = self.expect_register()?;
                self.expect_comma()?;
                let imm = self.parse_expr()? as u16 & 0x1F;
                self.emit_u32(encode_r(Opcode::D_Shr, dst, src, 0, imm));
                return Ok(());
            }
            // Simpler: encode as D_ADD with src2 being an immediate via a scratch approach.
            // We implement it as a true pseudo: two instructions.
            "D_ADD_I" => {
                let dst = self.expect_register()?;
                self.expect_comma()?;
                let imm = self.parse_expr()? as i32;
                // Use R24 (VM internal scratch) to hold immediate
                self.emit_u32(encode_i(Opcode::D_MovI, 24, imm));
                self.emit_u32(encode_r(Opcode::D_Add, dst, dst, 24, 0));
                return Ok(());
            }
            "D_SUB_I" => {
                let dst = self.expect_register()?;
                self.expect_comma()?;
                let imm = self.parse_expr()? as i32;
                self.emit_u32(encode_i(Opcode::D_MovI, 24, imm));
                self.emit_u32(encode_r(Opcode::D_Sub, dst, dst, 24, 0));
                return Ok(());
            }
            // L_LEA Rdst, label  →  load address of a rodata/code label into register
            // Encoded as two D_MOV_I for hi/lo 32-bit halves (placeholder, fixed up later)
            "L_LEA" => {
                let dst = self.expect_register()?;
                self.expect_comma()?;
                match self.peek().clone() {
                    Token::Ident(label) => {
                        self.advance();
                        let code_offset = self.code.len();
                        // Emit placeholder: D_MOV_I R25, hi16  then D_MOV_I Rdst, lo32
                        // For now: single D_MOV_I with placeholder 0 — fixed up in fixup pass
                        // We emit one instruction as placeholder and store reloc
                        self.emit_u32(encode_i(Opcode::D_MovI, dst, 0));
                        self.relocs.push(Reloc {
                            code_offset,
                            label,
                            kind: RelocKind::LeaRodata,
                            line,
                        });
                    }
                    _ => {
                        // Numeric expression — direct address
                        let addr = self.parse_expr()? as i32;
                        self.emit_u32(encode_i(Opcode::D_MovI, dst, addr));
                    }
                }
                return Ok(());
            }
            _ => {}
        }

        let op = lookup_opcode(mnemonic)
            .ok_or_else(|| anyhow!("line {}: unknown opcode '{}'", line, mnemonic))?;

        if is_no_operand(op) {
            self.emit_u32(encode_r(op, 0, 0, 0, 0));
            return Ok(());
        }

        if is_jump_mnemonic(op) {
            let word = self.parse_jump_target(op, line)?;
            self.emit_u32(word);
            return Ok(());
        }

        if is_immediate_mnemonic(op) {
            let dst = self.expect_register()?;
            self.expect_comma()?;
            let imm = self.parse_expr()? as i32;
            self.emit_u32(encode_i(op, dst, imm));
            return Ok(());
        }

        // V_CMP Ra, Rb — compare two registers (no dst, sets flags only)
        if op == Opcode::V_Cmp {
            let src1 = self.expect_register()?;
            self.expect_comma()?;
            let src2 = self.expect_register()?;
            self.emit_u32(encode_r(op, 0, src1, src2, 0));
            return Ok(());
        }

        // O_LOG / O_LOG_S / Im_FB_BLIT / Im_INPUT_RD / T_FRAME_SYN — single reg operand
        if matches!(op,
            Opcode::O_Log | Opcode::O_LogS |
            Opcode::Im_FbBlit | Opcode::Im_FbClear |
            Opcode::Im_InputRd | Opcode::T_FrameSyn |
            Opcode::T_Tick
        ) {
            let reg = self.expect_register()?;
            self.emit_u32(encode_r(op, reg, 0, 0, 0));
            return Ok(());
        }

        // Single-reg operands
        if matches!(op, Opcode::V_Assert | Opcode::V_Null | Opcode::L_IsNull |
                        Opcode::A_Push | Opcode::A_Pop | Opcode::A_Peek |
                        Opcode::A_Dup  | Opcode::A_Depth) {
            let reg = self.expect_register()?;
            self.emit_u32(encode_r(op, reg, reg, 0, 0));
            return Ok(());
        }

        // D_LOAD8/16/32/64 Rdst, Rsrc[, offset]  — Type R with optional offset in flags
        if matches!(op, Opcode::D_Load8 | Opcode::D_Load16 | Opcode::D_Load32 | Opcode::D_Load64) {
            let dst  = self.expect_register()?;
            self.expect_comma()?;
            let src1 = self.expect_register()?;
            let offset = if matches!(self.peek(), Token::Comma) {
                self.advance();
                self.parse_expr()? as u16
            } else { 0 };
            self.emit_u32(encode_r(op, dst, src1, 0, offset));
            return Ok(());
        }

        // D_STORE8/16/32/64 [Raddr, offset], Rsrc — Type R
        if matches!(op, Opcode::D_Store8 | Opcode::D_Store16 | Opcode::D_Store32 | Opcode::D_Store64) {
            let addr = self.expect_register()?;
            self.expect_comma()?;
            let src  = self.expect_register()?;
            let offset = if matches!(self.peek(), Token::Comma) {
                self.advance();
                self.parse_expr()? as u16
            } else { 0 };
            self.emit_u32(encode_r(op, addr, src, 0, offset));
            return Ok(());
        }

        // Default Type R: dst, src1[, src2]
        let dst  = self.expect_register()?;
        self.expect_comma()?;
        let src1 = self.expect_register()?;
        let src2 = if matches!(self.peek(), Token::Comma) {
            self.advance();
            self.expect_register()?
        } else { 0 };
        self.emit_u32(encode_r(op, dst, src1, src2, 0));
        Ok(())
    }

    fn parse_jump_target(&mut self, op: Opcode, line: usize) -> anyhow::Result<u32> {
        match self.peek().clone() {
            Token::Ident(label) => {
                self.advance();
                let instr_offset = self.code.len();
                let placeholder = encode_j(op, 0);
                self.relocs.push(Reloc {
                    code_offset: instr_offset,
                    label,
                    kind: RelocKind::Jump,
                    line,
                });
                Ok(placeholder)
            }
            _ => {
                let offset = self.parse_expr()? as i32;
                Ok(encode_j(op, offset))
            }
        }
    }

    // ─────────────────────────────────────────────────────────────────────────
    // Expression parser
    // ─────────────────────────────────────────────────────────────────────────

    fn parse_expr(&mut self) -> anyhow::Result<i64> {
        self.parse_expr_add()
    }

    fn parse_expr_add(&mut self) -> anyhow::Result<i64> {
        let mut lhs = self.parse_expr_primary()?;
        loop {
            match self.peek() {
                Token::Ident(s) if s == "+" => { self.advance(); lhs += self.parse_expr_primary()?; }
                Token::Ident(s) if s == "-" => { self.advance(); lhs -= self.parse_expr_primary()?; }
                _ => break,
            }
        }
        Ok(lhs)
    }

    fn parse_expr_primary(&mut self) -> anyhow::Result<i64> {
        match self.peek().clone() {
            Token::Integer(n) => { self.advance(); Ok(n) }
            Token::CharLit(c) => { self.advance(); Ok(c as i64) }
            Token::Ident(name) => {
                self.advance();
                if let Some(&v) = self.defines.get(&name) { Ok(v) }
                else { bail!("undefined symbol: '{}'", name) }
            }
            Token::LParen => {
                self.advance();
                let v = self.parse_expr()?;
                if !matches!(self.peek(), Token::RParen) { bail!("expected ')'"); }
                self.advance();
                Ok(v)
            }
            tok => bail!("expected expression, got {:?}", tok),
        }
    }

    // ─────────────────────────────────────────────────────────────────────────
    // Label fixup pass
    // ─────────────────────────────────────────────────────────────────────────

    fn fixup_labels(&mut self, ) -> anyhow::Result<()> {
        // VM memory layout (from memory/mod.rs):
        //   NULL_PAGE_END = 0x1000  ← .rodata loads here
        //   rodata_load   = 0x1000
        //   code_load     = 0x1000 + rodata.len() (aligned to 4)
        let rodata_load: usize = 0x1000;
        let code_load:   usize = rodata_load + align4(self.rodata.len());

        for reloc in &self.relocs {
            let existing = u32::from_le_bytes(
                self.code[reloc.code_offset..reloc.code_offset+4].try_into().unwrap()
            );
            let opcode_byte = (existing >> 24) as u8;

            let word = match reloc.kind {
                RelocKind::Jump => {
                    let (sec, target_off) = self.labels.get(&reloc.label)
                        .ok_or_else(|| anyhow!("line {}: undefined label '{}'", reloc.line, reloc.label))?;
                    let target_vm = match sec {
                        Section::Code   => code_load + target_off,
                        Section::Rodata | Section::Data => rodata_load + target_off,
                        _ => bail!("cannot jump to section {:?}", sec),
                    };
                    let instr_vm = code_load + reloc.code_offset;
                    // delta is relative to instr_pc (PC - 4 in exec_j, i.e. the instruction address).
                    // exec_j computes: target = instr_pc + offset = (PC - 4) + offset
                    // So: offset = target_vm - instr_vm   (no +4 subtraction)
                    let delta = target_vm as i64 - instr_vm as i64;
                    if delta > 0x7F_FFFF || delta < -0x80_0000 {
                        bail!("line {}: jump to '{}' exceeds ±8MB", reloc.line, reloc.label);
                    }
                    ((opcode_byte as u32) << 24) | ((delta as u32) & 0x00FF_FFFF)
                }
                RelocKind::LeaRodata => {
                    let (sec, target_off) = self.labels.get(&reloc.label)
                        .ok_or_else(|| anyhow!("line {}: undefined label '{}'", reloc.line, reloc.label))?;
                    let addr = match sec {
                        Section::Code   => (code_load   + target_off) as i64,
                        Section::Rodata | Section::Data => (rodata_load + target_off) as i64,
                        _ => bail!("cannot take address of section {:?}", sec),
                    };
                    // D_MOV_I Rdst, addr (19-bit signed — sufficient for our test range)
                    let dst = (existing >> 19) & 0x1F;
                    ((opcode_byte as u32) << 24)
                        | (dst << 19)
                        | (addr as u32 & 0x0007_FFFF)
                }
            };
            self.code[reloc.code_offset..reloc.code_offset+4].copy_from_slice(&word.to_le_bytes());
        }
        Ok(())
    }

    // ─────────────────────────────────────────────────────────────────────────
    // Token helpers
    // ─────────────────────────────────────────────────────────────────────────

    fn peek(&self) -> &Token {
        self.tokens.get(self.pos).map(|s| &s.token).unwrap_or(&Token::Eof)
    }
    fn current_line(&self) -> usize {
        self.tokens.get(self.pos).map(|s| s.span.line).unwrap_or(0)
    }
    fn advance(&mut self) -> &Token {
        let tok = self.tokens.get(self.pos).map(|s| &s.token).unwrap_or(&Token::Eof);
        self.pos += 1;
        tok
    }
    fn at_eof(&self) -> bool { matches!(self.peek(), Token::Eof) }
    fn skip_newlines(&mut self) {
        while matches!(self.peek(), Token::Newline) { self.advance(); }
    }
    fn skip_to_newline(&mut self) {
        while !matches!(self.peek(), Token::Newline | Token::Eof) { self.advance(); }
    }
    fn expect_newline(&mut self) -> anyhow::Result<()> {
        match self.peek() {
            Token::Newline | Token::Eof => { self.skip_newlines(); Ok(()) }
            tok => bail!("expected newline, got {:?}", tok),
        }
    }
    fn expect_ident(&mut self) -> anyhow::Result<String> {
        match self.peek().clone() {
            Token::Ident(s)    => { self.advance(); Ok(s) }
            Token::Directive(s)=> { self.advance(); Ok(s) }
            tok => bail!("expected identifier, got {:?}", tok),
        }
    }
    fn expect_register(&mut self) -> anyhow::Result<u8> {
        match self.peek().clone() {
            Token::Register(r) => { self.advance(); Ok(r) }
            tok => bail!("expected register, got {:?}", tok),
        }
    }
    fn expect_comma(&mut self) -> anyhow::Result<()> {
        match self.peek() {
            Token::Comma => { self.advance(); Ok(()) }
            tok => bail!("expected ',', got {:?}", tok),
        }
    }
    fn emit_u32(&mut self, word: u32) {
        self.code.extend_from_slice(&word.to_le_bytes());
    }
}

// ─────────────────────────────────────────────────────────────────────────────
// Helpers
// ─────────────────────────────────────────────────────────────────────────────

fn align4(n: usize) -> usize { (n + 3) & !3 }

// ─────────────────────────────────────────────────────────────────────────────
// Opcode lookup table
// ─────────────────────────────────────────────────────────────────────────────

pub fn lookup_opcode(mnemonic: &str) -> Option<Opcode> {
    match mnemonic {
        "A_PUSH"      => Some(Opcode::A_Push),
        "A_POP"       => Some(Opcode::A_Pop),
        "A_PUSH_I"    => Some(Opcode::A_PushI),
        "A_PEEK"      => Some(Opcode::A_Peek),
        "A_SWAP"      => Some(Opcode::A_Swap),
        "A_DUP"       => Some(Opcode::A_Dup),
        "A_DEPTH"     => Some(Opcode::A_Depth),
        "A_ENTER"     => Some(Opcode::A_Enter),
        "A_LEAVE"     => Some(Opcode::A_Leave),
        "A_ALLOC"     => Some(Opcode::A_Alloc),
        "A_ALLOC_Z"   => Some(Opcode::A_AllocZ),
        "A_FREE"      => Some(Opcode::A_Free),
        "St_NOP"      => Some(Opcode::St_Nop),
        "F_JMP"       => Some(Opcode::F_Jmp),
        "F_JMP_R"     => Some(Opcode::F_JmpR),
        "F_CALL"      => Some(Opcode::F_Call),
        "F_RET"       => Some(Opcode::F_Ret),
        "F_RET_N"     => Some(Opcode::F_RetN),
        "F_JZ"        => Some(Opcode::F_Jz),
        "F_JNZ"       => Some(Opcode::F_Jnz),
        "F_JL"        => Some(Opcode::F_Jl),
        "F_JLE"       => Some(Opcode::F_Jle),
        "F_JG"        => Some(Opcode::F_Jg),
        "F_JGE"       => Some(Opcode::F_Jge),
        "F_LOOP"      => Some(Opcode::F_Loop),
        "F_TRAP"      => Some(Opcode::F_Trap),
        "F_HALT"      => Some(Opcode::F_Halt),
        "F_YIELD"     => Some(Opcode::F_Yield),
        "It_GET_FLAG" => Some(Opcode::It_GetFlag),
        "It_CLR_FLAG" => Some(Opcode::It_ClrFlag),
        "It_TOG_FLAG" => Some(Opcode::It_TogFlag),
        "D_AND"       => Some(Opcode::D_And),
        "D_OR"        => Some(Opcode::D_Or),
        "D_XOR"       => Some(Opcode::D_Xor),
        "D_SHL"       => None, // handled as pseudo-instruction above
        "D_SHR"       => None, // handled as pseudo-instruction above
        "D_MOV"       => Some(Opcode::D_Mov),
        "D_MOV_I"     => Some(Opcode::D_MovI),
        "D_MOV_I64"   => Some(Opcode::D_MovI64),
        "D_XCHG"      => Some(Opcode::D_Xchg),
        "D_LOAD8"     => Some(Opcode::D_Load8),
        "D_LOAD16"    => Some(Opcode::D_Load16),
        "D_LOAD32"    => Some(Opcode::D_Load32),
        "D_LOAD64"    => Some(Opcode::D_Load64),
        "D_STORE8"    => Some(Opcode::D_Store8),
        "D_STORE16"   => Some(Opcode::D_Store16),
        "D_STORE32"   => Some(Opcode::D_Store32),
        "D_STORE64"   => Some(Opcode::D_Store64),
        "D_MEMCPY"    => Some(Opcode::D_Memcpy),
        "D_MEMSET"    => Some(Opcode::D_Memset),
        "D_ADD"       => Some(Opcode::D_Add),
        "D_SUB"       => Some(Opcode::D_Sub),
        "R_I2F"       => Some(Opcode::R_I2F),
        "R_F2I"       => Some(Opcode::R_F2I),
        "R_FIX2F"     => Some(Opcode::R_Fix2F),
        "R_F2FIX"     => Some(Opcode::R_F2Fix),
        "V_CMP"       => Some(Opcode::V_Cmp),
        "V_CMP_I"     => Some(Opcode::V_CmpI),
        "V_EQ"        => Some(Opcode::V_Eq),
        "V_NEQ"       => Some(Opcode::V_Neq),
        "V_LT"        => Some(Opcode::V_Lt),
        "V_LTE"       => Some(Opcode::V_Lte),
        "V_GT"        => Some(Opcode::V_Gt),
        "V_GTE"       => Some(Opcode::V_Gte),
        "V_ASSERT"    => Some(Opcode::V_Assert),
        "V_NULL"      => Some(Opcode::V_Null),
        "O_DUMP_REG"  => Some(Opcode::O_DumpReg),
        "O_LOG"       => Some(Opcode::O_Log),
        "O_LOG_S"     => Some(Opcode::O_LogS),
        "O_TRACE_ON"  => Some(Opcode::O_TraceOn),
        "O_TRACE_OFF" => Some(Opcode::O_TraceOff),
        "O_BREAK"     => Some(Opcode::O_Break),
        "Im_SYSCALL"  => Some(Opcode::Im_Syscall),
        "Im_FFI_CALL" => Some(Opcode::Im_FfiCall),
        "Im_FB_BLIT"  => Some(Opcode::Im_FbBlit),
        "Im_INPUT_RD" => Some(Opcode::Im_InputRd),
        "Im_FILE_RD"  => Some(Opcode::Im_FileRd),
        "Im_FILE_WR"  => Some(Opcode::Im_FileWr),
        "Im_REGISTER_CB" => Some(Opcode::Im_RegisterCb),
        "Im_KEY_QUERY"   => Some(Opcode::Im_KeyQuery),
        "Im_EXIT"     => Some(Opcode::Im_Exit),
        "T_TICK"      => Some(Opcode::T_Tick),
        "T_SLEEP"     => Some(Opcode::T_Sleep),
        "T_FRAME_SYN" => Some(Opcode::T_FrameSyn),
        "_^_NEW_OBJ"  => Some(Opcode::Pos_NewObj),
        "_^_SPAWN"    => Some(Opcode::Pos_Spawn),
        "_^_ARENA_B"  => Some(Opcode::Pos_ArenaB),
        "_^_LOCK"     => Some(Opcode::Pos_Lock),
        "_$_DEL_OBJ"  => Some(Opcode::Neg_DelObj),
        "_$_KILL"     => Some(Opcode::Neg_Kill),
        "_$_ARENA_E"  => Some(Opcode::Neg_ArenaE),
        "_$_UNLOCK"   => Some(Opcode::Neg_Unlock),
        "K_TYPEOF"    => Some(Opcode::K_Typeof),
        "K_IS_A"      => Some(Opcode::K_IsA),
        "Ss_PI"       => Some(Opcode::Ss_Pi),
        "Ss_NULL_T"   => Some(Opcode::Ss_NullT),
        "L_DEREF"     => Some(Opcode::L_Deref),
        "L_DEREF_W"   => Some(Opcode::L_DerefW),
        "L_NULL"      => Some(Opcode::L_Null),
        "L_IS_NULL"   => Some(Opcode::L_IsNull),
        "L_FAR_CALL"  => Some(Opcode::L_FarCall),
        "L_FAR_JMP"   => Some(Opcode::L_FarJmp),
        _ => None,
    }
}

fn is_no_operand(op: Opcode) -> bool {
    matches!(op,
        Opcode::St_Nop | Opcode::F_Ret | Opcode::F_Halt | Opcode::F_Yield |
        Opcode::A_Enter | Opcode::A_Leave | Opcode::A_Swap |
        Opcode::O_TraceOn | Opcode::O_TraceOff | Opcode::O_DumpReg | Opcode::O_Break |
        Opcode::Im_Exit | Opcode::T_Tick
    )
}
