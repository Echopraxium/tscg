// tsk-dbg/src/dap/server.rs
// Author: Echopraxium with the collaboration of Claude AI
//
// TCP DAP server — accepts one VS Code connection and runs the debug session.
// Protocol: HTTP-like headers + JSON body, each message on its own.
//
//   Content-Length: <N>\r\n
//   \r\n
//   { ... JSON DAP message ... }

use tokio::net::TcpListener;
use tokio::io::{AsyncBufReadExt, AsyncReadExt, AsyncWriteExt, BufReader};
use std::sync::Arc;
use tokio::sync::Mutex;

use crate::dap::types::*;
use crate::session::DebugSession;
use crate::symbols::SymbolTable;

/// Run the DAP TCP server. Blocks until the session ends.
pub async fn run_server(
    addr:             String,
    bytecode:         Vec<u8>,
    symbols:          SymbolTable,
    mem_size:         usize,
    max_instructions: u64,
) -> anyhow::Result<()> {
    let listener = TcpListener::bind(&addr).await?;

    // Accept exactly one connection (VS Code)
    let (socket, peer) = listener.accept().await?;
    log::info!("DAP client connected: {}", peer);

    let (reader, writer) = tokio::io::split(socket);
    let writer = Arc::new(Mutex::new(writer));

    let session = Arc::new(Mutex::new(
        DebugSession::new(bytecode, symbols, mem_size, max_instructions, writer.clone())
    ));

    let mut buf_reader = BufReader::new(reader);
    let mut seq_counter: u64 = 1;

    loop {
        // ── Read DAP message ──────────────────────────────────────────────────
        let content_length = read_content_length(&mut buf_reader).await?;
        if content_length == 0 {
            log::info!("DAP connection closed by client.");
            break;
        }

        let mut body_buf = vec![0u8; content_length];
        buf_reader.read_exact(&mut body_buf).await?;
        let body_str = String::from_utf8_lossy(&body_buf);

        log::debug!("← DAP recv: {}", body_str);

        let request: DapRequest = match serde_json::from_str(&body_str) {
            Ok(r)  => r,
            Err(e) => {
                log::error!("DAP parse error: {} — raw: {}", e, body_str);
                continue;
            }
        };

        // ── Dispatch to session ───────────────────────────────────────────────
        let mut sess = session.lock().await;
        let responses = sess.handle_request(&request, &mut seq_counter).await;
        drop(sess);

        // ── Send all responses/events ─────────────────────────────────────────
        for msg in responses {
            send_message(&writer, &msg).await?;
            seq_counter += 1;
        }

        // Exit cleanly on disconnect
        if request.command == "disconnect" {
            log::info!("DAP disconnect — shutting down.");
            break;
        }
    }

    Ok(())
}

// ─────────────────────────────────────────────────────────────────────────────
// DAP framing helpers
// ─────────────────────────────────────────────────────────────────────────────

/// Read "Content-Length: N\r\n\r\n" header. Returns N (0 = EOF).
async fn read_content_length<R>(reader: &mut BufReader<R>) -> anyhow::Result<usize>
where R: tokio::io::AsyncRead + Unpin
{
    let mut length = 0usize;
    let mut line   = String::new();

    loop {
        line.clear();
        let n = reader.read_line(&mut line).await?;
        if n == 0 { return Ok(0); }  // EOF

        let trimmed = line.trim();
        if trimmed.is_empty() {
            // blank line = end of headers
            break;
        }
        if let Some(val) = trimmed.strip_prefix("Content-Length:") {
            length = val.trim().parse::<usize>()?;
        }
        // ignore other headers (Content-Type etc.)
    }

    Ok(length)
}

/// Serialize a value and send it with DAP framing.
async fn send_message<T, W>(writer: &Arc<Mutex<W>>, msg: &T) -> anyhow::Result<()>
where
    T: serde::Serialize,
    W: tokio::io::AsyncWrite + Unpin,
{
    let json = serde_json::to_string(msg)?;
    log::debug!("→ DAP send: {}", json);

    let frame = format!("Content-Length: {}\r\n\r\n{}", json.len(), json);
    let mut w  = writer.lock().await;
    w.write_all(frame.as_bytes()).await?;
    w.flush().await?;
    Ok(())
}
