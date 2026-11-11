#!/usr/bin/env python3
"""Smoke test interaksi Field Kit di Chromium headless (Playwright).
Jalankan: python3 tools/smoke.py — keluar 0 = semua lolos.
"""
import pathlib
import sys

from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "tests" / "out"
OUT.mkdir(parents=True, exist_ok=True)

passed = failed = 0


def check(name, ok, detail=""):
    global passed, failed
    if ok:
        passed += 1
        print(f"PASS {name}")
    else:
        failed += 1
        print(f"FAIL {name} {detail}")


def test_app(pw, app):
    browser = pw.chromium.launch()
    page = browser.new_page(viewport={"width": 800, "height": 1400})
    url = f"file://{ROOT}/apps/{app}/index.html"
    page.goto(url)
    # 10 item ter-render
    items = page.locator(".item")
    check(f"{app} 10 item ter-render", items.count() == 10, f"got {items.count()}")
    # jawab item pertama OK -> tersimpan di localStorage
    items.nth(0).locator("button", has_text="OK").click()
    saved = page.evaluate("() => JSON.parse(localStorage.getItem('fieldkit-%s-v1')).answers" % app)
    check(f"{app} jawaban tersimpan localStorage",
          saved and list(saved.values())[0].get("status") == "OK", str(saved)[:120])
    # Final dengan item belum lengkap -> alert berisi daftar kekurangan
    dialog_text = []
    page.once("dialog", lambda d: (dialog_text.append(d.message), d.accept()))
    page.locator("#finalBtn").click()
    check(f"{app} Final diblokir bila belum lengkap",
          dialog_text and "Belum bisa Final" in dialog_text[0], str(dialog_text)[:120])
    check(f"{app} status tetap Draft setelah Final gagal",
          page.locator("#statusLabel").inner_text() == "Draft")
    # demo=final: ringkasan muncul, tombol PDF tampil
    page.goto(url + "?demo=final")
    page.wait_for_selector("#summary:not([hidden])", timeout=5000)
    check(f"{app} demo=final ringkasan tampil", True)
    summary = page.locator("#summary").inner_text()
    check(f"{app} ringkasan berisi hitungan", "OK: 8" in summary and "Perlu perbaikan: 2" in summary, summary[:160])
    check(f"{app} tombol PDF tampil setelah Final",
          page.locator("#printBtn").is_visible())
    check(f"{app} item terkunci setelah Final",
          page.locator(".item button").first.is_disabled())
    png = OUT / f"{app}-final.png"
    page.screenshot(path=str(png), full_page=True)
    check(f"{app} screenshot final", png.exists() and png.stat().st_size > 20000,
          f"size={png.stat().st_size if png.exists() else 0}")
    if app == "movein":
        pdf = OUT / "movein-final.pdf"
        page.pdf(path=str(pdf))
        check("MoveIn PDF 1-tap (print-to-pdf)", pdf.exists() and pdf.stat().st_size > 10000,
              f"size={pdf.stat().st_size if pdf.exists() else 0}")
    browser.close()


def main():
    with sync_playwright() as pw:
        test_app(pw, "movein")
        test_app(pw, "stallcheck")
    print(f"\n{passed} lolos, {failed} gagal")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
