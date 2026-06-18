// tsk-dbg/src/disasm.rs
// Author: Echopraxium with the collaboration of Claude AI
//
// Inline disassembler for tsk-dbg: decodes .tvmx bytecode around the current PC.
// Used by DAP stackTrace / disassemble requests.
//
// Instruction format: 32-bit fixed width.
//   bits [31:24] = opcode byte  ([7:4] category, [3:0] index)
//   bits [23:0]  = operands (Type R / Type I / Type J / Type X)
//
// Type R:  [23:19]=dst [18:14]=src1 [13:9]=src2 [8:0]=flags/imm9
// Type I:  [23:19]=dst [18:14]=src  [13:0]=imm14 (signed)
// Type J:  [23:0] = offset24 (signed, relative to PC+4)
// Type X:  [23:0] = payload (opcode-specific)

use crate::symbols::SymbolTable;

/// One decoded instruction for display.
#[derive(Debug, Clone)]
pub struct DecodedInsn {
    /// Byte address in bytecode
    pub addr:     u64,
    /// Raw 32-bit instruction word
    pub raw:      u32,
    /// Mnemonic string (e.g. "D_Mov R4, R5")
    pub text:     String,
    /// Label at this address (if any)
    pub label:    Option<String>,
}

/// Disassemble `count` instructions starting at `start_addr`.
/// `bytecode` is the full .tvmx payload (after header).
pub fn disassemble(
    bytecode:   &[u8],
    start_addr: u64,
    count:      usize,
    symbols:    &SymbolTable,
) -> Vec<DecodedInsn> {
    let mut result = Vec::with_capacity(count);
    let mut offset = start_addr as usize;

    for _ in 0..count {
        if offset + 4 > bytecode.len() {
            break;
        }

        let word = u32::from_le_bytes([
            bytecode[offset],
            bytecode[offset + 1],
            bytecode[offset + 2],
            bytecode[offset + 3],
        ]);

        let addr  = offset as u64;
        let label = symbols.label_at(addr).map(str::to_owned);
        let text  = decode_insn(word, addr);

        result.push(DecodedInsn { addr, raw: word, text, label });
        offset += 4;
    }

    result
}

/// Disassemble instructions centered around `pc` (± half_window on each side).
pub fn disassemble_around(
    bytecode:    &[u8],
    pc:          u64,
    half_window: usize,
    symbols:     &SymbolTable,
) -> Vec<DecodedInsn> {
    let start = pc.saturating_sub((half_window as u64) * 4);
    disassemble(bytecode, start, half_window * 2 + 1, symbols)
}

// ─────────────────────────────────────────────────────────────────────────────
// Instruction decoder
// ─────────────────────────────────────────────────────────────────────────────

