"""Dependency-free SVG chart primitives for the theft research report.

Every function returns a standalone `<svg>` string sized in a fixed user-space
coordinate system and scaled by CSS (`width:100%;height:auto`), so the report
stays a single self-contained HTML file with no CDN, no JS and no raster images.
Charts therefore survive offline viewing, printing and PDF export.
"""

from __future__ import annotations

from dataclasses import dataclass
from html import escape
from typing import Iterable, Sequence

# ---------------------------------------------------------------- palette ---

INK = "#12181f"
MUTED = "#5b6673"
GRID = "#e3e8ee"
AXIS = "#aab3bd"

PALETTE = [
    "#2f5d9e",  # deep blue
    "#c8542a",  # burnt orange
    "#3f8f6b",  # green
    "#8a5fb0",  # purple
    "#c2a02c",  # ochre
    "#b03a55",  # crimson
    "#4f8fbf",  # light blue
    "#7a8794",  # grey
]

ACCENT = "#c8542a"
POSITIVE = "#3f8f6b"
NEGATIVE = "#b03a55"


def _c(i: int) -> str:
    return PALETTE[i % len(PALETTE)]


def _esc(s: object) -> str:
    return escape(str(s), quote=True)


def _fmt(v: float, unit: str = "", dp: int | None = None) -> str:
    if dp is None:
        dp = 0 if abs(v) >= 10 or float(v).is_integer() else 1
    txt = f"{v:,.{dp}f}"
    return f"{txt}{unit}"


def _open(w: int, h: int, label: str) -> str:
    return (
        f'<svg viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" '
        f'role="img" aria-label="{_esc(label)}" '
        f'style="width:100%;height:auto;display:block;font-family:'
        f'-apple-system,BlinkMacSystemFont,\'Segoe UI\',Roboto,Helvetica,Arial,sans-serif">'
    )


def _text(x: float, y: float, s: object, size: float = 13, fill: str = INK,
          anchor: str = "start", weight: str = "400", opacity: float = 1.0) -> str:
    op = f' opacity="{opacity}"' if opacity != 1.0 else ""
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" '
        f'text-anchor="{anchor}" font-weight="{weight}"{op}>{_esc(s)}</text>'
    )


def _wrap(s: str, width: int) -> list[str]:
    words, lines, cur = str(s).split(), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if len(trial) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines or [""]


def _nice_ticks(vmax: float, count: int = 5) -> list[float]:
    """Round axis ticks to a human-readable step covering [0, vmax]."""
    if vmax <= 0:
        return [0.0, 1.0]
    raw = vmax / count
    mag = 10 ** (len(str(int(raw))) - 1) if raw >= 1 else 10 ** -2
    for mult in (1, 2, 2.5, 5, 10, 20, 25, 50, 100):
        step = mag * mult
        if step >= raw:
            break
    ticks, t = [], 0.0
    while t < vmax + step * 0.001:
        ticks.append(round(t, 6))
        t += step
    if ticks[-1] < vmax:
        ticks.append(round(ticks[-1] + step, 6))
    return ticks


# ------------------------------------------------------------- horizontal ---

@dataclass
class Bar:
    label: str
    value: float
    color: str | None = None
    note: str = ""


