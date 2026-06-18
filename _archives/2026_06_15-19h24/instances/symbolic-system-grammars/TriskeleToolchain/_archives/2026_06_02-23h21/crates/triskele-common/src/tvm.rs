// triskele-common/src/tvm.rs
// Author: Echopraxium with the collaboration of Claude AI
// Version: 0.2.0
//
// .tobj / .tvmx / .tvml binary format — from TriskeleVM_Format_TVM.md
//
// File layout:
//   [0x00]  Magic "TSKV"
//   [0x04]  Version (Base16 Triskele)
//   [0x08]  Flags
//   [0x0C]  Section count N
//   [0x10]  Entry point section index
//   [0x14]  Entry point offset
//   [0x18]  Timestamp (Unix epoch, 8 bytes)
//   [0x20]  Reserved (32 bytes)
//   [0x40]  Section table (N × 32 bytes)
//   [0x40 + N×32]  Section data

use std::io::{Read, Seek, SeekFrom};
use crate::error::VmError;

// ─────────────────────────────────────────────────────────────────────────────
// Constants
// ─────────────────────────────────────────────────────────────────────────────

pub const TVM_MAGIC: &[u8; 4] = b"TSKV";
pub const TVM_HEADER_BASE: u64 = 0x40;    // header size before section table
pub const TVM_SECTION_ENTRY: u64 = 32;    // bytes per section table entry

// ─────────────────────────────────────────────────────────────────────────────
// Section types
// ─────────────────────────────────────────────────────────────────────────────

#[repr(u8)]
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum SectionType {
    Code    = 0x01,  // .code — executable bytecode
    Data    = 0x02,  // .data — initialized globals
    Rodata  = 0x03,  // .rodata — read-only constants
    Bss     = 0x04,  // .bss — uninitialized data (size only)
    Symtab  = 0x05,  // .symtab — symbol table
    Strtab  = 0x06,  // .strtab — string table
    Reltab  = 0x07,  // .reltab — relocation table
    Debug   = 0x08,  // .debug — debug info
    Tscg    = 0x09,  // .tscg — TSCG semantic annotations
    GcRoots = 0x0A,  // .gc_roots — GC roots table
    Unwind  = 0x0B,  // .unwind — exception unwind tables
    Import  = 0x0C,  // .import — FFI import declarations
    Export  = 0x0D,  // .export — exported symbols
    Raw     = 0xFF,  // .raw — binary assets (textures, sounds, DLLs)
}

impl SectionType {
    pub fn from_u8(v: u8) -> Option<Self> {
        match v {
            0x01 => Some(Self::Code),
            0x02 => Some(Self::Data),
            0x03 => Some(Self::Rodata),
            0x04 => Some(Self::Bss),
            0x05 => Some(Self::Symtab),
            0x06 => Some(Self::Strtab),
            0x07 => Some(Self::Reltab),
            0x08 => Some(Self::Debug),
            0x09 => Some(Self::Tscg),
            0x0A => Some(Self::GcRoots),
            0x0B => Some(Self::Unwind),
            0x0C => Some(Self::Import),
            0x0D => Some(Self::Export),
            0xFF => Some(Self::Raw),
            _    => None,
        }
    }

    pub fn name(&self) -> &'static str {
        match self {
            Self::Code    => ".code",
            Self::Data    => ".data",
            Self::Rodata  => ".rodata",
            Self::Bss     => ".bss",
            Self::Symtab  => ".symtab",
            Self::Strtab  => ".strtab",
            Self::Reltab  => ".reltab",
            Self::Debug   => ".debug",
            Self::Tscg    => ".tscg",
            Self::GcRoots => ".gc_roots",
            Self::Unwind  => ".unwind",
            Self::Import  => ".import",
            Self::Export  => ".export",
            Self::Raw     => ".raw",
        }
    }
}

// ─────────────────────────────────────────────────────────────────────────────
// Section flags
// ─────────────────────────────────────────────────────────────────────────────

pub mod section_flags {
    pub const READABLE:   u32 = 1 << 0;
    pub const WRITABLE:   u32 = 1 << 1;
    pub const EXECUTABLE: u32 = 1 << 2;
    pub const BASE16:     u32 = 1 << 3;  // Base16 Triskele encoded (vs raw)
    pub const COMPRESSED: u32 = 1 << 4;  // future
}

