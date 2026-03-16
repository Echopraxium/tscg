"""
vco_sim.py
==========
TSCG Poclet Simulation — Voltage Controlled Oscillator (VCO)
Author: Echopraxium with the collaboration of Claude AI

Driven by:           M0_VCO.jsonld
Primary metaconcept: m2:Oscillator — ⊗⇒(Component, Process, Trajectory | Circular)
ASFID formula:       S ⊗ A ⊗ I ⊗ D ⊗ F

Audio engine: pygame.mixer (44 100 Hz, 16-bit, stereo) + numpy phase accumulator
Display:      pygame 1 280 × 760

Layout:
  LEFT   (320 px) — Controls : Frequency slider, Amplitude slider, Fine Tune,
                                Waveform tabs, audio ON/OFF
  CENTER (620 px) — Oscilloscope (live waveform) + note name + V/Oct curve
  RIGHT  (340 px) — ASFID / REVOI score bars + live parameter readout

Mouse controls:
  Drag sliders          — Frequency (log scale 20–2 000 Hz), Amplitude (0–100 %),
                          Fine Tune (±100 cents)
  Click waveform tabs   — Sine / Square / Triangle / Sawtooth
  Click [AUDIO] button  — toggle sound on/off
  ESC or ✕             — quit

Requirements:
  pip install pygame numpy

Run:
  python vco_sim.py
"""

from __future__ import annotations
import math
import sys
import numpy as np
import pygame

# ─────────────────────────────────────────────────────────────────────────────
# Audio constants
# ─────────────────────────────────────────────────────────────────────────────

SAMPLE_RATE   = 44_100
CHUNK_FRAMES  = 2_048          # frames per audio buffer (~46 ms latency)
CHANNELS      = 2              # stereo (pygame.mixer requirement)
BIT_DEPTH     = -16            # signed 16-bit

# ─────────────────────────────────────────────────────────────────────────────
# Display constants
# ─────────────────────────────────────────────────────────────────────────────

WIN_W, WIN_H = 1_280, 760
FPS          = 60

LEFT_W  = 320
RIGHT_W = 340
MID_W   = WIN_W - LEFT_W - RIGHT_W   # 620

# Palette
BG      = ( 10,  12,  18)
PANEL   = ( 20,  22,  32)
PANEL2  = ( 28,  30,  45)
BORDER  = ( 50,  55,  80)
TEXT    = (220, 225, 235)
DIM     = (110, 115, 140)
GOLD    = (255, 195,  40)
CYAN    = ( 50, 210, 225)
GREEN   = ( 65, 205, 110)
RED_C   = (220,  60,  60)
ORANGE  = (255, 150,  40)
PURPLE  = (170, 100, 255)
WHITE   = (255, 255, 255)
PAD     = 14

WAVEFORM_COLORS = {
    "Sine":     CYAN,
    "Square":   GREEN,
    "Triangle": ORANGE,
    "Sawtooth": GOLD,
}
WAVEFORMS = ["Sine", "Square", "Triangle", "Sawtooth"]

# ASFID / REVOI scores (from M0_VCO.jsonld)
ASFID = {"A": 0.90, "S": 0.75, "F": 0.85, "I": 0.80, "D": 0.90}
REVOI = {"R": 0.90, "E": 0.85, "V": 0.95, "O": 0.95, "I": 0.95}

# ─────────────────────────────────────────────────────────────────────────────
# Waveform synthesis (numpy, phase accumulator)
# ─────────────────────────────────────────────────────────────────────────────

def make_chunk(waveform: str, frequency: float, amplitude: float,
               phase: float, n_frames: int) -> tuple[np.ndarray, float]:
    """
    Generate one audio chunk.
    Returns (samples_int16_stereo, next_phase).
    phase is in [0, 2π).
    """
    t   = np.arange(n_frames, dtype=np.float64)
    phi = phase + 2.0 * math.pi * frequency * t / SAMPLE_RATE
    phi_mod = phi % (2.0 * math.pi)          # keep in [0, 2π)

    if waveform == "Sine":
        wave = np.sin(phi)

    elif waveform == "Square":
        wave = np.where(phi_mod < math.pi, 1.0, -1.0).astype(np.float64)

    elif waveform == "Triangle":
        # normalised phase in [0,1)
        p = phi_mod / (2.0 * math.pi)
        wave = np.where(p < 0.5, 4.0 * p - 1.0, 3.0 - 4.0 * p)

    elif waveform == "Sawtooth":
        p    = phi_mod / (2.0 * math.pi)
        wave = 2.0 * p - 1.0

    else:
        wave = np.zeros(n_frames)

    # amplitude in [0,1], scale to int16
    samples = (wave * amplitude * 32_767.0).astype(np.int16)
    # stereo interleave
    stereo  = np.column_stack([samples, samples])

    next_phase = float(phi[-1] + 2.0 * math.pi * frequency / SAMPLE_RATE)
    next_phase %= 2.0 * math.pi

    return stereo, next_phase


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