def hbar(bars: Sequence[Bar], unit: str = "%", label_w: int = 232,
         width: int = 780, row_h: int = 30, gap: int = 9,
         dp: int | None = None, vmax: float | None = None,
         title: str = "") -> str:
    """Horizontal bars, longest-first is the caller's job. Value printed at bar end."""
    n = len(bars)
    top = 26 if title else 8
    plot_x = label_w + 10
    plot_w = width - plot_x - 74
    h = top + n * (row_h + gap) + 34
    vmax = vmax or max(b.value for b in bars)
    ticks = _nice_ticks(vmax)
    scale = plot_w / ticks[-1]

    out = [_open(width, h, title or "bar chart")]
    if title:
        out.append(_text(0, 14, title, 13.5, INK, weight="600"))

    for t in ticks:
        x = plot_x + t * scale
        out.append(
            f'<line x1="{x:.1f}" y1="{top}" x2="{x:.1f}" y2="{top + n * (row_h + gap):.1f}" '
            f'stroke="{GRID}" stroke-width="1"/>'
        )
        out.append(_text(x, top + n * (row_h + gap) + 18, _fmt(t, unit), 11, MUTED, "middle"))

    for i, b in enumerate(bars):
        y = top + i * (row_h + gap)
        col = b.color or _c(i)
        bw = max(1.5, b.value * scale)
        lines = _wrap(b.label, 34)[:2]
        ly = y + row_h / 2 + (4 if len(lines) == 1 else -3)
        for j, ln in enumerate(lines):
            out.append(_text(label_w, ly + j * 13, ln, 12.5, INK, "end"))
        out.append(
            f'<rect x="{plot_x}" y="{y}" width="{bw:.1f}" height="{row_h}" '
            f'rx="2" fill="{col}"/>'
        )
        out.append(_text(plot_x + bw + 7, y + row_h / 2 + 4.5,
                         _fmt(b.value, unit, dp), 12.5, INK, "start", "600"))
        if b.note:
            out.append(_text(plot_x + 8, y + row_h / 2 + 4.5, b.note, 11, "#ffffff",
                             "start", "600"))
    out.append(f'<line x1="{plot_x}" y1="{top}" x2="{plot_x}" y2="{top + n * (row_h + gap):.1f}" '
               f'stroke="{AXIS}" stroke-width="1"/>')
    out.append("</svg>")
    return "".join(out)


# --------------------------------------------------------------- vertical ---

def vbar(bars: Sequence[Bar], unit: str = "", width: int = 780, height: int = 300,
         dp: int | None = None, title: str = "", label_lines: int = 2) -> str:
    left, right, top = 62, 14, 28 if title else 12
    bottom = 26 + 14 * label_lines
    n = len(bars)
    plot_w = width - left - right
    plot_h = height - top - bottom
    vmax = max(b.value for b in bars)
    ticks = _nice_ticks(vmax)
    scale = plot_h / ticks[-1]
    slot = plot_w / n
    bw = min(72, slot * 0.62)

    out = [_open(width, height, title or "column chart")]
    if title:
        out.append(_text(0, 14, title, 13.5, INK, weight="600"))
    for t in ticks:
        y = top + plot_h - t * scale
        out.append(f'<line x1="{left}" y1="{y:.1f}" x2="{width - right}" y2="{y:.1f}" '
                   f'stroke="{GRID}" stroke-width="1"/>')
        out.append(_text(left - 8, y + 4, _fmt(t, unit), 11, MUTED, "end"))
    for i, b in enumerate(bars):
        x = left + slot * i + (slot - bw) / 2
        bh = max(1.5, b.value * scale)
        y = top + plot_h - bh
        out.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw:.1f}" height="{bh:.1f}" '
                   f'rx="2" fill="{b.color or _c(i)}"/>')
        out.append(_text(x + bw / 2, y - 6, _fmt(b.value, unit, dp), 12, INK, "middle", "600"))
        for j, ln in enumerate(_wrap(b.label, max(10, int(slot / 6)))[:label_lines]):
            out.append(_text(x + bw / 2, top + plot_h + 18 + j * 13, ln, 11.5, MUTED, "middle"))
    out.append(f'<line x1="{left}" y1="{top + plot_h}" x2="{width - right}" '
               f'y2="{top + plot_h}" stroke="{AXIS}" stroke-width="1"/>')
    out.append("</svg>")
    return "".join(out)


# ------------------------------------------------------------------ donut ---

