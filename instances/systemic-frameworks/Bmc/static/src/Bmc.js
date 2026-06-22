/**
 * TSCG — Business Model Canvas Simulation
 * Author: Echopraxium with the collaboration of Claude AI
 * Date: 2026-06-20
 *
 * Architecture:
 *   - HTML/CSS: layout, sidebar, controls (native)
 *   - p5.js: 9-block BMC canvas + animated flux particles
 *   - Morphism: lerp-based interpolation between phase configs over MORPH_MS ms
 */

'use strict';

// ── Constants ──────────────────────────────────────────────────────────────
const MORPH_MS    = 3500;   // morphism duration in ms — slow enough to see block changes
const MAX_PARTS   = 280;    // particle pool size
const PHASE_NAMES  = ['Startup', 'Growth', 'Maturity', 'Decline', 'Transition'];

// ── Osterwalder taxonomy constants (moved from usecases.js) ──────────────────
const VALUE_LEVELS       = ['commodity','customization','excellence','innovation'];
const VALUE_LEVEL_LABELS = { commodity:'Commodity', customization:'Customization',
                              excellence:'Excellence', innovation:'Innovation' };
const VALUE_LEVEL_IDX    = { commodity:0, customization:1, excellence:2, innovation:3 };
const PRICE_LEVEL_ICONS  = { free:'🆓', economy:'💲', market:'💲💲', 'high-end':'💲💲💲' };
const REVENUE_ICONS      = { 'asset-sale':'📦', usage:'⏱', subscription:'🔄',
                              licensing:'©', brokerage:'🔀', advertising:'📣',
                              'cross-subsidy':'⚖' };
const SEGMENT_ICONS      = { mass:'👥', niche:'🎯', segmented:'◑',
                              diversified:'🔀', 'multi-sided':'⇄' };
const REL_ICONS          = { personal:'🤝', dedicated:'⭐', 'self-service':'🔧',
                              automated:'🤖', community:'🌐', 'co-creation':'🔨' };

// ── Generic TSCG block descriptions (tooltip fallback) ───────────────────────
const BLOCK_DESC = {
  KP:   'Network of suppliers & partners. Primary dim: S (Structure). m2:Structure, m2:Synergy.',
  KA:   'Most important actions to make BM work. Primary dim: F (Flow). m2:Flow, m2:Process.',
  KR:   'Most important assets required. Primary dim: S (Structure). m2:Structure, m2:Reservoir.',
  VP:   'Bundle of products/services creating value. Primary dim: A (Attractor). m2:Attractor, m2:Information.',
  CR:   'Relationships established with Customer Segments. Primary dim: D (Dynamics). m2:Dynamics, m2:Feedback.',
  CH:   'How the company reaches Customer Segments. Primary dim: F (Flow). m2:Flow, m2:Cascade.',
  CS:   'Distinct groups the business creates value for. Primary dim: It (Information). m2:Information, m2:Boundary.',
  'CS$':'All costs to operate the BM. Primary dim: F (Flow). m2:Equilibrium, m2:Polarity (vs VP).',
  RS:   'Cash generated from each Customer Segment. Primary dim: F (Flow). m2:Flow, m2:Amplification.',
};

// ── Generic phase block content (fallback when case has no blockContent) ─────
const GENERIC_BLOCKS = [
  // Phase 0 — Startup
  {
    KP:   { bullets:['Early suppliers','Angel investors','Founding team'], desc:'Early suppliers, incubator, angel investors, founding team.' },
    KA:   { bullets:['Build MVP','Customer discovery','Fundraising'], desc:'Product development, customer discovery, MVP iteration, fundraising.' },
    KR:   { bullets:['Founder expertise','Seed funding','Early prototype'], desc:'Founding team expertise, seed funding, early IP, brand embryo.' },
    VP:   { bullets:['Hypothesis only','Problem/solution?','Unvalidated'], desc:'Hypothesis: we solve [problem] for [segment]. Not yet validated.', osterwalder:{ valueLevel:'customization', priceLvl:'economy' } },
    CR:   { bullets:['Hands-on','Founders onboard','White-glove'], desc:'Founders personally onboard every customer.', osterwalder:{ relType:'personal' } },
    CH:   { bullets:['Direct outreach','Founder network','ProductHunt'], desc:'Direct outreach, founder network, early adopter communities.' },
    CS:   { bullets:['Niche early adopters','Innovators 1-3%','Narrow ICP'], desc:'Niche early adopters, innovators (1-3% of TAM), narrow ICP.', osterwalder:{ segmentType:'niche' } },
    'CS$':{ bullets:['High burn rate','Team salaries','Prototyping'], desc:'High burn rate. Fixed: team salaries. Variable: infra, prototyping.' },
    RS:   { bullets:['Near zero / seed','Pilot contracts','Grants'], desc:'Minimal or zero. Pilot contracts. Grants.', osterwalder:{ revenueType:'asset-sale', pricingMech:'fixed' } },
  },
  // Phase 1 — Growth
  {
    KP:   { bullets:['Channel partners','Key suppliers','Strategic investors'], desc:'Channel partners, resellers, key suppliers, strategic investors.' },
    KA:   { bullets:['Scale operations','Process build','Team growth'], desc:'Sales scaling, marketing automation, hiring, process standardization.' },
    KR:   { bullets:['Sales playbook','Customer data','Brand growing'], desc:'Growing team, sales playbook, customer data, brand recognition.' },
    VP:   { bullets:['PMF validated ✓','Customers pay','Clear differentiation'], desc:'PMF achieved. Customers pay. Clear differentiation vs. alternatives.', osterwalder:{ valueLevel:'excellence', priceLvl:'market' } },
    CR:   { bullets:['Self-service','CS team','Community building'], desc:'Transition to self-service onboarding, customer success team, community.', osterwalder:{ relType:'self-service' } },
    CH:   { bullets:['SEO + paid ads','Partner channels','Word of mouth'], desc:'SEO, content, paid acquisition (CAC < LTV), partner channels emerging.' },
    CS:   { bullets:['Early majority','Multiple segments','ICP refined'], desc:'Early majority entering. Multiple segments identified. ICP refined.', osterwalder:{ segmentType:'segmented' } },
    'CS$':{ bullets:['CAC dominant','Unit economics ↑','Burn ↑ (growth)'], desc:'Burn increasing. CAC dominant. Unit economics improving.' },
    RS:   { bullets:['MRR growing','Subscription / repeat','RS > COGS ✓'], desc:'Growing MRR. Subscription or repeat transactions. RS > COGS crossed.', osterwalder:{ revenueType:'subscription', pricingMech:'fixed' } },
  },
  // Phase 2 — Maturity
  {
    KP:   { bullets:['Ecosystem partners','OEM / white-label','Strategic alliances'], desc:'Ecosystem partners, OEM, white-label, strategic alliances.' },
    KA:   { bullets:['Optimize + retain','Upsell / expand','International'], desc:'Process optimization, customer retention, upsell/cross-sell, international.' },
    KR:   { bullets:['Brand (moat)','Proprietary data','Distribution'], desc:'Brand moat, customer relationships, data advantage, distribution network.' },
    VP:   { bullets:['Category leader','Defensible VP','Switching costs'], desc:'Category leader. VP well-defined and defensible. Switching costs established.', osterwalder:{ valueLevel:'excellence', priceLvl:'market' } },
    CR:   { bullets:['Automated low-touch','Account mgmt enterprise','Self-serve community'], desc:'Automated low-touch, account management for enterprise, self-serve community.', osterwalder:{ relType:'automated' } },
    CH:   { bullets:['Omni-channel','Partners 40%+','International CH'], desc:'Omni-channel. Partners 40%+. Direct 60%. International channels established.' },
    CS:   { bullets:['Mass market','Enterprise + SMB','International'], desc:'Mass market. Multiple segments. Enterprise + SMB + consumer. International.', osterwalder:{ segmentType:'mass' } },
    'CS$':{ bullets:['Optimized costs','Fixed costs spread','EBITDA positive'], desc:'Optimized. Fixed costs spread over large revenue base. EBITDA positive.' },
    RS:   { bullets:['Diversified RS','Recurring dominant','International'], desc:'Diversified: core + upsell + services + international. Recurring dominant.', osterwalder:{ revenueType:'subscription', pricingMech:'fixed' } },
  },
  // Phase 3 — Decline
  {
    KP:   { bullets:['Partners leaving ↓','Supplier leverage ↑','M&A targets'], desc:'Partners leaving for alternatives. Suppliers with more leverage.' },
    KA:   { bullets:['Cost-cutting','Restructuring','Defend core market'], desc:'Cost-cutting, restructuring, defending core market, M&A for growth.' },
    KR:   { bullets:['Eroding brand','Aging tech stack','Talent attrition'], desc:'Eroding brand, aging tech stack, shrinking customer base, talent attrition.' },
    VP:   { bullets:['Commoditized','Disrupted VP','Competitors cheaper'], desc:'Commoditized or disrupted. Competitors offer more for less.', osterwalder:{ valueLevel:'commodity', priceLvl:'economy' } },
    CR:   { bullets:['Automated only','Low investment','Churn > acquisition'], desc:'Automated (cost-driven). Low investment. Churn > acquisition.', osterwalder:{ relType:'automated' } },
    CH:   { bullets:['Existing only','No new investment','Channel decay'], desc:'Existing channels only. No investment in new channels.' },
    CS:   { bullets:['Shrinking CS','Late majority only','Competitors win'], desc:'Shrinking. Late majority / laggards only. Segments captured by competitors.', osterwalder:{ segmentType:'segmented' } },
    'CS$':{ bullets:['Rigid fixed costs','RS < C$ gap ↑','Margin compression'], desc:"Cost rigidity: fixed costs don't scale as fast as RS declines." },
    RS:   { bullets:['RS declining ↓','Price pressure','Churn accelerating'], desc:'Declining. Price pressure. Volume loss. Customer churn accelerating.', osterwalder:{ revenueType:'asset-sale', pricingMech:'dynamic' } },
  },
  // Phase 4 — Transition
  {
    KP:   { bullets:['New strategic KP','Pivot investors','Capability partners'], desc:'New strategic partners for the pivot. Investors supporting transformation.' },
    KA:   { bullets:['BM redesign ⟳','New capability build','Org restructuring'], desc:'Business model redesign, new capability building, organizational restructuring.' },
    KR:   { bullets:['New tech/IP ⟳','Brand repositioning','Transition assets'], desc:'New technology or capability being acquired/built. Brand repositioning.' },
    VP:   { bullets:['VP IN FLUX ⟳','Old VP weakening','New VP hypothesis'], desc:'IN FLUX: old VP weakening. New VP hypothesis being tested.', osterwalder:{ valueLevel:'innovation', priceLvl:'market' } },
    CR:   { bullets:['Old CS retained','New segment acquired','CR in transition ⟳'], desc:'Transitional: some old customers retained, new segment being acquired.', osterwalder:{ relType:'co-creation' } },
    CH:   { bullets:['Old CH phased out ⟳','New CH emerging','Dual-mode CH'], desc:'Old channels being phased out. New channels being established.' },
    CS:   { bullets:['CS segment shift ⟳','New B2B/B2C balance','CS in flux'], desc:'Segment shift: losing some, targeting new. Potentially new B2B/B2C balance.', osterwalder:{ segmentType:'diversified' } },
    'CS$':{ bullets:['Transition costs ↑ ⟳','Dual-mode ops','Restructuring charges'], desc:'Transition costs high. Restructuring charges. Dual-mode ops (old + new model).' },
    RS:   { bullets:['Revenue dip ⚠','New RS not at scale','Critical period'], desc:'Revenue dip during transition. New RS not yet at scale. Critical period.', osterwalder:{ revenueType:'cross-subsidy', pricingMech:'dynamic' } },
  },
];
const PH_COLORS    = ['#4A90E2', '#22C97A', '#F5A623', '#E64141', '#E8A020'];
const PHASE_TRANSITION_IDX = 4;  // index of Transition phase — keep only this one

// ASFID color palette
const COL = {
  A: '#ffb840', S: '#64c8ff', F: '#3dc896', It: '#c882ff', D: '#ff6464',
  bg: '#0d1117', panel: '#161b22', card: '#1c2130', border: '#30363d',
  text: '#e6edf3', muted: '#8b949e'
};

