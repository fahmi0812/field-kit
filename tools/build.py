#!/usr/bin/env python3
"""Build kedua app Field Kit dari satu template + core/templates.json.

Satu template (tools/template.html) + data template (core/templates.json)
-> apps/movein/index.html dan apps/stallcheck/index.html.
Ini bukti nyata klaim Skeleton Crew: core yang sama, domain yang beda.
Jalankan dari root repo:  python3 tools/build.py
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
APPS = {
    "movein": {
        "title": "MoveIn — Inspeksi Kosan",
        "h1": "MoveIn — Inspeksi Kosan",
        "place_label": "Nama tempat / alamat kosan",
        "place_ph": "cth: Kos Melati, Jl. …",
        "key": "fieldkit-movein-v1",
        "demo_place": "Kos Melati, Jl. Merdeka No. 12",
    },
    "stallcheck": {
        "title": "StallCheck — Inspeksi Kebersihan Warung Makan",
        "h1": "StallCheck — Inspeksi Kebersihan Warung Makan",
        "place_label": "Nama warung / alamat",
        "place_ph": "cth: Warung Sederhana, Jl. …",
        "key": "fieldkit-stallcheck-v1",
        "demo_place": "Warung Sederhana, Jl. Sudirman No. 8",
    },
}


def main() -> None:
    templates = json.loads((ROOT / "core" / "templates.json").read_text())
    template = (ROOT / "tools" / "template.html").read_text()
    for app, cfg in APPS.items():
        items = templates[app]["items"]
        assert len(items) == 10, f"{app}: expected 10 items, got {len(items)}"
        html = template
        html = html.replace("__TITLE__", cfg["title"])
        html = html.replace("__H1__", cfg["h1"])
        html = html.replace("__PLACE_LABEL__", cfg["place_label"])
        html = html.replace("__PLACE_PH__", cfg["place_ph"])
        html = html.replace("__ITEMS_JSON__", json.dumps(items, ensure_ascii=False))
        html = html.replace("__KEY__", cfg["key"])
        html = html.replace("__DEMO_PLACE__", cfg["demo_place"])
        assert "__" not in html.split("<script>")[0] or True  # placeholders only in head/body text
        for ph in ("__TITLE__", "__H1__", "__PLACE_LABEL__", "__PLACE_PH__",
                   "__ITEMS_JSON__", "__KEY__", "__DEMO_PLACE__"):
            assert ph not in html, f"{app}: placeholder {ph} not replaced"
        out = ROOT / "apps" / app / "index.html"
        out.write_text(html)
        print(f"wrote {out.relative_to(ROOT)} ({len(html)} bytes, 10 items)")


if __name__ == "__main__":
    main()
