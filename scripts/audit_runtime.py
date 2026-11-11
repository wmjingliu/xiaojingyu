"""Read-only audit of the installed pet and the current desktop animation contract.

Unknown app code fails closed. This is a static gate, not a substitute for UI playback
and visual approval of every animation after a candidate asset update.
"""

import argparse
import hashlib
import json
import re
import struct
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_ROWS = {
    "idle": (0, 6),
    "running-right": (1, 8),
    "running-left": (2, 8),
    "waving": (3, 4),
    "jumping": (4, 5),
    "failed": (5, 8),
    "waiting": (6, 6),
    "running": (7, 6),
    "review": (8, 6),
}


def read_bundles(asar_path):
    with asar_path.open("rb") as f:
        header = f.read(16)
        if len(header) != 16:
            raise ValueError("Truncated asar header")
        _, size, _, length = struct.unpack("<4I", header)
        tree = json.loads(f.read(length))["files"]["webview"]["files"]["assets"]["files"]
        prefixes = ("app-initial-", "avatar-overlay-native-page-", "avatar-mascot-button-")
        result = {}
        for prefix in prefixes:
            matches = [(name, item) for name, item in tree.items() if name.startswith(prefix) and name.endswith(".js")]
            if len(matches) != 1:
                raise ValueError(f"Expected one {prefix} bundle; found {len(matches)}")
            name, item = matches[0]
            f.seek(8 + size + int(item["offset"]))
            blob = f.read(item["size"])
            result[prefix] = {"name": name, "sha256": hashlib.sha256(blob).hexdigest(), "text": blob.decode("utf8")}
        return result


