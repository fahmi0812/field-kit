# Cara membuat repo GitHub + push Field Kit

**Kenapa file ini ada:** pembuatan repo lewat konektor GitHub yang
terhubung (akun EnMiChan) **GAGAL** dengan error persis:
`POST https://api.github.com/user/repos: 403 Resource not accessible
by integration`. Token GitHub App tidak diizinkan membuat repository
baru untuk akun user — itu batasan integrasi, bukan salah isi.
Jadi repo harus dibuat dulu oleh pemilik akun (Fahmi), lalu EnMi
push isinya lewat konektor yang sama.

## Langkah 1 — Fahmi membuat repo kosong (2 menit)

1. Login GitHub sebagai **fahmi0812** di browser.
2. https://github.com/new
3. Repository name: `field-kit`
4. Description: `Offline-first field checklist template with photo evidence and one-tap PDF reports — MoveIn + StallCheck. Kiroween 2026, Skeleton Crew.`
5. Pilih **Public**. JANGAN centang "Add a README file" (biarkan kosong).
6. Create repository.

## Langkah 2 — beri EnMiChan akses push

Di halaman repo baru → **Settings → Collaborators → Add people** →
cari `EnMiChan` → undang sebagai **Write**. (Alternatif: di pengaturan
konektor GitHub, pilih repo `fahmi0812/field-kit` untuk instalasi
GitHub App Muse.)

## Langkah 3 — EnMi push isi repo

Setelah langkah 1–2 selesai, beri tahu EnMi. EnMi menjalankan
`push-files` konektor GitHub (snapshot, file UTF-8 saja) dari
`~/workspace/field-kit/` ke branch `main` dengan pesan
`Field Kit — Kiroween 2026 (Skeleton Crew): core template + MoveIn + StallCheck`.
Lalu EnMi verifikasi dari GitHub langsung (HEAD commit + semua file ada).

## File yang ikut push (UTF-8, total < 16 MiB)

README.md, .gitignore, .kiro/specs/*, .kiro/steering/*,
.kiro/hooks/hooks.json, core/templates.json, core/fieldkit.js,
apps/movein/index.html + README.md, apps/stallcheck/index.html +
README.md, tools/build.py, tools/test.py, tools/smoke.py,
tools/template.html, tools/make_video.py, demo/README.md,
docs/submission.md, docs/repo-push.md.

## File yang TIDAK bisa ikut push konektor (biner)

`demo/field-kit-demo.mp4`, `demo/frames/*.png`,
`docs/screenshots/*.png`, `docs/screenshots/*.pdf` — snapshot
konektor hanya menerima file UTF-8. Setelah push teks selesai,
upload file-file ini lewat web GitHub (drag-drop ke folder
`demo/` dan `docs/screenshots/`), atau biarkan video hanya di
YouTube (sudah cukup untuk syarat submit — repo tidak wajib
menyimpan MP4-nya).