// ── BMC Block definitions (layout proportional coords 0-1) ────────────────
// Layout mirrors canonical BMC: left=infra, center=VP, right=customer
// Grid: 5 columns × 2 rows  (VP spans full height in col 2)
//   col0: KP        rows 0+1
//   col1: KA row0 / KR row1
//   col2: VP        rows 0+1  (center)
//   col3: CR row0 / CH row1
//   col4: CS        rows 0+1
// Bottom band: C$ (cols 0-1-2) | RS (cols 3-4)
const BLOCKS = [
  { id:'KP', label:'Key Partners',        abbr:'KP', dim:'S',  col:0, row:0, colSpan:1, rowSpan:2 },
  { id:'KA', label:'Key Activities',      abbr:'KA', dim:'F',  col:1, row:0, colSpan:1, rowSpan:1 },
  { id:'KR', label:'Key Resources',       abbr:'KR', dim:'S',  col:1, row:1, colSpan:1, rowSpan:1 },
  { id:'VP', label:'Value Proposition',   abbr:'VP', dim:'A',  col:2, row:0, colSpan:1, rowSpan:2 },
  { id:'CR', label:'Customer Relations',  abbr:'CR', dim:'D',  col:3, row:0, colSpan:1, rowSpan:1 },
  { id:'CH', label:'Channels',            abbr:'CH', dim:'F',  col:3, row:1, colSpan:1, rowSpan:1 },
  { id:'CS', label:'Customer Segments',   abbr:'CS', dim:'It', col:4, row:0, colSpan:1, rowSpan:2 },
  { id:'CS$', label:'Cost Structure',     abbr:'C$', dim:'F',  col:0, row:2, colSpan:3, rowSpan:1 },
  { id:'RS', label:'Revenue Streams',     abbr:'RS', dim:'F',  col:3, row:2, colSpan:2, rowSpan:1 },
];

// Tooltip descriptions per block
// → See usecases.js
// ── Flux paths (from → to, color dimension, base intensity key) ────────────
// Each path: list of block IDs forming the route
const FLUX_PATHS = [
  { id:'vp_ch',   from:'VP',  to:'CH',  via:[],       dim:'A',  key:'vp',    label:'VP → Channels' },
  { id:'ch_cs',   from:'CH',  to:'CS',  via:[],       dim:'F',  key:'vp',    label:'Channels → CS' },
  { id:'vp_cr',   from:'VP',  to:'CR',  via:[],       dim:'D',  key:'vp',    label:'VP → CR' },
  { id:'cs_rs',   from:'CS',  to:'RS',  via:[],       dim:'It', key:'conv',  label:'CS → RS (conversion)' },
  { id:'ka_vp',   from:'KA',  to:'VP',  via:[],       dim:'F',  key:'vp',    label:'KA → VP' },
  { id:'kr_ka',   from:'KR',  to:'KA',  via:[],       dim:'S',  key:'cost',  label:'KR → KA' },
  { id:'kp_ka',   from:'KP',  to:'KA',  via:[],       dim:'S',  key:'cost',  label:'KP → KA' },
  { id:'ka_cost', from:'KA',  to:'CS$', via:[],       dim:'F',  key:'cost',  label:'KA → Cost' },
  { id:'kr_cost', from:'KR',  to:'CS$', via:[],       dim:'F',  key:'cost',  label:'KR → Cost' },
  { id:'rs_sub',  from:'RS',  to:'CS',  via:[],       dim:'A',  key:'cross', label:'CrossSubsidy RS→CS' },
  { id:'net_fx',  from:'CS',  to:'VP',  via:[],       dim:'It', key:'net',   label:'Network Effect CS→VP' },
];

// → See usecases.js
// ── App State ──────────────────────────────────────────────────────────────
let caseIdx       = 0;
let fluxLayout    = 'experimental';  // always experimental flux
let pillarsVisible = false;          // pillars OFF by default
let selectedPillar    = null;
let transitionStartMs = null;
const TRANSITION_DURATION_MS = 5000;
let fluxVisible       = true;   // flux paths shown by default
let phaseIdx   = 0;
let playing    = false;
let speed      = 1;
let morphT     = 1.0;   // 0→1 during morph, 1 = stable
let morphStart = 0;
let morphFrom  = null;  // previous phase params
let morphTo    = null;  // target phase params

// Current interpolated params (updated during morphism)
let params = { vp:.7, conv:.5, cross:.3, net:.4, cost:.5 };

// Slider values (may diverge from case params when user adjusts manually)
let sliderOverride = false;

// Play clock
let playT       = 0;
let lastFrameMs = 0;
const PHASE_DURATION = 4000; // ms per phase before auto-advance

// ── Particle system ────────────────────────────────────────────────────────
class Particle {
  constructor(path, t) {
    this.path = path;
    this.t    = t;    // position along path 0→1
    this.speed = 0.004 + Math.random() * 0.003;
    this.alpha = 0;
    this.alive = true;
    this.size  = 2.5 + Math.random() * 2;
  }
  update(intensity) {
    this.t += this.speed * intensity * 1.2;
    if (this.t < 0.15) this.alpha = this.t / 0.15;
    else if (this.t > 0.85) this.alpha = (1 - this.t) / 0.15;
    else this.alpha = 1;
    if (this.t >= 1) this.alive = false;
  }
}

let particles  = [];
let blockRects = {};  // id → {x,y,w,h,cx,cy}
let spawnTimers = {};
FLUX_PATHS.forEach(fp => { spawnTimers[fp.id] = 0; });

// ── p5 sketch ──────────────────────────────────────────────────────────────
const sketch = (p) => {

  p.setup = () => {
    const cont = document.getElementById('p5-container');
    const cnv  = p.createCanvas(cont.offsetWidth, cont.offsetHeight);
    cnv.parent('p5-container');
    p.textFont('Arial');
    computeBlockRects(p.width, p.height);
    p.frameRate(60);
  };

  p.windowResized = () => {
    const cont = document.getElementById('p5-container');
    p.resizeCanvas(cont.offsetWidth, cont.offsetHeight);
    computeBlockRects(p.width, p.height);
  };

  p.draw = () => {
    p.background(13, 17, 23);
    const now = performance.now();
    const dt  = now - (p._lastDrawMs || now);
    p._lastDrawMs = now;

    updateMorph();
    updatePlay();
    checkTransitionTimer();
    checkDeclineCondition(dt);
    spawnParticles(p);
    updateParticles();
    if (fluxVisible) drawFluxPaths(p);
    drawBlocks(p);
    if (fluxVisible) drawParticles(p);
    if (pillarsVisible) drawPillars(p);  // on top — borders + labels visible
    updateLiveMetrics();
  };

  p.mouseMoved = () => {
    if (!showGaugeTooltip(p.mouseX, p.mouseY)) {
      showBlockTooltip(p.mouseX, p.mouseY);
    }
  };
  p.mouseOut    = () => hideTooltip();
  p.mousePressed = () => {
    if (pillarsVisible) handlePillarClick(p.mouseX, p.mouseY);
  };
};

// ── Layout computation ─────────────────────────────────────────────────────
function computeBlockRects(W, H) {
  // Margins
  const mx = 24, my = 20;
  const w  = W - mx * 2;
  const h  = H - my * 2;

  // 5 equal columns, 3 rows (row2 = bottom band = 22% height)
  const colW   = w / 5;
  const row0H  = h * 0.42;
  const row1H  = h * 0.36;
  const row2H  = h * 0.22;
  const rowY   = [my, my + row0H, my + row0H + row1H];
  const rowH   = [row0H, row1H, row2H];

  BLOCKS.forEach(b => {
    const x = mx + b.col * colW;
    const y = rowY[b.row];
    const bw = colW * b.colSpan - 4;
    const bh = (b.rowSpan === 2 ? row0H + row1H : rowH[b.row]) - 4;
    blockRects[b.id] = { x, y, w: bw, h: bh, cx: x + bw/2, cy: y + bh/2 };
  });
}

// ── Flux path geometry (straight lines between block centers with offset) ──
function pathCenter(id) {
  const r = blockRects[id];
  return r ? { x: r.cx, y: r.cy } : { x: 0, y: 0 };
}

function getPathPoints(fp) {
  const A = pathCenter(fp.from);
  const B = pathCenter(fp.to);
  // Slight curve via midpoint offset
  const mx = (A.x + B.x) / 2;
  const my = (A.y + B.y) / 2 + (fp.id === 'rs_sub' ? -30 : 0);
  return { A, M: { x: mx, y: my }, B };
}

function lerpPath(fp, t) {
  // Quadratic bezier: A → M → B
  const { A, M, B } = getPathPoints(fp);
  const x = (1-t)*(1-t)*A.x + 2*(1-t)*t*M.x + t*t*B.x;
  const y = (1-t)*(1-t)*A.y + 2*(1-t)*t*M.y + t*t*B.y;
  return { x, y };
}

// ── Particles ──────────────────────────────────────────────────────────────
function pathIntensity(fp) {
  const k = fp.key;
  let v = params[k] !== undefined ? params[k] : 0.5;

  // Amplify contrast: power curve makes low values much lower, high values stay high
  v = Math.pow(v, 0.7);

  // Transition phase: modulate emerging/fading flux intensities
  if (phaseIdx === PHASE_TRANSITION_IDX && morphT >= 1) {
    const ph = CASES[caseIdx].phases[PHASE_TRANSITION_IDX];
    if (ph) {
      if (ph.fadingFluxes   && ph.fadingFluxes.includes(fp.id))   v *= 0.15;
      if (ph.emergingFluxes && ph.emergingFluxes.includes(fp.id)) v *= 0.8;
    }
  }
  return Math.max(0, v);
}

// ── Transition helpers ─────────────────────────────────────────────────────
function isTransitionPhase() {
  return phaseIdx === PHASE_TRANSITION_IDX;
}

function currentTransitionData() {
  if (!isTransitionPhase()) return null;
  return CASES[caseIdx].phases[PHASE_TRANSITION_IDX] || null;
}

// Slow sine flicker for unstable blocks (0→1)
function flickerAlpha(p, speed) {
  return 0.5 + 0.5 * Math.sin(p.millis() * 0.001 * speed);
}

// ── Draw flux paths — dispatches to layout renderer ───────────────────────
function drawFluxPaths(p) {
  if (fluxLayout === 'experimental') {
    drawFluxPathsExperimental(p);
  } else {
    drawFluxPathsDefault(p);
  }
}

function lerpBezier(A, M, B, t) {
  return {
    x: (1-t)*(1-t)*A.x + 2*(1-t)*t*M.x + t*t*B.x,
    y: (1-t)*(1-t)*A.y + 2*(1-t)*t*M.y + t*t*B.y,
  };
}

