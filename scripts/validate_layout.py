"""Fail closed if an Oryx merge removes the custom chat integration."""
import argparse
from pathlib import Path
import re
import sys


def validate(folder, raw=False):
    code = (folder / "keymap.c").read_text(encoding="utf-8")
    if re.search(r"(?m)^(<<<<<<<|=======|>>>>>>>)", code):
        raise ValueError("Unresolved merge conflict in keymap.c.")
    if raw:
        if any(token in code for token in (
            "gaming_chat.h", "process_gaming_chat", "L_CHAT", "case KC_F24:"
        )) or (folder / "gaming_chat.h").exists():
            raise ValueError("The oryx branch contains custom chat code. Keep it a pure Oryx export; resolve merges on main, never merge main into oryx.")
        return
    if folder.name != "ZGMw7":
        raise ValueError("This protected workflow is configured for layout ZGMw7.")
    header = folder / "gaming_chat.h"
    if not header.is_file():
        raise ValueError("Missing gaming_chat.h; refusing to build without chat support.")
    if code.count('#include "gaming_chat.h"') != 1:
        raise ValueError("Missing or duplicated gaming_chat.h include.")
    entry = r"bool\s+process_record_user\s*\(uint16_t\s+keycode,\s*keyrecord_t\s*\*record\)\s*\{\s*if\s*\(!process_gaming_chat\(keycode,\s*record\)\)\s*\{\s*return false;\s*\}"
    if not re.search(entry, code):
        raise ValueError("Chat hook missing at the start of process_record_user. Restore it on main before building.")
    if len(re.findall(r"bool\s+process_record_user\s*\(", code)) != 1:
        raise ValueError("Expected exactly one process_record_user.")
    layers = {}
    for match in re.finditer(r"\[(\d+)\]\s*=\s*LAYOUT_voyager\(", code):
        start = pos = match.end()
        depth = 1
        keys = []
        while depth and pos < len(code):
            ch = code[pos]
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
            if (ch == "," and depth == 1) or depth == 0:
                keys.append(code[start:pos].strip())
                start = pos + 1
            pos += 1
        if depth or len(keys) != 52:
            raise ValueError("Invalid Voyager layer; expected 52 keys.")
        layers[int(match[1])] = keys
    if not {1, 2, 3}.issubset(layers):
        raise ValueError("Keep Gaming/G2/Chat at layers 1/2/3.")
    if "MO(2)" not in layers[1] or "KC_F24" not in layers[2]:
        raise ValueError("Gaming needs MO(2), and G2 needs F24 to open chat.")
    if not {"KC_ENTER", "KC_ESCAPE"}.issubset(layers[3]):
        raise ValueError("In Oryx, set plain Enter and Escape on Gaming Chat (layer 3), without hold actions. Compile again, then rerun this workflow.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder", type=Path)
    parser.add_argument("--oryx", action="store_true")
    args = parser.parse_args()
    try:
        validate(args.folder, args.oryx)
    except (ValueError, OSError) as error:
        print(f"::error::{error}", file=sys.stderr)
        sys.exit(1)
    print("Oryx/custom-code separation OK." if args.oryx else "Gaming chat integration OK.")