def donut(bars: Sequence[Bar], width: int = 780, height: int = 320,
          unit: str = "%", title: str = "", centre: str = "", sub: str = "") -> str:
    import math

    cx, cy, r, thick = 150, height / 2 + (8 if title else 0), 108, 44
    total = sum(b.value for b in bars) or 1
    out = [_open(width, height, title or "donut chart")]
    if title:
        out.append(_text(0, 14, title, 13.5, INK, weight="600"))
    ang = -math.pi / 2
    for i, b in enumerate(bars):
        frac = b.value / total
        sweep = frac * 2 * math.pi
        a0, a1 = ang, ang + sweep
        ang = a1
        large = 1 if sweep > math.pi else 0
        ro, ri = r, r - thick
        x0, y0 = cx + ro * math.cos(a0), cy + ro * math.sin(a0)
        x1, y1 = cx + ro * math.cos(a1), cy + ro * math.sin(a1)
        x2, y2 = cx + ri * math.cos(a1), cy + ri * math.sin(a1)
        x3, y3 = cx + ri * math.cos(a0), cy + ri * math.sin(a0)
        out.append(
            f'<path d="M{x0:.2f},{y0:.2f} A{ro},{ro} 0 {large} 1 {x1:.2f},{y1:.2f} '
            f'L{x2:.2f},{y2:.2f} A{ri},{ri} 0 {large} 0 {x3:.2f},{y3:.2f} Z" '
            f'fill="{b.color or _c(i)}" stroke="#ffffff" stroke-width="1.5"/>'
        )
    if centre:
        out.append(_text(cx, cy - 2, centre, 24, INK, "middle", "700"))
    if sub:
        out.append(_text(cx, cy + 18, sub, 11.5, MUTED, "middle"))

    lx = 300
    ly = cy - (len(bars) * 24) / 2 + 8
    for i, b in enumerate(bars):
        y = ly + i * 24
        out.append(f'<rect x="{lx}" y="{y - 10}" width="13" height="13" rx="2.5" '
                   f'fill="{b.color or _c(i)}"/>')
        out.append(_text(lx + 21, y + 1, b.label, 12.5, INK))
        out.append(_text(width - 4, y + 1, _fmt(b.value, unit), 12.5, INK, "end", "600"))
    out.append("</svg>")
    return "".join(out)


# ----------------------------------------------------------------- funnel ---

def funnel(steps: Sequence[tuple[str, float, str]], width: int = 780,
           title: str = "", unit: str = "") -> str:
    """steps: (label, value, annotation). Bar width is proportional to value.

    The value is rendered in a reserved right-hand column and the bar never
    enters it, so long labels on short bars cannot collide with the number.
    """
    top = 28 if title else 8
    row_h, gap = 54, 12
    n = len(steps)
    h = top + n * (row_h + gap) + 6
    vmax = steps[0][1] or 1
    val_col = 92
    max_w = width - val_col - 24

    out = [_open(width, h, title or "attrition funnel")]
    if title:
        out.append(_text(0, 14, title, 13.5, INK, weight="600"))
    for i, (lab, val, note) in enumerate(steps):
        y = top + i * (row_h + gap)
        bw = max(3.0, (val / vmax) * max_w)
        col = PALETTE[0] if i == 0 else ("#b03a55" if i == n - 1 else "#2f5d9e")
        fade = 1 - 0.42 * (i / max(1, n - 1))
        out.append(f'<rect x="0" y="{y}" width="{bw:.1f}" height="{row_h}" rx="3" '
                   f'fill="{col}" opacity="{fade:.2f}"/>')
        inside = bw > 220
        tx = 12 if inside else bw + 12
        out.append(_text(tx, y + 22, lab, 13, "#ffffff" if inside else INK,
                         "start", "600"))
        out.append(_text(tx, y + 39, note, 11, "#eef3f9" if inside else MUTED))
        out.append(_text(width - 4, y + 34, _fmt(val, unit, 1 if val < 10 else 0),
                         19, INK, "end", "700"))
    out.append("</svg>")
    return "".join(out)


# ----------------------------------------------------- effect-size dotplot ---

@dataclass
class Effect:
    label: str
    value: float           # point estimate, % change in crime (negative = reduction)
    lo: float | None = None
    hi: float | None = None
    note: str = ""
    strength: str = ""     # evidence grade shown as a chip