NOTES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

def freq_to_note(freq: float) -> str:
    """Return nearest note name+octave for a given frequency."""
    if freq <= 0:
        return "---"
    semitones = 12.0 * math.log2(freq / 440.0) + 69   # MIDI note number
    midi  = round(semitones)
    cents = round((semitones - midi) * 100)
    name  = NOTES[midi % 12]
    octave = midi // 12 - 1
    sign   = "+" if cents >= 0 else ""
    if cents == 0:
        return f"{name}{octave}"
    return f"{name}{octave} ({sign}{cents}¢)"


def lerp_color(c1, c2, t):
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))


def log_slider_value(raw: float, lo: float, hi: float,
                     lo_log: float, hi_log: float) -> float:
    """Map raw [lo,hi] to [lo_log, hi_log] on a log scale."""
    t = (raw - lo) / (hi - lo)
    return lo_log * (hi_log / lo_log) ** t


def value_to_slider_pos(value: float, lo_log: float, hi_log: float,
                         slider_lo: float, slider_hi: float) -> float:
    """Inverse of log_slider_value."""
    t = math.log(value / lo_log) / math.log(hi_log / lo_log)
    return slider_lo + t * (slider_hi - slider_lo)


# ─────────────────────────────────────────────────────────────────────────────
# UI widgets
# ─────────────────────────────────────────────────────────────────────────────

