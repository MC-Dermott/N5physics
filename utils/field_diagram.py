"""SVG diagrams for Higher "Forces on Charged Particles": a particle entering a magnetic field
(into / out of the page, or field lines across the page), and the tubes of a linear accelerator.
Directions are (x, y, z) unit vectors: x to the right, y up the page, z out of the page."""

_NS = 'xmlns="http://www.w3.org/2000/svg"'
_FONT = 'font-family="Arial, sans-serif" font-size="13"'
_MARK = ('<defs><marker id="ah" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto">'
         '<path d="M0,0 L9,4.5 L0,9 z" fill="#111"/></marker></defs>')


def _arrow(x1, y1, x2, y2, w=2.2):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#111" stroke-width="{w}" marker-end="url(#ah)"/>'


def _text(x, y, s, anchor="middle"):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" {_FONT} fill="#111">{s}</text>'


def _out_symbol(x, y):
    return (f'<circle cx="{x}" cy="{y}" r="9" fill="white" stroke="#111" stroke-width="1.6"/>'
            f'<circle cx="{x}" cy="{y}" r="2.6" fill="#111"/>')


def _into_symbol(x, y):
    return (f'<circle cx="{x}" cy="{y}" r="9" fill="white" stroke="#111" stroke-width="1.6"/>'
            f'<path d="M{x-6},{y-6} L{x+6},{y+6} M{x-6},{y+6} L{x+6},{y-6}" stroke="#111" stroke-width="1.6"/>')


def field_entry_svg(b, v, particle):
    """A particle entering a region of magnetic field. b: field direction, v: velocity direction."""
    bx0, by0, bw, bh = 150, 62, 200, 150
    parts = [f'<rect x="{bx0}" y="{by0}" width="{bw}" height="{bh}" fill="#d9d9d9"/>']
    if b[2]:
        for i in range(5):
            for j in range(4):
                x, y = bx0 + 25 + i * 37.5, by0 + 22 + j * 35
                parts.append(f'<circle cx="{x}" cy="{y}" r="2.6" fill="#111"/>' if b[2] > 0 else
                             f'<path d="M{x-5},{y-5} L{x+5},{y+5} M{x-5},{y+5} L{x+5},{y-5}" stroke="#111" stroke-width="1.4"/>')
        label = "magnetic field out of page" if b[2] > 0 else "magnetic field into page"
    else:
        dx, dy = b[0], -b[1]
        for k in range(4):
            if dx:
                y = by0 + 22 + k * 35
                x1, x2 = (bx0 + 15, bx0 + bw - 15) if dx > 0 else (bx0 + bw - 15, bx0 + 15)
                parts.append(_arrow(x1, y, x2, y, 1.6))
            else:
                x = bx0 + 28 + k * 48
                y1, y2 = (by0 + 15, by0 + bh - 15) if dy > 0 else (by0 + bh - 15, by0 + 15)
                parts.append(_arrow(x, y1, x, y2, 1.6))
        label = {(1, 0): "magnetic field left to right", (-1, 0): "magnetic field right to left",
                 (0, 1): "magnetic field up the page", (0, -1): "magnetic field down the page"}[(b[0], b[1])]
    cx, cy = bx0 + bw / 2, by0 + bh / 2
    if v[2]:
        parts.append(_out_symbol(cx, cy) if v[2] > 0 else _into_symbol(cx, cy))
        parts.append(_text(bx0, by0 + bh + 38, f"{particle} moving {'out of' if v[2] > 0 else 'into'} the page", "start"))
        h = 285
    else:
        vx, vy = v[0], -v[1]
        if vx:
            y = cy
            x1, x2 = (bx0 - 110, bx0) if vx > 0 else (bx0 + bw + 110, bx0 + bw)
            parts.append(_arrow(x1, y, x2, y)); parts.append(f'<circle cx="{x1}" cy="{y}" r="4" fill="#111"/>')
            parts.append(_text(x1, y - 12, particle))
        else:
            x = bx0 + bw - 25
            y1, y2 = (by0 - 44, by0) if vy > 0 else (by0 + bh + 48, by0 + bh)
            # screen y grows downwards, so vy > 0 is a particle moving down the page
            parts.append(_arrow(x, y1, x, y2)); parts.append(f'<circle cx="{x}" cy="{y1}" r="4" fill="#111"/>')
            parts.append(_text(x + 12, y1 + (4 if vy > 0 else 12), particle, "start"))
        h = 285
    parts.append(_text(bx0, by0 + bh + 18, label, "start"))
    return f'<svg {_NS} viewBox="0 0 {bx0*2+bw} {h}" width="{bx0*2+bw}" height="{h}">{_MARK}{"".join(parts)}</svg>'


