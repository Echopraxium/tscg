// tsk-asm/src/main.rs
// Author: Echopraxium with the collaboration of Claude AI
// Version: 0.3.0
// Source extension: .tasm  |  Output extension: auto-deduced from .type directive
//   .type executable  ->  .tvmx
//   .type library     ->  .tvml
//   .type object      ->  .tobj  (default when .type is absent)
//   .type archive     ->  error  (not yet supported)
// Override: -o <path> always wins over auto-deduction.

mod lexer;
mod assembler;
mod encoder;

use clap::Parser;
use std::path::PathBuf;
use triskele_common::tvm::{TvmBuilder, SectionType, section_flags};

#[derive(Parser, Debug)]
#[clap(name = "tsk-asm", version = "0.3.0",
       about = "TriskeleVM assembler — .tasm -> .tvmx / .tvml / .tobj")]
struct Args {
    /// Source file (.tasm)
    input: PathBuf,

    /// Output file (optional — auto-deduced from .type directive in source)
    #[clap(short, long)]
    output: Option<PathBuf>,

    /// Emit symbol table alongside output (<output>.sym, label -> address)
    #[clap(long)]
    emit_symbols: bool,

    #[clap(long)]
    verbose: bool,
}

fn main() {
    env_logger::init();
    let args = Args::parse();

    // ── Deduce output path ────────────────────────────────────────────────────
    let output = match args.output {
        Some(ref p) => p.clone(),
        None => {
            // Quick scan of the source to find .type directive
            let src = match std::fs::read_to_string(&args.input) {
                Ok(s)  => s,
                Err(e) => {
                    eprintln!("[tsk-asm] error: cannot read '{}': {}", args.input.display(), e);
                    std::process::exit(1);
                }
            };
            match deduce_output_path(&args.input, &src) {
                Ok(p)  => p,
                Err(e) => {
                    eprintln!("[tsk-asm] error: {}", e);
                    eprintln!("         Hint: add '.type executable' (or library/object) to your .tasm,");
                    eprintln!("               or specify output explicitly with -o <file>");
                    std::process::exit(1);
                }
            }
        }
    };

    match assemble_file(&args.input, &output, args.emit_symbols, args.verbose) {
        Ok(()) => eprintln!("[tsk-asm] {} -> {}", args.input.display(), output.display()),
        Err(e) => { eprintln!("[tsk-asm] error: {}", e); std::process::exit(1); }
    }
}

/// Scan source for `.type <kind>` and map to the correct extension.
fn deduce_output_path(input: &std::path::Path, src: &str) -> anyhow::Result<PathBuf> {
    let kind = extract_type_directive(src);

    let ext = match kind.as_deref() {
        Some("executable") => "tvmx",
        Some("library")    => "tvml",
        Some("object") | None => "tobj",
        Some("archive")    => anyhow::bail!(
            "'.type archive' is not yet supported by tsk-asm (no archiver implemented)"
        ),
        Some(other) => anyhow::bail!(
            "unknown .type value '{}' — expected: executable, library, object, archive", other
        ),
    };

    Ok(input.with_extension(ext))
}

/// Extract the value of the first `.type <value>` directive (case-insensitive, ignores comments).
fn extract_type_directive(src: &str) -> Option<String> {
    for line in src.lines() {
        let line = line.trim();
        // Skip blank lines and comments
        if line.is_empty() || line.starts_with(';') { continue; }
        // Strip inline comment
        let line = line.split(';').next().unwrap_or("").trim();
        // Match `.type <value>`
        if let Some(rest) = line.strip_prefix(".type") {
            let value = rest.trim().to_lowercase();
            if !value.is_empty() {
                return Some(value);
            }
        }
    }
    None
}

pub fn assemble_file(
    input:        &std::path::Path,
    output:       &std::path::Path,
    emit_symbols: bool,
    verbose:      bool,
) -> anyhow::Result<()> {
    let src = std::fs::read_to_string(input)
        .map_err(|e| anyhow::anyhow!("cannot read '{}': {}", input.display(), e))?;
    let (bytes, symbols) = assemble_str_with_symbols(&src, verbose)?;
    std::fs::write(output, &bytes)
        .map_err(|e| anyhow::anyhow!("cannot write '{}': {}", output.display(), e))?;

    if emit_symbols {
        let sym_path = output.with_extension("sym");
        let mut content = String::new();
        // Sort by address for readability
        let mut sorted: Vec<(&String, &u64)> = symbols.iter().collect();
        sorted.sort_by_key(|(_, a)| *a);
        for (label, addr) in sorted {
            content.push_str(&format!("{} 0x{:04X}\n", label, addr));
        }
        std::fs::write(&sym_path, &content)
            .map_err(|e| anyhow::anyhow!("cannot write symbol table '{}': {}", sym_path.display(), e))?;
        eprintln!("[tsk-asm] symbols -> {}", sym_path.display());
    }

    Ok(())
}

