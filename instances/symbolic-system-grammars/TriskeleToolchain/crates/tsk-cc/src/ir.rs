// tsk-cc/src/ir.rs
// Author: Echopraxium with the collaboration of Claude AI
// Version: 0.3.0
//
// LLVM IR subset AST — covers exactly what Wolf3D C89 generates.

// Many fields are part of the AST spec but not yet consumed by the codegen
// (they will be needed for optimization passes and type-checking later).
#![allow(dead_code)]

// ─────────────────────────────────────────────────────────────────────────────
// Types
// ─────────────────────────────────────────────────────────────────────────────

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub enum IrType {
    Void,
    I1,
    I8,
    I16,
    I32,
    I64,
    Ptr,
    Array(usize, Box<IrType>),
    Struct(Vec<IrType>),
    /// Named struct type not yet resolved (forward reference).
    /// Resolved to a concrete Struct by FuncGen::resolve_type via type_defs.
    Named(String),
}

impl IrType {
    pub fn byte_size(&self) -> usize {
        match self {
            IrType::Void          => 0,
            IrType::I1            => 1,
            IrType::I8            => 1,
            IrType::I16           => 2,
            IrType::I32           => 4,
            IrType::I64           => 8,
            IrType::Ptr           => 8,
            IrType::Array(n, t)   => n * t.byte_size(),
            IrType::Struct(fields)=> fields.iter().map(|f| f.byte_size()).sum(),
            IrType::Named(_)      => 8, // conservative fallback; resolved before use
        }
    }
}

// ─────────────────────────────────────────────────────────────────────────────
// Values
// ─────────────────────────────────────────────────────────────────────────────

#[derive(Debug, Clone)]
pub enum Value {
    Reg(String),
    Const(i64),
    Global(String),
    Null,
    Bool(bool),
    Undef,
}

// ─────────────────────────────────────────────────────────────────────────────
// ICmp predicate
// ─────────────────────────────────────────────────────────────────────────────

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum IcmpPred {
    Eq, Ne,
    Slt, Sgt, Sle, Sge,
    Ult, Ugt, Ule, Uge,
}

impl IcmpPred {
    pub fn from_str(s: &str) -> Option<Self> {
        match s {
            "eq"  => Some(Self::Eq),  "ne"  => Some(Self::Ne),
            "slt" => Some(Self::Slt), "sgt" => Some(Self::Sgt),
            "sle" => Some(Self::Sle), "sge" => Some(Self::Sge),
            "ult" => Some(Self::Ult), "ugt" => Some(Self::Ugt),
            "ule" => Some(Self::Ule), "uge" => Some(Self::Uge),
            _ => None,
        }
    }
}

// ─────────────────────────────────────────────────────────────────────────────
// Instructions
// ─────────────────────────────────────────────────────────────────────────────

