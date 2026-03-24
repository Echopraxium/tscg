"""
transistor_sim.py  v2.0
========================
TSCG Poclet Simulation – BJT NPN + MOSFET NMOS
Author: Echopraxium with the collaboration of Claude AI

Device-selector tab switches between two semiconductor devices, each with
its own sliders, I-V characteristic curves, animated schematic, and a
colour-coded operating-mode table.

BJT NPN  – 4 modes: Cutoff | Forward Active | Saturation | Reverse Active
MOSFET   – 3 modes: Cutoff | Triode/Linear  | Saturation (= amplifier!)

Key educational point encoded in the colour scheme:
  Both "amplifier" modes share BLUE  → BJT Forward Active = MOSFET Saturation
  BJT Saturation (switch ON) = ORANGE, MOSFET Triode (switch ON) = GREEN
  ⚠  same word "Saturation", opposite functions — highlighted by warning banner

Requirements:  pip install pygame numpy
Run:
    python transistor_sim.py
    python transistor_sim.py path/to/M0_Transistor.jsonld
"""

import sys, math, json
from pathlib import Path
import pygame

# ─────────────────────────────────────────────────────────────────────────────
# Window / layout
# ─────────────────────────────────────────────────────────────────────────────
WINDOW_W, WINDOW_H  = 1260, 740
FPS                  = 60
POCLET_OVERRIDE      = sys.argv[1] if len(sys.argv) > 1 else None

LEFT_W   = 300
RIGHT_W  = 230
MID_W    = WINDOW_W - LEFT_W - RIGHT_W   # 730
PAD      = 12

# ─────────────────────────────────────────────────────────────────────────────
# Colour palette
# ─────────────────────────────────────────────────────────────────────────────
BG          = (12,  12,  18)
PANEL_BG    = (22,  22,  32)
BORDER      = (55,  55,  75)
TEXT        = (220, 220, 230)
DIM         = (130, 130, 150)
GOLD        = (255, 200,  50)
GREEN_OK    = ( 80, 200, 120)
RED_WARN    = (220,  60,  60)
SLIDER_BG   = ( 38,  38,  52)
REVOI_COL   = (120, 180, 255)

# Operating-mode colours (functional: amplifier = blue in BOTH devices)
C_CUTOFF   = ( 80,  80, 112)    # gray-purple  – OFF
C_ACTIVE   = ( 64, 128, 255)    # blue         – AMPLIFIER (BJT Active = MOSFET Sat)
C_SAT_BJT  = (255, 140,   0)    # orange       – BJT switch ON  (NOT amplifier!)
C_TRIODE   = ( 80, 200, 120)    # green        – MOSFET switch ON / resistive
C_REVERSE  = (144,  64, 192)    # purple       – BJT reverse active (rare)

# Parameter slider accent colours
IB_COL, VCE_COL, BETA_COL = ( 80,210,210), (255,175, 45), (200,110,255)
VGS_COL, VDS_COL, VTH_COL = ( 80,210,150), (255,175, 45), (255,100,100)

# Curve palette for reference I-V lines
CURVE_PAL = [
    (255,100,100),(255,165,60),(255,220,60),
    (130,220,130),(80,200,220),(120,160,255),(200,130,255),
]

# ─────────────────────────────────────────────────────────────────────────────
# BJT physics  (NPN)
# ─────────────────────────────────────────────────────────────────────────────
VCE_SAT  = 0.2
VCE_MAX  = 20.0
IB_MAX   = 100.0
BETA_MIN, BETA_MAX = 50.0, 500.0
IB_REFS  = [10, 20, 30, 40, 60, 80, 100]   # μA

def bjt_ic(ib_uA, vce_V, beta):
    if ib_uA < 1.0:
        return 0.0
    ic_act = beta * ib_uA / 1000.0
    if vce_V < VCE_SAT:
        return ic_act * (vce_V / VCE_SAT) * 0.9
    return ic_act * (1.0 + vce_V / 80.0)

def bjt_region(ib_uA, vce_V):
    if ib_uA < 1.0:   return "Cutoff"
    if vce_V < VCE_SAT: return "Saturation"
    return "Forward Active"

BJT_MODES = [
    # (label, color, short condition, note/analogy)
    ("Cutoff",         C_CUTOFF,  "V_BE < 0.6 V  –  I_C ≈ 0",           "Open switch"),
    ("Forward Active", C_ACTIVE,  "V_BE≈0.7V, V_CE>0.2V  –  I_C=β·I_B", "Amplifier (proportional)"),
    ("Saturation",     C_SAT_BJT, "V_CE≈0.2V  –  fully ON, I_C max",     "Closed switch"),
    ("Reverse Active", C_REVERSE, "V_BC≈0.7V  –  low β, rare",           "Backwards (inefficient)"),
]

def bjt_region_col(r):
    return {"Cutoff":C_CUTOFF,"Forward Active":C_ACTIVE,
            "Saturation":C_SAT_BJT,"Reverse Active":C_REVERSE}.get(r,C_CUTOFF)