pub fn assemble_str(src: &str, verbose: bool) -> anyhow::Result<Vec<u8>> {
    let (bytes, _) = assemble_str_with_symbols(src, verbose)?;
    Ok(bytes)
}

pub fn assemble_str_with_symbols(
    src:     &str,
    verbose: bool,
) -> anyhow::Result<(Vec<u8>, std::collections::HashMap<String, u64>)> {
    let tokens  = lexer::Lexer::new(src).tokenize()?;
    let asm_out = assembler::Assembler::new(tokens).assemble()?;
    if verbose {
        eprintln!("[tsk-asm] module: {}", asm_out.module_name);
        eprintln!("[tsk-asm] rodata: {} bytes", asm_out.rodata.len());
        eprintln!("[tsk-asm] code:   {} bytes", asm_out.code.len());
        eprintln!("[tsk-asm] entry:  +{}", asm_out.entry_offset);
        eprintln!("[tsk-asm] labels: {}", asm_out.symbol_table.len());
    }
    let mut builder = TvmBuilder::new();
    if !asm_out.rodata.is_empty() {
        builder = builder.add_section(
            SectionType::Rodata,
            section_flags::READABLE,
            asm_out.rodata,
        );
    }
    // Build symtab section: [name\0][u32 offset] — format attendu par tsk-link
    let mut symtab: Vec<u8> = Vec::new();
    for (name, addr) in &asm_out.symbol_table {
        symtab.extend_from_slice(name.as_bytes());
        symtab.push(0u8);
        symtab.extend_from_slice(&(*addr as u32).to_le_bytes());
    }

    let mut b = builder.add_section(
        SectionType::Code,
        section_flags::READABLE | section_flags::EXECUTABLE,
        asm_out.code,
    )
    .entry(asm_out.entry_offset);

    if !symtab.is_empty() {
        b = b.add_section(SectionType::Symtab, 0x06, symtab);
    }

    let tvx = b.build();
    Ok((tvx, asm_out.symbol_table))
}

#[cfg(test)]
mod tests {
    use super::*;
    use triskele_common::tvm::{TvmFile, SectionType};
    use triskele_vm::{Cpu, memory::{Memory, NULL_PAGE_END}};
    use std::io::Cursor;

    const WOLF3D_HELLO: &str = r#"
; wolf3d_hello.tasm
.module  hello
.type    executable
.section .code
.entry   main
main:
    D_MOV_I  R0, 'H'
    O_LOG    R0
    D_MOV_I  R0, 'i'
    O_LOG    R0
    D_MOV_I  R0, '!'
    O_LOG    R0
    D_MOV_I  R0, '\n'
    O_LOG    R0
    D_MOV_I  R0, 0
    F_HALT
"#;

    /// Assemble `src`, load into VM, run, return (exit_code, cpu, captured_output).
    /// O_LOG output is captured to a Vec<u8> to avoid Windows console UTF-8 issues.
    fn run_src(src: &str) -> anyhow::Result<(i32, triskele_vm::Cpu)> {
        use triskele_vm::memory::{HEAP_BASE, HEAP_SIZE};
        use std::io::Write;
        use std::sync::{Arc, Mutex};

        let tvx = assemble_str(src, false)?;
        let tvm = TvmFile::load_from_reader(&mut Cursor::new(&tvx))?;

        let total = HEAP_BASE + HEAP_SIZE - NULL_PAGE_END;
        let mut mem = Memory::new(NULL_PAGE_END, total);

        let mut load_ptr = NULL_PAGE_END;
        if let Some(rodata) = tvm.find_section(SectionType::Rodata) {
            if !rodata.data.is_empty() {
                mem.write_bytes(load_ptr, &rodata.data)?;
                load_ptr += ((rodata.data.len() as u64) + 3) & !3;
            }
        }
        let code = tvm.find_section(SectionType::Code).unwrap();
        mem.write_bytes(load_ptr, &code.data)?;

        let entry = load_ptr + tvm.entry_offset() as u64;

        // Inject a Vec<u8> output sink — avoids Windows console non-UTF8 panic
        struct BufSink(Arc<Mutex<Vec<u8>>>);
        impl Write for BufSink {
            fn write(&mut self, d: &[u8]) -> std::io::Result<usize> {
                self.0.lock().unwrap().extend_from_slice(d); Ok(d.len())
            }
            fn flush(&mut self) -> std::io::Result<()> { Ok(()) }
        }
        unsafe impl Send for BufSink {}
        let sink = Arc::new(Mutex::new(Vec::<u8>::new()));
        let mut cpu = Cpu::new(mem, entry, false)
            .with_output(Box::new(BufSink(sink.clone())));
        let result = cpu.run()?;
        Ok((result, cpu))
    }

