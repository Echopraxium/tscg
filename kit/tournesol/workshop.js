/* TSCG Kit — Tournesol workshop definition
 * A young sunflower as a negative feedback loop that tracks a moving target:
 * the gap between the light direction and the plant orientation drives a
 * growth that turns the plant. An internal clock turns it back east at night.
 * Orientation in degrees: −90 = east, 0 = south, +90 = west.
 * Time unit: hours, one step = 5 minutes.
 * Author: Echopraxium with the collaboration of Claude AI
 */
(function (K) {
  "use strict";
  const syn = msg => ({ msg, tab: "synoptic" });
  const pan = msg => ({ msg, tab: "panel" });
  const hm = min => `${Math.floor(min / 60)} h ${String(Math.round(min % 60)).padStart(2, "0")}`;
  const orient = app => { const p = app.model.first("plante"); return p ? p.s.x : 0; };
  const dir = v => v < -10 ? `est ${Math.round(-v)}°` : v > 10 ? `ouest ${Math.round(v)}°` : "plein sud";
  const coreWired = m => m.linked("plante", "level", "ecart", "b") && m.linked("ecart", "d", "croissance", "x") && m.linked("croissance", "flow", "plante", "in");

  const W = {
    id: "tournesol",
    title: "Atelier TSCG — Tournesol",
    pageTitle: "TSCG Atelier — Tournesol",
    fluxLabel: "flux (rotation)",
    clock: { dt: 5 / 60, stepsPerSec: 12,
             fmt: t => `jour ${Math.floor(t / 24) + 1} · ${hm(Math.round((t % 24) * 60))}`,
             fmtSteps: n => hm(n * 5) },
    order: ["plante", "lampe", "ecart", "croissance", "soleil", "horloge"],
    home: { lampe: { x: 16, y: 24 }, soleil: { x: 16, y: 140 }, horloge: { x: 16, y: 256 },
            ecart: { x: 236, y: 24 }, croissance: { x: 456, y: 24 }, plante: { x: 456, y: 210 } },

    skins: {
      plante: { kind: "storage", name: "Plante", blurb: "son orientation change en poussant",
        ports: { in: "rotation", out: "", level: "orientation" },
        describe: n => dir(n.s.x),
        params: { C: { v: 1, hidden: true }, k: { v: 0, hidden: true }, x0: { label: "Orientation de départ (°)", v: 0, step: 10, min: -90, max: 90 },
                  lo: { v: -110, hidden: true }, hi: { v: 110, hidden: true } } },
      lampe: { kind: "clock", mode: "fixed", name: "Lampe", blurb: "une lumière qui ne bouge pas",
        ports: { out: "lumière" }, describe: n => "éclaire depuis l'" + dir(n.p.angle),
        params: { angle: { label: "Direction (°, −90 = est)", v: 50, step: 10, min: -90, max: 90 } } },
      soleil: { kind: "clock", mode: "sun", name: "Soleil", blurb: "traverse le ciel d'est en ouest",
        ports: { out: "lumière" }, describe: n => n.s.v === null ? "nuit" : "à l'" + dir(n.s.v),
        params: { irr: { label: "Irrégularité des jours", v: 0, step: 0.1, min: 0, max: 1 } } },
      horloge: { kind: "clock", mode: "night", fallback: true, name: "Horloge", blurb: "un rythme intérieur de 24 h",
        ports: { out: "rappel nocturne" }, describe: n => n.s.v === null ? "se tait" : "rappelle vers l'est",
        params: { angle: { label: "Direction du matin (°)", v: -90, step: 10, min: -90, max: 90 },
                  from: { label: "Se réveille à (h)", v: 1, step: 1, min: 0, max: 23 },
                  to: { label: "Se tait à (h)", v: 6, step: 1, min: 0, max: 23 } } },
      ecart: { kind: "gradient", name: "Écart", blurb: "compare la lumière et l'orientation",
        ports: { a: "lumière (cible)", b: "orientation", d: "écart" },
        describe: n => n.s.a === null ? "rien à viser" : "écart " + Math.round(n.s.d) + "°",
        params: { noise: { label: "Bruit de perception (°)", v: 0, step: 5, min: 0, max: 90 } } },
      croissance: { kind: "transducer", name: "Croissance", blurb: "pousse plus d'un côté que de l'autre",
        ports: { x: "écart", flow: "rotation" },
        describe: n => "tourne " + Math.round(n.s.flow) + "°/h",
        params: { k: { label: "Réactivité (/h)", v: 0.8, step: 0.1, min: 0, max: 4 },
                  max: { label: "Vitesse max (°/h)", v: 40, step: 5, min: 5, max: 120 },
                  noise: { label: "Bruit de croissance (°/h)", v: 0, step: 5, min: 0, max: 120 } } }
    },

    instruments: {
      orientation: { type: "gauge", orient: "h", len: 7, label: "Boussole de la plante", short: "Orientation", bind: { piece: "plante", get: "level" },
                     range: [-100, 100], center: 0, unit: "°", format: dir },
      jour:        { type: "lamp", label: "Témoin jour / nuit", short: "Jour", bind: { piece: "soleil", get: "day" } },
      irregularite:{ type: "slider", label: "Irrégularité des jours", short: "Irrégularité", bind: { piece: "soleil", param: "irr" }, range: [0, 1], step: 0.1, decimals: 1, unit: "" },
      bruit:       { type: "slider", label: "Bruit de perception", short: "Bruit", bind: { piece: "ecart", param: "noise" }, range: [0, 90], step: 5, decimals: 0, unit: "°" },
      reactivite:  { type: "slider", label: "Réactivité de la croissance", short: "Réactivité", bind: { piece: "croissance", param: "k" }, range: [0, 4], step: 0.1, decimals: 1, unit: "/h" }
    },

    chart: {
      range: [-100, 100], tickY: 50, span: 72, tick: 12, label: t => (t % 24 === 0 ? "j" + (t / 24 + 1) : (t % 24) + " h"),
      series: [{ piece: "plante", label: "Orientation de la plante", color: "--flux" },
               { piece: "soleil", label: "Direction du soleil", color: "#d4a017" },
               { piece: "lampe", label: "Direction de la lampe", color: "#d4a017" }],
      strips: [
        { label: "nuit", color: "--info", shade: true, on: p => p.night },
        { label: "horloge active", color: "--accent", on: (p, m) => { const h = m.first("horloge"); return !!(h && p.v[h.id] !== null && p.v[h.id] !== undefined); } }
      ]
    },

    steps: [
      { id: "lamp", title: "Une plante et une lampe",
        unlock: { pieces: ["plante", "lampe", "ecart", "croissance"], instruments: ["orientation"] },
        goal: "Dans le <b>Synoptique</b>, pose une <b>Plante</b>, une <b>Lampe</b>, un <b>Écart</b> et une <b>Croissance</b>. Relie la <i>lumière</i> de la Lampe et l'<i>orientation</i> de la Plante à l'Écart, l'Écart à la Croissance, et la <i>rotation</i> de la Croissance à la Plante. Ajoute la <b>boussole</b> au Panneau, puis lance le temps.",
        hint: "Quatre fils en tout : deux vers l'Écart, un vers la Croissance, un vers la Plante.",
        need: app => { const m = app.model;
          return !m.first("plante") || !m.first("lampe") || !m.first("ecart") || !m.first("croissance") ? syn("Pose les quatre pièces : Plante, Lampe, Écart, Croissance.") :
                 !m.linked("lampe", "out", "ecart", "a") ? syn("Relie la lumière de la Lampe à l'Écart (entrée « lumière »).") :
                 !m.linked("plante", "level", "ecart", "b") ? syn("Relie l'orientation de la Plante à l'Écart.") :
                 !m.linked("ecart", "d", "croissance", "x") ? syn("Relie l'Écart à la Croissance.") :
                 !m.linked("croissance", "flow", "plante", "in") ? syn("Relie la rotation de la Croissance à la Plante.") :
                 !app.panel.has("orientation") ? pan("Ajoute la boussole de la plante dans le Panneau.") : null; },
        check: (app, mem) => {
          const lamp = app.model.first("lampe"), ok = Math.abs(orient(app) - lamp.p.angle) < 5;
          mem.n = ok ? (mem.n || 0) + 1 : 0;
          return { p: mem.n / 12, done: mem.n >= 12, status: ok ? `Face à la lampe… ${app.fmtSteps(mem.n)} / 1 h 00` : "La plante se tourne…" };
        },
        takeaway: "La plante se tourne vers la lampe, vite d'abord, puis de plus en plus doucement, et s'arrête face à elle. C'est la même boucle que le thermostat, mais sans tout-ou-rien : plus l'écart est grand, plus elle tourne vite.",
        hood: "Plante = <b>Storage</b> (son orientation s'accumule). Écart = <b>Gradient</b>. Croissance = <b>Transducer</b>, comme le haut-parleur de Larsen. Lampe = <b>Clock</b> immobile." },

      { id: "sun", title: "Dehors, le soleil",
        unlock: { pieces: ["soleil"], instruments: ["jour"] },
        predict: { q: "Avant de lancer : la nuit, quand le soleil a disparu, où regardera la plante ?",
                   choices: ["Vers l'est, prête pour le lever", "Vers l'ouest, là où le soleil s'est couché", "N'importe où"] },
        goal: "Retire la Lampe (sélectionne-la, touche Suppr) et pose un <b>Soleil</b> à sa place, relié à l'Écart. Ajoute le <b>témoin jour / nuit</b>. Laisse passer un jour et demi.",
        hint: "Le bouton ×1 en haut accélère le temps.",
        need: app => { const m = app.model;
          return m.first("lampe") ? syn("Retire la Lampe : sélectionne-la dans le Synoptique, puis touche Suppr.") :
                 !m.first("soleil") ? syn("Pose un Soleil.") :
                 !m.linked("soleil", "out", "ecart", "a") ? syn("Relie la lumière du Soleil à l'Écart.") :
                 !coreWired(m) ? syn("Garde la boucle Écart → Croissance → Plante → Écart.") :
                 !app.panel.has("jour") ? pan("Ajoute le témoin jour / nuit dans le Panneau.") : null; },
        check: K.elapse(36 * 12),
        takeaway: "Le jour, la plante suit le soleil, toujours avec un peu de retard. Mais la nuit, elle n'a plus rien à viser : elle reste tournée vers l'ouest, et elle rate le lever du soleil.",
        hood: "Soleil = <b>Clock</b> : un rythme imposé du dehors. Sans lumière, l'Écart n'a plus de cible et la boucle s'arrête." },

      { id: "clock", title: "Une horloge intérieure",
        unlock: { pieces: ["horloge"] },
        goal: "Pose une <b>Horloge</b> et relie-la, elle aussi, à l'entrée <i>lumière</i> de l'Écart. Attends le prochain lever du soleil.",
        hint: "L'Horloge se réveille en fin de nuit, et ne compte que quand le soleil se tait.",
        need: app => { const m = app.model;
          return !m.first("horloge") ? syn("Pose une Horloge.") :
                 !m.linked("horloge", "out", "ecart", "a") ? syn("Relie l'Horloge à l'entrée « lumière » de l'Écart.") :
                 !m.linked("soleil", "out", "ecart", "a") ? syn("Garde aussi le Soleil relié à l'Écart.") :
                 !coreWired(m) ? syn("Garde la boucle Écart → Croissance → Plante → Écart.") : null; },
        check: (app, mem) => {
          const night = app.model.env.night;
          if (mem.prev === true && !night) mem.mornings = (mem.mornings || []).concat([orient(app)]);
          mem.prev = night;
          const good = (mem.mornings || []).some(v => v < -55);
          return { p: good ? 1 : night ? 0.5 : 0.2, done: good,
            status: night ? "Nuit… regarde où se tourne la plante." : (mem.mornings || []).length ? "Ce matin-là, elle n'était pas prête : attends le suivant." : "Attends la nuit, puis le lever du soleil." };
        },
        takeaway: "En fin de nuit, la plante se retourne vers l'est, avant même que le soleil revienne : elle anticipe. Le jeune tournesol fait réellement cela, grâce à une horloge interne.",
        hood: "Horloge = <b>Clock</b> intérieure, branchée en secours : elle ne compte que quand la lumière se tait. Une boucle, plus la mémoire d'un rythme." },

      { id: "irregular", title: "Des jours irréguliers",
        unlock: { instruments: ["irregularite", "bruit"] },
        predict: { q: "Si les jours deviennent irréguliers, tantôt courts, tantôt longs, la plante suivra-t-elle encore le soleil ?",
                   choices: ["Oui, toujours aussi bien", "Le jour oui, mais certains matins elle sera mal préparée", "Non, elle se perd complètement"] },
        goal: "Ajoute le curseur d'<b>irrégularité des jours</b> au Panneau et pousse-le au-delà de la moitié. Laisse passer trois jours en regardant la Maquette et les courbes.",
        hint: "Tu peux aussi ajouter le curseur de bruit, et chercher à partir d'où la plante erre.",
        need: app => { const m = app.model, s = m.first("soleil");
          return !s || !m.linked("soleil", "out", "ecart", "a") || !coreWired(m) ? syn("Garde le Soleil et la boucle reliés.") :
                 !app.panel.has("irregularite") ? pan("Ajoute le curseur d'irrégularité des jours dans le Panneau.") :
                 s.p.irr < 0.6 ? pan("Pousse l'irrégularité au-delà de la moitié.") : null; },
        check: K.elapse(72 * 12),
        takeaway: "Le jour, la boucle corrige quoi que fasse le soleil : la plante suit encore. Mais l'horloge, réglée sur un rythme fixe, se trompe d'heure certains matins. Ce qui marche bien dans un monde régulier peut échouer quand le rythme se dérègle.",
        hood: "Chaque mécanisme a son domaine de validité : la boucle tolère les irrégularités, l'horloge les suppose absentes." }
    ],

    final: {
      title: "La plante qui suit le soleil",
      text: "Réguler vers une consigne fixe (le thermostat) et poursuivre une cible qui bouge (le tournesol), c'est la même boucle négative. Elle sert aussi à l'œil qui suit une balle, au pilote automatique qui garde un cap, à l'antenne qui suit un satellite. Et quand la cible est prévisible, une horloge permet d'anticiper.",
      questions: [],
      hood: "Pièces génériques utilisées : Storage, Gradient, Transducer, Clock. Transducer était déjà dans Larsen."
    },

    free: {
      text: "Toutes les pièces et tous les curseurs sont débloqués. Essaie : une plante très réactive suit-elle mieux, ou se met-elle à trembler avec du bruit ? Remets la Lampe à côté du Soleil : qui l'emporte ? Jusqu'où peut aller le bruit avant que la plante erre au hasard ?",
      hood: "Le même assemblage, avec d'autres noms : une antenne de poursuite, un œil, un missile, un régulateur de vitesse."
    },

    // ---------------------------------------------------------------- Maquette
    view: function (host, model, api) {
      host.innerHTML = `
<svg viewBox="0 0 440 300" role="img" aria-label="Maquette : une plante en pot, le ciel et la lumière" preserveAspectRatio="xMidYMid meet">
  <defs><clipPath id="tsClip"><rect x="0" y="0" width="440" height="300" rx="12"/></clipPath></defs>
  <g clip-path="url(#tsClip)">
    <rect id="tsSky" x="0" y="0" width="440" height="300"/>
    <g id="tsStars" fill="#ffffff">${Array.from({ length: 30 }, (_, i) => `<circle cx="${(i * 71) % 430 + 5}" cy="${(i * 43) % 170 + 6}" r="${1 + (i % 3) * .4}"/>`).join("")}</g>
    <path d="M40 240 A 180 165 0 0 1 400 240" fill="none" stroke="#ffffff" stroke-opacity=".25" stroke-dasharray="3 6"/>
    <g id="tsSun"><circle r="16" fill="#ffd34d"/><circle r="24" fill="#ffd34d" opacity=".25"/></g>
    <g id="tsLamp">
      <line x1="0" y1="0" x2="0" y2="-60" stroke="#6e6a60" stroke-width="3" transform="translate(0 70)"/>
      <path d="M-18 -6 L18 -6 L10 10 L-10 10 Z" fill="#c9a24a" stroke="#6e6a60"/>
      <circle cx="0" cy="12" r="7" fill="#fff2a8"/>
    </g>
    <rect id="tsGround" x="0" y="246" width="440" height="54"/>
    <text class="mq-note" x="24" y="290" style="fill:#2f2d27">Est</text>
    <text class="mq-note" x="416" y="290" text-anchor="end" style="fill:#2f2d27">Ouest</text>
    <g id="tsPlant">
      <path id="tsStem" fill="none" stroke="#3f7d3a" stroke-width="5" stroke-linecap="round"/>
      <path id="tsLeaf1" fill="#4f9a47"/><path id="tsLeaf2" fill="#4f9a47"/>
      <g id="tsHead"><ellipse id="tsPetals" fill="#f2c230"/><ellipse id="tsDisc" fill="#6b4423"/></g>
      <path d="M196 246 L244 246 L238 282 L202 282 Z" fill="#b5653b" stroke="#7e4428"/>
    </g>
    <text id="tsEmpty" class="mq-note" x="220" y="150" text-anchor="middle" style="fill:#2f2d27">Pose une Plante dans le Synoptique.</text>
  </g>
</svg>`;
      const $ = id => host.querySelector("#" + id);
      const mix = (a, b, t) => `rgb(${a.map((v, i) => Math.round(v + (b[i] - v) * t)).join(",")})`;
      let head = 0;
      const sunPos = az => { const f = (az + 90) / 180; return { x: 40 + 360 * f, y: 240 - 165 * Math.sin(Math.PI * f) }; };

      return {
        update() {
          const plant = model.first("plante"), sun = model.first("soleil"), lamp = model.first("lampe");
          const outdoor = !!sun, night = model.env.night;
          let daylight = 1;
          if (outdoor && sun.s.v !== null) daylight = Math.min(1, Math.sin(Math.PI * (sun.s.v + 90) / 180) * 2 + 0.2);
          if (outdoor && sun.s.v === null) daylight = 0;
          $("tsSky").setAttribute("fill", outdoor ? mix([22, 28, 54], [150, 196, 235], daylight) : "#e9e3d6");
          $("tsStars").style.display = outdoor && night ? "" : "none";
          $("tsGround").setAttribute("fill", outdoor ? mix([38, 52, 34], [122, 160, 92], daylight) : "#b9ad98");
          $("tsSun").style.display = outdoor && sun.s.v !== null ? "" : "none";
          if (outdoor && sun.s.v !== null) { const p = sunPos(sun.s.v); $("tsSun").setAttribute("transform", `translate(${p.x.toFixed(1)} ${p.y.toFixed(1)})`); }
          $("tsLamp").style.display = lamp ? "" : "none";
          if (lamp) { const p = sunPos(lamp.p.angle); $("tsLamp").setAttribute("transform", `translate(${p.x.toFixed(1)} ${(p.y + 30).toFixed(1)})`); }
          $("tsEmpty").style.display = plant ? "none" : "";
          $("tsPlant").style.display = plant ? "" : "none";
          if (!plant) return;
          head += (plant.s.x - head) * 0.25;
          const a = Math.max(-100, Math.min(100, head)) / 90;          // −1 east … +1 west
          const hx = 220 + 58 * a, hy = 112 + 18 * Math.abs(a);
          $("tsStem").setAttribute("d", `M220 246 C220 200 ${220 + 20 * a} ${170} ${hx.toFixed(1)} ${hy.toFixed(1)}`);
          $("tsLeaf1").setAttribute("d", `M220 214 q-26 -10 -34 4 q14 10 34 -4 z`);
          $("tsLeaf2").setAttribute("d", `M220 196 q26 -12 34 2 q-14 10 -34 -2 z`);
          const rx = 30 - 14 * Math.min(1, Math.abs(a));              // the face turns away from us
          $("tsHead").setAttribute("transform", `translate(${hx.toFixed(1)} ${hy.toFixed(1)}) rotate(${(a * 18).toFixed(1)})`);
          $("tsPetals").setAttribute("rx", (rx + 9).toFixed(1)); $("tsPetals").setAttribute("ry", "38");
          $("tsDisc").setAttribute("rx", rx.toFixed(1)); $("tsDisc").setAttribute("ry", "26");
          $("tsDisc").setAttribute("cx", (6 * a).toFixed(1));
        }
      };
    }
  };

  (K.workshops = K.workshops || {}).tournesol = W;
})(window.TSCGKit = window.TSCGKit || {});