def linac_svg(kv):
    """Four hollow tubes joined alternately to an alternating supply."""
    xs, ln = [95, 190, 300, 430], [50, 78, 110, 150]
    p = [f'<line x1="30" y1="40" x2="{xs[2]+ln[2]/2}" y2="40" stroke="#111"/>',
         f'<line x1="30" y1="40" x2="30" y2="60" stroke="#111"/>',
         f'<line x1="30" y1="125" x2="30" y2="140" stroke="#111"/>',
         f'<line x1="30" y1="140" x2="{xs[3]+ln[3]/2}" y2="140" stroke="#111"/>',
         '<circle cx="30" cy="92" r="32" fill="white" stroke="#111" stroke-width="1.6"/>',
         '<text x="30" y="102" text-anchor="middle" font-size="28" font-family="Arial">~</text>']
    for i, (x, l) in enumerate(zip(xs, ln)):
        p.append(f'<rect x="{x}" y="68" width="{l}" height="48" fill="#d9d9d9" stroke="#111"/>'
                 f'<ellipse cx="{x}" cy="92" rx="8" ry="24" fill="#bbb" stroke="#111"/>'
                 + _text(x + l / 2 + 4, 97, "PQRS"[i]))
        cx = x + l / 2
        p.append(f'<line x1="{cx}" y1="40" x2="{cx}" y2="68" stroke="#111"/>' if i % 2 == 0 else
                 f'<line x1="{cx}" y1="116" x2="{cx}" y2="140" stroke="#111"/>')
    p.append(_arrow(xs[3] + ln[3] + 6, 92, xs[3] + ln[3] + 55, 92)); p.append(_text(xs[3] + ln[3] + 30, 78, "protons"))
    p.append(_text(30, 172, f"{kv:g} kV alternating supply", "start"))
    return f'<svg {_NS} viewBox="0 0 700 185" width="640" height="170">{_MARK}{"".join(p)}</svg>'


def deflection_svg(v, f, particle):
    """A particle entering a blank region of magnetic field and curving towards f (v, f in the page)."""
    bx0, by0, bw, bh = 150, 62, 200, 150
    cx, cy = bx0 + bw / 2, by0 + bh / 2
    vx, vy, fx, fy = v[0], -v[1], f[0], -f[1]
    # entry point on the edge the particle comes in through, path curves towards f
    sx, sy = cx - vx * bw / 2 if vx else cx - fx * 40, cy - vy * bh / 2 if vy else cy - fy * 30
    if vx:
        sx, sy = (bx0 if vx > 0 else bx0 + bw), cy - fy * 25
    else:
        sx, sy = cx - fx * 25, (by0 if vy > 0 else by0 + bh)
    ex, ey = sx + vx * 85 + fx * 55, sy + vy * 70 + fy * 55
    qx, qy = sx + vx * 85, sy + vy * 70
    parts = [f'<rect x="{bx0}" y="{by0}" width="{bw}" height="{bh}" fill="#d9d9d9"/>',
             _text(bx0, by0 + bh + 18, "region of magnetic field", "start")]
    if vx:
        x1 = bx0 - 110 if vx > 0 else bx0 + bw + 110
        parts.append(_arrow(x1, sy, sx, sy)); parts.append(f'<circle cx="{x1}" cy="{sy}" r="4" fill="#111"/>')
        parts.append(_text(x1, sy - 12, particle))
    else:
        y1 = by0 - 44 if vy > 0 else by0 + bh + 44
        parts.append(_arrow(sx, y1, sx, sy)); parts.append(f'<circle cx="{sx}" cy="{y1}" r="4" fill="#111"/>')
        parts.append(_text(sx + 12, y1 + (4 if vy > 0 else 12), particle, "start"))
    parts.append(f'<path d="M{sx},{sy} Q{qx},{qy} {ex},{ey}" fill="none" stroke="#111" stroke-width="2.2" '
                 f'stroke-dasharray="6,4" marker-end="url(#ah)"/>')
    return f'<svg {_NS} viewBox="0 0 {bx0*2+bw} 285" width="{bx0*2+bw}" height="285">{_MARK}{"".join(parts)}</svg>'