    #[test]
    fn test_deduce_executable() {
        let src = ".module foo\n.type executable\n.section .code\n.entry m\nm:\n F_HALT\n";
        let p = deduce_output_path(std::path::Path::new("foo.tasm"), src).unwrap();
        assert_eq!(p.extension().unwrap(), "tvmx");
    }

    #[test]
    fn test_deduce_library() {
        let src = ".module mylib\n.type library\n";
        let p = deduce_output_path(std::path::Path::new("mylib.tasm"), src).unwrap();
        assert_eq!(p.extension().unwrap(), "tvml");
    }

    #[test]
    fn test_deduce_object_default() {
        let src = ".module obj\n"; // no .type
        let p = deduce_output_path(std::path::Path::new("obj.tasm"), src).unwrap();
        assert_eq!(p.extension().unwrap(), "tobj");
    }

    #[test]
    fn test_deduce_archive_error() {
        let src = ".module ar\n.type archive\n";
        assert!(deduce_output_path(std::path::Path::new("ar.tasm"), src).is_err());
    }

    #[test]
    fn test_assemble_wolf3d_hello() {
        let tvx = assemble_str(WOLF3D_HELLO, false).unwrap();
        assert_eq!(&tvx[0..4], b"TSKV");
    }

    #[test]
    fn test_assemble_and_run() {
        let (code, _) = run_src(WOLF3D_HELLO).unwrap();
        assert_eq!(code, 0);
    }

    #[test]
    fn test_assemble_call_ret() {
        let src = r#"
.module  callret_test
.type    executable
.section .code
.entry   main
main:
    F_CALL   my_func
    D_MOV_I  R0, 0
    F_HALT
my_func:
    D_MOV_I  R1, 42
    F_RET
"#;
        let (code, cpu) = run_src(src).unwrap();
        assert_eq!(code, 0);
        assert_eq!(cpu.regs.get(1).unwrap(), 42);
    }

    #[test]
    fn test_assemble_define_constant() {
        let src = r#"
.module  defines_test
.type    executable
.section .code
.entry   main
#define  EXIT_OK  0
#define  ASCII_H  72
main:
    D_MOV_I  R0, ASCII_H
    O_LOG    R0
    D_MOV_I  R0, EXIT_OK
    F_HALT
"#;
        let (code, _) = run_src(src).unwrap();
        assert_eq!(code, 0);
    }

    #[test]
    fn test_assemble_forward_label() {
        let src = r#"
.module  fwd_label_test
.type    executable
.section .code
.entry   main
main:
    D_MOV_I  R1, 0
    V_CMP_I  R1, 0
    F_JZ     done
    D_MOV_I  R0, 1
    F_HALT
done:
    D_MOV_I  R0, 0
    F_HALT
"#;
        let (code, _) = run_src(src).unwrap();
        assert_eq!(code, 0, "forward label jump must skip the R0=1 path");
    }

    #[test]
    fn test_assemble_string_rodata() {
        let src = r#"
.module  string_test
.type    executable

.section .rodata
msg:  .string "Hi!\n"

.section .code
.entry   main

main:
    L_LEA    R1, msg
    D_MOV_I  R2, 4
print_loop:
    D_LOAD8  R0, R1, 0
    O_LOG    R0
    D_ADD_I  R1, 1
    D_SUB_I  R2, 1
    V_CMP_I  R2, 0
    F_JNZ    print_loop
    D_MOV_I  R0, 0
    F_HALT
"#;
        let (code, _) = run_src(src).unwrap();
        assert_eq!(code, 0, ".string + loop must exit cleanly");
    }
}
