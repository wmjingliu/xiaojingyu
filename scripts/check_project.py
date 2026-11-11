"""Verify that the publishable project is complete and the release is reproducible."""

import hashlib
import re
from pathlib import Path

from build_release import build_bytes
from validate_release import validate

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = "b9f89cb64753b051b5bdb2a86c36b5898d3265462029002f720b2a1c8ea43566"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    errors = []
    result = validate(ROOT / "pet")
    if not result["ok"]:
        errors.extend(result["errors"])
    if result["sheet_sha256"] != EXPECTED:
        errors.append("Release sprite SHA-256 differs from the approved version")
    if hashlib.sha256(build_bytes()).hexdigest() != EXPECTED:
        errors.append("Offline build does not reproduce the approved sprite")
    if sha(ROOT / "LICENSE") != sha(ROOT / "pet/LICENSE.txt"):
        errors.append("Root and package license files differ")
    page = (ROOT / "showcase/index.html").read_text(encoding="utf-8")
    images = re.findall(r'<img\b[^>]*\bsrc="([^"]+)"', page)
    if len(images) < 14:
        errors.append("The showcase has too few linked animations")
    errors.extend(f"Missing showcase image: {name}" for name in images if not (ROOT / "showcase" / name).is_file())
    if EXPECTED not in page:
        errors.append("Showcase hash does not identify the release")
    print(f"release={EXPECTED}\nrequired_frames={result['required_cells']}\nshowcase_links={len(images)}\nerrors={errors}")
    raise SystemExit(0 if not errors else 1)


if __name__ == "__main__":
    main()
