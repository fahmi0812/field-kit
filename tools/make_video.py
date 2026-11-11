#!/usr/bin/env python3
"""Buat video demo Field Kit (< 3 menit, bisu + teks di layar).

Jalankan dari root repo:  python3 tools/make_video.py
Output: demo/field-kit-demo.mp4 (1280x720, h264 + yuv420p, tanpa audio).

Alur:
  1. Playwright + Chromium headless: screenshot kedua app dalam state nyata
     (MoveIn kosong, MoveIn ?demo=draft, MoveIn ?demo=final,
     StallCheck ?demo=draft, StallCheck ?demo=final), viewport 1280x720.
  2. PIL: kartu judul / masalah / penutup + strip caption di tiap frame app.
  3. ffmpeg: rangkai semua frame jadi satu MP4 (concat demuxer).

Tidak mengubah isi app. Tidak butuh internet, tidak butuh login apa pun.
"""
import pathlib
import subprocess
import sys
import textwrap

from PIL import Image, ImageDraw, ImageFont

ROOT = pathlib.Path(__file__).resolve().parent.parent
DEMO = ROOT / "demo"
FRAMES = DEMO / "frames"
OUT = DEMO / "field-kit-demo.mp4"

W, H = 1280, 720
NAVY = (31, 42, 68)
NAVY_DARK = (20, 28, 48)
AMBER = (245, 197, 66)
WHITE = (255, 255, 255)
LIGHT = (205, 214, 230)
INK = (34, 34, 34)

