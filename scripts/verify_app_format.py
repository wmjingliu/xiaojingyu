"""Read-only check for the desktop app's known v2 pet sheet format."""

import argparse
import json
import re
import struct
from pathlib import Path


def verify(asar):
    asar = Path(asar)
    with asar.open("rb") as handle:
        header = handle.read(16)
        if len(header) != 16:
            raise ValueError("Truncated app.asar")
        _, header_size, _, tree_length = struct.unpack("<4I", header)
        tree = json.loads(handle.read(tree_length))["files"]["webview"]["files"]["assets"]["files"]
        matches = [(name, item) for name, item in tree.items() if name.startswith("app-initial-") and name.endswith(".js")]
        if len(matches) != 1:
            return False
        _, item = matches[0]
        handle.seek(8 + header_size + int(item["offset"]))
        code = handle.read(item["size"]).decode("utf-8")
    checks = [
        r"version:2,width:1536,height:2288,cellWidth:192,cellHeight:208,columns:8,rows:11,requiredFramesByRow:\[6,8,8,4,5,8,6,6,6,8,8\]",
        r"review:\w+\(8,6,150,280\)",
        r"running:\w+\(7,6,120,220\)",
        r"waiting:\w+\(6,6,150,260\)",
    ]
    return all(re.search(pattern, code) for pattern in checks)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--asar", type=Path, required=True)
    args = parser.parse_args()
    ok = verify(args.asar)
    print(json.dumps({"known_v2_format": ok, "asar": str(args.asar)}, ensure_ascii=False))
    raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    main()