// ── Draw blocks ────────────────────────────────────────────────────────────
function drawBlocks(p) {
  const td = currentTransitionData();

  BLOCKS.forEach(b => {
    const r   = blockRects[b.id];
    if (!r) return;
    const col = COL[b.dim] || '#ffffff';
    let pCol  = p.color(col);

    const intensity   = blockActivation(b);
    const isInstable  = td && td.instableBlocks && td.instableBlocks.includes(b.id) && morphT >= 1;

    // Transition: instable blocks flicker in amber
    if (isInstable) {
      const flicker = flickerAlpha(p, 2.5);  // stable sine, no random
      pCol = p.color('#E8A020');

      // Outer glow — amber pulse
      pCol.setAlpha(flicker * 60);
      p.fill(pCol);
      p.noStroke();
      p.rect(r.x - 6, r.y - 6, r.w + 12, r.h + 12, 12);

      // ── Oscillating border highlight for blocks changing during morphism ─────
    const isMorphing = morphT < 1 && morphFrom && morphTo;
    let borderOscillate = false;
    if (isMorphing && !isInstable) {
      const keyMap = { VP:'vp', CS:'conv', CH:'vp', CR:'vp',
                       RS:'conv', KA:'cost', KR:'cost', KP:'cost', 'CS$':'cost' };
      const k = keyMap[b.id];
      if (k) {
        const delta = Math.abs((morphTo[k] || 0) - (morphFrom[k] || 0));
        if (delta > 0.08) {  // only highlight blocks that change significantly
          borderOscillate = true;
          const osc = 0.5 + 0.5 * Math.sin(p.millis() * 0.006);  // ~1Hz oscillation
          const darkCol  = p.color(col); darkCol.setAlpha(80 + osc * 40);
          const lightCol = p.color(col); lightCol.setAlpha(140 + osc * 115);
          const borderCol = p.lerpColor(darkCol, lightCol, osc);
          p.stroke(borderCol);
          p.strokeWeight(2.5);
          p.noFill();
          p.rect(r.x, r.y, r.w, r.h, 6);
        }
      }
    }

    // Block body — dim between dark and amber-tinted
      p.fill(p.lerpColor(p.color(28, 33, 48), p.color(40, 35, 20), flicker * 0.6));
      pCol.setAlpha(100 + flicker * 155);
      p.stroke(pCol);
      p.strokeWeight(2);
      p.rect(r.x, r.y, r.w, r.h, 6);

      // "?" instability indicator top-right
      p.noStroke();
      p.fill(232, 160, 32, 180 + flicker * 75);
      p.textSize(10);
      p.textAlign(p.RIGHT, p.TOP);
      p.textStyle(p.BOLD);
      p.text('⟳', r.x + r.w - 5, r.y + 3);

    } else {
      // Normal rendering
      if (intensity > 0.1) {
        pCol.setAlpha(intensity * 40);
        p.fill(pCol);
        p.noStroke();
        p.rect(r.x - 4, r.y - 4, r.w + 8, r.h + 8, 10);
      }
      p.fill(28, 33, 48);
      pCol.setAlpha(180 + intensity * 75);
      p.stroke(pCol);
      p.strokeWeight(1.5);
      p.rect(r.x, r.y, r.w, r.h, 6);
    }

    // ── Layout constants ──────────────────────────────────────────────────
    const GAUGE_PAD   = 3;
    const GAUGE_MAX_W = 8;
    const GAUGE_MIN_W = 3;
    const DIM_SIZE    = Math.round(15 * 0.82);  // -18% → ~12px
    const DIM_H       = DIM_SIZE + 4;
    const GAUGE_TOP   = r.y + GAUGE_PAD + DIM_H;   // gauge starts below dim label
    const GAUGE_BOT   = r.y + r.h - GAUGE_PAD;
    const GAUGE_H     = GAUGE_BOT - GAUGE_TOP;      // shorter gauge, leaves room for label

    // ── Gauge A — ASFID activation ────────────────────────────────────────
    {
      const flow    = gaugeFlow(b);
      const absFlow = Math.abs(flow);
      const gW      = GAUGE_MIN_W + absFlow * (GAUGE_MAX_W - GAUGE_MIN_W);
      const gaugeCol = isInstable ? p.color('#E8A020') : p.color(col);
      const trackX   = r.x + GAUGE_PAD;

      // Dim label TOP-LEFT — bold + small colored background
      const dimCol = isInstable ? p.color('#E8A020') : p.color(col);

      // Background square behind dim label
      const bgCol = isInstable ? p.color('#E8A020') : p.color(col);
      bgCol.setAlpha(45);
      p.fill(bgCol);
      p.noStroke();
      p.rect(trackX + 2, r.y + GAUGE_PAD + 2, DIM_SIZE + 2, DIM_SIZE + 1, 2);

      // Dim label text — bold
      dimCol.setAlpha(210);
      p.fill(dimCol);
      p.textFont('Arial');
      p.textSize(DIM_SIZE);
      p.textStyle(p.BOLD);
      p.textAlign(p.LEFT, p.TOP);
      p.text(b.dim, trackX + 3, r.y + GAUGE_PAD + 3);
      p.textStyle(p.NORMAL);

      // Gauge starts BELOW both dim label AND V/R label (if VP or RS)
      const hasGaugeV2 = (b.id === 'VP' || b.id === 'RS');
      const labelRows  = hasGaugeV2 ? 2 : 1;   // 2 labels stacked for VP/RS
      const gTop = r.y + GAUGE_PAD + DIM_SIZE * labelRows + 4;
      const gBot = r.y + r.h - GAUGE_PAD;
      const gH   = Math.max(10, gBot - gTop);

      // Track
      p.fill(15, 18, 28, 180);
      p.rect(trackX, gTop, gW, gH, 2);
      // Fill (from bottom)
      const fillH = intensity * gH;
      const fillY = gTop + gH - fillH;
      gaugeCol.setAlpha(160 + absFlow * 80);
      p.fill(gaugeCol);
      p.rect(trackX, fillY, gW, fillH, 2);

      // ── Trend indicator at vertical midpoint of gauge ─────────────────────
      // ▲ filling  ▼ emptying  = stable (|flow| < 4%)
      const midY    = gTop + gH / 2;
      const midX    = trackX + gW / 2;
      const STABLE_THRESHOLD = 0.04;

      gaugeCol.setAlpha(230);
      p.fill(gaugeCol);
      p.noStroke();

      if (absFlow < STABLE_THRESHOLD) {
        // ── "=" sign — two small horizontal bars ──
        const bW = gW - 1;  // bar width fills gauge
        const bH = 1.5;
        const bX = trackX + 0.5;
        p.rect(bX, midY - 3, bW, bH, 1);
        p.rect(bX, midY + 1, bW, bH, 1);
      } else if (flow > 0) {
        // ── ▲ triangle pointing UP ──
        const tw = gW - 1;
        const th = Math.min(gH * 0.18, tw * 0.8);
        p.triangle(
          midX,          midY - th,      // apex top
          trackX + 0.5,  midY,           // bottom-left
          trackX + gW - 0.5, midY        // bottom-right
        );
      } else {
        // ── ▼ triangle pointing DOWN ──
        const tw = gW - 1;
        const th = Math.min(gH * 0.18, tw * 0.8);
        p.triangle(
          midX,          midY + th,      // apex bottom
          trackX + 0.5,  midY,           // top-left
          trackX + gW - 0.5, midY        // top-right
        );
      }

      // Flow arrow at fill boundary (kept for additional visual cue)
      if (absFlow > 0.05) {
        const arrowY = flow > 0 ? fillY - 1 : fillY + fillH + 1;
        const dir    = flow > 0 ? -1 : 1;
        gaugeCol.setAlpha(180);
        p.fill(gaugeCol);
        p.triangle(trackX + gW/2, arrowY + dir*4,
                   trackX,        arrowY - dir*2,
                   trackX + gW,   arrowY - dir*2);
      }

      // ── Gauge V (VP/RS only) — starts BELOW both dim + V/R labels ──────
      const hasGaugeV = (b.id === 'VP' || b.id === 'RS');
      if (hasGaugeV) {
        const vLevel   = getOsterwalderValue(b.id);
        const absVFlow = absFlow * 0.6;
        const gVW      = 5;
        const gVX      = trackX + gW + 2;
        const GOLD     = isInstable ? p.color('#E8A020') : p.color('#F5A623');

        // "V"/"R" label — pushed below dim label with extra gap
        const vLabelY = r.y + GAUGE_PAD + DIM_SIZE + 5;
        GOLD.setAlpha(190);
        p.fill(GOLD);
        p.textFont('Arial');
        p.textSize(9);
        p.textStyle(p.BOLD);
        p.textAlign(p.LEFT, p.TOP);
        p.text(b.id === 'VP' ? 'V' : 'R', gVX + 1, vLabelY);
        p.textStyle(p.NORMAL);

        // Gauge V track — starts below BOTH labels (dim + V/R)
        const gVTop = r.y + GAUGE_PAD + DIM_SIZE * 2 + 8;
        const gVH   = Math.max(10, r.y + r.h - GAUGE_PAD - gVTop);
        p.fill(15, 18, 28, 160);
        p.rect(gVX, gVTop, gVW, gVH, 2);
        const vFillH = vLevel * gVH;
        GOLD.setAlpha(140 + absVFlow * 80);
        p.fill(GOLD);
        p.rect(gVX, gVTop + gVH - vFillH, gVW, vFillH, 2);
      }
    }
    // ── End gauges ────────────────────────────────────────────────────────

    // ── Abbreviation — top of block, not centered ─────────────────────────
    const ABBR_SIZE  = b.id === 'CS$' ? 18 : 22;
    const LABEL_SIZE = Math.round(11 * 1.18);  // +18% → ~13px
    const CONTENT_X  = r.x + 18;   // left margin — closer to left edge
    const CONTENT_W  = r.w - 22;   // usable width

    const TITLE_TOP = r.y + 10;    // abbr starts near top

    const abbrevCol = isInstable ? p.color('#E8A020') : p.color(col);
    abbrevCol.setAlpha(220);
    p.fill(abbrevCol);
    p.textFont('Arial');
    p.textSize(ABBR_SIZE);
    p.textAlign(p.LEFT, p.TOP);
    p.textStyle(p.BOLD);
    p.text(b.abbr, CONTENT_X, TITLE_TOP);

    // Sub-title (Key Partners...) — directly under abbr, tight interligne
    const SUBTITLE_TOP = TITLE_TOP + ABBR_SIZE * 1.1;
    p.fill(190, 200, 215);
    p.textFont('Arial');
    p.textSize(LABEL_SIZE);
    p.textStyle(p.NORMAL);
    p.textAlign(p.LEFT, p.TOP);
    const maxChars = Math.max(8, Math.floor(CONTENT_W / (LABEL_SIZE * 0.6)));
    const lines = wrapText(b.label, maxChars);
    const lineH = LABEL_SIZE * 1.15;   // tight interligne
    lines.forEach((ln, i) => {
      p.text(ln, CONTENT_X, SUBTITLE_TOP + i * lineH);
    });

    // ── Bullets — 1.6× larger (8.5 → 13.5px) ────────────────────────────
    const bullets = getBlockBullets(b.id);
    // For bottom-band blocks (row 2: C$ and RS), start bullets closer to subtitle
    const isRow2    = (b.id === 'CS$' || b.id === 'RS');
    const CLIP_BOT  = r.y + r.h - 15;  // tighter clip — 15px from block bottom
    let bulletEndY  = SUBTITLE_TOP + lines.length * lineH + (isRow2 ? 2 : 8);
    if (bullets && bullets.length > 0) {
      const BULLET_SIZE  = Math.round(LABEL_SIZE * 1.04 * 0.88);  // ~10px
      const BULLET_LINEH = BULLET_SIZE * 1.2;  // tighter — was 1.45
      bulletEndY = SUBTITLE_TOP + lines.length * lineH + (isRow2 ? 2 : 8);
      const bulletColor = isInstable ? p.color('#E8A020') : p.color(col);
      const maxBulletW  = CONTENT_W - 10;

      bullets.slice(0, 3).forEach((bull, i) => {
        const y = bulletEndY + i * BULLET_LINEH;
        if (y > CLIP_BOT) return;
        // Dot
        bulletColor.setAlpha(160);
        p.fill(bulletColor);
        p.noStroke();
        p.circle(CONTENT_X + 4, y + BULLET_SIZE * 0.35, 4);
        // Text
        p.fill(185, 195, 210, 210);
        p.textFont('Arial');
        p.textSize(BULLET_SIZE);
        p.textStyle(p.NORMAL);
        p.textAlign(p.LEFT, p.TOP);
        let txt = bull;
        while (txt.length > 3 && p.textWidth(txt) > maxBulletW - 12) {
          txt = txt.slice(0, -2) + '…';
        }
        p.text(txt, CONTENT_X + 12, y);
      });
      bulletEndY += bullets.slice(0, 3).length * BULLET_LINEH;
      p.textAlign(p.CENTER, p.CENTER);
    }

    // ── Osterwalder badges ────────────────────────────────────────────────
    {
      const ost = getOsterwalderAttrs(b.id);
      if (ost) {
        const BADGE_SZ = Math.round(9 * 1.15);  // +15% → ~10px
        const BADGE_LH = BADGE_SZ + 5;
        let badgeY = bulletEndY + 6;
        p.textFont('Arial');
        p.textSize(BADGE_SZ);
        p.textStyle(p.NORMAL);
        p.textAlign(p.LEFT, p.CENTER);
        const GOLD = p.color('#F5A623');

        const badges = [];
        if (b.id === 'VP' && ost.valueLevel) {
          const vl    = ost.valueLevel;
          const vlIdx = VALUE_LEVEL_IDX[vl] || 0;
          const stars = '★'.repeat(vlIdx + 1) + '☆'.repeat(3 - vlIdx);
          badges.push({ txt: stars + ' ' + (VALUE_LEVEL_LABELS[vl] || vl), col: GOLD });
          if (ost.priceLvl) {
            badges.push({ txt: (PRICE_LEVEL_ICONS[ost.priceLvl] || '') + ' ' + ost.priceLvl,
                          col: p.color('#79c0ff') });
          }
        }
        if (b.id === 'RS' && ost.revenueType) {
          badges.push({ txt: (REVENUE_ICONS[ost.revenueType] || '💰') + ' ' + ost.revenueType,
                        col: p.color('#3dc896') });
        }
        if (b.id === 'CS' && ost.segmentType) {
          badges.push({ txt: (SEGMENT_ICONS[ost.segmentType] || '👥') + ' ' + ost.segmentType,
                        col: p.color('#c882ff') });
        }
        if (b.id === 'CR' && ost.relType) {
          badges.push({ txt: (REL_ICONS[ost.relType] || '↔') + ' ' + ost.relType,
                        col: p.color('#ff6464') });
        }

        badges.forEach(bd => {
          if (badgeY > CLIP_BOT) return;
          bd.col.setAlpha(30);
          p.fill(bd.col);
          p.noStroke();
          p.rect(CONTENT_X, badgeY - BADGE_SZ/2 - 1, CONTENT_W - 4, BADGE_SZ + 3, 3);
          bd.col.setAlpha(220);
          p.fill(bd.col);
          let txt = bd.txt;
          while (txt.length > 3 && p.textWidth(txt) > CONTENT_W - 8) txt = txt.slice(0, -1);
          p.text(txt, CONTENT_X + 3, badgeY);
          badgeY += BADGE_LH;
        });
        p.textAlign(p.CENTER, p.CENTER);
      }
    }
    // ── End Osterwalder badges ────────────────────────────────────────────

    // Instability label during Transition
    if (isInstable) {
      const sinceStable = morphT >= 1 ? (performance.now() - (morphStart + MORPH_MS)) : 0;
      if (morphT < 1 || sinceStable < 3000) {
        p.fill(232, 160, 32, 200);
        p.textFont('Arial');
        p.textSize(8);
        p.textAlign(p.CENTER, p.BOTTOM);
        p.text('⟳ en mutation', r.cx, r.y + r.h - 4);
      }
    }
  });

  // Transition phase: banner shown during morphism + 3s after, then gone
  if (isTransitionPhase() && td && td.transitionLabel) {
    // Banner visible during morph (morphT < 1) and for 3s after (bannerT)
    const sinceStable = morphT >= 1 ? (performance.now() - (morphStart + MORPH_MS)) : 0;
    const BANNER_HOLD = 3000; // ms to keep banner after morph ends
    if (morphT < 1 || sinceStable < BANNER_HOLD) {
      const bannerAlpha = morphT < 1
        ? Math.min(255, morphT * 600)
        : Math.max(0, 255 * (1 - sinceStable / BANNER_HOLD));
      const W = p.width;
      p.fill(20, 17, 10, bannerAlpha * 0.85);
      p.noStroke();
      p.rect(W/2 - 230, 6, 460, 24, 4);
      p.fill(232, 160, 32, bannerAlpha);
      p.textFont('Arial');
      p.textSize(11);
      p.textAlign(p.CENTER, p.CENTER);
      p.textStyle(p.BOLD);
      p.text('⟳ ' + td.transitionLabel, W/2, 18);
      p.textStyle(p.NORMAL);
    }
  }
}