// ─────────────────────────────────────────────────────────────────────────────
// File flags
// ─────────────────────────────────────────────────────────────────────────────

pub mod file_flags {
    pub const HAS_DEBUG_INFO:   u32 = 1 << 0;
    pub const HAS_SYMBOL_TABLE: u32 = 1 << 1;
    pub const HAS_RAW_ASSETS:   u32 = 1 << 2;
    pub const IS_LIBRARY:       u32 = 1 << 3;
    pub const IS_POSITION_INDEP:u32 = 1 << 4;
    pub const HAS_GC_METADATA:  u32 = 1 << 5;
    pub const HAS_TSCG_ANNOT:   u32 = 1 << 6;
    pub const HAS_EXCEPTIONS:   u32 = 1 << 7;
}

// ─────────────────────────────────────────────────────────────────────────────
// Section (in-memory representation)
// ─────────────────────────────────────────────────────────────────────────────

#[derive(Debug, Clone)]
pub struct Section {
    pub section_type: SectionType,
    pub flags:        u32,
    pub file_offset:  u64,
    pub size:         u64,
    pub alignment:    u32,
    pub m3_tag:       u32,   // dominant M3 primitive (semantic annotation)
    pub data:         Vec<u8>,
}

impl Section {
    pub fn is_executable(&self) -> bool {
        self.flags & section_flags::EXECUTABLE != 0
    }
    pub fn is_writable(&self) -> bool {
        self.flags & section_flags::WRITABLE != 0
    }
    pub fn is_readable(&self) -> bool {
        self.flags & section_flags::READABLE != 0
    }
}

// ─────────────────────────────────────────────────────────────────────────────
// TvmFile
// ─────────────────────────────────────────────────────────────────────────────

#[derive(Debug)]
pub struct TvmFile {
    pub version:       [u8; 4],
    pub flags:         u32,
    pub entry_section: u32,   // index of .code section containing entry point
    pub entry_offset:  u32,   // offset within .code section
    pub timestamp:     u64,
    pub sections:      Vec<Section>,
}

impl TvmFile {
    /// Load a .tobj/.tvmx binary from a file path.
    pub fn load_from_file(path: &str) -> Result<Self, VmError> {
        let mut f = std::fs::File::open(path)?;
        Self::load_from_reader(&mut f)
    }

    /// Load a .tobj/.tvmx binary from any reader.
    pub fn load_from_reader<R: Read + Seek>(r: &mut R) -> Result<Self, VmError> {
        // Magic
        let mut magic = [0u8; 4];
        r.read_exact(&mut magic).map_err(|e| VmError::IoError(e.to_string()))?;
        if &magic != TVM_MAGIC {
            return Err(VmError::InvalidTvxFile(format!(
                "bad magic: {:?} (expected 'TSKV')", magic
            )));
        }

        // Version
        let mut version = [0u8; 4];
        r.read_exact(&mut version)?;

        // Flags
        let flags = read_u32(r)?;

        // Section count
        let section_count = read_u32(r)? as usize;

        // Entry point
        let entry_section = read_u32(r)?;
        let entry_offset  = read_u32(r)?;

        // Timestamp (8 bytes)
        let timestamp = read_u64(r)?;

        // Reserved (32 bytes)
        let mut _reserved = [0u8; 32];
        r.read_exact(&mut _reserved)?;

        // Section table (N × 32 bytes each)
        let mut section_headers: Vec<(SectionType, u32, u64, u64, u32, u32)> = Vec::new();
        for _ in 0..section_count {
            let stype_raw = read_u32(r)?;
            let stype = SectionType::from_u8(stype_raw as u8)
                .ok_or_else(|| VmError::InvalidTvxFile(format!(
                    "unknown section type: 0x{:02X}", stype_raw
                )))?;
            let sflags    = read_u32(r)?;
            let soffset   = read_u64(r)?;
            let ssize     = read_u64(r)?;
            let salign    = read_u32(r)?;
            let sm3_tag   = read_u32(r)?;
            section_headers.push((stype, sflags, soffset, ssize, salign, sm3_tag));
        }

        // Section data
        let mut sections = Vec::with_capacity(section_count);
        for (section_type, flags, file_offset, size, alignment, m3_tag) in section_headers {
            r.seek(SeekFrom::Start(file_offset))?;
            let mut data = vec![0u8; size as usize];
            if section_type != SectionType::Bss {
                r.read_exact(&mut data)?;
            }
            sections.push(Section { section_type, flags, file_offset, size, alignment, m3_tag, data });
        }

        Ok(TvmFile { version, flags, entry_section, entry_offset, timestamp, sections })
    }

