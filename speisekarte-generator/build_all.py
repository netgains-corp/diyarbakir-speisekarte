# -*- coding: utf-8 -*-
"""Baut alles auf einmal: Speisekarte und Leuchttafeln, je mit und ohne Beschnitt.

    python3 build_all.py

Läuft jeder Teil in einem eigenen Prozess, weil BLEED_MM beim Import der
Skripte ausgewertet wird.
"""
import os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable


def run(script, **env):
    e = dict(os.environ, **{k: str(v) for k, v in env.items()})
    label = script + ("  " + "  ".join(f"{k}={v}" for k, v in env.items()) if env else "")
    print(f"→ {label}")
    r = subprocess.run([PY, os.path.join(HERE, script)], cwd=HERE, env=e,
                       capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stdout)
        print(r.stderr, file=sys.stderr)
        raise SystemExit(f"FEHLGESCHLAGEN: {label}")
    for line in r.stdout.splitlines():
        if "⚠" in line or "ZU HOCH" in line:
            print("   " + line.strip())


def main():
    t0 = time.time()

    print("\n== Speisekarte (A4) ==")
    run("build_menu.py")
    run("build_menu.py", BLEED_MM=3)

    print("\n== Leuchttafeln (200 x 60 cm) ==")
    run("build_tafeln.py")
    run("build_tafeln.py", BLEED_MM=3)

    print(f"\nFertig in {time.time() - t0:.0f} s.")
    print("Speisekarte:  " + HERE)
    print("Tafeln:       " + os.path.join(HERE, "tafeln"))


if __name__ == "__main__":
    main()