class Slider:
    """Vertical slider (drag up = increase)."""

    def __init__(self, x: int, cy: int, h: int, label: str,
                 lo: float, hi: float, value: float,
                 log_scale: bool = False,
                 lo_log: float = 20.0, hi_log: float = 2000.0,
                 color=CYAN):
        self.x         = x
        self.cy        = cy          # centre y of track
        self.h         = h           # track height
        self.label     = label
        self.lo        = lo
        self.hi        = hi
        self._value    = value
        self.log_scale = log_scale
        self.lo_log    = lo_log
        self.hi_log    = hi_log
        self.color     = color
        self.dragging  = False
        self.track_rect = pygame.Rect(x - 4, cy - h // 2, 8, h)

    # ------------------------------------------------------------------
    @property
    def value(self) -> float:
        return self._value

    @value.setter
    def value(self, v: float):
        if self.log_scale:
            self._value = max(self.lo_log, min(self.hi_log, v))
        else:
            self._value = max(self.lo, min(self.hi, v))

    # ------------------------------------------------------------------
    def _raw_from_value(self) -> float:
        """Convert logical value → raw [lo, hi]."""
        if self.log_scale:
            t = math.log(self._value / self.lo_log) / math.log(self.hi_log / self.lo_log)
            return self.lo + t * (self.hi - self.lo)
        return self._value

    def _value_from_raw(self, raw: float) -> float:
        if self.log_scale:
            return log_slider_value(raw, self.lo, self.hi, self.lo_log, self.hi_log)
        return raw

    # ------------------------------------------------------------------
    def thumb_y(self) -> int:
        raw = self._raw_from_value()
        t   = (raw - self.lo) / (self.hi - self.lo)
        return int(self.cy + self.h // 2 - t * self.h)

    # ------------------------------------------------------------------
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            thumb = pygame.Rect(self.x - 10, self.thumb_y() - 10, 20, 20)
            if thumb.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            my      = event.pos[1]
            t       = 1.0 - (my - (self.cy - self.h // 2)) / self.h
            t       = max(0.0, min(1.0, t))
            raw     = self.lo + t * (self.hi - self.lo)
            v = self._value_from_raw(raw)
            if self.log_scale:
                self._value = max(self.lo_log, min(self.hi_log, v))
            else:
                self._value = max(self.lo, min(self.hi, v))

    # ------------------------------------------------------------------
    def draw(self, surf: pygame.Surface, font_sm, font_xs):
        # Track
        pygame.draw.rect(surf, PANEL2, self.track_rect, border_radius=4)
        # Fill
        ty  = self.thumb_y()
        fill = pygame.Rect(self.x - 4,
                           ty,
                           8,
                           self.cy + self.h // 2 - ty)
        pygame.draw.rect(surf, lerp_color(self.color, BG, 0.4), fill, border_radius=4)
        # Thumb
        pygame.draw.circle(surf, self.color, (self.x, ty), 9)
        pygame.draw.circle(surf, WHITE, (self.x, ty), 4)
        # Label
        lbl = font_sm.render(self.label, True, DIM)
        surf.blit(lbl, (self.x - lbl.get_width() // 2,
                        self.cy + self.h // 2 + 6))
        # Value
        if self.log_scale:
            val_txt = f"{self._value:.1f} Hz"
        elif "Fine" in self.label:
            sign = "+" if self._value >= 0 else ""
            val_txt = f"{sign}{self._value:.0f} ¢"
        else:
            val_txt = f"{self._value * 100:.0f} %"
        vl = font_xs.render(val_txt, True, self.color)
        surf.blit(vl, (self.x - vl.get_width() // 2,
                       self.cy - self.h // 2 - 18))


class WaveformTabs:
    """Horizontal tab selector for waveform choice."""

    def __init__(self, x: int, y: int, w: int, h: int):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.selected = "Sine"
        self._tab_w   = w // len(WAVEFORMS)

    def _tab_rect(self, idx: int) -> pygame.Rect:
        return pygame.Rect(self.x + idx * self._tab_w, self.y,
                           self._tab_w - 2, self.h)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, name in enumerate(WAVEFORMS):
                if self._tab_rect(i).collidepoint(event.pos):
                    self.selected = name

    def draw(self, surf: pygame.Surface, font_sm):
        for i, name in enumerate(WAVEFORMS):
            rect   = self._tab_rect(i)
            active = (name == self.selected)
            color  = WAVEFORM_COLORS[name]
            bg     = lerp_color(color, PANEL, 0.75) if active else PANEL2
            pygame.draw.rect(surf, bg, rect, border_radius=5)
            pygame.draw.rect(surf, color if active else BORDER, rect, 1, border_radius=5)
            lbl = font_sm.render(name, True, color if active else DIM)
            surf.blit(lbl, (rect.centerx - lbl.get_width() // 2,
                            rect.centery - lbl.get_height() // 2))


class Button:
    def __init__(self, rect: pygame.Rect, label: str,
                 color_on=GREEN, color_off=DIM):
        self.rect      = rect
        self.label     = label
        self.color_on  = color_on
        self.color_off = color_off
        self.state     = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.state = not self.state

    def draw(self, surf, font_sm):
        color  = self.color_on if self.state else self.color_off
        bg     = lerp_color(color, PANEL, 0.72)
        pygame.draw.rect(surf, bg, self.rect, border_radius=6)
        pygame.draw.rect(surf, color, self.rect, 1, border_radius=6)
        lbl = font_sm.render(self.label, True, color)
        surf.blit(lbl, (self.rect.centerx - lbl.get_width() // 2,
                        self.rect.centery - lbl.get_height() // 2))


# ─────────────────────────────────────────────────────────────────────────────
# Score bar renderer
# ─────────────────────────────────────────────────────────────────────────────

def draw_score_bars(surf, font_sm, font_xs, x, y, w, scores: dict,
                    title: str, title_color=GOLD):
    """Draw a labelled set of horizontal score bars."""
    bar_h  = 14
    gap    = 6
    title_lbl = font_sm.render(title, True, title_color)
    surf.blit(title_lbl, (x, y))
    y += title_lbl.get_height() + 6

    for key, val in scores.items():
        # Key label
        kl = font_xs.render(key, True, DIM)
        surf.blit(kl, (x, y + (bar_h - kl.get_height()) // 2))
        bx = x + 22
        bw = w - 22

        # Background
        pygame.draw.rect(surf, PANEL2, (bx, y, bw, bar_h), border_radius=3)
        # Fill
        fill_w = int(bw * val)
        col    = lerp_color(RED_C, GREEN, val)
        if fill_w > 0:
            pygame.draw.rect(surf, col, (bx, y, fill_w, bar_h), border_radius=3)
        # Value text
        vl = font_xs.render(f"{val:.2f}", True, col)
        surf.blit(vl, (bx + bw + 4, y + (bar_h - vl.get_height()) // 2))

        y += bar_h + gap
    return y


# ─────────────────────────────────────────────────────────────────────────────
# Oscilloscope
# ─────────────────────────────────────────────────────────────────────────────

def draw_oscilloscope(surf, rect: pygame.Rect, waveform: str,
                      frequency: float, amplitude: float,
                      color, font_xs):
    """
    Draw the waveform over a fixed 20 ms time window.
    At low frequency few (or partial) cycles are shown; at high frequency
    many cycles are packed in — like a real oscilloscope with fixed timebase.
    """
    SCOPE_WINDOW_MS = 20.0

    pygame.draw.rect(surf, PANEL2, rect, border_radius=6)
    pygame.draw.rect(surf, BORDER, rect, 1, border_radius=6)

    cy   = rect.centery
    w    = rect.width  - 40
    h    = rect.height - 40
    x0   = rect.x + 20
    y0   = rect.y + 20

    window_s = SCOPE_WINDOW_MS / 1000.0
    n_cycles = frequency * window_s   # e.g. 440 Hz * 0.02 s = 8.8 cycles

    # Centre line
    pygame.draw.line(surf, BORDER, (x0, cy), (x0 + w, cy), 1)

    # Vertical grid: one line per complete cycle (cap at 32 to avoid clutter)
    n_grid = min(int(n_cycles), 32)
    if n_grid >= 1:
        for k in range(1, n_grid + 1):
            gx = int(x0 + k / n_cycles * w)
            if x0 <= gx <= x0 + w:
                pygame.draw.line(surf, BORDER, (gx, y0), (gx, y0 + h), 1)
    else:
        for frac in [0.25, 0.5, 0.75]:
            gx = int(x0 + frac * w)
            pygame.draw.line(surf, BORDER, (gx, y0), (gx, y0 + h), 1)

    # Waveform points
    points = []
    for px in range(w):
        t       = px / w * window_s
        phi     = 2.0 * math.pi * frequency * t
        phi_mod = phi % (2.0 * math.pi)
        tn      = phi_mod / (2.0 * math.pi)

        if waveform == "Sine":
            val = math.sin(phi)
        elif waveform == "Square":
            val = 1.0 if phi_mod < math.pi else -1.0
        elif waveform == "Triangle":
            val = (4.0 * tn - 1.0) if tn < 0.5 else (3.0 - 4.0 * tn)
        elif waveform == "Sawtooth":
            val = 2.0 * tn - 1.0
        else:
            val = 0.0

        py = int(cy - val * amplitude * (h / 2))
        points.append((x0 + px, py))

    if len(points) >= 2:
        pygame.draw.lines(surf, color, False, points, 2)

    # Labels
    if n_cycles >= 1.0:
        cycle_txt = f"{n_cycles:.1f} cycles  @ {frequency:.1f} Hz"
    else:
        cycle_txt = f"{1000.0/frequency:.0f} ms/cycle  @ {frequency:.1f} Hz"
    fl = font_xs.render(cycle_txt, True, DIM)
    surf.blit(fl, (x0, y0 - 2))
    al = font_xs.render(f"Amp {amplitude * 100:.0f}%  |  {SCOPE_WINDOW_MS:.0f} ms window", True, DIM)
    surf.blit(al, (x0 + w - al.get_width(), y0 - 2))


# ─────────────────────────────────────────────────────────────────────────────
# V/Oct curve
# ─────────────────────────────────────────────────────────────────────────────

def draw_voct_curve(surf, rect: pygame.Rect, base_freq: float,
                    current_freq: float, color, font_xs):
    """Draw the V/Oct exponential law and mark the current frequency."""
    pygame.draw.rect(surf, PANEL2, rect, border_radius=6)
    pygame.draw.rect(surf, BORDER, rect, 1, border_radius=6)

    mx = rect.x + 10
    my = rect.y + 10
    mw = rect.width  - 20
    mh = rect.height - 20

    cv_lo, cv_hi = -3.0, 5.0      # volts
    f_lo  = base_freq * (2.0 ** cv_lo)
    f_hi  = base_freq * (2.0 ** cv_hi)

    def cv_to_px(cv):
        return int(mx + (cv - cv_lo) / (cv_hi - cv_lo) * mw)

    def freq_to_py(f):
        t = math.log(f / f_lo) / math.log(f_hi / f_lo)
        return int(my + mh - t * mh)

    # Grid lines — every octave (1V)
    for cv in range(int(cv_lo), int(cv_hi) + 1):
        gx = cv_to_px(cv)
        pygame.draw.line(surf, BORDER, (gx, my), (gx, my + mh), 1)
        lbl = font_xs.render(f"{cv:+d}V", True, DIM)
        surf.blit(lbl, (gx - lbl.get_width() // 2, my + mh + 2))

    # Curve
    pts = []
    for px in range(mw):
        cv = cv_lo + px / mw * (cv_hi - cv_lo)
        f  = base_freq * (2.0 ** cv)
        py = freq_to_py(f)
        if my <= py <= my + mh:
            pts.append((mx + px, py))
    if len(pts) >= 2:
        pygame.draw.lines(surf, lerp_color(color, BG, 0.35), False, pts, 1)

    # Current frequency marker
    if f_lo < current_freq < f_hi:
        cv_cur = math.log2(current_freq / base_freq)
        if cv_lo <= cv_cur <= cv_hi:
            gx = cv_to_px(cv_cur)
            gy = freq_to_py(current_freq)
            pygame.draw.line(surf, color, (gx, my), (gx, my + mh), 1)
            pygame.draw.circle(surf, color, (gx, gy), 5)
            fl = font_xs.render(f"{current_freq:.1f} Hz", True, color)
            sx = min(gx + 6, mx + mw - fl.get_width())
            surf.blit(fl, (sx, gy - fl.get_height() - 2))

    # Title
    t = font_xs.render("V/Oct law  f = f₀ × 2^CV", True, DIM)
    surf.blit(t, (mx, my - 2))


# ─────────────────────────────────────────────────────────────────────────────
# Audio streaming thread
# ─────────────────────────────────────────────────────────────────────────────

class AudioEngine:
    """
    Continuous audio output using pygame.sndarray.
    Runs in the main thread via pump() called each frame.
    Uses a Sound object fed with numpy-generated chunks.
    """

    def __init__(self):
        self.phase     = 0.0
        self.waveform  = "Sine"
        self.frequency = 440.0
        self.amplitude = 0.5
        self.enabled   = False
        self._sound    = None
        self._channel  = None

    # ------------------------------------------------------------------
    def _make_sound(self) -> pygame.Sound:
        """Generate one chunk as a pygame.Sound object."""
        chunk, self.phase = make_chunk(
            self.waveform, self.frequency, self.amplitude,
            self.phase, CHUNK_FRAMES
        )
        # pygame.sndarray expects shape (frames, channels)
        sound = pygame.sndarray.make_sound(chunk)
        return sound

    # ------------------------------------------------------------------
    def pump(self):
        """Call every frame. Refills the audio channel when needed."""
        if not self.enabled:
            if self._channel and self._channel.get_busy():
                self._channel.stop()
            return

        if self._channel is None or not self._channel.get_busy():
            sound = self._make_sound()
            self._channel = sound.play()
        elif self._channel.get_queue() is None:
            sound = self._make_sound()
            self._channel.queue(sound)


def make_chunk(waveform: str, frequency: float, amplitude: float,
               phase: float, n_frames: int):
    """
    Generate n_frames samples.
    Returns (int16 stereo ndarray shape (n,2), next_phase).
    """
    t   = np.arange(n_frames, dtype=np.float64)
    phi = phase + 2.0 * math.pi * frequency * t / SAMPLE_RATE
    p   = phi % (2.0 * math.pi)

    if waveform == "Sine":
        wave = np.sin(phi)
    elif waveform == "Square":
        wave = np.where(p < math.pi, 1.0, -1.0).astype(np.float64)
    elif waveform == "Triangle":
        pn   = p / (2.0 * math.pi)
        wave = np.where(pn < 0.5, 4.0 * pn - 1.0, 3.0 - 4.0 * pn)
    elif waveform == "Sawtooth":
        pn   = p / (2.0 * math.pi)
        wave = 2.0 * pn - 1.0
    else:
        wave = np.zeros(n_frames)

    samples = (wave * amplitude * 32_767.0).clip(-32_768, 32_767).astype(np.int16)
    stereo  = np.ascontiguousarray(np.column_stack([samples, samples]))
    next_phase = float((phi[-1] + 2.0 * math.pi * frequency / SAMPLE_RATE)
                       % (2.0 * math.pi))
    return stereo, next_phase


# ─────────────────────────────────────────────────────────────────────────────
# Main application
# ─────────────────────────────────────────────────────────────────────────────

def main():
    pygame.init()
    pygame.mixer.init(frequency=SAMPLE_RATE,
                      size=BIT_DEPTH,
                      channels=CHANNELS,
                      buffer=CHUNK_FRAMES)
    pygame.display.set_caption("TSCG — VCO Simulation  [m2:Oscillator]")
    screen = pygame.display.set_mode((WIN_W, WIN_H))
    clock  = pygame.time.Clock()

    # ── Fonts ─────────────────────────────────────────────────────────
    font_lg = pygame.font.SysFont("monospace", 18, bold=True)
    font_sm = pygame.font.SysFont("monospace", 13)
    font_xs = pygame.font.SysFont("monospace", 11)

    # ── Widgets ───────────────────────────────────────────────────────
    # Sliders — centred in left panel
    sl_cx  = LEFT_W // 2
    sl_h   = 180

    sl_freq = Slider(
        x=sl_cx - 60, cy=200, h=sl_h,
        label="Frequency",
        lo=0.0, hi=1.0, value=0.0,   # raw [0,1] for log mapping
        log_scale=True,
        lo_log=20.0, hi_log=2000.0,
        color=CYAN
    )
    # Set initial value (440 Hz)
    sl_freq._value = log_slider_value(
        value_to_slider_pos(440.0, 20.0, 2000.0, 0.0, 1.0),
        0.0, 1.0, 20.0, 2000.0
    )

    sl_amp = Slider(
        x=sl_cx + 60, cy=200, h=sl_h,
        label="Amplitude",
        lo=0.0, hi=1.0, value=0.5,
        log_scale=False,
        color=GOLD
    )

    sl_fine = Slider(
        x=sl_cx, cy=470, h=80,
        label="Fine Tune",
        lo=-1.0, hi=1.0, value=0.0,
        log_scale=False,
        color=ORANGE
    )

    tabs = WaveformTabs(x=12, y=580, w=LEFT_W - 24, h=34)

    btn_audio = Button(
        rect=pygame.Rect(LEFT_W // 2 - 50, WIN_H - 60, 100, 36),
        label="◉  AUDIO",
        color_on=GREEN,
        color_off=DIM
    )

    # ── Audio engine ──────────────────────────────────────────────────
    audio = AudioEngine()

    # ── Main loop ─────────────────────────────────────────────────────
    running = True
    while running:

        # ── Events ────────────────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

            sl_freq.handle_event(event)
            sl_amp.handle_event(event)
            sl_fine.handle_event(event)
            tabs.handle_event(event)
            btn_audio.handle_event(event)

        # ── Compute current VCO parameters ────────────────────────────
        base_freq = sl_freq.value       # already in Hz (log mapped)
        # Fine tune: ±100 cents → ×2^(cents/1200)
        fine_ratio = 2.0 ** (sl_fine.value * 100.0 / 1200.0)
        frequency  = base_freq * fine_ratio
        amplitude  = sl_amp.value
        waveform   = tabs.selected
        waveform_color = WAVEFORM_COLORS[waveform]

        # ── Feed audio engine ─────────────────────────────────────────
        audio.waveform  = waveform
        audio.frequency = max(20.0, frequency)
        audio.amplitude = amplitude
        audio.enabled   = btn_audio.state
        audio.pump()

        # ── Draw ──────────────────────────────────────────────────────
        screen.fill(BG)

        # ── LEFT PANEL ────────────────────────────────────────────────
        pygame.draw.rect(screen, PANEL,
                         pygame.Rect(0, 0, LEFT_W, WIN_H))
        pygame.draw.line(screen, BORDER,
                         (LEFT_W, 0), (LEFT_W, WIN_H), 1)

        # Title
        tl = font_lg.render("VCO", True, GOLD)
        screen.blit(tl, (PAD, PAD))
        sub = font_xs.render("Voltage Controlled Oscillator", True, DIM)
        screen.blit(sub, (PAD, PAD + tl.get_height() + 2))
        mc  = font_xs.render("m2:Oscillator  |  S⊗A⊗I⊗D⊗F", True,
                              lerp_color(CYAN, DIM, 0.5))
        screen.blit(mc, (PAD, PAD + tl.get_height() + 18))

        # Sliders
        sl_freq.draw(screen, font_sm, font_xs)
        sl_amp.draw(screen,  font_sm, font_xs)
        sl_fine.draw(screen, font_sm, font_xs)

        # Note name
        note_str = freq_to_note(frequency)
        note_lbl = font_lg.render(note_str, True, waveform_color)
        screen.blit(note_lbl, (sl_cx - note_lbl.get_width() // 2, 390))
        hz_lbl = font_xs.render(f"{frequency:.2f} Hz", True, DIM)
        screen.blit(hz_lbl, (sl_cx - hz_lbl.get_width() // 2, 416))

        # Waveform label above tabs
        wl = font_sm.render("Waveform", True, DIM)
        screen.blit(wl, (PAD, 562))
        tabs.draw(screen, font_sm)

        # Audio button
        btn_audio.draw(screen, font_sm)

        # ── CENTER PANEL ──────────────────────────────────────────────
        cx0 = LEFT_W + 10
        scope_rect = pygame.Rect(cx0, 10, MID_W - 20, WIN_H // 2 - 20)
        draw_oscilloscope(screen, scope_rect, waveform,
                          frequency, amplitude, waveform_color, font_xs)

        voct_rect = pygame.Rect(cx0, WIN_H // 2 + 10,
                                MID_W - 20, WIN_H // 2 - 20)
        draw_voct_curve(screen, voct_rect, 440.0,
                        frequency, waveform_color, font_xs)

        # ── RIGHT PANEL ───────────────────────────────────────────────
        rx0 = LEFT_W + MID_W
        pygame.draw.rect(screen, PANEL,
                         pygame.Rect(rx0, 0, RIGHT_W, WIN_H))
        pygame.draw.line(screen, BORDER,
                         (rx0, 0), (rx0, WIN_H), 1)

        ry = PAD
        # ASFID
        ry = draw_score_bars(screen, font_sm, font_xs,
                             rx0 + PAD, ry, RIGHT_W - PAD * 2 - 40,
                             ASFID, "ASFID  (Eagle Eye)", GOLD)
        ry += 16
        # REVOI
        ry = draw_score_bars(screen, font_sm, font_xs,
                             rx0 + PAD, ry, RIGHT_W - PAD * 2 - 40,
                             REVOI, "REVOI  (Sphinx Eye)", CYAN)
        ry += 20

        # Live parameters
        params = [
            ("Waveform",   waveform),
            ("Frequency",  f"{frequency:.2f} Hz"),
            ("Amplitude",  f"{amplitude * 100:.0f} %"),
            ("Note",       freq_to_note(frequency)),
            ("Phase",      "Arbitrary (free-run)"),
            ("Damping ζ",  "Undamped (active)"),
            ("Audio",      "ON" if btn_audio.state else "OFF"),
        ]
        hdr = font_sm.render("Live Parameters", True, ORANGE)
        screen.blit(hdr, (rx0 + PAD, ry))
        ry += hdr.get_height() + 6
        pygame.draw.line(screen, BORDER,
                         (rx0 + PAD, ry), (rx0 + RIGHT_W - PAD, ry), 1)
        ry += 6
        for key, val in params:
            kl = font_xs.render(key + ":", True, DIM)
            vl = font_xs.render(val, True, TEXT)
            screen.blit(kl, (rx0 + PAD, ry))
            screen.blit(vl, (rx0 + PAD + 90, ry))
            ry += kl.get_height() + 4

        # Bottom credits
        cr = font_xs.render(
            "Echopraxium with the collaboration of Claude AI  |  TSCG v15.8.0",
            True, DIM)
        screen.blit(cr, (WIN_W // 2 - cr.get_width() // 2, WIN_H - 18))

        pygame.display.flip()
        clock.tick(FPS)

    # ── Cleanup ───────────────────────────────────────────────────────
    pygame.mixer.quit()
    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
