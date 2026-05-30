"""
launcher.py — TscgOntologyExplorer Smart Launcher
==================================================
If port 8000 is already in use, shows a dialog offering:
  A. Kill the existing server → start normally on port 8000
  B. Start in-memory on port 8001

Communicates via environment variables to the npm start sub-shell.

Usage   : python launcher.py  (called by launch.bat)
Location: instances/tscg-tools/TscgOntologyExplorer/

Env vars set in child process:
  TSCG_API_PORT       — port to use (8000 or 8001)
  TSCG_API_IN_MEMORY  — "true" if store should be in-memory

Author  : Echopraxium with the collaboration of Claude AI
Version : 1.2.0
"""

import os, sys, socket, subprocess, time
from pathlib import Path

SCRIPT_DIR    = Path(__file__).parent.resolve()
SERVER_PORT   = 8000
FALLBACK_PORT = 8001
HOST          = "127.0.0.1"
NPM           = "npm.cmd" if sys.platform == "win32" else "npm"


# ── Helpers ───────────────────────────────────────────────────────────────────

def is_port_busy(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        try:    s.connect((HOST, port)); return True
        except: return False


def find_pids(port: int) -> list[int]:
    pids = []
    try:
        cmd = ["netstat", "-ano", "-p", "TCP"] if sys.platform == "win32"               else ["lsof", "-t", f"-i:{port}", "-sTCP:LISTEN"]
        enc = "cp1252" if sys.platform == "win32" else "utf-8"
        out = subprocess.check_output(cmd, encoding=enc, errors="replace",
                                      stderr=subprocess.DEVNULL)
        if sys.platform == "win32":
            for line in out.splitlines():
                if f":{port}" in line and "LISTENING" in line:
                    parts = line.split()
                    try: pids.append(int(parts[-1]))
                    except: pass
        else:
            for p in out.strip().splitlines():
                try: pids.append(int(p))
                except: pass
    except: pass
    return list(set(pids))


def kill_pids(pids: list[int]):
    """Kill all processes holding the port (re-query after each kill)."""
    print(f"[launcher] kill_pids called with: {pids}")
    if sys.platform == "win32":
        # Kill by image name (python.exe) that holds the port — most reliable
        # Also kill process tree for each PID
        for pid in pids:
            subprocess.call(
                ["taskkill", "/F", "/T", "/PID", str(pid)],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
        # Re-check and kill any remaining process on the port
        remaining = find_pids(SERVER_PORT)
        for pid in remaining:
            subprocess.call(
                ["taskkill", "/F", "/T", "/PID", str(pid)],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
    else:
        import signal
        for pid in pids:
            try: os.killpg(os.getpgid(pid), signal.SIGKILL)
            except: pass


def npm_start(extra_env: dict):
    """Launch npm start in current shell with extra env vars."""
    env = os.environ.copy()
    env.update(extra_env)
    subprocess.Popen([NPM, "start"], cwd=str(SCRIPT_DIR), env=env).wait()


# ── Dialog ────────────────────────────────────────────────────────────────────

def show_dialog(pids: list[int]) -> str:
    """Show conflict dialog. Returns 'kill' | 'inmemory' | 'cancel'."""
    import tkinter as tk

    root = tk.Tk()
    root.withdraw()
    choice = {"v": "cancel"}

    dlg = tk.Toplevel(root)
    dlg.title("TscgOntologyExplorer — Port Conflict")
    dlg.resizable(False, False)
    dlg.grab_set()
    dlg.attributes("-topmost", True)

    W, H = 460, 220
    sw = dlg.winfo_screenwidth()
    sh = dlg.winfo_screenheight()
    dlg.geometry(f"{W}x{H}+{(sw-W)//2}+{(sh-H)//2}")

    pid_str = ", ".join(str(p) for p in pids) or "unknown"

    tk.Label(dlg, text="⚠️", font=("Segoe UI", 24), fg="#e67e22").pack(pady=(14, 0))
    tk.Label(dlg, text=f"Port {SERVER_PORT} is already in use  (PID: {pid_str})",
             font=("Segoe UI", 10, "bold")).pack()
    tk.Label(dlg, text="TscgOntologyAPIServer may already be running.",
             font=("Segoe UI", 9), fg="#666").pack(pady=(2, 12))

    f = tk.Frame(dlg); f.pack()

    def pick(v):
        choice["v"] = v
        dlg.destroy()

    tk.Button(f,
        text=f"A — Kill existing server → start on port {SERVER_PORT}",
        command=lambda: pick("kill"),
        width=44, font=("Segoe UI", 9),
        bg="#e74c3c", fg="white", activebackground="#c0392b",
        relief="flat", cursor="hand2"
    ).pack(pady=3)

    tk.Button(f,
        text=f"B — Start in-memory on port {FALLBACK_PORT}  (no persistence)",
        command=lambda: pick("inmemory"),
        width=44, font=("Segoe UI", 9),
        bg="#2980b9", fg="white", activebackground="#1a6a9a",
        relief="flat", cursor="hand2"
    ).pack(pady=3)

    tk.Button(f,
        text="Cancel",
        command=lambda: pick("cancel"),
        width=44, font=("Segoe UI", 9),
        bg="#95a5a6", fg="white",
        relief="flat", cursor="hand2"
    ).pack(pady=3)

    dlg.protocol("WM_DELETE_WINDOW", lambda: pick("cancel"))
    root.wait_window(dlg)
    root.destroy()
    return choice["v"]


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print(f"[launcher] Checking {HOST}:{SERVER_PORT}…")

    if not is_port_busy(SERVER_PORT):
        # Port free — silent start
        npm_start({"TSCG_API_PORT": str(SERVER_PORT), "TSCG_API_IN_MEMORY": "false"})
        return

    pids = find_pids(SERVER_PORT)
    print(f"[launcher] Port {SERVER_PORT} busy — PIDs found: {pids}")
    print(f"[launcher] Raw netstat output for port {SERVER_PORT}:")
    try:
        out = subprocess.check_output(["netstat", "-ano", "-p", "TCP"],
                                      encoding="cp1252", errors="replace",
                                      stderr=subprocess.DEVNULL)
        for line in out.splitlines():
            if f":{SERVER_PORT}" in line and "LISTENING" in line:
                print(f"  {line.strip()}")
    except Exception as e:
        print(f"  netstat error: {e}")

    choice = show_dialog(pids)

    if choice == "cancel":
        print("[launcher] Cancelled.")

    elif choice == "kill":
        print(f"[launcher] Killing {pids}…")
        kill_pids(pids)
        time.sleep(3.0)
        if is_port_busy(SERVER_PORT):
            import tkinter as tk
            from tkinter import messagebox
            tk.Tk().withdraw()
            messagebox.showerror("TscgOntologyExplorer",
                f"Could not free port {SERVER_PORT}.\n"
                "Please close the existing instance manually.")
        else:
            npm_start({"TSCG_API_PORT": str(SERVER_PORT), "TSCG_API_IN_MEMORY": "false"})

    elif choice == "inmemory":
        npm_start({"TSCG_API_PORT": str(FALLBACK_PORT), "TSCG_API_IN_MEMORY": "true"})


if __name__ == "__main__":
    main()
