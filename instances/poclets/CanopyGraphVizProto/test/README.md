# Canopée — smoke test

`node test/boot-smoke.js` (run from the project root) loads the three modules in browser
order against stubbed DOM and BabylonJS, then exercises every arrangement, slice isolation
and folding.

It exists because a refactor once removed `buildSlices`, `renderSliceLabels` and
`buildStubs` while deleting a neighbouring block: the files still passed `node --check`,
since a syntax check cannot see a call to a function that was never defined. Only running
the initialisation catches that class of error.

Run it after any surgery on `src/canopy-core.js`.