function spawnParticles(p) {
  FLUX_PATHS.forEach(fp => {
    const intensity = pathIntensity(fp);
    if (intensity < 0.08) return;  // hard cutoff — no particles on very weak flows
    spawnTimers[fp.id] = (spawnTimers[fp.id] || 0) + 1;
    // Spawn rate inversely proportional to intensity — high intensity = frequent spawns
    // Range: intensity 0.1 → rate 50 frames; intensity 1.0 → rate 3 frames
    const rate = Math.max(3, Math.round(30 / (intensity * intensity)));
    if (spawnTimers[fp.id] >= rate && particles.length < MAX_PARTS) {
      particles.push(new Particle(fp, 0));
      spawnTimers[fp.id] = 0;
    }
  });
}

function updateParticles() {
  particles.forEach(pt => {
    const intensity = pathIntensity(pt.path);
    pt.update(intensity);
  });
  particles = particles.filter(pt => pt.alive);
}

// ── Tangent of quadratic Bézier at t (normalized direction vector) ─────────
function tangentPath(fp, t) {
  const { A, M, B } = getPathPoints(fp);
  // Derivative of quadratic Bézier: dB/dt = 2(1-t)(M-A) + 2t(B-M)
  const dx = 2*(1-t)*(M.x - A.x) + 2*t*(B.x - M.x);
  const dy = 2*(1-t)*(M.y - A.y) + 2*t*(B.y - M.y);
  return Math.atan2(dy, dx);  // angle in radians
}

// ── Tangent for straight line (experimental layout) ───────────────────────
function tangentLine(A, B) {
  return Math.atan2(B.y - A.y, B.x - A.x);
}

function drawParticles(p) {
  particles.forEach(pt => {
    const pos   = lerpPath(pt.path, pt.t);
    const angle = tangentPath(pt.path, pt.t);
    const intensity = pathIntensity(pt.path);

    // Chevron size: base 10px, scales with intensity and particle alpha
    const sz    = (8 + intensity * 6) * pt.alpha;
    const col   = p.color(COL[pt.path.dim] || '#ffffff');

    // Glow halo
    col.setAlpha(pt.alpha * 45);
    p.noStroke();
    p.fill(col);
    p.circle(pos.x, pos.y, sz * 2.2);

    // Chevron — drawn as two lines forming a "›" shape, rotated to tangent
    col.setAlpha(pt.alpha * 220);
    p.stroke(col);
    p.strokeWeight(1.8);
    p.noFill();

    p.push();
    p.translate(pos.x, pos.y);
    p.rotate(angle);
    // Chevron: two strokes meeting at tip (right), opening to left
    const h = sz * 0.45;  // half-height of chevron opening
    const w = sz * 0.55;  // depth of chevron
    p.line(-w, -h,  0, 0);  // top arm → tip
    p.line(-w,  h,  0, 0);  // bottom arm → tip
    p.pop();

    p.noStroke();
  });
}

// ── Pillar bounding box cache (populated in drawPillars) ──────────────────
let pillarBounds = {};  // id → {zx,zy,zw,zh,lx,bannerY,bannerH,bannerW}

function handlePillarClick(mx, my) {
  let hit = null;
  for (const [id, b] of Object.entries(pillarBounds)) {
    // Hit test on banner only (the clickable label area)
    if (mx >= b.lx - b.bannerW/2 && mx <= b.lx + b.bannerW/2 &&
        my >= b.bannerY && my <= b.bannerY + b.bannerH) {
      hit = id; break;
    }
  }
  // Toggle: click same pillar = deselect, click new = select
  selectedPillar = (hit === selectedPillar) ? null : hit;
}

// ── Osterwalder 4 Pillars ─────────────────────────────────────────────────
// Product | Customer Interface | Infrastructure Management | Financial Aspects
// Drawn as translucent zones BEHIND blocks, with label
function drawPillars(p) {
  if (!blockRects['KP']) return;

  const CRAN = 8;  // 1 cran = 8px vertical offset

  const PILLAR_DEFS = [
    {
      id: 'infrastructure',
      label: 'Infrastructure Management',
      color: [100, 160, 255],
      blocks: ['KP','KA','KR','CS$'],
      bottomOffset: CRAN * 1,   // 1 cran down — avoids overlap with Financial top
    },
    {
      id: 'product',
      label: 'Product',
      color: [255, 184, 64],
      blocks: ['VP'],
      bottomOffset: 0,
    },
    {
      id: 'customer',
      label: 'Customer Interface',
      color: [100, 220, 160],
      blocks: ['CS','CR','CH','RS'],
      bottomOffset: CRAN * 2,   // 2 crans down — visually distinct from Infrastructure
    },
    {
      id: 'financial',
      label: 'Financial Aspects',
      color: [200, 130, 255],
      blocks: ['CS$','RS'],
      bottomOffset: 0,
      rightOffset: CRAN * 1,   // 1 cran right — avoids overlap with Customer Interface
    },
  ];

  const PAD = 8;

  PILLAR_DEFS.forEach(pillar => {
    let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
    pillar.blocks.forEach(id => {
      const r = blockRects[id];
      if (!r) return;
      minX = Math.min(minX, r.x);
      minY = Math.min(minY, r.y);
      maxX = Math.max(maxX, r.x + r.w);
      maxY = Math.max(maxY, r.y + r.h);
    });
    if (minX === Infinity) return;

    const zx = minX - PAD;
    const zy = minY - PAD;
    const zw = maxX - minX + PAD * 2 + (pillar.rightOffset || 0);
    const zh = maxY - minY + PAD * 2 + (pillar.bottomOffset || 0);
    const [rv, gv, bv] = pillar.color;

    const isSelected = selectedPillar === pillar.id;
    const osc        = 0.5 + 0.5 * Math.sin(p.millis() * 0.006);  // ~1Hz

    // Translucent fill — brighter when selected
    p.noStroke();
    p.fill(rv, gv, bv, isSelected ? 45 : 28);
    p.rect(zx, zy, zw, zh, 10);

    // Dashed border — oscillating thickness when selected
    const borderAlpha = isSelected ? 180 + osc * 75 : 160;
    const borderW     = isSelected ? 1.5 + osc * 2.5 : 2;
    p.stroke(rv, gv, bv, borderAlpha);
    p.strokeWeight(borderW);
    p.noFill();
    const DASH = 10, GAP = 6;
    for (let x = zx; x < zx + zw; x += DASH + GAP)
      p.line(x, zy, Math.min(x + DASH, zx + zw), zy);
    for (let x = zx; x < zx + zw; x += DASH + GAP)
      p.line(x, zy + zh, Math.min(x + DASH, zx + zw), zy + zh);
    for (let y = zy; y < zy + zh; y += DASH + GAP)
      p.line(zx, y, zx, Math.min(y + DASH, zy + zh));
    for (let y = zy; y < zy + zh; y += DASH + GAP)
      p.line(zx + zw, y, zx + zw, Math.min(y + DASH, zy + zh));
    p.noStroke();

    // Label banner
    const LABEL_SZ    = 11;
    const lx          = zx + zw / 2;
    const isFinancial = pillar.id === 'financial';
    const bannerH     = LABEL_SZ + 6;
    const bannerW     = Math.min(zw - 8, pillar.label.length * LABEL_SZ * 0.62 + 20);
    const bannerY     = isFinancial
      ? zy + zh - bannerH * 0.25
      : zy      - bannerH * 0.75;
    const labelY      = bannerY + bannerH / 2;

    // Cache bounds for click detection
    pillarBounds[pillar.id] = { lx, bannerY, bannerH, bannerW };

    // Opaque banner background
    p.noStroke();
    p.fill(13, 17, 23);
    p.rect(lx - bannerW / 2, bannerY, bannerW, bannerH, 5);
    p.fill(rv, gv, bv, isSelected ? 180 : 110);
    p.rect(lx - bannerW / 2, bannerY, bannerW, bannerH, 5);

    // Luminous outline on banner when selected (2px, oscillating)
    if (isSelected) {
      const glowAlpha = 200 + osc * 55;
      p.stroke(rv, gv, bv, glowAlpha);
      p.strokeWeight(2);
      p.noFill();
      p.rect(lx - bannerW / 2, bannerY, bannerW, bannerH, 5);
      // Extra outer glow
      p.stroke(rv, gv, bv, glowAlpha * 0.4);
      p.strokeWeight(4);
      p.rect(lx - bannerW / 2 - 1, bannerY - 1, bannerW + 2, bannerH + 2, 6);
      p.noStroke();
    }

    // Label text
    p.fill(rv, gv, bv, 255);
    p.textFont('Arial');
    p.textSize(LABEL_SZ);
    p.textStyle(p.BOLD);
    p.textAlign(p.CENTER, p.CENTER);
    p.text(pillar.label, lx, labelY);
    p.textStyle(p.NORMAL);
    p.textAlign(p.CENTER, p.CENTER);
  });
}

// ── Layout DEFAULT — Bézier ghost lines ───────────────────────────────────
function drawFluxPathsDefault(p) {
  const td = currentTransitionData();
  FLUX_PATHS.forEach(fp => {
    const intensity = pathIntensity(fp);
    if (intensity < 0.02) return;
    const { A, M, B } = getPathPoints(fp);
    const col = p.color(COL[fp.dim] || '#ffffff');
    let baseAlpha = 30 + intensity * 40;
    let strokeW   = 1;
    let dashed    = false;
    if (td && morphT >= 1) {
      if (td.fadingFluxes && td.fadingFluxes.includes(fp.id)) {
        baseAlpha = 15 + flickerAlpha(p, 1.5) * 20; strokeW = 0.5; dashed = true;
      } else if (td.emergingFluxes && td.emergingFluxes.includes(fp.id)) {
        const amberCol = p.color('#E8A020');
        amberCol.setAlpha(20 + flickerAlpha(p, 2.2) * 50);
        p.stroke(amberCol); p.strokeWeight(1.5); p.noFill();
        p.beginShape(); p.vertex(A.x, A.y);
        p.quadraticVertex(M.x, M.y, B.x, B.y); p.endShape();
        return;
      }
    }
    col.setAlpha(baseAlpha);
    p.stroke(col); p.strokeWeight(strokeW); p.noFill();
    if (dashed) {
      for (let i = 0; i < 20; i += 2) {
        const p0 = lerpBezier(A, M, B, i/20);
        const p1 = lerpBezier(A, M, B, (i+0.8)/20);
        p.line(p0.x, p0.y, p1.x, p1.y);
      }
    } else {
      p.beginShape(); p.vertex(A.x, A.y);
      p.quadraticVertex(M.x, M.y, B.x, B.y); p.endShape();
    }
  });
}

