# Field Kit — Kiroween 2026 (Skeleton Crew)

**Satu template checklist lapangan offline-first + foto bukti + PDF 1-tap,
dibuktikan lewat 2 app yang benar-benar beda domain.**

| App | Untuk siapa | Masalah yang diselesaikan |
|---|---|---|
| **MoveIn** | Penyewa / agen kosan | Sengketa deposit karena kondisi awal kosan tidak terdokumentasi |
| **StallCheck** | Pemeriksa / pemilik warung makan | Kebersihan warung sulit dibuktikan tanpa laporan standar |

> Dibuat untuk [Kiroween 2026](https://kiroween.devpost.com/) — kategori
> **Skeleton Crew**. Deadline submit: **4 Des 2026 14:00 PT**
> (= 5 Des 2026 05:00 WIB). Oleh **Fahmi Harun**
> ([Devpost](https://devpost.com/fahmiharun0812)).

## Demo 60 detik

1. Buka `apps/movein/index.html` di HP/laptop — tanpa server, tanpa akun.
2. Isi nama kosan + pemeriksa, ambil GPS, jawab 10 item (OK / Perlu
   perbaikan / Tidak berlaku), lampirkan foto bukti.
3. Tekan **Final & kunci** → laporan terkunci → **PDF / Print** → PDF rapi.
4. Buka `apps/stallcheck/index.html` — core yang sama, checklist dan
   konteks berubah total. Itu inti Skeleton Crew: template reusable.

🎬 **Video demo (< 3 menit):** `demo/field-kit-demo.mp4`
(dan di YouTube — link menyusul setelah upload oleh pemilik akun).

## Cara jalanin (offline)

```bash
# tanpa build, tanpa install: buka file-nya langsung
open apps/movein/index.html      # macOS
xdg-open apps/movein/index.html  # Linux
# atau layani statis:  python3 -m http.server 8000
```

Tidak ada CDN, font eksternal, atau API — semua tersimpan lokal
(`localStorage`). Matikan internet, app tetap jalan penuh.

## Struktur

```
field-kit/
  .kiro/                  # WAJIB di root (syarat Devpost), jangan di-.gitignore
    specs/core/spec.md    # spec core template
    specs/movein/spec.md  # spec MoveIn
    specs/stallcheck/spec.md
    steering/offline-first.md
    hooks/hooks.json      # validasi template + rebuild app saat core berubah
  core/
    templates.json        # 10 item MoveIn + 10 item StallCheck
    fieldkit.js           # logika murni: validateFinal, summarize
  apps/movein/index.html      # di-render dari tools/template.html
  apps/stallcheck/index.html
  tools/
    build.py              # 1 template + templates.json -> 2 app
    test.py               # 24 tes (template, HTML, offline, .kiro, smoke)
    smoke.py              # tes interaksi di Chromium headless (Playwright)
    template.html         # template tunggal kedua app
  demo/field-kit-demo.mp4 # video demo < 3 menit
  docs/submission.md      # paket submission Devpost
```

## Cara pakai Kiro (untuk write-up Devpost)

- **Spec-driven (specs):** `.kiro/specs/core/spec.md` ditulis **sebelum**
  kode app; spec per app mengikuti core. Pola pemenang Skeleton Crew 2025
  (InteractionKit, Impulse Kit): template inti reusable + 2–3 app beda.
- **Steering:** `.kiro/steering/offline-first.md` — offline dulu, Final
  mengunci laporan, foto adalah bukti, satu core dua app, jangan lunakkan
  tes demi green.
- **Hooks:** `.kiro/hooks/hooks.json` — (1) `validate-template`: template
  harus lolos `python3 tools/test.py` sebelum app di-build ulang;
  (2) `rebuild-apps-on-core-change`: perubahan core → `build.py` +
  tes ulang kedua app. Jangan edit `apps/*/index.html` langsung.
- **Build & tes:**
  ```bash
  python3 tools/build.py   # render kedua app dari template
  python3 tools/test.py     # 24 tes — terakhir jalan: 24 lolos, 0 gagal
  ```
- **Model Kiro yang dipakai:** akun Free (Auto / Claude Sonnet 4.5 /
  open-weight). Kredit Kiroween 4.000 adalah saldo, bukan upgrade plan —
  model frontier (Opus, GPT-5.6) tetap butuh Pro, jadi tidak dipakai di sini.
  Build ini tidak bergantung pada model berbayar apa pun.

## Aturan laporan (steering, singkat)

- Draft → Final (terkunci) → PDF. Final butuh semua item terjawab dan semua
  item `photoRequired` berfoto. Setelah Final tidak bisa diubah diam-diam.
- Foto menyimpan timestamp otomatis (+ GPS bila diizinkan), di-downscale
  max 1024px (JPEG 0.8).

## Status

- [x] Spec core + 2 app (10 item masing-masing)
- [x] Tes: 24/24 lolos (termasuk smoke test interaksi di Chromium headless)
- [x] Repo publik GitHub + `/.kiro` di root
- [x] Video demo < 3 menit
- [ ] Upload video ke YouTube (butuh login pemilik akun)
- [ ] Submit Devpost (butuh login pemilik akun)

## Lisensi

MIT — bebas dipakai, termasuk untuk inspeksi lapangan sungguhan.