def wire_svg(kind, current, points=("P", "Q"), label="", arrow_label="current"):
    """kind 'end_on': a wire seen end-on (current +1 out of the page, -1 into it) with circles to guide the eye.
    kind 'in_plane': a vertical wire in the page (current +1 up the page, -1 down) with a point either side."""
    if kind == "end_on":
        parts = ['<circle cx="150" cy="115" r="38" fill="none" stroke="#bbb" stroke-dasharray="4,4"/>',
                 '<circle cx="150" cy="115" r="75" fill="none" stroke="#bbb" stroke-dasharray="4,4"/>',
                 _out_symbol(150, 115) if current > 0 else _into_symbol(150, 115),
                 _text(150, 222, label or "wire: current " + ("out of" if current > 0 else "into") + " the page")]
        return f'<svg {_NS} viewBox="0 0 300 235" width="300" height="235">{_MARK}{"".join(parts)}</svg>'
    parts = ['<line x1="150" y1="20" x2="150" y2="200" stroke="#111" stroke-width="5"/>',
             _arrow(150, 110 if current > 0 else 90, 150, 28 if current > 0 else 192, 2.6),
             _text(166, 36 if current > 0 else 190, arrow_label, "start"),
             '<circle cx="70" cy="110" r="5" fill="#111"/>', _text(70, 132, points[0]),
             '<circle cx="230" cy="110" r="5" fill="#111"/>', _text(230, 132, points[1])]
    return f'<svg {_NS} viewBox="0 0 300 215" width="300" height="215">{_MARK}{"".join(parts)}</svg>'


# ── Bar-magnet field patterns ──────────────────────────────────────────────────
import functools as _ft
import math as _math

_MAGNET_SCALE, _MAGNET_CX, _MAGNET_CY = 26.0, 190.0, 118.0


def _pole_field(x, y, poles):
    bx = by = 0.0
    for px, py, q in poles:
        dx, dy = x - px, y - py
        r2 = dx * dx + dy * dy + 1e-12
        r3 = r2 * _math.sqrt(r2)
        bx += q * dx / r3
        by += q * dy / r3
    return bx, by


def _trace_line(start, poles, ends, limit, step=0.04, max_steps=3000):
    x, y = start
    pts = [(x, y)]

    def f(px, py):
        bx, by = _pole_field(px, py, poles)
        n = _math.hypot(bx, by) + 1e-12
        return bx / n, by / n

    for _ in range(max_steps):
        k1 = f(x, y); k2 = f(x + step / 2 * k1[0], y + step / 2 * k1[1])
        k3 = f(x + step / 2 * k2[0], y + step / 2 * k2[1]); k4 = f(x + step * k3[0], y + step * k3[1])
        x += step / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
        y += step / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
        pts.append((x, y))
        if any(_math.hypot(x - ex, y - ey) < 0.12 for ex, ey in ends):
            break
        if abs(x) > limit[0] or abs(y) > limit[1]:
            break
    return pts


