# autocad-mcp

Sambungkan Claude Code ke AutoCAD / Civil 3D yang **sedang berjalan**, supaya
Claude boleh menjalankan command terus pada gambar yang terbuka — bukan sekadar
menghasilkan fail DXF atau LISP untuk anda muat sendiri.

```
Claude Code  <-- MCP (stdio) -->  acad_mcp.py  <-- COM -->  AutoCAD
```

Tiada .NET diperlukan. Python + COM sahaja.

## Keperluan

| | |
|---|---|
| OS | Windows (COM tidak ada di Mac/Linux) |
| AutoCAD | Versi penuh, bukan LT. Diuji sasaran: 2022 |
| Python | 3.10 atau lebih baru, 64-bit (sama bit dengan AutoCAD) |
| Claude | Claude Code atau Claude Desktop yang berjalan **di PC itu** |

Sesi Claude di awan (claude.ai/code) **tidak boleh** guna ini — ia berjalan
dalam container Linux dan tiada akses ke mesin anda.

## Pasang

```bat
git clone https://github.com/ghazalimahir/survcalc.git
cd survcalc\autocad-mcp
py -3 -m pip install -r requirements.txt
```

## Langkah 1 — uji jalur COM dahulu

Buka AutoCAD dengan satu gambar, kemudian:

```bat
py -3 probe_acad.py
py -3 probe_acad.py --draw
```

`probe_acad.py` tidak melibatkan MCP sama sekali. Ia menguji tiga perkara:

1. **Baca** — versi AutoCAD, nama gambar, bilangan entity, layer aktif
2. **Dua hala** — hantar LISP `(setvar "USERS1" ...)`, baca balik dengan COM
3. **Lukis** (dengan `--draw`) — garisan, bulatan, teks pada layer `CLAUDE_UJIAN`

Kalau ketiga-tiganya lulus, MCP server pasti boleh jalan. Kalau gagal, mesej
ralatnya menyebut sebab yang mungkin (AutoCAD tak dibuka, LT, salah bit, dll).

Padam bentuk ujian: pilih layer `CLAUDE_UJIAN`, `ERASE`.

## Langkah 2 — daftar MCP server

```bat
claude mcp add autocad -- py -3 C:\laluan\penuh\ke\autocad-mcp\acad_mcp.py
```

Atau salin `mcp.json.contoh` jadi `.mcp.json` dalam folder projek anda dan
betulkan laluannya. Semak dengan `/mcp` dalam Claude Code.

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

## Catatan reka bentuk

**Menulis guna LISP, membaca guna COM.** Semua operasi menulis dihantar
sebagai LISP melalui `SendCommand`. Ini mengelak `VARIANT` array (punca utama
kod COM AutoCAD pecah antara versi) dan berkelakuan sama merentas versi.
Operasi membaca guna property COM, kerana `SendCommand` tidak memulangkan nilai.

**Saluran nilai pulangan.** COM tidak boleh membaca pembolehubah LISP. Tetapi
LISP boleh menulis ke sysvar `USERS1` dan COM boleh `GetVariable` — itulah cara
`acad_lisp(capture_result=True)` memulangkan hasil. Had 255 aksara.

**Command ditulis `_.XXXX`.** `_` = nama antarabangsa (tidak bergantung bahasa
antaramuka), `.` = abai redefinition. Jadi kod ini jalan pada AutoCAD berbahasa
apa pun.

**AutoCAD mesti idle.** `SendCommand` ditolak kalau ada command atau dialog
terbuka. Setiap tool memeriksa sysvar `CMDACTIVE` dahulu dan memberi mesej
yang jelas, bukan ralat COM mentah.

## Belum disiapkan

- **API Civil 3D sendiri** (COGO points, alignment, surface, parcel). Itu
  ProgID COM yang berasingan daripada `AutoCAD.Application`, dan nombor
  versinya berbeza ikut keluaran. Perlu dikenal pasti di mesin sebenar dahulu.
- Operasi memilih entity (`SSGET`) dan mengubah entity yang sudah ada.
- Export terus dari SurvCalc ke AutoCAD — SurvCalc ialah PWA dalam browser,
  jadi ia tiada akses COM. Jalur yang betul: SurvCalc keluarkan CSV/DXF,
  kemudian `acad_plot_points` memasukkannya.

## Status pengujian

Kod ini **belum diuji terhadap AutoCAD sebenar**. Ia ditulis dan disemak
sintaksnya dalam container Linux, yang tiada AutoCAD mahupun COM. Pengujian
sebenar adalah langkah seterusnya di PC Windows.
