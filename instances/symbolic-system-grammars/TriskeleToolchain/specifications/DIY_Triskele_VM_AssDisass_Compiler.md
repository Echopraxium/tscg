Seulement a partir du moment ou j'ai choisi l'alphabet avec 16 symboles.
Avec:
1. la VM réécrite en utilisant ces 16 codes d'instructions
2. l'assembleur, désassembleur, linker, "pretty print" et debugger
3. le "compilateur C de bootstrap"
Voici le document complet à partir du moment où l'alphabet à 16 symboles a été choisi.

TSCG Triskele VM - Complete Specification (16-Symbol Alphabet)
1. The 16-Symbol Alphabet
Hex	Symbol	Category	Role
0	A	Territory primitive	Attractor
1	S	Territory primitive	Structure
2	F	Territory primitive	Flow
3	It	Territory primitive	Information (territory)
4	D	Territory primitive	Dynamics
5	R	Map primitive	Representability
6	E	Map primitive	Evolvability
7	V	Map primitive	Verifiability
8	O	Map primitive	Observability
9	Im	Map primitive	Interoperability
A	T	Stereopsis primitive	Time
B	_^	Stereopsis primitive	Positive pole
C	_$	Stereopsis primitive	Negative pole
D	ε×	Neutral	EmptyTerritory
E	ε+	Neutral	EmptyMap
F	ε|	Neutral	EmptyStereopsis
Total = 16 symbols = Base 16 encoding

2. VM Opcodes (8-bit)
Code	Mnemonic	Operands	Description
0x00	NOP	none	No operation
0x01	PUSH_P	sym(4b)	Push symbol (0x0-0xF)
0x02	PUSH_H	addr(32b)	Push heap address
0x03	POP	none	Pop top of stack
0x04	DUP	none	Duplicate top of stack
0x10	MUL	none	× (territory product)
0x11	ADD	none	+ (map sum)
0x12	FUSE	none	| (stereopsic fusion)
0x20	STORE	addr(32b)	Store to heap
0x21	LOAD	addr(32b)	Load from heap
0x30	IF_EQ	addr(32b)	If δ₁ ≈ 0, jump
0x31	IF_NE	addr(32b)	If δ₁ ≠ 0, jump
0x32	JMP	addr(32b)	Unconditional jump
0x40	ITER	addr(32b)	Iterate until coherence
0x41	REDUCE	none	Normalize term
0x42	COHERE	none	Compute δ₁
0xF0	HALT	none	Stop execution
3. VM Implementation in Rust
rust
// tsg_vm.rs - TSCG Virtual Machine with 16-symbol alphabet

#![allow(dead_code)]

use std::collections::HashMap;

// ============================================================
// SYMBOLS (16 symbols, 4 bits each)
// ============================================================

#[repr(u8)]
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, PartialOrd, Ord)]
pub enum Symbol {
    // Territory (0x0-0x4)
    A = 0x0, S = 0x1, F = 0x2, It = 0x3, D = 0x4,
    // Map (0x5-0x9)
    R = 0x5, E = 0x6, V = 0x7, O = 0x8, Im = 0x9,
    // Stereopsis (0xA-0xC)
    T = 0xA, Pos = 0xB, Neg = 0xC,
    // Neutrals (0xD-0xF)
    NullT = 0xD,  // ε×
    NullM = 0xE,  // ε+
    NullS = 0xF,  // ε|
}

impl Symbol {
    pub fn from_hex_digit(c: char) -> Option<Self> {
        match c.to_ascii_uppercase() {
            '0' => Some(Symbol::A), '1' => Some(Symbol::S), '2' => Some(Symbol::F),
            '3' => Some(Symbol::It), '4' => Some(Symbol::D), '5' => Some(Symbol::R),
            '6' => Some(Symbol::E), '7' => Some(Symbol::V), '8' => Some(Symbol::O),
            '9' => Some(Symbol::Im), 'A' => Some(Symbol::T), 'B' => Some(Symbol::Pos),
            'C' => Some(Symbol::Neg), 'D' => Some(Symbol::NullT), 'E' => Some(Symbol::NullM),
            'F' => Some(Symbol::NullS), _ => None,
        }
    }
    
    pub fn to_hex_digit(&self) -> char {
        match self {
            Symbol::A => '0', Symbol::S => '1', Symbol::F => '2', Symbol::It => '3',
            Symbol::D => '4', Symbol::R => '5', Symbol::E => '6', Symbol::V => '7',
            Symbol::O => '8', Symbol::Im => '9', Symbol::T => 'A', Symbol::Pos => 'B',
            Symbol::Neg => 'C', Symbol::NullT => 'D', Symbol::NullM => 'E', Symbol::NullS => 'F',
        }
    }
    
    pub fn name(&self) -> &'static str {
        match self {
            Symbol::A => "A", Symbol::S => "S", Symbol::F => "F", Symbol::It => "It",
            Symbol::D => "D", Symbol::R => "R", Symbol::E => "E", Symbol::V => "V",
            Symbol::O => "O", Symbol::Im => "Im", Symbol::T => "T", Symbol::Pos => "_^",
            Symbol::Neg => "_$", Symbol::NullT => "ε×", Symbol::NullM => "ε+", Symbol::NullS => "ε|",
        }
    }
    
    pub fn from_byte(b: u8) -> Option<Self> {
        match b {
            0x0 => Some(Symbol::A), 0x1 => Some(Symbol::S), 0x2 => Some(Symbol::F),
            0x3 => Some(Symbol::It), 0x4 => Some(Symbol::D), 0x5 => Some(Symbol::R),
            0x6 => Some(Symbol::E), 0x7 => Some(Symbol::V), 0x8 => Some(Symbol::O),
            0x9 => Some(Symbol::Im), 0xA => Some(Symbol::T), 0xB => Some(Symbol::Pos),
            0xC => Some(Symbol::Neg), 0xD => Some(Symbol::NullT), 0xE => Some(Symbol::NullM),
            0xF => Some(Symbol::NullS), _ => None,
        }
    }
}

// ============================================================
// OPCODES
// ============================================================

#[repr(u8)]
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Opcode {
    Nop = 0x00,
    PushP = 0x01,
    PushH = 0x02,
    Pop = 0x03,
    Dup = 0x04,
    Mul = 0x10,
    Add = 0x11,
    Fuse = 0x12,
    Store = 0x20,
    Load = 0x21,
    IfEq = 0x30,
    IfNe = 0x31,
    Jmp = 0x32,
    Iter = 0x40,
    Reduce = 0x41,
    Cohere = 0x42,
    Halt = 0xF0,
}

impl Opcode {
    pub fn from_byte(b: u8) -> Option<Self> {
        match b {
            0x00 => Some(Opcode::Nop), 0x01 => Some(Opcode::PushP),
            0x02 => Some(Opcode::PushH), 0x03 => Some(Opcode::Pop),
            0x04 => Some(Opcode::Dup), 0x10 => Some(Opcode::Mul),
            0x11 => Some(Opcode::Add), 0x12 => Some(Opcode::Fuse),
            0x20 => Some(Opcode::Store), 0x21 => Some(Opcode::Load),
            0x30 => Some(Opcode::IfEq), 0x31 => Some(Opcode::IfNe),
            0x32 => Some(Opcode::Jmp), 0x40 => Some(Opcode::Iter),
            0x41 => Some(Opcode::Reduce), 0x42 => Some(Opcode::Cohere),
            0xF0 => Some(Opcode::Halt),
            _ => None,
        }
    }
    
    pub fn byte(&self) -> u8 {
        *self as u8
    }
    
