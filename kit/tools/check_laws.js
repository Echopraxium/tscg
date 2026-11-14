#!/usr/bin/env node
/* TSCG Kit — check_laws.js
 * Rule (kit/ENGINE_SCOPE.md, "Rules for workshops" #2): no physics outside K.LAWS.
 * The Maquette, the Panel and the curves read the model (n.s, w.power); they never
 * recompute a law.
 *
 * Heuristic, line by line, on every workshop.js:
 *   FAIL  a line that combines a law parameter (n.p.k, n.p.C, …) with a state value
 *         (n.s.…) in arithmetic: that is a law being recomputed outside the engine.
 *   WARN  a line that writes a state value directly (n.s.x = …), bypassing the model
 *         (acceptable for a scenario's initial condition; say so with the marker).
 * A line can be exempted with a trailing comment  // law-ok: <reason>
 * Reading a parameter alone (to display a set point) is fine.
 *
 * Usage: node kit/tools/check_laws.js [files…]   (default: every workshop.js)
 * Exit code 1 when there is at least one FAIL.
 * Author: Echopraxium with the collaboration of Claude AI
 */
"use strict";
const fs = require("fs"), path = require("path");

const ROOT = path.resolve(__dirname, "..", "..");
// the law parameters are the ones K.LAWS reads: load sim.js in a stub window and collect them
function lawParams() {
  const src = fs.readFileSync(path.join(ROOT, "kit", "lib", "sim.js"), "utf8");
  const start = src.indexOf("const LAWS = {"), end = src.indexOf("const ENGINE = [");
  if (start < 0 || end < 0) throw new Error("check_laws: K.LAWS not found in kit/lib/sim.js");
  const block = src.slice(start, end), names = new Set();
  for (const m of block.matchAll(/\.p\.([A-Za-z_]\w*)/g)) names.add(m[1]);
  return names;
}

function defaultFiles() {
  const out = [];
  for (const d of fs.readdirSync(path.join(ROOT, "kit"))) {
    const f = path.join(ROOT, "kit", d, "workshop.js");
    if (fs.existsSync(f)) out.push(f);
  }
  const pocl = path.join(ROOT, "instances", "poclets");
  if (fs.existsSync(pocl)) for (const d of fs.readdirSync(pocl)) {
    const f = path.join(pocl, d, "static", "src", "workshop.js");
    if (fs.existsSync(f)) out.push(f);
  }
  return out;
}

function check(file, params) {
  const found = [];
  const pRe = new RegExp(`\\.p\\.(${[...params].join("|")})\\b`);
  fs.readFileSync(file, "utf8").split("\n").forEach((line, i) => {
    if (/\/\/\s*law-ok:/.test(line)) return;
    // strip comments and string contents ("gain ×" + n.p.gain is display, not arithmetic)
    const code = line.replace(/\/\/.*$/, "").replace(/(["'`])(?:\\.|(?!\1).)*\1/g, '""');
    const p = code.match(pRe);
    const arith = p && (new RegExp(`\\.p\\.${p[1]}\\b\\s*[-+*/](?!\\s*"")`).test(code) ||
                        new RegExp(`(?<!""\\s*)[-+*/]\\s*[\\w.]*\\.p\\.${p[1]}\\b`).test(code));
    // a law parameter used in arithmetic on a line that also reads model state
    if (arith && /\.s\.\w+/.test(code))
      found.push({ level: "FAIL", file, line: i + 1, why: `recomputes a law with parameter .p.${p[1]} and state`, text: line.trim() });
    else if (/\.s\.\w+\s*=[^=]/.test(code))
      found.push({ level: "WARN", file, line: i + 1, why: "writes model state directly", text: line.trim() });
  });
  return found;
}

const params = lawParams();
const files = process.argv.length > 2 ? process.argv.slice(2).map(f => path.resolve(f)) : defaultFiles();
const all = files.flatMap(f => check(f, params));
for (const r of all) console.log(`${r.level}  ${path.relative(ROOT, r.file)}:${r.line}  ${r.why}\n      ${r.text.slice(0, 160)}`);
const fails = all.filter(r => r.level === "FAIL").length;
console.log(`check_laws: ${files.length} file(s), ${fails} FAIL, ${all.length - fails} WARN — ${fails ? "FAIL" : "PASS"}`);
process.exit(fails ? 1 : 0);
