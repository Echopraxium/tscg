/* TSCG Kit — Thermostat workshop definition
 * Pieces (skins over generic kinds), panel instruments, tutorial steps and the
 * 2D scale model. The scale model shows no number at all: numbers live on the Panel.
 * The definition is a factory: L(english, french) picks every text.
 * Author: Echopraxium with the collaboration of Claude AI
 */
(function (K) {
  "use strict";
  const inBand = app => { const r = app.model.first("room"); return !!r && r.s.x >= 19 && r.s.x <= 21; };
  const syn = msg => ({ msg, tab: "synoptic" });
  const pan = msg => ({ msg, tab: "panel" });

  const factory = L => {
    const OUT_OF_BAND = L("Outside the 19–21 °C zone: the counter restarts from zero.", "Hors de la zone 19–21 °C : le compteur repart de zéro.");
    return {
    id: "thermostat",
    title: L("TSCG Workshop — Thermostat", "Atelier TSCG — Thermostat"),
    pageTitle: L("TSCG Workshop — Thermostat", "TSCG Atelier — Thermostat"),
    fluxLabel: L("flux (heat)", "flux (chaleur)"),
    chart: {
      range: [0, 32], tickY: 10, span: 8, tick: 2, label: t => t + " h",
      band: [19, 21], showBand: app => app.S.free || app.S.pieces.has("heater"),
      strips: [
        { label: L("heater on", "chauffage en marche"), color: "--flux", on: (p, m) => { const h = m.first("heater"); return !!(h && p.u[h.id]); } },
        { label: L("window open", "fenêtre ouverte"), color: "--info", on: p => p.open }
      ]
    },
    order: ["room", "wall", "heater", "bimetal", "radiator"],
    // where each piece lands: heat flows left to right, control sits below
    home: { heater: { x: 16, y: 20 }, radiator: { x: 16, y: 220 }, room: { x: 206, y: 20 }, wall: { x: 396, y: 20 }, bimetal: { x: 206, y: 180 } },

    skins: {
      room: { kind: "storage", name: L("Room", "Pièce"), blurb: L("stores heat", "accumule la chaleur"), unit: "°C", color: "#d9822b",
        ports: { in: L("heat in", "chaleur reçue"), out: L("losses", "pertes"), level: L("temperature", "température") },
        params: { C: { label: L("Capacity (kWh/°C)", "Capacité (kWh/°C)"), v: 0.5, step: 0.1, min: 0.05, max: 5 },
                  k: { label: L("Leak (kW/°C)", "Fuite (kW/°C)"), v: 0.1, step: 0.05, min: 0, max: 2 },
                  x0: { label: L("Start temp. (°C)", "Temp. initiale (°C)"), v: 20, step: 1, min: -10, max: 40 } } },
      wall: { kind: "sink", name: L("Wall", "Mur"), blurb: L("lets heat escape outside", "laisse filer la chaleur dehors"), unit: "°C", levelText: L("outside", "dehors"),
        ports: { in: L("losses", "pertes") },
        params: { level: { label: L("Outside temp. (°C)", "Temp. extérieure (°C)"), v: 5, step: 1, min: -20, max: 30 },
                  kOpen: { label: L("Open-window leak (kW/°C)", "Fuite fenêtre ouverte (kW/°C)"), v: 0.6, step: 0.1, min: 0, max: 5 } } },
      heater: { kind: "source", name: L("Heater", "Chauffage"), blurb: L("produces heat", "produit de la chaleur"), onText: L("heating", "chauffe"), offText: L("off", "à l'arrêt"),
        ports: { cmd: L("command", "commande"), flow: L("heat", "chaleur") },
        params: { P: { label: L("Power (kW)", "Puissance (kW)"), v: 2.5, step: 0.5, min: 0, max: 10 } } },
      bimetal: { kind: "threshold", name: L("Bimetal", "Bilame"), blurb: L("bends with heat", "se courbe avec la chaleur"), onText: L("contact closed", "contact fermé"), offText: L("contact open", "contact ouvert"),
        ports: { x: L("temperature", "température"), u: L("command", "commande") },
        params: { set: { label: L("Set point (°C)", "Consigne (°C)"), v: 20, step: 0.5, min: 5, max: 30 },
                  h: { label: L("Hysteresis (°C)", "Hystérésis (°C)"), v: 1, step: 0.25, min: 0, max: 5 } } },
      radiator: { kind: "storage", name: L("Radiator", "Radiateur"), blurb: L("a mass that stores heat, then gives it back", "masse qui stocke puis rend la chaleur"), unit: "°C", color: "#c0392b",
        ports: { in: L("heat in", "chaleur reçue"), out: L("gives", "rendue"), level: L("temperature", "température") },
        params: { C: { label: L("Mass (kWh/°C)", "Masse (kWh/°C)"), v: 0.3, step: 0.1, min: 0.05, max: 5 },
                  k: { label: L("Exchange (kW/°C)", "Échange (kW/°C)"), v: 0.5, step: 0.05, min: 0, max: 3 },
                  x0: { label: L("Start temp. (°C)", "Temp. initiale (°C)"), v: 20, step: 1, min: -10, max: 80 } } }
    },

    instruments: {
      roomTemp:     { type: "gauge",  label: L("Room thermometer", "Thermomètre de la pièce"), short: L("Room", "Pièce"), bind: { piece: "room", get: "level" }, range: [0, 30], step: 0.1, unit: "°C", zone: [19, 21] },
      heaterSwitch: { type: "toggle", label: L("Heater switch", "Interrupteur du chauffage"), short: L("Heater", "Chauffage"), bind: { piece: "heater", set: "manual" } },
      bimetalLamp:  { type: "lamp",   label: L("Bimetal light (contact closed)", "Témoin du bilame (contact fermé)"), short: L("Contact", "Contact"), bind: { piece: "bimetal", get: "u" } },
      setpoint:     { type: "slider", label: L("Bimetal set point", "Consigne du bilame"), short: L("Set point", "Consigne"), bind: { piece: "bimetal", param: "set" }, range: [10, 28], step: 0.5, unit: "°C" },
      radiatorTemp: { type: "gauge",  label: L("Radiator thermometer", "Thermomètre du radiateur"), short: L("Radiator", "Radiateur"), bind: { piece: "radiator", get: "level" }, range: [0, 60], step: 0.1, unit: "°C" },
      outsideTemp:  { type: "slider", label: L("Outside temperature", "Température extérieure"), short: L("Outside", "Dehors"), bind: { piece: "wall", param: "level" }, range: [-15, 25], step: 1, unit: "°C" }
    },

    steps: [
      { id: "room", title: L("A room", "Une pièce"),
        unlock: { pieces: ["room"], instruments: ["roomTemp"] },
        goal: L("In the <b>Synoptic</b>, place a <b>Room</b>. Then, in the <b>Panel</b>, add its thermometer. Finally, start the time with ▶ and watch for an hour.",
                "Dans le <b>Synoptique</b>, pose une <b>Pièce</b>. Puis, dans le <b>Panneau</b>, ajoute son thermomètre. Enfin, lance le temps avec ▶ et observe pendant une heure."),
        need: app => !app.model.first("room") ? syn(L("Place a Room in the Synoptic.", "Pose une Pièce dans le Synoptique.")) :
                     !app.panel.has("roomTemp") ? pan(L("Add the room thermometer in the Panel.", "Ajoute le thermomètre de la pièce dans le Panneau.")) : null,
        check: K.elapse(60),
        takeaway: L("The temperature does not move. A store of heat only changes when something flows in or out.",
                    "La température ne bouge pas. Une réserve de chaleur ne change que si quelque chose y entre ou en sort."),
        hood: L("Room = <b>Storage</b>: it accumulates a quantity (here, heat).", "Pièce = <b>Storage</b> : elle accumule une quantité (ici, de la chaleur).") },

      { id: "wall", title: L("The wall and winter", "Le mur et l'hiver"),
        unlock: { pieces: ["wall"] },
        goal: L("Outside, it is cold. Place a <b>Wall</b> and wire the Room's <i>losses</i> output to the Wall's input. Then let 6 hours go by.",
                "Dehors, il fait froid. Pose un <b>Mur</b> et relie la sortie <i>pertes</i> de la Pièce à l'entrée du Mur. Puis laisse passer 6 heures."),
        predict: { q: L("Before you start: where do you think the temperature will be in 6 hours?", "Avant de lancer : à ton avis, où sera la température dans 6 heures ?"),
                   choices: [L("Still around 20 °C", "Toujours vers 20 °C"), L("Lower, but still above 5 °C", "Elle descend, mais reste au-dessus de 5 °C"), L("Down to 5 °C or less", "Elle tombe à 5 °C ou moins")] },
        hint: L("Tip: the ×1 button at the top speeds up time.", "Astuce : le bouton ×1 en haut accélère le temps."),
        need: app => !app.model.first("room") ? syn(L("The Room is missing.", "Il manque la Pièce.")) :
                     !app.model.linked("room", "out", "wall", "in") ? syn(L("Wire the Room to the Wall in the Synoptic.", "Relie la Pièce au Mur dans le Synoptique.")) : null,
        check: K.elapse(360),
        takeaway: L("The temperature falls towards the outside one, more and more slowly. Without heating, that is where the room always ends up.",
                    "La température descend vers celle du dehors, de plus en plus lentement. Sans chauffage, c'est là que la pièce finit toujours."),
        hood: L("Wall = <b>Sink</b>: the exit of the system. The state everything tends to is called an <b>attractor</b>.",
                "Mur = <b>Sink</b> : la sortie du système. L'état vers lequel tout tend s'appelle un <b>attracteur</b>.") },

      { id: "manual", title: L("Heating by hand", "Chauffer à la main"),
        unlock: { pieces: ["heater"], instruments: ["heaterSwitch"] },
        enter: app => { const r = app.model.first("room"); if (r) r.s.x = 17; },
        goal: L("The room has dropped to 17 °C. Place a <b>Heater</b>, wire its <i>heat</i> to the Room, add its <b>switch</b> to the Panel, and keep the room <b>between 19 and 21 °C for 2 hours</b>.",
                "La pièce est retombée à 17 °C. Pose un <b>Chauffage</b>, relie sa <i>chaleur</i> à la Pièce, ajoute son <b>interrupteur</b> au Panneau, et garde la pièce <b>entre 19 et 21 °C pendant 2 heures</b>."),
        hint: L("The green zone of the thermometer shows where to stay.", "La zone verte du thermomètre montre où tenir."),
        need: app => !app.model.first("room") ? syn(L("The Room is missing.", "Il manque la Pièce.")) :
                     !app.model.linked("room", "out", "wall", "in") ? syn(L("Keep the Room wired to the Wall.", "Garde la Pièce reliée au Mur.")) :
                     !app.model.linked("heater", "flow", "room", "in") ? syn(L("Wire the Heater to the Room in the Synoptic.", "Relie le Chauffage à la Pièce dans le Synoptique.")) :
                     app.model.wiresTo(app.model.first("heater").id, "cmd").length ? syn(L("In this step you are in command: remove the wire plugged into the command.", "Pour cette étape, c'est toi qui commandes : retire le fil branché sur la commande.")) :
                     !app.panel.has("heaterSwitch") ? pan(L("Add the heater switch in the Panel.", "Ajoute l'interrupteur du chauffage dans le Panneau.")) : null,
        check: K.hold(120, inBand, OUT_OF_BAND),
        takeaway: L("Regulating by hand is exhausting: you have to watch all the time. If only an object could do it for us…",
                    "Réguler à la main, c'est épuisant : il faut surveiller sans arrêt. On rêverait d'un objet qui le ferait à notre place…"),
        hood: L("Heater = <b>Source</b>: the energy input of the system.", "Chauffage = <b>Source</b> : l'entrée d'énergie du système.") },

      { id: "loop", title: L("Closing the loop", "Fermer la boucle"),
        unlock: { pieces: ["bimetal"], instruments: ["bimetalLamp", "setpoint"] },
        goal: L("Place a <b>Bimetal</b>. Wire the Room's <i>temperature</i> to the Bimetal, then the Bimetal's <i>command</i> to the Heater. Add the bimetal <b>light</b> to the Panel. Then hands off: <b>2 hours between 19 and 21 °C</b>.",
                "Pose un <b>Bilame</b>. Relie la <i>température</i> de la Pièce au Bilame, puis la <i>commande</i> du Bilame au Chauffage. Ajoute le <b>témoin</b> du bilame au Panneau. Ensuite, ne touche plus à rien : <b>2 heures entre 19 et 21 °C</b>."),
        hint: L("Watch the bimetal in the scale model while time goes by.", "Regarde le bilame dans la Maquette pendant que le temps passe."),
        need: app => !app.model.first("room") ? syn(L("The Room is missing.", "Il manque la Pièce.")) :
                     !app.model.linked("heater", "flow", "room", "in") ? syn(L("Wire the Heater to the Room.", "Relie le Chauffage à la Pièce.")) :
                     !app.model.linked("room", "level", "bimetal", "x") ? syn(L("Wire the Room's temperature to the Bimetal.", "Relie la température de la Pièce au Bilame.")) :
                     !app.model.linked("bimetal", "u", "heater", "cmd") ? syn(L("Wire the Bimetal's command to the Heater.", "Relie la commande du Bilame au Chauffage.")) :
                     !app.panel.has("bimetalLamp") ? pan(L("Add the bimetal light in the Panel.", "Ajoute le témoin du bilame dans le Panneau.")) : null,
        check: K.hold(120, inBand, OUT_OF_BAND),
        takeaway: L("The room regulates itself. But look: the temperature is never exactly 20 °C, it keeps going up and down around it.",
                    "La pièce se règle toute seule. Mais regarde : la température n'est jamais exactement à 20 °C, elle monte et descend sans cesse autour."),
        hood: L("Bimetal = <b>Threshold</b> with hysteresis. The wire coming back from the Room to the Heater forms a negative <b>Feedback Loop</b>: it is not a piece, it is a wiring.",
                "Bilame = <b>Threshold</b> avec hystérésis. Le fil qui revient de la Pièce vers le Chauffage forme une <b>Feedback Loop</b> négative : ce n'est pas une pièce, c'est un câblage.") },

      { id: "window", title: L("A cold snap", "Un coup de froid"),
        goal: L("In the <b>scale model</b>, click the window to open it. Leave it open for at least 10 minutes, then close it.",
                "Dans la <b>Maquette</b>, clique sur la fenêtre pour l'ouvrir. Laisse-la ouverte au moins 10 minutes, puis referme-la."),
        hint: L("Meanwhile, watch the scale model as well as the Panel.", "Pendant ce temps, regarde aussi bien la Maquette que le Panneau."),
        need: app => !app.model.linked("bimetal", "u", "heater", "cmd") ? syn(L("Keep the loop closed (Bimetal → Heater).", "Garde la boucle fermée (Bilame → Chauffage).")) : null,
        check: (app, mem) => {
          const wall = app.model.first("wall"), open = !!(wall && wall.s.open);
          mem.open = (mem.open || 0) + (open ? 1 : 0);
          if (open) { mem.n = 0; return { p: 0.4 * Math.min(1, mem.open / 10), done: false, status: mem.open < 10 ? L("Window open…", "Fenêtre ouverte…") : L("You can close the window (click in the scale model).", "Tu peux refermer la fenêtre (clic dans la Maquette).") }; }
          if (mem.open < 10) return { p: 0.4 * mem.open / 10, done: false, status: mem.open ? L("Open it a little longer: at least 10 minutes in all.", "Rouvre-la encore un peu : au moins 10 minutes en tout.") : L("Click the window, in the scale model on the right.", "Clique sur la fenêtre, dans la Maquette à droite.") };
          const ok = inBand(app); mem.n = ok ? (mem.n || 0) + 1 : 0;
          return { p: 0.4 + 0.6 * Math.min(1, mem.n / 60), done: mem.n >= 60, status: ok ? L("Back to calm… ", "Retour au calme… ") + `${app.fmtSteps(mem.n)} / 1 h 00` : L("The heater brings the room back up…", "Le chauffage remonte la pièce…") };
        },
        takeaway: L("The shock is absorbed: with nobody around, the room comes back by itself between 19 and 21 °C.",
                    "Le choc est encaissé : sans personne, la pièce revient d'elle-même entre 19 et 21 °C."),
        hood: L("This is <b>homeostasis</b>: a system that returns to its set point after a disturbance.",
                "C'est l'<b>homéostasie</b> : un système qui revient vers son état de consigne après une perturbation.") }
    ],

    final: {
      title: L("The loop runs by itself", "La boucle tourne seule"),
      unlock: { pieces: ["radiator"], instruments: ["radiatorTemp", "outsideTemp"] },
      text: L("It was not really about a radiator: it was a <b>feedback loop</b>. With other names, the same pieces describe blood sugar (sugar is the store, insulin the command), a fridge, a float-valve toilet cistern, or the reorder point of a stock.",
              "Ce n'était pas vraiment un radiateur : c'était une <b>boucle de rétroaction</b>. Avec d'autres noms, les mêmes pièces décrivent la glycémie (le sucre est la réserve, l'insuline la commande), un réfrigérateur, la chasse d'eau à flotteur, ou le seuil de réapprovisionnement d'un stock."),
      questions: [],
      hood: L("The Panel is a <b>Map</b>: it only shows what its instruments measure. The scale model plays the part of the <b>Territory</b>. The gap between the two is what a model does not see.",
              "Le Panneau est une <b>Carte</b> : il ne montre que ce que ses instruments mesurent. La Maquette joue le rôle du <b>Territoire</b>. L'écart entre les deux, c'est ce qu'un modèle ne voit pas.")
    },

    free: {
      text: L("Every piece and instrument is unlocked. Try putting a <b>Radiator</b> between the Heater and the Room, and put its thermometer on the Panel: which one reacts first when the contact opens? You can also make winter harsher, widen the bimetal's hysteresis, or stretch and rotate the instruments.",
              "Toutes les pièces et tous les instruments sont débloqués. Essaie d'intercaler un <b>Radiateur</b> entre le Chauffage et la Pièce, et mets son thermomètre sur le Panneau : lequel réagit en premier quand le contact s'ouvre ? Tu peux aussi rendre l'hiver plus rude, élargir l'hystérésis du bilame, ou étirer et pivoter les instruments."),
      hood: L("Generic pieces used: Storage, Sink, Source, Threshold. The same ones serve in the other workshops.",
              "Pièces génériques utilisées : Storage, Sink, Source, Threshold. Les mêmes servent dans les autres ateliers.")
    },

    // ---------------------------------------------------------------- scale model
    view: function (host, model, api) {
      host.innerHTML = `
<svg viewBox="0 0 440 300" role="img" preserveAspectRatio="xMidYMid meet">
  <rect id="mqSky" x="0" y="0" width="440" height="300" rx="12"/>
  <g id="mqSnow" fill="#ffffff" opacity=".9">${Array.from({ length: 26 }, (_, i) => `<circle cx="${(i * 67) % 430 + 6}" cy="${(i * 37) % 250 + 6}" r="${1.4 + (i % 3) * .5}"/>`).join("")}</g>
  <rect id="mqGround" x="0" y="262" width="440" height="38" rx="0"/>
  <g id="mqHouse">
    <path d="M40 76 L220 18 L400 76 Z" fill="#9b6b4f"/>
    <rect id="mqAir" x="60" y="76" width="320" height="186"/>
    <rect id="mqWalls" x="55" y="76" width="330" height="186" fill="none" stroke-width="10"/>
    <line x1="50" y1="262" x2="390" y2="262" stroke="#6e6a60" stroke-width="3"/>
    <g id="mqWindow" class="mq-click">
      <rect x="368" y="118" width="34" height="84" fill="transparent"/>
      <rect id="mqWinHole" x="380" y="124" width="10" height="72"/>
      <rect id="mqWinGlass" x="380" y="124" width="10" height="72" fill="#cfe7f7" stroke="#7d8a94" stroke-width="1.5"/>
      <rect id="mqWinLeaf" x="390" y="124" width="22" height="6" fill="#cfe7f7" stroke="#7d8a94" stroke-width="1.5"/>
      <g id="mqDraft" stroke="#3f7fd6" stroke-width="2" fill="none" stroke-linecap="round">
        <path d="M402 140 q-10 4 -22 0 t-24 0"/><path d="M402 160 q-10 4 -22 0 t-30 0"/><path d="M402 180 q-10 4 -22 0 t-24 0"/>
      </g>
    </g>
    <g id="mqHeat">
      <rect id="mqRadBody" x="74" y="180" width="54" height="66" rx="5" stroke="#6e6a60" stroke-width="1.5"/>
      ${[0, 1, 2, 3, 4].map(i => `<line x1="${84 + i * 9}" y1="186" x2="${84 + i * 9}" y2="240" stroke="#6e6a60" stroke-width="1" opacity=".5"/>`).join("")}
      <g id="mqWaves" stroke="#e07b39" stroke-width="2" fill="none" stroke-linecap="round">
        <path d="M86 172 q4 -8 0 -16 t0 -16"/><path d="M101 172 q4 -8 0 -16 t0 -16"/><path d="M116 172 q4 -8 0 -16 t0 -16"/>
      </g>
    </g>
    <path id="mqCable" d="M208 136 V150 H140 V200 H128" fill="none" stroke="#6e6a60" stroke-width="1.5" stroke-dasharray="3 3"/>
    <g id="mqBim">
      <rect x="186" y="96" width="56" height="40" rx="5" fill="#f4f2ec" stroke="#6e6a60" stroke-width="1.5"/>
      <circle cx="194" cy="126" r="3" fill="#6e6a60"/>
      <circle id="mqContact" cx="232" cy="110" r="3.5"/>
      <path id="mqStrip" fill="none" stroke-width="4" stroke-linecap="round"/>
      <path id="mqStrip2" fill="none" stroke-width="2" stroke-linecap="round"/>
    </g>
  </g>
  <text id="mqEmpty" class="mq-note" x="220" y="150" text-anchor="middle"></text>
</svg>`;
      const $ = id => host.querySelector("#" + id);
      const disp = { heat: 0, strip: 1, waves: 0 };
      const ease = (k, target, f = 0.12) => { disp[k] += (target - disp[k]) * f; return disp[k]; };
      const mix = (a, b, t) => a.map((v, i) => Math.round(v + (b[i] - v) * t));
      const hex = c => `rgb(${c[0]},${c[1]},${c[2]})`;
      const ramp = (stops, v) => {
        if (v <= stops[0][0]) return hex(stops[0][1]);
        for (let i = 1; i < stops.length; i++) if (v <= stops[i][0]) {
          const [a, ca] = stops[i - 1], [b, cb] = stops[i]; return hex(mix(ca, cb, (v - a) / (b - a)));
        }
        return hex(stops[stops.length - 1][1]);
      };
      const AIR = [[0, [120, 160, 214]], [12, [178, 205, 232]], [19, [241, 234, 215]], [23, [246, 214, 168]], [30, [238, 150, 90]]];
      const METAL = [[0, [200, 205, 210]], [25, [214, 208, 198]], [40, [240, 160, 110]], [60, [220, 70, 40]]];
      const SKY_COLD = [[-15, [150, 170, 196]], [5, [184, 204, 226]], [25, [196, 226, 245]]];

      $("mqWindow").addEventListener("click", () => {
        const wall = model.first("wall");
        if (!wall) { api.toast(K.L("There is no outside yet: place a Wall in the Synoptic.", "Il n'y a pas encore de dehors : pose un Mur dans le Synoptique.")); return; }
        wall.s.open = !wall.s.open;
        api.log("window", wall.s.open ? "open" : "closed");
      });

      return {
        update() {
          const room = model.first("room"), wall = model.first("wall"), heater = model.first("heater"),
                bim = model.first("bimetal"), rad = model.first("radiator");
          host.querySelector("svg").setAttribute("aria-label", K.L("Scale model: a heated room, in cross-section", "Maquette : une pièce chauffée vue en coupe"));
          $("mqEmpty").textContent = K.L("Empty scale model: place a Room in the Synoptic.", "Maquette vide : pose une Pièce dans le Synoptique.");
          $("mqEmpty").style.display = room ? "none" : "";
          $("mqHouse").style.display = room ? "" : "none";
          const outside = wall ? wall.p.level : 15;
          $("mqSky").setAttribute("fill", wall ? ramp(SKY_COLD, outside) : "#e7e5df");
          $("mqSnow").style.display = wall && outside <= 5 ? "" : "none";
          $("mqGround").setAttribute("fill", wall && outside <= 2 ? "#eef2f6" : "#b9c4a3");
          if (!room) return;
          $("mqAir").setAttribute("fill", ramp(AIR, room.s.x));
          $("mqWalls").setAttribute("stroke", wall ? "#8a857a" : "#b7b2a6");
          $("mqWalls").setAttribute("stroke-dasharray", wall ? "" : "6 5");
          // window: only meaningful once there is an outside
          const open = !!(wall && wall.s.open);
          $("mqWindow").style.display = wall ? "" : "none";
          $("mqWinHole").setAttribute("fill", ramp(SKY_COLD, outside));
          $("mqWinGlass").style.display = open ? "none" : "";
          $("mqWinLeaf").style.display = open ? "" : "none";
          $("mqDraft").style.display = open ? "" : "none";
          // heater / radiator: glows with its own temperature, or with the on/off state
          $("mqHeat").style.display = heater ? "" : "none";
          if (heater) {
            const hot = rad ? Math.max(0, Math.min(1, (rad.s.x - 20) / 12)) : ease("heat", heater.s.u, 0.08);
            $("mqRadBody").setAttribute("fill", ramp(METAL, 20 + hot * 40));
            const toRoom = rad ? Math.max(0, rad.p.k * (rad.s.x - room.s.x)) / Math.max(0.5, heater.p.P) : (model.linked("heater", "flow", "room", "in") ? disp.heat : 0);
            $("mqWaves").setAttribute("opacity", ease("waves", Math.min(1, toRoom), 0.1).toFixed(2));
          }
          // bimetal: the strip curls away from the contact when it gets warm
          $("mqBim").style.display = bim ? "" : "none";
          const looped = bim && heater && model.linked("bimetal", "u", "heater", "cmd");
          $("mqCable").style.display = looped ? "" : "none";
          if (bim) {
            const closed = bim.s.x === null ? 1 : bim.s.u;
            const s = ease("strip", closed, 0.1);
            const ex = 230 - 3 * (1 - s), ey = 112 - 14 * (1 - s), cy = 120 - 12 * (1 - s);
            const d = `M194 126 Q212 ${cy} ${ex} ${ey}`;
            $("mqStrip").setAttribute("d", d); $("mqStrip").setAttribute("stroke", "#b87333");
            $("mqStrip2").setAttribute("d", d); $("mqStrip2").setAttribute("stroke", "#c9ccd1");
            $("mqContact").setAttribute("fill", s > 0.9 && looped ? "#e07b39" : "#9a968c");
          }
        }
      };
    }
  };
  };

  (K.workshops = K.workshops || {}).thermostat = factory;
})(window.TSCGKit = window.TSCGKit || {});
