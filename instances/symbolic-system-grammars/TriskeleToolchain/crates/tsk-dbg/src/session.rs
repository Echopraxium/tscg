// tsk-dbg/src/session.rs
// Author: Echopraxium with the collaboration of Claude AI
// Version: 0.3.0 — async run_vm with spawn_blocking for true pause support
//
// Architecture:
//   handle_request() is async
//   run_vm() uses tokio::task::spawn_blocking to run the VM in a thread pool
//   pause is implemented via AtomicBool (pause_flag) shared with the VM thread
//   The DAP server can receive pause/evaluate/disconnect while VM runs

use std::collections::HashSet;
use std::sync::Arc;
use std::sync::atomic::Ordering;
use tokio::sync::Mutex;
use serde_json::{json, Value};

use crate::dap::types::*;
use crate::disasm::disassemble_around;
use crate::symbols::SymbolTable;
use crate::vm_runner::{RunMode, StopCause, VmRunner};

const VAR_REF_REGISTERS:   u32 = 1;
const VAR_REF_STACK:       u32 = 2;
const VAR_REF_DISASSEMBLY: u32 = 100;
fn reg_detail_ref(reg: usize) -> u32 { 10 + reg as u32 }

pub struct DebugSession<W> {
    runner:           VmRunner,
    symbols:          SymbolTable,
    bytecode:         Vec<u8>,
    _writer:          Arc<Mutex<W>>,
    source:           Option<DapSource>,
    stop_on_entry:    bool,
    max_instructions: u64,   // 0 = unlimited
}

