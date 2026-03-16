"""
tscg_explorer.py
================
TSCG Tool — tscg-explorer v2.1.0
Author : Echopraxium with the collaboration of Claude AI
Date   : 2026-03-01

Three-panel interactive visualizer for M2 GenericConcepts (laptop 1280x760).

LEFT   panel — IS-A Tree Explorer (file-explorer style, collapsible)
CENTER panel — 2D concept net (3 projection modes, zoom, pan)
               + colour legend (top-left of net)
RIGHT  panel — Concept profile + README (horizontal drag-splitter)

Three resizable panels separated by two VERTICAL drag-splitters.
One HORIZONTAL drag-splitter inside the right panel (profile / readme).

Projection modes:
  A (default) — ASFID ratio x Dimensionality
  B           — Family x Dimensionality
  C           — ASFID count x REVOI count

Node shapes:
  Triangle  — atomic GenericConcept
  Diamond   — GenericConceptCombo (synergistic N-ary assembly)

Node colours by family (shown in legend):
  Structural(21) blue  Dynamic(15) orange  Informational(8) green
  Ontological(9) purple  Regulatory(8) red  Relational(5) teal
  Adaptive(4) yellow  Energetic(2) deep-orange  Teleonomic(1) sky-blue
  Combo(8) grey-white

Tensor formula tiles in profile:
  ASFID (warm): A=red  S=blue  F=cyan  I=green  D=amber
  REVOI (cool): R=purple  E=magenta  V=mauve  O=teal  Im=lavender
  Tensor product operator: drawn as circle-with-cross (⊗)

Graph edges:
  solid  blue   : IS-A (rdfs:subClassOf)
  dashed orange : Combo component (tensor assembly)

Controls:
  [A][B][C]            keyboard or buttons — projection mode
  Drag vertical bars   resize tree / net / info panels
  Drag horizontal bar  resize profile / readme inside right panel
  Wheel on net         zoom (cursor-centred)
  Drag on net          pan
  Click tree row       select / toggle family or node
  Click net node       select concept
  Wheel on profile / readme / tree   scroll
  ESC                  quit

Requirements : pip install pygame
Run          : python tscg_explorer.py
"""

import math, sys
import pygame

# =============================================================================
# INITIAL LAYOUT  (splitters make these dynamic at runtime)
# =============================================================================
WIN_W, WIN_H  = 1280, 760
FPS           = 60
STATUS_H      = 30
CONTENT_H     = WIN_H - STATUS_H

_INIT_TREE_W  = 230        # initial tree panel width
_INIT_NET_W   = 560        # initial net panel width
VSP_W         = 6          # vertical splitter width
HSP_H         = 6          # horizontal splitter height (inside right panel)
MIN_TREE_W    = 100
MIN_NET_W     = 200
MIN_INFO_W    = 150
MIN_ZONE_H    = 60         # min height for profile / readme

PAD           = 8
ROW_H         = 18

# =============================================================================
# COLOURS
# =============================================================================
BG            = ( 18,  20,  30)
PANEL_BG      = ( 26,  29,  44)
BORDER        = ( 55,  65,  95)
C_TEXT        = (220, 225, 240)
C_DIM         = (120, 130, 155)
C_HIGH        = (255, 230,  80)
C_SEL         = (255, 255, 100)
C_HOV         = (175, 175, 175)
EDGE_ISA      = (110, 155, 255)
EDGE_COMBO    = (255, 145,  55)
GRID_C        = ( 32,  37,  56)
AXIS_C        = ( 62,  72, 102)
BTN_ON        = ( 50,  88, 200)
BTN_OFF       = ( 36,  42,  66)
SPL_VC        = ( 55,  68,  98)   # vertical splitter
SPL_VH        = ( 95, 115, 165)   # vertical splitter hovered
SPL_HC        = ( 65,  78, 110)   # horizontal splitter
SPL_HH        = (105, 125, 175)   # horizontal splitter hovered
TREE_SEL_C    = ( 48,  62, 118)
TREE_HOV_C    = ( 36,  44,  72)
STATUS_C      = ( 20,  24,  38)
SB_BG         = ( 38,  44,  66)
SB_FG         = ( 80,  95, 140)

FAMILY_COLORS = {
    "Structural":    ( 70, 130, 220),
    "Dynamic":       (245, 140,  35),
    "Informational": ( 70, 195,  75),
    "Ontological":   (160,  80, 215),
    "Regulatory":    (215,  55,  55),
    "Relational":    ( 50, 195, 185),
    "Adaptive":      (240, 205,  45),
    "Energetic":     (255,  85,  20),
    "Teleonomic":    ( 35, 175, 250),
    "Combo":         (185, 190, 200),
}

FAMILY_ORDER = [
    "Structural","Dynamic","Informational","Ontological","Regulatory",
    "Relational","Adaptive","Energetic","Teleonomic","Combo",
]

DIM_COL = {
    "A": (220, 75, 45),  "S": (55, 115, 210),  "F": (25, 195, 210),
    "I": (50, 185, 75),  "It":(50, 185, 75),   "Ft":(25, 195, 210),
    "D": (225,160, 25),  "R": (150, 55, 210),  "E": (215, 45, 160),
    "V": (190, 95,150),  "O": (38, 165, 145),  "Im":(125,105, 210),
}
DIM_LBL = {
    "A":"A","S":"S","F":"F","I":"I","It":"I","Ft":"F","D":"D",
    "R":"R","E":"E","V":"V","O":"O","Im":"Im",
}
_ASFID = {"A","S","F","I","D","It","Ft"}
_REVOI = {"R","E","V","O","Im"}