// ── Layout EXPERIMENTAL — connectors on block edges + animated pipe ────────
// Connector anchors: each FLUX_PATH defines fromAnchor/toAnchor on block edges
const FLUX_ANCHORS = {
  vp_ch:   { from:'VP',  fromEdge:'right',  to:'CH',  toEdge:'left'   },
  ch_cs:   { from:'CH',  fromEdge:'right',  to:'CS',  toEdge:'left'   },
  vp_cr:   { from:'VP',  fromEdge:'right',  to:'CR',  toEdge:'left'   },
  cs_rs:   { from:'CS',  fromEdge:'bottom', to:'RS',  toEdge:'right'  },
  ka_vp:   { from:'KA',  fromEdge:'right',  to:'VP',  toEdge:'left'   },
  kr_ka:   { from:'KR',  fromEdge:'top',    to:'KA',  toEdge:'bottom' },
  kp_ka:   { from:'KP',  fromEdge:'right',  to:'KA',  toEdge:'left'   },
  ka_cost: { from:'KA',  fromEdge:'bottom', to:'CS$', toEdge:'top'    },
  kr_cost: { from:'KR',  fromEdge:'bottom', to:'CS$', toEdge:'top'    },
  rs_sub:  { from:'RS',  fromEdge:'top',    to:'CS',  toEdge:'bottom' },
  net_fx:  { from:'CS',  fromEdge:'left',   to:'VP',  toEdge:'right'  },
};

function edgePoint(blockId, edge) {
  const r = blockRects[blockId];
  if (!r) return { x:0, y:0 };
  switch (edge) {
    case 'left':   return { x: r.x,           y: r.cy };
    case 'right':  return { x: r.x + r.w,     y: r.cy };
    case 'top':    return { x: r.cx,           y: r.y  };
    case 'bottom': return { x: r.cx,           y: r.y + r.h };
    default:       return { x: r.cx,           y: r.cy };
  }
}

function drawFluxPathsExperimental(p) {
  const now = p.millis();
  FLUX_PATHS.forEach(fp => {
    const intensity = pathIntensity(fp);
    if (intensity < 0.05) return;
    const anchor = FLUX_ANCHORS[fp.id];
    if (!anchor) return;

    const A = edgePoint(anchor.from, anchor.fromEdge);
    const B = edgePoint(anchor.to,   anchor.toEdge);
    if (!A || !B) return;

    const col     = p.color(COL[fp.dim] || '#ffffff');
    const pipeW   = 3 + intensity * 8;   // pipe width 3→11px
    const flowSpd = intensity * 0.4;     // animation speed

    // ── Pipe track (background) ───────────────────────────────────────────
    col.setAlpha(30);
    p.stroke(col); p.strokeWeight(pipeW); p.strokeCap(p.ROUND);
    p.noFill();
    p.line(A.x, A.y, B.x, B.y);

    // ── Animated chevron sliding along pipe ──────────────────────────────
    const t    = ((now * flowSpd * 0.001) % 1.0);
    const SEG  = 0.35;
    const chevX = A.x + (B.x - A.x) * (t + SEG * 0.5);
    const chevY = A.y + (B.y - A.y) * (t + SEG * 0.5);
    const angle = tangentLine(A, B);
    const sz    = 5 + intensity * 5;

    col.setAlpha(180 + intensity * 70);
    p.stroke(col);
    p.strokeWeight(2);
    p.noFill();
    p.push();
    p.translate(chevX, chevY);
    p.rotate(angle);
    p.line(-sz * 0.5, -sz * 0.45,  0, 0);
    p.line(-sz * 0.5,  sz * 0.45,  0, 0);
    p.pop();
    p.noStroke();

    // ── Connector circles on block edges ──────────────────────────────────
    col.setAlpha(200); p.fill(col);
    p.circle(A.x, A.y, 9);
    p.fill(28, 33, 48);
    p.circle(A.x, A.y, 5);
    col.setAlpha(200); p.fill(col);
    p.circle(B.x, B.y, 9);
    col.setAlpha(160 + intensity * 60); p.fill(col);
    p.circle(B.x, B.y, 5);
  });
  p.strokeCap(p.SQUARE);  // restore default
}

// ── Gauge flow (débit) — signed derivative of block level ─────────────────
// Computed from morphism progress: how fast is this block's param changing?
// Returns value in [-1, +1] : positive = filling, negative = emptying
let _prevParams = null;
let _prevParamsFrame = 0;

function gaugeFlow(b) {
  // During morphism: compute derivative from morphFrom → morphTo
  if (morphT >= 1 || !morphFrom || !morphTo) {
    // Stable phase — no flow (or tiny noise for "alive" feeling)
    return 0;
  }

  // Map block to its primary param key
  const keyMap = {
    VP: 'vp',  CS: 'conv', CH: 'vp',  CR: 'vp',
    RS: 'conv', KA: 'cost', KR: 'cost', KP: 'cost', 'CS$': 'cost',
  };
  const k = keyMap[b.id];
  if (!k) return 0;

  const from = Math.pow(morphFrom[k] || 0, 0.6);
  const to   = Math.pow(morphTo[k]   || 0, 0.6);
  const delta = to - from;  // signed: + = filling, - = emptying

  // Scale by morphism speed (faster morph = higher flow)
  const speed = Math.min(1, Math.abs(delta) * 2.5);
  return Math.sign(delta) * speed;
}

// ── Get Osterwalder VALUE LEVEL as 0→1 (for Gauge V) ─────────────────────
function getOsterwalderValue(blockId) {
  const ost = getOsterwalderAttrs(blockId);
  if (!ost) return 0.5;
  if (blockId === 'VP' && ost.valueLevel) {
    return (VALUE_LEVEL_IDX[ost.valueLevel] || 0) / 3;
  }
  if (blockId === 'RS' && ost.revenueType) {
    // Revenue complexity as value: asset-sale=0.25, usage=0.5, subscription=0.6,
    // advertising=0.7, brokerage=0.75, licensing=0.8, cross-subsidy=1.0
    const map = { 'asset-sale':0.25,'usage':0.5,'subscription':0.6,
                  'advertising':0.7,'brokerage':0.75,'licensing':0.8,'cross-subsidy':1.0 };
    return map[ost.revenueType] || 0.5;
  }
  return 0.5;
}

// ── Get Osterwalder attributes for a block in current case+phase ──────────
function getOsterwalderAttrs(blockId) {
  const cs  = CASES[caseIdx];
  const ph  = cs ? cs.phases[phaseIdx] : null;
  const bc  = ph && ph.blockContent ? ph.blockContent[blockId] : null;
  if (bc && bc.osterwalder) return bc.osterwalder;
  const gen = GENERIC_BLOCKS[phaseIdx];
  if (gen && gen[blockId] && gen[blockId].osterwalder) return gen[blockId].osterwalder;
  return null;
}

// ── Get bullets for a block in current case+phase ─────────────────────────
// ── Smart bullet generator ─────────────────────────────────────────────────
// Priority: 1) case blockContent  2) generated from phase data  3) generic fallback
function getBlockBullets(blockId) {
  const cs = CASES[caseIdx];
  const ph = cs ? cs.phases[phaseIdx] : null;

  // 1. Case-specific blockContent (highest priority)
  if (ph && ph.blockContent && ph.blockContent[blockId] &&
      Array.isArray(ph.blockContent[blockId].bullets) &&
      ph.blockContent[blockId].bullets.length > 0) {
    return ph.blockContent[blockId].bullets;
  }

  // 2. Generate contextual bullets from phase narrative/driver + case pattern
  if (ph && cs) {
    const generated = generateBullets(blockId, cs, ph, phaseIdx);
    if (generated && generated.length > 0) return generated;
  }

  // 3. Generic phase fallback
  const generic = GENERIC_BLOCKS[phaseIdx];
  if (generic && generic[blockId] && generic[blockId].bullets) {
    return generic[blockId].bullets;
  }
  return [];
}

