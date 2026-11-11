"""Validate the local v2 pet sheet and every required animation cell."""

import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
COUNTS = [6, 8, 8, 4, 5, 8, 6, 6, 6, 8, 8]


def validate(pet_dir):
    pet_dir = Path(pet_dir)
    pet = json.loads((pet_dir / "pet.json").read_text(encoding="utf-8"))
    sheet = pet_dir / pet["spritesheetPath"]
    image = Image.open(sheet)
    errors = []
    if pet.get("spriteVersionNumber") != 2 or pet.get("spritesheetPath") != "spritesheet.png":
        errors.append("Expected v2 pet.json with spritesheet.png")
    if image.size != (1536, 2288) or image.mode != "RGBA":
        errors.append("Expected 1536×2288 RGBA sprite sheet")
    if image.size == (1536, 2288):
        for row, required in enumerate(COUNTS):
            hashes = []
            for col in range(8):
                frame = image.crop((col * 192, row * 208, (col + 1) * 192, (row + 1) * 208))
                alpha = frame.getchannel("A")
                if col >= required:
                    if alpha.getbbox():
                        errors.append(f"Unused cell {row}/{col} is not transparent")
                    continue
                box = alpha.point(lambda value: 255 if value > 16 else 0).getbbox()
                if not box:
                    errors.append(f"Empty cell {row}/{col}")
                elif box[0] < 2 or box[1] < 2 or box[2] > 190 or box[3] > 206:
                    errors.append(f"Insufficient margin in {row}/{col}: {box}")
                hashes.append(hashlib.sha256(frame.tobytes()).hexdigest())
            if len(set(hashes)) < min(required, 4):
                errors.append(f"Too few distinct frames in row {row}")
    return {"ok": not errors, "errors": errors, "required_cells": sum(COUNTS), "sheet_sha256": hashlib.sha256(sheet.read_bytes()).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pet-dir", type=Path, default=ROOT / "pet")
    args = parser.parse_args()
    report = validate(args.pet_dir)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    raise SystemExit(0 if report["ok"] else 1)


if __name__ == "__main__":
    main()