# =============================================================================
# CONCEPT DATA  (81 GenericConcepts)
# =============================================================================
_RAW = [
    # Structural (21)
    {"name":"Channel",       "dims":["S","I","F","E"],            "family":"Structural"},
    {"name":"Cluster",       "dims":["A","I","S","D","O"],        "family":"Structural"},
    {"name":"Capacity",      "dims":["S","I","A","E","O"],        "family":"Structural"},
    {"name":"Component",     "dims":["S","I","F","R"],            "family":"Structural"},
    {"name":"Composition",   "dims":["S","I","A"],                "family":"Structural"},
    {"name":"Hub",           "dims":["S","F","E"],                "family":"Structural"},
    {"name":"Hierarchy",     "dims":["A","S","V","R"],            "family":"Structural"},
    {"name":"Identity",      "dims":["S","I","A","V","E"],        "family":"Structural"},
    {"name":"Imbrication",   "dims":["S"],                        "family":"Structural"},
    {"name":"Interoperability","dims":["S","Im"],                 "family":"Structural"},
    {"name":"Invariant",     "dims":["A","S","V"],                "family":"Structural"},
    {"name":"Modularity",    "dims":["S","I","Im"],               "family":"Structural"},
    {"name":"Network",       "dims":["S","I","F","D","Im"],       "family":"Structural"},
    {"name":"Node",          "dims":["S","I","F","Im"],           "family":"Structural"},
    {"name":"Path",          "dims":["S","I","D","O"],            "family":"Structural"},
    {"name":"Polarity",      "dims":["A","I","S","R"],            "family":"Structural"},
    {"name":"Segmentation",  "dims":["S","I","D","R"],            "family":"Structural"},
    {"name":"Step",          "dims":["S","I","D","Im"],           "family":"Structural"},
    {"name":"Symmetry",      "dims":["S"],                        "family":"Structural"},
    {"name":"Topology",      "dims":["S","I","A","V"],            "family":"Structural"},
    {"name":"Workflow",      "dims":["D","F","S","V"],            "family":"Structural"},
    # Dynamic (15)
    {"name":"Action",        "dims":["D","I","E"],                "family":"Dynamic"},
    {"name":"Alignment",     "dims":["I","A","S"],                "family":"Dynamic"},
    {"name":"Amplification", "dims":["F","D","I","R","O"],        "family":"Dynamic"},
    {"name":"Behavior",      "dims":["D","F","S","R"],            "family":"Dynamic"},
    {"name":"Bifurcation",   "dims":["A","D","S"],                "family":"Dynamic",
                             "superclass":"Duplication"},
    {"name":"Convergence",   "dims":["D"],                        "family":"Dynamic"},
    {"name":"Duplication",   "dims":["S","I","F","D","V"],        "family":"Dynamic"},
    {"name":"Event",         "dims":["D","I","O"],                "family":"Dynamic"},
    {"name":"FeedbackLoop",  "dims":["A","S","I","F","D","V","R","E"],"family":"Dynamic",
                             "superclass":"GenericConceptCombo",
                             "combo_of":["Process","Alignment","Homeostasis"]},
    {"name":"Fusion",        "dims":["S","D"],                    "family":"Dynamic"},
    {"name":"Process",       "dims":["D","F","R"],                "family":"Dynamic"},
    {"name":"Synergy",       "dims":["D","I","R"],                "family":"Dynamic"},
    {"name":"Transformation","dims":["S","I","D","F","V"],        "family":"Dynamic"},
    {"name":"Trajectory",    "dims":["S","I","D","F"],            "family":"Dynamic"},
    {"name":"Tropism",       "dims":["A","S","D","F"],            "family":"Dynamic"},
    # Informational (8)
    {"name":"Code",          "dims":["S","I","V"],                "family":"Informational"},
    {"name":"Coding",        "dims":["S","I","D","F","R"],        "family":"Informational"},
    {"name":"Language",      "dims":["S","I","F","A","R"],        "family":"Informational"},
    {"name":"Pattern",       "dims":["S","It","A","R","Im"],      "family":"Informational"},
    {"name":"Representation","dims":["S","I","V","R"],            "family":"Informational"},
    {"name":"Signal",        "dims":["F","I","R"],                "family":"Informational"},
    {"name":"Signature",     "dims":["S","I","A","O"],            "family":"Informational"},
    {"name":"ValueSpace",    "dims":["I","V","O","R","Im"],       "family":"Informational"},
    # Ontological (9)
    {"name":"Environment",   "dims":["F","I","O"],                "family":"Ontological"},
    {"name":"Gradient",      "dims":["F"],                        "family":"Ontological"},
    {"name":"Observer",      "dims":["A","I","R"],                "family":"Ontological"},
    {"name":"Resource",      "dims":["F","I","A"],                "family":"Ontological"},
    {"name":"Scope",         "dims":["A","S","R"],                "family":"Ontological"},
    {"name":"Space",         "dims":["S","I","D","E"],            "family":"Ontological"},
    {"name":"State",         "dims":["I"],                        "family":"Ontological"},
    {"name":"Substrate",     "dims":["S","F","O"],                "family":"Ontological"},
    {"name":"System",        "dims":["S","F","V"],                "family":"Ontological"},
    # Regulatory (8)
    {"name":"Activation",    "dims":["A","D"],                    "family":"Regulatory"},
    {"name":"Balance",       "dims":["A","S","F","O","V"],        "family":"Regulatory"},
    {"name":"Constraint",    "dims":["S","I","F","V","R"],        "family":"Regulatory"},
    {"name":"Homeostasis",   "dims":["A","S","F","V","E"],        "family":"Regulatory"},
    {"name":"Regulation",    "dims":["A","S","F","V","R"],        "family":"Regulatory"},
    {"name":"Threshold",     "dims":["A","I","O"],                "family":"Regulatory"},
    {"name":"Trade-off",     "dims":["A","I","F"],                "family":"Regulatory"},
    {"name":"Trigger",       "dims":["D","I","V"],                "family":"Regulatory"},
    # Relational (5)
    {"name":"Agent",         "dims":["S","I","D","A","E"],        "family":"Relational"},
    {"name":"Link",          "dims":["S","I","F","V"],            "family":"Relational"},
    {"name":"Mediator",      "dims":["S","I","F","O"],            "family":"Relational"},
    {"name":"Relation",      "dims":["S","I","A","Im"],           "family":"Relational"},
    {"name":"Role",          "dims":["S","I","F","O","R"],        "family":"Relational"},
    # Adaptive (4)
    {"name":"Adaptation",    "dims":["I","F","D"],                "family":"Adaptive"},
    {"name":"Emergence",     "dims":["S","I","D","V"],            "family":"Adaptive"},
    {"name":"Memory",        "dims":["D","F"],                    "family":"Adaptive"},
    {"name":"Resilience",    "dims":["A","S","E"],                "family":"Adaptive"},
    # Energetic (2)
    {"name":"Dissipation",   "dims":["D","F","V"],                "family":"Energetic"},
    {"name":"Storage",       "dims":["S","F","R"],                "family":"Energetic"},
    # Teleonomic (1)
    {"name":"Self-Organization","dims":["A","I","D"],             "family":"Teleonomic"},
    # Combo (8)  — all shown flat (depth=1) regardless of superclass
    {"name":"GenericConceptCombo","dims":[],"family":"Combo","abstract":True},
    {"name":"ButterflyEffect","dims":["A","S","F","D"],           "family":"Combo",
                             "superclass":"GenericConceptCombo",
                             "combo_of":["Cascade","Amplification"]},
    {"name":"Cascade",       "dims":["S","I","D","F","R"],        "family":"Combo",
                             "superclass":"GenericConceptCombo",
                             "combo_of":["Process","Step","Trajectory"]},
    {"name":"FeedbackLoop",  "dims":["A","S","I","F","D","V","R","E"],"family":"Combo",
                             "superclass":"GenericConceptCombo",
                             "combo_of":["Process","Alignment","Homeostasis"]},
    {"name":"LocalActivationLateralInhibition",
                             "dims":["S","A","F","I"],            "family":"Combo",
                             "superclass":"GenericConceptCombo",
                             "combo_of":["Activation","Regulation","Threshold"]},
    {"name":"Narration",     "dims":["S","I","D","F","V","R","A","Im"],"family":"Combo",
                             "superclass":"GenericConceptCombo",
                             "combo_of":["Transformation","Representation","Relation"]},
    {"name":"Oscillator",    "dims":["S","A","I","D","F"],        "family":"Combo",
                             "superclass":"GenericConceptCombo",
                             "combo_of":["Component","Process","Trajectory"]},
    {"name":"Processor",     "dims":["S","F","D","R","I"],        "family":"Combo",
                             "superclass":"GenericConceptCombo",
                             "combo_of":["Component","Process","Signal"]},
    {"name":"Propagation",   "dims":["S","I","D","F","R","V","Im"],"family":"Combo",
                             "superclass":"GenericConceptCombo",
                             "combo_of":["Cascade","Duplication","Network"]},
]