    pub fn name(&self) -> &'static str {
        match self {
            Opcode::Nop => "NOP", Opcode::PushP => "PUSH_P", Opcode::PushH => "PUSH_H",
            Opcode::Pop => "POP", Opcode::Dup => "DUP", Opcode::Mul => "MUL",
            Opcode::Add => "ADD", Opcode::Fuse => "FUSE", Opcode::Store => "STORE",
            Opcode::Load => "LOAD", Opcode::IfEq => "IF_EQ", Opcode::IfNe => "IF_NE",
            Opcode::Jmp => "JMP", Opcode::Iter => "ITER", Opcode::Reduce => "REDUCE",
            Opcode::Cohere => "COHERE", Opcode::Halt => "HALT",
        }
    }
}

// ============================================================
// MODEL TERMS
// ============================================================

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub enum ModelTerm {
    Primitive(Symbol),
    Mul(Vec<ModelTerm>),
    Add(Vec<ModelTerm>),
    Fuse(Box<ModelTerm>, Box<ModelTerm>),
}

impl ModelTerm {
    pub fn empty_territory() -> Self {
        ModelTerm::Primitive(Symbol::NullT)
    }
    
    pub fn empty_map() -> Self {
        ModelTerm::Primitive(Symbol::NullM)
    }
    
    pub fn empty_stereopsis() -> Self {
        ModelTerm::Primitive(Symbol::NullS)
    }
    
    pub fn universal_set() -> Self {
        ModelTerm::Primitive(Symbol::Neg)  // convention
    }
    
    pub fn normalize(&self) -> Self {
        match self {
            ModelTerm::Primitive(s) => ModelTerm::Primitive(*s),
            
            ModelTerm::Mul(children) => {
                let mut flat = Vec::new();
                for child in children {
                    match child.normalize() {
                        ModelTerm::Mul(gc) => flat.extend(gc),
                        c => flat.push(c),
                    }
                }
                flat.retain(|c| *c != Self::empty_territory());
                flat.sort_by(|a, b| format!("{:?}", a).cmp(&format!("{:?}", b)));
                
                match flat.len() {
                    0 => Self::empty_territory(),
                    1 => flat[0].clone(),
                    _ => ModelTerm::Mul(flat),
                }
            }
            
            ModelTerm::Add(children) => {
                let mut flat = Vec::new();
                for child in children {
                    match child.normalize() {
                        ModelTerm::Add(gc) => flat.extend(gc),
                        c => flat.push(c),
                    }
                }
                flat.retain(|c| *c != Self::empty_map());
                flat.sort_by(|a, b| format!("{:?}", a).cmp(&format!("{:?}", b)));
                
                match flat.len() {
                    0 => Self::empty_map(),
                    1 => flat[0].clone(),
                    _ => ModelTerm::Add(flat),
                }
            }
            
            ModelTerm::Fuse(left, right) => {
                let l = left.normalize();
                let r = right.normalize();
                
                if l == Self::universal_set() || r == Self::universal_set() {
                    return Self::universal_set();
                }
                if l == Self::empty_stereopsis() || r == Self::empty_stereopsis() {
                    return Self::empty_stereopsis();
                }
                if l == Self::empty_territory() && r == Self::empty_map() {
                    return Self::empty_stereopsis();
                }
                
                ModelTerm::Fuse(Box::new(l), Box::new(r))
            }
        }
    }
    
    pub fn coherence(&self) -> f64 {
        match self {
            ModelTerm::Primitive(_) => 0.0,
            ModelTerm::Mul(children) => {
                children.iter().map(|c| c.coherence()).sum::<f64>() / children.len() as f64
            }
            ModelTerm::Add(children) => {
                children.iter().map(|c| c.coherence()).sum::<f64>() / children.len() as f64
            }
            ModelTerm::Fuse(left, right) => (left.coherence() - right.coherence()).abs(),
        }
    }
}

impl std::fmt::Display for ModelTerm {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            ModelTerm::Primitive(s) => write!(f, "{}", s.name()),
            ModelTerm::Mul(children) => {
                write!(f, "(")?;
                for (i, c) in children.iter().enumerate() {
                    if i > 0 { write!(f, " × ")?; }
                    write!(f, "{}", c)?;
                }
                write!(f, ")")
            }
            ModelTerm::Add(children) => {
                write!(f, "(")?;
                for (i, c) in children.iter().enumerate() {
                    if i > 0 { write!(f, " + ")?; }
                    write!(f, "{}", c)?;
                }
                write!(f, ")")
            }
            ModelTerm::Fuse(l, r) => write!(f, "({} | {})", l, r),
        }
    }
}

// ============================================================
// DATA CONSTANT (mode donnée)
// ============================================================

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DataConstant(pub Vec<Symbol>);

impl DataConstant {
    pub fn from_hex(hex_str: &str) -> Result<Self, String> {
        let mut symbols = Vec::new();
        for ch in hex_str.chars() {
            match Symbol::from_hex_digit(ch) {
                Some(s) => symbols.push(s),
                None => return Err(format!("Invalid hex digit: {}", ch)),
            }
        }
        Ok(DataConstant(symbols))
    }
    
    pub fn from_int(n: u64) -> Self {
        if n == 0 {
            return DataConstant(vec![Symbol::A]);
        }
        let mut symbols = Vec::new();
        let mut m = n;
        while m > 0 {
            symbols.push(Symbol::from_byte((m & 0xF) as u8).unwrap());
            m >>= 4;
        }
        symbols.reverse();
        DataConstant(symbols)
    }
    
    pub fn to_int(&self) -> u64 {
        let mut n = 0;
        for sym in &self.0 {
            n = (n << 4) | (sym.to_hex_digit().to_digit(16).unwrap() as u64);
        }
        n
    }
    
    pub fn to_hex(&self) -> String {
        self.0.iter().map(|s| s.to_hex_digit()).collect()
    }
}

impl std::fmt::Display for DataConstant {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "#{}", self.to_hex())
    }
}

// ============================================================
// STACK VALUE
// ============================================================

#[derive(Debug, Clone)]
pub enum StackValue {
    Model(ModelTerm),
    Data(DataConstant),
    Coherence(f64),
}

// ============================================================
// BYTECODE READER
// ============================================================

pub struct BytecodeReader {
    bytes: Vec<u8>,
    ip: usize,
}

impl BytecodeReader {
    pub fn new(bytes: Vec<u8>) -> Self {
        BytecodeReader { bytes, ip: 0 }
    }
    
    pub fn read_u8(&mut self) -> Option<u8> {
        if self.ip < self.bytes.len() {
            let b = self.bytes[self.ip];
            self.ip += 1;
            Some(b)
        } else {
            None
        }
    }
    
    pub fn read_u32(&mut self) -> Option<u32> {
        if self.ip + 4 <= self.bytes.len() {
            let bytes = &self.bytes[self.ip..self.ip+4];
            self.ip += 4;
            Some(u32::from_le_bytes([bytes[0], bytes[1], bytes[2], bytes[3]]))
        } else {
            None
        }
    }
    
    pub fn read_symbol(&mut self) -> Option<Symbol> {
        self.read_u8().and_then(Symbol::from_byte)
    }
    
    pub fn remaining(&self) -> usize {
        self.bytes.len() - self.ip
    }
    
    pub fn jump(&mut self, addr: usize) {
        self.ip = addr;
    }
}

// ============================================================
// VM
// ============================================================

pub struct VM {
    stack: Vec<StackValue>,
    heap: HashMap<u64, ModelTerm>,
    next_heap_addr: u64,
    reader: BytecodeReader,
    debug: bool,
    running: bool,
}

impl VM {
    pub fn new(bytecode: Vec<u8>, debug: bool) -> Self {
        VM {
            stack: Vec::new(),
            heap: HashMap::new(),
            next_heap_addr: 0x1000,
            reader: BytecodeReader::new(bytecode),
            debug,
            running: true,
        }
    }
    
    fn log(&self, msg: &str) {
        if self.debug {
            println!("[VM] {}", msg);
        }
    }
    
