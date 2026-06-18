// vscode-triskele/src/extension.js
// Author: Echopraxium with the collaboration of Claude AI
// Version: 0.1.2 — removed checkPort (was consuming the single tsk-dbg connection)

'use strict';

const vscode = require('vscode');
const cp     = require('child_process');
const path   = require('path');

let tskDbgProcess = null;

function activate(context) {
    console.log('[triskele-debug] extension activated — v0.1.2');

    const factory = new TriskeleDebugAdapterFactory();
    context.subscriptions.push(
        vscode.debug.registerDebugAdapterDescriptorFactory('triskele', factory)
    );

    context.subscriptions.push(
        vscode.debug.registerDebugConfigurationProvider('triskele', {
            resolveDebugConfiguration(folder, config) {
                console.log('[triskele-debug] resolveDebugConfiguration:', JSON.stringify(config));
                if (!config.program) {
                    const editor = vscode.window.activeTextEditor;
                    if (editor && editor.document.languageId === 'tasm') {
                        const tasmPath = editor.document.uri.fsPath;
                        config.program = tasmPath.replace(/\.tasm$/, '.tvmx');
                        config.symbols = tasmPath.replace(/\.tasm$/, '.sym');
                    }
                }
                return config;
            }
        })
    );
}

function deactivate() {
    if (tskDbgProcess) {
        tskDbgProcess.kill();
        tskDbgProcess = null;
    }
}

class TriskeleDebugAdapterFactory {
    async createDebugAdapterDescriptor(session, executable) {
        const config = session.configuration;
        const port   = config.port || 4711;

        console.log(`[triskele-debug] createDebugAdapterDescriptor — port=${port}`);
        console.log(`[triskele-debug] program=${config.program}`);

        // Auto-launch tsk-dbg if requested
        if (config.autoLaunchDebugger) {
            if (!config.tskDbgPath) {
                vscode.window.showErrorMessage(
                    'TriskeleVM: autoLaunchDebugger=true requires tskDbgPath in launch.json'
                );
                return null;
            }
            await launchTskDbg(config, port);
        }

        // Connect directly — no checkPort (would consume the single tsk-dbg connection)
        console.log(`[triskele-debug] connecting to 127.0.0.1:${port}`);
        return new vscode.DebugAdapterServer(port, '127.0.0.1');
    }
}

function launchTskDbg(config, port) {
    return new Promise((resolve, reject) => {
        const args = [config.program];
        if (config.symbols) { args.push('--symbols', config.symbols); }
        args.push('--port', String(port));

        console.log(`[triskele-debug] spawning: ${config.tskDbgPath} ${args.join(' ')}`);

        tskDbgProcess = cp.spawn(config.tskDbgPath, args, {
            cwd:   path.dirname(config.program),
            stdio: ['ignore', 'pipe', 'pipe'],
        });

        tskDbgProcess.stdout.on('data', d => console.log('[tsk-dbg stdout]', d.toString().trim()));
        tskDbgProcess.stderr.on('data', d => console.log('[tsk-dbg stderr]', d.toString().trim()));
        tskDbgProcess.on('error', err => {
            vscode.window.showErrorMessage(`Failed to launch tsk-dbg: ${err.message}`);
            reject(err);
        });

        // Wait 1.5s for tsk-dbg to start listening
        setTimeout(resolve, 1500);
    });
}

module.exports = { activate, deactivate };