def _norm(c):
    return {"name":c["name"],"dims":c.get("dims",[]),"family":c.get("family","Structural"),
            "superclass":c.get("superclass"),"combo_of":c.get("combo_of",[]),
            "abstract":c.get("abstract",False)}

# Deduplicate (FeedbackLoop appears twice intentionally in Dynamic and Combo)
_seen=set(); _deduped=[]
for c in _RAW:
    if c["name"] not in _seen: _seen.add(c["name"]); _deduped.append(c)

CONCEPTS = [_norm(c) for c in _deduped]
NAME_MAP  = {c["name"]:i for i,c in enumerate(CONCEPTS)}

def dc(dims):
    a=sum(1 for d in dims if d in _ASFID)
    r=sum(1 for d in dims if d in _REVOI)
    return a,r

def is_combo(c):
    return bool(c["combo_of"]) or c["abstract"] or c["family"]=="Combo"

# =============================================================================
# TREE  — Combo family is always flat (all depth=1)
# =============================================================================
class TNode:
    __slots__=("idx","depth","children","expanded")
    def __init__(self,idx,d): self.idx=idx;self.depth=d;self.children=[];self.expanded=True

def build_tree():
    fm={f:[] for f in FAMILY_ORDER}
    for i,c in enumerate(CONCEPTS): fm[c["family"]].append(i)
    roots=[]
    for fam in FAMILY_ORDER:
        idxs=fm[fam]
        if fam=="Combo":
            # All Combos flat at depth=1 — IS-A shown on graph, not in tree
            nodes=[TNode(i,1) for i in sorted(idxs,key=lambda x:CONCEPTS[x]["name"])]
        else:
            cm={i:[] for i in idxs}; top=[]
            for i in idxs:
                sc=CONCEPTS[i]["superclass"]
                if sc and sc in NAME_MAP and NAME_MAP[sc] in cm:
                    cm[NAME_MAP[sc]].append(i)
                else:
                    top.append(i)
            def mk(idx,d):
                n=TNode(idx,d)
                for ci in sorted(cm[idx],key=lambda x:CONCEPTS[x]["name"]):
                    n.children.append(mk(ci,d+1))
                return n
            nodes=[mk(i,1) for i in sorted(top,key=lambda x:CONCEPTS[x]["name"])]
        roots.append((fam,nodes))
    return roots

TREE_ROOTS=build_tree()

def flatten_tree(roots,fam_exp):
    rows=[]
    for fam,nodes in roots:
        rows.append(("F",fam))
        if fam_exp.get(fam,True):
            def walk(n):
                rows.append(("C",n.idx,n.depth,bool(n.children),n))
                if n.expanded:
                    for ch in n.children: walk(ch)
            for n in nodes: walk(n)
    return rows

# =============================================================================
# PROJECTIONS
# =============================================================================
def jitter(ji,jt,sp=13):
    return 0 if jt<=1 else (ji-(jt-1)/2)*sp

def pos_A(concepts):
    md=max((len(c["dims"]) for c in concepts),default=1) or 1
    cc={}
    for c in concepts:
        a,_=dc(c["dims"]); t=len(c["dims"])
        k=(t,round(a/t,2) if t else 0.5); cc[k]=cc.get(k,0)+1
    ci={}; out=[]
    for c in concepts:
        a,_=dc(c["dims"]); t=len(c["dims"])
        rat=a/t if t else 0.5; k=(t,round(rat,2))
        idx=ci.get(k,0); ci[k]=idx+1
        out.append((rat,t/md,idx,cc[k]))
    return out

def pos_B(concepts):
    md=max((len(c["dims"]) for c in concepts),default=1) or 1
    nf=len(FAMILY_ORDER); cc={}
    for c in concepts:
        k=(FAMILY_ORDER.index(c["family"]),len(c["dims"])); cc[k]=cc.get(k,0)+1
    ci={}; out=[]
    for c in concepts:
        fi=FAMILY_ORDER.index(c["family"]); t=len(c["dims"]); k=(fi,t)
        idx=ci.get(k,0); ci[k]=idx+1
        out.append((fi/(nf-1),t/md,idx,cc[k]))
    return out

def pos_C(concepts):
    ma=max((dc(c["dims"])[0] for c in concepts),default=1) or 1
    mr=max((dc(c["dims"])[1] for c in concepts),default=1) or 1
    cc={}
    for c in concepts:
        k=dc(c["dims"]); cc[k]=cc.get(k,0)+1
    ci={}; out=[]
    for c in concepts:
        a,r=dc(c["dims"]); k=(a,r)
        idx=ci.get(k,0); ci[k]=idx+1
        out.append((a/ma,r/mr,idx,cc[k]))
    return out

# =============================================================================
# DRAWING PRIMITIVES
# =============================================================================
def dashed(surf,col,p1,p2,dash=7,gap=4,w=1):
    dx,dy=p2[0]-p1[0],p2[1]-p1[1]; L=math.hypot(dx,dy)
    if L<1: return
    ux,uy=dx/L,dy/L; pos=0; on=True
    while pos<L:
        ep=min(pos+(dash if on else gap),L)
        if on:
            pygame.draw.line(surf,col,
                (int(p1[0]+ux*pos),int(p1[1]+uy*pos)),
                (int(p1[0]+ux*ep), int(p1[1]+uy*ep)),w)
        pos+=(dash if on else gap); on=not on

