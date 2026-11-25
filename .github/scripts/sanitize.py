#!/usr/bin/env python3
"""Bereinigte Kopien der ESPHome-Dateien erzeugen (ohne Secrets/Passwörter).
Aufruf: python3 .github/scripts/sanitize.py <Quellordner> <Zielordner>"""
import re, shutil, sys, pathlib

SRC = pathlib.Path(sys.argv[1]).resolve()
OUT = pathlib.Path(sys.argv[2]).resolve()
ROOTS = ["esphome"]          # Projektordner; ["."] = das ganze Repo
SKIP_DIRS = {".git", ".github", "sanitized", "dist", ".esphome", "node_modules"}
SKIP_FILES = {"secrets.yaml", "secrets.yml"}
KEEP_EXT = {".h", ".hpp", ".cpp", ".c", ".ttf", ".otf", ".wav", ".mp3",
            ".flac", ".png", ".jpg", ".jpeg", ".bmp", ".gif", ".svg"}
KEY_RE = re.compile(r"^(\s*(?:-\s+)*)([A-Za-z0-9_\-]+)\s*:(.*)$")


def sanitize(text):
    nodes, stack = [], []
    for line in text.splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            if "!secret" not in line:
                nodes.append(dict(t=line, keep=True, parent=None,
                                  block=False, touched=False))
            continue
        m = KEY_RE.match(line)
        if not m:
            nodes.append(dict(t=line, keep=True,
                              parent=stack[-1][2] if stack else None,
                              block=False, touched=False))
            continue
        level = len(m.group(1))
        key, val = m.group(2), m.group(3).strip()
        while stack and stack[-1][0] >= level:
            stack.pop()
        parent_idx = stack[-1][2] if stack else None
        parent_key = stack[-1][1] if stack else None
        drop = (
            key in ("password", "psk", "passphrase")
            or "!secret" in val
            or (key == "ssid" and parent_key == "wifi")
            or (key == "username" and parent_key == "auth")
            or (key == "key" and parent_key == "encryption")
        )
        idx = len(nodes)
        nodes.append(dict(t=line, keep=not drop, parent=parent_idx,
                          block=(val == "" or val.startswith("#")),
                          touched=False))
        if drop and parent_idx is not None:
            nodes[parent_idx]["touched"] = True
        elif not drop and val == "":
            stack.append((level, key, idx))

    kids = [0] * len(nodes)
    for n in nodes:
        if n["keep"] and n["parent"] is not None:
            kids[n["parent"]] += 1
    for i in range(len(nodes) - 1, -1, -1):
        n = nodes[i]
        if (n["keep"] and n["block"] and n["touched"]
                and n["parent"] is not None and kids[i] == 0):
            n["keep"] = False
            kids[n["parent"]] -= 1
            nodes[n["parent"]]["touched"] = True
    return "\n".join(n["t"] for n in nodes if n["keep"]) + "\n"


for root in ROOTS:
    for f in (SRC / root).rglob("*"):
        rel = f.relative_to(SRC)
        if (not f.is_file() or f.name in SKIP_FILES
                or any(p in SKIP_DIRS for p in rel.parts)):
            continue
        target = OUT / rel
        if f.suffix in (".yaml", ".yml"):
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(sanitize(f.read_text(encoding="utf-8")),
                              encoding="utf-8")
        elif f.suffix.lower() in KEEP_EXT:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, target)

for name in ("LICENSE", "THIRD_PARTY.md"):
    f = SRC / name
    if f.is_file():
        shutil.copy2(f, OUT / name)