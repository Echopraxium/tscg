/* TSCG Kit — i18n.js
 * Language of the Kit: English by default, French on demand.
 * - K.lang          current language ("en" | "fr"), from ?lang=, then the saved choice
 * - K.setLang(l)    switch and remember (per browser)
 * - K.L(en, fr)     pick a string in the current language (used by workshops and views)
 * - K.t(key, ...)   shared interface strings below, with {0}, {1} placeholders
 * Author: Echopraxium with the collaboration of Claude AI
 */
(function (K) {
  "use strict";
  const KEY = "tscg-kit-lang";
  function initial() {
    try { const q = new URLSearchParams(location.search).get("lang"); if (q === "en" || q === "fr") return q; } catch (e) { /* no URL */ }
    try { const s = localStorage.getItem(KEY); if (s === "en" || s === "fr") return s; } catch (e) { /* storage blocked */ }
    return "en";
  }
  K.lang = initial();
  K.setLang = l => { K.lang = l; try { localStorage.setItem(KEY, l); } catch (e) { /* storage blocked */ } document.documentElement.lang = l; };
  K.L = (en, fr) => (K.lang === "fr" ? fr : en);

  // Theme: dark by default, light on demand; remembered per browser (same key as the home page)
  const THEME = "tscg-kit-theme";
  K.theme = (() => { try { const s = localStorage.getItem(THEME); if (s === "light" || s === "dark") return s; } catch (e) { /* storage blocked */ } return "dark"; })();
  K.applyTheme = () => { document.documentElement.dataset.theme = K.theme; };
  K.setTheme = th => { K.theme = th; try { localStorage.setItem(THEME, th); } catch (e) { /* storage blocked */ } K.applyTheme(); };
  K.applyTheme();

  const T = {
    en: {
      pieces: "Blocks", info: "information", locked: "locked",
      wire_help: "Drag a wire from an output (right side of a block) to an input (left side) of the same colour.",
      syn_aria: "Synoptic: pieces and wires",
      rej_self: "A block cannot be wired to itself.",
      rej_flux: "A flux (orange) only plugs into a flux input.",
      rej_info: "Information (blue) only plugs into an information input.",
      params_hint: "Click a block to adjust it. Press Delete to remove a block or a wire.",
      wire_selected: "Wire selected.", del_wire: "Delete the wire", del_piece: "Delete the block",
      d_level: "level", d_on: "on", d_off: "off", d_unlinked: "not linked", d_closed: "closed", d_open: "open",
      d_sat: "saturated · ", d_out: "output", d_notarget: "nothing to aim at", d_gap: "gap",
      pn_add: "Add an instrument:", pn_empty: "The panel is empty. Add an instrument with the buttons above.",
      pn_none: "none yet", pn_present: "Already on the panel", pn_need: "First place a {0} in the Synoptic",
      pn_addtip: "Add to the panel", pn_rotate: "Rotate", pn_remove: "Remove from the panel", pn_stretch: "Stretch",
      pn_absent: "{0} — {1} missing from the Synoptic", pn_auto: "auto", pn_on: "on", pn_off: "off",
      pn_nospace: "No room here: instruments cannot overlap.",
      pn_isauto: "This command is now driven by a wire in the Synoptic: the switch is automatic.",
      tu_step: "Step {0} / {1}", tu_bet: "Your bet: “{0}”.", tu_done: "Step completed.", tu_next: "Next step", tu_finish: "Finish",
      tu_free: "Free workshop", tu_back: "Back to the tutorial", tu_openfree: "Open the free workshop",
      tu_answer: "Answer the question above first.", tu_play: "Start the time with ▶ (at the top).",
      tu_running: "Running…", tu_runningof: "Running… {0} / {1}", tu_gopanel: "Go to the Panel →", tu_gosyn: "Go to the Synoptic →",
      tu_ph: "Your answer, in a few words…", tu_save: "Save my answers", tu_skip: "Skip",
      tu_thanks: "Thank you! Your answers will be in the “Export my session” file.",
      play: "▶ Start", pause: "⏸ Pause", play_tip: "Start / pause (space bar)", speed_tip: "Speed of time", reset_tip: "Reset the clock",
      hood: "Under the hood", hood_tip: "Show the generic names of the blocks",
      free: "Free mode", free_tip: "Unlock every block and leave the tutorial",
      export: "Export my session", export_tip: "Download the session log (for user tests)",
      tab_panel: "Panel", tab_syn: "Synoptic", maquette: "Scale model", curves: "Curves",
      pal_hint: "Hover or click a block to read what it does.", locked_info: "Unlocked later in the tutorial.",
      theme_tip: "Light / dark theme", info_box: "About this block",
      zoom_out: "Zoom out (Ctrl + wheel)", zoom_in: "Zoom in (Ctrl + wheel)", zoom_reset: "Back to 100 %", zoom_fit: "Show every block",
      speed_down: "Slower", speed_up: "Faster", speed_label: "Real time ↔ simulated time",
      home_tip: "All workshops", lang_btn: "FR", lang_tip: "Passer en français",
      g_threshold: "Threshold (hysteresis)", g_gradient: "Gradient (gap)", g_clock: "Clock (rhythm)"
    },
    fr: {
      pieces: "Blocs", info: "information", locked: "verrouillée",
      wire_help: "Tire un fil d'une sortie (à droite d'un bloc) vers une entrée (à gauche) de la même couleur.",
      syn_aria: "Synoptique : pièces et fils",
      rej_self: "Un bloc ne se branche pas sur lui-même.",
      rej_flux: "Un flux (orange) ne se branche que sur une entrée de flux.",
      rej_info: "Une information (bleu) ne se branche que sur une entrée d'information.",
      params_hint: "Clique un bloc pour le régler. Touche Suppr pour enlever un bloc ou un fil.",
      wire_selected: "Fil sélectionné.", del_wire: "Supprimer le fil", del_piece: "Supprimer le bloc",
      d_level: "niveau", d_on: "marche", d_off: "arrêt", d_unlinked: "non relié", d_closed: "fermé", d_open: "ouvert",
      d_sat: "saturé · ", d_out: "sortie", d_notarget: "rien à viser", d_gap: "écart",
      pn_add: "Ajouter un instrument :", pn_empty: "Le panneau est vide. Ajoute un instrument avec les boutons ci-dessus.",
      pn_none: "aucun pour l'instant", pn_present: "Déjà sur le panneau", pn_need: "Pose d'abord : {0} (dans le Synoptique)",
      pn_addtip: "Ajouter au panneau", pn_rotate: "Pivoter", pn_remove: "Retirer du panneau", pn_stretch: "Étirer",
      pn_absent: "{0} — {1} absent(e) du Synoptique", pn_auto: "auto", pn_on: "marche", pn_off: "arrêt",
      pn_nospace: "Pas de place ici : les instruments ne se chevauchent pas.",
      pn_isauto: "Cette commande est maintenant pilotée par un fil du Synoptique : l'interrupteur est en automatique.",
      tu_step: "Étape {0} / {1}", tu_bet: "Ton pari : « {0} ».", tu_done: "Étape réussie.", tu_next: "Étape suivante", tu_finish: "Terminer",
      tu_free: "Atelier libre", tu_back: "Reprendre le tutoriel", tu_openfree: "Ouvrir l'atelier libre",
      tu_answer: "Réponds d'abord à la question ci-dessus.", tu_play: "Lance le temps avec ▶ (en haut).",
      tu_running: "En cours…", tu_runningof: "En cours… {0} / {1}", tu_gopanel: "Aller au Panneau →", tu_gosyn: "Aller au Synoptique →",
      tu_ph: "Ta réponse, en quelques mots…", tu_save: "Enregistrer mes réponses", tu_skip: "Passer",
      tu_thanks: "Merci ! Tes réponses seront dans le fichier « Exporter ma session ».",
      play: "▶ Lancer", pause: "⏸ Pause", play_tip: "Lancer / mettre en pause (barre d'espace)", speed_tip: "Vitesse du temps", reset_tip: "Remettre l'horloge à zéro",
      hood: "Sous le capot", hood_tip: "Montrer les noms génériques des blocs",
      free: "Mode libre", free_tip: "Débloquer tous les blocs et quitter le tutoriel",
      export: "Exporter ma session", export_tip: "Télécharger le journal de la session (pour les tests)",
      tab_panel: "Panneau", tab_syn: "Synoptique", maquette: "Maquette", curves: "Courbes",
      pal_hint: "Survole ou clique un bloc pour savoir ce qu'il fait.", locked_info: "Débloqué plus tard dans le tutoriel.",
      theme_tip: "Thème clair / sombre", info_box: "À propos du bloc",
      zoom_out: "Dézoomer (Ctrl + molette)", zoom_in: "Zoomer (Ctrl + molette)", zoom_reset: "Revenir à 100 %", zoom_fit: "Afficher tous les blocs",
      speed_down: "Plus lent", speed_up: "Plus rapide", speed_label: "Temps réel ↔ temps simulé",
      home_tip: "Tous les ateliers", lang_btn: "EN", lang_tip: "Switch to English",
      g_threshold: "Threshold (hystérésis)", g_gradient: "Gradient (écart)", g_clock: "Clock (rythme)"
    }
  };
  K.t = function (key) {
    let s = (T[K.lang] && T[K.lang][key]) || T.en[key] || key;
    for (let i = 1; i < arguments.length; i++) s = s.replace("{" + (i - 1) + "}", arguments[i]);
    return s;
  };
  // generic piece names, shown "under the hood"
  K.generic = kind => ({ storage: "Storage", sink: "Sink", source: "Source", amplify: "Amplification", transducer: "Transducer",
                         threshold: K.t("g_threshold"), gradient: K.t("g_gradient"), clock: K.t("g_clock") }[kind] || kind);
})(window.TSCGKit = window.TSCGKit || {});