    /// Find the first section of a given type.
    pub fn find_section(&self, stype: SectionType) -> Option<&Section> {
        self.sections.iter().find(|s| s.section_type == stype)
    }

    /// Absolute entry point address in the .code section (VM load address not yet applied).
    pub fn entry_offset(&self) -> u32 {
        self.entry_offset
    }

    /// True if this is a library (no entry point).
    pub fn is_library(&self) -> bool {
        self.flags & file_flags::IS_LIBRARY != 0
    }
}

// ─────────────────────────────────────────────────────────────────────────────
// Minimal .tvx builder (for tests and tsk-asm)
// ─────────────────────────────────────────────────────────────────────────────

pub struct TvmBuilder {
    sections: Vec<(SectionType, u32, Vec<u8>)>,  // (type, flags, data)
    entry_offset: u32,
}

impl TvmBuilder {
    pub fn new() -> Self {
        Self { sections: Vec::new(), entry_offset: 0 }
    }

    pub fn add_section(mut self, stype: SectionType, flags: u32, data: Vec<u8>) -> Self {
        self.sections.push((stype, flags, data));
        self
    }

    pub fn entry(mut self, offset: u32) -> Self {
        self.entry_offset = offset;
        self
    }

    /// Serialize to a .tobj binary (in-memory).
    pub fn build(self) -> Vec<u8> {
        let n = self.sections.len() as u32;
        let header_size = (TVM_HEADER_BASE + n as u64 * TVM_SECTION_ENTRY) as usize;
        let mut out = vec![0u8; header_size];

        // Magic
        out[0..4].copy_from_slice(TVM_MAGIC);
        // Version 0.2.0.0
        out[4..8].copy_from_slice(&[0, 2, 0, 0]);
        // Flags: has_symbol_table
        out[8..12].copy_from_slice(&(file_flags::HAS_SYMBOL_TABLE).to_le_bytes());
        // Section count
        out[12..16].copy_from_slice(&n.to_le_bytes());
        // Entry section index = 0 (first section = .code)
        out[16..20].copy_from_slice(&0u32.to_le_bytes());
        // Entry offset
        out[20..24].copy_from_slice(&self.entry_offset.to_le_bytes());
        // Timestamp = 0
        out[24..32].copy_from_slice(&0u64.to_le_bytes());
        // Reserved: already zero

        // Section table + data
        let mut data_offset = header_size as u64;
        for (i, (stype, flags, data)) in self.sections.iter().enumerate() {
            let base = TVM_HEADER_BASE as usize + i * TVM_SECTION_ENTRY as usize;
            out[base..base+4].copy_from_slice(&(*stype as u32).to_le_bytes());
            out[base+4..base+8].copy_from_slice(&flags.to_le_bytes());
            out[base+8..base+16].copy_from_slice(&data_offset.to_le_bytes());
            out[base+16..base+24].copy_from_slice(&(data.len() as u64).to_le_bytes());
            out[base+24..base+28].copy_from_slice(&4u32.to_le_bytes());  // alignment
            let m3_tag: u32 = match stype {
                SectionType::Code   => 0x02,  // F — Flow
                SectionType::Data   => 0x01,  // St — Structure
                SectionType::Rodata => 0x01,
                SectionType::Symtab => 0x0E,  // Ss — Symbol
                _                   => 0x00,
            };
            out[base+28..base+32].copy_from_slice(&m3_tag.to_le_bytes());
            data_offset += data.len() as u64;
        }

        // Section data
        for (_, _, data) in &self.sections {
            out.extend_from_slice(data);
        }
        out
    }
}

// ─────────────────────────────────────────────────────────────────────────────
// Read helpers (little-endian)
// ─────────────────────────────────────────────────────────────────────────────

fn read_u32<R: Read>(r: &mut R) -> Result<u32, VmError> {
    let mut buf = [0u8; 4];
    r.read_exact(&mut buf)?;
    Ok(u32::from_le_bytes(buf))
}

fn read_u64<R: Read>(r: &mut R) -> Result<u64, VmError> {
    let mut buf = [0u8; 8];
    r.read_exact(&mut buf)?;
    Ok(u64::from_le_bytes(buf))
}