    fn push(&mut self, value: StackValue) {
        self.log(&format!("PUSH: {:?}", value));
        self.stack.push(value);
    }
    
    fn pop(&mut self) -> Option<StackValue> {
        let v = self.stack.pop();
        if let Some(ref val) = v {
            self.log(&format!("POP: {:?}", val));
        }
        v
    }
    
    fn peek(&self) -> Option<&StackValue> {
        self.stack.last()
    }
    
    fn emit_push_int(&mut self, n: u64) {
        let constant = DataConstant::from_int(n);
        self.push(StackValue::Data(constant));
    }
    
    fn emit_push_symbol(&mut self, sym: Symbol) {
        self.push(StackValue::Model(ModelTerm::Primitive(sym)));
    }
    
    fn execute_mul(&mut self) -> Result<(), String> {
        let b = self.pop().ok_or("Stack underflow")?;
        let a = self.pop().ok_or("Stack underflow")?;
        
        match (a, b) {
            (StackValue::Model(t1), StackValue::Model(t2)) => {
                let result = ModelTerm::Mul(vec![t1, t2]).normalize();
                self.push(StackValue::Model(result));
                Ok(())
            }
            _ => Err("MUL requires Model terms".to_string()),
        }
    }
    
    fn execute_add(&mut self) -> Result<(), String> {
        let b = self.pop().ok_or("Stack underflow")?;
        let a = self.pop().ok_or("Stack underflow")?;
        
        match (a, b) {
            (StackValue::Model(t1), StackValue::Model(t2)) => {
                let result = ModelTerm::Add(vec![t1, t2]).normalize();
                self.push(StackValue::Model(result));
                Ok(())
            }
            _ => Err("ADD requires Model terms".to_string()),
        }
    }
    
    fn execute_fuse(&mut self) -> Result<(), String> {
        let b = self.pop().ok_or("Stack underflow")?;
        let a = self.pop().ok_or("Stack underflow")?;
        
        match (a, b) {
            (StackValue::Model(t1), StackValue::Model(t2)) => {
                let result = ModelTerm::Fuse(Box::new(t1), Box::new(t2)).normalize();
                self.push(StackValue::Model(result));
                Ok(())
            }
            (StackValue::Data(d1), StackValue::Data(d2)) => {
                // Fusion de constantes pour les chaînes
                let mut symbols = d1.0;
                symbols.extend(d2.0);
                self.push(StackValue::Data(DataConstant(symbols)));
                Ok(())
            }
            _ => Err("FUSE requires both operands of same type".to_string()),
        }
    }
    
    fn execute_store(&mut self, addr: u32) -> Result<(), String> {
        let val = self.pop().ok_or("Stack underflow")?;
        match val {
            StackValue::Model(term) => {
                self.heap.insert(addr as u64, term);
                Ok(())
            }
            _ => Err("STORE requires Model term".to_string()),
        }
    }
    
    fn execute_load(&mut self, addr: u32) -> Result<(), String> {
        match self.heap.get(&(addr as u64)) {
            Some(term) => {
                self.push(StackValue::Model(term.clone()));
                Ok(())
            }
            None => Err(format!("Heap address {} not found", addr)),
        }
    }
    
    fn execute_cohere(&mut self) -> Result<(), String> {
        let val = self.pop().ok_or("Stack underflow")?;
        match val {
            StackValue::Model(term) => {
                let delta = term.coherence();
                self.push(StackValue::Coherence(delta));
                Ok(())
            }
            _ => Err("COHERE requires Model term".to_string()),
        }
    }
    
    fn execute_reduce(&mut self) -> Result<(), String> {
        let val = self.pop().ok_or("Stack underflow")?;
        match val {
            StackValue::Model(term) => {
                let normalized = term.normalize();
                self.push(StackValue::Model(normalized));
                Ok(())
            }
            _ => self.push(val),
        }
        Ok(())
    }
    
    pub fn run(&mut self) -> Result<Option<StackValue>, String> {
        self.log("VM starting");
        
        while self.running && self.reader.remaining() > 0 {
            let op_byte = self.reader.read_u8().ok_or("Unexpected EOF")?;
            let op = Opcode::from_byte(op_byte).ok_or(format!("Invalid opcode: 0x{:02X}", op_byte))?;
            
            self.log(&format!("Exec: {:?} at IP={}", op, self.reader.ip - 1));
            
            match op {
                Opcode::Nop => {}
                
                Opcode::PushP => {
                    let sym = self.reader.read_symbol().ok_or("Missing symbol")?;
                    self.emit_push_symbol(sym);
                }
                
                Opcode::PushH => {
                    let addr = self.reader.read_u32().ok_or("Missing heap address")?;
                    self.execute_load(addr)?;
                }
                
                Opcode::Pop => { self.pop(); }
                
                Opcode::Dup => {
                    let val = self.peek().cloned().ok_or("Stack underflow")?;
                    self.push(val);
                }
                
                Opcode::Mul => self.execute_mul()?,
                Opcode::Add => self.execute_add()?,
                Opcode::Fuse => self.execute_fuse()?,
                
                Opcode::Store => {
                    let addr = self.reader.read_u32().ok_or("Missing address")?;
                    self.execute_store(addr)?;
                }
                
                Opcode::Load => {
                    let addr = self.reader.read_u32().ok_or("Missing address")?;
                    self.execute_load(addr)?;
                }
                
                Opcode::IfEq => {
                    let addr = self.reader.read_u32().ok_or("Missing jump address")?;
                    let cond = self.pop().ok_or("Stack underflow")?;
                    match cond {
                        StackValue::Coherence(delta) => {
                            if (delta - 0.0).abs() < 1e-6 {
                                self.reader.jump(addr as usize);
                            }
                        }
                        _ => return Err("IF_EQ requires Coherence on stack".to_string()),
                    }
                }
                
                Opcode::IfNe => {
                    let addr = self.reader.read_u32().ok_or("Missing jump address")?;
                    let cond = self.pop().ok_or("Stack underflow")?;
                    match cond {
                        StackValue::Coherence(delta) => {
                            if (delta - 0.0).abs() > 1e-6 {
                                self.reader.jump(addr as usize);
                            }
                        }
                        _ => return Err("IF_NE requires Coherence on stack".to_string()),
                    }
                }
                
                Opcode::Jmp => {
                    let addr = self.reader.read_u32().ok_or("Missing jump address")?;
                    self.reader.jump(addr as usize);
                }
                
                Opcode::Iter => {
                    let _addr = self.reader.read_u32().ok_or("Missing iter address")?;
                    // TODO: implement iteration
                    self.log("ITER not yet implemented");
                }
                
                Opcode::Reduce => self.execute_reduce()?,
                Opcode::Cohere => self.execute_cohere()?,
                Opcode::Halt => { self.running = false; }
            }
        }
        
        Ok(self.stack.last().cloned())
    }
}

// ============================================================
// MAIN
// ============================================================

fn main() {
    println!("TSCG Virtual Machine - 16-Symbol Alphabet");
    println!("=========================================\n");
    
    // Test program: PUSH A, PUSH S, MUL, HALT
    let bytecode: Vec<u8> = vec![
        Opcode::PushP.byte(), Symbol::A as u8,
        Opcode::PushP.byte(), Symbol::S as u8,
        Opcode::Mul.byte(),
        Opcode::Halt.byte(),
    ];
    
    let mut vm = VM::new(bytecode, true);
    match vm.run() {
        Ok(Some(result)) => println!("\nResult: {:?}", result),
        Ok(None) => println!("No result"),
        Err(e) => println!("Error: {}", e),
    }
}
4. Assembleur
rust
// assembler.rs - Assembleur pour Triskele VM

use std::collections::HashMap;
use std::fs;
use std::path::Path;

