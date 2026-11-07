/* TSCG Kit — Drinking bird workshop definition
 * A glass bird bobs and drinks, on its own, for hours. The wet felt on its head
 * evaporates and cools it: the vapour pressure drops in the head, the liquid climbs
 * up the neck, the bird tips, its beak dips, the tube opens, the liquid runs back
 * down, and it straightens up. The level in the head runs between two thresholds
 * and never settles: a loop with no resting place, an oscillator.
 * Time unit: seconds, one step = 0.1 s.
 * The definition is a factory: L(english, french) picks every text.
 * Author: Echopraxium with the collaboration of Claude AI
 */
(function (K) {
  "use strict";
  const syn = msg => ({ msg, tab: "synoptic" });
  const pan = msg => ({ msg, tab: "panel" });
  const tipped = app => { const b = app.model.first("bascule"); return !!(b && b.s.x !== null && b.s.u); };
  const head = app => { const t = app.model.first("tete"); return t ? t.s.x : 0; };
  // counts the times the bird tips forward (rising edges of the Tilt)
  const countTips = (app, mem) => { const t = tipped(app); if (t && !mem.prev) mem.tips = (mem.tips || 0) + 1; mem.prev = t; return mem.tips || 0; };
  const T = s => (s < 60 ? `${Math.floor(s)} s` : `${Math.floor(s / 60)} min ${String(Math.floor(s % 60)).padStart(2, "0")} s`);

  const factory = L => {
    const KEEP_HEAD = L("Keep the Evaporation wired to the Head.", "Garde l'Évaporation reliée à la Tête.");
    const KEEP_TILT = L("Keep the Head's level wired to the Tilt.", "Garde le niveau de la Tête relié à la Bascule.");
    const KEEP_BACK = L("Keep the return: Head → Return, and Tilt → Return's opening.", "Garde le retour : Tête → Retour, et Bascule → ouverture du Retour.");
    const loopOK = m => m.linked("evap", "flow", "tete", "in") && m.linked("tete", "level", "bascule", "x") &&
                        m.linked("tete", "out", "retour", "in") && m.linked("bascule", "u", "retour", "cmd");
    return {
    id: "oiseau",
    title: L("TSCG Workshop — Drinking bird", "Atelier TSCG — Oiseau buveur"),
    pageTitle: L("TSCG Workshop — Drinking bird", "TSCG Atelier — Oiseau buveur"),
    fluxLabel: L("flux (liquid, water)", "flux (liquide, eau)"),
    clock: { dt: 0.1, stepsPerSec: 10, fmt: t => T(t), fmtSteps: n => T(n * 0.1),
             speedLabel: (spr, LL) => Math.abs(spr - 1) < 1e-6 ? LL("real time", "temps réel") : "×" + Math.round(spr * 100) / 100 },
    order: ["tete", "evap", "bascule", "retour", "feutre", "verre"],
    home: { evap: { x: 16, y: 20 }, tete: { x: 206, y: 20 }, retour: { x: 396, y: 20 }, bascule: { x: 206, y: 190 },
            feutre: { x: 16, y: 200 }, verre: { x: 16, y: 330 } },

    skins: {
      tete: { kind: "storage", icon: "head", name: L("Head", "Tête"), blurb: L("the liquid climbs up the neck into it", "le liquide y monte par le cou"), color: "#c0392b", unit: "%",
        ports: { in: L("liquid rising", "liquide qui monte"), out: L("back down", "redescente"), level: L("level", "niveau") },
        describe: n => K.L("liquid ", "liquide ") + n.s.x.toFixed(0) + " %",
        params: { C: { label: L("Neck volume", "Volume du cou"), v: 30, step: 5, min: 5, max: 200 },
                  x0: { label: L("Start level (%)", "Niveau initial (%)"), v: 30, step: 5, min: 0, max: 100 },
                  k: { v: 0, hidden: true }, lo: { v: 0, hidden: true }, hi: { v: 100, hidden: true } } },
      evap: { kind: "source", icon: "evap", on: true, name: L("Evaporation", "Évaporation"),
        blurb: L("the wet felt cools the head: the vapour pushes the liquid up", "le feutre mouillé refroidit la tête : la vapeur pousse le liquide vers le haut"),
        ports: { cmd: L("felt wet?", "feutre mouillé ?"), flow: L("rising", "montée") },
        describe: n => !n.s.u ? K.L("dry felt: stopped", "feutre sec : arrêt") :
                       n.p.P <= 0 ? K.L("saturated air: nothing evaporates", "air saturé : rien ne s'évapore") :
                       K.L("evaporating · dry air ", "s'évapore · air sec ") + n.p.P + " %",
        params: { P: { label: L("Air dryness (%)", "Sécheresse de l'air (%)"), v: 60, step: 5, min: 0, max: 100 } } },
      bascule: { kind: "threshold", icon: "tilt", above: true, name: L("Tilt", "Bascule"),
        blurb: L("tips forward when the head is heavy, straightens up when it is light", "penche quand la tête est lourde, se redresse quand elle est légère"),
        onText: L("tipped: drinks", "penché : boit"), offText: L("upright", "debout"),
        ports: { x: L("level", "niveau"), u: L("tipped", "penché") },
        params: { set: { label: L("Balance point (%)", "Point d'équilibre (%)"), v: 70, step: 5, min: 10, max: 95 },
                  h: { label: L("Hysteresis (%)", "Hystérésis (%)"), v: 40, step: 5, min: 0, max: 80 } } },
      retour: { kind: "sink", icon: "drain", name: L("Return", "Retour"),
        blurb: L("when the bird tips, the tube opens and the liquid runs back to the body", "quand l'oiseau penche, le tube s'ouvre et le liquide redescend dans le ventre"),
        ports: { in: L("liquid", "liquide"), cmd: L("opening", "ouverture") },
        describe: n => n.s.open ? K.L("tube open: back down", "tube ouvert : ça redescend") : K.L("tube closed", "tube fermé"),
        params: { kOpen: { label: L("Return speed", "Vitesse du retour"), v: 12, step: 1, min: 1, max: 60 }, level: { v: 0, hidden: true } } },
      feutre: { kind: "storage", icon: "felt", name: L("Felt", "Feutre"), blurb: L("the cloth on the head: it dries in the air", "l'étoffe sur la tête : elle sèche à l'air"), color: "#3f7fd6",
        ports: { in: L("water", "eau"), out: "", level: L("wet?", "mouillé ?") },
        describe: n => K.L("wet ", "mouillé ") + Math.round(n.s.x * 100) + " %",
        params: { decay: { label: L("Drying (/s)", "Séchage (/s)"), v: 0.012, step: 0.002, min: 0, max: 0.2 },
                  C: { v: 1, hidden: true }, k: { v: 0, hidden: true }, x0: { v: 1, hidden: true }, lo: { v: 0, hidden: true }, hi: { v: 1, hidden: true } } },
      verre: { kind: "source", icon: "glass", name: L("Glass of water", "Verre d'eau"), blurb: L("the beak dips into it and wets the felt again", "le bec y trempe et remouille le feutre"),
        ports: { cmd: L("beak dips", "bec qui trempe"), flow: L("water", "eau") },
        describe: n => n.p.P <= 0 ? K.L("empty", "vide") : n.s.u ? K.L("beak in the water", "bec dans l'eau") : K.L("full", "plein"),
        params: { P: { label: L("Wetting (/s)", "Mouillage (/s)"), v: 0.6, step: 0.1, min: 0, max: 3 } } }
    },

    instruments: {
      headGauge: { type: "gauge", label: L("Level in the head", "Niveau dans la tête"), short: L("Head", "Tête"), bind: { piece: "tete", get: "level" }, range: [0, 100], step: 1, decimals: 0, unit: "%" },
      drinkLamp: { type: "lamp", label: L("Tilt light (drinking)", "Témoin de bascule (boit)"), short: L("Drinks", "Boit"), bind: { piece: "bascule", get: "u" } },
      drySlider: { type: "slider", label: L("Air dryness", "Sécheresse de l'air"), short: L("Dry air", "Air sec"), bind: { piece: "evap", param: "P" }, range: [0, 100], step: 5, decimals: 0, unit: "%" },
      evapLamp:  { type: "lamp", label: L("Evaporation light", "Témoin d'évaporation"), short: L("Evap.", "Évap."), bind: { piece: "evap", get: "u" } }
    },

    chart: {
      range: [0, 100], tickY: 25, span: 120, unit: 1,
      series: [{ piece: "tete", label: L("Liquid in the head", "Liquide dans la tête"), color: "#c0392b", unit: "%", decimals: 0 }],
      lines: [{ piece: "bascule", value: n => n.p.set + n.p.h / 2, label: L("tips at", "bascule à"), color: "--bad", unit: "%", decimals: 0 },
              { piece: "bascule", value: n => n.p.set - n.p.h / 2, label: L("straightens at", "se redresse à"), color: "--good", unit: "%", decimals: 0 }],
      strips: [
        { label: L("drinking", "boit"), color: "--info", on: (p, m) => { const b = m.first("bascule"); return !!(b && p.v[b.id] === 1); } },
        { label: L("dry felt", "feutre sec"), color: "--bad", on: (p, m) => { const f = m.first("feutre"); return !!(f && p.v[f.id] < 0.5); } }
      ]
    },

    steps: [
      { id: "fill", title: L("A head that fills up", "Une tête qui se remplit"),
        unlock: { pieces: ["tete", "evap"], instruments: ["headGauge"] },
        goal: L("In the <b>Synoptic</b>, place a <b>Head</b> and an <b>Evaporation</b>, and wire the Evaporation's <i>rising</i> to the Head. In the <b>Panel</b>, add the gauge of the <b>level in the head</b>. Start the time and watch.",
                "Dans le <b>Synoptique</b>, pose une <b>Tête</b> et une <b>Évaporation</b>, et relie la <i>montée</i> de l'Évaporation à la Tête. Dans le <b>Panneau</b>, ajoute la jauge du <b>niveau dans la tête</b>. Lance le temps et observe."),
        hint: L("Watch the neck of the bird in the scale model.", "Regarde le cou de l'oiseau dans la Maquette."),
        need: app => { const m = app.model;
          return !m.first("tete") || !m.first("evap") ? syn(L("Place a Head and an Evaporation in the Synoptic.", "Pose une Tête et une Évaporation dans le Synoptique.")) :
                 !m.linked("evap", "flow", "tete", "in") ? syn(L("Wire the Evaporation to the Head.", "Relie l'Évaporation à la Tête.")) :
                 !app.panel.has("headGauge") ? pan(L("Add the head level gauge in the Panel.", "Ajoute la jauge du niveau dans la tête dans le Panneau.")) : null; },
        check: (app, mem) => {
          const full = head(app) >= 99.5; mem.n = full ? (mem.n || 0) + 1 : 0;
          return { p: full ? 0.8 + 0.2 * mem.n / 50 : 0.8 * head(app) / 100, done: mem.n >= 50,
                   status: full ? L("Full… and now?", "Plein… et maintenant ?") : L("The liquid climbs…", "Le liquide monte…") };
        },
        takeaway: L("The liquid climbs, the bird leans a little… and then nothing more happens: the head is full, and stays full. A store that only fills ends up stuck.",
                    "Le liquide monte, l'oiseau se penche un peu… puis plus rien : la tête est pleine, et le reste. Une réserve qui ne fait que se remplir finit bloquée."),
        hood: L("Head = <b>Storage</b>. Evaporation = <b>Source</b>: here the energy comes from the air around.", "Tête = <b>Storage</b>. Évaporation = <b>Source</b> : ici, l'énergie vient de l'air ambiant.") },

      { id: "tilt", title: L("Tipping over", "Basculer"),
        unlock: { pieces: ["bascule"], instruments: ["drinkLamp"] },
        enter: app => { const t = app.model.first("tete"); if (t) t.s.x = 30; },
        goal: L("The head has emptied back to 30 %. Place a <b>Tilt</b> and wire the Head's <i>level</i> to it. Add the <b>tilt light</b> to the Panel. Start the time again.",
                "La tête est redescendue à 30 %. Pose une <b>Bascule</b> et relie-lui le <i>niveau</i> de la Tête. Ajoute le <b>témoin de bascule</b> au Panneau. Relance le temps."),
        need: app => { const m = app.model;
          return !m.linked("evap", "flow", "tete", "in") ? syn(KEEP_HEAD) :
                 !m.first("bascule") ? syn(L("Place a Tilt in the Synoptic.", "Pose une Bascule dans le Synoptique.")) :
                 !m.linked("tete", "level", "bascule", "x") ? syn(L("Wire the Head's level to the Tilt.", "Relie le niveau de la Tête à la Bascule.")) :
                 !app.panel.has("drinkLamp") ? pan(L("Add the tilt light in the Panel.", "Ajoute le témoin de bascule dans le Panneau.")) : null; },
        check: (app, mem) => {
          const t = tipped(app); mem.n = t ? (mem.n || 0) + 1 : 0;
          return { p: t ? 0.6 + 0.4 * mem.n / 60 : 0.6 * Math.min(1, head(app) / 90), done: mem.n >= 60,
                   status: t ? L("It drinks… ", "Il boit… ") + T(mem.n * 0.1) : L("The head gets heavier…", "La tête s'alourdit…") };
        },
        takeaway: L("It tips forward and drinks… and stays there, beak in the water. Nothing takes the liquid out of the head, so it never gets light again.",
                    "Il penche et boit… et reste là, le bec dans l'eau. Rien ne fait ressortir le liquide de la tête : elle ne redevient jamais légère."),
        hood: L("Tilt = <b>Threshold</b> with hysteresis: it tips above 90 % but straightens up only below 50 %.",
                "Bascule = <b>Threshold</b> avec hystérésis : elle penche au-dessus de 90 % mais ne se redresse qu'en dessous de 50 %.") },

      { id: "drink", title: L("Drinking, again and again", "Boire, encore et encore"),
        unlock: { pieces: ["retour"] },
        enter: app => { const t = app.model.first("tete"); if (t) t.s.x = 30; },
        predict: { q: L("Before you start: once the return is wired, what will the bird do?", "Avant de lancer : une fois le retour branché, que va faire l'oiseau ?"),
                   choices: [L("Drink once, then stay upright", "Boire une fois, puis rester debout"), L("Settle half-leaning", "Se stabiliser à moitié penché"), L("Drink again and again", "Boire encore et encore")] },
        goal: L("Place a <b>Return</b>. Wire the Head's <i>back down</i> output to it, and the Tilt's <i>tipped</i> output to the Return's <i>opening</i>. Let the bird drink <b>4 times</b>.",
                "Pose un <b>Retour</b>. Relie-lui la sortie <i>redescente</i> de la Tête, et la sortie <i>penché</i> de la Bascule à l'<i>ouverture</i> du Retour. Laisse l'oiseau boire <b>4 fois</b>."),
        curves: true,
        hint: L("Look at the curve: between which two lines does the level travel?", "Regarde la courbe : entre quelles deux lignes le niveau voyage-t-il ?"),
        need: app => { const m = app.model;
          return !m.linked("evap", "flow", "tete", "in") ? syn(KEEP_HEAD) : !m.linked("tete", "level", "bascule", "x") ? syn(KEEP_TILT) :
                 !m.first("retour") ? syn(L("Place a Return in the Synoptic.", "Pose un Retour dans le Synoptique.")) :
                 !m.linked("tete", "out", "retour", "in") ? syn(L("Wire the Head's back down output to the Return.", "Relie la redescente de la Tête au Retour.")) :
                 !m.linked("bascule", "u", "retour", "cmd") ? syn(L("Wire the Tilt's tipped output to the Return's opening.", "Relie la sortie penché de la Bascule à l'ouverture du Retour.")) : null; },
        check: (app, mem) => { const n = countTips(app, mem);
          return { p: n / 4, done: n >= 4, status: L("Drinks: ", "Gorgées : ") + `${n} / 4` }; },
        takeaway: L("It never stops. Each sip empties the head, which fills up again, which tips it again… The level goes back and forth between the two lines and never settles anywhere.",
                    "Il ne s'arrête plus. Chaque gorgée vide la tête, qui se remplit à nouveau, qui le fait basculer à nouveau… Le niveau fait l'aller-retour entre les deux lignes et ne se pose jamais nulle part."),
        hood: L("Return = <b>Sink</b> opened by a command. Head → Tilt → Return → Head is a negative <b>Feedback Loop</b>; with a hysteresis and no resting point inside it, the loop <b>oscillates</b>.",
                "Retour = <b>Sink</b> ouvert par une commande. Tête → Bascule → Retour → Tête est une <b>Feedback Loop</b> négative ; avec une hystérésis et aucun point de repos à l'intérieur, la boucle <b>oscille</b>.") },

      { id: "humid", title: L("Humid air", "L'air humide"),
        unlock: { instruments: ["drySlider"] },
        predict: { q: L("Before trying: if the air becomes more and more humid, what happens to the bird?", "Avant d'essayer : si l'air devient de plus en plus humide, que devient l'oiseau ?"),
                   choices: [L("Nothing changes", "Rien ne change"), L("It drinks faster", "Il boit plus vite"), L("It drinks more slowly", "Il boit plus lentement")] },
        goal: L("Add the <b>air dryness</b> slider. Lower it to 30 % or less and let the bird drink once. Then bring it down to <b>0 %</b> (saturated air) and watch for 30 seconds.",
                "Ajoute le curseur de <b>sécheresse de l'air</b>. Baisse-le à 30 % ou moins et laisse l'oiseau boire une fois. Puis descends-le à <b>0 %</b> (air saturé) et observe pendant 30 secondes."),
        need: app => !loopOK(app.model) ? syn(KEEP_BACK) :
                     !app.panel.has("drySlider") ? pan(L("Add the air dryness slider in the Panel.", "Ajoute le curseur de sécheresse de l'air dans le Panneau.")) : null,
        check: (app, mem) => {
          const P = app.model.first("evap").p.P, n = countTips(app, mem);
          if (!mem.slow) {
            if (P <= 30 && P > 0) { if (mem.base === undefined) mem.base = n; if (n > mem.base) mem.slow = true; }
            else mem.base = undefined;
            return { p: 0.1 + (mem.base !== undefined ? 0.3 : 0), done: false,
                     status: P > 30 ? L("Lower the dryness to 30 % or less.", "Baisse la sécheresse à 30 % ou moins.") :
                             P <= 0 ? L("First let it drink once with a little dry air (5 to 30 %).", "Laisse-le d'abord boire une fois avec un peu d'air sec (5 à 30 %).") :
                             L("Wait for the next sip… it takes longer.", "Attends la prochaine gorgée… elle se fait attendre.") };
          }
          mem.n = P <= 0 ? (mem.n || 0) + 1 : 0;
          return { p: 0.5 + 0.5 * mem.n / 300, done: mem.n >= 300,
                   status: P > 0 ? L("Now bring the dryness down to 0 %.", "Descends maintenant la sécheresse à 0 %.") : L("Saturated air… ", "Air saturé… ") + T(mem.n * 0.1) + " / 30 s" };
        },
        takeaway: L("The more humid the air, the more slowly it drinks. In saturated air, it stops. The bird has no battery: the energy that makes it move comes from the dry air of the room.",
                    "Plus l'air est humide, plus il boit lentement. Dans un air saturé, il s'arrête. L'oiseau n'a pas de pile : l'énergie qui le fait bouger vient de l'air sec de la pièce."),
        hood: L("The <b>Source</b> of a system is often outside it. Here, the drinking bird is a small heat engine fed by the gap between dry air and wet felt.",
                "La <b>Source</b> d'un système est souvent hors de lui. Ici, l'oiseau buveur est un petit moteur thermique nourri par l'écart entre l'air sec et le feutre mouillé.") },

      { id: "glass", title: L("The glass of water", "Le verre d'eau"),
        unlock: { pieces: ["feutre", "verre"], instruments: ["evapLamp"] },
        enter: app => { const e = app.model.first("evap"); if (e && e.p.P < 40) e.p.P = 60; },
        goal: L("The air is dry again. Place a <b>Felt</b> and a <b>Glass of water</b>. Wire the Felt's <i>wet?</i> to the Evaporation, the Glass's <i>water</i> to the Felt, and the Tilt's <i>tipped</i> to the Glass (<i>beak dips</i>). Add the <b>evaporation light</b>. Once the bird drinks, click the <b>glass</b> in the scale model to empty it.",
                "L'air est redevenu sec. Pose un <b>Feutre</b> et un <b>Verre d'eau</b>. Relie le <i>mouillé ?</i> du Feutre à l'Évaporation, l'<i>eau</i> du Verre au Feutre, et le <i>penché</i> de la Bascule au Verre (<i>bec qui trempe</i>). Ajoute le <b>témoin d'évaporation</b>. Quand l'oiseau boit, clique sur le <b>verre</b> dans la Maquette pour le vider."),
        need: app => { const m = app.model;
          return !loopOK(m) ? syn(KEEP_BACK) :
                 !m.first("feutre") || !m.first("verre") ? syn(L("Place a Felt and a Glass of water.", "Pose un Feutre et un Verre d'eau.")) :
                 !m.linked("feutre", "level", "evap", "cmd") ? syn(L("Wire the Felt's wet? output to the Evaporation.", "Relie le mouillé ? du Feutre à l'Évaporation.")) :
                 !m.linked("verre", "flow", "feutre", "in") ? syn(L("Wire the Glass's water to the Felt.", "Relie l'eau du Verre au Feutre.")) :
                 !m.linked("bascule", "u", "verre", "cmd") ? syn(L("Wire the Tilt's tipped output to the Glass.", "Relie le penché de la Bascule au Verre.")) :
                 !app.panel.has("evapLamp") ? pan(L("Add the evaporation light in the Panel.", "Ajoute le témoin d'évaporation dans le Panneau.")) : null; },
        check: (app, mem) => {
          const m = app.model, n = countTips(app, mem), g = m.first("verre"), f = m.first("feutre");
          const empty = g.p.P <= 0, dry = f.s.x < 0.5;
          if (!mem.drank) { if (n >= 1 && !empty) mem.drank = true;
            return { p: 0.1, done: false, status: empty ? L("Fill the glass again first (click it).", "Remplis d'abord le verre (clique dessus).") : L("Wait for a sip with the full glass…", "Attends une gorgée avec le verre plein…") }; }
          if (!empty) return { p: 0.35, done: false, status: L("Now click the glass, in the scale model on the right.", "Clique maintenant sur le verre, dans la Maquette à droite.") };
          mem.n = dry ? (mem.n || 0) + 1 : 0;
          return { p: dry ? 0.8 + 0.2 * mem.n / 100 : 0.4 + 0.4 * (1 - Math.min(1, (f.s.x - 0.5) / 0.5)), done: mem.n >= 100,
                   status: dry ? L("The felt is dry…", "Le feutre est sec…") : L("The felt dries… ", "Le feutre sèche… ") + Math.round(f.s.x * 100) + " %" };
        },
        takeaway: L("Without water, the felt dries, evaporation stops, and the bird comes to rest. It needed two things from outside: dry air, and water.",
                    "Sans eau, le feutre sèche, l'évaporation s'arrête et l'oiseau s'immobilise. Il lui fallait deux choses venues du dehors : de l'air sec, et de l'eau."),
        hood: L("Felt = <b>Storage</b> that empties itself (drying); Glass = <b>Source</b> commanded by the Tilt. A second loop, Tilt → Glass → Felt → Evaporation, keeps the first one supplied.",
                "Feutre = <b>Storage</b> qui se vide de lui-même (séchage) ; Verre = <b>Source</b> commandée par la Bascule. Une seconde boucle, Bascule → Verre → Feutre → Évaporation, entretient la première.") }
    ],

    final: {
      title: L("The bird that never stops drinking", "L'oiseau qui n'arrête pas de boire"),
      text: L("A store that fills slowly, a threshold that empties it all at once: the same shape is found in a dripping tap, a geyser, the siphon of an automatic flush tank, the cells that pace the heart, a firefly's flashes, the hiss of a pressure-cooker valve. And go back to the Thermostat: its curve was already a sawtooth.",
              "Une réserve qui se remplit lentement, un seuil qui la vide d'un coup : on retrouve la même forme dans un robinet qui goutte, un geyser, le siphon d'une chasse d'eau automatique, les cellules qui donnent le rythme du cœur, les éclairs d'une luciole, le sifflement de la soupape d'une cocotte-minute. Et retourne voir le Thermostat : sa courbe faisait déjà des dents de scie."),
      questions: [],
      hood: L("Negative loop + threshold with hysteresis + no resting point inside the band = <b>relaxation oscillator</b>. Regulation and oscillation are made of the same wires: what differs is whether the loop has a place to rest.",
              "Boucle négative + seuil avec hystérésis + aucun point de repos dans la bande = <b>oscillateur à relaxation</b>. Régulation et oscillation sont faites des mêmes fils : ce qui change, c'est que la boucle ait ou non un endroit où se poser.")
    },

    free: {
      text: L("Every block is unlocked. Try: what does a narrower hysteresis do to the rhythm? A wider neck? Can you find the dryness at which the felt dries faster than the bird drinks, so that it stops even with a full glass?",
              "Tous les blocs sont débloqués. Essaie : que fait une hystérésis plus étroite au rythme ? Un cou plus large ? Peux-tu trouver la sécheresse à laquelle le feutre sèche plus vite que l'oiseau ne boit, au point qu'il s'arrête même avec un verre plein ?"),
      hood: L("Generic blocks used: Storage, Source, Threshold, Sink. The same ones as in the Thermostat.",
              "Blocs génériques utilisés : Storage, Source, Threshold, Sink. Les mêmes que dans le Thermostat.")
    },

    // ---------------------------------------------------------------- scale model
    // The bird pivots on its stand; the liquid shows in the glass neck; the felt darkens
    // when wet; the beak dips into the glass when the bird tips.
    view: function (host, model, api) {
      const PX = 205, PY = 170;                       // pivot
      host.innerHTML = `
<svg viewBox="0 0 440 300" role="img" preserveAspectRatio="xMidYMid meet">
  <defs>
    <clipPath id="obClip"><rect x="0" y="0" width="440" height="300" rx="12"/></clipPath>
    <linearGradient id="obWall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e9e3d6"/><stop offset="1" stop-color="#d9d0bf"/></linearGradient>
    <linearGradient id="obTable" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#a0714a"/><stop offset="1" stop-color="#7a5235"/></linearGradient>
    <linearGradient id="obGlassTube" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#ffffff" stop-opacity=".25"/><stop offset=".35" stop-color="#ffffff" stop-opacity=".7"/><stop offset="1" stop-color="#ffffff" stop-opacity=".15"/></linearGradient>
    <radialGradient id="obBulb" cx=".35" cy=".35" r=".7"><stop offset="0" stop-color="#ffffff" stop-opacity=".75"/><stop offset="1" stop-color="#ffffff" stop-opacity=".12"/></radialGradient>
    <clipPath id="obBulbClip"><circle cx="0" cy="62" r="25"/></clipPath>
    <clipPath id="obHeadClip"><circle cx="0" cy="-100" r="16"/></clipPath>
  </defs>
  <g clip-path="url(#obClip)">
    <rect x="0" y="0" width="440" height="300" fill="url(#obWall)"/>
    <rect id="obHaze" x="0" y="0" width="440" height="300" fill="#9fb3c8" opacity="0"/>
    <g opacity=".5" stroke="#cfc5b1" stroke-width="1">${Array.from({ length: 9 }, (_, i) => `<line x1="${i * 55}" y1="0" x2="${i * 55}" y2="262"/>`).join("")}</g>
    <rect x="0" y="262" width="440" height="38" fill="url(#obTable)"/>
    <line x1="0" y1="262" x2="440" y2="262" stroke="#5e3e27" stroke-width="2"/>
    <g id="obBird">
      <g id="obStand">
        <path d="M${PX} ${PY} L${PX - 27} 262 M${PX} ${PY} L${PX + 27} 262" stroke="#7d8790" stroke-width="3.5" stroke-linecap="round"/>
        <rect x="${PX - 40}" y="258" width="80" height="6" rx="3" fill="#5f6870"/>
      </g>
      <g id="obBody">
        <path d="M-24 58 Q-54 46 -60 22 Q-44 54 -22 74 Z" fill="#3fa36b" stroke="#2c7a50" stroke-width="1"/>
        <path d="M-22 64 Q-48 60 -58 44 Q-40 68 -20 78 Z" fill="#e0b13a" stroke="#b58c22" stroke-width="1"/>
        <g clip-path="url(#obBulbClip)"><rect id="obBulbLiq" x="-26" y="40" width="52" height="50" fill="#d0342c"/></g>
        <circle cx="0" cy="62" r="25" fill="url(#obBulb)" stroke="#8aa0b0" stroke-width="1.5"/>
        <rect x="-4" y="-86" width="8" height="128" rx="3" fill="#ffffff" fill-opacity=".25" stroke="#8aa0b0" stroke-width="1.2"/>
        <rect id="obNeckLiq" x="-2" width="4" fill="#d0342c"/>
        <rect x="-4" y="-86" width="8" height="128" rx="3" fill="url(#obGlassTube)"/>
        <circle cx="0" cy="0" r="5" fill="#5f6870"/><rect x="-14" y="-2" width="28" height="4" rx="2" fill="#5f6870"/>
        <circle id="obFelt" cx="0" cy="-100" r="17" stroke="#6e6658" stroke-width="1.2"/>
        <g clip-path="url(#obHeadClip)"><rect id="obHeadLiq" x="-18" y="-84" width="36" height="0" fill="#d0342c" opacity=".55"/></g>
        <path d="M14 -104 L50 -97 L14 -91 Z" fill="#e8a33c" stroke="#b9791d" stroke-width="1"/>
        <circle cx="6" cy="-106" r="4.2" fill="#ffffff" stroke="#6e6658" stroke-width=".8"/><circle cx="7.2" cy="-106" r="2" fill="#1d1d1b"/>
        <rect x="-22" y="-119" width="44" height="5" rx="2" fill="#2b2b33"/>
        <rect x="-14" y="-136" width="28" height="18" rx="2" fill="#2b2b33"/>
        <rect x="-14" y="-123" width="28" height="4" fill="#c0392b"/>
      </g>
    </g>
    <g id="obVapour" stroke="#ffffff" stroke-width="2" fill="none" stroke-linecap="round">${[0, 1, 2].map(i => `<path class="obV" data-i="${i}"/>`).join("")}</g>
    <g id="obGlass" class="mq-click">
      <rect x="276" y="186" width="64" height="80" fill="transparent"/>
      <path id="obWater" d="M287.6 206 L328.4 206 L325.8 260 L290.2 260 Z" fill="#5fa8e0" opacity=".65"/>
      <path d="M286 196 L330 196 L326 262 L290 262 Z" fill="#dff0fb" fill-opacity=".25" stroke="#8aa0b0" stroke-width="1.5"/>
      <path d="M290 200 L292 256" stroke="#ffffff" stroke-opacity=".7" stroke-width="2" stroke-linecap="round"/>
    </g>
  </g>
  <text id="obEmpty" class="mq-note" x="220" y="150" text-anchor="middle"></text>
</svg>`;
      const $ = id => host.querySelector("#" + id);
      const mix = (a, b, t) => `rgb(${a.map((v, i) => Math.round(v + (b[i] - v) * t)).join(",")})`;
      let ang = -6, vel = 0, phase = 0, last = performance.now();

      $("obGlass").addEventListener("click", () => {
        const g = model.first("verre");
        if (!g) { api.toast(K.L("This glass is not wired to anything yet: place a Glass of water in the Synoptic.", "Ce verre n'est encore relié à rien : pose un Verre d'eau dans le Synoptique.")); return; }
        g.p.P = g.p.P > 0 ? 0 : model.skins.verre.params.P.v;
        api.log("glass", g.p.P > 0 ? "filled" : "emptied");
      });

      return {
        update(running) {
          const now = performance.now(), dtR = Math.min(0.05, (now - last) / 1000); last = now;
          const tete = model.first("tete"), evap = model.first("evap"), bas = model.first("bascule"),
                felt = model.first("feutre"), verre = model.first("verre");
          host.querySelector("svg").setAttribute("aria-label", K.L("Scale model: a drinking bird on its stand, in front of a glass of water", "Maquette : un oiseau buveur sur son support, devant un verre d'eau"));
          $("obEmpty").textContent = K.L("Empty scale model: place a Head in the Synoptic.", "Maquette vide : pose une Tête dans le Synoptique.");
          $("obEmpty").style.display = tete ? "none" : "";
          $("obBird").style.display = tete ? "" : "none";
          const dry = evap ? evap.p.P : 60;
          $("obHaze").setAttribute("opacity", (0.38 * (1 - dry / 100)).toFixed(2));
          const full = !verre || verre.p.P > 0;
          $("obWater").style.display = full ? "" : "none";
          if (!tete) { $("obVapour").style.display = "none"; return; }
          const f = Math.max(0, Math.min(1, tete.s.x / 100));
          // the bird leans as the head gets heavy; it tips over when the Tilt says so
          const isTipped = !!(bas && bas.s.x !== null && bas.s.u);
          const target = isTipped ? 84 : -6 + 22 * Math.min(1, f / 0.9);
          if (running || Math.abs(target - ang) > 0.2) {          // a damped spring: the bird swings a little
            const sub = 4;
            for (let i = 0; i < sub; i++) { const h = dtR / sub; vel += ((target - ang) * 60 - vel * 9) * h; ang += vel * h; }
          }
          $("obBody").setAttribute("transform", `translate(${PX} ${PY}) rotate(${ang.toFixed(2)})`);
          const top = 40 - 124 * f;
          $("obNeckLiq").setAttribute("y", top.toFixed(1)); $("obNeckLiq").setAttribute("height", (42 - top).toFixed(1));
          const bl = 1 - 0.8 * f;                                  // liquid left in the body
          $("obBulbLiq").setAttribute("y", (87 - 50 * bl).toFixed(1)); $("obBulbLiq").setAttribute("height", (50 * bl + 2).toFixed(1));
          const hl = Math.max(0, (f - 0.85) / 0.15);
          $("obHeadLiq").setAttribute("y", (-84 - 30 * hl).toFixed(1)); $("obHeadLiq").setAttribute("height", (30 * hl).toFixed(1));
          const wet = felt ? Math.max(0, Math.min(1, felt.s.x)) : 1;
          $("obFelt").setAttribute("fill", mix([236, 226, 205], [96, 128, 168], wet));
          // vapour rising from the head while it evaporates
          const evaporating = !!(evap && evap.s.u && evap.p.P > 0 && model.linked("evap", "flow", "tete", "in"));
          $("obVapour").style.display = evaporating ? "" : "none";
          if (evaporating) {
            if (running) phase = (phase + dtR * 0.5) % 1;
            const a = ang * Math.PI / 180, hx = PX + 100 * Math.sin(a), hy = PY - 100 * Math.cos(a);
            host.querySelectorAll(".obV").forEach(p => {
              const i = +p.dataset.i, k = (phase + i / 3) % 1, x = hx - 10 + i * 10, y = hy - 22 - 40 * k;
              p.setAttribute("d", `M${x.toFixed(1)} ${y.toFixed(1)} q4 -5 0 -10 t0 -10`);
              p.setAttribute("opacity", (Math.sin(Math.PI * k) * 0.9 * Math.min(1, 0.3 + dry / 80)).toFixed(2));
            });
          }
        }
      };
    }
  };
  };

  // Place on the map of scenarios: an articulation from the pivot (read by the home page, without the libraries)
  factory.meta = { icon: "bird",
    name: { en: "Drinking bird", fr: "Oiseau buveur" },
    what: { en: "A head, an evaporation, a tilt, a return.", fr: "Une tête, une évaporation, une bascule, un retour." },
    concept: { en: "A loop that never settles: it goes back and forth, forever.", fr: "Une boucle qui ne se pose jamais : elle va et vient, sans fin." },
    articulation: { from: "thermostat", dir: "lateral",
      carried: { en: "the sawtooth of the thermostat's curve", fr: "la dent de scie de la courbe du thermostat" },
      change: { en: "no more resting point", fr: "plus de point de repos" } } };
  (K.workshops = K.workshops || {}).oiseau = factory;
})(window.TSCGKit = window.TSCGKit || {});
