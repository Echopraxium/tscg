# Vendored libraries

Third-party code kept locally so the poclet has fewer remote points of
failure and keeps working offline. Not TSCG code — do not edit.

| File | Version | Licence | Size | Why local |
|---|---|---|---|---|
| `qrcode.js` | 1.4.4 | MIT | 57 KB | **Strictly essential** — no QR means no poclet. Must not depend on a CDN. UTF-8 capable, so accented and non-Latin input encodes correctly. |
| `earcut.min.js` | 2.2.4 | ISC | 7 KB | BabylonJS needs it for `ExtrudePolygon`, used to build the arch tunnels. Small enough that vendoring costs nothing. |

Source in both cases:

```
npm install qrcode-generator@1.4.4   →  node_modules/qrcode-generator/qrcode.js
npm install earcut@2.2.4             →  node_modules/earcut/dist/earcut.min.js
```

`qrcode.js` ships unminified — the package has no minified build. 57 KB is
acceptable for a local file and keeps the source readable.

## Deliberately still remote

| Resource | Why not vendored |
|---|---|
| BabylonJS (`cdn.babylonjs.com`) | ~4 MB. The whole poclet family loads it from the CDN by convention; vendoring it per poclet would be wasteful. |
| Cantata One (Google Fonts) | Webfonts are the accepted CDN exception. Absence degrades sign typography to a fallback serif, nothing more. |

## Degradation behaviour

| Missing | Consequence |
|---|---|
| `qrcode.js` | Fatal — startup reports the failure in the diagnostic console |
| BabylonJS | Fatal — same |
| `earcut.min.js` | Arch tunnels disabled, city otherwise intact |
| Cantata One | Signs fall back to a serif face |