fn decode_insn(word: u32, pc: u64) -> String {
    let opcode = (word >> 24) as u8;
    let cat    = opcode >> 4;
    let idx    = opcode & 0xF;

    // Operand fields (Type R layout — most instructions)
    let dst  = ((word >> 19) & 0x1F) as u8;
    let src1 = ((word >> 14) & 0x1F) as u8;
    let src2 = ((word >>  9) & 0x1F) as u8;
    let imm9 =  (word & 0x1FF) as i16;
    // Type I: imm14 signed
    let imm14 = sign_extend((word & 0x3FFF) as u32, 14);
    // Type J: offset24 signed
    let off24 = sign_extend(word & 0x00FF_FFFF, 24);

    // Register name helper
    let r = reg_name;

    match (cat, idx) {
        // ── A_ Attractor ──────────────────────────────────────────────────────
        (0x0, 0x0) => format!("A_Push    {}", r(src1)),
        (0x0, 0x1) => format!("A_Pop     {}", r(dst)),
        (0x0, 0x2) => format!("A_PushI   #{}", imm14),
        (0x0, 0x3) => format!("A_Peek    {}", r(dst)),
        (0x0, 0x4) => format!("A_Swap"),
        (0x0, 0x5) => format!("A_Dup"),
        (0x0, 0x6) => format!("A_Depth   {}", r(dst)),
        (0x0, 0x8) => format!("A_Enter   #{}", imm14),
        (0x0, 0x9) => format!("A_Leave"),
        (0x0, 0xA) => format!("A_Alloc   {}, {}", r(dst), r(src1)),
        (0x0, 0xD) => format!("A_Free    {}", r(src1)),

        // ── St_ Structure ─────────────────────────────────────────────────────
        (0x1, 0x0) => "St_Nop".into(),

        // ── F_ Flow ───────────────────────────────────────────────────────────
        (0x2, 0x0) => format!("F_Jmp     {:+}  ; → 0x{:04X}", off24, (pc as i64 + 4 + off24) as u64),
        (0x2, 0x1) => format!("F_JmpR    {:+}  ; → 0x{:04X}", imm14, (pc as i64 + 4 + imm14) as u64),
        (0x2, 0x2) => format!("F_Call    {:+}  ; → 0x{:04X}", off24, (pc as i64 + 4 + off24) as u64),
        (0x2, 0x3) => "F_Ret".into(),
        (0x2, 0x4) => format!("F_RetN    #{}", imm14),
        (0x2, 0x5) => format!("F_Jz      {:+}  ; → 0x{:04X}", imm14, (pc as i64 + 4 + imm14) as u64),
        (0x2, 0x6) => format!("F_Jnz     {:+}  ; → 0x{:04X}", imm14, (pc as i64 + 4 + imm14) as u64),
        (0x2, 0x7) => format!("F_Jl      {:+}  ; → 0x{:04X}", imm14, (pc as i64 + 4 + imm14) as u64),
        (0x2, 0x8) => format!("F_Jle     {:+}  ; → 0x{:04X}", imm14, (pc as i64 + 4 + imm14) as u64),
        (0x2, 0x9) => format!("F_Jg      {:+}  ; → 0x{:04X}", imm14, (pc as i64 + 4 + imm14) as u64),
        (0x2, 0xA) => format!("F_Jge     {:+}  ; → 0x{:04X}", imm14, (pc as i64 + 4 + imm14) as u64),
        (0x2, 0xB) => format!("F_Loop    {:+}  ; → 0x{:04X}", imm14, (pc as i64 + 4 + imm14) as u64),
        (0x2, 0xE) => "F_Halt".into(),
        (0x2, 0xF) => "F_Yield".into(),

        // ── It_ Information + bitwise (repurposed) ────────────────────────────
        (0x3, 0x0) => format!("It_DefFlag  #{}", imm14),
        (0x3, 0x1) => format!("It_DefState #{}", imm14),
        (0x3, 0x2) => format!("It_DefEvent #{}", imm14),
        (0x3, 0x3) => format!("It_DefIrq   #{}", imm14),
        (0x3, 0x4) => format!("D_And     {}, {}, {}", r(dst), r(src1), r(src2)),
        (0x3, 0x5) => format!("D_Or      {}, {}, {}", r(dst), r(src1), r(src2)),
        (0x3, 0x6) => format!("D_Xor     {}, {}, {}", r(dst), r(src1), r(src2)),
        (0x3, 0x7) => format!("D_Not     {}, {}", r(dst), r(src1)),
        (0x3, 0x8) => format!("It_GetFlag  {}, #{}", r(dst), imm9),
        (0x3, 0x9) => format!("It_ClrFlag  #{}", imm14),
        (0x3, 0xA) => format!("It_TogFlag  #{}", imm14),
        (0x3, 0xB) => format!("It_SetState #{}", imm14),
        (0x3, 0xC) => format!("It_Emit     #{}", imm14),
        (0x3, 0xD) => format!("It_Subscribe #{}", imm14),
        (0x3, 0xE) => format!("D_Shl     {}, {}, #{}", r(dst), r(src1), word & 0x1F),
        (0x3, 0xF) => format!("D_Shr     {}, {}, #{}", r(dst), r(src1), word & 0x1F),

        // ── D_ Dynamics ───────────────────────────────────────────────────────
        (0x4, 0x0) => format!("D_Mov     {}, {}", r(dst), r(src1)),
        (0x4, 0x1) => format!("D_MovI    {}, #{}", r(dst), imm14),
        (0x4, 0x2) => format!("D_MovI64  {}, #<imm64>", r(dst)),
        (0x4, 0x3) => format!("D_Xchg    {}, {}", r(dst), r(src1)),
        (0x4, 0x4) => format!("D_Load8   {}, [{}+{}]", r(dst), r(src1), imm9),
        (0x4, 0x5) => format!("D_Load16  {}, [{}+{}]", r(dst), r(src1), imm9),
        (0x4, 0x6) => format!("D_Load32  {}, [{}+{}]", r(dst), r(src1), imm9),
        (0x4, 0x7) => format!("D_Load64  {}, [{}+{}]", r(dst), r(src1), imm9),
        (0x4, 0x8) => format!("D_Store8  [{}+{}], {}", r(src1), imm9, r(dst)),
        (0x4, 0x9) => format!("D_Store16 [{}+{}], {}", r(src1), imm9, r(dst)),
        (0x4, 0xA) => format!("D_Store32 [{}+{}], {}", r(src1), imm9, r(dst)),
        (0x4, 0xB) => format!("D_Store64 [{}+{}], {}", r(src1), imm9, r(dst)),
        (0x4, 0xC) => format!("D_Memcpy  {}, {}, {}", r(dst), r(src1), r(src2)),
        (0x4, 0xD) => format!("D_Memset  {}, {}, {}", r(dst), r(src1), r(src2)),
        (0x4, 0xE) => format!("D_Add     {}, {}, {}", r(dst), r(src1), r(src2)),
        (0x4, 0xF) => format!("D_Sub     {}, {}, {}", r(dst), r(src1), r(src2)),

        // ── R_ Representability ───────────────────────────────────────────────
        (0x5, 0x0) => format!("R_I2F     {}, {}", r(dst), r(src1)),
        (0x5, 0x1) => format!("R_F2I     {}, {}", r(dst), r(src1)),
        (0x5, 0xC) => format!("R_Fix2F   {}, {}", r(dst), r(src1)),
        (0x5, 0xD) => format!("R_F2Fix   {}, {}", r(dst), r(src1)),
        (0x5, 0xE) => format!("R_FixMul  {}, {}, {}", r(dst), r(src1), r(src2)),
        (0x5, 0xF) => format!("R_FixDiv  {}, {}, {}", r(dst), r(src1), r(src2)),

        // ── V_ Verifiability ──────────────────────────────────────────────────
        (0x7, 0x0) => format!("V_Cmp     {}, {}", r(src1), r(src2)),
        (0x7, 0x1) => format!("V_CmpI    {}, #{}", r(src1), imm9),
        (0x7, 0x9) => format!("V_Assert  {}", r(src1)),

        // ── O_ Observability ──────────────────────────────────────────────────
        (0x8, 0x0) => "O_DumpReg".into(),
        (0x8, 0x1) => format!("O_DumpStk #{}", imm14),
        (0x8, 0x2) => format!("O_DumpMem {}, #{}", r(src1), imm14),
        (0x8, 0x3) => "O_TraceOn".into(),
        (0x8, 0x4) => "O_TraceOff".into(),
        (0x8, 0x5) => "O_Break".into(),    // DAP breakpoint opcode
        (0x8, 0x6) => format!("O_Watch   {}", r(src1)),
        (0x8, 0x7) => format!("O_Log     {}", r(src1)),
        (0x8, 0x8) => format!("O_LogS    {}", r(src1)),

        // ── Im_ Interoperability ──────────────────────────────────────────────
        (0x9, 0x0) => format!("Im_Syscall  #{}", imm14),
        (0x9, 0x2) => format!("Im_FbBlit   {}, {}, {}", r(src1), r(src2), r(dst)),
        (0x9, 0x3) => "Im_FbClear".into(),
        (0x9, 0x4) => format!("Im_InputRd  {}", r(dst)),
        (0x9, 0x9) => format!("Im_RegisterCb #{}, {}", imm9, r(src1)),
        (0x9, 0xF) => format!("Im_Exit     #{}", imm14),

        // ── T_ Temporality ────────────────────────────────────────────────────
        (0xA, 0x0) => format!("T_Tick    {}", r(dst)),
        (0xA, 0x2) => format!("T_Sleep   #{}", imm14),
        (0xA, 0x6) => format!("T_FrameSyn #{}", imm14),

        // ── _^_ Positive Pole ─────────────────────────────────────────────────
        (0xB, 0xE) => format!("_^_ARENA_B {}, #{}", r(dst), imm14),
        (0xB, 0xF) => format!("_^_ACTIVATE {}", r(src1)),

        // ── _$_ Negative Pole ─────────────────────────────────────────────────
        (0xC, 0xC) => format!("_$_ARENA_E {}", r(src1)),
        (0xC, 0xF) => "Neg_Abort".into(),

        // ── L_ Localizability ─────────────────────────────────────────────────
        (0xF, 0x0) => format!("L_Lea     {}, [{}+{}]", r(dst), r(src1), imm9),
        (0xF, 0x4) => format!("L_Deref   {}, {}", r(dst), r(src1)),
        (0xF, 0xE) => format!("L_FarCall {}", r(src1)),

        // ── Fallback: raw hex ─────────────────────────────────────────────────
        _ => format!("??? 0x{:08X}  ; cat=0x{:X} idx=0x{:X}", word, cat, idx),
    }
}

// ─────────────────────────────────────────────────────────────────────────────
// Helpers
// ─────────────────────────────────────────────────────────────────────────────

fn reg_name(r: u8) -> &'static str {
    match r {
        0  => "R0",  1  => "R1",  2  => "R2",  3  => "R3",
        4  => "R4",  5  => "R5",  6  => "R6",  7  => "R7",
        8  => "R8",  9  => "R9",  10 => "R10", 11 => "R11",
        12 => "R12", 13 => "R13", 14 => "R14", 15 => "R15",
        16 => "R16", 17 => "R17", 18 => "R18", 19 => "R19",
        20 => "R20", 21 => "R21", 22 => "R22", 23 => "R23",
        24 => "R24", 25 => "R25", 26 => "R26", 27 => "R27",
        28 => "FP",  29 => "SP",  30 => "LR",  31 => "PC",
        _  => "??",
    }
}

fn sign_extend(value: u32, bits: u32) -> i64 {
    let shift = 64 - bits;
    ((value as i64) << shift) >> shift
}