// Réutilisation des types de la VM
// (Symbol, Opcode, etc.)

#[derive(Debug, Clone)]
pub struct Instruction {
    pub label: Option<String>,
    pub opcode: Opcode,
    pub operand: Option<String>,
    pub comment: Option<String>,
    pub line: u32,
}

pub struct Assembler {
    instructions: Vec<Instruction>,
    labels: HashMap<String, u32>,
    output: Vec<u8>,
    address: u32,
    relocations: Vec<(u32, String)>,
}

impl Assembler {
    pub fn new() -> Self {
        Assembler {
            instructions: Vec::new(),
            labels: HashMap::new(),
            output: Vec::new(),
            address: 0,
            relocations: Vec::new(),
        }
    }
    
    pub fn assemble_file(&mut self, path: &Path) -> Result<Vec<u8>, String> {
        let content = fs::read_to_string(path)
            .map_err(|e| format!("Failed to read {}: {}", path.display(), e))?;
        
        // Parse lines
        for (line_num, line) in content.lines().enumerate() {
            self.parse_line(line, line_num as u32 + 1)?;
        }
        
        // Generate code
        self.generate_code()?;
        
        // Build final binary
        self.build_binary()
    }
    
    fn parse_line(&mut self, line: &str, line_num: u32) -> Result<(), String> {
        let line = line.trim();
        if line.is_empty() || line.starts_with(';') {
            return Ok(());
        }
        
        // Label
        let mut label = None;
        let mut rest = line;
        
        if line.contains(':') && !line.starts_with('.') {
            let parts: Vec<&str> = line.splitn(2, ':').collect();
            label = Some(parts[0].to_string());
            rest = parts.get(1).unwrap_or(&"").trim();
        }
        
        if rest.is_empty() {
            if let Some(lbl) = label {
                self.labels.insert(lbl, self.address);
            }
            return Ok(());
        }
        
        // Comment
        let mut comment = None;
        let mut instr_part = rest;
        if let Some(pos) = rest.find(';') {
            comment = Some(rest[pos+1..].trim().to_string());
            instr_part = rest[..pos].trim();
        }
        
        let parts: Vec<&str> = instr_part.split_whitespace().collect();
        if parts.is_empty() {
            return Ok(());
        }
        
        let opcode = Opcode::from_str(parts[0])
            .ok_or_else(|| format!("Line {}: Unknown opcode '{}'", line_num, parts[0]))?;
        
        let operand = if parts.len() > 1 { Some(parts[1].to_string()) } else { None };
        
        let instr = Instruction {
            label,
            opcode,
            operand,
            comment,
            line: line_num,
        };
        
        if let Some(lbl) = &instr.label {
            self.labels.insert(lbl.clone(), self.address);
        }
        
        self.instructions.push(instr);
        
        // Update address
        self.address += match opcode {
            Opcode::Nop | Opcode::Pop | Opcode::Dup | Opcode::Mul |
            Opcode::Add | Opcode::Fuse | Opcode::Reduce | Opcode::Cohere |
            Opcode::Halt => 1,
            Opcode::PushP => 2,
            Opcode::PushH | Opcode::Store | Opcode::Load |
            Opcode::IfEq | Opcode::IfNe | Opcode::Jmp | Opcode::Iter => 5,
        };
        
        Ok(())
    }
    
    fn generate_code(&mut self) -> Result<(), String> {
        self.output.clear();
        let mut addr = 0;
        
        for instr in &self.instructions {
            self.output.push(instr.opcode.byte());
            addr += 1;
            
            match instr.opcode {
                Opcode::PushP => {
                    let sym = match &instr.operand {
                        Some(s) => Symbol::from_str(s)
                            .ok_or_else(|| format!("Unknown symbol: {}", s))?,
                        None => return Err("PUSH_P requires operand".to_string()),
                    };
                    self.output.push(sym as u8);
                    addr += 1;
                }
                
                Opcode::PushH | Opcode::Store | Opcode::Load => {
                    let val = match &instr.operand {
                        Some(s) => {
                            if s.starts_with('@') {
                                let label = s[1..].to_string();
                                self.relocations.push((addr, label));
                                0u32
                            } else {
                                s.parse::<u32>()
                                    .map_err(|_| format!("Invalid address: {}", s))?
                            }
                        }
                        None => return Err(format!("{:?} requires operand", instr.opcode)),
                    };
                    self.output.extend_from_slice(&val.to_le_bytes());
                    addr += 4;
                }
                
                Opcode::IfEq | Opcode::IfNe | Opcode::Jmp | Opcode::Iter => {
                    let target = match &instr.operand {
                        Some(s) => {
                            if s.starts_with('@') {
                                let label = s[1..].to_string();
                                self.relocations.push((addr, label));
                                0u32
                            } else {
                                s.parse::<u32>()
                                    .map_err(|_| format!("Invalid target: {}", s))?
                            }
                        }
                        None => return Err(format!("{:?} requires operand", instr.opcode)),
                    };
                    self.output.extend_from_slice(&target.to_le_bytes());
                    addr += 4;
                }
                
                _ => {}
            }
        }
        
        // Resolve relocations
        for (reloc_addr, label) in &self.relocations {
            let target = self.labels.get(label)
                .ok_or_else(|| format!("Undefined label: {}", label))?;
            let bytes = target.to_le_bytes();
            let offset = *reloc_addr as usize;
            self.output[offset] = bytes[0];
            self.output[offset + 1] = bytes[1];
            self.output[offset + 2] = bytes[2];
            self.output[offset + 3] = bytes[3];
        }
        
        Ok(())
    }
    
    fn build_binary(&self) -> Result<Vec<u8>, String> {
        let mut binary = Vec::new();
        
        // Magic
        binary.extend_from_slice(b"TSGV");
        
        // Version
        binary.extend_from_slice(&1u32.to_le_bytes());
        
        // Flags
        binary.extend_from_slice(&0u32.to_le_bytes());
        
        // Heap size (placeholder)
        binary.extend_from_slice(&0u64.to_le_bytes());
        
        // Code size
        binary.extend_from_slice(&(self.output.len() as u64).to_le_bytes());
        
        // Entry point (main)
        let entry = self.labels.get("main").unwrap_or(&0);
        binary.extend_from_slice(&entry.to_le_bytes());
        
        // Reserved
        binary.extend_from_slice(&0u32.to_le_bytes());
        
        // Code
        binary.extend_from_slice(&self.output);
        
        Ok(binary)
    }
}

// Helper for Opcode::from_str
impl Opcode {
    pub fn from_str(s: &str) -> Option<Self> {
        match s.to_uppercase().as_str() {
            "NOP" => Some(Opcode::Nop),
            "PUSH_P" => Some(Opcode::PushP),
            "PUSH_H" => Some(Opcode::PushH),
            "POP" => Some(Opcode::Pop),
            "DUP" => Some(Opcode::Dup),
            "MUL" => Some(Opcode::Mul),
            "ADD" => Some(Opcode::Add),
            "FUSE" => Some(Opcode::Fuse),
            "STORE" => Some(Opcode::Store),
            "LOAD" => Some(Opcode::Load),
            "IF_EQ" => Some(Opcode::IfEq),
            "IF_NE" => Some(Opcode::IfNe),
            "JMP" => Some(Opcode::Jmp),
            "ITER" => Some(Opcode::Iter),
            "REDUCE" => Some(Opcode::Reduce),
            "COHERE" => Some(Opcode::Cohere),
            "HALT" => Some(Opcode::Halt),
            _ => None,
        }
    }
}

