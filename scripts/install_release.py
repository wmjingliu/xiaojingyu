"""Dry-run installer for the fixed local pet identity; --apply needs a reviewed sheet hash."""

import argparse
import hashlib
import json
import os
import shutil
import tempfile
import time
import uuid
from pathlib import Path

from validate_release import validate
from verify_app_format import verify

ROOT = Path(__file__).resolve().parents[1]
RELEASE = ROOT / "pet"
FILES = ("pet.json", "spritesheet.png", "LICENSE.txt")
ID = "xiaojingyu-keleus"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def target_path():
    home = Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex")
    pets = home / "pets"
    target = pets / ID
    if target.is_symlink() or (hasattr(target, "is_junction") and target.is_junction()):
        raise RuntimeError("Refusing symlink or junction target")
    if target.resolve().parent != pets.resolve():
        raise RuntimeError("Target escaped the pets directory")
    return pets, target


def fingerprint(folder):
    return {p.name: sha(p) for p in folder.iterdir() if p.is_file()}


def backup(target):
    root = ROOT / "backups/install"
    root.mkdir(parents=True, exist_ok=True)
    folder = root / (time.strftime("%Y%m%d-%H%M%S") + "-" + uuid.uuid4().hex[:6])
    folder.mkdir()
    if target.exists():
        shutil.copytree(target, folder / "pet")
        manifest = {"installed": True, "files": fingerprint(folder / "pet")}
    else:
        manifest = {"installed": False, "files": {}}
    (folder / "backup.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return folder


def install(args):
    validation = validate(RELEASE)
    if not validation["ok"]:
        raise RuntimeError(f"Invalid release: {validation['errors']}")
    if not verify(args.asar):
        raise RuntimeError("Unknown app format; inspect the current app before installation")
    pets, target = target_path()
    sheet_hash = validation["sheet_sha256"]
    if not args.apply:
        return {"dry_run": True, "identity": f"custom:{ID}", "target": str(target), "sheet_sha256": sheet_hash}
    if args.approved_hash != sheet_hash:
        raise RuntimeError("--approved-hash must match the exact previewed release sheet")
    pets.mkdir(parents=True, exist_ok=True)
    saved = backup(target)
    staging = Path(tempfile.mkdtemp(prefix="xiaojingyu-stage-", dir=pets.parent))
    displaced = pets.parent / ("xiaojingyu-displaced-" + uuid.uuid4().hex)
    try:
        for name in FILES:
            shutil.copy2(RELEASE / name, staging / name)
        if fingerprint(staging) != {name: sha(RELEASE / name) for name in FILES}:
            raise RuntimeError("Staging file hashes differ")
        if target.exists():
            target.rename(displaced)
        staging.rename(target)
    except Exception:
        if not target.exists() and displaced.exists():
            displaced.rename(target)
        raise
    finally:
        if staging.exists():
            shutil.rmtree(staging)
    if displaced.exists():
        displaced.rename(saved / "displaced-original")
    return {"installed": str(target), "backup": str(saved), "sheet_sha256": sha(target / "spritesheet.png"), "refresh_in_app": True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--asar", type=Path, required=True, help="Current desktop app resources/app.asar")
    parser.add_argument("--approved-hash", help="Exact SHA-256 of the reviewed sprite sheet; required with --apply")
    parser.add_argument("--apply", action="store_true", help="Install after validation and backup")
    args = parser.parse_args()
    print(json.dumps(install(args), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