def effects(items: Sequence[Effect], width: int = 780, label_w: int = 250,
            vmin: float = -60, vmax: float = 30, title: str = "") -> str:
    top = 40 if title else 30
    row_h = 30
    n = len(items)
    h = top + n * row_h + 40
    plot_x = label_w + 12
    plot_w = width - plot_x - 96
    span = vmax - vmin
    sx = lambda v: plot_x + (v - vmin) / span * plot_w  # noqa: E731

    out = [_open(width, h, title or "effect sizes")]
    if title:
        out.append(_text(0, 14, title, 13.5, INK, weight="600"))
    step = 10 if span <= 100 else 20
    t = vmin
    while t <= vmax + 0.01:
        x = sx(t)
        out.append(f'<line x1="{x:.1f}" y1="{top - 6}" x2="{x:.1f}" y2="{top + n * row_h:.1f}" '
                   f'stroke="{GRID}" stroke-width="1"/>')
        out.append(_text(x, top + n * row_h + 17, f"{t:+.0f}%" if t else "0", 11, MUTED, "middle"))
        t += step
    x0 = sx(0)
    out.append(f'<line x1="{x0:.1f}" y1="{top - 6}" x2="{x0:.1f}" y2="{top + n * row_h:.1f}" '
               f'stroke="{INK}" stroke-width="1.4"/>')
    out.append(_text(x0 - 6, top - 12, "fewer crimes", 10.5, POSITIVE, "end", "600"))
    out.append(_text(x0 + 6, top - 12, "more crimes", 10.5, NEGATIVE, "start", "600"))

    for i, e in enumerate(items):
        y = top + i * row_h + row_h / 2
        col = POSITIVE if e.value < 0 else NEGATIVE
        for j, ln in enumerate(_wrap(e.label, max(20, int(label_w / 6.3)))[:1]):
            out.append(_text(label_w, y + 4, ln, 12.5, INK, "end"))
        if e.lo is not None and e.hi is not None:
            out.append(f'<line x1="{sx(e.lo):.1f}" y1="{y:.1f}" x2="{sx(e.hi):.1f}" y2="{y:.1f}" '
                       f'stroke="{col}" stroke-width="2.4" opacity="0.42"/>')
            for b in (e.lo, e.hi):
                out.append(f'<line x1="{sx(b):.1f}" y1="{y - 5:.1f}" x2="{sx(b):.1f}" '
                           f'y2="{y + 5:.1f}" stroke="{col}" stroke-width="2.4" opacity="0.42"/>')
        out.append(f'<circle cx="{sx(e.value):.1f}" cy="{y:.1f}" r="5.6" fill="{col}"/>')
        out.append(_text(width - 4, y + 4, f"{e.value:+.0f}%", 12.5, INK, "end", "600"))
    out.append("</svg>")
    return "".join(out)


# ------------------------------------------------------------------- line ---

def line(series: Sequence[tuple[str, Sequence[float], str | None]],
         xlabels: Sequence[str], width: int = 780, height: int = 320,
         unit: str = "", title: str = "", ymin: float = 0.0) -> str:
    # right margin must fit the inline series label, else it is clipped
    right = 22 + int(max(len(name) for name, _, _ in series) * 6.4)
    left, top, bottom = 66, 30 if title else 12, 40
    plot_w = width - left - right
    plot_h = height - top - bottom
    vmax = max(max(v for v in vals) for _, vals, _ in series)
    ticks = _nice_ticks(vmax)
    sy = lambda v: top + plot_h - (v - ymin) / (ticks[-1] - ymin) * plot_h  # noqa: E731
    n = len(xlabels)
    sx = lambda i: left + (plot_w * i / max(1, n - 1))  # noqa: E731

    out = [_open(width, height, title or "trend")]
    if title:
        out.append(_text(0, 14, title, 13.5, INK, weight="600"))
    for t in ticks:
        y = sy(t)
        out.append(f'<line x1="{left}" y1="{y:.1f}" x2="{width - right}" y2="{y:.1f}" '
                   f'stroke="{GRID}" stroke-width="1"/>')
        out.append(_text(left - 8, y + 4, _fmt(t, unit), 11, MUTED, "end"))
    for i, lab in enumerate(xlabels):
        out.append(_text(sx(i), top + plot_h + 18, lab, 11.5, MUTED, "middle"))
    # end-of-line labels can collide when series converge; nudge them apart
    ends = sorted(((sy(vals[-1]), k) for k, (_, vals, _) in enumerate(series)))
    placed: dict[int, float] = {}
    last_y = -1e9
    for yv, k in ends:
        y = yv if yv - last_y >= 14 else last_y + 14
        placed[k] = y
        last_y = y
    for k, (name, vals, colour) in enumerate(series):
        col = colour or _c(k)
        pts = " ".join(f"{sx(i):.1f},{sy(v):.1f}" for i, v in enumerate(vals))
        out.append(f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="2.6" '
                   f'stroke-linejoin="round" stroke-linecap="round"/>')
        for i, v in enumerate(vals):
            out.append(f'<circle cx="{sx(i):.1f}" cy="{sy(v):.1f}" r="3.6" fill="{col}"/>')
        out.append(_text(width - right + 8, placed[k] + 4, name, 11.5, col, "start", "600"))
    out.append(f'<line x1="{left}" y1="{top + plot_h}" x2="{width - right}" '
               f'y2="{top + plot_h}" stroke="{AXIS}" stroke-width="1"/>')
    out.append("</svg>")
    return "".join(out)