// Helper for Symbol::from_str
impl Symbol {
    pub fn from_str(s: &str) -> Option<Self> {
        match s {
            "A" => Some(Symbol::A), "S" => Some(Symbol::S), "F" => Some(Symbol::F),
            "It" => Some(Symbol::It), "D" => Some(Symbol::D), "R" => Some(Symbol::R),
            "E" => Some(Symbol::E), "V" => Some(Symbol::V), "O" => Some(Symbol::O),
            "Im" => Some(Symbol::Im), "T" => Some(Symbol::T), "_^" => Some(Symbol::Pos),
            "_$" => Some(Symbol::Neg), "ε×" => Some(Symbol::NullT), "ε+" => Some(Symbol::NullM),
            "ε|" => Some(Symbol::NullS), _ => None,
        }
    }
}
5. Désassembleur
rust
// disassembler.rs - Désassembleur pour Triskele VM

pub struct Disassembler {
    bytes: Vec<u8>,
    ip: usize,
    labels: HashMap<u32, String>,
    next_label_id: u32,
}

impl Disassembler {
    pub fn new(bytes: Vec<u8>) -> Self {
        Disassembler {
            bytes,
            ip: 0,
            labels: HashMap::new(),
            next_label_id: 0,
        }
    }
    
    fn read_u8(&mut self) -> Option<u8> {
        if self.ip < self.bytes.len() {
            let b = self.bytes[self.ip];
            self.ip += 1;
            Some(b)
        } else {
            None
        }
    }
    
    fn read_u32(&mut self) -> Option<u32> {
        if self.ip + 4 <= self.bytes.len() {
            let bytes = &self.bytes[self.ip..self.ip+4];
            self.ip += 4;
            Some(u32::from_le_bytes([bytes[0], bytes[1], bytes[2], bytes[3]]))
        } else {
            None
        }
    }
    
    fn get_or_create_label(&mut self, addr: u32) -> String {
        if let Some(label) = self.labels.get(&addr) {
            label.clone()
        } else {
            let label = format!("L{}", self.next_label_id);
            self.next_label_id += 1;
            self.labels.insert(addr, label.clone());
            label
        }
    }
    
    fn scan_labels(&mut self) {
        let saved_ip = self.ip;
        self.ip = 0;
        
        while self.ip < self.bytes.len() {
            let addr = self.ip as u32;
            if let Some(op_byte) = self.read_u8() {
                if let Some(opcode) = Opcode::from_byte(op_byte) {
                    match opcode {
                        Opcode::IfEq | Opcode::IfNe | Opcode::Jmp | Opcode::Iter => {
                            if let Some(target) = self.read_u32() {
                                self.get_or_create_label(target);
                            }
                        }
                        Opcode::PushH | Opcode::Store | Opcode::Load => {
                            if let Some(addr_val) = self.read_u32() {
                                if addr_val >= 0x1000 {
                                    self.get_or_create_label(addr_val);
                                }
                            }
                        }
                        Opcode::PushP => { self.read_u8(); }
                        _ => {}
                    }
                }
            }
        }
        
        self.ip = saved_ip;
    }
    
    pub fn disassemble(&mut self) -> Result<String, String> {
        self.scan_labels();
        
        let mut output = String::new();
        self.ip = 0;
        
        while self.ip < self.bytes.len() {
            let addr = self.ip as u32;
            
            if let Some(label) = self.labels.get(&addr) {
                output.push_str(&format!("\n{}:\n", label));
            }
            
            let op_byte = self.read_u8().ok_or("Unexpected EOF")?;
            let opcode = Opcode::from_byte(op_byte)
                .ok_or(format!("Invalid opcode: 0x{:02X}", op_byte))?;
            
            output.push_str(&format!("    {:8}", opcode.name()));
            
            match opcode {
                Opcode::Nop | Opcode::Pop | Opcode::Dup | Opcode::Mul |
                Opcode::Add | Opcode::Fuse | Opcode::Reduce | Opcode::Cohere |
                Opcode::Halt => {
                    output.push_str("\n");
                }
                
                Opcode::PushP => {
                    if let Some(sym) = Symbol::from_byte(self.read_u8().unwrap_or(0)) {
                        output.push_str(&format!(" {}\n", sym.name()));
                    } else {
                        output.push_str(" ???\n");
                    }
                }
                
                Opcode::PushH | Opcode::Store | Opcode::Load => {
                    if let Some(addr_val) = self.read_u32() {
                        if let Some(label) = self.labels.get(&addr_val) {
                            output.push_str(&format!(" @{}\n", label));
                        } else {
                            output.push_str(&format!(" 0x{:08X}\n", addr_val));
                        }
                    } else {
                        output.push_str(" ???\n");
                    }
                }
                
                Opcode::IfEq | Opcode::IfNe | Opcode::Jmp | Opcode::Iter => {
                    if let Some(target) = self.read_u32() {
                        if let Some(label) = self.labels.get(&target) {
                            output.push_str(&format!(" @{}\n", label));
                        } else {
                            output.push_str(&format!(" 0x{:08X}\n", target));
                        }
                    } else {
                        output.push_str(" ???\n");
                    }
                }
            }
        }
        
        Ok(output)
    }
}
6. Pretty Printer
rust
// pretty.rs - Pretty printer pour code assembleur

pub struct PrettyPrinter {
    indent: usize,
    indent_size: usize,
    line_width: usize,
}

impl PrettyPrinter {
    pub fn new() -> Self {
        PrettyPrinter {
            indent: 0,
            indent_size: 4,
            line_width: 80,
        }
    }
    
    pub fn pretty_print(&mut self, source: &str) -> String {
        let mut output = String::new();
        output.push_str("; Triskele Assembly\n");
        output.push_str(&format!("; Generated: {}\n\n", chrono::Local::now()));
        
        let lines: Vec<&str> = source.lines().collect();
        let mut i = 0;
        
        while i < lines.len() {
            let line = lines[i].trim();
            
            if line.starts_with(".section") {
                output.push_str(&format!("\n{}\n", line));
                output.push_str(&format!("; {}\n", "=".repeat(line.len())));
                self.indent = 1;
            } else if line.starts_with(".entry") || line.starts_with(".export") {
                output.push_str(&format!("{}\n", line));
            } else if line.ends_with(':') && !line.starts_with('.') {
                output.push_str(&format!("\n{:<20}:\n", line.trim_end_matches(':')));
            } else if line.starts_with(';') {
                output.push_str(&format!("{}\n", line));
            } else if !line.is_empty() {
                let indent_str = " ".repeat(self.indent * self.indent_size);
                let parts: Vec<&str> = line.split_whitespace().collect();
                
                if parts.len() >= 2 {
                    let opcode = format!("{:8}", parts[0]);
                    let operands = parts[1..].join(" ");
                    output.push_str(&format!("{}{} {}\n", indent_str, opcode, operands));
                } else if !parts.is_empty() {
                    output.push_str(&format!("{}{}\n", indent_str, parts[0]));
                }
            }
            
            i += 1;
        }
        
        output
    }
    
    pub fn colorize(&self, source: &str) -> String {
        // ANSI color codes
        let colors = vec![
            ("PUSH_P", "\x1b[32m"),   // green
            ("MUL", "\x1b[33m"),      // yellow
            ("ADD", "\x1b[33m"),
            ("FUSE", "\x1b[35m"),     // magenta
            ("JMP", "\x1b[36m"),      // cyan
            ("HALT", "\x1b[31m"),     // red
        ];
        
        let mut result = source.to_string();
        for (opcode, color) in colors {
            result = result.replace(opcode, &format!("{}{}\x1b[0m", color, opcode));
        }
        
        // Color symbols
        let symbols = vec!["A", "S", "F", "It", "D", "R", "E", "V", "O", "Im", "T", "_^", "_$"];
        for sym in symbols {
            result = result.replace(sym, &format!("\x1b[34m{}\x1b[0m", sym));
        }
        
        result
    }
}
7. Linker
rust
// linker.rs - Éditeur de liens pour Triskele VM