impl<W: tokio::io::AsyncWrite + Unpin + Send + 'static> DebugSession<W> {
    pub fn new(
        bytecode:         Vec<u8>,
        symbols:          SymbolTable,
        mem_size:         usize,
        max_instructions: u64,
        writer:           Arc<Mutex<W>>,
    ) -> Self {
        let runner = VmRunner::new(&bytecode, mem_size);
        Self {
            runner, symbols, bytecode,
            _writer: writer,
            source: None,
            stop_on_entry: true,
            max_instructions,
        }
    }

    // -------------------------------------------------------------------------
    // Main DAP dispatch (async)
    // -------------------------------------------------------------------------

    pub async fn handle_request(
        &mut self,
        req:     &DapRequest,
        out_seq: &mut u64,
    ) -> Vec<Value> {
        let mut out: Vec<Value> = Vec::new();
        let rseq = req.seq;

        match req.command.as_str() {

            "initialize" => {
                let caps = json!({
                    "supportsConfigurationDoneRequest": true,
                    "supportsFunctionBreakpoints":      true,
                    "supportsConditionalBreakpoints":   false,
                    "supportsDisassembleRequest":       true,
                    "supportsStepBack":                 false,
                    "supportsEvaluateForHovers":        true,
                    "supportsRestartRequest":           false,
                    "supportsTerminateRequest":         true,
                });
                let resp = DapResponse::ok(*out_seq, rseq, "initialize", Some(caps));
                out.push(serde_json::to_value(resp).unwrap());
                *out_seq += 1;
                let ev = DapEvent::new(*out_seq, "initialized", None);
                out.push(serde_json::to_value(ev).unwrap());
                *out_seq += 1;
            }

            "launch" => {
                if let Some(args) = &req.arguments {
                    if let Ok(la) = serde_json::from_value::<LaunchArgs>(args.clone()) {
                        self.source = Some(DapSource {
                            name: Some(
                                std::path::Path::new(&la.program)
                                    .file_name().unwrap_or_default()
                                    .to_string_lossy().into_owned()
                            ),
                            path: Some(la.program.clone()),
                        });
                        self.stop_on_entry = la.stop_on_entry;
                    }
                }
                let resp = DapResponse::ok(*out_seq, rseq, "launch", None);
                out.push(serde_json::to_value(resp).unwrap());
                *out_seq += 1;

                if self.stop_on_entry {
                    self.runner.mode = RunMode::Paused;
                    let body = json!({
                        "reason": "entry", "description": "Stopped at entry",
                        "threadId": 1, "allThreadsStopped": true,
                    });
                    out.push(serde_json::to_value(
                        DapEvent::new(*out_seq, "stopped", Some(body))
                    ).unwrap());
                    *out_seq += 1;
                }
            }

            "configurationDone" => {
                let resp = DapResponse::ok(*out_seq, rseq, "configurationDone", None);
                out.push(serde_json::to_value(resp).unwrap());
                *out_seq += 1;
                if !self.stop_on_entry {
                    self.runner.mode = RunMode::Continue;
                    let events = self.run_vm_blocking(out_seq).await;
                    out.extend(events);
                }
            }

            "setFunctionBreakpoints" => {
                let mut resolved = HashSet::new();
                let mut bp_results: Vec<Value> = Vec::new();
                if let Some(args) = &req.arguments {
                    if let Ok(fba) = serde_json::from_value::<SetFunctionBreakpointsArgs>(args.clone()) {
                        for fb in &fba.breakpoints {
                            if let Some(addr) = self.symbols.addr_of(&fb.name) {
                                resolved.insert(addr);
                                bp_results.push(json!({
                                    "verified": true,
                                    "message": format!("{} -> 0x{:04X}", fb.name, addr),
                                }));
                                log::info!("Breakpoint set: {} = 0x{:04X}", fb.name, addr);
                            } else {
                                bp_results.push(json!({
                                    "verified": false,
                                    "message": format!("Label '{}' not found", fb.name),
                                }));
                            }
                        }
                    }
                }
                self.runner.set_breakpoints(resolved);
                let body = json!({ "breakpoints": bp_results });
                let resp = DapResponse::ok(*out_seq, rseq, "setFunctionBreakpoints", Some(body));
                out.push(serde_json::to_value(resp).unwrap());
                *out_seq += 1;
            }

            "setBreakpoints" => {
                let body = json!({ "breakpoints": [] });
                let resp = DapResponse::ok(*out_seq, rseq, "setBreakpoints", Some(body));
                out.push(serde_json::to_value(resp).unwrap());
                *out_seq += 1;
            }

            "continue" => {
                let body = json!({ "allThreadsContinued": true });
                let resp = DapResponse::ok(*out_seq, rseq, "continue", Some(body));
                out.push(serde_json::to_value(resp).unwrap());
                *out_seq += 1;
                self.runner.mode = RunMode::Continue;
                let events = self.run_vm_blocking(out_seq).await;
                out.extend(events);
            }

            "next" => {
                let resp = DapResponse::ok(*out_seq, rseq, "next", None);
                out.push(serde_json::to_value(resp).unwrap());
                *out_seq += 1;
                self.runner.mode = RunMode::StepOne;
                let events = self.run_vm_blocking(out_seq).await;
                out.extend(events);
            }

            "stepIn" => {
                let resp = DapResponse::ok(*out_seq, rseq, "stepIn", None);
                out.push(serde_json::to_value(resp).unwrap());
                *out_seq += 1;
                self.runner.mode = RunMode::StepOne;
                let events = self.run_vm_blocking(out_seq).await;
                out.extend(events);
            }

            "pause" => {
                // Signal the VM thread to stop at next CHECK_INTERVAL
                self.runner.pause_flag.store(true, Ordering::Relaxed);
                self.runner.mode = RunMode::Paused;
                let resp = DapResponse::ok(*out_seq, rseq, "pause", None);
                out.push(serde_json::to_value(resp).unwrap());
                *out_seq += 1;
                let pc = self.runner.pc();
                let body = json!({
                    "reason": "pause", "threadId": 1,
                    "allThreadsStopped": true,
                    "description": format!("Paused at PC=0x{:04X}", pc),
                });
                out.push(serde_json::to_value(
                    DapEvent::new(*out_seq, "stopped", Some(body))
                ).unwrap());
                *out_seq += 1;
            }

            "threads" => {
                let body = json!({ "threads": [{ "id": 1, "name": "TriskeleVM main" }] });
                let resp = DapResponse::ok(*out_seq, rseq, "threads", Some(body));
                out.push(serde_json::to_value(resp).unwrap());
                *out_seq += 1;
            }

            "stackTrace" => {
                let pc    = self.runner.pc();
                let label = self.symbols.label_at(pc)
                    .map(str::to_owned)
                    .unwrap_or_else(|| format!("0x{:04X}", pc));
                let frame = StackFrame {
                    id: 0, name: label,
                    source: self.source.clone(),
                    line: 1, column: 1,
                    instruction_pointer_reference: Some(format!("0x{:08X}", pc)),
                };
                let body = json!({
                    "stackFrames": [serde_json::to_value(&frame).unwrap()],
                    "totalFrames": 1,
                });
                let resp = DapResponse::ok(*out_seq, rseq, "stackTrace", Some(body));
                out.push(serde_json::to_value(resp).unwrap());
                *out_seq += 1;
            }

            "scopes" => {
                let scopes = vec![
                    json!({ "name": "Registers",  "variablesReference": VAR_REF_REGISTERS,   "expensive": false }),
                    json!({ "name": "Stack",      "variablesReference": VAR_REF_STACK,       "expensive": false }),
                    json!({ "name": "Disassembly","variablesReference": VAR_REF_DISASSEMBLY, "expensive": false }),
                ];
                let resp = DapResponse::ok(*out_seq, rseq, "scopes", Some(json!({ "scopes": scopes })));
                out.push(serde_json::to_value(resp).unwrap());
                *out_seq += 1;
            }

            "variables" => {
                let vref = req.arguments.as_ref()
                    .and_then(|a| a["variablesReference"].as_u64())
                    .unwrap_or(0) as u32;
                let vars = self.build_variables(vref);
                let resp = DapResponse::ok(*out_seq, rseq, "variables", Some(json!({ "variables": vars })));
                out.push(serde_json::to_value(resp).unwrap());
                *out_seq += 1;
            }

            "evaluate" => {
                let expr = req.arguments.as_ref()
                    .and_then(|a| a["expression"].as_str())
                    .unwrap_or("").trim().to_string();
                let result = self.evaluate_expr(&expr);
                let resp = DapResponse::ok(*out_seq, rseq, "evaluate",
                    Some(json!({ "result": result, "variablesReference": 0 })));
                out.push(serde_json::to_value(resp).unwrap());
                *out_seq += 1;
            }

            "disassemble" => {
                let pc    = self.runner.pc();
                let count = req.arguments.as_ref()
                    .and_then(|a| a["instructionCount"].as_u64())
                    .unwrap_or(11) as usize;
                let insns = disassemble_around(&self.bytecode, pc, count / 2, &self.symbols);
                let dap_insns: Vec<Value> = insns.iter().map(|i| json!({
                    "address":     format!("0x{:08X}", i.addr),
                    "instruction": i.text,
                    "symbol":      i.label,
                })).collect();
                let resp = DapResponse::ok(*out_seq, rseq, "disassemble",
                    Some(json!({ "instructions": dap_insns })));
                out.push(serde_json::to_value(resp).unwrap());
                *out_seq += 1;
            }

            "terminate" | "disconnect" => {
                self.runner.mode = RunMode::Terminated;
                let resp = DapResponse::ok(*out_seq, rseq, &req.command, None);
                out.push(serde_json::to_value(resp).unwrap());
                *out_seq += 1;
                out.push(serde_json::to_value(
                    DapEvent::new(*out_seq, "terminated", None)
                ).unwrap());
                *out_seq += 1;
            }

            cmd => {
                log::warn!("Unknown DAP command: {}", cmd);
                let resp = DapResponse::err(*out_seq, rseq, cmd,
                    &format!("tsk-dbg: unsupported command '{}'", cmd));
                out.push(serde_json::to_value(resp).unwrap());
                *out_seq += 1;
            }
        }

        out
    }

    // -------------------------------------------------------------------------
    // VM execution — spawn_blocking so DAP server stays responsive
    // -------------------------------------------------------------------------

    async fn run_vm_blocking(&mut self, out_seq: &mut u64) -> Vec<Value> {
        let mem_size = self.runner.state.memory.len();
        let max_insn = self.max_instructions;

        // Swap runner into blocking thread — avoids blocking the async DAP server
        let runner = std::mem::replace(&mut self.runner, VmRunner::new_empty(mem_size));

        let (cause, runner_back) = tokio::task::spawn_blocking(move || {
            let mut runner = runner;
            let cause = if max_insn > 0 {
                runner.run_until_stop_limited(max_insn)
            } else {
                runner.run_until_stop()
            };
            (cause, runner)
        }).await.unwrap_or_else(|e| {
            log::error!("spawn_blocking panicked: {:?}", e);
            (StopCause::Exception("VM thread panicked".into()), VmRunner::new_empty(mem_size))
        });

        self.runner = runner_back;
        *out_seq += 1;
        self.make_stopped_event(cause, out_seq)
    }

    fn make_stopped_event(&self, cause: StopCause, out_seq: &mut u64) -> Vec<Value> {
        let (reason, description) = match &cause {
            StopCause::Breakpoint(pc) => {
                let lbl = self.symbols.label_at(*pc)
                    .map(|l| format!(" ({})", l)).unwrap_or_default();
                ("breakpoint", format!("Breakpoint at 0x{:04X}{}", pc, lbl))
            }
            StopCause::Step(pc)     => ("step",      format!("Stepped to 0x{:04X}", pc)),
            StopCause::Pause(pc)    => ("pause",     format!("Paused at 0x{:04X}", pc)),
            StopCause::Entry        => ("entry",     "Stopped at entry".into()),
            StopCause::Halt         => ("exited",    "VM halted (F_Halt)".into()),
            StopCause::Exception(m) => ("exception", m.clone()),
        };

        if matches!(cause, StopCause::Halt) {
            return vec![serde_json::to_value(
                DapEvent::new(*out_seq, "terminated", Some(json!({ "restart": false })))
            ).unwrap()];
        }

        let body = json!({
            "reason": reason, "description": description,
            "threadId": 1, "allThreadsStopped": true,
        });
        vec![serde_json::to_value(DapEvent::new(*out_seq, "stopped", Some(body))).unwrap()]
    }

    // -------------------------------------------------------------------------
    // Variable builders
    // -------------------------------------------------------------------------

    fn build_variables(&self, vref: u32) -> Vec<Value> {
        match vref {
            VAR_REF_REGISTERS   => self.build_registers(),
            VAR_REF_STACK       => self.build_stack(),
            VAR_REF_DISASSEMBLY => self.build_disassembly(),
            r if r >= 10 && r < 42 => self.build_register_detail((r - 10) as usize),
            _ => vec![],
        }
    }

    fn build_registers(&self) -> Vec<Value> {
        let regs  = &self.runner.state.regs.r;
        let pc    = self.runner.pc();
        let flags = self.runner.state.regs.flags;

        let mut vars: Vec<Value> = (0..32usize).map(|i| {
            let v = regs[i];
            json!({
                "name": reg_alias(i),
                "value": format!("0x{:016X}  ({})", v, v as i64),
                "type": "u64",
                "variablesReference": reg_detail_ref(i),
            })
        }).collect();

        if let Some(label) = self.symbols.label_at(pc) {
            vars[31]["value"] = json!(format!("0x{:016X}  <- {}", pc, label));
        }

        vars.push(json!({
            "name": "FLAGS",
            "value": format!("ZF={} SF={} OF={} CF={}",
                (flags>>0)&1, (flags>>1)&1, (flags>>2)&1, (flags>>3)&1),
            "type": "u8",
            "variablesReference": 0,
        }));
        vars
    }

    fn build_register_detail(&self, reg: usize) -> Vec<Value> {
        let v     = self.runner.state.regs.r[reg];
        let fix   = v as i32;
        let fix_f = fix as f32 / 65536.0;
        vec![
            json!({ "name": "hex",     "value": format!("0x{:016X}", v),                             "variablesReference": 0 }),
            json!({ "name": "i64",     "value": format!("{}", v as i64),                              "variablesReference": 0 }),
            json!({ "name": "fixed16", "value": format!("{:.6}  (raw 0x{:08X})", fix_f, fix as u32), "variablesReference": 0 }),
            json!({ "name": "f32",     "value": format!("{:.6}", f32::from_bits(v as u32)),           "variablesReference": 0 }),
        ]
    }

    fn build_stack(&self) -> Vec<Value> {
        let sp      = self.runner.state.regs.sp();
        let mem_top = self.runner.state.memory.len() as u64;
        if sp >= mem_top.saturating_sub(8) { return vec![]; }
        let entries = self.runner.state.stack_peek_n(16);
        if entries.is_empty() { return vec![]; }
        entries.iter().enumerate().map(|(i, (addr, v))| {
            json!({
                "name":  format!("SP+{}", i * 8),
                "value": format!("0x{:016X}  ({})  @ 0x{:04X}", v, *v as i64, addr),
                "type":  "u64",
                "variablesReference": 0,
            })
        }).collect()
    }

    fn build_disassembly(&self) -> Vec<Value> {
        let pc    = self.runner.pc();
        let insns = disassemble_around(&self.bytecode, pc, 5, &self.symbols);
        insns.iter().map(|insn| {
            let marker = if insn.addr == pc { "► " } else { "  " };
            let label  = insn.label.as_deref()
                .map(|l| format!("\n{}:", l)).unwrap_or_default();
            json!({
                "name":  format!("0x{:04X}", insn.addr),
                "value": format!("{}0x{:04X}  {:08X}  {}{}", marker, insn.addr, insn.raw, label, insn.text),
                "variablesReference": 0,
            })
        }).collect()
    }

    // -------------------------------------------------------------------------
    // REPL
    // -------------------------------------------------------------------------

    fn evaluate_expr(&self, expr: &str) -> String {
        let parts: Vec<&str> = expr.split_whitespace().collect();
        if parts.is_empty() { return "(empty expression)".into(); }

        match parts[0].to_lowercase().as_str() {
            "pc" => {
                let pc  = self.runner.pc();
                let lbl = self.symbols.label_at(pc)
                    .map(|l| format!("  ; {}", l)).unwrap_or_default();
                format!("PC = 0x{:08X}{}", pc, lbl)
            }
            "flags" => {
                let f = self.runner.state.regs.flags;
                format!("ZF={} SF={} OF={} CF={}",
                    (f>>0)&1, (f>>1)&1, (f>>2)&1, (f>>3)&1)
            }
            "sym" => {
                if parts.len() < 2 { return "Usage: sym <label>".into(); }
                match self.symbols.addr_of(parts[1]) {
                    Some(a) => format!("{} = 0x{:08X}", parts[1], a),
                    None    => format!("Symbol '{}' not found", parts[1]),
                }
            }
            "mem" | "dump" => {
                if parts.len() < 3 { return "Usage: mem <hex_addr> <byte_count>".into(); }
                let addr  = parse_hex(parts[1]).unwrap_or(0) as usize;
                let count = parts[2].parse::<usize>().unwrap_or(16).min(256);
                let mem   = &self.runner.state.memory;
                let mut out = format!("Memory dump 0x{:04X} ({} bytes):\n", addr, count);
                for row in 0..(count + 15) / 16 {
                    let base = addr + row * 16;
                    if base >= mem.len() { break; }
                    let end  = (base + 16).min(mem.len()).min(addr + count);
                    out += &format!("  0x{:04X}  ", base);
                    for b in &mem[base..end] { out += &format!("{:02X} ", b); }
                    for _ in 0..(16 - (end - base)) { out += "   "; }
                    out += "  |";
                    for b in &mem[base..end] {
                        out.push(if b.is_ascii_graphic() { *b as char } else { '.' });
                    }
                    out += "|\n";
                }
                out
            }
            r_name => {
                if let Some(idx) = parse_reg_name(r_name) {
                    let v   = self.runner.state.regs.r[idx];
                    let fix = v as i32;
                    format!("{} = 0x{:016X}\n  i64   = {}\n  fixed = {:.6}\n  f32   = {}",
                        reg_alias(idx), v, v as i64,
                        fix as f32 / 65536.0, f32::from_bits(v as u32))
                } else {
                    format!("Unknown: '{}'\nTry: R4, pc, flags, sym <label>, mem 0x1000 32", expr)
                }
            }
        }
    }
}

// =============================================================================
// Free helpers
// =============================================================================

fn reg_alias(i: usize) -> String {
    match i {
        28 => "FP (R28)".into(), 29 => "SP (R29)".into(),
        30 => "LR (R30)".into(), 31 => "PC (R31)".into(),
        n  => format!("R{}", n),
    }
}

fn parse_reg_name(s: &str) -> Option<usize> {
    match s.to_lowercase().as_str() {
        "fp" | "r28" => Some(28), "sp" | "r29" => Some(29),
        "lr" | "r30" => Some(30), "pc" | "r31" => Some(31),
        other => other.strip_prefix('r')
            .and_then(|n| n.parse::<usize>().ok())
            .filter(|&n| n < 32),
    }
}

fn parse_hex(s: &str) -> Option<u64> {
    let s = s.trim();
    if let Some(h) = s.strip_prefix("0x").or_else(|| s.strip_prefix("0X")) {
        u64::from_str_radix(h, 16).ok()
    } else {
        s.parse::<u64>().ok()
    }
}


