// tsk-dbg/src/dap/types.rs
// Author: Echopraxium with the collaboration of Claude AI
//
// DAP (Debug Adapter Protocol) message types.
// Subset required for TriskeleVM debugging:
//   initialize, launch, setBreakpoints, configurationDone,
//   continue, next (stepOver), stepIn, pause, disconnect,
//   stackTrace, scopes, variables, evaluate (for memory dump)
//
// DAP spec: https://microsoft.github.io/debug-adapter-protocol/

use serde::{Deserialize, Serialize};
use serde_json::Value;

// ─────────────────────────────────────────────────────────────────────────────
// Base message envelope
// ─────────────────────────────────────────────────────────────────────────────

/// Every DAP message has a seq number and a type.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DapMessage {
    pub seq:  u64,
    #[serde(rename = "type")]
    pub kind: String,   // "request" | "response" | "event"
    #[serde(flatten)]
    pub body: Value,    // parsed further per kind
}

// ─────────────────────────────────────────────────────────────────────────────
// Request
// ─────────────────────────────────────────────────────────────────────────────

#[derive(Debug, Clone, Deserialize)]
pub struct DapRequest {
    pub seq:       u64,
    pub command:   String,
    pub arguments: Option<Value>,
}

// ─────────────────────────────────────────────────────────────────────────────
// Response
// ─────────────────────────────────────────────────────────────────────────────

#[derive(Debug, Clone, Serialize)]
pub struct DapResponse {
    pub seq:          u64,
    #[serde(rename = "type")]
    pub kind:         String,          // always "response"
    pub request_seq:  u64,
    pub success:      bool,
    pub command:      String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub message:      Option<String>,  // error message if !success
    #[serde(skip_serializing_if = "Option::is_none")]
    pub body:         Option<Value>,
}

impl DapResponse {
    pub fn ok(seq: u64, request_seq: u64, command: &str, body: Option<Value>) -> Self {
        Self {
            seq, kind: "response".into(), request_seq,
            success: true, command: command.into(), message: None, body,
        }
    }

    pub fn err(seq: u64, request_seq: u64, command: &str, msg: &str) -> Self {
        Self {
            seq, kind: "response".into(), request_seq,
            success: false, command: command.into(),
            message: Some(msg.into()), body: None,
        }
    }
}

// ─────────────────────────────────────────────────────────────────────────────
// Event
// ─────────────────────────────────────────────────────────────────────────────

#[derive(Debug, Clone, Serialize)]
pub struct DapEvent {
    pub seq:   u64,
    #[serde(rename = "type")]
    pub kind:  String,   // always "event"
    pub event: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub body:  Option<Value>,
}

impl DapEvent {
    pub fn new(seq: u64, event: &str, body: Option<Value>) -> Self {
        Self { seq, kind: "event".into(), event: event.into(), body }
    }
}

// ─────────────────────────────────────────────────────────────────────────────
// Specific request argument structs
// ─────────────────────────────────────────────────────────────────────────────

#[derive(Debug, Deserialize)]
pub struct InitializeArgs {
    #[serde(rename = "clientName")]
    pub client_name: Option<String>,
    #[serde(rename = "linesStartAt1")]
    pub lines_start_at1: Option<bool>,
}

#[derive(Debug, Deserialize)]
pub struct LaunchArgs {
    /// Path to .tvmx binary (passed from launch.json)
    pub program: String,
    /// Optional: path to .sym symbol table
    pub symbols: Option<String>,
    /// Stop at entry point before first instruction
    #[serde(rename = "stopOnEntry", default)]
    pub stop_on_entry: bool,
}

#[derive(Debug, Deserialize)]
pub struct SetBreakpointsArgs {
    pub source:      DapSource,
    pub breakpoints: Vec<SourceBreakpoint>,
}

#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct DapSource {
    pub name: Option<String>,
    pub path: Option<String>,
}

/// Breakpoint as sent by VS Code — we use `name` (label) via the hint field.
/// Since .tasm has no line numbers in .tvmx, we use the `column` as a label
/// lookup key OR the `name` field of a function breakpoint.
#[derive(Debug, Clone, Deserialize)]
pub struct SourceBreakpoint {
    pub line:      u32,
    pub column:    Option<u32>,
    /// Condition (e.g. "R4 == 5") — Phase 2
    pub condition: Option<String>,
}

/// Function breakpoint — used for label-based breakpoints.
#[derive(Debug, Clone, Deserialize)]
pub struct FunctionBreakpoint {
    pub name: String,   // label name, e.g. "ray_loop"
}

#[derive(Debug, Deserialize)]
pub struct SetFunctionBreakpointsArgs {
    pub breakpoints: Vec<FunctionBreakpoint>,
}

#[derive(Debug, Clone, Serialize)]
pub struct Breakpoint {
    pub id:       Option<u32>,
    pub verified: bool,
    pub message:  Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub line:     Option<u32>,
}

#[derive(Debug, Deserialize)]
pub struct StackTraceArgs {
    #[serde(rename = "threadId")]
    pub thread_id: u32,
    #[serde(rename = "startFrame")]
    pub start_frame: Option<u32>,
    pub levels:      Option<u32>,
}

#[derive(Debug, Clone, Serialize)]
pub struct StackFrame {
    pub id:     u32,
    pub name:   String,    // label or hex address
    pub source: Option<DapSource>,
    pub line:   u32,       // always 0 (no .tasm source correlation yet)
    pub column: u32,
    #[serde(rename = "instructionPointerReference")]
    pub instruction_pointer_reference: Option<String>,  // hex PC
}

#[derive(Debug, Clone, Serialize)]
pub struct Scope {
    pub name:                 String,
    #[serde(rename = "variablesReference")]
    pub variables_reference:  u32,   // handle for variables request
    pub expensive:            bool,
}

#[derive(Debug, Clone, Serialize)]
pub struct Variable {
    pub name:                String,
    pub value:               String,   // formatted for display
    #[serde(rename = "type")]
    pub var_type:            Option<String>,
    #[serde(rename = "variablesReference")]
    pub variables_reference: u32,      // 0 = leaf (no children)
}

#[derive(Debug, Deserialize)]
pub struct VariablesArgs {
    #[serde(rename = "variablesReference")]
    pub variables_reference: u32,
}

#[derive(Debug, Deserialize)]
pub struct EvaluateArgs {
    pub expression: String,
    #[serde(rename = "frameId")]
    pub frame_id:   Option<u32>,
    pub context:    Option<String>,   // "repl" | "watch" | "hover"
}

#[derive(Debug, Deserialize)]
pub struct ContinueArgs {
    #[serde(rename = "threadId")]
    pub thread_id: u32,
}

#[derive(Debug, Deserialize)]
pub struct NextArgs {
    #[serde(rename = "threadId")]
    pub thread_id: u32,
}

#[derive(Debug, Deserialize)]
pub struct StepInArgs {
    #[serde(rename = "threadId")]
    pub thread_id: u32,
}

// ─────────────────────────────────────────────────────────────────────────────
// Stopped event reasons
// ─────────────────────────────────────────────────────────────────────────────

pub enum StopReason {
    Breakpoint,
    Step,
    Pause,
    Entry,
    Exception,
}

impl StopReason {
    pub fn as_str(&self) -> &'static str {
        match self {
            Self::Breakpoint => "breakpoint",
            Self::Step       => "step",
            Self::Pause      => "pause",
            Self::Entry      => "entry",
            Self::Exception  => "exception",
        }
    }
}
