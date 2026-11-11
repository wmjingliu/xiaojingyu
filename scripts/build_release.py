"""Rebuild the current sprite sheet from the frozen clarity base. No network calls."""

import argparse
import hashlib
import io
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "assets/clarity-base.png"
RELEASE = ROOT / "pet/spritesheet.png"
READY_SOURCES = [(3, 0), (3, 1), (3, 2), (3, 2), (3, 1), (3, 0)]
READY_OVERLAYS = ROOT / "assets/ready-overlays.png"
WAITING_OVERLAYS = ROOT / "assets/waiting-overlays.png"


def cell(sheet, row, col):
    return sheet.crop((col * 192, row * 208, (col + 1) * 192, (row + 1) * 208))


def build_bytes():
    base = Image.open(BASE).convert("RGBA")
    ready_overlay = Image.open(READY_OVERLAYS).convert("RGBA")
    waiting_overlay = Image.open(WAITING_OVERLAYS).convert("RGBA")
    if base.size != (1536, 2288):
        raise ValueError("The frozen clarity base must be 1536×2288")
    if ready_overlay.size != (1152, 208) or waiting_overlay.size != (1152, 208):
        raise ValueError("Each six-frame overlay must be 1152×208")
    result = base.copy()
    for col, (row, source_col) in enumerate(READY_SOURCES):
        frame = Image.alpha_composite(cell(base, row, source_col), ready_overlay.crop((col * 192, 0, (col + 1) * 192, 208)))
        result.paste(frame, (col * 192, 8 * 208))
    for col in range(6):
        frame = Image.alpha_composite(cell(base, 6, col), waiting_overlay.crop((col * 192, 0, (col + 1) * 192, 208)))
        result.paste(frame, (col * 192, 6 * 208))
    stream = io.BytesIO()
    result.save(stream, format="PNG", optimize=True)
    return stream.getvalue()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Write a new candidate file; existing files are never overwritten")
    args = parser.parse_args()
    data = build_bytes()
    digest = hashlib.sha256(data).hexdigest()
    current = hashlib.sha256(RELEASE.read_bytes()).hexdigest()
    print(f"rebuilt={digest}\nrelease={current}\nreproducible={digest == current}")
    if args.output:
        if args.output.exists():
            raise SystemExit(f"Refusing to overwrite {args.output}")
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_bytes(data)
    raise SystemExit(0 if digest == current else 1)


if __name__ == "__main__":
    main()
