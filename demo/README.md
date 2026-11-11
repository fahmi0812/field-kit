# Video demo Field Kit

`field-kit-demo.mp4` — video demo resmi Field Kit untuk Kiroween 2026
(Skeleton Crew). **Bisu, tanpa audio** — semua penjelasan ada sebagai teks
di layar (kartu judul/masalah/penutup + strip caption di tiap frame app).

- Durasi: **121,97 detik** (< 3 menit, sesuai syarat Devpost)
- Resolusi: **1280×720**, H.264 + yuv420p (bisa diputar di mana saja)
- Ukuran: **~1,1 MB** · 15 segmen · 30 fps

## Isi video

| Waktu | Segmen |
|---|---|
| 0:00–0:08 | Judul: Field Kit + Skeleton Crew |
| 0:08–0:18 | Masalah: inspeksi tanpa bukti (kartu + MoveIn kosong) |
| 0:18–0:48 | MoveIn: isi 10 item + foto bukti + GPS |
| 0:48–1:08 | MoveIn Final & kunci + ringkasan + PDF 1-tap |
| 1:08–1:38 | StallCheck: core sama, domain beda |
| 1:38–1:53 | StallCheck Final + ringkasan |
| 1:53–2:02 | Penutup: offline-first + cara coba |

Semua cuplikan app adalah screenshot nyata dari `apps/movein/index.html`
dan `apps/stallcheck/index.html` dalam mode demo (`?demo=draft` /
`?demo=final`) — jawaban, foto placeholder, GPS demo, dan ringkasan
(OK 8 · Perlu perbaikan 2) semuanya asli dari app.

## Regenerate

```bash
# dari root repo field-kit/
python3 tools/make_video.py
```

Butuh: Python 3.12 + Playwright + Chromium headless, ffmpeg, font
Noto Sans (`/usr/share/fonts/truetype/noto/`). Tidak butuh internet.

Skrip `tools/make_video.py` melakukan 3 langkah:

1. **Screenshot** — Playwright membuka kedua app (viewport 1280×720)
   dalam state kosong / `?demo=draft` / `?demo=final`, termasuk scroll
   ke item berfoto, ringkasan, dan tombol PDF (disorot outline kuning).
2. **Frame** — PIL membuat 3 kartu teks (judul/masalah/penutup) dan
   menempel strip caption di bawah tiap screenshot app.
3. **Rangkai** — ffmpeg (concat demuxer, libx264, crf 20, yuv420p,
   `-t` tepat 123 dtk rencana) menjadi `demo/field-kit-demo.mp4`.

Frame perantara tersimpan di `demo/frames/` (`*.png` final +
`raw/` screenshot mentah + `concat.txt`) — aman dihapus, dibuat ulang
tiap kali skrip dijalankan.

## Catatan

- Video ini **belum di-upload ke YouTube** — upload butuh login
  pemilik akun (Fahmi). File MP4 ini yang di-upload nanti.
- Isi app tidak diubah untuk video ini; kalau app berubah, jalankan
  ulang `python3 tools/test.py` lalu regenerate video ini.