FONT_REG = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Bungkus teks ke beberapa baris agar muat dalam max_w piksel."""
    lines = []
    for para in text.split("\n"):
        if not para:
            lines.append("")
            continue
        words, cur = para.split(), ""
        for w in words:
            trial = (cur + " " + w).strip()
            if draw.textlength(trial, font=fnt) <= max_w:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines


def card(path, title, subtitle, bullets, footer="Field Kit  ·  Kiroween 2026  ·  Skeleton Crew"):
    """Kartu judul/masalah/penutup layar penuh 1280x720."""
    img = Image.new("RGB", (W, H), NAVY_DARK)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 10], fill=AMBER)
    d.rectangle([0, H - 10, W, H], fill=AMBER)
    y = 120
    f_title = font(FONT_BOLD, 92 if len(title) <= 12 else 72)
    for line in wrap(d, title, f_title, W - 160):
        d.text((80, y), line, font=f_title, fill=WHITE)
        y += f_title.size + 14
    y += 10
    f_sub = font(FONT_REG, 38)
    for line in wrap(d, subtitle, f_sub, W - 160):
        d.text((80, y), line, font=f_sub, fill=AMBER)
        y += 52
    y += 18
    f_b = font(FONT_REG, 31)
    for b in bullets:
        for i, line in enumerate(wrap(d, b, f_b, W - 220)):
            d.text((80, y), "•" if i == 0 else " ", font=f_b, fill=AMBER)
            d.text((118, y), line, font=f_b, fill=LIGHT)
            y += 46
        y += 8
    d.text((80, H - 64), footer, font=font(FONT_REG, 24), fill=(140, 152, 175))
    img.save(path)
    print(f"card  {path.name}")


def caption_frame(shot_path, caption, out_path):
    """Tempel screenshot app (1280x628) + strip caption 92px di bawahnya."""
    shot = Image.open(shot_path).convert("RGB")
    if shot.size != (W, 628):
        shot = shot.resize((W, 628), Image.LANCZOS)
    frame = Image.new("RGB", (W, H), NAVY)
    frame.paste(shot, (0, 0))
    d = ImageDraw.Draw(frame)
    d.rectangle([0, 628, W, H], fill=NAVY)
    d.rectangle([0, 628, 10, H], fill=AMBER)
    f_cap = font(FONT_BOLD, 30)
    lines = wrap(d, caption, f_cap, W - 80)
    if len(lines) > 2:  # jaga-jaga: kecilkan font bila caption 3 baris
        f_cap = font(FONT_BOLD, 26)
        lines = wrap(d, caption, f_cap, W - 80)[:2]
    y = 628 + (92 - len(lines) * 36) // 2
    for line in lines:
        d.text((28, y), line, font=f_cap, fill=WHITE)
        y += 36
    frame.save(out_path)
    print(f"frame {out_path.name}  <- {caption}")


# ---------------------------------------------------------------- Playwright
def shoot():
    """Screenshot state nyata kedua app. Mengembalikan dict nama -> path PNG mentah."""
    from playwright.sync_api import sync_playwright

    raw = FRAMES / "raw"
    raw.mkdir(parents=True, exist_ok=True)
    shots = {}

    def grab(page, name, target=None, highlight=None):
        if target is None:
            page.evaluate("window.scrollTo(0, 0)")
        else:
            target.scroll_into_view_if_needed()
        if highlight:
            # Sorot tombol yang sedang dibahas (hanya di halaman, bukan di file app).
            page.evaluate(
                """(sel) => { const b = document.querySelector(sel);
                   b.style.outline = '5px solid #f5c542';
                   b.style.outlineOffset = '3px'; }""", highlight)
        page.wait_for_timeout(400)
        p = raw / f"{name}.png"
        page.screenshot(path=str(p))
        shots[name] = p
        print(f"shot  {name}")

    with sync_playwright() as pw:
        browser = pw.chromium.launch()

        # -- MoveIn kosong (state awal, localStorage bersih) --
        ctx = browser.new_context(viewport={"width": W, "height": H})
        page = ctx.new_page()
        page.goto(f"file://{ROOT}/apps/movein/index.html")
        page.wait_for_selector(".item")
        grab(page, "movein-empty")
        ctx.close()

        # -- MoveIn terisi (demo=draft) --
        ctx = browser.new_context(viewport={"width": W, "height": H})
        page = ctx.new_page()
        page.goto(f"file://{ROOT}/apps/movein/index.html?demo=draft")
        page.wait_for_selector(".item")
        grab(page, "movein-draft-top")
        grab(page, "movein-draft-photo", page.locator(".item").nth(1))
        grab(page, "movein-draft-lower", page.locator(".item").nth(7))
        ctx.close()

        # -- MoveIn Final (demo=final) --
        ctx = browser.new_context(viewport={"width": W, "height": H})
        page = ctx.new_page()
        page.goto(f"file://{ROOT}/apps/movein/index.html?demo=final")
        page.wait_for_selector("#summary:not([hidden])")
        grab(page, "movein-final-top")
        grab(page, "movein-final-summary", page.locator("#summary"))
        grab(page, "movein-final-pdf", page.locator(".actions"),
             highlight="#printBtn")
        ctx.close()

        # -- StallCheck terisi (demo=draft) --
        ctx = browser.new_context(viewport={"width": W, "height": H})
        page = ctx.new_page()
        page.goto(f"file://{ROOT}/apps/stallcheck/index.html?demo=draft")
        page.wait_for_selector(".item")
        grab(page, "stall-draft-top")
        grab(page, "stall-draft-photo", page.locator(".item").nth(1))
        grab(page, "stall-draft-lower", page.locator(".item").nth(7))
        ctx.close()

        # -- StallCheck Final (demo=final) --
        ctx = browser.new_context(viewport={"width": W, "height": H})
        page = ctx.new_page()
        page.goto(f"file://{ROOT}/apps/stallcheck/index.html?demo=final")
        page.wait_for_selector("#summary:not([hidden])")
        grab(page, "stall-final-top")
        grab(page, "stall-final-summary", page.locator("#summary"))
        ctx.close()

        browser.close()
    return shots


# ----------------------------------------------------------------- segmen
# (nama frame, durasi detik, sumber, caption / None untuk kartu)
SEGMENTS = [
    ("01-title", 8, "card", None),
    ("02-problem", 5, "card", None),
    ("03-movein-empty", 5, "movein-empty",
     "Masalahnya: inspeksi kosan tanpa bukti — kondisi awal tak tercatat."),
    ("04-movein-draft-top", 8, "movein-draft-top",
     "MoveIn: isi nama kosan, pemeriksa, lalu ambil lokasi (GPS)."),
    ("05-movein-draft-photo", 12, "movein-draft-photo",
     "Jawab 10 item — OK / Perlu perbaikan / Tidak berlaku — + foto bukti."),
    ("06-movein-draft-lower", 10, "movein-draft-lower",
     "Foto bukti tersimpan lokal di perangkat, lengkap dengan waktu & GPS."),
    ("07-movein-final-top", 6, "movein-final-top",
     "Final & kunci — laporan terkunci, tidak bisa diubah diam-diam."),
    ("08-movein-final-summary", 8, "movein-final-summary",
     "Ringkasan otomatis: OK 8 · Perlu perbaikan 2 · temuan tercatat."),
    ("09-movein-final-pdf", 6, "movein-final-pdf",
     "PDF 1-tap — tombol PDF / Print langsung dari laporan Final."),
    ("10-stall-draft-top", 8, "stall-draft-top",
     "StallCheck: core yang sama, domain beda — inspeksi warung makan."),
    ("11-stall-draft-photo", 12, "stall-draft-photo",
     "Checklist kebersihan warung: 10 item + foto bukti, cara pakai sama."),
    ("12-stall-draft-lower", 10, "stall-draft-lower",
     "Satu template — checklist & konteks berubah total antar app."),
    ("13-stall-final-top", 6, "stall-final-top",
     "StallCheck Final — terkunci seperti MoveIn, aturan yang sama."),
    ("14-stall-final-summary", 9, "stall-final-summary",
     "Ringkasan StallCheck: OK 8 · Perlu perbaikan 2 · siap dibuktikan."),
    ("15-closing", 10, "card", None),
]

CARDS = {
    "01-title": dict(
        title="FIELD KIT",
        subtitle="Satu template checklist lapangan offline-first + foto bukti + PDF 1-tap",
        bullets=["Dua app: MoveIn (inspeksi kosan)  ×  StallCheck (kebersihan warung makan)",
                 "Kiroween 2026  ·  Skeleton Crew  ·  oleh Fahmi Harun"]),
    "02-problem": dict(
        title="Masalahnya",
        subtitle="Inspeksi lapangan tanpa bukti itu rapuh.",
        bullets=["Kondisi awal kosan tak tercatat, berujung sengketa deposit saat pindah",
                 "Kebersihan warung sulit dibuktikan tanpa laporan standar",
                 "Laporan kertas hilang, tidak konsisten, tidak bisa dilacak"]),
    "15-closing": dict(
        title="Offline-first",
        subtitle="Tanpa server, tanpa akun, tanpa internet — tetap jalan penuh.",
        bullets=["Satu template, dua app beda domain. Itu inti Skeleton Crew.",
                 "Coba sendiri: buka apps/movein/index.html di browser — gratis.",
                 "Field Kit  ·  Kiroween 2026  ·  dibuat dengan Kiro"]),
}


def build_frames(shots):
    for name, _dur, src, caption in SEGMENTS:
        out = FRAMES / f"{name}.png"
        if src == "card":
            card(out, **CARDS[name])
        else:
            caption_frame(shots[src], caption, out)


def assemble():
    """Rangkai frame -> MP4 via ffmpeg concat demuxer."""
    total = sum(d for _, d, _, _ in SEGMENTS)
    print(f"total durasi rencana: {total} dtk ({len(SEGMENTS)} segmen)")
    assert total < 180, "video harus < 3 menit"
    lst = FRAMES / "concat.txt"
    with open(lst, "w") as f:
        for name, dur, _, _ in SEGMENTS:
            f.write(f"file '{FRAMES / (name + '.png')}'\n")
            f.write(f"duration {dur}\n")
        # concat demuxer butuh file terakhir diulang tanpa durasi
        f.write(f"file '{FRAMES / (SEGMENTS[-1][0] + '.png')}'\n")
    cmd = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(lst),
           "-vf", "format=yuv420p", "-c:v", "libx264", "-r", "30",
           "-crf", "20", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
           "-an", "-t", str(total), str(OUT)]
    # -t total: concat demuxer menambah ekor dari file terakhir tanpa
    # durasi; potong tepat di akhir segmen penutup agar durasi = rencana.
    print(" ".join(cmd))
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-3000:])
        sys.exit(1)
    print(f"OK {OUT} ({OUT.stat().st_size / 1e6:.2f} MB)")


def main():
    FRAMES.mkdir(parents=True, exist_ok=True)
    shots = shoot()
    build_frames(shots)
    assemble()


if __name__ == "__main__":
    main()