// ── Generate contextual bullets from case+phase data ──────────────────────
// Extracts case-specific keywords from narrative+driver per block
function generateBullets(blockId, cs, ph, phIdx) {
  const driver = ph.driver || '';
  const narr   = ph.narrative || '';
  const short  = cs.short || cs.name;
  const isT    = phIdx === PHASE_TRANSITION_IDX;
  const phName = PHASE_NAMES[phIdx] || '';

  const figures = () => (driver+' '+narr).match(/[\$€£][\d.,]+[BMK]?[^\s,.(]*/gi) || [];
  const nums    = () => (driver+' '+narr).match(/[\d.]+[BMK]\+?(?:\s*\w+)?/gi) || [];
  const extract = (patterns, src) => {
    src = src || driver+' '+narr;
    for (const re of patterns) { const m = src.match(re); if (m) return m[0].trim().substring(0,26); }
    return null;
  };

  switch (blockId) {
    case 'VP': {
      const vpText  = narr.includes('—') ? narr.split('—').slice(1).join('—').replace(/[\'"«»]/g,'').trim() : narr.replace(/[\'"«»]/g,'').trim();
      const phLabel = ['Hypothesis','PMF validated ✓','Category leader','VP eroded ↓','VP in flux ⟳'][phIdx] || phName;
      const metric  = figures()[0] || (nums()[0]||'').substring(0,22) || '';
      return [phLabel, vpText.substring(0,26), metric || (isT?'≥3 blocks changing':short)].filter(s=>s&&s.trim().length>1).slice(0,3);
    }
    case 'RS': {
      const figs   = figures().slice(0,2);
      const rsType = extract([/subscription|pay-per|usage|brokerage|advertising|licensing|cross-subsidy|freemium/i]);
      const rsPhase= ['Near zero / seed','RS growing ↑','Diversified RS','RS declining ↓','RS in transition ⟳'][phIdx];
      return [rsPhase, figs[0]||rsType||driver.substring(0,22), figs[1]||short].filter(s=>s&&s.trim().length>1).slice(0,3);
    }
    case 'CS': {
      const csNums = nums().slice(0,2);
      const csType = extract([/multi-sided|platform|two-sided|niche|mass market|segmented|diversified/i]);
      const csPhase= ['Niche early adopters','Early majority','Mass market','CS shrinking ↓','CS shift ⟳'][phIdx];
      return [csPhase, csNums[0]||csType||driver.substring(0,22), csNums[1]||short+' — '+phName].filter(s=>s&&s.trim().length>1).slice(0,3);
    }
    case 'KA': {
      const actions = (driver+' '+narr).match(/\b(?:production|delivery|platform|management|development|analytics|algorithm|content|logistics|engineering|operations|monitoring|optimization)\b/gi)||[];
      const base = [['Build + discover','MVP iteration','Fundraising'],['Scale operations','Process build','Team growth'],['Optimize + retain','Upsell / expand','International'],['Cost-cutting','Restructuring','Defend market'],['BM redesign ⟳','New capability','Org restructuring']][phIdx]||['Operations','Management','Delivery'];
      if (actions[0]) base[0]=actions[0].substring(0,22);
      if (actions[1]) base[1]=actions[1].substring(0,22);
      return base.slice(0,3);
    }
    case 'KR': {
      const res = (driver+' '+narr).match(/\b(?:algorithm|brand|patent|data|platform|network|tech|IP|infrastructure|talent|license|content|community|supercharger|fleet)\b/gi)||[];
      const base = [['Founder + seed','Early prototype','Tech platform'],['Sales playbook','Customer data','Brand growing'],['Brand (moat)','Proprietary data','Distribution'],['Eroding brand','Aging tech stack','Talent risk'],['New tech/IP ⟳','Brand repositioning','Transition assets']][phIdx]||['Resources','Assets','IP'];
      if (res[0]) base[0]=res[0].substring(0,22);
      if (res[1]) base[1]=res[1].substring(0,22);
      return base.slice(0,3);
    }
    case 'KP': {
      const kpNames = (driver+' '+narr).match(/\b(?:AWS|USPS|Stripe|PayPal|Panasonic|NVIDIA|Anthropic|Universal|Sony|Warner|Apple|Google|Intel|AMD|Tesla|BYD|Microsoft|Salesforce|WWE|NFL|FIFA)\b/gi)||[];
      const base = [['Early suppliers','Angel investors','Advisors / incubator'],['Channel partners','Key suppliers','Strategic investors'],['Ecosystem partners','OEM / white-label','Strategic alliances'],['Partners leaving ↓','Supplier leverage ↑','M&A targets'],['New strategic KP ⟳','Pivot investors','Capability partners']][phIdx]||['Partners','Suppliers','Investors'];
      if (kpNames[0]) base[0]=kpNames[0].substring(0,22);
      if (kpNames[1]) base[1]=kpNames[1].substring(0,22);
      return base.slice(0,3);
    }
    case 'CR': {
      const relType = extract([/personal|dedicated|self-service|automated|community|co-creation/i]);
      const base = [['Hands-on','Founders respond','White-glove'],['Self-service','CS team','Community building'],['Automated low-touch','Account mgmt','Self-serve community'],['Automated only','Low investment','Churn > acquisition'],['CR in transition ⟳','Old CS retained','New segment acquired']][phIdx]||['Relationship','Service','Support'];
      if (relType) base[0]=relType.substring(0,22);
      return base.slice(0,3);
    }
    case 'CH': {
      const channels = (driver+' '+narr).match(/\b(?:app|web|mobile|direct|online|store|marketplace|API|partner|distributor|retail|digital|console|website)\b/gi)||[];
      const base = [['Direct outreach','Founder network','ProductHunt / press'],['SEO + paid ads','Partner channels','Word of mouth'],['Omni-channel','Partners 40%+','International CH'],['Existing only','No new investment','Channel decay'],['Old CH phased out ⟳','New CH emerging','Dual-mode CH']][phIdx]||['Channels','Distribution','Access'];
      if (channels[0]) base[0]=channels[0].substring(0,22);
      if (channels[1]) base[1]=channels[1].substring(0,22);
      return base.slice(0,3);
    }
    case 'CS$': {
      const cFigs  = figures().slice(0,2);
      const cType  = extract([/fixed|variable|capex|opex|burn rate|margin|EBITDA/i]);
      const base = [['High burn rate','Team salaries','Infrastructure'],['CAC dominant','Unit economics ↑','Burn ↑ (growth)'],['Optimized costs','Fixed costs spread','EBITDA positive'],['Rigid fixed costs','RS < C$ gap ↑','Margin compression'],['Transition costs ↑ ⟳','Dual-mode ops','Restructuring']][phIdx]||['Costs','Structure','Expenses'];
      if (cFigs[0]) base[1]=cFigs[0].substring(0,22);
      if (cType)    base[0]=cType.substring(0,22);
      return base.slice(0,3);
    }
    default: return [];
  }
}

function blockActivation(b) {
  // Map block to its primary param, amplified for visual contrast
  const raw = {
    VP:   params.vp,
    CS:   params.conv,
    CH:   params.vp * 0.9,
    CR:   params.vp * 0.85,
    RS:   params.conv,
    KA:   params.cost * 0.9,
    KR:   params.cost * 0.85,
    KP:   params.cost * 0.75,
    'CS$': params.cost,
  };
  // Amplify contrast: remap [0, 1] → exaggerated visual range
  const v = raw[b.id] !== undefined ? raw[b.id] : 0.4;
  // Apply a power curve to exaggerate differences (low=darker, high=brighter)
  return Math.min(1, Math.pow(v, 0.6));
}

function wrapText(text, maxChars) {
  const words = text.split(' ');
  const lines = [];
  let cur = '';
  words.forEach(w => {
    if ((cur + ' ' + w).trim().length > maxChars && cur) {
      lines.push(cur.trim());
      cur = w;
    } else {
      cur = (cur + ' ' + w).trim();
    }
  });
  if (cur) lines.push(cur.trim());
  return lines;
}

// ── Morphism ───────────────────────────────────────────────────────────────
function startMorph(fromParams, toParams) {
  morphFrom  = { ...fromParams };
  morphTo    = { ...toParams };
  morphT     = 0;
  morphStart = performance.now();
}

function updateMorph() {
  const wasMorphing = morphT < 1;
  if (morphT >= 1) return;
  const elapsed = performance.now() - morphStart;
  morphT = Math.min(1, elapsed / MORPH_MS);
  const ease = easeInOut(morphT);

  ['vp','conv','cross','net','cost'].forEach(k => {
    params[k] = morphFrom[k] + (morphTo[k] - morphFrom[k]) * ease;
  });

  if (!sliderOverride) {
    document.getElementById('sl-vp').value    = params.vp;
    document.getElementById('sl-conv').value  = params.conv;
    document.getElementById('sl-cross').value = params.cross;
    document.getElementById('sl-net').value   = params.net;
    document.getElementById('sl-cost').value  = params.cost;
  }

  // Start transition countdown as soon as morphism completes
  if (wasMorphing && morphT >= 1 && phaseIdx === PHASE_TRANSITION_IDX) {
    transitionStartMs = performance.now();
  }

  // Update morph bar
  const morphFill  = document.getElementById('morph-bar-fill');
  const morphLabel = document.getElementById('morph-label');
  if (morphFill)  morphFill.style.width = (morphT * 100) + '%';
  if (morphLabel) morphLabel.textContent = morphT < 1 ? 'Morphing…' : '—';
}

function easeInOut(t) {
  return t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
}

// ── Play / phase advance ───────────────────────────────────────────────────
function updatePlay() {
  if (!playing) return;
  const now  = performance.now();
  const dt   = now - lastFrameMs;
  lastFrameMs = now;
  if (dt > 200) return;

  playT += dt * speed;
  const dur = PHASE_DURATION;
  const progress = playT / (dur * PHASE_NAMES.length);
  document.getElementById('progress-fill').style.width = (progress * 100) + '%';

  const newPhase = Math.min(PHASE_NAMES.length - 1, Math.floor(playT / dur));
  if (newPhase !== phaseIdx) {
    // Skip Decline (idx 3) in sequential play — Decline is cursor-induced only
    if (newPhase === 3) {
      playT = 4 * dur;  // skip straight to Transition
      jumpPhase(4);
    } else {
      jumpPhase(newPhase);
    }
  }

  // Auto-stop at end of sequence (after Transition)
  if (playT >= dur * PHASE_NAMES.length) {
    playing = false;
    document.getElementById('btn-play').textContent = '▶ Play';
    document.getElementById('btn-play').classList.remove('active');
    document.getElementById('status-dot').className = 'status-dot paused';
    document.getElementById('status-label').textContent = 'Done';
  }
}

// ── Transition combolist ───────────────────────────────────────────────────
function updateTransitionSelect() {
  const sel = document.getElementById('transition-select');
  if (!sel) return;
  sel.innerHTML = '<option value="">— None —</option>';

  const cs = CASES[caseIdx];
  if (!cs || !cs.transitions || cs.transitions.length === 0) return;

  cs.transitions.forEach((t, i) => {
    const opt = document.createElement('option');
    opt.value = i;
    const icon = t.outcome === 'Success'     ? '✅'
               : t.outcome === 'Failure'     ? '❌'
               : '🔄';
    opt.textContent = icon + ' T' + (t.index + 1) + ' — ' + t.label;
    opt.title       = t.fromPhase + ' → ' + t.toPhase;
    sel.appendChild(opt);
  });
}

window.applyTransition = function(val) {
  if (val === '' || val === null) return;
  const cs = CASES[caseIdx];
  if (!cs) return;
  const t = cs.transitions[parseInt(val)];
  if (!t) return;

  // Ensure a Transition phase exists at index 4 (create synthetically if missing)
  if (!cs.phases[PHASE_TRANSITION_IDX]) {
    cs.phases[PHASE_TRANSITION_IDX] = {
      vp: t.vp ?? 0.45, conv: t.conv ?? 0.40,
      cross: t.cross ?? 0.20, net: t.net ?? 0.30, cost: t.cost ?? 0.65,
      narrative: 'Transition — ' + (t.label || ''),
      driver:    t.fromPhase + ' → ' + t.toPhase,
      blockContent: t.blockContent || null,
      transitionLabel:  t.label,
      instableBlocks:   t.instableBlocks  || [],
      emergingFluxes:   t.emergingFluxes  || [],
      fadingFluxes:     t.fadingFluxes    || [],
      _transitionOutcome: t.outcome,
      _transitionFrom:    t.fromPhase,
      _transitionTo:      t.toPhase,
    };
  } else {
    // Update existing Transition phase with this transition's data
    const transPhase = cs.phases[PHASE_TRANSITION_IDX];
    if (t.vp !== null && t.vp !== undefined) {
      transPhase.vp    = t.vp;
      transPhase.conv  = t.conv;
      transPhase.cross = t.cross;
      transPhase.net   = t.net;
      transPhase.cost  = t.cost;
    }
    transPhase.narrative         = 'Transition — ' + (t.label || '');
    transPhase.driver            = t.fromPhase + ' → ' + t.toPhase;
    transPhase.transitionLabel   = t.label;
    transPhase.instableBlocks    = t.instableBlocks  || [];
    transPhase.emergingFluxes    = t.emergingFluxes  || [];
    transPhase.fadingFluxes      = t.fadingFluxes    || [];
    transPhase.blockContent      = t.blockContent    || transPhase.blockContent || null;
    transPhase._transitionOutcome = t.outcome;
    transPhase._transitionFrom    = t.fromPhase;
    transPhase._transitionTo      = t.toPhase;
  }

  // Jump to the Transition phase
  jumpPhase(PHASE_TRANSITION_IDX);
};

// Sync sliders to current params (after applyTransition)
function syncSliders() {
  const s = {vp:'sl-vp', conv:'sl-conv', cross:'sl-cross', net:'sl-net', cost:'sl-cost'};
  Object.entries(s).forEach(([k, id]) => {
    const el = document.getElementById(id);
    if (el) el.value = params[k];
  });
}

// ── Post-Transition routing ────────────────────────────────────────────────
// Called when user clicks "Exit Transition" or outcome button
function exitTransition() {
  const cs = CASES[caseIdx];
  if (!cs) return;
  const transPhase = cs.phases[PHASE_TRANSITION_IDX];
  const outcome    = transPhase?._transitionOutcome || 'Success';
  const toPhase    = transPhase?._transitionTo      || '';

  // Map toPhase name → phase index
  const nameToIdx = { Startup:0, Growth:1, Maturity:2, Decline:3, Transition:4 };
  let targetPhaseIdx;
  if (outcome === 'Success') {
    // Find the named target phase, default to Growth
    targetPhaseIdx = nameToIdx[toPhase] ?? 1;
    if (targetPhaseIdx === PHASE_TRANSITION_IDX) targetPhaseIdx = 1; // avoid loop
  } else if (outcome === 'Failure') {
    targetPhaseIdx = 3;  // Decline
  } else {
    targetPhaseIdx = nameToIdx[toPhase] ?? 2;  // InProgress → Maturity or named
  }

  // Clamp to available phases
  targetPhaseIdx = Math.max(0, Math.min(cs.phases.length - 2, targetPhaseIdx));

  jumpPhase(targetPhaseIdx);
  playT = targetPhaseIdx * PHASE_DURATION;

  // Reset combolist
  const sel = document.getElementById('transition-select');
  if (sel) sel.value = '';
}
window.exitTransition = exitTransition;

// ── Transition auto-exit timer ─────────────────────────────────────────────
function checkTransitionTimer() {
  if (phaseIdx !== PHASE_TRANSITION_IDX) return;
  if (transitionStartMs === null) return;
  if (morphT < 1) return;  // wait for morphism to complete first

  const elapsed = performance.now() - transitionStartMs;
  // Show countdown in pattern label
  const remaining = Math.max(0, TRANSITION_DURATION_MS - elapsed);
  const patEl = document.getElementById('case-pattern');
  if (patEl && remaining > 0) {
    const cs = CASES[caseIdx];
    const ph = cs?.phases[PHASE_TRANSITION_IDX];
    const label = ph?.transitionLabel || 'Transition';
    patEl.textContent = '⟳ ' + label + ' — ' + Math.ceil(remaining / 1000) + 's';
  }

  if (elapsed >= TRANSITION_DURATION_MS) {
    transitionStartMs = null;
    exitTransition();
  }
}

// ── Decline auto-trigger ───────────────────────────────────────────────────
const DECLINE_VP_THRESHOLD   = 0.35;  // VP must be below this
const DECLINE_COST_THRESHOLD = 0.70;  // Cost must be above this
let   declineHoldMs  = 0;
const DECLINE_HOLD_REQUIRED  = 4000;  // ms sustained before triggering

function checkDeclineCondition(dt) {
  // Only trigger from Maturity (phase 2) — not from other phases
  if (phaseIdx !== 2) { declineHoldMs = 0; return; }
  if (playing)        { declineHoldMs = 0; return; }  // let Play handle sequencing

  const vpLow   = params.vp   < DECLINE_VP_THRESHOLD;
  const costHigh = params.cost > DECLINE_COST_THRESHOLD;

  if (vpLow && costHigh) {
    declineHoldMs += dt;
    if (declineHoldMs >= DECLINE_HOLD_REQUIRED) {
      declineHoldMs = 0;
      triggerDecline();
    }
  } else {
    declineHoldMs = 0;
  }
}

function triggerDecline() {
  // Flash alert on Decline button
  const declineBtn = document.querySelector('.phase-btn[data-phase-idx="3"], .phase-btn:nth-child(4)');
  if (declineBtn) {
    declineBtn.style.opacity = '1';
    declineBtn.style.boxShadow = '0 0 10px rgba(230,65,65,0.8)';
    setTimeout(() => {
      declineBtn.style.opacity = '0.45';
      declineBtn.style.boxShadow = '';
    }, 2000);
  }
  jumpPhase(3);
  playT = 3 * PHASE_DURATION;
  // Show alert in narrative
  document.getElementById('phase-narrative-text').textContent =
    '⚠ Decline triggered — VP too low + costs too high. Adjust sliders or trigger a Transition.';
}

// ── Phase jump ─────────────────────────────────────────────────────────────
function jumpPhase(idx) {
  const prevPhase = phaseIdx;
  phaseIdx = Math.max(0, Math.min(PHASE_NAMES.length - 1, idx));

  const cs   = CASES[caseIdx];
  const prev = cs.phases[prevPhase];
  const next = cs.phases[phaseIdx];

  // Extract only numeric params for morphism
  const pick = ph => ({ vp: ph.vp, conv: ph.conv, cross: ph.cross, net: ph.net, cost: ph.cost });
  startMorph(pick(prev), pick(next));

  // Clear particles on phase change for clean visual transition
  particles = [];

  // Update narrative
  document.getElementById('phase-narrative-text').textContent = next.narrative;
  document.getElementById('phase-driver-text').textContent    = next.driver;
  document.getElementById('ls-phase').textContent = PHASE_NAMES[phaseIdx];

  // Update header title
  const headerInfo = document.getElementById('header-case-info');
  if (headerInfo) {
    const cs = CASES[caseIdx];
    headerInfo.textContent = cs
      ? cs.short + ' — phase: ' + PHASE_NAMES[phaseIdx]
      : '';
  }

  // Show transition label in compbar if Transition phase
  const patEl = document.getElementById('case-pattern');
  if (phaseIdx === PHASE_TRANSITION_IDX && next.transitionLabel) {
    if (patEl) patEl.textContent = '⟳ ' + next.transitionLabel;
  } else {
    if (patEl) patEl.textContent = cs.pattern || '';
  }

  // Phase buttons
  document.querySelectorAll('.phase-btn').forEach((btn, i) => {
    btn.classList.toggle('active', i === phaseIdx);
  });

  sliderOverride = false;
  updateCaseCard();
  updateTransitionSelect();

  // Auto-exit Transition after 5 seconds (timer starts when morphism completes)
  if (phaseIdx === PHASE_TRANSITION_IDX) {
    transitionStartMs = null;  // will be set when morphT reaches 1
  } else {
    transitionStartMs = null;
  }
}

// ── Case selection ─────────────────────────────────────────────────────────
function selectCase(idx) {
  caseIdx   = idx;
  phaseIdx  = 0;
  playT     = 0;
  sliderOverride = false;

  const cs = CASES[idx];
  const ph = cs.phases[0];

  // Only copy numeric params — do NOT pollute with narrative/driver strings
  params = { vp: ph.vp, conv: ph.conv, cross: ph.cross, net: ph.net, cost: ph.cost };
  morphT = 1;  // no morph on case switch

  // Clear all particles so new case starts fresh
  particles = [];
  Object.keys(spawnTimers).forEach(k => { spawnTimers[k] = 0; });

  // Sync sliders
  document.getElementById('sl-vp').value    = params.vp;
  document.getElementById('sl-conv').value  = params.conv;
  document.getElementById('sl-cross').value = params.cross;
  document.getElementById('sl-net').value   = params.net;
  document.getElementById('sl-cost').value  = params.cost;

  document.getElementById('phase-narrative-text').textContent = ph.narrative;
  document.getElementById('phase-driver-text').textContent    = ph.driver;
  document.getElementById('ls-case').textContent  = cs.name;
  document.getElementById('ls-phase').textContent = PHASE_NAMES[0];

  // Show pattern in compbar
  const patEl = document.getElementById('case-pattern');
  if (patEl) patEl.textContent = cs.pattern || '';

  document.querySelectorAll('.phase-btn').forEach((btn, i) => {
    btn.classList.toggle('active', i === 0);
  });

  document.getElementById('progress-fill').style.width = '0%';
  document.getElementById('morph-bar-fill') && (document.getElementById('morph-bar-fill').style.width = '0%');
  updateCaseCard();
  updateTransitionSelect();
}

// ── Update sidebar case card ───────────────────────────────────────────────
function updateCaseCard() {
  const cs = CASES[caseIdx];
  if (!cs) return;

  document.getElementById('cc-name').textContent    = cs.name;
  document.getElementById('cc-pattern').textContent = cs.pattern || '';

  // Phase rows — clickable
  const phasesEl = document.getElementById('cc-phases');
  phasesEl.innerHTML = '';
  cs.phases.forEach((ph, i) => {
    const row = document.createElement('div');
    row.className = 'case-phase-row' + (i === phaseIdx ? ' active' : '');

    const dot = document.createElement('div');
    dot.className = 'case-phase-dot';
    dot.style.background = PH_COLORS[i] || '#8b949e';

    const name = document.createElement('span');
    name.className = 'case-phase-name';
    name.textContent = PHASE_NAMES[i];

    const txt = document.createElement('span');
    txt.className = 'case-phase-text';
    const narr  = ph.narrative || '';
    const short = narr.includes('—') ? narr.split('—').slice(1).join('—').trim() : narr;
    txt.textContent = short.substring(0, 55) + (short.length > 55 ? '…' : '');

    if (i === 3) {
      // Decline — display only, not clickable
      row.style.opacity = '0.5';
      row.style.cursor  = 'default';
      row.title = 'Decline is induced automatically by slider manipulation';
      const tag = document.createElement('span');
      tag.style.cssText = 'font-size:8px;color:#E64141;margin-left:4px;opacity:0.8';
      tag.textContent = '⚙ auto';
      name.appendChild(tag);
    } else {
      row.style.cursor = 'pointer';
      row.onclick = () => { jumpPhase(i); playT = i * PHASE_DURATION; };
    }

    row.appendChild(dot); row.appendChild(name); row.appendChild(txt);
    phasesEl.appendChild(row);
  });

  // Next phase hint
  const nextEl    = document.getElementById('cc-next');
  const nextPhase = cs.phases[phaseIdx + 1];
  if (nextPhase && nextPhase.transitionLabel) {
    nextEl.textContent = '⟳ ' + nextPhase.transitionLabel;
  } else if (nextPhase) {
    const n = nextPhase.narrative || '';
    const s = n.includes('—') ? n.split('—').slice(1).join('—').trim() : n;
    nextEl.textContent = '→ ' + s.substring(0, 60);
  } else {
    nextEl.textContent = '— end of lifecycle —';
  }
}

// ── Live metrics ───────────────────────────────────────────────────────────
function updateLiveMetrics() {
  const nPart = particles.length;
  const ratio = params.conv > 0 ? (params.conv / Math.max(0.01, params.cost)).toFixed(2) : '—';
  document.getElementById('ls-particles').textContent = nPart;
  document.getElementById('ls-ratio').textContent = ratio + 'x';
}

// ── Tooltip ────────────────────────────────────────────────────────────────

// Gauge tooltip — priority over block tooltip. Returns true if gauge hit.
function showGaugeTooltip(mx, my) {
  const GAUGE_STRIP_W = 22;
  let hitBlock = null, hitGaugeV = false;

  BLOCKS.forEach(b => {
    const r = blockRects[b.id];
    if (!r) return;
    if (mx >= r.x && mx <= r.x + GAUGE_STRIP_W && my >= r.y && my <= r.y + r.h) {
      hitBlock  = b;
      hitGaugeV = (b.id === 'VP' || b.id === 'RS') && mx >= r.x + 10;
    }
  });
  if (!hitBlock) return false;

  const r   = blockRects[hitBlock.id];
  const b   = hitBlock;
  const col = COL[b.dim] || '#ffffff';
  const act = blockActivation(b);
  const flow = gaugeFlow(b);
  const trend = Math.abs(flow) < 0.04 ? '= Stable' : flow > 0 ? '▲ Filling' : '▼ Emptying';
  const ostAttrs = getOsterwalderAttrs(b.id);

  let html = '';
  if (!hitGaugeV) {
    const dimDesc = { A:'Attractor — VP pull strength', S:'Structure — block coupling',
                      F:'Flow — value & cost', It:'Information — CS signals',
                      D:'Dynamics — lifecycle' };
    html = `
      <div class="tt-title">Gauge A — ASFID: <span style="color:${col}">${b.dim}</span></div>
      <div class="tt-dim">Level: <strong>${(act*100).toFixed(0)}%</strong> &nbsp;·&nbsp; Trend: <strong>${trend}</strong></div>
      <div class="tt-sep"></div>
      <div class="tt-body">
        <strong>${b.dim}</strong> = ${dimDesc[b.dim] || b.dim}<br>
        Height = activation in current phase.<br>
        Width = rate of change (débit).<br>
        ▲▼= = trend vs. previous phase.
      </div>`;
  } else {
    const isVP = b.id === 'VP';
    const vlMap = { commodity:'Commodity ☆☆☆', customization:'Customization ★☆☆',
                    excellence:'Excellence ★★☆', innovation:'Innovation ★★★' };
    const revMap = { 'asset-sale':'Asset Sale','usage':'Usage Fee','subscription':'Subscription',
                     'licensing':'Licensing','brokerage':'Brokerage',
                     'advertising':'Advertising','cross-subsidy':'CrossSubsidy' };
    const label = isVP
      ? (ostAttrs && ostAttrs.valueLevel ? vlMap[ostAttrs.valueLevel] : '—')
      : (ostAttrs && ostAttrs.revenueType ? revMap[ostAttrs.revenueType] || ostAttrs.revenueType : '—');
    html = `
      <div class="tt-title">Gauge V — ${isVP ? 'Value Level' : 'Revenue Type'}</div>
      <div class="tt-dim"><strong>${label}</strong></div>
      <div class="tt-sep"></div>
      <div class="tt-body">
        ${isVP
          ? 'Height = Osterwalder Value Level:<br>Commodity → Customization → Excellence → Innovation.'
          : 'Height = Revenue Complexity:<br>Asset Sale → Usage → Subscription → Brokerage → CrossSubsidy.'}
        <br><span style="color:#F5A623">■ Golden gauge</span> = Osterwalder PhD (2004).
      </div>`;
  }

  const tt = document.getElementById('block-tooltip');
  tt.innerHTML = html;
  tt.className = 'tt-gauge';
  tt.style.setProperty('--tt-accent', hitGaugeV ? '#F5A623' : (COL[hitBlock.dim] || '#64c8ff'));
  tt.style.display = 'block';

  const ca    = document.getElementById('canvas-area').getBoundingClientRect();
  const GAP   = -5;
  const tx    = ca.left + r.x + GAUGE_STRIP_W + GAP;
  // Bottom of tooltip aligned with bottom of block
  const ttH   = tt.offsetHeight || 140;
  const blockBottom = ca.top + r.y + r.h;
  const ty    = Math.max(ca.top + 4, blockBottom - ttH);

  tt.style.left = tx + 'px';
  tt.style.top  = ty + 'px';
  return true;
}

function showBlockTooltip(mx, my) {
  const tt = document.getElementById('block-tooltip');
  let found = null;
  BLOCKS.forEach(b => {
    const r = blockRects[b.id];
    if (!r) return;
    if (mx >= r.x && mx <= r.x + r.w && my >= r.y && my <= r.y + r.h) found = b;
  });
  if (!found) { hideTooltip(); return; }

  const r    = blockRects[found.id];
  const act  = blockActivation(found).toFixed(2);
  const id   = found.id;

  // Try to get case-specific block content for current phase
  const cs   = CASES[caseIdx];
  const ph   = cs ? cs.phases[phaseIdx] : null;
  const bcObj = ph && ph.blockContent ? ph.blockContent[id] : null;
  const bcGeneric = GENERIC_BLOCKS[phaseIdx] ? GENERIC_BLOCKS[phaseIdx][id] : null;
  const bc   = bcObj || bcGeneric;

  // Phase label and color
  const phName  = PHASE_NAMES[phaseIdx] || '';
  const phColor = PH_COLORS[phaseIdx]   || '#8b949e';

  // Generic TSCG framing (always shown)
  const generic = BLOCK_DESC[id] || '';
  const blockCol = COL[found.dim] || '#64c8ff';

  // Header: title + phase right-aligned, dim row below
  const headerHtml = `
    <div class="tt-header">
      <div class="tt-title-row">
        <span class="tt-title">${found.label} (${found.abbr})</span>
        <span class="tt-phase-badge">${phName}</span>
      </div>
      <div class="tt-dim">ASFID: ${found.dim} &nbsp;·&nbsp; Activation: ${act}</div>
    </div>
    <div class="tt-body-wrap">`;

  let bodyHtml = '';
  if (bc) {
    const desc = bc.desc || '';
    const descLines = desc.split('\\n').map(l => l.trim()).filter(Boolean);
    // No case-label line — removed
    bodyHtml += `<div class="tt-block-content">`;
    descLines.forEach(l => {
      const formatted = l.replace(/^(GUESTS|HOSTS|B2B|B2C):/,
        '<span class="tt-segment">$1:</span>');
      bodyHtml += `<div class="tt-bc-line">${formatted}</div>`;
    });
    bodyHtml += `</div><div class="tt-sep"></div>`;
  }
  bodyHtml += `<div class="tt-body">${generic}</div></div>`;

  tt.innerHTML = headerHtml + bodyHtml;
  tt.className = 'tt-block';
  tt.style.setProperty('--tt-accent', blockCol);
  tt.style.display = 'block';

  // position:fixed → coords relative to viewport, not canvas
  // Anchor: just to the right of the abbr label (top-left of block content area)
  // CONTENT_X = r.x + 18,  TITLE_TOP = r.y + 10  (matching drawBlocks constants)
  const ca       = document.getElementById('canvas-area').getBoundingClientRect();
  const ABBR_PX  = found.abbr.length <= 2 ? 36 : 48;  // approx abbr pixel width at 22px bold
  const anchorX  = ca.left + r.x + 18 + ABBR_PX + 6;  // right of abbr + small gap
  const anchorY  = ca.top  + r.y + 10;                 // same height as title

  const tx = anchorX;
  const ty = Math.max(ca.top + 4, Math.min(anchorY, (window.innerHeight || 800) - 220));

  tt.style.left = tx + 'px';
  tt.style.top  = ty + 'px';
}

function hideTooltip() {
  document.getElementById('block-tooltip').style.display = 'none';
}

// ── Public controls (called from HTML) ────────────────────────────────────
window.toggleFlux = function() {
  fluxVisible = !fluxVisible;
  const btn = document.getElementById('btn-flux');
  if (btn) {
    btn.style.opacity     = fluxVisible ? '1' : '0.4';
    btn.style.borderColor = fluxVisible ? '#79c0ff' : '';
    btn.style.color       = fluxVisible ? '#79c0ff' : '';
  }
};

window.togglePillars = function() {
  pillarsVisible = !pillarsVisible;
  const btn = document.getElementById('btn-pillars');
  if (pillarsVisible) {
    btn.classList.add('active');
    btn.style.boxShadow = '0 0 8px 2px rgba(100,200,255,0.5)';
    btn.style.borderColor = '#79c0ff';
    btn.style.color = '#79c0ff';
  } else {
    btn.classList.remove('active');
    btn.style.boxShadow = '';
    btn.style.borderColor = '';
    btn.style.color = '';
  }
};

window.togglePlay = function() {
  playing = !playing;
  const btn = document.getElementById('btn-play');
  const dot = document.getElementById('status-dot');
  const lbl = document.getElementById('status-label');
  if (playing) {
    if (playT >= PHASE_DURATION * PHASE_NAMES.length) {
      playT = 0; phaseIdx = 0;
      jumpPhase(0);
    }
    lastFrameMs = performance.now();
    btn.textContent = '⏸ Pause';
    btn.classList.add('active');
    dot.className = 'status-dot running';
    lbl.textContent = 'Playing';
  } else {
    btn.textContent = '▶ Play';
    btn.classList.remove('active');
    dot.className = 'status-dot paused';
    lbl.textContent = 'Paused';
  }
};

window.resetSim = function() {
  playing = false; selectedPillar = null;
  playT   = 0; phaseIdx = 0;
  document.getElementById('btn-play').textContent = '▶ Play';
  document.getElementById('btn-play').classList.remove('active');
  document.getElementById('status-dot').className = 'status-dot';
  document.getElementById('status-label').textContent = 'Stopped';
  selectCase(caseIdx);
  particles = [];
};

window.setSpeed = function(s) {
  speed = s;
  ['btn-spd1','btn-spd2','btn-spd4'].forEach(id => {
    document.getElementById(id).classList.remove('spd-active');
  });
  document.getElementById('btn-spd' + s).classList.add('spd-active');
};

window.seekProgress = function(e) {
  const rect = e.currentTarget.getBoundingClientRect();
  const ratio = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
  playT = ratio * PHASE_DURATION * PHASE_NAMES.length;
  const newPhase = Math.min(PHASE_NAMES.length - 1, Math.floor(playT / PHASE_DURATION));
  jumpPhase(newPhase);
  document.getElementById('progress-fill').style.width = (ratio * 100) + '%';
};

window.activateTab = function(idx) {
  document.querySelectorAll('.tab-panel').forEach((p, i) => {
    p.classList.toggle('active', i === idx);
  });
  document.querySelectorAll('.tab-btn').forEach((b, i) => {
    b.classList.toggle('active', i === idx);
  });
};

// ── Slider event listeners ─────────────────────────────────────────────────
function bindSliders() {
  const map = {
    'sl-vp':   'vp',   'sl-conv': 'conv', 'sl-cross': 'cross',
    'sl-net':  'net',  'sl-cost': 'cost'
  };
  Object.entries(map).forEach(([id, key]) => {
    const el = document.getElementById(id);
    el.addEventListener('input', () => {
      params[key] = parseFloat(el.value);
      sliderOverride = true;
      morphT = 1; // cancel morphism
    });
  });
}

// ── Build compbar UI ───────────────────────────────────────────────────────
function buildUI() {
  // Case dropdown
  const sel = document.getElementById('case-select');
  CASES.forEach((c, i) => {
    const opt = document.createElement('option');
    opt.value = i; opt.textContent = c.name;
    sel.appendChild(opt);
  });
  sel.addEventListener('change', () => selectCase(parseInt(sel.value)));

  // Phase buttons — Decline (idx 3) and Transition (idx 4) not shown as buttons
  const pb = document.getElementById('phase-btns');
  PHASE_NAMES.forEach((nm, i) => {
    if (i === 3 || i === 4) return;  // Decline: cursor-induced. Transition: combolist-triggered.
    const btn = document.createElement('button');
    btn.className = 'phase-btn' + (i === 0 ? ' active' : '');
    btn.textContent = (i + 1) + ' ' + nm;
    btn.dataset.phaseIdx = i;
    btn.style.background  = hexAlpha(PH_COLORS[i], 0.12);
    btn.style.borderColor = hexAlpha(PH_COLORS[i], 0.25);
    btn.style.color       = PH_COLORS[i];
    btn.onclick = () => { jumpPhase(i); playT = i * PHASE_DURATION; };
    pb.appendChild(btn);
  });
}

function hexAlpha(hex, a) {
  const r = parseInt(hex.slice(1,3), 16);
  const g = parseInt(hex.slice(3,5), 16);
  const b = parseInt(hex.slice(5,7), 16);
  return `rgba(${r},${g},${b},${a})`;
}

// ── Splitter drag ──────────────────────────────────────────────────────────
function initSplitter() {
  const splitter = document.getElementById('splitter');
  const app      = document.getElementById('app');
  let dragging   = false;
  let startX, startW;

  splitter.addEventListener('mousedown', e => {
    dragging = true;
    startX   = e.clientX;
    startW   = parseInt(getComputedStyle(document.documentElement)
                 .getPropertyValue('--sidebar-w'));
    splitter.classList.add('dragging');
    document.body.style.cursor = 'col-resize';
    e.preventDefault();
  });
  window.addEventListener('mousemove', e => {
    if (!dragging) return;
    const delta = startX - e.clientX;
    const newW  = Math.max(180, Math.min(500, startW + delta));
    document.documentElement.style.setProperty('--sidebar-w', newW + 'px');
  });
  window.addEventListener('mouseup', () => {
    if (!dragging) return;
    dragging = false;
    splitter.classList.remove('dragging');
    document.body.style.cursor = '';
  });
}

// ── Init ───────────────────────────────────────────────────────────────────
// ── Ontology loader — fetch from GitHub, fallback to local .jsonld.js ────────
const JSONLD_URL =
  'https://raw.githubusercontent.com/Echopraxium/tscg/main/' +
  'instances/systemic-frameworks/Bmc/M0_BmcSimulation.jsonld';

async function loadCases() {
  // 1. Try GitHub raw (works for file:// too — CORS: Access-Control-Allow-Origin: *)
  try {
    const url  = JSONLD_URL + '?v=' + Date.now();  // cache-bust for dev
    const resp = await fetch(url, { cache: 'no-cache' });
    if (resp.ok) {
      const ontology = await resp.json();
      const cases    = buildCasesFromGraph(ontology['@graph']);
      if (cases && cases.length > 0) {
        console.info(`[BMC] Ontology loaded from GitHub (${cases.length} cases)`);
        showLoadSource('GitHub');
        return cases;
      }
    }
  } catch (e) {
    console.warn('[BMC] GitHub fetch failed:', e.message);
  }

  // 2. Fallback: local M0_BmcSimulation.jsonld.js (already loaded as script tag)
  if (typeof buildCasesFromOntology === 'function') {
    const cases = buildCasesFromOntology();
    console.info(`[BMC] Ontology loaded from local fallback (${cases.length} cases)`);
    showLoadSource('local');
    return cases;
  }

  // 3. Last resort: empty array (simulation starts with no cases)
  console.error('[BMC] No ontology source available');
  return [];
}

// Build CASES from a raw @graph array (used for GitHub fetch path)
function buildCasesFromGraph(graph) {
  // Reuse the same builder from M0_BmcSimulation.jsonld.js
  // by temporarily overriding the ontology's @graph
  if (typeof buildCasesFromOntology !== 'function') return [];
  const orig = BMC_SIMULATION_ONTOLOGY['@graph'];
  BMC_SIMULATION_ONTOLOGY['@graph'] = graph;
  const result = buildCasesFromOntology();
  BMC_SIMULATION_ONTOLOGY['@graph'] = orig;
  return result;
}

function showLoadSource(source) {
  const el = document.getElementById('ontology-source');
  if (!el) return;
  el.textContent = source === 'GitHub' ? '☁ GitHub' : '💾 local';
  el.title = source === 'GitHub'
    ? 'Ontology loaded from GitHub raw (M0_BmcSimulation.jsonld)'
    : 'Ontology loaded from local M0_BmcSimulation.jsonld.js (GitHub unavailable)';
  el.className = 'ontology-badge ' + (source === 'GitHub' ? 'badge-online' : 'badge-offline');
}

// ── Async init ────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', async () => {
  // Load cases (async — GitHub or local fallback)
  const loadedCases = await loadCases();

  // Inject into global CASES array (used by all rendering functions)
  CASES.length = 0;
  loadedCases.forEach(c => CASES.push(c));

  // Start simulation
  buildUI();
  bindSliders();
  initSplitter();
  selectCase(0);
  new p5(sketch, document.getElementById('p5-container'));
  document.getElementById('btn-spd1').classList.add('spd-active');
});