def has(pattern, text):
    return re.search(pattern, text, flags=re.S) is not None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--asar", type=Path, required=True)
    parser.add_argument("--pet-dir", type=Path, required=True)
    parser.add_argument("--report", type=Path, help="Optional JSON output path; default is stdout only")
    args = parser.parse_args()

    bundles = read_bundles(args.asar)
    initial = bundles["app-initial-"]["text"]
    overlay = bundles["avatar-overlay-native-page-"]["text"]
    button = bundles["avatar-mascot-button-"]["text"]
    pet = json.loads((args.pet_dir / "pet.json").read_text(encoding="utf8"))
    sheet = args.pet_dir / pet["spritesheetPath"]
    with Image.open(sheet) as image:
        dimensions = list(image.size)
        mode = image.mode
    fmt = json.loads((ROOT / "codex-format.json").read_text(encoding="utf8"))

    checks = {
        "pet_identity_and_v2": args.pet_dir.name == "xiaojingyu-keleus" and pet.get("spriteVersionNumber") == 2,
        "geometry": dimensions == [1536, 2288] and mode == "RGBA" and fmt["requiredFramesByRow"] == [6, 8, 8, 4, 5, 8, 6, 6, 6, 8, 8],
        "renderer_rows": all(has(rf"(?:^|[,{{])(?:\"{re.escape(state)}\"|{re.escape(state)}):GX\({row},{count},", initial) for state, (row, count) in EXPECTED_ROWS.items() if state != "idle"),
        "renderer_default_non_looping": has(r"qGa=\(\{[^}]*loop:r=!1", initial),
        "renderer_three_cycles_then_idle": has(r"function MGa\(e,t,n=!1\).*?if\(n\)return\{frames:r,loopStartIndex:0\};let i=\[\.\.\.r,\.\.\.r,\.\.\.r\];return\{frames:\[\.\.\.i,\.\.\.RGa\]", initial),
        "overlay_calls_renderer_without_loop": has(r"\(0,N\.jsx\)\(g,\{[^}]*lookFrame:x,source:s,state:f\}", button),
        "profile_explicitly_loops": has(r"\(0,qYa\.jsx\)\(qGa,\{[^}]*loop:!0\}", initial),
        "overlay_state_prop": has(r"state:zt\.mascotState", overlay),
        "running_status": has(r"isLoading\)return\{[^}]*mascotState:`running`", overlay),
        "waiting_status": has(r"case`warning`:return\{[^}]*mascotState:`waiting`", overlay),
        "blocked_status": has(r"case`danger`:return\{[^}]*mascotState:`failed`", overlay),
        "ready_status": has(r"case`success`:return\{[^}]*mascotState:`review`", overlay),
        "idle_status": has(r"case`info`:return gd", overlay) and has(r"gd=\{[^}]*mascotState:`idle`", overlay),
        "ready_requires_unread": has(r"hasUnreadTurn\?`review`:`idle`", overlay) and has(r"has_unread_turn\?`review`:`idle`", overlay),
        "drag_directions": has(r"hr\(`running-right`\).*?hr\(`running-left`\)", overlay),
        "hover_jump": has(r"ne\?`jumping`:te", button),
        "first_awake_waves": has(r"kind===`first-awake`\)return _d", overlay) and has(r"_d=\{\.\.\.gd,mascotState:`waving`\}", overlay),
        "look_frame_can_preempt": has(r"if\(n!=null\)\{e\.style\.backgroundPosition=PGa\(n,p\);return\}", initial) and has(r"f===`idle`\|\|f===`running`\|\|f===`waving`", button),
        "pet_has_no_loop_configuration": not any("loop" in key.lower() for key in pet),
    }
    expected_running_ms = 3 * (5 * 120 + 220)
    sheet_hash = hashlib.sha256(sheet.read_bytes()).hexdigest()
    known_review_art = {
        "f2a70ab3c9359923883350913d1ca389e3e9bb27a287fb8eeb1eff03e8fd56f6": "thinking_at_desk",
        "b9f89cb64753b051b5bdb2a86c36b5898d3265462029002f720b2a1c8ea43566": "approved_small_wave_with_check",
    }.get(sheet_hash, "unknown_requires_visual_review")
    known_contract = all(checks.values())
    runtime_blockers = {
        "persistent_states_fall_back_to_idle": checks["renderer_three_cycles_then_idle"] and checks["overlay_calls_renderer_without_loop"],
        "ready_only_when_unread": checks["ready_requires_unread"],
        "look_frame_can_replace_running_animation": checks["look_frame_can_preempt"],
    }
    # This script recognizes the current implementation. If any pattern changes,
    # fail closed and inspect the new app version before changing the contract.
    asset_only_sufficient = known_contract and not any(runtime_blockers.values())
    result = {
        "asar": str(args.asar.resolve()),
        "pet_dir": str(args.pet_dir.resolve()),
        "installed_sheet_sha256": sheet_hash,
        "known_review_art": known_review_art,
        "bundle_sha256": {prefix: bundle["sha256"] for prefix, bundle in bundles.items()},
        "checks": checks,
        "observed_running_animation_before_idle_ms": expected_running_ms if all(checks[k] for k in ("renderer_default_non_looping", "renderer_three_cycles_then_idle", "overlay_calls_renderer_without_loop")) else None,
        "known_current_contract": known_contract,
        "runtime_blockers": runtime_blockers,
        "asset_only_sufficient_for_one_to_one": asset_only_sufficient,
        "candidate_visual_and_live_ui_review_required": known_review_art != "approved_small_wave_with_check",
        "live_ui_review_required": True,
        "blocking_reasons": [
            "Floating pet invokes the renderer without loop=true, so persistent states fall back to idle after three cycles.",
            "Ready is driven by unread completed activity, not by every result arrival.",
            ("The installed review row depicts thinking rather than completed delivery." if known_review_art == "thinking_at_desk" else
             "The installed review row has an approved completion cue, but live desktop playback remains unverified." if known_review_art == "approved_small_wave_with_check" else
             "The installed review row has unknown artwork and requires visual review."),
            ("Live UI playback remains required for the approved asset candidate." if known_review_art == "approved_small_wave_with_check" else
             "Live UI playback and human semantic review are required for the asset candidate."),
        ],
        "note": "Read-only audit. A future app change makes unknown patterns fail closed for manual inspection; this script never edits the app or installed pet.",
    }
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 2 if not known_contract else (0 if asset_only_sufficient else 1)


if __name__ == "__main__":
    raise SystemExit(main())
