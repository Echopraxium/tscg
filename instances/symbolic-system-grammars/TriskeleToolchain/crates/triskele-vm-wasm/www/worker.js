// worker.js — TriskeleVM VM worker
// Author: Echopraxium with the collaboration of Claude AI

import init, { worker_entry } from './pkg/triskele_vm_wasm.js';

// Initialise the WASM module — pass the .wasm URL explicitly so the worker
// can resolve it correctly regardless of how import.meta.url is handled.
// The .wasm file sits next to the .js glue in pkg/.
const wasmUrl = new URL('./pkg/triskele_vm_wasm_bg.wasm', import.meta.url);
await init(wasmUrl);

console.log('[VM worker] WASM initialised, waiting for start message');

// Wait for the start message from the main thread.
self.addEventListener('message', (event) => {
    const { type, tvmxBytes, sab } = event.data;
    if (type !== 'start') return;

    console.log('[VM worker] received start, bytes=', tvmxBytes.length);

    try {
        worker_entry(tvmxBytes, sab);
    } catch(e) {
        console.error('[VM worker] worker_entry threw:', e);
        self.postMessage({ type: 'halted', exitCode: -1 });
    }
}, { once: true });
