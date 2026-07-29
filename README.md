# mSurvey PWA v0.3.4 CLEAN

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