def tri(surf,col,cx,cy,r,outline=None):
    h=r*math.sqrt(3)
    pts=[(cx,cy-r*1.15),(cx-h*0.6,cy+r*0.7),(cx+h*0.6,cy+r*0.7)]
    pygame.draw.polygon(surf,col,pts)
    if outline: pygame.draw.polygon(surf,outline,pts,1)

def dia(surf,col,cx,cy,r,outline=None):
    pts=[(cx,cy-r),(cx+r,cy),(cx,cy+r),(cx-r,cy)]
    pygame.draw.polygon(surf,col,pts)
    if outline: pygame.draw.polygon(surf,outline,pts,1)

def draw_node(surf,c,cx,cy,r,ring=None):
    col=FAMILY_COLORS.get(c["family"],(160,160,160))
    if c["abstract"]: col=tuple(max(0,v-40) for v in col)
    if ring:
        if is_combo(c): dia(surf,ring,cx,cy,int(r+4))
        else:           tri(surf,ring,cx,cy,int(r+4))
    if is_combo(c): dia(surf,col,cx,cy,int(r))
    else:           tri(surf,col,cx,cy,int(r))

def otimes(surf,cx,cy,r,col):
    """Draw tensor-product operator ⊗ as a circle with a cross inside."""
    pygame.draw.circle(surf,col,(cx,cy),r,1)
    pygame.draw.line(surf,col,(cx-r,cy),(cx+r,cy),1)
    pygame.draw.line(surf,col,(cx,cy-r),(cx,cy+r),1)

def scrollbar_draw(surf,rect,scroll,total_h):
    if total_h<=rect.height: return
    ratio=rect.height/total_h
    bh=max(18,int(rect.height*ratio))
    by=rect.y+int(scroll/total_h*rect.height)
    pygame.draw.rect(surf,SB_BG,(rect.right-5,rect.y,5,rect.height))
    pygame.draw.rect(surf,SB_FG,(rect.right-5,by,5,bh),border_radius=2)