@_ft.lru_cache(maxsize=None)
def magnet_svg(kind, show_points=False, label_poles=True):
    """Field lines between/around bar magnets. kind: 'single' (one magnet, S on the left, N on the right),
    'unlike' (the N pole of the left magnet faces the S pole of the right one), 'nn' (north poles facing),
    'ss' (south poles facing). Poles are drawn as P and Q when label_poles is False (the pole on the left
    is P, the pole on the right is Q); show_points adds a point X in the gap and Y above it."""
    if kind == "single":
        mags, xlim, ylim = [(-1.6, 1.6, True)], (-4.4, 4.4), (-4.2, 4.2)
        angles = [-130, -108, -90, -76, 76, 90, 108, 130]
        keep_open = False
    elif kind == "unlike":
        mags, xlim, ylim = [(-9.0, -1.6, True), (1.6, 9.0, True)], (-4.6, 4.6), (-4.3, 4.3)
        angles = [-100, -70, -40, -15, 0, 15, 40, 70, 100]
        keep_open = False
    else:  # 'nn' / 'ss' share a geometry; for 'ss' the arrows and pole colours are reversed
        mags, xlim, ylim = [(-4.6, -1.6, True), (1.6, 4.6, False)], (-6.2, 6.2), (-4.3, 4.3)
        angles = [-100, -70, -40, -15, 15, 40, 70, 100]
        keep_open = True
    reverse = kind == "ss"
    poles = []
    for x0, x1, n_right in mags:
        poles.append((x0, 0.0, -1 if n_right else 1))
        poles.append((x1, 0.0, 1 if n_right else -1))
    s_poles = [(x, y) for x, y, q in poles if q < 0]
    sx = lambda x: _MAGNET_CX + x * _MAGNET_SCALE
    sy = lambda y: _MAGNET_CY - y * _MAGNET_SCALE
    w, h = int(2 * _MAGNET_CX), int(2 * _MAGNET_CY)
    parts = []
    # field lines (drawn first so the magnets sit on top)
    for nx, ny, q in poles:
        if q < 0:
            continue
        out = 1 if any(abs(nx - m[1]) < 1e-9 for m in mags) else -1
        for a in angles:
            th = _math.radians(a)
            pts = _trace_line((nx + out * 0.13 * _math.cos(th), ny + 0.13 * _math.sin(th)), poles, s_poles,
                              (abs(xlim[0]) + 0.6, abs(ylim[0]) + 0.6))
            ends_ok = any(_math.hypot(pts[-1][0] - ex, pts[-1][1] - ey) < 0.2 for ex, ey in s_poles)
            if not ends_ok and not keep_open:
                continue
            vis = [p for p in pts if xlim[0] < p[0] < xlim[1] and ylim[0] < p[1] < ylim[1]]
            if len(vis) < 8:
                continue
            vis = vis[::3] if len(vis) > 60 else vis
            path = "M" + " L".join(f"{sx(x):.1f},{sy(y):.1f}" for x, y in vis)
            parts.append(f'<path d="{path}" fill="none" stroke="#111" stroke-width="1.6"/>')
            seq = vis[::-1] if reverse else vis
            i = max(1, min(len(seq) - 2, int(len(seq) * (0.5 if ends_ok else 0.45))))
            (x1, y1), (x2, y2) = seq[i - 1], seq[i + 1]
            ang = _math.atan2(sy(y2) - sy(y1), sx(x2) - sx(x1))
            cx, cy = sx(seq[i][0]), sy(seq[i][1])
            tip = (cx + 6 * _math.cos(ang), cy + 6 * _math.sin(ang))
            l = (cx + 5 * _math.cos(ang + 2.5), cy + 5 * _math.sin(ang + 2.5))
            r = (cx + 5 * _math.cos(ang - 2.5), cy + 5 * _math.sin(ang - 2.5))
            parts.append(f'<polygon points="{tip[0]:.1f},{tip[1]:.1f} {l[0]:.1f},{l[1]:.1f} {r[0]:.1f},{r[1]:.1f}" fill="#111"/>')
    # magnets
    hh = 0.4
    for x0, x1, n_right in mags:
        n_right = (not n_right) if reverse else n_right
        xm = (x0 + x1) / 2
        halves = [(x0, xm, "S" if n_right else "N"), (xm, x1, "N" if n_right else "S")]
        for a, b, pole in halves:
            fill = "#f4b6b6" if pole == "N" else "#b6c9f4"
            if not label_poles:
                fill = "#d9d9d9"
            xa, xb = max(sx(a), 0), min(sx(b), w)
            if xb <= xa:
                continue
            parts.append(f'<rect x="{xa:.1f}" y="{sy(hh):.1f}" width="{xb - xa:.1f}" height="{2 * hh * _MAGNET_SCALE:.1f}" '
                         f'fill="{fill}" stroke="#111" stroke-width="1.6"/>')
            if label_poles and xlim[0] < (a + b) / 2 < xlim[1]:
                parts.append(f'<text x="{sx((a + b) / 2):.1f}" y="{sy(0) + 6:.1f}" text-anchor="middle" font-family="Arial, sans-serif" '
                             f'font-size="17" font-weight="bold" fill="#111">{pole}</text>')
    if not label_poles and kind == "unlike":
        parts.append(_text(sx(-2.3), sy(0) + 6, "P")); parts.append(_text(sx(2.3), sy(0) + 6, "Q"))
    if show_points:
        for px, py, name in ((0.0, 0.0, "X"), (0.0, 2.7, "Y")):
            parts.append(f'<path d="M{sx(px) - 5:.1f},{sy(py) - 5:.1f} L{sx(px) + 5:.1f},{sy(py) + 5:.1f} '
                         f'M{sx(px) - 5:.1f},{sy(py) + 5:.1f} L{sx(px) + 5:.1f},{sy(py) - 5:.1f}" stroke="#111" stroke-width="2.2"/>')
            parts.append(_text(sx(px) + 14, sy(py) - 8, f"<tspan font-weight='bold'>{name}</tspan>"))
    return f'<svg {_NS} viewBox="0 0 {w} {h}" width="{w}" height="{h}">{"".join(parts)}</svg>'
