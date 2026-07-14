/* tslint:disable */
/* eslint-disable */

/**
 * Create the stdin SAB — call this on the main thread, then transfer to the
 * worker via postMessage.
 */
export function create_stdin_sab(): SharedArrayBuffer;

/**
 * Non-interactive one-shot run — stdin = EOF (patch-1 behaviour preserved).
 */
export function run_tvmx(tvmx_bytes: Uint8Array): string;

/**
 * Interactive VM worker entry point — called by worker.js.
 * Receives the .tvmx bytes and the stdin SAB.
 * Sends postMessage events to the main thread hub:
 *   { type: "output",   text: "…" }
 *   { type: "needInput" }
 *   { type: "halted",   exitCode: N }
 */
export function worker_entry(tvmx_bytes: Uint8Array, sab: SharedArrayBuffer): void;

export type InitInput = RequestInfo | URL | Response | BufferSource | WebAssembly.Module;

export interface InitOutput {
    readonly memory: WebAssembly.Memory;
    readonly create_stdin_sab: () => any;
    readonly run_tvmx: (a: number, b: number) => [number, number];
    readonly worker_entry: (a: number, b: number, c: any) => void;
    readonly __wbindgen_exn_store: (a: number) => void;
    readonly __externref_table_alloc: () => number;
    readonly __wbindgen_externrefs: WebAssembly.Table;
    readonly __wbindgen_malloc: (a: number, b: number) => number;
    readonly __wbindgen_free: (a: number, b: number, c: number) => void;
    readonly __wbindgen_start: () => void;
}

export type SyncInitInput = BufferSource | WebAssembly.Module;

/**
 * Instantiates the given `module`, which can either be bytes or
 * a precompiled `WebAssembly.Module`.
 *
 * @param {{ module: SyncInitInput }} module - Passing `SyncInitInput` directly is deprecated.
 *
 * @returns {InitOutput}
 */
export function initSync(module: { module: SyncInitInput } | SyncInitInput): InitOutput;

/**
 * If `module_or_path` is {RequestInfo} or {URL}, makes a request and
 * for everything else, calls `WebAssembly.instantiate` directly.
 *
 * @param {{ module_or_path: InitInput | Promise<InitInput> }} module_or_path - Passing `InitInput` directly is deprecated.
 *
 * @returns {Promise<InitOutput>}
 */
export default function __wbg_init (module_or_path?: { module_or_path: InitInput | Promise<InitInput> } | InitInput | Promise<InitInput>): Promise<InitOutput>;
