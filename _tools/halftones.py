"""Halftone dot patterns for the website, used as CSS masks (so they take any colour).

Usage: python3 _tools/halftones.py assets/images
"""
import math
import sys

OUT = sys.argv[1]


def halftone(width, height, spacing, max_r, size_at, angle=45):
    """Dots on a rotated grid; size_at(x, y) gives 0..1 for the dot size there."""
    a = math.radians(angle)
    ca, sa = math.cos(a), math.sin(a)
    n = int(max(width, height) / spacing) * 2 + 4
    dots = []
    for i in range(-n, n):
        for j in range(-n, n):
            x = width / 2 + (i * ca - j * sa) * spacing
            y = height / 2 + (i * sa + j * ca) * spacing
            if not (-max_r <= x <= width + max_r and -max_r <= y <= height + max_r):
                continue
            r = max_r * size_at(x, y)
            if r > 0.35:
                dots.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.2f}"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
            f'width="{width}" height="{height}">' + "".join(dots) + "</svg>\n")


def clamp(v):
    return min(max(v, 0.0), 1.0)


patterns = {
    # A corner that grows toward the top right (profile card)
    "halftone-corner.svg": halftone(220, 220, 11, 4.6,
                                    lambda x, y: clamp((x / 220 + (1 - y / 220)) / 2 - 0.15) ** 1.5 * 1.35),
}
for name, svg in patterns.items():
    with open(f"{OUT}/{name}", "w") as fh:
        fh.write(svg)
    print(name, len(svg), "bytes")
