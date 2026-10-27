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