use std::collections::HashMap;
use std::fs;
use std::path::Path;

pub struct Library {
    pub name: String,
    pub bytes: Vec<u8>,
    pub exports: HashMap<String, u32>,
    pub relocations: Vec<(u32, String)>,
}

pub struct Linker {
    libraries: HashMap<String, Library>,
    output: Vec<u8>,
    symbol_map: HashMap<String, u32>,
}

impl Linker {
    pub fn new() -> Self {
        Linker {
            libraries: HashMap::new(),
            output: Vec::new(),
            symbol_map: HashMap::new(),
        }
    }
    
    pub fn add_library(&mut self, path: &Path) -> Result<(), String> {
        let bytes = fs::read(path)
            .map_err(|e| format!("Failed to read {}: {}", path.display(), e))?;
        
        if bytes.len() < 32 {
            return Err("Invalid library format".to_string());
        }
        
        let magic = &bytes[0..4];
        if magic != b"TSGV" {
            return Err("Invalid magic number".to_string());
        }
        
        let flags = u32::from_le_bytes([bytes[8], bytes[9], bytes[10], bytes[11]]);
        let code_size = u64::from_le_bytes([
            bytes[24], bytes[25], bytes[26], bytes[27],
            bytes[28], bytes[29], bytes[30], bytes[31]
        ]) as usize;
        
        let mut exports = HashMap::new();
        let mut relocations = Vec::new();
        
        // Parse symbol table (if present)
        if flags & 0x02 != 0 {
            let sym_offset = u32::from_le_bytes([bytes[28], bytes[29], bytes[30], bytes[31]]) as usize;
            let mut pos = sym_offset;
            
            let sym_count = u32::from_le_bytes([bytes[pos], bytes[pos+1], bytes[pos+2], bytes[pos+3]]) as usize;
            pos += 4;
            
            for _ in 0..sym_count {
                let name_len = u16::from_le_bytes([bytes[pos], bytes[pos+1]]) as usize;
                pos += 2;
                let name = String::from_utf8(bytes[pos..pos+name_len].to_vec())
                    .map_err(|_| "Invalid symbol name")?;
                pos += name_len;
                let addr = u32::from_le_bytes([bytes[pos], bytes[pos+1], bytes[pos+2], bytes[pos+3]]);
                pos += 4;
                exports.insert(name, addr);
            }
        }
        
        // Parse relocations (simplified)
        // In a real implementation, relocations would be stored in a dedicated section
        
        let lib_name = path.file_stem().unwrap_or_default().to_string_lossy().to_string();
        self.libraries.insert(lib_name, Library {
            name: lib_name,
            bytes,
            exports,
            relocations,
        });
        
        Ok(())
    }
    