#[derive(Debug, Clone)]
pub enum Instr {
    BinOp { dst: String, op: BinOpKind, ty: IrType, lhs: Value, rhs: Value },
    ICmp  { dst: String, pred: IcmpPred, ty: IrType, lhs: Value, rhs: Value },
    BrUncond { target: String },
    BrCond { cond: Value, then_bb: String, else_bb: String },
    Switch { cond: Value, default_bb: String, cases: Vec<(i64, String)> },
    Phi { dst: String, ty: IrType, incoming: Vec<(Value, String)> },
    Alloca { dst: String, ty: IrType, align: usize },
    Load   { dst: String, ty: IrType, ptr: Value, align: usize },
    Store  { ty: IrType, val: Value, ptr: Value, align: usize },
    Gep { dst: String, elem_ty: IrType, ptr: Value, indices: Vec<Value> },
    Zext  { dst: String, from_ty: IrType, val: Value, to_ty: IrType },
    Sext  { dst: String, from_ty: IrType, val: Value, to_ty: IrType },
    Trunc { dst: String, from_ty: IrType, val: Value, to_ty: IrType },
    Bitcast  { dst: String, from_ty: IrType, val: Value, to_ty: IrType },
    PtrToInt { dst: String, val: Value, to_ty: IrType },
    IntToPtr { dst: String, val: Value, to_ty: IrType },
    /// select i1 %cond, ty %true_val, ty %false_val
    Select { dst: String, cond: Value, ty: IrType, true_val: Value, false_val: Value },
    /// llvm.abs.* — abs(val): if val < 0 { -val } else { val }
    Abs { dst: String, ty: IrType, val: Value },
    /// llvm.memset — dst_ptr, byte_val, len, is_volatile
    MemSet { dst_ptr: Value, byte_val: Value, len: Value },
    /// llvm.memcpy — dst_ptr, src_ptr, len, is_volatile
    MemCpy { dst_ptr: Value, src_ptr: Value, len: Value },
    /// llvm.va_start.p0(ptr %slot) — store current SP (arg area) into alloca slot.
    /// On Windows x64 ABI with clang -O0, variadic args are pushed on the caller stack
    /// in R0..Rn already (TriskeleVM calling convention mirrors this).
    /// VaStart writes SP+vararg_offset into %slot so the callee can read args from there.
    VaStart { slot: Value },
    Call { dst: Option<String>, ret_ty: IrType, func: Value, args: Vec<(IrType, Value)> },
    Ret { ty: IrType, val: Option<Value> },
    Unreachable,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum BinOpKind {
    Add, Sub, Mul, SDiv, UDiv, SRem, URem,
    Shl, LShr, AShr,
    And, Or, Xor,
}

impl BinOpKind {
    pub fn from_str(s: &str) -> Option<Self> {
        match s {
            "add"  => Some(Self::Add),  "sub"  => Some(Self::Sub),
            "mul"  => Some(Self::Mul),  "sdiv" => Some(Self::SDiv),
            "udiv" => Some(Self::UDiv), "srem" => Some(Self::SRem),
            "urem" => Some(Self::URem), "shl"  => Some(Self::Shl),
            "lshr" => Some(Self::LShr), "ashr" => Some(Self::AShr),
            "and"  => Some(Self::And),  "or"   => Some(Self::Or),
            "xor"  => Some(Self::Xor),
            _ => None,
        }
    }
}

// ─────────────────────────────────────────────────────────────────────────────
// Basic Block
// ─────────────────────────────────────────────────────────────────────────────

#[derive(Debug, Clone)]
pub struct BasicBlock {
    pub label:  String,
    pub instrs: Vec<Instr>,
}

// ─────────────────────────────────────────────────────────────────────────────
// Function
// ─────────────────────────────────────────────────────────────────────────────

#[derive(Debug, Clone)]
pub struct Function {
    pub name:    String,
    pub ret_ty:  IrType,
    pub params:  Vec<(IrType, String)>,
    pub blocks:  Vec<BasicBlock>,
    pub is_decl: bool,
}

// ─────────────────────────────────────────────────────────────────────────────
// Global variable
// ─────────────────────────────────────────────────────────────────────────────

#[derive(Debug, Clone)]
pub struct Global {
    pub name:    String,
    pub ty:      IrType,
    pub mutable: bool,
    pub init:    GlobalInit,
    pub align:   usize,
}

#[derive(Debug, Clone)]
pub enum GlobalInit {
    ZeroInit,
    Integer(i64),
    Undef,
    /// External reference — declared in another object file; no data emitted here.
    External,
    /// Byte array initializer — used for string literals like c"%d\0"
    Bytes(Vec<u8>),
    /// Array of pointers to named globals: [N x ptr] [ptr @a, ptr @b, ...]
    /// Each String is the target symbol name; the linker patches each slot
    /// with the final VM address of that symbol.
    PointerArray(Vec<String>),
    /// Single pointer to a named global: ptr @sym
    /// Used for globals initialized with a ptr to another global.
    PointerTo(String),
}

// ─────────────────────────────────────────────────────────────────────────────
// Module
// ─────────────────────────────────────────────────────────────────────────────

#[derive(Debug, Default)]
pub struct Module {
    pub name:      String,
    /// Named struct type definitions parsed from LLVM IR type declarations.
    /// Key: "struct.actor_t" (without %)  Value: IrType::Struct([field types])
    pub type_defs: std::collections::HashMap<String, IrType>,
    pub globals:   Vec<Global>,
    pub functions: Vec<Function>,
}
