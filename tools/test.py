#!/usr/bin/env python3
"""Tes Field Kit — jalankan dari root repo:  python3 tools/test.py
Keluar 0 = semua lolos. Tidak butuh internet, tidak butuh dependency luar.
"""
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = "/opt/meta-chromium/chrome"
passed = failed = 0


def check(name, ok, detail=""):
    global passed, failed
    if ok:
        passed += 1
        print(f"PASS {name}")
    else:
        failed += 1
        print(f"FAIL {name} {detail}")


def main():
    templates = json.loads((ROOT / "core" / "templates.json").read_text())
    # 1. Template: 10 item per app, id unik, field lengkap
    for app in ("movein", "stallcheck"):
        items = templates[app]["items"]
        check(f"templates.{app} 10 item", len(items) == 10, f"got {len(items)}")
        ids = [i["id"] for i in items]
        check(f"templates.{app} id unik", len(set(ids)) == len(ids))
        check(f"templates.{app} field lengkap",
              all(set(i) >= {"id", "title", "instruction", "photoRequired"} for i in items))
        check(f"templates.{app} photoRequired bool",
              all(isinstance(i["photoRequired"], bool) for i in items))

    # 2. HTML app: ITEMS sama persis dengan templates.json
    for app in ("movein", "stallcheck"):
        html = (ROOT / "apps" / app / "index.html").read_text()
        m = re.search(r"const ITEMS = (\[.*?\]);\n", html, re.S)
        check(f"{app} ITEMS ter-parse", bool(m))
        if m:
            items = json.loads(m.group(1))
            check(f"{app} ITEMS == templates.json", items == templates[app]["items"])
            check(f"{app} 10 item di HTML", len(items) == 10)
        # 3. Offline: tanpa referensi eksternal
        check(f"{app} tanpa referensi eksternal",
              not re.search(r"https?://|<script[^>]+src=|<link[^>]+href=", html))

    # 4. .kiro wajib ada di root
    for p in (".kiro/specs/core/spec.md", ".kiro/specs/movein/spec.md",
              ".kiro/specs/stallcheck/spec.md", ".kiro/steering/offline-first.md",
              ".kiro/hooks/hooks.json"):
        check(f".kiro {p} ada", (ROOT / p).exists())
    check(".kiro tidak di-.gitignore",
          not ((ROOT / ".gitignore").exists() and ".kiro" in (ROOT / ".gitignore").read_text()))

    # 5. Logika core (node, tanpa dependency)
    node = subprocess.run(
        ["node", "-e",
         "const f=require('./core/fieldkit.js');"
         "const items=[{id:'a',title:'A',photoRequired:true},{id:'b',title:'B',photoRequired:false}];"
         "const miss=f.validateFinal(items,{a:{status:'OK'}});"
         "if(miss.length!==2) throw new Error('validateFinal: '+JSON.stringify(miss));"
         "const s=f.summarize(items,{a:{status:'OK',photo:'x'},b:{status:'Perlu perbaikan',note:'n'}});"
         "if(s.counts.OK!==1||s.counts['Perlu perbaikan']!==1||s.findings.length!==1) throw new Error('summarize');"
         "console.log('core logic ok');"],
        cwd=ROOT, capture_output=True, text=True)
    check("core/fieldkit.js validateFinal+summarize", node.returncode == 0,
          node.stderr.strip()[:200])

    # 6. Smoke test interaksi di Chromium headless (Playwright)
    r = subprocess.run([sys.executable, "tools/smoke.py"], cwd=ROOT,
                       capture_output=True, text=True, timeout=300)
    print(r.stdout, end="")
    check("smoke test Playwright (render, simpan, gating Final, PDF)",
          r.returncode == 0, r.stderr.strip()[-300:] if r.returncode else "")

    print(f"\n{passed} lolos, {failed} gagal")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
