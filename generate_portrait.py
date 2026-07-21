"""
Bonus utility (not part of the original reference repo): turns any photo into
the portrait.txt ASCII-art file that ascii_to_svg.py expects.

Usage:
    pip install pillow
    python generate_portrait.py my_photo.jpg

Then run ascii_to_svg.py to turn portrait.txt into SVG <tspan> markup, and
paste that block into light.svg / dark.svg.
"""

import sys
from pathlib import Path
from PIL import Image, ImageEnhance

COLS, ROWS = 120, 53          # matches the <g transform> box in light.svg / dark.svg
LEADING_BLANK_LINES = 4        # top padding to match the card layout
RAMP = " .:-=+*#%@"            # light -> dense. Works well for photos with a dark background.


def photo_to_ascii(path: str) -> str:
    src = Image.open(path).convert("L")
    w, h = src.size

    # Center-crop to a square, biased slightly toward the top (good for headshots)
    side = min(w, h)
    left = (w - side) // 2
    top = max(0, min((h - side) // 3, h - side))
    cropped = src.crop((left, top, left + side, top + side))

    resized = cropped.resize((COLS, ROWS), Image.LANCZOS)
    resized = ImageEnhance.Contrast(resized).enhance(1.15)
    resized = ImageEnhance.Brightness(resized).enhance(1.05)
    pixels = resized.load()

    lines = [""] * LEADING_BLANK_LINES
    for y in range(ROWS):
        row = []
        for x in range(COLS):
            brightness = pixels[x, y]
            idx = int((brightness / 255) * (len(RAMP) - 1))
            row.append(RAMP[idx])
        lines.append("".join(row).rstrip())

    return "\n".join(lines)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python generate_portrait.py <path-to-photo>")
        sys.exit(1)

    art = photo_to_ascii(sys.argv[1])
    Path("portrait.txt").write_text(art, encoding="utf-8")
    print("Wrote portrait.txt — now run: python ascii_to_svg.py")
