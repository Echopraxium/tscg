/* TSCG Kit — icons.js
 * Line icons for blocks (24×24, stroke = currentColor). A skin names its icon with
 * `icon: "<name>"`; without one, the generic kind gives a fallback.
 * - K.iconSvg(name, cls)   HTML <svg> string (palette, panel)
 * - K.iconPath(name)       the path data alone (drawn inside the Synoptic SVG)
 * Author: Echopraxium with the collaboration of Claude AI
 */
(function (K) {
  "use strict";
  const P = {
    // thermostat workshop
    room: "M3 11 L12 4 L21 11 M5 9.5 V20 H19 V9.5 M10 20 V15 H14 V20",
    wall: "M3 5 H21 V19 H3 Z M3 9.7 H21 M3 14.3 H21 M9 5 V9.7 M15 5 V9.7 M6 9.7 V14.3 M12 9.7 V14.3 M18 9.7 V14.3 M9 14.3 V19 M15 14.3 V19",
    heater: "M12 3 C15.5 7 17.5 9.5 17.5 13.5 A5.5 5.5 0 0 1 6.5 13.5 C6.5 10.5 8.5 9 9.8 7 C10.8 9 11.8 10 12 3 Z M12 20 C10.3 20 9.5 18.8 9.5 17.5 C9.5 16 10.7 15.2 12 13.5 C13.3 15.2 14.5 16 14.5 17.5 C14.5 18.8 13.7 20 12 20 Z",
    thermostat: "M5 3 H19 A1 1 0 0 1 20 4 V20 A1 1 0 0 1 19 21 H5 A1 1 0 0 1 4 20 V4 A1 1 0 0 1 5 3 Z M12 7 A4 4 0 1 1 11.99 7 M12 11 L14.5 8.8 M9 18 H15",
    radiator: "M6 5 V19 M10 5 V19 M14 5 V19 M18 5 V19 M4 8 H20 M4 16 H20 M5 21 V19 M19 21 V19",
    // larsen workshop
    hall: "M3 20 H21 M5 20 V9 M19 20 V9 M3 9 L12 4 L21 9 M9 20 V14 H15 V20 M8 11.5 H8.01 M16 11.5 H16.01",
    voice: "M8 9 A3 3 0 1 1 7.99 9 M2.5 20 C3 15.5 13 15.5 13.5 20 M16 7.5 Q18 10.5 16 13.5 M18.8 5 Q22.5 10.5 18.8 16",
    amp: "M5 4.5 L19.5 12 L5 19.5 Z M1.5 12 H5 M19.5 12 H22.5 M8 12 H12 M10 10 V14",
    speaker: "M3.5 9 H7.5 L12.5 5 V19 L7.5 15 H3.5 Z M15.5 9 Q17.5 12 15.5 15 M18.2 6.5 Q22 12 18.2 17.5",
    // sunflower workshop
    plant: "M12 21 V11 M12 14 C12 9 8.5 7 4 7 C4 11 7 14 12 14 M12 11.5 C12 7.5 15 5.5 20 5.5 C20 9.5 17 11.5 12 11.5 M8 21 H16",
    lamp: "M8.5 3.5 H15.5 L19 10.5 H5 Z M12 10.5 V19 M8 20.5 H16 M12 13 L12 13.01",
    sun: "M12 8 A4 4 0 1 1 11.99 8 M12 2 V4.5 M12 19.5 V22 M2 12 H4.5 M19.5 12 H22 M4.9 4.9 L6.7 6.7 M17.3 17.3 L19.1 19.1 M4.9 19.1 L6.7 17.3 M17.3 6.7 L19.1 4.9",
    clock: "M12 3 A9 9 0 1 1 11.99 3 M12 7 V12 L15.5 14",
    gap: "M12 4 L20.5 19.5 H3.5 Z M12 10 V14 M12 16.8 V16.81",
    growth: "M4 20 C10 20 14 16.5 16 6.5 M12.3 8.5 L16 5.2 L19.5 8.8",
    // drinking-bird workshop
    bird: "M9 4.5 A3 3 0 1 1 8.99 4.5 M11.8 7 L16 7.8 L11.7 8.6 M9 10.5 V16 M9 20.5 A3.2 3.2 0 1 1 9.01 20.5 M9 13 L5 21 M9 13 L13 21",
    head: "M4 12 A6 6 0 1 0 16 12 A6 6 0 1 0 4 12 M16 11 L21.5 12.5 L15.8 14 M8.5 10.5 H8.51",
    evap: "M12 21 C9 21 7.5 19 7.5 17 C7.5 14.5 12 10.5 12 10.5 C12 10.5 16.5 14.5 16.5 17 C16.5 19 15 21 12 21 Z M8 7 Q9.5 5.5 8 4 M12 7 Q13.5 5.5 12 4 M16 7 Q17.5 5.5 16 4",
    tilt: "M3 15 L21 7 M12 11 L8.5 20 H15.5 Z",
    drain: "M9 3 V13 M15 3 V13 M12 8 V20 M8.5 16.5 L12 20 L15.5 16.5",
    felt: "M5 15 A7 7 0 0 1 19 15 Z M7 19 H17 M8 11 L6.8 9 M12 9 V6.8 M16 11 L17.2 9",
    glass: "M6 4 H18 L16.5 20 H7.5 Z M7 10 H17",
    // generic fallbacks
    storage: "M5 6 C5 4.3 19 4.3 19 6 V18 C19 19.7 5 19.7 5 18 Z M5 6 C5 7.7 19 7.7 19 6 M5 12 C5 13.7 19 13.7 19 12",
    sink: "M4 5 H20 L14 13 V19 H10 V13 Z",
    source: "M12 3 V14 M7.5 9.5 L12 14 L16.5 9.5 M5 20 H19",
    threshold: "M3 18 H10 V6 H21",
    amplify: "M5 4.5 L19.5 12 L5 19.5 Z",
    transducer: "M3 12 H8 M16 12 H21 M8 7 H16 V17 H8 Z M10 12 L14 12",
    gradient: "M12 4 L20.5 19.5 H3.5 Z"
  };
  K.ICONS = P;
  K.iconPath = name => P[name] || P.storage;
  K.iconSvg = (name, cls) =>
    `<svg class="${cls || "k-icon"}" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="${K.iconPath(name)}"/></svg>`;
  K.iconOf = skin => skin.icon || skin.kind;
})(window.TSCGKit = window.TSCGKit || {});
