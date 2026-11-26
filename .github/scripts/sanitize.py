#!/usr/bin/env python3
"""Bereinigte Kopien der ESPHome-Projektdateien erzeugen.

Entfernt alle Verweise auf Secrets sowie Passwörter und WLAN-Zugangsdaten,
damit die Dateien z. B. die Anforderungen von devices.esphome.io erfüllen.
Bearbeitet nur die Haupt-YAML und die YAMLs unter examples/.

Aufruf:  MAIN_YAML=esphome/tododisplay.yaml \
         python3 .github/scripts/sanitize.py <Quellordner> <Zielordner>
"""
import os
import pathlib
import re
import shutil
import sys

if len(sys.argv) != 3:
    sys.exit("Aufruf: sanitize.py <Quellordner> <Zielordner>")

SRC = pathlib.Path(sys.argv[1]).resolve()
OUT = pathlib.Path(sys.argv[2]).resolve()

MAIN_YAML = os.environ.get("MAIN_YAML", "esphome/tododisplay.yaml")
EXAMPLES_DIR = os.environ.get("EXAMPLES_DIR", "examples")
SKIP_FILES = {"secrets.yaml", "secrets.yml"}

# Wird unverändert kopiert, weil die bereinigte Haupt-YAML es zum Bauen braucht
COPY_PATHS = [
    "esphome/eink_header.h",
    "esphome/fonts",
    "esphome/audio",
    "LICENSE",
    "THIRD_PARTY.md",
]

KEY_RE = re.compile(r"^(\s*(?:-\s+)*)([A-Za-z0-9_\-]+)\s*:(.*)$")


def sanitize(text):
    nodes, stack = [], []
    for line in text.splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            # Kommentare mit Verweis auf Secrets entfallen
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

    # Leer gewordene Unterblöcke entfernen (oberste Schlüssel bleiben)
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


# --- Zu bereinigende Dateien: Haupt-YAML und examples/ ---------------------
targets = [pathlib.Path(MAIN_YAML)]
examples = SRC / EXAMPLES_DIR
if examples.is_dir():
    targets += [
        p.relative_to(SRC)
        for p in sorted(examples.rglob("*"))
        if p.is_file() and p.suffix in (".yaml", ".yml")
        and p.name not in SKIP_FILES
    ]

for rel in targets:
    source = SRC / rel
    if not source.is_file():
        sys.exit(f"Datei fehlt: {rel}")
    target = OUT / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(sanitize(source.read_text(encoding="utf-8")),
                      encoding="utf-8")
    print(f"bereinigt: {rel}")

# --- Dateien, die unverändert mitgehen -------------------------------------
for item in COPY_PATHS:
    p, t = SRC / item, OUT / item
    if p.is_dir():
        shutil.copytree(p, t, dirs_exist_ok=True)
        print(f"kopiert:   {item}/")
    elif p.is_file():
        t.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, t)
        print(f"kopiert:   {item}")