# ─────────────────────────────────────────────────────────────────────────────
# MOSFET physics  (NMOS enhancement)
# ─────────────────────────────────────────────────────────────────────────────
VGS_MAX  = 5.0
VDS_MAX  = 10.0
VTH_MIN, VTH_MAX = 0.5, 3.0
KN       = 1.5    # mA/V²
VGS_REFS = [1.0,1.5,2.0,2.5,3.0,3.5,4.0]  # ΔV above V_th

def mosfet_id(vgs_V, vds_V, vth_V):
    vov = vgs_V - vth_V
    if vov <= 0: return 0.0
    if vds_V < vov:
        return KN * (vov*vds_V - 0.5*vds_V**2)
    return 0.5 * KN * vov**2

def mosfet_region(vgs_V, vds_V, vth_V):
    vov = vgs_V - vth_V
    if vov <= 0:    return "Cutoff"
    if vds_V < vov: return "Triode"
    return "Saturation"

MOSFET_MODES = [
    ("Cutoff",           C_CUTOFF, "V_GS < V_th  –  I_D = 0",                    "Open switch"),
    ("Triode / Linear",  C_TRIODE, "V_DS < V_GS−V_th  –  V-ctrl resistor",        "Closed switch (ON)"),
    ("Saturation (Amp)", C_ACTIVE, "V_DS ≥ V_GS−V_th  –  I_D = k_n/2·V_ov²",    "Amplifier ← same as BJT Active!"),
]

def mosfet_region_col(r):
    return {"Cutoff":C_CUTOFF,"Triode":C_TRIODE,"Saturation":C_ACTIVE}.get(r,C_CUTOFF)

NAMING_WARN = ("⚠  'Saturation' means OPPOSITE things:  "
               "BJT Sat. = switch ON (orange)  |  MOSFET Sat. = amplifier (blue)  "
               "—  BJT Active ↔ MOSFET Saturation  (both amplifiers, both blue)")

# ─────────────────────────────────────────────────────────────────────────────
# Mode presets  — typical slider values for each operating mode
# Clicking a mode row snaps sliders to these values
# ─────────────────────────────────────────────────────────────────────────────
# BJT: (I_B μA, V_CE V, β)
BJT_PRESETS = {
    "Cutoff":         ( 0.0,  10.0, 150.0),
    "Forward Active": (40.0,   5.0, 150.0),
    "Saturation":     (80.0,   0.1, 150.0),
    "Reverse Active": ( 0.5,   0.5,  20.0),   # very low β in reverse
}
# MOSFET: (V_GS V, V_DS V, V_th V)
MOSFET_PRESETS = {
    "Cutoff":           (0.3, 5.0, 1.0),
    "Triode":           (3.0, 0.5, 1.0),
    "Saturation":       (3.0, 5.0, 1.0),
}

# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────
def clamp(v, lo=0.0, hi=1.0):
    return max(lo, min(hi, v))

# ─────────────────────────────────────────────────────────────────────────────
# Slider widget
# ─────────────────────────────────────────────────────────────────────────────
class Slider:
    def __init__(self, x, y, w, vmin, vmax, init, label, unit, color):
        self.rect = pygame.Rect(x, y, w, 20)
        self.vmin, self.vmax = float(vmin), float(vmax)
        self.value = float(init)
        self.label, self.unit, self.color = label, unit, color
        self.dragging = False

    @property
    def ratio(self): return (self.value-self.vmin)/(self.vmax-self.vmin)
    @property
    def hx(self): return int(self.rect.x + self.ratio*self.rect.w)

    def handle_event(self, e):
        cy = self.rect.centery
        if e.type == pygame.MOUSEBUTTONDOWN and e.button==1:
            if math.hypot(e.pos[0]-self.hx, e.pos[1]-cy) < 15:
                self.dragging = True
        elif e.type == pygame.MOUSEBUTTONUP: self.dragging = False
        elif e.type == pygame.MOUSEMOTION and self.dragging:
            r = (e.pos[0]-self.rect.x)/max(self.rect.w,1)
            self.value = clamp(self.vmin+r*(self.vmax-self.vmin),self.vmin,self.vmax)

    def draw(self, surf, font_sm, val_str=None):
        cy = self.rect.centery
        if val_str is None: val_str = f"{self.value:.2f} {self.unit}"
        pygame.draw.rect(surf,SLIDER_BG,(self.rect.x,cy-3,self.rect.w,6),border_radius=3)
        fw=int(self.ratio*self.rect.w)
        if fw>0: pygame.draw.rect(surf,self.color,(self.rect.x,cy-3,fw,6),border_radius=3)
        pygame.draw.circle(surf,self.color,(self.hx,cy),10)
        pygame.draw.circle(surf,TEXT,(self.hx,cy),10,1)
        surf.blit(font_sm.render(self.label,True,TEXT),(self.rect.x,self.rect.y-20))
        v=font_sm.render(val_str,True,self.color)
        surf.blit(v,(self.rect.right-v.get_width(),self.rect.y-20))

