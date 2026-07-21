"""
Converts portrait.txt (a plain-text ASCII-art rendering of a photo) into a block
of SVG <tspan> elements, ready to paste into light.svg / dark.svg inside the
<text class="ascii"> ... </text> block.

Run this again whenever you regenerate portrait.txt (e.g. from a new photo).
Output is written to portrait_tspan.txt.
"""

from pathlib import Path
from html import escape

INPUT = "portrait.txt"
OUTPUT = "portrait_tspan.txt"

# SVG placement — keep these in sync with the <g transform="translate(...) scale(...)">
# wrapper in light.svg / dark.svg so the art lines up correctly.
START_X = -10
START_Y = -30
LINE_HEIGHT = 9

# Optional trimming
TRIM_LEFT = 0
TRIM_RIGHT = 0

# Keep every portrait line (including blank padding lines)
REMOVE_EMPTY = False

lines = Path(INPUT).read_text(
    encoding="utf-8",
    errors="ignore"
).splitlines()

# remove trailing spaces only
lines = [l.rstrip() for l in lines]

if REMOVE_EMPTY:
    lines = [l for l in lines if l.strip()]

# trim columns if desired
processed = []
for line in lines:
    if TRIM_RIGHT > 0:
        line = line[:-TRIM_RIGHT]
    if TRIM_LEFT > 0:
        line = line[TRIM_LEFT:]
    processed.append(line)

y = START_Y
svg = []
for line in processed:
    if line.strip() == "":
        svg.append(f'<tspan x="{START_X}" y="{y}"/>')
    else:
        svg.append(f'<tspan x="{START_X}" y="{y}">{escape(line)}</tspan>')
    y += LINE_HEIGHT

Path(OUTPUT).write_text("\n".join(svg), encoding="utf-8")
print(f"Generated {len(svg)} tspans -> {OUTPUT}")
