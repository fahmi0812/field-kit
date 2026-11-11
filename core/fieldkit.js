// Field Kit — shared core engine (pure logic, no DOM).
// Aturan yang sama dipakai kedua app (MoveIn & StallCheck):
//   - jawaban per item: "OK" | "Perlu perbaikan" | "Tidak berlaku"
//   - item photoRequired wajib punya foto sebelum Final
//   - Final mengunci laporan (tidak bisa diubah diam-diam)
//   - ringkasan: hitung OK / Perlu perbaikan / Tidak berlaku / Belum dijawab + daftar temuan
// App HTML (hasil tools/build.py) mengimplementasikan aturan ini 1:1;
// file ini adalah sumber kebenaran yang dites di tests/test_core.py.
const STATUSES = ["OK", "Perlu perbaikan", "Tidak berlaku"];

function validateFinal(items, answers) {
  const missing = [];
  for (const it of items) {
    const a = answers[it.id] || {};
    if (!a.status) missing.push(it.title + " (belum dijawab)");
    else if (it.photoRequired && !a.photo) missing.push(it.title + " (foto wajib belum ada)");
  }
  return missing;
}

function summarize(items, answers) {
  const c = { OK: 0, "Perlu perbaikan": 0, "Tidak berlaku": 0, kosong: 0 };
  const findings = [];
  for (const it of items) {
    const st = (answers[it.id] || {}).status;
    if (c[st] != null) c[st]++;
    else c.kosong++;
    if (st === "Perlu perbaikan") {
      findings.push(it.title + (answers[it.id].note ? ": " + answers[it.id].note : ""));
    }
  }
  return { counts: c, findings };
}

if (typeof module !== "undefined") module.exports = { STATUSES, validateFinal, summarize };
