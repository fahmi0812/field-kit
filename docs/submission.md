# Paket Submission Devpost — Field Kit (Kiroween 2026)

**Status paket: SIAP.** Yang tersisa butuh login Fahmi sendiri: buat repo
GitHub (2 menit, lihat `docs/repo-push.md`), upload video ke YouTube
(lihat bawah), lalu klik submit di Devpost.

## 1. Isian Devpost (copy-paste)

- **Judul:** Field Kit — Offline-First Field Checklist Template
- **Tagline:** Satu template checklist lapangan offline + foto bukti +
  PDF 1-tap — dibuktikan MoveIn (inspeksi kosan) dan StallCheck
  (inspeksi kebersihan warung makan).
- **Kategori:** Skeleton Crew
- **Repo GitHub (publik):** https://github.com/fahmi0812/field-kit
  *(ganti dengan URL repo sebenarnya setelah dibuat — lihat
  `docs/repo-push.md`. Jangan submit dengan URL ini sebelum repo ada.)*
- **Video demo (YouTube, publik, < 3 menit):** *(isi link YouTube
  setelah upload `demo/field-kit-demo.mp4` — durasi 121,97 dtk)*
- **Deskripsi singkat:** Lihat `README.md` repo (bagian atas) — sudah
  ditulis sebagai deskripsi proyek.

## 2. Write-up: cara pakai Kiro (untuk kolom "How I used Kiro")

> Field Kit dibangun spec-first di Kiro. Saya menulis
> `.kiro/specs/core/spec.md` sebelum kode app: satu core template
> (checklist engine, evidence foto + timestamp + GPS, status
> Draft → Final → PDF) yang dipakai dua app.
> `.kiro/steering/offline-first.md` mengikat desain: offline dulu,
> Final mengunci laporan, foto adalah bukti.
> `.kiro/hooks/hooks.json` punya 2 hook: validasi template
> (`python3 tools/test.py`) dan rebuild kedua app dari satu template
> (`python3 tools/build.py`) setiap core berubah.
> Hasilnya: satu template (`tools/template.html` +
> `core/templates.json`) me-render dua app yang benar-benar beda
> domain — MoveIn (inspeksi kosan) dan StallCheck (inspeksi
> kebersihan warung makan). 24 tes otomatis lolos, termasuk smoke
> test interaksi di Chromium headless. Akun Kiro Free (Auto /
> Claude Sonnet 4.5); kredit Kiroween 4.000 dipakai sebagai saldo
> build, bukan untuk model frontier berbayar.

## 3. Checklist syarat submit (aturan resmi)

- [x] Repo GitHub **publik** — dibuat setelah langkah di
      `docs/repo-push.md` (repo belum ada saat paket ini ditulis;
      JANGAN klaim sudah ada)
- [x] Folder `/.kiro` di root repo (specs, steering, hooks) —
      dan TIDAK masuk `.gitignore` (sudah dicek tes)
- [x] Video demo publik **< 3 menit** — `demo/field-kit-demo.mp4`,
      121,97 dtk, 1280×720 (belum di-upload ke YouTube — butuh login Fahmi)
- [x] Proyek baru (dibuat mulai 30 Okt 2026, untuk Kiroween 2026)
- [x] App jalan pakai Kiro, repo berisi `/.kiro` di root
- [ ] Submit di Devpost sebelum **4 Des 2026 14:00 PT
      (= 5 Des 2026 05:00 WIB)** — butuh login Fahmi

## 4. Upload video ke YouTube (2 menit, oleh Fahmi)

1. Buka https://studio.youtube.com — login akun Google Fahmi.
2. Klik **Create → Upload videos** → pilih file
   `demo/field-kit-demo.mp4` (1,1 MB).
3. Judul: `Field Kit — Offline-First Field Checklist (Kiroween 2026 Demo)`
4. Deskripsi: tempel tagline + link repo GitHub + link Devpost
   https://kiroween.devpost.com/
5. Visibility: **Public** (wajib — video privat/unlisted tidak
   memenuhi syarat submit).
6. Publish → salin URL YouTube → tempel di kolom video Devpost (bagian 1).

## 5. Bonus yang masih bisa dikejar (opsional)

- **Bonus Blog (2.000 kredit × 100):** tulis blog publik tentang
  proses build Field Kit, tautkan dari submission.
- **Best Demo ($1.000):** video sudah < 3 menit dan menunjukkan alur
  lengkap 60 detik + PDF — sudah memenuhi syarat dasar.
- **Social Blitz:** posting dengan `#KiroweenHackathon26`.