# ------------------------------------------------------------ stacked bar ---

def stacked(rows: Sequence[tuple[str, Sequence[float]]], keys: Sequence[str],
            width: int = 780, unit: str = "%", title: str = "",
            label_w: int = 190, row_h: int = 34) -> str:
    top = 48 if title else 30
    n = len(rows)
    h = top + n * (row_h + 12) + 10
    plot_x = label_w + 10
    plot_w = width - plot_x - 20
    out = [_open(width, h, title or "stacked bar")]
    if title:
        out.append(_text(0, 14, title, 13.5, INK, weight="600"))
    lx = plot_x
    for k, key in enumerate(keys):
        out.append(f'<rect x="{lx}" y="{top - 24}" width="11" height="11" rx="2" fill="{_c(k)}"/>')
        out.append(_text(lx + 16, top - 14, key, 11.5, MUTED))
        lx += 20 + len(key) * 6.6
    for i, (lab, vals) in enumerate(rows):
        y = top + i * (row_h + 12)
        total = sum(vals) or 1
        out.append(_text(label_w, y + row_h / 2 + 4, lab, 12.5, INK, "end"))
        x = plot_x
        for k, v in enumerate(vals):
            w = v / total * plot_w
            out.append(f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{row_h}" '
                       f'fill="{_c(k)}"/>')
            if w > 42:
                out.append(_text(x + w / 2, y + row_h / 2 + 4.5, _fmt(v, unit),
                                 12, "#ffffff", "middle", "600"))
            x += w
    out.append("</svg>")
    return "".join(out)


# --------------------------------------------------------- bounded ranges ---

@dataclass
class Range:
    label: str
    lo: float
    hi: float
    note: str = ""
    color: str | None = None


def rangebar(items: Sequence[Range], width: int = 780, label_w: int = 250,
             unit: str = "%", vmax: float = 100.0, title: str = "",
             row_h: int = 34, gap: int = 12) -> str:
    """Floating bars spanning lo..hi - for estimates that are genuinely a range.

    Used where a single point estimate would overstate what the sources support.
    """
    top = 30 if title else 10
    n = len(items)
    h = top + n * (row_h + gap) + 34
    plot_x = label_w + 10
    plot_w = width - plot_x - 96
    ticks = _nice_ticks(vmax)
    scale = plot_w / ticks[-1]

    out = [_open(width, h, title or "range chart")]
    if title:
        out.append(_text(0, 14, title, 13.5, INK, weight="600"))
    for t in ticks:
        x = plot_x + t * scale
        out.append(f'<line x1="{x:.1f}" y1="{top}" x2="{x:.1f}" '
                   f'y2="{top + n * (row_h + gap):.1f}" stroke="{GRID}" stroke-width="1"/>')
        out.append(_text(x, top + n * (row_h + gap) + 18, _fmt(t, unit), 11, MUTED, "middle"))
    for i, r in enumerate(items):
        y = top + i * (row_h + gap)
        col = r.color or _c(i)
        x0, x1 = plot_x + r.lo * scale, plot_x + r.hi * scale
        w = max(2.5, x1 - x0)
        for j, ln in enumerate(_wrap(r.label, 36)[:2]):
            out.append(_text(label_w, y + row_h / 2 + (4 if len(_wrap(r.label, 36)) == 1
                                                      else -2) + j * 13, ln, 12.5, INK, "end"))
        out.append(f'<rect x="{x0:.1f}" y="{y}" width="{w:.1f}" height="{row_h}" rx="2" '
                   f'fill="{col}" opacity="0.30"/>')
        for bx in (x0, x1):
            out.append(f'<line x1="{bx:.1f}" y1="{y}" x2="{bx:.1f}" y2="{y + row_h}" '
                       f'stroke="{col}" stroke-width="2.6"/>')
        lbl = (f"{r.lo:.0f}\u2013{r.hi:.0f}{unit}" if r.lo != r.hi
               else _fmt(r.hi, unit))
        out.append(_text(x1 + 8, y + row_h / 2 + 4.5, lbl, 12.5, INK, "start", "600"))
        if r.note:
            out.append(_text(plot_x + 8, y + row_h / 2 + 4.5, r.note, 11, MUTED))
    out.append(f'<line x1="{plot_x}" y1="{top}" x2="{plot_x}" '
               f'y2="{top + n * (row_h + gap):.1f}" stroke="{AXIS}" stroke-width="1"/>')
    out.append("</svg>")
    return "".join(out)


