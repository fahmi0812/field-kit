# StallCheck — Inspeksi Kebersihan Warung Makan (Field Kit)

Inspeksi kebersihan warung makan — laporan standar yang bisa dibuktikan.
Checklist: `core/templates.json` (stallcheck, 10 item).

Buka `index.html` di browser (HP/laptop) — tanpa server, tanpa akun:
10 item, jawaban OK / Perlu perbaikan / Tidak berlaku, foto bukti +
timestamp + GPS, tersimpan lokal (localStorage, offline-first), Final
mengunci laporan, lalu cetak / simpan PDF lewat tombol Print.

Core yang sama dengan MoveIn, domain yang beda — itu pembuktian
template reusable Field Kit.

File ini di-render dari `tools/template.html` oleh `tools/build.py` —
jangan edit langsung; ubah template lalu build ulang.
