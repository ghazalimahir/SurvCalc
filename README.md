# mSurvey PWA v0.4.0 CLEAN

Pakej kemas kini bersih untuk GitHub Pages.

## Perubahan
- Ukur Trabas menyokong banyak garisan.
- Butang **+ Tambah Garisan** dan buang baris.
- Bearing penutup dibundarkan kepada 1 saat.
- Jarak penutup dipaparkan kepada 0.001 unit.
- Cache PWA dinaik taraf kepada `msurvey-v0.3.2` dan mengutamakan fail terkini dari rangkaian.

## Upload ke GitHub
Upload semua fail yang kelihatan dalam folder ini terus ke root repository `mSurvey`.
Jangan upload folder luarnya dan jangan upload fail ZIP.


## Tambahan v0.3.2
- Tikaian lurus dan nisbah tikaian.
- Jumlah jarak garisan.
- Perimeter trabas tertutup.
- Keluasan trabas daripada koordinat relatif terkumpul.

## Tambahan v0.3.3
Empat modul terakhir yang dahulu "Belum disahkan" kini diaktifkan. Formula diambil terus
daripada bytecode APK asal (kelas P6, P9, P10, P21 dalam classes.dex), bukan tekaan:
- **Hilang 2 Jarak** — hitung jarak 1-2 dan 1-3 daripada tiga bearing (1-2, 1-3, 2-3) dan jarak 2-3, guna petua sinus.
- **Sekan Lebar Sama** — bearing dan jarak titik sekan apabila lebar tikai daripada bearing belakang dan hadapan sama (titik pada pembahagi dua sudut).
- **Sekan Lebar Beza** — bearing dan jarak titik sekan apabila dua lebar tikai berbeza.
- **Sudut Dalam** — sudut dalam pada stesen tengah daripada koordinat tiga titik (belakang, tengah, hadapan).

## Tambahan v0.3.4
Pembetulan berdasarkan maklum balas selepas cuba semua modul di iPhone:
- **Format bearing dikemas kini** — output bearing/sudut kini dipaparkan `DDD° MM' SS.SS"` (contoh `090° 00' 00.00"`) menggantikan format lama `090.0000.00` yang mengelirukan (dua titik perpuluhan bertindih).
- **Butang tukar tanda (±)** ditambah pada setiap medan input berangka. Papan kekunci `decimal` di iPhone/Safari tiada kekunci tolak (`-`), jadi koordinat negatif (contoh Timur/Barat, Utara/Selatan) kini boleh dimasukkan dengan menekan butang ± di sebelah medan tanpa perlu menaip tanda tolak terus.
- Cache PWA dinaik taraf kepada `msurvey-v0.3.4`.

## Tambahan v0.4.0
Dua modul baharu — generalisasi "Hilang 2 Jarak" kepada trabas tertutup lebih daripada 3 sisi,
guna kaedah *omitted measurements* piawai dalam ukur (bukan reka-reka, formula matematik terbukti
dan disahkan dengan data sintetik + AutoCAD sebelum dilancarkan):
- **Trabas: Hilang 2 Jarak** — semua bearing diketahui, jarak semua garisan diketahui KECUALI 2
  garisan terakhir. Guna syarat penutupan trabas (Σ ΔN = 0, Σ ΔE = 0) diselesaikan sebagai sistem
  linear 2×2 (petua Cramer) untuk cari 2 jarak yang hilang.
- **Trabas: Hilang 2 Bearing** — semua jarak diketahui (termasuk 2 garisan terakhir), bearing 2
  garisan terakhir tidak diketahui. Diselesaikan sebagai persilangan dua bulatan (trilaterasi);
  memaparkan **2 kemungkinan penyelesaian** (cerminan geometri) — surveyor pilih mengikut susun
  atur sebenar di lapangan.
- Cache PWA dinaik taraf kepada `msurvey-v0.4.0`.