# ------------------------------------------------- single 100% segment bar ---

def segments(parts: Sequence[Bar], width: int = 780, height: int = 128,
             title: str = "", unit: str = "%") -> str:
    """One full-width bar split into labelled segments, with a callout legend."""
    top = 28 if title else 6
    bar_h = 52
    total = sum(p.value for p in parts) or 1
    out = [_open(width, height, title or "composition bar")]
    if title:
        out.append(_text(0, 14, title, 13.5, INK, weight="600"))
    x = 0.0
    for i, p in enumerate(parts):
        w = p.value / total * width
        col = p.color or _c(i)
        out.append(f'<rect x="{x:.1f}" y="{top}" width="{w:.1f}" height="{bar_h}" '
                   f'fill="{col}"/>')
        if w > 46:
            out.append(_text(x + w / 2, top + bar_h / 2 + 5, _fmt(p.value, unit),
                             13, "#ffffff", "middle", "700"))
        x += w
    x = 0.0
    for i, p in enumerate(parts):
        w = p.value / total * width
        if w > 74:
            for j, ln in enumerate(_wrap(p.label, max(9, int(w / 6.4)))[:2]):
                out.append(_text(x + w / 2, top + bar_h + 18 + j * 13, ln, 11.5,
                                 MUTED, "middle"))
        x += w
    out.append("</svg>")
    return "".join(out)


# ------------------------------------------------------- paired comparison ---

def pairbar(rows: Sequence[tuple[str, float, float]], keys: tuple[str, str],
            width: int = 780, label_w: int = 250, unit: str = "%",
            colors: tuple[str, str] = (POSITIVE, NEGATIVE),
            title: str = "", row_h: int = 15, gap: int = 13,
            vmax: float | None = None) -> str:
    """Two bars per row sharing one axis - for contrasting the same categories
    across two populations, where the *difference* is the message."""
    top = 50 if title else 32
    n = len(rows)
    h = top + n * (row_h * 2 + gap) + 34
    plot_x = label_w + 10
    plot_w = width - plot_x - 74
    vmax = vmax or max(max(a, b) for _, a, b in rows)
    ticks = _nice_ticks(vmax)
    scale = plot_w / ticks[-1]

    out = [_open(width, h, title or "paired bar chart")]
    if title:
        out.append(_text(0, 14, title, 13.5, INK, weight="600"))
    lx = plot_x
    for k, key in enumerate(keys):
        out.append(f'<rect x="{lx}" y="{top - 22}" width="11" height="11" rx="2" '
                   f'fill="{colors[k]}"/>')
        out.append(_text(lx + 16, top - 12, key, 11.5, MUTED))
        lx += 26 + len(key) * 6.6
    bottom_y = top + n * (row_h * 2 + gap)
    for t in ticks:
        x = plot_x + t * scale
        out.append(f'<line x1="{x:.1f}" y1="{top}" x2="{x:.1f}" y2="{bottom_y:.1f}" '
                   f'stroke="{GRID}" stroke-width="1"/>')
        out.append(_text(x, bottom_y + 18, _fmt(t, unit), 11, MUTED, "middle"))
    for i, (lab, a, b) in enumerate(rows):
        y = top + i * (row_h * 2 + gap)
        out.append(_text(label_w, y + row_h + 4, lab, 12.5, INK, "end"))
        for k, v in enumerate((a, b)):
            bw = max(1.2, v * scale)
            yy = y + k * row_h
            out.append(f'<rect x="{plot_x}" y="{yy}" width="{bw:.1f}" height="{row_h - 1.5}" '
                       f'rx="1.5" fill="{colors[k]}"/>')
            out.append(_text(plot_x + bw + 6, yy + row_h - 4, _fmt(v, unit, 1),
                             11, INK, "start", "600"))
    out.append(f'<line x1="{plot_x}" y1="{top}" x2="{plot_x}" y2="{bottom_y:.1f}" '
               f'stroke="{AXIS}" stroke-width="1"/>')
    out.append("</svg>")
    return "".join(out)