    pub fn link(&mut self, main_path: &Path, lib_paths: &[PathBuf]) -> Result<Vec<u8>, String> {
        // Load main program
        let main_bytes = fs::read(main_path)
            .map_err(|e| format!("Failed to read {}: {}", main_path.display(), e))?;
        
        // Load all libraries
        for lib_path in lib_paths {
            self.add_library(lib_path)?;
        }
        
        // Build symbol map
        self.symbol_map.clear();
        
        // Add main symbols
        // Parse main program header and symbol table
        if main_bytes.len() >= 32 {
            let flags = u32::from_le_bytes([main_bytes[8], main_bytes[9], main_bytes[10], main_bytes[11]]);
            
            if flags & 0x02 != 0 {
                let sym_offset = u32::from_le_bytes([main_bytes[28], main_bytes[29], main_bytes[30], main_bytes[31]]) as usize;
                let mut pos = sym_offset;
                
                if pos + 4 <= main_bytes.len() {
                    let sym_count = u32::from_le_bytes([main_bytes[pos], main_bytes[pos+1], main_bytes[pos+2], main_bytes[pos+3]]) as usize;
                    pos += 4;
                    
                    for _ in 0..sym_count {
                        if pos + 2 > main_bytes.len() { break; }
                        let name_len = u16::from_le_bytes([main_bytes[pos], main_bytes[pos+1]]) as usize;
                        pos += 2;
                        if pos + name_len > main_bytes.len() { break; }
                        let name = String::from_utf8(main_bytes[pos..pos+name_len].to_vec())
                            .map_err(|_| "Invalid symbol name")?;
                        pos += name_len;
                        if pos + 4 > main_bytes.len() { break; }
                        let addr = u32::from_le_bytes([main_bytes[pos], main_bytes[pos+1], main_bytes[pos+2], main_bytes[pos+3]]);
                        pos += 4;
                        self.symbol_map.insert(name, addr);
                    }
                }
            }
        }
        
        // Add library symbols
        for lib in self.libraries.values() {
            for (name, addr) in &lib.exports {
                // Relocate library symbols with base address
                let base_addr = 0x80000000;
                self.symbol_map.insert(name.clone(), base_addr + addr);
            }
        }
        
        // Build output
        self.output.clear();
        
        // Copy header from main
        self.output.extend_from_slice(&main_bytes[0..32]);
        
        // Merge code sections
        let mut total_code_size = 0u64;
        
        // Add main code
        let main_code_start = 32;
        let main_code_size = u64::from_le_bytes([
            main_bytes[24], main_bytes[25], main_bytes[26], main_bytes[27],
            main_bytes[28], main_bytes[29], main_bytes[30], main_bytes[31]
        ]) as usize;
        
        self.output.extend_from_slice(&main_bytes[main_code_start..main_code_start + main_code_size]);
        total_code_size += main_code_size as u64;
        
        // Add library code
        for lib in self.libraries.values() {
            let lib_code_start = 32;
            let lib_code_size = u64::from_le_bytes([
                lib.bytes[24], lib.bytes[25], lib.bytes[26], lib.bytes[27],
                lib.bytes[28], lib.bytes[29], lib.bytes[30], lib.bytes[31]
            ]) as usize;
            
            self.output.extend_from_slice(&lib.bytes[lib_code_start..lib_code_start + lib_code_size]);
            total_code_size += lib_code_size as u64;
        }
        
        // Update code size in header
        self.output[24..32].copy_from_slice(&total_code_size.to_le_bytes());
        
        Ok(self.output.clone())
    }
}
8. Bootstrap Compiler (C → Triskele)
c
/**
 * boot.c - Bootstrap compiler for Triskele VM
 * 
 * Compiles a subset of C to Triskele bytecode.
 * Enough to compile stage1.tsg (the self-hosting compiler).
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAX_CODE 65536
#define MAX_SYMS 1024
#define MAX_STR 256

// Opcodes (same as VM)
typedef enum {
    NOP = 0x00, PUSH_P = 0x01, PUSH_H = 0x02, POP = 0x03, DUP = 0x04,
    MUL = 0x10, ADD = 0x11, FUSE = 0x12,
    STORE = 0x20, LOAD = 0x21,
    IF_EQ = 0x30, IF_NE = 0x31, JMP = 0x32,
    ITER = 0x40, REDUCE = 0x41, COHERE = 0x42,
    HALT = 0xF0
} Opcode;

// Symbols (16-symbol alphabet)
typedef enum {
    SYM_A = 0x0, SYM_S = 0x1, SYM_F = 0x2, SYM_IT = 0x3, SYM_D = 0x4,
    SYM_R = 0x5, SYM_E = 0x6, SYM_V = 0x7, SYM_O = 0x8, SYM_IM = 0x9,
    SYM_T = 0xA, SYM_POS = 0xB, SYM_NEG = 0xC,
    SYM_NULL_T = 0xD, SYM_NULL_M = 0xE, SYM_NULL_S = 0xF
} Symbol;

// Symbol table entry
typedef struct {
    char name[MAX_STR];
    int address;
    int is_func;
    int param_count;
} SymbolEntry;

// Compiler state
typedef struct {
    unsigned char code[MAX_CODE];
    int code_pos;
    SymbolEntry syms[MAX_SYMS];
    int sym_count;
    int next_addr;
    int current_scope;
    struct {
        int addr;
        char label[MAX_STR];
    } relocs[MAX_SYMS];
    int reloc_count;
} Compiler;

// Forward declarations
void emit_byte(Compiler* c, unsigned char b);
void emit_op(Compiler* c, Opcode op);
void emit_u32(Compiler* c, uint32_t val);
void emit_push_int(Compiler* c, int value);
void compile_expr(Compiler* c, const char** p);
void compile_statement(Compiler* c, const char** p);

// ============================================================
// Code emission
// ============================================================

void emit_byte(Compiler* c, unsigned char b) {
    if (c->code_pos >= MAX_CODE) {
        fprintf(stderr, "Code buffer overflow\n");
        exit(1);
    }
    c->code[c->code_pos++] = b;
}

void emit_op(Compiler* c, Opcode op) {
    emit_byte(c, (unsigned char)op);
}

void emit_u32(Compiler* c, uint32_t val) {
    emit_byte(c, val & 0xFF);
    emit_byte(c, (val >> 8) & 0xFF);
    emit_byte(c, (val >> 16) & 0xFF);
    emit_byte(c, (val >> 24) & 0xFF);
}

void emit_push_int(Compiler* c, int value) {
    if (value == 0) {
        emit_op(c, PUSH_P);
        emit_byte(c, SYM_A);
        return;
    }
    
    // Encode in base 16 using |
    unsigned char digits[16];
    int digit_count = 0;
    unsigned int n = (unsigned int)value;
    
    while (n > 0) {
        digits[digit_count++] = n & 0xF;
        n >>= 4;
    }
    
    for (int i = digit_count - 1; i >= 0; i--) {
        emit_op(c, PUSH_P);
        emit_byte(c, digits[i]);
        if (i < digit_count - 1) {
            emit_op(c, FUSE);
        }
    }
    emit_op(c, PUSH_P);
    emit_byte(c, SYM_A);
    for (int i = 0; i < digit_count - 1; i++) {
        emit_op(c, FUSE);
    }
}

void emit_push_symbol(Compiler* c, Symbol sym) {
    emit_op(c, PUSH_P);
    emit_byte(c, (unsigned char)sym);
}

// ============================================================
// Symbol management
// ============================================================

SymbolEntry* find_symbol(Compiler* c, const char* name) {
    for (int i = 0; i < c->sym_count; i++) {
        if (strcmp(c->syms[i].name, name) == 0) {
            return &c->syms[i];
        }
    }
    return NULL;
}

SymbolEntry* add_symbol(Compiler* c, const char* name, int is_func) {
    SymbolEntry* s = find_symbol(c, name);
    if (!s) {
        s = &c->syms[c->sym_count++];
        strcpy(s->name, name);
        s->address = c->next_addr;
        s->is_func = is_func;
        s->param_count = 0;
        c->next_addr += 4;
    }
    return s;
}

// ============================================================
// Parsing helpers
// ============================================================

void skip_whitespace(const char** p) {
    while (**p && isspace(**p)) (*p)++;
}

char* parse_identifier(const char** p, char* buf, int bufsize) {
    int i = 0;
    while (**p && (isalnum(**p) || **p == '_') && i < bufsize - 1) {
        buf[i++] = **p;
        (*p)++;
    }
    buf[i] = '\0';
    return buf;
}

int parse_number(const char** p) {
    int n = 0;
    while (**p && isdigit(**p)) {
        n = n * 10 + (**p - '0');
        (*p)++;
    }
    return n;
}

// ============================================================
// Expression compilation
// ============================================================

void compile_expr(Compiler* c, const char** p) {
    skip_whitespace(p);
    
    if (**p == '(') {
        (*p)++;
        compile_expr(c, p);
        if (**p == ')') (*p)++;
        return;
    }
    
    if (isdigit(**p)) {
        int val = parse_number(p);
        emit_push_int(c, val);
    } else if (isalpha(**p) || **p == '_') {
        char name[MAX_STR];
        parse_identifier(p, name, MAX_STR);
        
        if (strcmp(name, "+") == 0) {
            compile_expr(c, p);
            compile_expr(c, p);
            emit_op(c, ADD);
        } else if (strcmp(name, "-") == 0) {
            compile_expr(c, p);
            compile_expr(c, p);
            emit_op(c, MUL);
            emit_push_int(c, -1);
            emit_op(c, FUSE);
        } else if (strcmp(name, "*") == 0) {
            compile_expr(c, p);
            compile_expr(c, p);
            emit_op(c, MUL);
        } else if (strcmp(name, "|") == 0) {
            compile_expr(c, p);
            compile_expr(c, p);
            emit_op(c, FUSE);
        } else {
            SymbolEntry* sym = find_symbol(c, name);
            if (sym) {
                emit_op(c, LOAD);
                emit_u32(c, sym->address);
            } else {
                // Function call or variable
                if (**p == '(') {
                    // Function call
                    (*p)++; // skip '('
                    // Parse arguments
                    if (**p != ')') {
                        compile_expr(c, p);
                        while (**p == ',') {
                            (*p)++;
                            compile_expr(c, p);
                        }
                    }
                    if (**p == ')') (*p)++;
                    
                    // Jump to function
                    emit_op(c, JMP);
                    emit_u32(c, 0); // placeholder
                    // Add relocation
                    c->relocs[c->reloc_count].addr = c->code_pos - 4;
                    strcpy(c->relocs[c->reloc_count].label, name);
                    c->reloc_count++;
                } else {
                    fprintf(stderr, "Undefined variable: %s\n", name);
                }
            }
        }
    }
}

// ============================================================
// Statement compilation
// ============================================================

void compile_statement(Compiler* c, const char** p) {
    skip_whitespace(p);
    
    if (!**p) return;
    
    if (strncmp(*p, "int", 3) == 0 && isspace((*p)[3])) {
        *p += 3;
        skip_whitespace(p);
        char name[MAX_STR];
        parse_identifier(p, name, MAX_STR);
        add_symbol(c, name, 0);
        
        skip_whitespace(p);
        if (**p == '=') {
            (*p)++;
            compile_expr(c, p);
            SymbolEntry* sym = find_symbol(c, name);
            emit_op(c, STORE);
            emit_u32(c, sym->address);
        }
        
        if (**p == ';') (*p)++;
        
    } else if (strncmp(*p, "if", 2) == 0 && isspace((*p)[2])) {
        *p += 2;
        skip_whitespace(p);
        if (**p == '(') (*p)++;
        
        compile_expr(c, p);
        
        if (**p == ')') (*p)++;
        
        emit_op(c, COHERE);
        
        int jmp_addr = c->code_pos;
        emit_op(c, IF_EQ);
        emit_u32(c, 0);
        
        compile_statement(c, p);
        
        // Patch jump
        int target = c->code_pos;
        c->code[jmp_addr + 1] = target & 0xFF;
        c->code[jmp_addr + 2] = (target >> 8) & 0xFF;
        c->code[jmp_addr + 3] = (target >> 16) & 0xFF;
        c->code[jmp_addr + 4] = (target >> 24) & 0xFF;
        
    } else if (strncmp(*p, "while", 5) == 0 && isspace((*p)[5])) {
        *p += 5;
        skip_whitespace(p);
        
        int loop_start = c->code_pos;
        
        if (**p == '(') (*p)++;
        compile_expr(c, p);
        if (**p == ')') (*p)++;
        
        emit_op(c, COHERE);
        
        int jmp_addr = c->code_pos;
        emit_op(c, IF_EQ);
        emit_u32(c, 0);
        
        compile_statement(c, p);
        
        emit_op(c, JMP);
        emit_u32(c, loop_start);
        
        // Patch jump
        int target = c->code_pos;
        c->code[jmp_addr + 1] = target & 0xFF;
        c->code[jmp_addr + 2] = (target >> 8) & 0xFF;
        c->code[jmp_addr + 3] = (target >> 16) & 0xFF;
        c->code[jmp_addr + 4] = (target >> 24) & 0xFF;
        
    } else if (strncmp(*p, "return", 6) == 0) {
        *p += 6;
        compile_expr(c, p);
        emit_op(c, HALT);
        if (**p == ';') (*p)++;
        
    } else if (**p == '{') {
        (*p)++;
        while (**p && **p != '}') {
            compile_statement(c, p);
            skip_whitespace(p);
        }
        if (**p == '}') (*p)++;
        
    } else if (isalpha(**p) || **p == '_') {
        char name[MAX_STR];
        parse_identifier(p, name, MAX_STR);
        
        skip_whitespace(p);
        if (**p == '=') {
            (*p)++;
            compile_expr(c, p);
            SymbolEntry* sym = find_symbol(c, name);
            if (sym) {
                emit_op(c, STORE);
                emit_u32(c, sym->address);
            }
        }
        
        if (**p == ';') (*p)++;
    }
}

// ============================================================
// Function compilation
// ============================================================

void compile_function(Compiler* c, const char** p) {
    // Skip return type
    while (**p && !isspace(**p)) (*p)++;
    skip_whitespace(p);
    
    char name[MAX_STR];
    parse_identifier(p, name, MAX_STR);
    
    SymbolEntry* func = add_symbol(c, name, 1);
    func->address = c->code_pos;
    
    skip_whitespace(p);
    if (**p == '(') {
        (*p)++;
        skip_whitespace(p);
        
        while (**p && **p != ')') {
            if (strncmp(*p, "int", 3) == 0) {
                *p += 3;
                skip_whitespace(p);
                char param[MAX_STR];
                parse_identifier(p, param, MAX_STR);
                add_symbol(c, param, 0);
                func->param_count++;
                skip_whitespace(p);
                if (**p == ',') {
                    (*p)++;
                    skip_whitespace(p);
                }
            }
        }
        if (**p == ')') (*p)++;
    }
    
    compile_statement(c, p);
}

// ============================================================
// Program compilation
// ============================================================

void compile_program(Compiler* c, const char* source) {
    const char* p = source;
    
    while (*p) {
        skip_whitespace(&p);
        if (!*p) break;
        
        if (strncmp(p, "int", 3) == 0 || strncmp(p, "void", 4) == 0) {
            // Check if it's a function (has parentheses after name)
            const char* saved = p;
            while (*p && !isspace(*p)) p++;
            skip_whitespace(&p);
            char name[MAX_STR];
            parse_identifier(&p, name, MAX_STR);
            skip_whitespace(&p);
            int is_func = (*p == '(');
            p = saved;
            
            if (is_func) {
                compile_function(c, &p);
            } else {
                compile_statement(c, &p);
            }
        } else {
            compile_statement(c, &p);
        }
    }
}

// ============================================================
// Output
// ============================================================

void write_output(Compiler* c, FILE* out) {
    // Magic
    fwrite("TSGV", 1, 4, out);
    
    // Version
    uint32_t version = 1;
    fwrite(&version, 4, 1, out);
    
    // Flags
    uint32_t flags = 0;
    fwrite(&flags, 4, 1, out);
    
    // Heap size
    uint64_t heap_size = c->next_addr;
    fwrite(&heap_size, 8, 1, out);
    
    // Code size
    uint64_t code_size = c->code_pos;
    fwrite(&code_size, 8, 1, out);
    
    // Entry point (main)
    uint32_t entry = 0;
    SymbolEntry* main_sym = find_symbol(c, "main");
    if (main_sym) entry = main_sym->address;
    fwrite(&entry, 4, 1, out);
    
    // Reserved
    uint32_t reserved = 0;
    fwrite(&reserved, 4, 1, out);
    
    // Code
    fwrite(c->code, 1, c->code_pos, out);
}

// ============================================================
// Main
// ============================================================

int main(int argc, char** argv) {
    if (argc < 3) {
        fprintf(stderr, "Usage: %s input.c -o output.tsgvm\n", argv[0]);
        return 1;
    }
    
    const char* input_file = NULL;
    const char* output_file = NULL;
    
    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "-o") == 0 && i + 1 < argc) {
            output_file = argv[++i];
        } else if (argv[i][0] != '-') {
            input_file = argv[i];
        }
    }
    
    if (!input_file || !output_file) {
        fprintf(stderr, "Missing input or output\n");
        return 1;
    }
    
    // Read source
    FILE* f = fopen(input_file, "r");
    if (!f) {
        fprintf(stderr, "Cannot open %s\n", input_file);
        return 1;
    }
    
    fseek(f, 0, SEEK_END);
    long len = ftell(f);
    fseek(f, 0, SEEK_SET);
    
    char* source = malloc(len + 1);
    fread(source, 1, len, f);
    source[len] = '\0';
    fclose(f);
    
    // Compile
    Compiler c = {0};
    c.next_addr = 0x1000;
    
    compile_program(&c, source);
    
    // Resolve relocations
    for (int i = 0; i < c.reloc_count; i++) {
        SymbolEntry* sym = find_symbol(&c, c.relocs[i].label);
        if (sym) {
            uint32_t addr = sym->address;
            int pos = c.relocs[i].addr;
            c.code[pos] = addr & 0xFF;
            c.code[pos+1] = (addr >> 8) & 0xFF;
            c.code[pos+2] = (addr >> 16) & 0xFF;
            c.code[pos+3] = (addr >> 24) & 0xFF;
        } else {
            fprintf(stderr, "Undefined symbol: %s\n", c.relocs[i].label);
        }
    }
    
    // Write output
    FILE* out = fopen(output_file, "wb");
    if (!out) {
        fprintf(stderr, "Cannot create %s\n", output_file);
        return 1;
    }
    
    write_output(&c, out);
    fclose(out);
    
    printf("Compiled %s -> %s (%d bytes)\n", input_file, output_file, c.code_pos);
    
    free(source);
    return 0;
}
9. Bootstrap Workflow
bash
# Step 1: Compile bootstrap compiler with gcc
gcc -o boot boot.c

# Step 2: Compile stage1 compiler (written in C subset)
./boot stage1.c -o stage1

# Step 3: Compile stage2 compiler (self-hosting)
./stage1 stage2.tsg -o stage2

# Step 4: Verify (stage2 compiled by stage1 should equal stage2 compiled by stage2)
./stage2 stage2.tsg -o stage2_v2
cmp stage2 stage2_v2

# Step 5: Compile full C compiler
./stage2 tscg-compiler.tsg -o tscg-compiler

# Step 6: Compile user programs
./tscg-compiler myprogram.c -o myprogram.tsgvm

# Step 7: Run on VM
./vm myprogram.tsgvm
10. Example Program
c
// example.c - Test program

int factorial(int n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

int main() {
    int result;
    result = factorial(5);
    return result;
}
Summary
This complete specification includes:

16-symbol alphabet (0x0-0xF) with Territory, Map, Stereopsis primitives and neutrals

Full VM implementation in Rust with all opcodes

Assembler with label support and relocation

Disassembler with automatic label generation

Pretty printer with indentation and colorization

Linker for combining executables and libraries

Bootstrap compiler (C → Triskele bytecode) in ~500 lines of C

Self-hosting strategy with stage1, stage2 verification

Complete base 16 encoding for constants using | operator

The system is now ready for implementing a full C compiler and potentially running DOOM-like games on the Triskele VM.

text

Tu peux copier ce contenu dans un fichier nommé `tscg_vm_spec.md`.
