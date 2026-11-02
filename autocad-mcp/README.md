# autocad-mcp

Sambungkan Claude ke AutoCAD / Civil 3D yang **sedang berjalan**, supaya Claude
boleh menjalankan command terus pada gambar yang terbuka — bukan sekadar
menghasilkan fail DXF atau LISP untuk anda muat sendiri.

```
Claude Code  <-- MCP (stdio) -->  acad_mcp.py  <-- COM -->  AutoCAD
```

Tiada .NET diperlukan.

---

## Anda tidak perlu tahu Python

Python hanyalah enjin di belakang. Anda tidak akan menulis atau membacanya.
Klik dua kali empat fail ini, ikut urutan:

| Klik dua kali | Apa jadi | Ubah gambar? |
|---|---|---|
| **`1-PASANG.bat`** | Pasang keperluan. Sekali sahaja | Tidak |
| **`2-UJI.bat`** | Uji sambungan ke AutoCAD | **Tidak** — baca sahaja |
| **`3-UJI-LUKIS.bat`** | Uji melukis garisan/bulatan/teks | Ya, pada layer `CLAUDE_UJIAN` |
| **`4-DAFTAR-CLAUDE.bat`** | Sambungkan ke Claude Code | Tidak |

Setiap fail menerangkan apa yang berlaku, berhenti untuk anda baca, dan tidak
menutup tetingkap sendiri. Kalau ada yang gagal, mesejnya menyebut sebab dan
apa yang perlu dibuat.

**Kalau `1-PASANG.bat` kata tiada Python:** muat turun dari
[python.org](https://www.python.org/downloads/windows/), pilih *Windows
installer (64-bit)*, dan **tandakan kotak `Add python.exe to PATH`** semasa
pemasangan. Kotak itu di bahagian bawah skrin pertama dan senang terlepas.
Lepas itu klik `1-PASANG.bat` semula.

Selepas langkah 4, anda bercakap dengan Claude macam biasa:

> "periksa status autocad"
> "lukis garisan dari 0,0 ke 100,50"
> "plot titik traverse ini dan labelkan"

---

## Keperluan

| | |
|---|---|
| OS | Windows (COM tidak ada di Mac/Linux) |
| AutoCAD | Versi penuh, bukan LT. Disasarkan: 2022 |
| Python | 3.10+, **64-bit** (mesti sama bit dengan AutoCAD) |
| Claude | Claude Code / Claude Desktop yang berjalan **di PC itu** |

Sesi Claude di laman web (claude.ai/code) **tidak boleh** guna ini. Ia berjalan
dalam container Linux di awan dan tiada akses ke mesin anda.

## Pindah ke laptop

Tak perlu USB. Ulang arahan yang sama:

```bat
git clone https://github.com/ghazalimahir/SurvCalc.git
cd SurvCalc
git checkout claude/pc-reset-issue-n9y76h
```

Kemudian masuk folder `autocad-mcp` dan klik `1-PASANG.bat` seperti biasa.

---

## Tool yang disediakan

**Baca**
- `acad_status` — periksa sambungan dan keadaan gambar
- `acad_list_layers` — senarai layer, warna, keadaan
- `acad_list_entities` — senarai entity, boleh tapis ikut layer

**Arahan mentah**
- `acad_command` — jalankan apa-apa command AutoCAD
- `acad_lisp` — jalankan AutoLISP, boleh tangkap nilai pulangan

**Melukis**
- `acad_set_layer` — buat/tukar layer aktif
- `acad_draw_line`, `acad_draw_circle`, `acad_draw_text`, `acad_draw_polyline`
- `acad_plot_points` — plot banyak titik survey + label sekali gus

**Paparan dan fail**
- `acad_zoom_extents`, `acad_save`

## Pasang secara manual (kalau tidak mahu guna .bat)

```bat
py -3 -m pip install -r requirements.txt
py -3 probe_acad.py
py -3 probe_acad.py --draw
claude mcp add autocad -- py -3 C:\laluan\penuh\ke\autocad-mcp\acad_mcp.py
```

Atau salin `mcp.json.contoh` jadi `.mcp.json` dalam folder projek dan betulkan
laluannya. Semak dengan `/mcp` dalam Claude Code.

## Catatan reka bentuk

**Menulis guna LISP, membaca guna COM.** Semua operasi menulis dihantar sebagai
LISP melalui `SendCommand`. Ini mengelak `VARIANT` array (punca utama kod COM
AutoCAD pecah antara versi) dan berkelakuan sama merentas versi. Operasi
membaca guna property COM, kerana `SendCommand` tidak memulangkan nilai.

**Saluran nilai pulangan.** COM tidak boleh membaca pembolehubah LISP. Tetapi
LISP boleh menulis ke sysvar `USERS1` dan COM boleh `GetVariable` — itulah cara
`acad_lisp(capture_result=True)` memulangkan hasil. Had 255 aksara.

**Command ditulis `_.XXXX`.** `_` = nama antarabangsa (tidak bergantung bahasa
antaramuka), `.` = abai redefinition. Jadi kod ini jalan pada AutoCAD berbahasa
apa pun.

**AutoCAD mesti idle.** `SendCommand` ditolak kalau ada command atau dialog
terbuka. Setiap tool memeriksa sysvar `CMDACTIVE` dahulu dan memberi mesej yang
jelas, bukan ralat COM mentah.

## Belum disiapkan

- **API Civil 3D sendiri** (COGO points, alignment, surface, parcel). Itu ProgID
  COM yang berasingan daripada `AutoCAD.Application`, dan nombor versinya
  berbeza ikut keluaran — perlu dikenal pasti di mesin sebenar dahulu.
- Operasi memilih dan mengubah entity yang sudah ada (`SSGET`).
- Export terus dari SurvCalc ke AutoCAD — SurvCalc ialah PWA dalam browser, jadi
  ia tiada akses COM. Jalur yang betul: SurvCalc keluarkan CSV/DXF, kemudian
  `acad_plot_points` memasukkannya.

## Status pengujian

Kod ini **belum diuji terhadap AutoCAD sebenar**. Ia ditulis dan disemak
sintaksnya dalam container Linux, yang tiada AutoCAD mahupun COM. Fail `.bat`
pula tidak boleh dijalankan di sana sama sekali. Pengujian sebenar adalah
langkah seterusnya di PC Windows.