def vsplitter_draw(surf,x,h,hovered):
    col=SPL_VH if hovered else SPL_VC
    pygame.draw.rect(surf,col,(x-VSP_W//2,0,VSP_W,h))
    for dy in range(h//2-20,h//2+21,6):
        pygame.draw.circle(surf,(120,135,170),(x,dy),1)

# =============================================================================
# README TEXT
# =============================================================================
README = """
# M2 GenericConcepts — Quick Reference
v15.9.0 · 2026-02-28
Echopraxium with the collaboration of Claude AI

## ASFID — Eagle Eye (Territory)
A  Attractor    stable states, goals, equilibria
S  Structure    topology, architecture
F  Flow         flux, transfer, exchange
I  Information  content, signal, state
D  Dynamics     temporal evolution, change rate

## REVOI — Sphinx Eye (Map)
R  Representability  semantic encodability
   !!! NOT Reproducibility !!!
E  Evolvability      model adaptability
V  Verifiability     testability, fidelity
O  Observability     measurability of states
Im Interoperability  subsystem compatibility

## Statistics (v15.9.0)
Total GenericConcepts : 81
  Atomic (triangles)  : 73
  Combos (diamonds)   : 7 + 1 abstract
Families              : 10

## Families & dominant dims
Structural   (21)  S, I dominant
Dynamic      (15)  D, F dominant
Informational (8)  I, R dominant
Ontological   (9)  S, F patterns
Regulatory    (8)  A dominant
Relational    (5)  S, I, F
Adaptive      (4)  I, D
Energetic     (2)  F, D
Teleonomic    (1)  A, I, D
Combo         (8)  synergistic assemblies

## GenericConceptCombos
Cascade        Process+Step+Trajectory      5D
Oscillator     Component+Process+Traj       5D
Propagation    Cascade+Duplic+Network       7D
Narration      Transf+Repr+Relation         8D
FeedbackLoop   Process+Alignment+Homeo      8D
Processor      Component+Process+Signal     5D
ButterflyEffect  Cascade+Amplification      4D
LALI           Activ+Regul+Threshold        4D

## IS-A relationships (solid blue edges)
Bifurcation  -> Duplication
All Combos   -> GenericConceptCombo (abstract)

## Projection modes
A (default) : ASFID_ratio x Dimensionality
  Reveals Territory/Map balance of corpus
B : Family x Dimensionality
  Groups concepts by family
C : ASFID_count x REVOI_count
  Pure bicephalous decomposition

## Tensor tile colours
Warm (ASFID):
  A = red-orange   Attractor
  S = blue         Structure
  F = cyan         Flow
  I = green        Information
  D = amber        Dynamics
Cool (REVOI):
  R = purple       Representability
  E = magenta      Evolvability
  V = mauve        Verifiability
  O = teal         Observability
  Im= lavender     Interoperability

The ⊗ operator (circle+cross) separates
dimension tiles in tensor formulas.

## Key principle
"The map is not the territory"
  — Korzybski, 1933

TSCG bicephalous distinction:
  Territory (ASFID) = what a system IS
  Map       (REVOI) = how a system is KNOWN

Epistemic gap delta = 1 - mean(sigma_ii)
  delta~0.0  mature (physics, engineering)
  delta~0.6  emerging (early social sciences)
""".strip().split("\n")

# =============================================================================
# APPLICATION
# =============================================================================
class App:

    def __init__(self):
        pygame.init()
        self.screen=pygame.display.set_mode((WIN_W,WIN_H))
        pygame.display.set_caption("TSCG Explorer v2.1 — M2 GenericConcepts")
        self.clock=pygame.time.Clock()

        # UI fonts (normal)
        self.fB   = pygame.font.SysFont("Arial",13,bold=True)
        self.fN   = pygame.font.SysFont("Arial",12)
        self.fS   = pygame.font.SysFont("Arial",11)
        self.fXS  = pygame.font.SysFont("Arial",10)
        # README fonts (1.6x)
        self.fRB  = pygame.font.SysFont("Arial",21,bold=True)   # headers
        self.fRS  = pygame.font.SysFont("Arial",18,bold=True)   # sub-headers
        self.fRM  = pygame.font.SysFont("Courier New",16)       # body

        # State
        self.mode    = "A"
        self.sel     = None
        self.hov_net = None

        # Net pan/zoom
        self.zoom=1.0; self.pan_x=0.0; self.pan_y=0.0
        self._d0=None; self._p0=None

        # Tree
        self.fam_exp  = {f:True for f in FAMILY_ORDER}
        self.tree_scr = 0

        # Scroll for profile and readme
        self.prof_scr = 0
        self.read_scr = 0

        # Vertical splitters (x positions of the bar centres)
        self.spl_l = _INIT_TREE_W                    # between tree and net
        self.spl_r = _INIT_TREE_W + _INIT_NET_W      # between net and info
        self._dl   = False   # dragging left vertical splitter
        self._dr   = False   # dragging right vertical splitter

        # Horizontal splitter inside right panel
        self.spl_h   = int(CONTENT_H * 0.48)
        self._dh     = False

        self._pos={}; self._rebuild()

    # ── layout helpers ────────────────────────────────────────────────────────
    @property
    def tree_w(self): return self.spl_l - VSP_W//2
    @property
    def net_x(self):  return self.spl_l + VSP_W//2 + 1
    @property
    def net_w(self):  return self.spl_r - self.net_x - VSP_W//2
    @property
    def info_x(self): return self.spl_r + VSP_W//2 + 1
    @property
    def info_w(self): return WIN_W - self.info_x

    def _clamp_splitters(self):
        self.spl_l=max(MIN_TREE_W+VSP_W//2,
                       min(self.spl_l, self.spl_r-MIN_NET_W-VSP_W))
        self.spl_r=max(self.spl_l+MIN_NET_W+VSP_W,
                       min(self.spl_r, WIN_W-MIN_INFO_W-VSP_W//2))

    # ── positions ─────────────────────────────────────────────────────────────
    def _rebuild(self):
        mg=52; cw=self.net_w-2*mg; ch=CONTENT_H-2*mg
        for m,fn in [("A",pos_A),("B",pos_B),("C",pos_C)]:
            raw=fn(CONCEPTS)
            self._pos[m]=[(mg+nx*cw+jitter(ji,jt,13),
                           mg+(1-ny)*ch+jitter(ji+3,jt,13))
                          for nx,ny,ji,jt in raw]

    def c2s(self,cx,cy): return cx*self.zoom+self.pan_x, cy*self.zoom+self.pan_y
    def s2c(self,sx,sy): return (sx-self.pan_x)/self.zoom,(sy-self.pan_y)/self.zoom
    def nr(self,idx):    return max(7,5+len(CONCEPTS[idx]["dims"])*1.3)*min(self.zoom,1.6)

    def pick(self,sx,sy):
        cx,cy=self.s2c(sx,sy); best_i=None; best_d=1e9
        for i,(px,py) in enumerate(self._pos[self.mode]):
            d=math.hypot(cx-px,cy-py)
            if d<self.nr(i)/self.zoom+4 and d<best_d: best_d,best_i=d,i
        return best_i

    # ── grid ──────────────────────────────────────────────────────────────────
    def draw_grid(self):
        nx=self.net_x; nw=self.net_w
        s=max(1,int(60*self.zoom))
        ox=nx+int(self.pan_x%s); oy=int(self.pan_y%s)
        for x in range(ox,nx+nw,s):
            pygame.draw.line(self.screen,GRID_C,(x,0),(x,CONTENT_H))
        for y in range(oy,CONTENT_H,s):
            pygame.draw.line(self.screen,GRID_C,(nx,y),(nx+nw,y))

    # ── edges ─────────────────────────────────────────────────────────────────
    def draw_edges(self):
        nx=self.net_x; pos=self._pos[self.mode]
        clip=pygame.Rect(nx,0,self.net_w,CONTENT_H)
        self.screen.set_clip(clip)
        for i,c in enumerate(CONCEPTS):
            sx,sy=self.c2s(*pos[i]); sx+=nx
            if c["superclass"] and c["superclass"] in NAME_MAP:
                j=NAME_MAP[c["superclass"]]
                tx,ty=self.c2s(*pos[j]); tx+=nx
                pygame.draw.line(self.screen,EDGE_ISA,(int(sx),int(sy)),(int(tx),int(ty)),1)
            for cn in c["combo_of"]:
                if cn in NAME_MAP:
                    j=NAME_MAP[cn]; tx,ty=self.c2s(*pos[j]); tx+=nx
                    dashed(self.screen,EDGE_COMBO,(int(sx),int(sy)),(int(tx),int(ty)),7,4,1)
        self.screen.set_clip(None)

    # ── nodes ─────────────────────────────────────────────────────────────────
    def draw_nodes(self):
        nx=self.net_x; pos=self._pos[self.mode]
        clip=pygame.Rect(nx,0,self.net_w,CONTENT_H)
        self.screen.set_clip(clip)
        for p in (0,1):
            for i,c in enumerate(CONCEPTS):
                is_s=(i==self.sel); is_h=(i==self.hov_net)
                if p==0 and (is_s or is_h): continue
                if p==1 and not(is_s or is_h): continue
                sx,sy=self.c2s(*pos[i]); sx+=nx
                r=self.nr(i)
                ring=C_SEL if is_s else (C_HOV if is_h else None)
                draw_node(self.screen,c,int(sx),int(sy),r,ring)
                if self.zoom>0.65 or is_s or is_h:
                    nm=c["name"][:14]
                    lb=self.fXS.render(nm,True,C_TEXT)
                    self.screen.blit(lb,(int(sx)-lb.get_width()//2,int(sy)+int(r)+2))
        self.screen.set_clip(None)

    # ── legend ────────────────────────────────────────────────────────────────
    def draw_legend(self):
        nx=self.net_x; lx=nx+7; ly=8; sq=9; rh=sq+3
        bw=153; bh=16+len(FAMILY_ORDER)*rh+28
        bg=pygame.Surface((bw,bh),pygame.SRCALPHA)
        bg.fill((16,18,28,210))
        self.screen.blit(bg,(lx-3,ly-3))
        h=self.fXS.render("Family colours  (shape=type):",True,C_DIM)
        self.screen.blit(h,(lx,ly)); ly+=14
        for fam in FAMILY_ORDER:
            col=FAMILY_COLORS[fam]; cx2=lx+sq//2; cy2=ly+sq//2
            if fam=="Combo": dia(self.screen,col,cx2,cy2,sq//2+1)
            else:            tri(self.screen,col,cx2,cy2,sq//2+1)
            cnt=sum(1 for c in CONCEPTS if c["family"]==fam)
            t=self.fXS.render(f"{fam} ({cnt})",True,C_TEXT)
            self.screen.blit(t,(lx+sq+4,ly-1)); ly+=rh
        ly+=3
        pygame.draw.line(self.screen,EDGE_ISA,(lx,ly),(lx+20,ly),1)
        self.screen.blit(self.fXS.render("IS-A",True,C_DIM),(lx+23,ly-4)); ly+=10
        dashed(self.screen,EDGE_COMBO,(lx,ly),(lx+20,ly),5,3,1)
        self.screen.blit(self.fXS.render("Combo component",True,C_DIM),(lx+23,ly-4))

    # ── mode buttons ──────────────────────────────────────────────────────────
    def draw_modes(self):
        nx=self.net_x; nw=self.net_w
        bw,bh,gap=30,20,4
        bx=nx+nw//2-(3*bw+2*gap)//2; by=6
        for mi,m in enumerate(["A","B","C"]):
            r=pygame.Rect(bx+mi*(bw+gap),by,bw,bh)
            pygame.draw.rect(self.screen,BTN_ON if self.mode==m else BTN_OFF,r,border_radius=4)
            lb=self.fS.render(m,True,C_TEXT)
            self.screen.blit(lb,(r.centerx-lb.get_width()//2,r.centery-lb.get_height()//2))
        desc={"A":"ASFID ratio x Dims","B":"Family x Dims","C":"ASFID ct x REVOI ct"}
        d=self.fXS.render(desc[self.mode],True,C_DIM)
        self.screen.blit(d,(nx+nw//2-d.get_width()//2,by+bh+2))

    def check_mode_btn(self,mx,my):
        nx=self.net_x; nw=self.net_w
        bw,bh,gap=30,20,4
        bx=nx+nw//2-(3*bw+2*gap)//2; by=6
        for mi,m in enumerate(["A","B","C"]):
            if pygame.Rect(bx+mi*(bw+gap),by,bw,bh).collidepoint(mx,my): return m
        return None

    # ── axis labels ───────────────────────────────────────────────────────────
    def draw_axis(self):
        nx=self.net_x; nw=self.net_w
        labs={"A":("ASFID ratio (0=Map  1=Territory)","Dimensionality (1-8D)"),
              "B":("Family (Structural -> Combo)","Dimensionality (1-8D)"),
              "C":("ASFID dimension count (0-5)","REVOI dimension count (0-5)")}
        xl,yl=labs[self.mode]
        xs=self.fXS.render(xl,True,AXIS_C)
        ys=self.fXS.render(yl,True,AXIS_C)
        yr=pygame.transform.rotate(ys,90)
        self.screen.blit(xs,(nx+nw//2-xs.get_width()//2,CONTENT_H-13))
        self.screen.blit(yr,(nx+3,CONTENT_H//2-yr.get_height()//2))

    # ── tree panel ────────────────────────────────────────────────────────────
    def draw_tree(self):
        tw=self.tree_w
        pygame.draw.rect(self.screen,PANEL_BG,(0,0,tw,CONTENT_H))
        hdr=self.fB.render("M2 GenericConcepts",True,C_HIGH)
        self.screen.blit(hdr,(6,4))
        pygame.draw.line(self.screen,BORDER,(0,20),(tw,20))

        rows=flatten_tree(TREE_ROOTS,self.fam_exp)
        self._rows=rows
        clip=pygame.Rect(0,21,tw-6,CONTENT_H-21)
        self.screen.set_clip(clip)
        mx,my=pygame.mouse.get_pos()
        y=21-self.tree_scr

        for row in rows:
            ry=y; y+=ROW_H
            if ry+ROW_H<21 or ry>CONTENT_H: continue
            rr=pygame.Rect(0,ry,tw,ROW_H)
            if row[0]=="F":
                fam=row[1]; hov=rr.collidepoint(mx,my)
                if hov: pygame.draw.rect(self.screen,TREE_HOV_C,rr)
                col=FAMILY_COLORS[fam]
                arr="▾" if self.fam_exp.get(fam,True) else "▸"
                self.screen.blit(self.fXS.render(arr,True,C_DIM),(3,ry+2))
                pygame.draw.circle(self.screen,col,(17,ry+ROW_H//2),4)
                cnt=sum(1 for c in CONCEPTS if c["family"]==fam)
                self.screen.blit(self.fS.render(f"{fam} ({cnt})",True,col),(23,ry+2))
            elif row[0]=="C":
                _,idx,depth,has_ch,node=row
                c=CONCEPTS[idx]; is_s=(idx==self.sel); is_h=rr.collidepoint(mx,my)
                bg=TREE_SEL_C if is_s else (TREE_HOV_C if is_h else None)
                if bg: pygame.draw.rect(self.screen,bg,rr)
                ind=12+depth*9; col=FAMILY_COLORS.get(c["family"],(160,160,160))
                if has_ch:
                    arr="▾" if node.expanded else "▸"
                    self.screen.blit(self.fXS.render(arr,True,C_DIM),(ind-8,ry+2))
                sr=4; scx=ind+sr+1; scy=ry+ROW_H//2
                if is_combo(c): dia(self.screen,col,scx,scy,sr)
                else:           tri(self.screen,col,scx,scy,sr)
                max_c=max(4,(tw-ind-18)//6)
                nm=c["name"] if len(c["name"])<=max_c else c["name"][:max_c-1]+"…"
                tc=C_HIGH if is_s else C_TEXT
                self.screen.blit(self.fXS.render(nm,True,tc),(ind+sr*2+4,ry+2))

        self.screen.set_clip(None)
        total=len(rows)*ROW_H
        scrollbar_draw(self.screen,pygame.Rect(0,21,tw,CONTENT_H-21),self.tree_scr,total+21)

    # ── tensor formula: tiles + ⊗ as circle-cross ─────────────────────────────
    def draw_formula(self,surf,dims,x,y,sq=13):
        """Draw dimension tiles separated by ⊗ (circle+cross) operators."""
        cx=x; r_op=4   # radius of ⊗ circle
        for i,d in enumerate(dims):
            col=DIM_COL.get(d,(100,100,100))
            pygame.draw.rect(surf,col,(cx,y,sq,sq),border_radius=2)
            lb=self.fXS.render(DIM_LBL.get(d,d),True,(255,255,255))
            surf.blit(lb,(cx+sq//2-lb.get_width()//2,y+sq//2-lb.get_height()//2))
            cx+=sq
            if i<len(dims)-1:
                # ⊗ operator: circle with cross, centred between tiles
                op_cx=cx+r_op+3; op_cy=y+sq//2
                otimes(surf,op_cx,op_cy,r_op,C_DIM)
                cx+=r_op*2+7
        return cx

    # ── profile panel ─────────────────────────────────────────────────────────
    def draw_profile(self):
        ix=self.info_x; iw=self.info_w; ph=self.spl_h
        pygame.draw.rect(self.screen,PANEL_BG,(ix,0,iw,ph))
        pygame.draw.line(self.screen,BORDER,(ix,0),(ix,CONTENT_H))
        hdr=self.fB.render("Concept Profile",True,C_DIM)
        self.screen.blit(hdr,(ix+PAD,4))
        pygame.draw.line(self.screen,BORDER,(ix,19),(WIN_W,19))

        clip=pygame.Rect(ix,20,iw,ph-20)
        self.screen.set_clip(clip)

        if self.sel is None:
            msg=self.fS.render("Click a node or tree row to inspect.",True,C_DIM)
            self.screen.blit(msg,(ix+PAD,30))
            self.screen.set_clip(None); return

        c=CONCEPTS[self.sel]; col=FAMILY_COLORS.get(c["family"],(160,160,160))
        a,r=dc(c["dims"]); t=len(c["dims"])

        pw=iw-16; surf_h=900
        ps=pygame.Surface((pw,surf_h),pygame.SRCALPHA)
        ps.fill((0,0,0,0))
        py=4; lh=17

        def row(label,val,vc=C_TEXT):
            nonlocal py
            lb=self.fS.render(label+":",True,C_DIM); ps.blit(lb,(0,py))
            vl=self.fN.render(str(val),True,vc); ps.blit(vl,(92,py)); py+=lh

        def sep():
            nonlocal py
            pygame.draw.line(ps,BORDER,(0,py+2),(pw-10,py+2)); py+=8

        pygame.draw.circle(ps,col,(8,py+8),6)
        ps.blit(self.fB.render(c["name"],True,C_HIGH),(18,py)); py+=lh+2
        sep()

        row("Family",c["family"],col)
        shape="◆ GenericConceptCombo" if is_combo(c) else "▲ Atomic concept"
        row("Type",shape,C_DIM)
        if c["abstract"]: row("Abstract","yes (no formula)",C_DIM)
        sep()

        # Formula tiles with ⊗ circle-cross operators
        ps.blit(self.fS.render("Formula:",True,C_DIM),(0,py)); py+=lh
        if c["dims"]:
            self.draw_formula(ps,c["dims"],4,py); py+=18
            fs=" ⊗ ".join(c["dims"])
            ps.blit(self.fXS.render(fs,True,C_DIM),(4,py)); py+=lh
        else:
            ps.blit(self.fS.render("(abstract — no tensor formula)",True,C_DIM),(4,py)); py+=lh
        sep()

        ps.blit(self.fB.render("Dimensions:",True,C_TEXT),(0,py)); py+=lh
        row("  Total",t)
        row("  ASFID (Territory)",a,(120,180,255))
        row("  REVOI (Map)",r,(255,170,120))
        if t: row("  ASFID ratio",f"{a/t:.2f}",C_DIM)
        sep()

        if c["superclass"]:
            ps.blit(self.fB.render("IS-A (subClassOf):",True,C_TEXT),(0,py)); py+=lh
            sc=FAMILY_COLORS.get(CONCEPTS[NAME_MAP[c["superclass"]]]["family"],C_DIM) \
               if c["superclass"] in NAME_MAP else C_DIM
            ps.blit(self.fN.render("→  "+c["superclass"],True,sc),(4,py)); py+=lh
            sep()

        if c["combo_of"]:
            ps.blit(self.fB.render("⊗⇒ Assembly of:",True,C_TEXT),(0,py)); py+=lh
            for comp in c["combo_of"]:
                ci2=NAME_MAP.get(comp)
                cc2=FAMILY_COLORS.get(CONCEPTS[ci2]["family"],(160,160,160)) \
                    if ci2 is not None else C_DIM
                ps.blit(self.fN.render("•  "+comp,True,cc2),(4,py)); py+=lh
            sep()

        subs=[CONCEPTS[i]["name"] for i,cc3 in enumerate(CONCEPTS)
              if cc3["superclass"]==c["name"]]
        if subs:
            ps.blit(self.fB.render(f"Subclasses ({len(subs)}):",True,C_TEXT),(0,py)); py+=lh
            for s in subs:
                sc2=FAMILY_COLORS.get(CONCEPTS[NAME_MAP[s]]["family"],C_DIM)
                ps.blit(self.fN.render("•  "+s,True,sc2),(4,py)); py+=lh
            sep()

        used=[CONCEPTS[i]["name"] for i,cc4 in enumerate(CONCEPTS)
              if c["name"] in cc4["combo_of"]]
        if used:
            ps.blit(self.fB.render("Used in Combos:",True,C_TEXT),(0,py)); py+=lh
            for u in used:
                uc=FAMILY_COLORS.get(CONCEPTS[NAME_MAP[u]]["family"],C_DIM)
                ps.blit(self.fN.render("◆  "+u,True,uc),(4,py)); py+=lh
            sep()

        contracts=[]
        if a>=1: contracts.append("Observable")
        if any(d in c["dims"] for d in ["A","D"]): contracts.append("Triggerable")
        if any(d in c["dims"] for d in ["S","Im"]): contracts.append("Composable")
        if "I" in c["dims"] or "It" in c["dims"]: contracts.append("Stateful")
        if contracts:
            ps.blit(self.fB.render("ConceptContracts (heuristic):",True,C_TEXT),(0,py)); py+=lh
            ps.blit(self.fN.render("  "+" · ".join(contracts),True,(180,210,255)),(0,py)); py+=lh

        total_ph=py
        scr=max(0,min(self.prof_scr,max(0,total_ph-(ph-24))))
        self.prof_scr=scr
        self.screen.blit(ps,(ix+PAD,21-scr))
        self.screen.set_clip(None)
        scrollbar_draw(self.screen,pygame.Rect(ix,20,iw,ph-20),scr,total_ph)

    # ── horizontal splitter (inside right panel) ───────────────────────────────
    def draw_hsplitter(self):
        ix=self.info_x; iw=self.info_w; sy=self.spl_h
        mx,my=pygame.mouse.get_pos()
        hov=(mx>=ix and abs(my-sy)<7)
        col=SPL_HH if(hov or self._dh) else SPL_HC
        pygame.draw.rect(self.screen,col,(ix,sy-2,iw,HSP_H))
        for dx in range(-14,15,5):
            pygame.draw.circle(self.screen,(115,128,162),(ix+iw//2+dx,sy+1),1)

    # ── readme panel (1.6x fonts, line height 21) ─────────────────────────────
    def draw_readme(self):
        ix=self.info_x; iw=self.info_w
        ry=self.spl_h+HSP_H+1; rh=CONTENT_H-ry
        if rh<10: return
        pygame.draw.rect(self.screen,(21,24,37),(ix,ry,iw,rh))
        hdr=self.fB.render("README",True,C_DIM)
        self.screen.blit(hdr,(ix+PAD,ry+3))
        pygame.draw.line(self.screen,BORDER,(ix,ry+18),(WIN_W,ry+18))

        clip=pygame.Rect(ix,ry+20,iw-6,rh-20)
        self.screen.set_clip(clip)

        lh=21   # 1.6x line height (was 13)
        total=len(README)*lh
        scr=max(0,min(self.read_scr,max(0,total-(rh-22))))
        self.read_scr=scr
        y=ry+20-scr

        for line in README:
            if y+lh>ry+20 and y<ry+rh:
                if line.startswith("# "):
                    col,f,t=C_HIGH,self.fRB,line[2:]
                elif line.startswith("## "):
                    col,f,t=(140,200,255),self.fRS,line[3:]
                elif line.startswith("  "):
                    col,f,t=C_DIM,self.fRM,line
                else:
                    col,f,t=C_TEXT,self.fRM,line
                self.screen.blit(f.render(t[:55],True,col),(ix+PAD,y))
            y+=lh

        self.screen.set_clip(None)
        scrollbar_draw(self.screen,pygame.Rect(ix,ry+20,iw,rh-20),scr,total)

    # ── vertical splitters ────────────────────────────────────────────────────
    def draw_vsplitters(self):
        mx,my=pygame.mouse.get_pos()
        vsplitter_draw(self.screen,self.spl_l,CONTENT_H,
                       abs(mx-self.spl_l)<5 or self._dl)
        vsplitter_draw(self.screen,self.spl_r,CONTENT_H,
                       abs(mx-self.spl_r)<5 or self._dr)

    # ── status bar ────────────────────────────────────────────────────────────
    def draw_status(self):
        y=CONTENT_H
        pygame.draw.rect(self.screen,STATUS_C,(0,y,WIN_W,STATUS_H))
        pygame.draw.line(self.screen,BORDER,(0,y),(WIN_W,y))
        modes={"A":"A: ASFID ratio x Dims","B":"B: Family x Dims","C":"C: ASFID ct x REVOI ct"}
        t=f"Mode {modes[self.mode]}  |  81 GenericConcepts · 10 families  |  [A][B][C] · Wheel zoom · Drag pan · Drag splitters · ESC"
        self.screen.blit(self.fXS.render(t,True,C_DIM),(8,y+8))

    # ── main draw ─────────────────────────────────────────────────────────────
    def draw(self):
        self.screen.fill(BG)
        # Net panel background
        pygame.draw.rect(self.screen,PANEL_BG,(self.net_x,0,self.net_w,CONTENT_H))
        self.draw_grid()
        self.draw_edges()
        self.draw_nodes()
        self.draw_legend()
        self.draw_axis()
        self.draw_modes()
        # Panels
        self.draw_tree()
        self.draw_profile()
        self.draw_hsplitter()
        self.draw_readme()
        # Vertical splitters drawn last (on top)
        self.draw_vsplitters()
        self.draw_status()
        pygame.display.flip()

    # ── events ────────────────────────────────────────────────────────────────
    def handle(self):
        mx,my=pygame.mouse.get_pos()
        in_net  = self.net_x<=mx<self.net_x+self.net_w and my<CONTENT_H
        in_tree = mx<self.tree_w and my>20 and my<CONTENT_H
        in_prof = mx>=self.info_x and my<self.spl_h
        in_read = mx>=self.info_x and my>self.spl_h+HSP_H

        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: return False

            if ev.type==pygame.KEYDOWN:
                if ev.key==pygame.K_ESCAPE: return False
                if ev.key==pygame.K_a: self.mode="A"; self._rebuild()
                if ev.key==pygame.K_b: self.mode="B"; self._rebuild()
                if ev.key==pygame.K_c: self.mode="C"; self._rebuild()

            elif ev.type==pygame.MOUSEBUTTONDOWN and ev.button==1:
                # Vertical splitters have priority
                if abs(mx-self.spl_l)<6 and my<CONTENT_H:
                    self._dl=True
                elif abs(mx-self.spl_r)<6 and my<CONTENT_H:
                    self._dr=True
                # Horizontal splitter
                elif mx>=self.info_x and abs(my-self.spl_h)<8:
                    self._dh=True
                elif in_net:
                    m=self.check_mode_btn(mx,my)
                    if m:
                        self.mode=m; self._rebuild()
                    else:
                        idx=self.pick(mx-self.net_x,my)
                        if idx is not None: self.sel=idx; self.prof_scr=0
                        self._d0=(mx,my); self._p0=(self.pan_x,self.pan_y)
                elif in_tree:
                    self._tree_click(mx,my)

            elif ev.type==pygame.MOUSEBUTTONDOWN:
                if ev.button==4:
                    if in_net:    self._zoom(mx,my,1.1)
                    elif in_prof: self.prof_scr=max(0,self.prof_scr-22)
                    elif in_read: self.read_scr=max(0,self.read_scr-22)
                    elif in_tree: self.tree_scr=max(0,self.tree_scr-ROW_H*2)
                elif ev.button==5:
                    if in_net:    self._zoom(mx,my,1/1.1)
                    elif in_prof: self.prof_scr+=22
                    elif in_read: self.read_scr+=22
                    elif in_tree: self.tree_scr+=ROW_H*2

            elif ev.type==pygame.MOUSEBUTTONUP and ev.button==1:
                self._dl=False; self._dr=False; self._dh=False; self._d0=None

            elif ev.type==pygame.MOUSEMOTION:
                if self._dl:
                    self.spl_l=mx; self._clamp_splitters(); self._rebuild()
                elif self._dr:
                    self.spl_r=mx; self._clamp_splitters(); self._rebuild()
                elif self._dh:
                    self.spl_h=max(MIN_ZONE_H,min(CONTENT_H-MIN_ZONE_H-HSP_H,my))
                elif self._d0:
                    dx=mx-self._d0[0]; dy=my-self._d0[1]
                    if abs(dx)>2 or abs(dy)>2:
                        self.pan_x=self._p0[0]+dx; self.pan_y=self._p0[1]+dy
                self.hov_net=self.pick(mx-self.net_x,my) if in_net else None

        return True

    def _tree_click(self,mx,my):
        rows=flatten_tree(TREE_ROOTS,self.fam_exp)
        y=21-self.tree_scr
        for row in rows:
            if y<=my<y+ROW_H:
                if row[0]=="F":
                    fam=row[1]; self.fam_exp[fam]=not self.fam_exp.get(fam,True)
                elif row[0]=="C":
                    _,idx,depth,has_ch,node=row
                    if has_ch and mx<12+depth*9:
                        node.expanded=not node.expanded
                    else:
                        self.sel=idx; self.prof_scr=0
                break
            y+=ROW_H

    def _zoom(self,mx,my,f):
        nx=self.net_x; lx=mx-nx
        cx=(lx-self.pan_x)/self.zoom; cy=(my-self.pan_y)/self.zoom
        self.zoom=max(0.2,min(4.0,self.zoom*f))
        self.pan_x=lx-cx*self.zoom; self.pan_y=my-cy*self.zoom

    def run(self):
        running=True
        while running: running=self.handle(); self.draw(); self.clock.tick(FPS)
        pygame.quit(); sys.exit()

if __name__=="__main__":
    App().run()
