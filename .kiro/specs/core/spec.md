# Field Kit — Core Spec

**Kategori:** Skeleton Crew (Kiroween 2026)
**Pemilik:** Fahmi Harun — Devpost https://devpost.com/fahmiharun0812
**Prinsip:** spec dulu, baru kode. Satu core template, dua app pembuktian.

## 1. Masalah
Inspeksi lapangan (kosan, warung makan) hari ini: foto tersebar di galeri HP,
catatan di kertas/chat, tidak ada laporan standar. Akibatnya sengketa deposit
dan klaim kebersihan sulit dibuktikan.

## 2. Core template (`/core`)
Satu-satunya kode yang dibagi kedua app:
- **Checklist engine** — template = daftar item (judul, instruksi singkat,
  `photoRequired` ya/tidak). Jawaban per item: `OK` / `Perlu perbaikan` /
  `Tidak berlaku` + catatan bebas.
- **Evidence** — tiap item bisa lampirkan foto + timestamp otomatis + GPS
  opsional. Foto disimpan lokal dulu (offline-first), di-downscale ke max
  1024px (JPEG 0.8) supaya localStorage tidak penuh.
- **Status** — `Draft → Final (terkunci) → PDF`. Final hanya bisa dicapai
  bila semua item terjawab dan semua item `photoRequired` sudah punya foto.
  Setelah Final, item tidak bisa diubah diam-diam; edit = inspeksi baru.
- **PDF 1-tap** — `window.print()` dengan CSS print: header (tempat, tanggal,
  pemeriksa, GPS), ringkasan skor, daftar temuan + foto bukti, tanda tangan.
- **Sync-when-online (rencana)** — data dibuat offline, diunggah saat online.
  Invarian: laporan offline-then-sync harus identik dengan laporan online.

## 3. Bukti template reusable
`tools/build.py` me-render `tools/template.html` + `core/templates.json`
menjadi `apps/movein/index.html` dan `apps/stallcheck/index.html`.
Satu template, dua domain. Mengubah template = mengubah kedua app sekaligus.

## 4. Tes
`python3 tools/test.py` — validasi template (10 item/app, id unik),
kecocokan item HTML vs `templates.json`, cek offline (tanpa referensi
eksternal), dan smoke test render di headless Chrome.
Logika core: `core/fieldkit.js` (`validateFinal`, `summarize`).

## 5. Yang sengaja TIDAK dibuat
- Tanpa server, tanpa akun, tanpa database.
- Tanpa OCR/vision (risiko gagal demo) — foto adalah bukti, bukan input ML.
- Tanpa MCP — tidak ada yang benar-benar membutuhkannya di MVP ini.
