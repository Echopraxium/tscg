/* TSCG Kit — Larsen workshop definition
 * A room, a voice, an amplifier and a loudspeaker. Sound levels are an envelope
 * model (no waveform): the room absorbs, the loudspeaker re-injects what the
 * microphone picks up. Above a loop gain of 1 the loop feeds itself: Larsen.
 * Time unit: seconds, one step = 10 ms, shown in slow motion.
 * The definition is a factory: L(english, french) picks every text.
 * Author: Echopraxium with the collaboration of Claude AI
 */
(function (K) {
  "use strict";
  const syn = msg => ({ msg, tab: "synoptic" });
  const pan = msg => ({ msg, tab: "panel" });
  const lvl = app => { const r = app.model.first("salle"); return r ? r.s.x : 0; };
  const speaking = app => { const v = app.model.first("voix"); return !!(v && v.s.u); };
  const saturated = app => { const a = app.model.first("ampli"); return !!(a && a.s.sat); };
  const loopWired = m => m.linked("salle", "level", "ampli", "x") && m.linked("ampli", "y", "hp", "x") && m.linked("hp", "flow", "salle", "in");

  const factory = L => {
    const KEEP_LOOP = L("Keep the loop Room → Amp → Loudspeaker → Room.", "Garde la boucle Salle → Ampli → Haut-parleur → Salle.");
    return {
    id: "larsen",
    title: L("TSCG Workshop — Larsen", "Atelier TSCG — Larsen"),
    pageTitle: L("TSCG Workshop — Larsen", "TSCG Atelier — Larsen"),
    fluxLabel: L("flux (sound)", "flux (son)"),
    clock: { dt: 0.01, stepsPerSec: 25, fmt: t => t.toFixed(1) + " s", fmtSteps: n => (n * 0.01).toFixed(1) + " s" },
    order: ["salle", "voix", "ampli", "hp"],
    home: { voix: { x: 16, y: 20 }, salle: { x: 206, y: 20 }, ampli: { x: 396, y: 170 }, hp: { x: 16, y: 170 } },

    skins: {
      salle: { kind: "storage", name: L("Room", "Salle"), blurb: L("sound builds up, then dies out", "le son s'y accumule puis s'éteint"),
        ports: { in: L("sound in", "son reçu"), out: L("leak", "fuite"), level: L("picked up by the mic", "capté par le micro") },
        describe: n => K.L("level ", "niveau ") + n.s.x.toFixed(0),
        params: { decay: { label: L("Absorption (/s)", "Absorption (/s)"), v: 10, step: 1, min: 1, max: 40 },
                  C: { v: 1, hidden: true }, k: { v: 0, hidden: true }, x0: { v: 0, hidden: true },
                  base: { label: L("Ambient noise", "Bruit ambiant"), v: 0.5, step: 0.5, min: 0, max: 20 }, lo: { v: 0, hidden: true } } },
      voix: { kind: "source", name: L("Voice", "Voix"), blurb: L("someone speaks", "quelqu'un parle"), onText: L("speaking", "parle"), offText: L("silent", "se tait"),
        ports: { cmd: L("command", "commande"), flow: L("sound", "son") },
        params: { P: { label: L("Voice strength", "Force de la voix"), v: 100, step: 10, min: 0, max: 300 } } },
      ampli: { kind: "amplify", name: L("Amp", "Ampli"), blurb: L("multiplies the mic signal", "multiplie le signal du micro"),
        ports: { x: L("mic", "micro"), y: L("amplified", "amplifié") },
        describe: n => (n.s.sat ? K.L("saturated", "saturé") : "gain ×" + n.p.gain.toFixed(2)),
        params: { gain: { label: L("Volume (gain)", "Volume (gain)"), v: 0.3, step: 0.05, min: 0, max: 2.5 },
                  max: { label: L("Output ceiling", "Plafond de sortie"), v: 90, step: 5, min: 10, max: 200 } } },
      hp: { kind: "transducer", name: L("Loudspeaker", "Haut-parleur"), blurb: L("turns the signal into sound", "change le signal en son"),
        ports: { x: L("signal", "signal"), flow: L("sound", "son") },
        describe: n => (n.s.att < 1 ? K.L("mic far · ", "micro éloigné · ") : "") + K.L("sound ", "son ") + n.s.flow.toFixed(0),
        params: { k: { label: L("Efficiency", "Rendement"), v: 10, step: 1, min: 0, max: 30 }, max: { v: 5000, hidden: true }, noise: { v: 0, hidden: true } } }
    },

    instruments: {
      vumetre: { type: "gauge", label: L("Room level meter", "Vu-mètre de la salle"), short: L("Level", "Niveau"), bind: { piece: "salle", get: "level" }, range: [0, 100], decimals: 0, unit: "", zone: [18, 30] },
      parler:  { type: "toggle", label: L("Voice button", "Bouton de la voix"), short: L("Voice", "Voix"), bind: { piece: "voix", set: "manual" }, onText: L("speak", "parle"), offText: L("silence", "silence") },
      volume:  { type: "slider", label: L("Amp volume", "Volume de l'ampli"), short: "Volume", bind: { piece: "ampli", param: "gain" }, range: [0, 2.5], step: 0.05, decimals: 2, unit: "×" },
      sature:  { type: "lamp", label: L("Amp saturation light", "Témoin de saturation de l'ampli"), short: "Saturation", bind: { piece: "ampli", get: "sat" } }
    },

    chart: {
      range: [0, 100], tickY: 25, span: 4, tick: 1, label: t => t + " s",
      series: [{ piece: "salle", label: L("Level in the room", "Niveau dans la salle"), color: "--flux" }],
      strips: [
        { label: L("voice", "voix"), color: "--info", on: (p, m) => { const v = m.first("voix"); return !!(v && p.u[v.id]); } },
        { label: L("amp saturated", "ampli saturé"), color: "--bad", on: (p, m) => { const a = m.first("ampli"); return !!(a && p.u[a.id]); } }
      ]
    },

    steps: [
      { id: "talk", title: L("Speaking in the room", "Parler dans la salle"),
        unlock: { pieces: ["salle", "voix"], instruments: ["vumetre", "parler"] },
        goal: L("In the <b>Synoptic</b>, place a <b>Room</b> and a <b>Voice</b>, and wire the Voice's <i>sound</i> to the Room. In the <b>Panel</b>, add the <b>level meter</b> and the <b>voice button</b>. Start the time, speak for a moment, then fall silent.",
                "Dans le <b>Synoptique</b>, pose une <b>Salle</b> et une <b>Voix</b>, et relie le <i>son</i> de la Voix à la Salle. Dans le <b>Panneau</b>, ajoute le <b>vu-mètre</b> et le <b>bouton de la voix</b>. Lance le temps, parle un instant, puis tais-toi."),
        need: app => { const m = app.model;
          return !m.first("salle") || !m.first("voix") ? syn(L("Place a Room and a Voice in the Synoptic.", "Pose une Salle et une Voix dans le Synoptique.")) :
                 !m.linked("voix", "flow", "salle", "in") ? syn(L("Wire the Voice's sound to the Room.", "Relie le son de la Voix à la Salle.")) :
                 !app.panel.has("vumetre") ? pan(L("Add the level meter in the Panel.", "Ajoute le vu-mètre dans le Panneau.")) :
                 !app.panel.has("parler") ? pan(L("Add the voice button in the Panel.", "Ajoute le bouton de la voix dans le Panneau.")) : null; },
        check: (app, mem) => {
          if (speaking(app)) mem.spoke = (mem.spoke || 0) + 1;
          const s = mem.spoke || 0;
          if (s < 30) return { p: 0.5 * s / 30, done: false, status: s ? L("Keep speaking a moment…", "Continue de parler un instant…") : L("Click the voice button to speak.", "Clique sur le bouton de la voix pour parler.") };
          if (speaking(app)) return { p: 0.5, done: false, status: L("Now fall silent (click the button again).", "Maintenant, tais-toi (clique à nouveau sur le bouton).") };
          return { p: lvl(app) < 1 ? 1 : 0.75, done: lvl(app) < 1, status: L("Listen to the level dropping…", "Écoute le niveau retomber…") };
        },
        takeaway: L("When you speak, the level rises then settles. When you stop, it falls back by itself: the room absorbs sound. Silence is the state it always returns to.",
                    "Quand tu parles, le niveau monte puis se stabilise. Quand tu te tais, il retombe tout seul : la salle absorbe le son. Le silence est l'état vers lequel elle revient toujours."),
        hood: L("Room = <b>Storage</b> that empties itself (absorption). Voice = <b>Source</b>.", "Salle = <b>Storage</b> qui se vide d'elle-même (absorption). Voix = <b>Source</b>.") },

      { id: "amplify", title: L("Adding a PA", "Sonoriser"),
        unlock: { pieces: ["ampli", "hp"], instruments: ["volume"] },
        goal: L("Place an <b>Amp</b> and a <b>Loudspeaker</b>. Wire what the Room <i>picks up by the mic</i> to the Amp, the Amp to the Loudspeaker, and the Loudspeaker's <i>sound</i> to the Room. Add the <b>volume slider</b>. Then, while speaking, bring the level meter into the green zone and hold one second.",
                "Pose un <b>Ampli</b> et un <b>Haut-parleur</b>. Relie ce que la Salle <i>capte par le micro</i> à l'Ampli, l'Ampli au Haut-parleur, et le <i>son</i> du Haut-parleur à la Salle. Ajoute le <b>curseur de volume</b>. Puis, en parlant, amène le vu-mètre dans la zone verte et tiens une seconde."),
        hint: L("Turn the volume up gently.", "Monte le volume doucement."),
        need: app => { const m = app.model;
          return !m.first("ampli") || !m.first("hp") ? syn(L("Place an Amp and a Loudspeaker.", "Pose un Ampli et un Haut-parleur.")) :
                 !m.linked("salle", "level", "ampli", "x") ? syn(L("Wire what the mic picks up (Room) to the Amp.", "Relie ce que capte le micro (Salle) à l'Ampli.")) :
                 !m.linked("ampli", "y", "hp", "x") ? syn(L("Wire the Amp to the Loudspeaker.", "Relie l'Ampli au Haut-parleur.")) :
                 !m.linked("hp", "flow", "salle", "in") ? syn(L("Wire the Loudspeaker's sound to the Room.", "Relie le son du Haut-parleur à la Salle.")) :
                 !app.panel.has("volume") ? pan(L("Add the volume slider in the Panel.", "Ajoute le curseur de volume dans le Panneau.")) : null; },
        check: (app, mem) => {
          const ok = speaking(app) && lvl(app) >= 18 && lvl(app) <= 30 && !saturated(app);
          mem.n = ok ? (mem.n || 0) + 1 : 0;
          return { p: mem.n / 100, done: mem.n >= 100,
            status: !speaking(app) ? L("Speak (voice button) to fill the room.", "Parle (bouton de la voix) pour remplir la salle.") :
                    ok ? L("Hold on… ", "Tiens bon… ") + `${app.fmtSteps(mem.n)} / 1.0 s` :
                    lvl(app) < 18 ? L("Not loud enough: turn the volume up a little.", "Pas assez fort : monte un peu le volume.") : L("Too loud: turn the volume down a little.", "Trop fort : baisse un peu le volume.") };
        },
        takeaway: L("Your voice carries further: the loudspeaker sends back into the room what the mic picks up, which is picked up again, sent back… The output comes back to reinforce the input. For now, each round trip gives back less than it receives, and all stays calm.",
                    "Ta voix porte plus loin : le haut-parleur renvoie dans la salle ce que le micro capte, qui est capté à nouveau, renvoyé… La sortie revient renforcer l'entrée. Pour l'instant, chaque tour rend moins qu'il ne reçoit, et tout reste calme."),
        hood: L("Amp = <b>Amplification</b>. Loudspeaker = <b>Transducer</b> (signal → sound). The path Room → Amp → Loudspeaker → Room forms a positive <b>Feedback Loop</b>.",
                "Ampli = <b>Amplification</b>. Haut-parleur = <b>Transducer</b> (signal → son). Le chemin Salle → Ampli → Haut-parleur → Salle forme une <b>Feedback Loop</b> positive.") },

      { id: "whistle", title: L("The howl", "Le sifflement"),
        unlock: { instruments: ["sature"] },
        predict: { q: L("Before trying: if you turn the volume up further, then fall silent, what will happen?", "Avant d'essayer : si tu montes encore le volume, puis que tu te tais, que va-t-il se passer ?"),
                   choices: [L("The sound fades, as before", "Le son retombe, comme avant"), L("The sound stays a bit louder", "Le son reste un peu plus fort"), L("It howls, and it does not stop", "Ça siffle, et ça ne s'arrête plus")] },
        goal: L("Add the <b>saturation light</b>. Turn the volume up little by little, then fall silent. Watch the level meter, the scale model… and listen.",
                "Ajoute le <b>témoin de saturation</b>. Monte le volume petit à petit, puis tais-toi. Observe le vu-mètre, la Maquette… et écoute."),
        hint: L("The scale model's sound is muted with the small speaker icon at the top right.", "Le son de la Maquette se coupe avec le petit haut-parleur en haut à droite."),
        need: app => !loopWired(app.model) ? syn(KEEP_LOOP) :
                     !app.panel.has("sature") ? pan(L("Add the saturation light in the Panel.", "Ajoute le témoin de saturation dans le Panneau.")) : null,
        check: (app, mem) => {
          const ok = !speaking(app) && saturated(app);
          mem.n = ok ? (mem.n || 0) + 1 : 0;
          return { p: mem.n / 100, done: mem.n >= 100,
            status: speaking(app) ? L("Fall silent, to see what the loop does on its own.", "Tais-toi, pour voir ce que fait la boucle toute seule.") :
                    ok ? L("It holds on its own… ", "Ça tient tout seul… ") + `${app.fmtSteps(mem.n)} / 1.0 s` : L("Turn the volume up again, gently.", "Monte encore le volume, doucement.") };
        },
        takeaway: L("Beyond a certain volume, the loop sustains itself: no need to speak any more, the slightest noise is enough to start it. Only the amp's ceiling stops it. That is the Larsen effect.",
                    "Au-delà d'un certain volume, la boucle s'entretient d'elle-même : plus besoin de parler, le moindre bruit suffit à la lancer. Seul le plafond de l'ampli l'arrête. C'est l'effet Larsen."),
        hood: L("The threshold is when one round trip gives back as much as it receives (loop gain = 1). There is no “threshold” piece: it is born from the wiring.",
                "Le seuil, c'est quand un tour de boucle rend autant qu'il reçoit (gain de boucle = 1). Il n'y a pas de pièce « seuil » : il naît du câblage.") },

      { id: "distance", title: L("Moving the mic away", "Éloigner le micro"),
        goal: L("Leave the volume above the threshold. In the <b>scale model</b>, click the <b>mic</b> to move it away from the loudspeaker. Does the howl stop?",
                "Laisse le volume au-dessus du seuil. Dans la <b>Maquette</b>, clique sur le <b>micro</b> pour l'éloigner du haut-parleur. Le sifflement s'arrête-t-il ?"),
        need: app => { const a = app.model.first("ampli");
          return !loopWired(app.model) ? syn(KEEP_LOOP) :
                 a.p.gain < 1.05 ? pan(L("First turn the volume back up to the howl (above ×1).", "Remonte d'abord le volume jusqu'au sifflement (au-dessus de ×1).")) : null; },
        check: (app, mem) => {
          const hp = app.model.first("hp"), far = hp && hp.s.att < 1;
          const ok = far && !speaking(app) && lvl(app) < 2;
          mem.n = ok ? (mem.n || 0) + 1 : 0;
          return { p: mem.n / 100, done: mem.n >= 100,
            status: !far ? L("Click the mic, in the scale model on the right.", "Clique sur le micro, dans la Maquette à droite.") :
                    speaking(app) ? L("Fall silent to listen.", "Tais-toi pour écouter.") :
                    ok ? L("Calm returns… ", "Le calme revient… ") + `${app.fmtSteps(mem.n)} / 1.0 s` : L("Still howling: turn the volume down a little if needed.", "Ça siffle encore : baisse un peu le volume si besoin.") };
        },
        takeaway: L("The howl dies out without touching the volume. The threshold does not depend on a single piece but on the whole round trip, including the distance between mic and loudspeaker, which the Panel does not control.",
                    "Le sifflement s'éteint sans toucher au volume. Le seuil ne dépend pas d'une seule pièce mais de tout le tour de boucle, y compris de la distance entre le micro et le haut-parleur, que le Panneau ne règle pas."),
        hood: L("Loop gain = volume × efficiency × mic/loudspeaker coupling. The same volume can be tame or explosive depending on the rest of the circuit.",
                "Gain de boucle = volume × rendement × couplage micro/haut-parleur. Le même volume peut être sage ou explosif selon le reste du circuit.") }
    ],

    final: {
      title: L("You tamed the Larsen effect", "Tu as dompté le Larsen"),
      text: L("Wherever an output comes back to reinforce its input, there is a threshold beyond which everything runs away: a rumour going viral, a bank run, applause speeding up, an arms race. And often it is an outside ceiling, not the loop itself, that finally stops it.",
              "Partout où une sortie revient renforcer son entrée, il existe un seuil au-delà duquel tout s'emballe : une rumeur qui devient virale, une panique bancaire, des applaudissements qui s'accélèrent, une course aux armements. Et souvent, c'est un plafond extérieur, pas la boucle elle-même, qui finit par l'arrêter."),
      questions: [],
      hood: L("The Thermostat showed a loop that corrects (negative). Larsen shows a loop that reinforces (positive). Both are made of the same wires.",
              "Le Thermostat montrait une boucle qui corrige (négative). Larsen montre une boucle qui renforce (positive). Les deux sont faites des mêmes fils.")
    },

    free: {
      text: L("Every piece is unlocked. Try: does a more absorbent room (less reverberation) take more volume? What happens with a higher amp ceiling? Can you trigger the Larsen without ever speaking, with ambient noise alone?",
              "Toutes les pièces sont débloquées. Essaie : une salle plus absorbante (moins de réverbération) supporte-t-elle plus de volume ? Que se passe-t-il si le plafond de l'ampli est plus haut ? Peux-tu provoquer le Larsen sans jamais parler, avec le seul bruit ambiant ?"),
      hood: L("Generic pieces used: Storage, Source, Amplification, Transducer.", "Pièces génériques utilisées : Storage, Source, Amplification, Transducer.")
    },

    // ---------------------------------------------------------------- scale model
    view: function (host, model, api) {
      const arcs = (cx, cy, n, cls) => Array.from({ length: n }, (_, i) =>
        `<path class="${cls}" data-i="${i}" d="M${cx} ${cy - 14 - i * 12} A ${16 + i * 12} ${16 + i * 12} 0 0 0 ${cx} ${cy + 14 + i * 12}" fill="none" stroke-width="2.5" stroke-linecap="round"/>`).join("");
      host.innerHTML = `
<svg viewBox="0 0 440 300" role="img" preserveAspectRatio="xMidYMid meet">
  <rect x="0" y="0" width="440" height="300" rx="12" fill="#2b2a33"/>
  <rect id="lxAir" x="16" y="16" width="408" height="236" rx="8"/>
  <rect x="16" y="252" width="408" height="32" fill="#5a4636"/>
  <g id="lxPerson">
    <circle cx="70" cy="150" r="13" fill="#e9c9a6"/>
    <path d="M52 252 V190 Q52 172 70 172 Q88 172 88 190 V252 Z" fill="#4f6d8f"/>
    <g id="lxSpeech" stroke="#ffffff" stroke-width="2" fill="none" stroke-linecap="round" opacity="0">
      <path d="M90 140 q6 10 0 20"/><path d="M98 134 q9 16 0 32"/>
    </g>
  </g>
  <g id="lxMic" class="mq-click">
    <rect id="lxMicHit" x="0" y="0" width="40" height="150" fill="transparent"/>
    <line x1="20" y1="40" x2="20" y2="148" stroke="#b9b6ad" stroke-width="3"/>
    <line x1="8" y1="150" x2="32" y2="150" stroke="#b9b6ad" stroke-width="4" stroke-linecap="round"/>
    <rect x="13" y="16" width="14" height="26" rx="7" fill="#d8d5cc" stroke="#8a877e" stroke-width="1.5"/>
  </g>
  <g id="lxSpk">
    <rect x="352" y="96" width="56" height="96" rx="6" fill="#1d1c22" stroke="#77736a" stroke-width="2"/>
    <circle cx="380" cy="122" r="10" fill="#3a3942" stroke="#77736a"/>
    <circle id="lxCone" cx="380" cy="164" r="18" fill="#3a3942" stroke="#77736a" stroke-width="2"/>
    <line x1="380" y1="192" x2="380" y2="252" stroke="#77736a" stroke-width="4"/>
    <g id="lxWaves">${arcs(344, 160, 6, "lxArc")}</g>
  </g>
  <g id="lxMute" class="mq-click" transform="translate(396 24)">
    <rect width="28" height="24" rx="6" fill="#3a3942"/>
    <path d="M7 9 h4 l5 -4 v14 l-5 -4 h-4 z" fill="#d8d5cc"/>
    <path id="lxMuteOn" d="M19 8 q4 4 0 8" stroke="#d8d5cc" stroke-width="1.8" fill="none"/>
    <path id="lxMuteOff" d="M18 8 l6 8 M24 8 l-6 8" stroke="#e2685a" stroke-width="1.8"/>
  </g>
  <text id="lxEmpty" class="mq-note" x="220" y="150" text-anchor="middle" style="fill:#d8d5cc"></text>
</svg>`;
      const $ = id => host.querySelector("#" + id);
      const NEAR = 250, FAR = 150;
      let micX = NEAR, muted = false, audio = null;
      const ease = { lvl: 0, cone: 0 };

      function ensureAudio() {
        if (audio || muted) return;
        try {
          const AC = window.AudioContext || window.webkitAudioContext; if (!AC) return;
          const ctx = new AC(), osc = ctx.createOscillator(), gain = ctx.createGain();
          osc.type = "sine"; osc.frequency.value = 2200; gain.gain.value = 0;
          osc.connect(gain).connect(ctx.destination); osc.start();
          audio = { ctx, osc, gain };
        } catch (e) { audio = null; }
      }
      document.addEventListener("pointerdown", ensureAudio);
      $("lxMute").addEventListener("click", () => { muted = !muted; api.log("mute", muted); if (!muted) ensureAudio(); });
      $("lxMic").addEventListener("click", () => {
        const hp = model.first("hp");
        if (!hp) { api.toast(K.L("The mic only matters once there is a loudspeaker: place it in the Synoptic.", "Le micro ne compte que s'il y a un haut-parleur : pose-le dans le Synoptique.")); return; }
        hp.s.att = hp.s.att < 1 ? 1 : 0.5;
        api.log("mic", hp.s.att < 1 ? "far" : "near");
      });

      return {
        update(running) {
          const salle = model.first("salle"), voix = model.first("voix"), hp = model.first("hp"), ampli = model.first("ampli");
          host.querySelector("svg").setAttribute("aria-label", K.L("Scale model: a room with a PA system", "Maquette : une salle sonorisée"));
          $("lxEmpty").textContent = K.L("Empty room: place a Room in the Synoptic.", "Salle vide : pose une Salle dans le Synoptique.");
          $("lxEmpty").style.display = salle ? "none" : "";
          const Lv = salle ? salle.s.x : 0;
          ease.lvl += (Lv - ease.lvl) * 0.2;
          const f = Math.max(0, Math.min(1, ease.lvl / 100)), sat = !!(ampli && ampli.s.sat);
          $("lxAir").setAttribute("fill", salle ? `rgb(${Math.round(58 + 120 * f * (sat ? 1 : .5))},${Math.round(56 + 20 * f)},${Math.round(70 + 10 * f)})` : "#3a3942");
          $("lxPerson").style.display = voix && salle ? "" : "none";
          $("lxSpeech").setAttribute("opacity", voix && voix.s.u ? 0.9 : 0);
          $("lxMic").style.display = salle ? "" : "none";
          const far = !!(hp && hp.s.att < 1);
          micX += ((far ? FAR : NEAR) - micX) * 0.15;
          $("lxMic").setAttribute("transform", `translate(${(micX - 20).toFixed(1)} 98)`);
          $("lxSpk").style.display = hp ? "" : "none";
          if (hp) {
            const out = Math.max(0, Math.min(1, (hp.s.flow || 0) / 900));
            ease.cone = running ? Math.sin(performance.now() / (sat ? 18 : 60)) * out : 0;
            $("lxCone").setAttribute("r", (18 + 2.5 * ease.cone).toFixed(2));
            host.querySelectorAll(".lxArc").forEach(a => {
              const i = +a.dataset.i, on = out > i / 6 + 0.01;
              a.setAttribute("stroke", sat ? "#ff8a3d" : "#cfd8e6");
              a.setAttribute("opacity", on ? (0.85 - i * 0.1).toFixed(2) : 0);
            });
          }
          $("lxMuteOn").style.display = muted ? "none" : ""; $("lxMuteOff").style.display = muted ? "" : "none";
          if (audio) {
            const loud = !muted && running && hp ? Math.max(0, Math.min(1, (Lv - 30) / 60)) : 0;
            audio.gain.gain.setTargetAtTime(0.05 * loud, audio.ctx.currentTime, 0.05);
            audio.osc.frequency.setTargetAtTime(far ? 2600 : 2100, audio.ctx.currentTime, 0.2);
          }
        }
      };
    }
  };
  };

  (K.workshops = K.workshops || {}).larsen = factory;
})(window.TSCGKit = window.TSCGKit || {});
