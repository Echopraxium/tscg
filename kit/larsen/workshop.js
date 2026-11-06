/* TSCG Kit — Larsen workshop definition
 * A room, a voice, an amplifier and a loudspeaker. Sound levels are an envelope
 * model (no waveform): the room absorbs, the loudspeaker re-injects what the
 * microphone picks up. Above a loop gain of 1 the loop feeds itself: Larsen.
 * Time unit: seconds, one step = 10 ms, shown in slow motion.
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

  const W = {
    id: "larsen",
    title: "Atelier TSCG — Larsen",
    pageTitle: "TSCG Atelier — Larsen",
    fluxLabel: "flux (son)",
    clock: { dt: 0.01, stepsPerSec: 25, fmt: t => t.toFixed(1) + " s", fmtSteps: n => (n * 0.01).toFixed(1) + " s" },
    order: ["salle", "voix", "ampli", "hp"],
    home: { voix: { x: 16, y: 24 }, salle: { x: 236, y: 24 }, ampli: { x: 456, y: 220 }, hp: { x: 16, y: 220 } },

    skins: {
      salle: { kind: "storage", name: "Salle", blurb: "le son s'y accumule puis s'éteint",
        ports: { in: "son reçu", out: "fuite", level: "capté par le micro" },
        describe: n => "niveau " + n.s.x.toFixed(0),
        params: { decay: { label: "Absorption (/s)", v: 10, step: 1, min: 1, max: 40 },
                  C: { v: 1, hidden: true }, k: { v: 0, hidden: true }, x0: { v: 0, hidden: true },
                  base: { label: "Bruit ambiant", v: 0.5, step: 0.5, min: 0, max: 20 }, lo: { v: 0, hidden: true } } },
      voix: { kind: "source", name: "Voix", blurb: "quelqu'un parle", onText: "parle", offText: "se tait",
        ports: { cmd: "commande", flow: "son" },
        params: { P: { label: "Force de la voix", v: 100, step: 10, min: 0, max: 300 } } },
      ampli: { kind: "amplify", name: "Ampli", blurb: "multiplie le signal du micro",
        ports: { x: "signal du micro", y: "signal amplifié" },
        describe: n => (n.s.sat ? "saturé" : "gain ×" + n.p.gain.toFixed(2)),
        params: { gain: { label: "Volume (gain)", v: 0.3, step: 0.05, min: 0, max: 2.5 },
                  max: { label: "Plafond de sortie", v: 90, step: 5, min: 10, max: 200 } } },
      hp: { kind: "transducer", name: "Haut-parleur", blurb: "change le signal en son",
        ports: { x: "signal", flow: "son" },
        describe: n => (n.s.att < 1 ? "micro éloigné · " : "") + "son " + n.s.flow.toFixed(0),
        params: { k: { label: "Rendement", v: 10, step: 1, min: 0, max: 30 }, max: { v: 5000, hidden: true }, noise: { v: 0, hidden: true } } }
    },

    instruments: {
      vumetre: { type: "gauge", label: "Vu-mètre de la salle", short: "Niveau", bind: { piece: "salle", get: "level" }, range: [0, 100], decimals: 0, unit: "", zone: [18, 30] },
      parler:  { type: "toggle", label: "Bouton de la voix", short: "Voix", bind: { piece: "voix", set: "manual" }, onText: "parle", offText: "silence" },
      volume:  { type: "slider", label: "Volume de l'ampli", short: "Volume", bind: { piece: "ampli", param: "gain" }, range: [0, 2.5], step: 0.05, decimals: 2, unit: "×" },
      sature:  { type: "lamp", label: "Témoin de saturation de l'ampli", short: "Saturation", bind: { piece: "ampli", get: "sat" } }
    },

    chart: {
      range: [0, 100], tickY: 25, span: 4, tick: 1, label: t => t + " s",
      series: [{ piece: "salle", label: "Niveau dans la salle", color: "--flux" }],
      strips: [
        { label: "voix", color: "--info", on: (p, m) => { const v = m.first("voix"); return !!(v && p.u[v.id]); } },
        { label: "ampli saturé", color: "--bad", on: (p, m) => { const a = m.first("ampli"); return !!(a && p.u[a.id]); } }
      ]
    },

    steps: [
      { id: "talk", title: "Parler dans la salle",
        unlock: { pieces: ["salle", "voix"], instruments: ["vumetre", "parler"] },
        goal: "Dans le <b>Synoptique</b>, pose une <b>Salle</b> et une <b>Voix</b>, et relie le <i>son</i> de la Voix à la Salle. Dans le <b>Panneau</b>, ajoute le <b>vu-mètre</b> et le <b>bouton de la voix</b>. Lance le temps, parle un instant, puis tais-toi.",
        need: app => { const m = app.model;
          return !m.first("salle") || !m.first("voix") ? syn("Pose une Salle et une Voix dans le Synoptique.") :
                 !m.linked("voix", "flow", "salle", "in") ? syn("Relie le son de la Voix à la Salle.") :
                 !app.panel.has("vumetre") ? pan("Ajoute le vu-mètre dans le Panneau.") :
                 !app.panel.has("parler") ? pan("Ajoute le bouton de la voix dans le Panneau.") : null; },
        check: (app, mem) => {
          if (speaking(app)) mem.spoke = (mem.spoke || 0) + 1;
          const s = mem.spoke || 0;
          if (s < 30) return { p: 0.5 * s / 30, done: false, status: s ? "Continue de parler un instant…" : "Clique sur le bouton de la voix pour parler." };
          if (speaking(app)) return { p: 0.5, done: false, status: "Maintenant, tais-toi (clique à nouveau sur le bouton)." };
          return { p: lvl(app) < 1 ? 1 : 0.75, done: lvl(app) < 1, status: "Écoute le niveau retomber…" };
        },
        takeaway: "Quand tu parles, le niveau monte puis se stabilise. Quand tu te tais, il retombe tout seul : la salle absorbe le son. Le silence est l'état vers lequel elle revient toujours.",
        hood: "Salle = <b>Storage</b> qui se vide d'elle-même (absorption). Voix = <b>Source</b>." },

      { id: "amplify", title: "Sonoriser",
        unlock: { pieces: ["ampli", "hp"], instruments: ["volume"] },
        goal: "Pose un <b>Ampli</b> et un <b>Haut-parleur</b>. Relie ce que la Salle <i>capte par le micro</i> à l'Ampli, l'Ampli au Haut-parleur, et le <i>son</i> du Haut-parleur à la Salle. Ajoute le <b>curseur de volume</b>. Puis, en parlant, amène le vu-mètre dans la zone verte et tiens une seconde.",
        hint: "Monte le volume doucement.",
        need: app => { const m = app.model;
          return !m.first("ampli") || !m.first("hp") ? syn("Pose un Ampli et un Haut-parleur.") :
                 !m.linked("salle", "level", "ampli", "x") ? syn("Relie ce que capte le micro (Salle) à l'Ampli.") :
                 !m.linked("ampli", "y", "hp", "x") ? syn("Relie l'Ampli au Haut-parleur.") :
                 !m.linked("hp", "flow", "salle", "in") ? syn("Relie le son du Haut-parleur à la Salle.") :
                 !app.panel.has("volume") ? pan("Ajoute le curseur de volume dans le Panneau.") : null; },
        check: (app, mem) => {
          const ok = speaking(app) && lvl(app) >= 18 && lvl(app) <= 30 && !saturated(app);
          mem.n = ok ? (mem.n || 0) + 1 : 0;
          return { p: mem.n / 100, done: mem.n >= 100,
            status: !speaking(app) ? "Parle (bouton de la voix) pour remplir la salle." : ok ? `Tiens bon… ${app.fmtSteps(mem.n)} / 1.0 s` :
                    lvl(app) < 18 ? "Pas assez fort : monte un peu le volume." : "Trop fort : baisse un peu le volume." };
        },
        takeaway: "Ta voix porte plus loin : le haut-parleur renvoie dans la salle ce que le micro capte, qui est capté à nouveau, renvoyé… La sortie revient renforcer l'entrée. Pour l'instant, chaque tour rend moins qu'il ne reçoit, et tout reste calme.",
        hood: "Ampli = <b>Amplification</b>. Haut-parleur = <b>Transducer</b> (signal → son). Le chemin Salle → Ampli → Haut-parleur → Salle forme une <b>Feedback Loop</b> positive." },

      { id: "whistle", title: "Le sifflement",
        unlock: { instruments: ["sature"] },
        predict: { q: "Avant d'essayer : si tu montes encore le volume, puis que tu te tais, que va-t-il se passer ?",
                   choices: ["Le son retombe, comme avant", "Le son reste un peu plus fort", "Ça siffle, et ça ne s'arrête plus"] },
        goal: "Ajoute le <b>témoin de saturation</b>. Monte le volume petit à petit, puis tais-toi. Observe le vu-mètre, la Maquette… et écoute.",
        hint: "Le son de la Maquette se coupe avec le petit haut-parleur en haut à droite.",
        need: app => !loopWired(app.model) ? syn("Garde la boucle Salle → Ampli → Haut-parleur → Salle.") :
                     !app.panel.has("sature") ? pan("Ajoute le témoin de saturation dans le Panneau.") : null,
        check: (app, mem) => {
          const ok = !speaking(app) && saturated(app);
          mem.n = ok ? (mem.n || 0) + 1 : 0;
          return { p: mem.n / 100, done: mem.n >= 100,
            status: speaking(app) ? "Tais-toi, pour voir ce que fait la boucle toute seule." : ok ? `Ça tient tout seul… ${app.fmtSteps(mem.n)} / 1.0 s` : "Monte encore le volume, doucement." };
        },
        takeaway: "Au-delà d'un certain volume, la boucle s'entretient d'elle-même : plus besoin de parler, le moindre bruit suffit à la lancer. Seul le plafond de l'ampli l'arrête. C'est l'effet Larsen.",
        hood: "Le seuil, c'est quand un tour de boucle rend autant qu'il reçoit (gain de boucle = 1). Il n'y a pas de pièce « seuil » : il naît du câblage." },

      { id: "distance", title: "Éloigner le micro",
        goal: "Laisse le volume au-dessus du seuil. Dans la <b>Maquette</b>, clique sur le <b>micro</b> pour l'éloigner du haut-parleur. Le sifflement s'arrête-t-il ?",
        need: app => { const a = app.model.first("ampli");
          return !loopWired(app.model) ? syn("Garde la boucle Salle → Ampli → Haut-parleur → Salle.") :
                 a.p.gain < 1.05 ? pan("Remonte d'abord le volume jusqu'au sifflement (au-dessus de ×1).") : null; },
        check: (app, mem) => {
          const hp = app.model.first("hp"), far = hp && hp.s.att < 1;
          const ok = far && !speaking(app) && lvl(app) < 2;
          mem.n = ok ? (mem.n || 0) + 1 : 0;
          return { p: mem.n / 100, done: mem.n >= 100,
            status: !far ? "Clique sur le micro, dans la Maquette à droite." : speaking(app) ? "Tais-toi pour écouter." : ok ? `Le calme revient… ${app.fmtSteps(mem.n)} / 1.0 s` : "Ça siffle encore : baisse un peu le volume si besoin." };
        },
        takeaway: "Le sifflement s'éteint sans toucher au volume. Le seuil ne dépend pas d'une seule pièce mais de tout le tour de boucle, y compris de la distance entre le micro et le haut-parleur, que le Panneau ne règle pas.",
        hood: "Gain de boucle = volume × rendement × couplage micro/haut-parleur. Le même volume peut être sage ou explosif selon le reste du circuit." }
    ],

    final: {
      title: "Tu as dompté le Larsen",
      text: "Partout où une sortie revient renforcer son entrée, il existe un seuil au-delà duquel tout s'emballe : une rumeur qui devient virale, une panique bancaire, des applaudissements qui s'accélèrent, une course aux armements. Et souvent, c'est un plafond extérieur, pas la boucle elle-même, qui finit par l'arrêter.",
      questions: [],
      hood: "Le Thermostat montrait une boucle qui corrige (négative). Larsen montre une boucle qui renforce (positive). Les deux sont faites des mêmes fils."
    },

    free: {
      text: "Toutes les pièces sont débloquées. Essaie : une salle plus absorbante (moins de réverbération) supporte-t-elle plus de volume ? Que se passe-t-il si le plafond de l'ampli est plus haut ? Peux-tu provoquer le Larsen sans jamais parler, avec le seul bruit ambiant ?",
      hood: "Pièces génériques utilisées : Storage, Source, Amplification, Transducer."
    },

    // ---------------------------------------------------------------- Maquette
    view: function (host, model, api) {
      const arcs = (cx, cy, n, cls) => Array.from({ length: n }, (_, i) =>
        `<path class="${cls}" data-i="${i}" d="M${cx} ${cy - 14 - i * 12} A ${16 + i * 12} ${16 + i * 12} 0 0 0 ${cx} ${cy + 14 + i * 12}" fill="none" stroke-width="2.5" stroke-linecap="round"/>`).join("");
      host.innerHTML = `
<svg viewBox="0 0 440 300" role="img" aria-label="Maquette : une salle sonorisée" preserveAspectRatio="xMidYMid meet">
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
  <text id="lxEmpty" class="mq-note" x="220" y="150" text-anchor="middle" fill="#d8d5cc" style="fill:#d8d5cc">Salle vide : pose une Salle dans le Synoptique.</text>
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
        if (!hp) { api.toast("Le micro ne compte que s'il y a un haut-parleur : pose-le dans le Synoptique."); return; }
        hp.s.att = hp.s.att < 1 ? 1 : 0.5;
        api.log("mic", hp.s.att < 1 ? "far" : "near");
      });

      return {
        update(running) {
          const salle = model.first("salle"), voix = model.first("voix"), hp = model.first("hp"), ampli = model.first("ampli");
          $("lxEmpty").style.display = salle ? "none" : "";
          const L = salle ? salle.s.x : 0;
          ease.lvl += (L - ease.lvl) * 0.2;
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
            const loud = !muted && running && hp ? Math.max(0, Math.min(1, (L - 30) / 60)) : 0;
            audio.gain.gain.setTargetAtTime(0.05 * loud, audio.ctx.currentTime, 0.05);
            audio.osc.frequency.setTargetAtTime(far ? 2600 : 2100, audio.ctx.currentTime, 0.2);
          }
        }
      };
    }
  };

  (K.workshops = K.workshops || {}).larsen = W;
})(window.TSCGKit = window.TSCGKit || {});
