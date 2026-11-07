/* TSCG Kit — Tournesol (sunflower) workshop definition
 * A young sunflower as a negative feedback loop that tracks a moving target:
 * the gap between the light direction and the plant orientation drives a
 * growth that turns the plant. An internal clock turns it back east late at night.
 * Orientation in degrees: −90 = east, 0 = south, +90 = west.
 * Time unit: hours, one step = 5 minutes.
 * The definition is a factory: L(english, french) picks every text.
 * Author: Echopraxium with the collaboration of Claude AI
 */
(function (K) {
  "use strict";
  const syn = msg => ({ msg, tab: "synoptic" });
  const pan = msg => ({ msg, tab: "panel" });
  const hm = min => `${Math.floor(min / 60)} h ${String(Math.round(min % 60)).padStart(2, "0")}`;
  const orient = app => { const p = app.model.first("plante"); return p ? p.s.x : 0; };
  const coreWired = m => m.linked("plante", "level", "ecart", "b") && m.linked("ecart", "d", "croissance", "x") && m.linked("croissance", "flow", "plante", "in");

  const factory = L => {
    const dir = v => v < -10 ? L("east ", "est ") + Math.round(-v) + "°" : v > 10 ? L("west ", "ouest ") + Math.round(v) + "°" : L("due south", "plein sud");
    const KEEP = L("Keep the loop Gap → Growth → Plant → Gap.", "Garde la boucle Écart → Croissance → Plante → Écart.");
    return {
    id: "tournesol",
    title: L("TSCG Workshop — Sunflower", "Atelier TSCG — Tournesol"),
    pageTitle: L("TSCG Workshop — Sunflower", "TSCG Atelier — Tournesol"),
    fluxLabel: L("flux (rotation)", "flux (rotation)"),
    clock: { dt: 5 / 60, stepsPerSec: 12,
             fmt: t => `${L("day", "jour")} ${Math.floor(t / 24) + 1} · ${hm(Math.round((t % 24) * 60))}`,
             fmtSteps: n => hm(n * 5) },
    order: ["plante", "lampe", "ecart", "croissance", "soleil", "horloge"],
    home: { lampe: { x: 16, y: 20 }, soleil: { x: 16, y: 120 }, horloge: { x: 16, y: 220 },
            ecart: { x: 206, y: 20 }, croissance: { x: 396, y: 20 }, plante: { x: 396, y: 170 } },

    skins: {
      plante: { kind: "storage", icon: "plant", name: L("Plant", "Plante"), blurb: L("its orientation changes as it grows", "son orientation change en poussant"),
        ports: { in: L("rotation", "rotation"), out: "", level: L("orientation", "orientation") },
        describe: n => dir(n.s.x),
        params: { C: { v: 1, hidden: true }, k: { v: 0, hidden: true }, x0: { label: L("Start orientation (°)", "Orientation de départ (°)"), v: 0, step: 10, min: -90, max: 90 },
                  lo: { v: -110, hidden: true }, hi: { v: 110, hidden: true } } },
      lampe: { kind: "clock", icon: "lamp", mode: "fixed", name: L("Lamp", "Lampe"), blurb: L("a light that does not move", "une lumière qui ne bouge pas"),
        ports: { out: L("light", "lumière") }, describe: n => L("shines from ", "éclaire depuis ") + dir(n.p.angle),
        params: { angle: { label: L("Direction (°, −90 = east)", "Direction (°, −90 = est)"), v: 50, step: 10, min: -90, max: 90 } } },
      soleil: { kind: "clock", icon: "sun", mode: "sun", name: L("Sun", "Soleil"), blurb: L("crosses the sky from east to west", "traverse le ciel d'est en ouest"),
        ports: { out: L("light", "lumière") }, describe: n => n.s.v === null ? L("night", "nuit") : dir(n.s.v),
        params: { irr: { label: L("Irregular days", "Irrégularité des jours"), v: 0, step: 0.1, min: 0, max: 1 } } },
      horloge: { kind: "clock", icon: "clock", mode: "night", fallback: true, name: L("Clock", "Horloge"), blurb: L("an inner 24-hour rhythm", "un rythme intérieur de 24 h"),
        ports: { out: L("night call", "rappel nocturne") }, describe: n => n.s.v === null ? L("silent", "se tait") : L("calls back east", "rappelle vers l'est"),
        params: { angle: { label: L("Morning direction (°)", "Direction du matin (°)"), v: -90, step: 10, min: -90, max: 90 },
                  from: { label: L("Wakes at (h)", "Se réveille à (h)"), v: 1, step: 1, min: 0, max: 23 },
                  to: { label: L("Falls silent at (h)", "Se tait à (h)"), v: 6, step: 1, min: 0, max: 23 } } },
      ecart: { kind: "gradient", icon: "gap", name: L("Gap", "Écart"), blurb: L("compares light and orientation", "compare la lumière et l'orientation"),
        ports: { a: L("light (target)", "lumière (cible)"), b: L("orientation", "orientation"), d: L("gap", "écart") },
        describe: n => n.s.a === null ? L("nothing to aim at", "rien à viser") : L("gap ", "écart ") + Math.round(n.s.d) + "°",
        params: { noise: { label: L("Perception noise (°)", "Bruit de perception (°)"), v: 0, step: 5, min: 0, max: 90 } } },
      croissance: { kind: "transducer", icon: "growth", name: L("Growth", "Croissance"), blurb: L("grows more on one side than the other", "pousse plus d'un côté que de l'autre"),
        ports: { x: L("gap", "écart"), flow: L("rotation", "rotation") },
        describe: n => L("turns ", "tourne ") + Math.round(n.s.flow) + "°/h",
        params: { k: { label: L("Reactivity (/h)", "Réactivité (/h)"), v: 0.8, step: 0.1, min: 0, max: 4 },
                  max: { label: L("Max speed (°/h)", "Vitesse max (°/h)"), v: 40, step: 5, min: 5, max: 120 },
                  noise: { label: L("Growth noise (°/h)", "Bruit de croissance (°/h)"), v: 0, step: 5, min: 0, max: 120 } } }
    },

    instruments: {
      orientation: { type: "gauge", orient: "h", len: 7, label: L("Plant compass", "Boussole de la plante"), short: L("Orientation", "Orientation"), bind: { piece: "plante", get: "level" },
                     range: [-100, 100], center: 0, unit: "°", format: dir },
      jour:        { type: "lamp", label: L("Day / night light", "Témoin jour / nuit"), short: L("Day", "Jour"), bind: { piece: "soleil", get: "day" } },
      irregularite:{ type: "slider", label: L("Irregular days", "Irrégularité des jours"), short: L("Irregularity", "Irrégularité"), bind: { piece: "soleil", param: "irr" }, range: [0, 1], step: 0.1, decimals: 1, unit: "" },
      bruit:       { type: "slider", label: L("Perception noise", "Bruit de perception"), short: L("Noise", "Bruit"), bind: { piece: "ecart", param: "noise" }, range: [0, 90], step: 5, decimals: 0, unit: "°" },
      reactivite:  { type: "slider", label: L("Growth reactivity", "Réactivité de la croissance"), short: L("Reactivity", "Réactivité"), bind: { piece: "croissance", param: "k" }, range: [0, 4], step: 0.1, decimals: 1, unit: "/h" }
    },

    chart: {
      range: [-100, 100], tickY: 50, span: 72, tick: 12, label: t => (t % 24 === 0 ? L("d", "j") + (t / 24 + 1) : (t % 24) + " h"),
      series: [{ piece: "plante", label: L("Plant orientation", "Orientation de la plante"), color: "--flux", fmt: dir },
               { piece: "soleil", label: L("Sun direction", "Direction du soleil"), color: "#d4a017", fmt: dir },
               { piece: "lampe", label: L("Lamp direction", "Direction de la lampe"), color: "#d4a017", fmt: dir }],
      strips: [
        { label: L("night", "nuit"), color: "--info", shade: true, on: p => p.night },
        { label: L("clock active", "horloge active"), color: "--accent", on: (p, m) => { const h = m.first("horloge"); return !!(h && p.v[h.id] !== null && p.v[h.id] !== undefined); } }
      ]
    },

    steps: [
      { id: "lamp", title: L("A plant and a lamp", "Une plante et une lampe"),
        unlock: { pieces: ["plante", "lampe", "ecart", "croissance"], instruments: ["orientation"] },
        goal: L("In the <b>Synoptic</b>, place a <b>Plant</b>, a <b>Lamp</b>, a <b>Gap</b> and a <b>Growth</b>. Wire the Lamp's <i>light</i> and the Plant's <i>orientation</i> to the Gap, the Gap to the Growth, and the Growth's <i>rotation</i> to the Plant. Add the <b>compass</b> to the Panel, then start the time.",
                "Dans le <b>Synoptique</b>, pose une <b>Plante</b>, une <b>Lampe</b>, un <b>Écart</b> et une <b>Croissance</b>. Relie la <i>lumière</i> de la Lampe et l'<i>orientation</i> de la Plante à l'Écart, l'Écart à la Croissance, et la <i>rotation</i> de la Croissance à la Plante. Ajoute la <b>boussole</b> au Panneau, puis lance le temps."),
        hint: L("Four wires in all: two into the Gap, one into the Growth, one into the Plant.", "Quatre fils en tout : deux vers l'Écart, un vers la Croissance, un vers la Plante."),
        need: app => { const m = app.model;
          return !m.first("plante") || !m.first("lampe") || !m.first("ecart") || !m.first("croissance") ? syn(L("Place the four blocks: Plant, Lamp, Gap, Growth.", "Pose les quatre blocs : Plante, Lampe, Écart, Croissance.")) :
                 !m.linked("lampe", "out", "ecart", "a") ? syn(L("Wire the Lamp's light to the Gap (“light” input).", "Relie la lumière de la Lampe à l'Écart (entrée « lumière »).")) :
                 !m.linked("plante", "level", "ecart", "b") ? syn(L("Wire the Plant's orientation to the Gap.", "Relie l'orientation de la Plante à l'Écart.")) :
                 !m.linked("ecart", "d", "croissance", "x") ? syn(L("Wire the Gap to the Growth.", "Relie l'Écart à la Croissance.")) :
                 !m.linked("croissance", "flow", "plante", "in") ? syn(L("Wire the Growth's rotation to the Plant.", "Relie la rotation de la Croissance à la Plante.")) :
                 !app.panel.has("orientation") ? pan(L("Add the plant compass in the Panel.", "Ajoute la boussole de la plante dans le Panneau.")) : null; },
        check: (app, mem) => {
          const lamp = app.model.first("lampe"), ok = Math.abs(orient(app) - lamp.p.angle) < 5;
          mem.n = ok ? (mem.n || 0) + 1 : 0;
          return { p: mem.n / 12, done: mem.n >= 12, status: ok ? L("Facing the lamp… ", "Face à la lampe… ") + `${app.fmtSteps(mem.n)} / 1 h 00` : L("The plant is turning…", "La plante se tourne…") };
        },
        takeaway: L("The plant turns towards the lamp, quickly at first, then more and more slowly, and stops facing it. It is the same loop as the thermostat, but without on/off: the bigger the gap, the faster it turns.",
                    "La plante se tourne vers la lampe, vite d'abord, puis de plus en plus doucement, et s'arrête face à elle. C'est la même boucle que le thermostat, mais sans tout-ou-rien : plus l'écart est grand, plus elle tourne vite."),
        hood: L("Plant = <b>Storage</b> (its orientation accumulates). Gap = <b>Gradient</b>. Growth = <b>Transducer</b>, like Larsen's loudspeaker. Lamp = a still <b>Clock</b>.",
                "Plante = <b>Storage</b> (son orientation s'accumule). Écart = <b>Gradient</b>. Croissance = <b>Transducer</b>, comme le haut-parleur de Larsen. Lampe = <b>Clock</b> immobile.") },

      { id: "sun", title: L("Outside, the sun", "Dehors, le soleil"),
        unlock: { pieces: ["soleil"], instruments: ["jour"] },
        predict: { q: L("Before you start: at night, when the sun has gone, where will the plant face?", "Avant de lancer : la nuit, quand le soleil a disparu, où regardera la plante ?"),
                   choices: [L("East, ready for sunrise", "Vers l'est, prête pour le lever"), L("West, where the sun set", "Vers l'ouest, là où le soleil s'est couché"), L("Anywhere", "N'importe où")] },
        goal: L("Remove the Lamp (select it, press Delete) and place a <b>Sun</b> instead, wired to the Gap. Add the <b>day / night light</b>. Let a day and a half go by.",
                "Retire la Lampe (sélectionne-la, touche Suppr) et pose un <b>Soleil</b> à sa place, relié à l'Écart. Ajoute le <b>témoin jour / nuit</b>. Laisse passer un jour et demi."),
        hint: L("The ×1 button at the top speeds up time.", "Le bouton ×1 en haut accélère le temps."),
        need: app => { const m = app.model;
          return m.first("lampe") ? syn(L("Remove the Lamp: select it in the Synoptic, then press Delete.", "Retire la Lampe : sélectionne-la dans le Synoptique, puis touche Suppr.")) :
                 !m.first("soleil") ? syn(L("Place a Sun.", "Pose un Soleil.")) :
                 !m.linked("soleil", "out", "ecart", "a") ? syn(L("Wire the Sun's light to the Gap.", "Relie la lumière du Soleil à l'Écart.")) :
                 !coreWired(m) ? syn(KEEP) :
                 !app.panel.has("jour") ? pan(L("Add the day / night light in the Panel.", "Ajoute le témoin jour / nuit dans le Panneau.")) : null; },
        check: K.elapse(36 * 12),
        takeaway: L("By day, the plant follows the sun, always slightly behind. But at night it has nothing to aim at: it stays turned west, and misses the sunrise.",
                    "Le jour, la plante suit le soleil, toujours avec un peu de retard. Mais la nuit, elle n'a plus rien à viser : elle reste tournée vers l'ouest, et elle rate le lever du soleil."),
        hood: L("Sun = <b>Clock</b>: a rhythm imposed from outside. Without light, the Gap has no target and the loop stops.",
                "Soleil = <b>Clock</b> : un rythme imposé du dehors. Sans lumière, l'Écart n'a plus de cible et la boucle s'arrête.") },

      { id: "clock", title: L("An inner clock", "Une horloge intérieure"),
        unlock: { pieces: ["horloge"] },
        goal: L("Place a <b>Clock</b> and wire it, too, to the Gap's <i>light</i> input. Wait for the next sunrise.",
                "Pose une <b>Horloge</b> et relie-la, elle aussi, à l'entrée <i>lumière</i> de l'Écart. Attends le prochain lever du soleil."),
        hint: L("The Clock wakes up late at night, and only counts when the sun is silent.", "L'Horloge se réveille en fin de nuit, et ne compte que quand le soleil se tait."),
        need: app => { const m = app.model;
          return !m.first("horloge") ? syn(L("Place a Clock.", "Pose une Horloge.")) :
                 !m.linked("horloge", "out", "ecart", "a") ? syn(L("Wire the Clock to the Gap's “light” input.", "Relie l'Horloge à l'entrée « lumière » de l'Écart.")) :
                 !m.linked("soleil", "out", "ecart", "a") ? syn(L("Keep the Sun wired to the Gap too.", "Garde aussi le Soleil relié à l'Écart.")) :
                 !coreWired(m) ? syn(KEEP) : null; },
        check: (app, mem) => {
          const night = app.model.env.night;
          if (mem.prev === true && !night) mem.mornings = (mem.mornings || []).concat([orient(app)]);
          mem.prev = night;
          const good = (mem.mornings || []).some(v => v < -55);
          return { p: good ? 1 : night ? 0.5 : 0.2, done: good,
            status: night ? L("Night… watch where the plant turns.", "Nuit… regarde où se tourne la plante.") :
                    (mem.mornings || []).length ? L("That morning it was not ready: wait for the next one.", "Ce matin-là, elle n'était pas prête : attends le suivant.") : L("Wait for the night, then the sunrise.", "Attends la nuit, puis le lever du soleil.") };
        },
        takeaway: L("Late at night, the plant turns back east, before the sun even returns: it anticipates. The young sunflower really does this, thanks to an inner clock.",
                    "En fin de nuit, la plante se retourne vers l'est, avant même que le soleil revienne : elle anticipe. Le jeune tournesol fait réellement cela, grâce à une horloge interne."),
        hood: L("Clock = an inner <b>Clock</b>, wired as a fallback: it only counts when the light is silent. A loop, plus the memory of a rhythm.",
                "Horloge = <b>Clock</b> intérieure, branchée en secours : elle ne compte que quand la lumière se tait. Une boucle, plus la mémoire d'un rythme.") },

      { id: "irregular", title: L("Irregular days", "Des jours irréguliers"),
        unlock: { instruments: ["irregularite", "bruit"] },
        predict: { q: L("If the days become irregular, sometimes short, sometimes long, will the plant still follow the sun?", "Si les jours deviennent irréguliers, tantôt courts, tantôt longs, la plante suivra-t-elle encore le soleil ?"),
                   choices: [L("Yes, just as well", "Oui, toujours aussi bien"), L("By day yes, but some mornings it will not be ready", "Le jour oui, mais certains matins elle sera mal préparée"), L("No, it gets completely lost", "Non, elle se perd complètement")] },
        goal: L("Add the <b>irregular days</b> slider to the Panel and push it past the middle. Let three days go by while watching the scale model and the curves.",
                "Ajoute le curseur d'<b>irrégularité des jours</b> au Panneau et pousse-le au-delà de la moitié. Laisse passer trois jours en regardant la Maquette et les courbes."),
        hint: L("You can also add the noise slider, and look for the point where the plant starts to wander.", "Tu peux aussi ajouter le curseur de bruit, et chercher à partir d'où la plante erre."),
        need: app => { const m = app.model, s = m.first("soleil");
          return !s || !m.linked("soleil", "out", "ecart", "a") || !coreWired(m) ? syn(L("Keep the Sun and the loop wired.", "Garde le Soleil et la boucle reliés.")) :
                 !app.panel.has("irregularite") ? pan(L("Add the irregular days slider in the Panel.", "Ajoute le curseur d'irrégularité des jours dans le Panneau.")) :
                 s.p.irr < 0.6 ? pan(L("Push the irregularity past the middle.", "Pousse l'irrégularité au-delà de la moitié.")) : null; },
        check: K.elapse(72 * 12),
        takeaway: L("By day, the loop corrects whatever the sun does: the plant still follows. But the clock, set on a fixed rhythm, gets the time wrong some mornings. What works well in a regular world can fail when the rhythm breaks down.",
                    "Le jour, la boucle corrige quoi que fasse le soleil : la plante suit encore. Mais l'horloge, réglée sur un rythme fixe, se trompe d'heure certains matins. Ce qui marche bien dans un monde régulier peut échouer quand le rythme se dérègle."),
        hood: L("Each mechanism has its domain of validity: the loop tolerates irregularity, the clock assumes there is none.",
                "Chaque mécanisme a son domaine de validité : la boucle tolère les irrégularités, l'horloge les suppose absentes.") }
    ],

    final: {
      title: L("The plant that follows the sun", "La plante qui suit le soleil"),
      text: L("Regulating towards a fixed set point (the thermostat) and pursuing a moving target (the sunflower) are the same negative loop. It also serves the eye following a ball, the autopilot holding a heading, the antenna tracking a satellite. And when the target is predictable, a clock lets you anticipate.",
              "Réguler vers une consigne fixe (le thermostat) et poursuivre une cible qui bouge (le tournesol), c'est la même boucle négative. Elle sert aussi à l'œil qui suit une balle, au pilote automatique qui garde un cap, à l'antenne qui suit un satellite. Et quand la cible est prévisible, une horloge permet d'anticiper."),
      questions: [],
      hood: L("Generic blocks used: Storage, Gradient, Transducer, Clock. Transducer was already in Larsen.",
              "Blocs génériques utilisés : Storage, Gradient, Transducer, Clock. Transducer était déjà dans Larsen.")
    },

    free: {
      text: L("Every block and slider is unlocked. Try: does a very reactive plant follow better, or does it start shaking with noise? Put the Lamp back next to the Sun: which one wins? How much noise before the plant wanders at random?",
              "Tous les blocs et tous les curseurs sont débloqués. Essaie : une plante très réactive suit-elle mieux, ou se met-elle à trembler avec du bruit ? Remets la Lampe à côté du Soleil : qui l'emporte ? Jusqu'où peut aller le bruit avant que la plante erre au hasard ?"),
      hood: L("The same assembly, with other names: a tracking antenna, an eye, a cruise control.",
              "Le même assemblage, avec d'autres noms : une antenne de poursuite, un œil, un régulateur de vitesse.")
    },

    // ---------------------------------------------------------------- scale model
    // A young sunflower in a pot. Outdoors: a sky that goes from day to night (sun with
    // rays, hills, twinkling stars, a crescent moon). Indoors (lamp only): a lit room.
    view: function (host, model, api) {
      const rnd = (i, k) => { const s = Math.sin(i * 91.7 + k * 47.3) * 43758.5453; return s - Math.floor(s); };
      const stars = Array.from({ length: 70 }, (_, i) => ({ x: 6 + rnd(i, 1) * 428, y: 6 + rnd(i, 2) * 175, r: 0.5 + rnd(i, 3) * 1.4, w: 1 + rnd(i, 4) * 3, ph: rnd(i, 5) * 6.28 }));
      const seeds = Array.from({ length: 120 }, (_, i) => { const a = i * 2.39996, r = 1.25 * Math.sqrt(i); return `<circle cx="${(r * Math.cos(a)).toFixed(2)}" cy="${(r * Math.sin(a)).toFixed(2)}" r="${(0.55 + i / 400).toFixed(2)}"/>`; }).join("");
      const petals = (n, len, wid, rot, cls) => Array.from({ length: n }, (_, i) =>
        `<path class="${cls}" transform="rotate(${(i * 360 / n + rot).toFixed(1)})" d="M0 -12 C${wid} -${12 + len * 0.35} ${wid * 0.7} -${12 + len * 0.85} 0 -${12 + len} C-${wid * 0.7} -${12 + len * 0.85} -${wid} -${12 + len * 0.35} 0 -12 Z"/>`).join("");
      const grass = Array.from({ length: 90 }, (_, i) => { const x = i * 4.9 + rnd(i, 7) * 3, h = 4 + rnd(i, 8) * 7; return `M${x.toFixed(1)} 252 q${(rnd(i, 9) * 4 - 2).toFixed(1)} -${(h / 2).toFixed(1)} ${(rnd(i, 6) * 3 - 1.5).toFixed(1)} -${h.toFixed(1)}`; }).join(" ");
      host.innerHTML = `
<svg viewBox="0 0 440 300" role="img" preserveAspectRatio="xMidYMid meet">
  <defs>
    <clipPath id="tsClip"><rect x="0" y="0" width="440" height="300" rx="12"/></clipPath>
    <linearGradient id="tsDay" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3f8ee0"/><stop offset="1" stop-color="#cfe9f8"/></linearGradient>
    <linearGradient id="tsNight" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#070b24"/><stop offset=".7" stop-color="#1b1a45"/><stop offset="1" stop-color="#3a2a55"/></linearGradient>
    <linearGradient id="tsDusk" x1="0" y1="0" x2="0" y2="1"><stop offset=".35" stop-color="#ff9a4d" stop-opacity="0"/><stop offset="1" stop-color="#ff8a3d" stop-opacity=".85"/></linearGradient>
    <radialGradient id="tsSunGlow"><stop offset="0" stop-color="#fff6c2" stop-opacity=".95"/><stop offset=".35" stop-color="#ffd34d" stop-opacity=".55"/><stop offset="1" stop-color="#ffd34d" stop-opacity="0"/></radialGradient>
    <radialGradient id="tsLampGlow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#fff1b0" stop-opacity=".85"/><stop offset="1" stop-color="#fff1b0" stop-opacity="0"/></radialGradient>
    <linearGradient id="tsGrass" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6fae4f"/><stop offset="1" stop-color="#3f7a33"/></linearGradient>
    <linearGradient id="tsPetal" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#e48a12"/><stop offset=".55" stop-color="#f7c22b"/><stop offset="1" stop-color="#ffe066"/></linearGradient>
    <radialGradient id="tsDiscGrad"><stop offset="0" stop-color="#3b2312"/><stop offset=".75" stop-color="#5a3518"/><stop offset="1" stop-color="#7a4a1e"/></radialGradient>
    <linearGradient id="tsStemGrad" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#2f6b2a"/><stop offset=".5" stop-color="#5a9e45"/><stop offset="1" stop-color="#2f6b2a"/></linearGradient>
    <linearGradient id="tsPot" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#9a4f2b"/><stop offset=".45" stop-color="#c86b3c"/><stop offset="1" stop-color="#8a4326"/></linearGradient>
    <filter id="tsBlur" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="9"/></filter>
    <mask id="tsMoonMask"><rect x="300" y="20" width="60" height="60" fill="#fff"/><circle cx="337" cy="45" r="13" fill="#000"/></mask>
  </defs>
  <g clip-path="url(#tsClip)">
    <g id="tsOutdoor">
      <rect x="0" y="0" width="440" height="300" fill="url(#tsDay)"/>
      <rect id="tsNightSky" x="0" y="0" width="440" height="300" fill="url(#tsNight)"/>
      <rect id="tsDuskSky" x="0" y="0" width="440" height="300" fill="url(#tsDusk)"/>
      <ellipse id="tsMilky" cx="230" cy="80" rx="240" ry="26" fill="#c9c3ff" opacity=".12" filter="url(#tsBlur)" transform="rotate(-14 230 80)"/>
      <g id="tsStars" fill="#ffffff">${stars.map((s, i) => `<circle data-i="${i}" cx="${s.x.toFixed(1)}" cy="${s.y.toFixed(1)}" r="${s.r.toFixed(2)}"/>`).join("")}</g>
      <circle id="tsMoon" cx="328" cy="48" r="14" fill="#f3efd9" mask="url(#tsMoonMask)"/>
      <path d="M40 240 A 180 165 0 0 1 400 240" fill="none" stroke="#ffffff" stroke-opacity=".18" stroke-dasharray="3 6"/>
      <g id="tsSun">
        <circle r="46" fill="url(#tsSunGlow)"/>
        <g id="tsRays" stroke="#ffd34d" stroke-width="2.2" stroke-linecap="round">${Array.from({ length: 12 }, (_, i) => `<line x1="0" y1="-22" x2="0" y2="-30" transform="rotate(${i * 30})"/>`).join("")}</g>
        <circle r="15" fill="#ffe27a" stroke="#ffc93a" stroke-width="2"/>
      </g>
      <path id="tsHill2" d="M0 236 C60 214 120 222 180 232 C250 244 310 214 440 226 V300 H0 Z"/>
      <path id="tsHill1" d="M0 246 C80 236 150 242 220 247 C300 252 370 238 440 244 V300 H0 Z"/>
    </g>
    <g id="tsIndoor">
      <rect x="0" y="0" width="440" height="300" fill="#e8dfcc"/>
            <rect x="0" y="246" width="440" height="54" fill="#b79c7a"/>
      <line x1="0" y1="246" x2="440" y2="246" stroke="#9b8162" stroke-width="2"/>
      <circle id="tsLampGlowSpot" r="120" fill="url(#tsLampGlow)"/>
    </g>
    <g id="tsLamp">
      <line x1="0" y1="12" x2="0" y2="96" stroke="#6e6a60" stroke-width="3"/>
      <ellipse cx="0" cy="98" rx="16" ry="4" fill="#6e6a60"/>
      <path d="M-20 -8 L20 -8 L12 12 L-12 12 Z" fill="#c9a24a" stroke="#6e6a60" stroke-width="1.5"/>
      <circle cx="0" cy="13" r="6" fill="#fff6c8"/>
    </g>
    <rect id="tsGround" x="0" y="250" width="440" height="50" fill="url(#tsGrass)"/>
    <path id="tsGrassBlades" d="${grass}" stroke="#4f8f3c" stroke-width="1.2" fill="none" stroke-linecap="round"/>
    <text id="tsEast" class="mq-note" x="18" y="291"></text>
    <text id="tsWest" class="mq-note" x="422" y="291" text-anchor="end"></text>
    <g id="tsPlant">
      <path id="tsStem" fill="none" stroke="url(#tsStemGrad)" stroke-width="6" stroke-linecap="round"/>
      <g id="tsLeafL"><path d="M0 0 C-10 -12 -34 -14 -44 -4 C-34 6 -12 8 0 0 Z" fill="#4e9a3f" stroke="#2f6b2a" stroke-width="1"/><path d="M0 0 C-14 -4 -28 -5 -40 -4" stroke="#2f6b2a" stroke-width="1" fill="none"/></g>
      <g id="tsLeafR"><path d="M0 0 C10 -12 34 -16 46 -6 C36 5 12 8 0 0 Z" fill="#58a646" stroke="#2f6b2a" stroke-width="1"/><path d="M0 0 C14 -5 30 -6 42 -6" stroke="#2f6b2a" stroke-width="1" fill="none"/></g>
      <g id="tsHead">
        <g id="tsHeadInner">
          <g fill="#3f7d32">${Array.from({ length: 10 }, (_, i) => `<path transform="rotate(${i * 36 + 18})" d="M0 -10 L4 -26 L0 -22 L-4 -26 Z"/>`).join("")}</g>
          <g fill="url(#tsPetal)" stroke="#d98b12" stroke-width=".6">${petals(16, 24, 7, 11, "pb")}</g>
          <g fill="url(#tsPetal)" stroke="#d98b12" stroke-width=".6">${petals(16, 22, 6.5, 0, "pf")}</g>
          <circle r="15" fill="url(#tsDiscGrad)" stroke="#3b2312" stroke-width="1"/>
          <g fill="#2a170a">${seeds}</g>
        </g>
      </g>
      <path d="M190 252 H250 L244 288 Q220 293 196 288 Z" fill="url(#tsPot)" stroke="#6e3a1f" stroke-width="1.2"/>
      <rect x="186" y="246" width="68" height="9" rx="2.5" fill="#c46a3a" stroke="#6e3a1f" stroke-width="1.2"/>
      <ellipse cx="220" cy="248" rx="30" ry="3.2" fill="#3a2516"/>
    </g>
    <text id="tsEmpty" class="mq-note" x="220" y="150" text-anchor="middle"></text>
  </g>
</svg>`;
      const $ = id => host.querySelector("#" + id);
      const mix = (a, b, t) => `rgb(${a.map((v, i) => Math.round(v + (b[i] - v) * t)).join(",")})`;
      const starEls = [...host.querySelectorAll("#tsStars circle")];
      let head = 0, rays = 0, last = performance.now();
      const sunPos = az => { const f = (az + 90) / 180; return { x: 40 + 360 * f, y: 240 - 165 * Math.sin(Math.PI * f) }; };

      return {
        update(running) {
          const now = performance.now(), dtR = Math.min(0.1, (now - last) / 1000); last = now;
          const plant = model.first("plante"), sun = model.first("soleil"), lamp = model.first("lampe");
          host.querySelector("svg").setAttribute("aria-label", K.L("Scale model: a young sunflower in a pot, the sky and the light", "Maquette : un jeune tournesol en pot, le ciel et la lumière"));
          $("tsEast").textContent = K.L("East", "Est"); $("tsWest").textContent = K.L("West", "Ouest");
          $("tsEmpty").textContent = K.L("Place a Plant in the Synoptic.", "Pose une Plante dans le Synoptique.");
          const outdoor = !!sun;
          let daylight = 1;
          if (outdoor) daylight = sun.s.v === null ? 0 : Math.min(1, Math.sin(Math.PI * (sun.s.v + 90) / 180) * 2.2 + 0.15);
          $("tsOutdoor").style.display = outdoor ? "" : "none";
          $("tsIndoor").style.display = outdoor ? "none" : "";
          if (outdoor) {
            const night = 1 - daylight;
            $("tsNightSky").setAttribute("opacity", night.toFixed(3));
            $("tsDuskSky").setAttribute("opacity", (daylight > 0 && daylight < 0.85 ? Math.sin(Math.PI * daylight / 0.85) * 0.8 : 0).toFixed(3));
            $("tsMilky").setAttribute("opacity", (0.14 * night).toFixed(3));
            const t = now / 1000;
            starEls.forEach((el, i) => { const s = stars[i]; el.setAttribute("opacity", (night * (0.55 + 0.45 * Math.sin(t * s.w + s.ph))).toFixed(2)); });
            $("tsMoon").setAttribute("opacity", (night * 0.95).toFixed(2));
            $("tsHill2").setAttribute("fill", mix([28, 40, 50], [128, 170, 120], daylight));
            $("tsHill1").setAttribute("fill", mix([22, 34, 30], [98, 150, 86], daylight));
            $("tsSun").style.display = sun.s.v !== null ? "" : "none";
            if (sun.s.v !== null) {
              const p = sunPos(sun.s.v);
              if (running) rays = (rays + dtR * 8) % 360;
              $("tsSun").setAttribute("transform", `translate(${p.x.toFixed(1)} ${p.y.toFixed(1)})`);
              $("tsRays").setAttribute("transform", `rotate(${rays.toFixed(1)})`);
            }
          }
          $("tsGround").setAttribute("opacity", outdoor ? (0.35 + 0.65 * daylight).toFixed(2) : "0");
          $("tsGrassBlades").style.display = outdoor ? "" : "none";
          const ink = outdoor && daylight < 0.4 ? "#d8d5cc" : "#2f2d27";
          $("tsEast").style.fill = ink; $("tsWest").style.fill = ink;
          $("tsLamp").style.display = lamp ? "" : "none";
          if (lamp) {
            const p = sunPos(lamp.p.angle);
            $("tsLamp").setAttribute("transform", `translate(${p.x.toFixed(1)} ${(p.y + 30).toFixed(1)}) scale(${outdoor ? 0.8 : 1})`);
            $("tsLampGlowSpot").setAttribute("cx", p.x.toFixed(1)); $("tsLampGlowSpot").setAttribute("cy", (p.y + 45).toFixed(1));
          }
          $("tsEmpty").style.display = plant ? "none" : "";
          $("tsPlant").style.display = plant ? "" : "none";
          $("tsPlant").style.filter = outdoor && daylight < 0.95 ? `brightness(${(0.42 + 0.58 * daylight).toFixed(2)}) saturate(${(0.55 + 0.45 * daylight).toFixed(2)})` : "";
          if (!plant) return;
          head += (plant.s.x - head) * 0.25;
          const a = Math.max(-100, Math.min(100, head)) / 90;          // −1 east … +1 west
          const hx = 220 + 52 * a, hy = 108 + 14 * Math.abs(a);
          $("tsStem").setAttribute("d", `M220 248 C221 205 ${(220 + 26 * a).toFixed(1)} 168 ${hx.toFixed(1)} ${(hy + 8).toFixed(1)}`);
          $("tsLeafL").setAttribute("transform", `translate(${(220.5 + 4 * a).toFixed(1)} 214) rotate(${(-8 + 6 * a).toFixed(1)})`);
          $("tsLeafR").setAttribute("transform", `translate(${(221 + 10 * a).toFixed(1)} 190) rotate(${(6 + 6 * a).toFixed(1)})`);
          const sx = 1 - 0.62 * Math.min(1, Math.abs(a));              // the face turns away from us
          $("tsHead").setAttribute("transform", `translate(${hx.toFixed(1)} ${hy.toFixed(1)}) rotate(${(a * 16).toFixed(1)})`);
          $("tsHeadInner").setAttribute("transform", `scale(${sx.toFixed(3)} 1)`);
        }
      };
    }
  };
  };

  (K.workshops = K.workshops || {}).tournesol = factory;
})(window.TSCGKit = window.TSCGKit || {});