# ─────────────────────────────────────────────────────────────────────────────
# Mode-table panel  (clickable rows)
# ─────────────────────────────────────────────────────────────────────────────
def draw_mode_table(surf, x, y, w, modes, active_label, hover_label,
                    font_sm, font_xs):
    """
    Draws mode rows. Active row glows. Hovered row highlighted.
    Returns list of (pygame.Rect, label_str) for click hit-testing.
    """
    row_h  = 40
    gap    = 3
    rects  = []

    for lbl, col, cond, note in modes:
        is_active = (active_label in lbl or lbl.startswith(active_label))
        is_hover  = (hover_label  in lbl or lbl.startswith(hover_label)) \
                     if hover_label else False
        row_rect  = pygame.Rect(x, y, w, row_h)
        rects.append((row_rect, lbl))

        # Background
        bg_a   = 70 if is_active else (38 if is_hover else 18)
        bord_a = 220 if is_active else (140 if is_hover else 45)
        bg = pygame.Surface((w, row_h), pygame.SRCALPHA)
        bg.fill((*col, bg_a))
        pygame.draw.rect(bg, (*col, bord_a), (0, 0, w, row_h), 2, border_radius=5)
        surf.blit(bg, (x, y))

        # Colour badge
        bcol = col if (is_active or is_hover) else tuple(c // 4 for c in col)
        pygame.draw.rect(surf, bcol, (x+5, y+8, 6, row_h-16), border_radius=3)

        # "▶ Click" hint on hover (not already active)
        if is_hover and not is_active:
            hint = font_xs.render("▶ click to apply", True, (*col, 200))
            surf.blit(hint, (x + w - hint.get_width() - 6, y + row_h - 14))

        # Text
        tcol = TEXT if (is_active or is_hover) else DIM
        surf.blit(font_sm.render(lbl,  True, bcol), (x+16, y+3))
        surf.blit(font_xs.render(cond, True, tcol), (x+16, y+21))

        y += row_h + gap

    return rects

# ─────────────────────────────────────────────────────────────────────────────
# Bar / panel helpers
# ─────────────────────────────────────────────────────────────────────────────
def draw_bar(surf, x, y, w, h, val, col):
    pygame.draw.rect(surf,SLIDER_BG,(x,y,w,h),border_radius=3)
    fw=int(clamp(val)*w)
    if fw>0: pygame.draw.rect(surf,col,(x,y,fw,h),border_radius=3)

def draw_panel_bg(surf, rect, title, font_md):
    pygame.draw.rect(surf,PANEL_BG,rect,border_radius=8)
    pygame.draw.rect(surf,BORDER,rect,1,border_radius=8)
    y=rect.y+PAD
    if title:
        t=font_md.render(title,True,GOLD); surf.blit(t,(rect.x+PAD,y))
        y+=t.get_height()+4
    return y

def draw_asfid(surf, rect, live, base, font_md, font_sm, font_xs):
    y=draw_panel_bg(surf,rect,"ASFID  (Eagle Eye · Territory)",font_md)
    x=rect.x+PAD; bw=rect.w-PAD*2-38
    for d,lv,bv,col in zip("ASFID",live,base,
        [(255,180,60),(100,200,255),(60,200,160),(200,130,255),(255,100,100)]):
        surf.blit(font_sm.render(d,True,col),(x,y+1))
        draw_bar(surf,x+22,y,bw,14,lv,col)
        bx=x+22+int(bv*bw); pygame.draw.line(surf,(200,200,200),(bx,y),(bx,y+14),1)
        surf.blit(font_xs.render(f"{lv:.2f}",True,col),(x+22+bw+4,y)); y+=22

def draw_revoi(surf, rect, revoi, font_md, font_sm, font_xs):
    y=draw_panel_bg(surf,rect,"REVOI  (Sphinx Eye · Map)",font_md)
    x=rect.x+PAD; bw=rect.w-PAD*2-38
    cols=[(100,180,255),(180,255,120),(255,220,80),(255,130,200),(130,220,255)]
    for d,v,col in zip("REVOI",revoi,cols):
        surf.blit(font_sm.render(d,True,col),(x,y+1))
        draw_bar(surf,x+22,y,bw,14,v,col)
        surf.blit(font_xs.render(f"{v:.2f}",True,col),(x+22+bw+4,y)); y+=22
    surf.blit(font_xs.render(f"mean = {sum(revoi)/5:.2f}",True,REVOI_COL),(x,y+2))

def draw_status(surf, rect, device, region, val_lines, font_md, font_sm, font_xs):
    y=draw_panel_bg(surf,rect,"Status",font_md); x=rect.x+PAD
    rcol=bjt_region_col(region) if device=="BJT" else mosfet_region_col(region)
    surf.blit(font_sm.render(f"Device: {device}",True,GOLD),(x,y)); y+=16
    surf.blit(font_sm.render(f"Region: {region}",True,rcol),(x,y)); y+=18
    for lbl,col in val_lines:
        surf.blit(font_sm.render(lbl,True,col),(x,y)); y+=15
    y+=4
    eqs=["I_C=β·I_B  (active)","P_D=V_CE·I_C"] if device=="BJT" else \
        ["I_D=k_n/2·V_ov²  (sat.)","I_D=k_n·(V_ov·V_DS-V_DS²/2)","  (triode)","P_D=V_DS·I_D"]
    for eq in eqs:
        surf.blit(font_xs.render(eq,True,DIM),(x,y)); y+=13
    y+=4
    surf.blit(font_xs.render("Metaconcepts: 11 | ΔΘ=0.01",True,DIM),(x,y))

# ─────────────────────────────────────────────────────────────────────────────
# I-V characteristic plane
# ─────────────────────────────────────────────────────────────────────────────
def iv_px(v, i, xmax, ymax, pr):
    px = pr.x + int(v/xmax * pr.w)
    py = pr.bottom - int(clamp(i/ymax)*pr.h)
    return px, py

def draw_axes(surf, pr, xmax, ymax, xlabel, ylabel, font_xs):
    pygame.draw.rect(surf,(18,18,26),pr)
    pygame.draw.rect(surf,BORDER,pr,1)
    for i in range(1,5):
        gx=pr.x+int(i/5*pr.w); pygame.draw.line(surf,(30,30,42),(gx,pr.y),(gx,pr.bottom))
        gy=pr.y+int((1-i/5)*pr.h); pygame.draw.line(surf,(30,30,42),(pr.x,gy),(pr.right,gy))
    for i in range(5):
        v=xmax*i/4; px=pr.x+int(i/4*pr.w)
        surf.blit(font_xs.render(f"{v:.0f}",True,DIM),(px-8,pr.bottom+3))
    surf.blit(font_xs.render(xlabel,True,VCE_COL),(pr.x+pr.w//2-20,pr.bottom+17))
    for i in range(5):
        iy=ymax*i/4; py=pr.bottom-int(i/4*pr.h)
        surf.blit(font_xs.render(f"{iy:.0f}",True,DIM),(pr.x-30,py-5))
    surf.blit(font_xs.render(ylabel,True,IB_COL),(pr.x-28,pr.y-14))

def draw_qpoint(surf, qx, qy, rcol, label, pr, font_xs):
    pygame.draw.line(surf,(*rcol,80),(pr.x,qy),(pr.right,qy),1)
    pygame.draw.line(surf,(*rcol,80),(qx,pr.y),(qx,pr.bottom),1)
    for r in [13,9,6]:
        s=pygame.Surface((r*2,r*2),pygame.SRCALPHA)
        pygame.draw.circle(s,(*rcol,30+r*8),(r,r),r); surf.blit(s,(qx-r,qy-r))
    pygame.draw.circle(surf,rcol,(qx,qy),7)
    pygame.draw.circle(surf,TEXT,(qx,qy),7,1)
    lbl=font_xs.render(label,True,rcol)
    surf.blit(lbl,(min(qx+10,pr.right-lbl.get_width()-2),max(qy-17,pr.y+2)))

def draw_bjt_iv(surf, pr, ib_uA, vce_V, beta, font_sm, font_xs):
    ic_max=max(bjt_ic(IB_REFS[-1],VCE_MAX,beta)*1.25,5.0)
    draw_axes(surf,pr,VCE_MAX,ic_max,"V_CE (V)","I_C (mA)",font_xs)
    # Saturation boundary
    sx=pr.x+int(VCE_SAT/VCE_MAX*pr.w)
    pygame.draw.line(surf,(80,60,30),(sx,pr.y),(sx,pr.bottom),1)
    surf.blit(font_xs.render("Sat.",True,(100,80,40)),(sx-8,pr.bottom+3))
    # Curves
    N=300
    for idx,rib in enumerate(IB_REFS):
        col=CURVE_PAL[idx%len(CURVE_PAL)]
        pts=[iv_px(VCE_MAX*k/N,bjt_ic(float(rib),VCE_MAX*k/N,beta),VCE_MAX,ic_max,pr) for k in range(N+1)]
        pygame.draw.lines(surf,col,False,pts,1)
        surf.blit(font_xs.render(f"{rib}μA",True,col),(pts[-1][0]-26,pts[-1][1]-9))
    # Q-point
    region=bjt_region(ib_uA,vce_V); rcol=bjt_region_col(region)
    ic_val=bjt_ic(ib_uA,vce_V,beta)
    qx,qy=iv_px(vce_V,ic_val,VCE_MAX,ic_max,pr)
    draw_qpoint(surf,qx,qy,rcol,f"Q({vce_V:.1f}V, {ic_val:.2f}mA)",pr,font_xs)
    return ic_val

def draw_mosfet_iv(surf, pr, vgs_V, vds_V, vth_V, font_sm, font_xs):
    vgs_abs=[vth_V+dv for dv in VGS_REFS]
    id_max=max(mosfet_id(vgs_abs[-1],VDS_MAX,vth_V)*1.25,2.0)
    draw_axes(surf,pr,VDS_MAX,id_max,"V_DS (V)","I_D (mA)",font_xs)
    N=300
    for idx,vg in enumerate(vgs_abs):
        if vg<=vth_V: continue
        col=CURVE_PAL[idx%len(CURVE_PAL)]
        pts=[iv_px(VDS_MAX*k/N,mosfet_id(vg,VDS_MAX*k/N,vth_V),VDS_MAX,id_max,pr) for k in range(N+1)]
        pygame.draw.lines(surf,col,False,pts,1)
        # label at knee
        vov=vg-vth_V
        if vov<VDS_MAX:
            kx,ky=iv_px(vov,mosfet_id(vg,vov,vth_V),VDS_MAX,id_max,pr)
            surf.blit(font_xs.render(f"{vg:.1f}V",True,col),(kx+3,ky-9))
    # Boundary parabola
    bpts=[]
    for k in range(N+1):
        vov=VDS_MAX*k/N; vg=vov+vth_V
        if vg>VGS_MAX: break
        bpts.append(iv_px(vov,mosfet_id(vg,vov,vth_V),VDS_MAX,id_max,pr))
    if len(bpts)>2:
        pygame.draw.lines(surf,(110,110,55),False,bpts,1)
    surf.blit(font_xs.render("Triode | Saturation",True,(110,110,55)),(pr.x+6,pr.y+4))
    # Q-point
    region=mosfet_region(vgs_V,vds_V,vth_V); rcol=mosfet_region_col(region)
    id_val=mosfet_id(vgs_V,vds_V,vth_V)
    qx,qy=iv_px(vds_V,id_val,VDS_MAX,id_max,pr)
    draw_qpoint(surf,qx,qy,rcol,f"Q({vds_V:.1f}V, {id_val:.2f}mA)",pr,font_xs)
    return id_val

# ─────────────────────────────────────────────────────────────────────────────
# BJT NPN schematic
# ─────────────────────────────────────────────────────────────────────────────
def draw_bjt_schematic(surf, cx, cy, region, ic_val, beta, font_xs):
    rcol=bjt_region_col(region); br=30
    pygame.draw.circle(surf,(20,22,35),(cx,cy),br)
    pygame.draw.circle(surf,rcol,(cx,cy),br,2)
    bx=cx-12
    pygame.draw.line(surf,rcol,(bx,cy-20),(bx,cy+20),3)
    # Emitter
    ex,ey=cx+br-5,cy+22
    pygame.draw.line(surf,rcol,(bx,cy+10),(ex,ey),2)
    ang=math.atan2(ey-(cy+10),ex-bx)
    for da in(0.4,-0.4):
        ax=ex-int(8*math.cos(ang+da)); ay=ey-int(8*math.sin(ang+da))
        pygame.draw.line(surf,rcol,(ex,ey),(ax,ay),2)
    # Collector
    ccx,ccy=cx+br-5,cy-22
    pygame.draw.line(surf,rcol,(bx,cy-10),(ccx,ccy),2)
    # Leads & labels
    pygame.draw.line(surf,IB_COL,(cx-br-20,cy),(bx,cy),2)
    pygame.draw.line(surf,VCE_COL,(ccx,ccy),(ccx,ccy-20),2)
    pygame.draw.line(surf,VCE_COL,(ccx,ccy-20),(ccx+14,ccy-20),2)
    surf.blit(font_xs.render("VCC",True,VCE_COL),(ccx+6,ccy-30))
    for i,lw in enumerate([14,9,5]):
        pygame.draw.line(surf,VCE_COL,(ex-lw,ey+18+i*6),(ex+lw,ey+18+i*6),2)
    surf.blit(font_xs.render("B",True,IB_COL),(cx-br-30,cy-7))
    surf.blit(font_xs.render("C",True,VCE_COL),(ccx+4,ccy-9))
    surf.blit(font_xs.render("E",True,VCE_COL),(ex+4,ey+5))
    # Current arrows
    if region!="Cutoff":
        ic_n=clamp(ic_val/(beta*IB_MAX/1000.0+1e-9))
        al=int(10+ic_n*12)
        pygame.draw.line(surf,IB_COL,(ccx,ccy-6),(ccx,ccy-6+al),2)
        pygame.draw.polygon(surf,IB_COL,[(ccx,ccy-6+al),(ccx-4,ccy-6+al-7),(ccx+4,ccy-6+al-7)])
    surf.blit(font_xs.render(region,True,rcol),(cx-28,cy+br+8))

# ─────────────────────────────────────────────────────────────────────────────
# MOSFET NMOS schematic (simplified symbol)
# ─────────────────────────────────────────────────────────────────────────────
def draw_mosfet_schematic(surf, cx, cy, region, id_val, vov, font_xs):
    rcol=mosfet_region_col(region)
    gx=cx-36
    # Gate lead + metal plate
    pygame.draw.line(surf,VGS_COL,(gx-20,cy),(gx,cy),2)
    pygame.draw.line(surf,VGS_COL,(gx,cy-22),(gx,cy+22),3)
    # Oxide gap (dashed)
    ox=gx+9
    for dy in range(-22,23,4):
        pygame.draw.line(surf,DIM,(ox,cy+dy),(ox,cy+dy+2),1)
    # Channel
    chx=ox+9
    ch_col=rcol if region!="Cutoff" else (35,35,55)
    pygame.draw.line(surf,ch_col,(chx,cy-22),(chx,cy+22),4)
    # Drain and Source horizontal leads
    pygame.draw.line(surf,VDS_COL,(chx,cy-22),(chx+28,cy-22),2)
    pygame.draw.line(surf,VDS_COL,(chx,cy+22),(chx+28,cy+22),2)
    # Drain goes up to VDD
    pygame.draw.line(surf,VDS_COL,(chx+28,cy-22),(chx+28,cy-48),2)
    surf.blit(font_xs.render("V_DD",True,VDS_COL),(chx+20,cy-62))
    # Source GND
    for i,lw in enumerate([14,9,5]):
        pygame.draw.line(surf,VDS_COL,(chx+28-lw,cy+22+16+i*6),(chx+28+lw,cy+22+16+i*6),2)
    # Terminal labels
    surf.blit(font_xs.render("G",True,VGS_COL),(gx-30,cy-7))
    surf.blit(font_xs.render("D",True,VDS_COL),(chx+32,cy-28))
    surf.blit(font_xs.render("S",True,VDS_COL),(chx+32,cy+16))
    # Overdrive
    if vov>0:
        surf.blit(font_xs.render(f"V_ov={vov:.2f}V",True,rcol),(gx-20,cy+36))
    surf.blit(font_xs.render(region,True,rcol),(cx-30,cy+58))

# ─────────────────────────────────────────────────────────────────────────────
# Poclet loader
# ─────────────────────────────────────────────────────────────────────────────
DEFAULTS={'label':'BJT NPN + MOSFET NMOS','domain':'Electronics',
          'asfid':[0.70,0.90,0.95,0.85,0.80],'revoi':[0.95,0.60,0.90,0.90,0.95],'gap':0.01}

def load_poclet(path):
    try:
        data=json.load(open(path,'r',encoding='utf-8'))
        node=data.get('@graph',[{}])[0]
        asfid=[float(node.get('m0:asfidScores',{}).get(k,d)) for k,d in zip('ASFID',DEFAULTS['asfid'])]
        revoi=[float(node.get('m0:revoiScores', {}).get(k,d)) for k,d in zip('REVOI',DEFAULTS['revoi'])]
        return {'label':node.get('rdfs:label',DEFAULTS['label']),
                'domain':node.get('m0:domain',DEFAULTS['domain']),
                'asfid':asfid,'revoi':revoi,
                'gap':float(node.get('m0:epistemicGap',DEFAULTS['gap']))}
    except Exception as ex:
        print(f"[TSCG] poclet load failed: {ex}"); return DEFAULTS.copy()

def find_poclet():
    if POCLET_OVERRIDE: return Path(POCLET_OVERRIDE)
    cur=Path(__file__).resolve().parent
    for _ in range(8):
        c=cur/"instances"/"poclets"/"transistor"/"M0_Transistor.jsonld"
        if c.exists(): return c
        p=cur.parent
        if p==cur: break
        cur=p
    loc=Path(__file__).parent/"M0_Transistor.jsonld"
    return loc if loc.exists() else None

# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────
def main():
    pp=find_poclet()
    poclet=load_poclet(pp) if pp else DEFAULTS.copy()
    print(f"[TSCG] {poclet['label']}")

    pygame.init()
    screen=pygame.display.set_mode((WINDOW_W,WINDOW_H))
    pygame.display.set_caption("TSCG · BJT NPN / MOSFET NMOS — Operating Modes")
    clock=pygame.time.Clock()

    font_lg=pygame.font.SysFont("segoeui",19,bold=True)
    font_md=pygame.font.SysFont("segoeui",14,bold=True)
    font_sm=pygame.font.SysFont("segoeui",13)
    font_xs=pygame.font.SysFont("segoeui",11)

    sw=LEFT_W-PAD*4
    # BJT sliders
    s_ib   =Slider(PAD*2, 88, sw, 0, IB_MAX,   40,  "Base Current (I_B)",        "μA",IB_COL)
    s_vce  =Slider(PAD*2,164, sw, 0, VCE_MAX,   5.0,"Coll-Emit Voltage (V_CE)", "V", VCE_COL)
    s_beta =Slider(PAD*2,240, sw, BETA_MIN,BETA_MAX,150,"Current Gain (β)",      "",  BETA_COL)
    # MOSFET sliders
    s_vgs  =Slider(PAD*2, 88, sw, 0, VGS_MAX,   2.5,"Gate-Source Voltage (V_GS)","V",VGS_COL)
    s_vds  =Slider(PAD*2,164, sw, 0, VDS_MAX,   3.0,"Drain-Source Voltage (V_DS)","V",VDS_COL)
    s_vth  =Slider(PAD*2,240, sw, VTH_MIN,VTH_MAX,1.0,"Threshold Voltage (V_th)","V",VTH_COL)

    device_idx  = 0   # 0=BJT  1=MOSFET
    hover_mode  = ""  # label of mode row under mouse cursor
    mode_rects  = []  # list of (rect, label) for current frame

    TAB_Y, TAB_W, TAB_H, TAB_GAP = 6, 122, 32, 6

    def apply_preset(label):
        """Snap sliders to typical values for the given mode label."""
        if device_idx == 0:
            # Find best matching key (label may be "Forward Active" etc.)
            key = next((k for k in BJT_PRESETS if k in label or label.startswith(k)), None)
            if key:
                ib, vce, b = BJT_PRESETS[key]
                s_ib.value  = clamp(ib,   s_ib.vmin,   s_ib.vmax)
                s_vce.value = clamp(vce,  s_vce.vmin,  s_vce.vmax)
                s_beta.value= clamp(b,    s_beta.vmin, s_beta.vmax)
        else:
            key = next((k for k in MOSFET_PRESETS if k in label or label.startswith(k)), None)
            if key:
                vgs, vds, vth = MOSFET_PRESETS[key]
                s_vgs.value = clamp(vgs, s_vgs.vmin, s_vgs.vmax)
                s_vds.value = clamp(vds, s_vds.vmin, s_vds.vmax)
                s_vth.value = clamp(vth, s_vth.vmin, s_vth.vmax)

    running=True
    while running:
        clock.tick(FPS)

        active_sliders=[s_ib,s_vce,s_beta] if device_idx==0 else [s_vgs,s_vds,s_vth]

        # Update hover state from current mouse position
        mx_now, my_now = pygame.mouse.get_pos()
        hover_mode = ""
        for r, lbl in mode_rects:
            if r.collidepoint(mx_now, my_now):
                hover_mode = lbl
                break
        # Set hand cursor when hovering a mode row
        if hover_mode:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        for event in pygame.event.get():
            if event.type==pygame.QUIT: running=False
            if event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE: running=False
            if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
                mx,my=event.pos
                # Tab click
                if TAB_Y<my<TAB_Y+TAB_H:
                    tx0=LEFT_W+10; tx1=tx0+TAB_W+TAB_GAP
                    if tx0<mx<tx0+TAB_W: device_idx=0
                    elif tx1<mx<tx1+TAB_W: device_idx=1
                # Mode row click → apply preset
                for r, lbl in mode_rects:
                    if r.collidepoint(mx, my):
                        apply_preset(lbl)
                        break
            for s in active_sliders:
                s.handle_event(event)

        # Physical values
        if device_idx==0:
            ib_uA=s_ib.value; vce_V=s_vce.value; beta=s_beta.value
            region=bjt_region(ib_uA,vce_V); rcol=bjt_region_col(region)
            ic_val=bjt_ic(ib_uA,vce_V,beta)
        else:
            vgs_V=s_vgs.value; vds_V=s_vds.value; vth_V=s_vth.value
            region=mosfet_region(vgs_V,vds_V,vth_V); rcol=mosfet_region_col(region)
            id_val=mosfet_id(vgs_V,vds_V,vth_V); vov=max(vgs_V-vth_V,0.0)

        # Dynamic ASFID
        ba=poclet['asfid']
        if device_idx==0:
            amp=(region=="Forward Active")
            ic_n=clamp(ic_val/(beta*IB_MAX/1000.0+1e-9))
            asfid_live=[clamp(ba[0]*(0.3+0.7*(1 if amp else 0.2))),ba[1],
                        clamp(ba[2]*(0.1+0.9*ic_n)),
                        clamp(ba[3]*(0.2+0.8*(beta-BETA_MIN)/(BETA_MAX-BETA_MIN))),
                        clamp(ba[4]*(0.1+0.9*vce_V/VCE_MAX))]
        else:
            amp=(region=="Saturation")
            id_n=clamp(id_val/(0.5*KN*(VGS_MAX-vth_V)**2+1e-9))
            asfid_live=[clamp(ba[0]*(0.3+0.7*(1 if amp else 0.2))),ba[1],
                        clamp(ba[2]*(0.05+0.95*id_n)),
                        clamp(ba[3]*(0.2+0.8*vgs_V/VGS_MAX)),
                        clamp(ba[4]*(0.1+0.9*vds_V/VDS_MAX))]

        # ── DRAW ─────────────────────────────────────────────────────────────
        screen.fill(BG)

        # ── LEFT PANEL
        pygame.draw.rect(screen,PANEL_BG,(0,0,LEFT_W,WINDOW_H))
        pygame.draw.line(screen,BORDER,(LEFT_W,0),(LEFT_W,WINDOW_H))

        dev_lbl="BJT NPN" if device_idx==0 else "MOSFET NMOS"
        t=font_lg.render(f"⚡ {dev_lbl}",True,GOLD); screen.blit(t,(PAD+4,PAD+4))
        screen.blit(font_xs.render(f"Domain: {poclet['domain']}  |  ΔΘ={poclet['gap']:.2f}",
                                    True,DIM),(PAD+4,PAD+4+t.get_height()+2))

        sep=PAD+t.get_height()+16
        pygame.draw.line(screen,BORDER,(PAD,sep),(LEFT_W-PAD,sep))
        screen.blit(font_md.render("Parameter Controls",True,TEXT),(PAD+4,sep+5))

        if device_idx==0:
            s_ib.draw(screen,font_sm,f"{s_ib.value:.1f} μA")
            s_vce.draw(screen,font_sm,f"{s_vce.value:.2f} V")
            s_beta.draw(screen,font_sm,f"β = {int(s_beta.value)}")
        else:
            s_vgs.draw(screen,font_sm,f"{s_vgs.value:.2f} V")
            s_vds.draw(screen,font_sm,f"{s_vds.value:.2f} V")
            s_vth.draw(screen,font_sm,f"{s_vth.value:.2f} V")

        sch_cy=s_beta.rect.bottom+54 if device_idx==0 else s_vth.rect.bottom+54
        if device_idx==0:
            draw_bjt_schematic(screen,LEFT_W//2,sch_cy,region,ic_val,beta,font_xs)
        else:
            draw_mosfet_schematic(screen,LEFT_W//2,sch_cy,region,id_val,vov,font_xs)

        # Mode table (clickable)
        modes=BJT_MODES if device_idx==0 else MOSFET_MODES
        mt_y=sch_cy+100
        pygame.draw.line(screen,BORDER,(PAD,mt_y-22),(LEFT_W-PAD,mt_y-22))
        screen.blit(font_md.render("Operating Modes",True,TEXT),(PAD+4,mt_y-18))
        hint_s = font_xs.render("← click a mode to apply", True, (100, 140, 100))
        screen.blit(hint_s, (LEFT_W - hint_s.get_width() - PAD, mt_y - 16))
        mode_rects = draw_mode_table(screen, PAD+2, mt_y, LEFT_W-PAD*2-4,
                                     modes, region, hover_mode, font_sm, font_xs)

        # ── CENTRE PANEL
        pygame.draw.rect(screen,(16,16,24),(LEFT_W,0,MID_W,WINDOW_H))

        # Device tabs
        for i,(tlbl,tbcol) in enumerate([("BJT NPN",(60,120,200)),
                                          ("MOSFET NMOS",(60,160,100))]):
            tx=LEFT_W+10+i*(TAB_W+TAB_GAP); ty=TAB_Y
            sel=(i==device_idx)
            bg=(32+sel*18,32+sel*28,48+sel*30)
            pygame.draw.rect(screen,bg,(tx,ty,TAB_W,TAB_H),border_radius=6)
            pygame.draw.rect(screen,tbcol if sel else (50,50,70),(tx,ty,TAB_W,TAB_H),2,border_radius=6)
            ls=font_md.render(tlbl,True,TEXT if sel else DIM)
            screen.blit(ls,(tx+TAB_W//2-ls.get_width()//2,ty+TAB_H//2-ls.get_height()//2))

        # I-V plot area
        IV_L,IV_T,IV_R,IV_B=52,TAB_Y+TAB_H+40,18,52
        pr=pygame.Rect(LEFT_W+IV_L,IV_T,MID_W-IV_L-IV_R,WINDOW_H-IV_T-IV_B)

        if device_idx==0:
            draw_bjt_iv(screen,pr,ib_uA,vce_V,beta,font_sm,font_xs)
        else:
            draw_mosfet_iv(screen,pr,vgs_V,vds_V,vth_V,font_sm,font_xs)

        # Region colour legend
        cols_legend=[(lbl[:11],col,_c) for lbl,col,_c,_ in (BJT_MODES if device_idx==0 else MOSFET_MODES)]
        lx=LEFT_W+IV_L; ly=pr.bottom+3
        for rlbl,rcl,_ in cols_legend:
            s=font_xs.render(f"● {rlbl}",True,rcl); screen.blit(s,(lx,ly)); lx+=s.get_width()+18

        # Naming-inversion warning banner
        wb=24
        ws=pygame.Surface((MID_W,wb),pygame.SRCALPHA); ws.fill((255,200,0,18))
        screen.blit(ws,(LEFT_W,WINDOW_H-wb))
        wt=font_xs.render(NAMING_WARN,True,(180,160,50))
        screen.blit(wt,(LEFT_W+6,WINDOW_H-wb+5))

        screen.blit(font_xs.render("Source: M0_Transistor.jsonld",True,(50,50,70)),
                    (LEFT_W+6,WINDOW_H-wb-14))

        # ── RIGHT PANEL
        rp=LEFT_W+MID_W
        pygame.draw.rect(screen,PANEL_BG,(rp,0,RIGHT_W,WINDOW_H))
        pygame.draw.line(screen,BORDER,(rp,0),(rp,WINDOW_H))

        ar=pygame.Rect(rp+2,4,       RIGHT_W-4,163)
        rr=pygame.Rect(rp+2,ar.bottom+4, RIGHT_W-4,158)
        sr=pygame.Rect(rp+2,rr.bottom+4, RIGHT_W-4, WINDOW_H-rr.bottom-8)

        draw_asfid(screen,ar,asfid_live,poclet['asfid'],font_md,font_sm,font_xs)
        draw_revoi(screen,rr,poclet['revoi'],font_md,font_sm,font_xs)

        if device_idx==0:
            vlines=[(f"I_B  = {ib_uA:.1f} μA",IB_COL),(f"V_CE = {vce_V:.2f} V",VCE_COL),
                    (f"β    = {int(beta)}",BETA_COL),(f"I_C  = {ic_val:.2f} mA",GREEN_OK),
                    (f"P_D  = {vce_V*ic_val:.1f} mW",RED_WARN)]
        else:
            vlines=[(f"V_GS = {vgs_V:.2f} V",VGS_COL),(f"V_DS = {vds_V:.2f} V",VDS_COL),
                    (f"V_th = {vth_V:.2f} V",VTH_COL),(f"V_ov = {vov:.2f} V",GREEN_OK),
                    (f"I_D  = {id_val:.2f} mA",GREEN_OK),(f"P_D  = {vds_V*id_val:.1f} mW",RED_WARN)]
        draw_status(screen,sr,"BJT" if device_idx==0 else "MOSFET",
                    region,vlines,font_md,font_sm,font_xs)

        screen.blit(font_xs.render(f"FPS:{int(clock.get_fps())}",True,(45,45,65)),
                    (LEFT_W+4,WINDOW_H-40))
        pygame.display.flip()

    pygame.quit()
    print("[TSCG] Simulation ended.")

if __name__=="__main__":
    main()
