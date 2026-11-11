# Steering — Offline-first

Aturan desain yang mengikat semua perubahan Field Kit:

1. **Offline dulu, online belakangan.** App harus jalan penuh tanpa internet:
   single HTML, tanpa CDN, tanpa font eksternal, tanpa API. Data di
   `localStorage` perangkat. Kalau butuh internet untuk jalan, itu bug.
2. **Tidak ada temuan yang dihapus diam-diam.** Status Final mengunci laporan.
   Mengubah laporan Final = buat inspeksi baru (Reset). Jangan tambahkan
   tombol "edit Final".
3. **Foto adalah bukti, bukan hiasan.** Item `photoRequired` tidak bisa Final
   tanpa foto. Foto menyimpan timestamp otomatis (+ GPS bila ada).
4. **Satu core, dua app.** Logika checklist, status, dan PDF tinggal di
   `core/` + `tools/template.html`. Jangan duplikasi logika ke app; ubah
   template, lalu jalankan `python3 tools/build.py`.
5. **Jangan lunakkan tes demi green.** Kalau tes gagal, perbaiki kode atau
   spec-nya — jangan hapus assertion-nya.
6. **Bahasa pengguna: Indonesia.** UI, instruksi, dan laporan berbahasa
   Indonesia. Istilah teknis (Draft/Final/PDF) boleh Inggris.
