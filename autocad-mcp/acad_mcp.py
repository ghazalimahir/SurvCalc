"""MCP server: sambungkan Claude Code ke AutoCAD yang sedang berjalan.

    Claude Code  <-- MCP (stdio) -->  server ini  <-- COM -->  AutoCAD

Windows sahaja, AutoCAD penuh (bukan LT). Pasang:

    py -3 -m pip install "mcp[cli]" pywin32

Daftar ke Claude Code (jalankan di folder projek anda):

    claude mcp add autocad -- py -3 C:\\laluan\\ke\\autocad-mcp\\acad_mcp.py

Reka bentuk: semua operasi MENULIS dibuat melalui LISP yang dihantar dengan
SendCommand, bukan melalui objek COM terus. Sebabnya LISP tidak memerlukan
VARIANT array dan berkelakuan sama merentas versi AutoCAD. Operasi MEMBACA
guna property COM, kerana itu satu-satunya cara mendapat nilai pulangan.
"""

import sys

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    sys.exit('Pakej MCP belum dipasang. Jalankan: py -3 -m pip install "mcp[cli]" pywin32')

mcp = FastMCP("autocad")

_acad = None  # cache sambungan COM


# --------------------------------------------------------------------------
# Lapisan sambungan
# --------------------------------------------------------------------------

def _doc():
    """Pulangkan dokumen aktif, sambung semula kalau sambungan sudah mati."""
    global _acad
    try:
        import win32com.client
    except ImportError:
        raise RuntimeError("pywin32 belum dipasang: py -3 -m pip install pywin32")

    if _acad is not None:
        try:
            return _acad.ActiveDocument
        except Exception:
            _acad = None  # AutoCAD ditutup; cuba sambung semula di bawah

    try:
        _acad = win32com.client.GetActiveObject("AutoCAD.Application")
    except Exception as exc:
        raise RuntimeError(
            "Tidak jumpa AutoCAD yang sedang berjalan. Buka AutoCAD dengan satu "
            "gambar, kemudian cuba lagi. (Ralat COM: %s)" % exc
        )
    try:
        return _acad.ActiveDocument
    except Exception as exc:
        raise RuntimeError("AutoCAD berjalan tetapi tiada gambar terbuka: %s" % exc)


def _pastikan_idle(doc):
    """SendCommand ditolak kalau AutoCAD sedang dalam command atau dialog."""
    try:
        if int(doc.GetVariable("CMDACTIVE")) != 0:
            raise RuntimeError(
                "AutoCAD sedang dalam command atau ada dialog terbuka. "
                "Tekan ESC di AutoCAD, kemudian cuba lagi."
            )
    except RuntimeError:
        raise
    except Exception:
        pass  # sysvar tidak dapat dibaca; biar SendCommand yang melaporkan


def _hantar(kod):
    """Hantar satu baris kod (command atau LISP) ke AutoCAD."""
    doc = _doc()
    _pastikan_idle(doc)
    if not kod.endswith("\n"):
        kod += "\n"
    try:
        doc.SendCommand(kod)
    except Exception as exc:
        raise RuntimeError("AutoCAD menolak arahan: %s" % exc)
    return doc


def _lstr(teks):
    """Tukar teks Python jadi literal string LISP yang selamat."""
    bersih = str(teks).replace("\r", " ").replace("\n", " ")
    return '"' + bersih.replace("\\", "\\\\").replace('"', '\\"') + '"'


def _pt(x, y):
    return '"%s,%s"' % (x, y)


# --------------------------------------------------------------------------
# Tool: baca
# --------------------------------------------------------------------------

@mcp.tool()
def acad_status() -> str:
    """Periksa sambungan ke AutoCAD dan laporkan keadaan gambar aktif.

    Guna tool ini dahulu sebelum tool lain, untuk pastikan AutoCAD terbuka.
    """
    doc = _doc()
    baris = []
    for label, ambil in [
        ("versi", lambda: _acad.Version),
        ("gambar", lambda: doc.Name),
        ("laluan", lambda: doc.FullName or "(belum disimpan)"),
        ("entity", lambda: doc.ModelSpace.Count),
        ("layer", lambda: doc.Layers.Count),
        ("layer_aktif", lambda: doc.ActiveLayer.Name),
        ("insunits", lambda: doc.GetVariable("INSUNITS")),
        ("cmdactive", lambda: doc.GetVariable("CMDACTIVE")),
    ]:
        try:
            baris.append("%s=%s" % (label, ambil()))
        except Exception as exc:
            baris.append("%s=[ralat: %s]" % (label, exc))
    return "Bersambung ke AutoCAD. " + ", ".join(baris)


@mcp.tool()
def acad_list_layers() -> str:
    """Senaraikan semua layer dalam gambar aktif, dengan warna dan keadaannya."""
    doc = _doc()
    keluar = []
    for i in range(doc.Layers.Count):
        lay = doc.Layers.Item(i)
        try:
            keluar.append(
                "%s (warna=%s, on=%s, beku=%s, lock=%s)"
                % (lay.Name, lay.Color, lay.LayerOn, lay.Freeze, lay.Lock)
            )
        except Exception:
            keluar.append(str(lay.Name))
    return "%d layer:\n" % len(keluar) + "\n".join(keluar)


@mcp.tool()
def acad_list_entities(limit: int = 50, layer: str = "") -> str:
    """Senaraikan entity dalam model space (jenis, layer, dan titik rujukan).

    Args:
        limit: bilangan maksimum entity untuk dilaporkan.
        layer: kalau diberi, hanya entity pada layer ini dilaporkan.
    """
    doc = _doc()
    ms = doc.ModelSpace
    jumlah = ms.Count
    keluar = []
    for i in range(jumlah):
        if len(keluar) >= limit:
            break
        try:
            ent = ms.Item(i)
            nama_layer = ent.Layer
            if layer and nama_layer != layer:
                continue
            rujukan = ""
            for sifat in ("Center", "InsertionPoint", "StartPoint", "Coordinates"):
                try:
                    nilai = getattr(ent, sifat)
                    rujukan = " %s=%s" % (sifat, tuple(round(float(v), 4) for v in nilai))
                    break
                except Exception:
                    continue
            keluar.append("[%d] %s layer=%s%s" % (i, ent.EntityName, nama_layer, rujukan))
        except Exception as exc:
            keluar.append("[%d] [tidak dapat dibaca: %s]" % (i, exc))
    kepala = "%d entity dalam model space" % jumlah
    if layer:
        kepala += " (ditapis layer=%s)" % layer
    return kepala + ", %d dilaporkan:\n" % len(keluar) + "\n".join(keluar)


# --------------------------------------------------------------------------
# Tool: jalankan arahan mentah
# --------------------------------------------------------------------------

@mcp.tool()
def acad_command(command: str) -> str:
    """Jalankan satu command AutoCAD pada gambar yang sedang terbuka.

    Pisahkan setiap input dengan \\n, sama seperti menaip di command line.
    Awalan "_." disyorkan supaya tidak bergantung bahasa antaramuka.
    Contoh: "_.LINE\\n0,0\\n100,100\\n\\n"

    Tool ini tidak memulangkan output command. Guna acad_status atau
    acad_list_entities selepasnya untuk periksa hasilnya.
    """
    doc = _hantar(command)
    return "Dihantar. Entity dalam model space sekarang: %d" % doc.ModelSpace.Count


@mcp.tool()
def acad_lisp(code: str, capture_result: bool = False) -> str:
    """Jalankan kod AutoLISP pada gambar yang sedang terbuka.

    Args:
        code: ungkapan LISP, contoh '(command "_.circle" "0,0" 50)'.
        capture_result: kalau True, nilai ungkapan disalin ke sysvar USERS1
            dan dibaca balik. Hasil ditukar jadi string, maksimum 255 aksara.
            Gunakan ini apabila anda perlu melihat nilai pulangan LISP.
    """
    if capture_result:
        doc = _doc()
        asal = doc.GetVariable("USERS1")
        bungkus = '(setvar "USERS1" (vl-princ-to-string (progn %s)))' % code
        _hantar(bungkus)
        hasil = _doc().GetVariable("USERS1")
        try:
            _hantar('(setvar "USERS1" %s)' % _lstr(asal))
        except Exception:
            pass
        return "Hasil LISP: %r" % hasil
    _hantar(code)
    return "LISP dihantar (tiada penangkapan hasil; set capture_result=True untuk melihat nilai)."


# --------------------------------------------------------------------------
# Tool: melukis
# --------------------------------------------------------------------------

@mcp.tool()
def acad_set_layer(name: str, color: int = 7) -> str:
    """Buat layer kalau belum ada, kemudian jadikan ia layer aktif.

    Args:
        name: nama layer.
        color: nombor warna AutoCAD (1=merah, 2=kuning, 3=hijau, 7=putih/hitam).
    """
    lisp = (
        '(progn (if (not (tblsearch "layer" %(n)s))'
        ' (command "_.-layer" "_m" %(n)s "_c" "%(c)d" "" ""))'
        ' (setvar "clayer" %(n)s) (princ))'
    ) % {"n": _lstr(name), "c": int(color)}
    _hantar(lisp)
    doc = _doc()
    return "Layer aktif sekarang: %s" % doc.ActiveLayer.Name


@mcp.tool()
def acad_draw_line(x1: float, y1: float, x2: float, y2: float) -> str:
    """Lukis satu garisan dari (x1,y1) ke (x2,y2) dalam model space."""
    sebelum = _doc().ModelSpace.Count
    _hantar('(command "_.line" %s %s "")' % (_pt(x1, y1), _pt(x2, y2)))
    return "Garisan dilukis. Entity: %d -> %d" % (sebelum, _doc().ModelSpace.Count)


@mcp.tool()
def acad_draw_circle(x: float, y: float, radius: float) -> str:
    """Lukis satu bulatan berpusat di (x,y) dengan radius yang diberi."""
    sebelum = _doc().ModelSpace.Count
    _hantar('(command "_.circle" %s "%s")' % (_pt(x, y), radius))
    return "Bulatan dilukis. Entity: %d -> %d" % (sebelum, _doc().ModelSpace.Count)


@mcp.tool()
def acad_draw_text(x: float, y: float, text: str, height: float = 2.5,
                   rotation: float = 0.0) -> str:
    """Letak teks satu baris pada (x,y).

    Args:
        x, y: titik asas teks.
        text: kandungan teks.
        height: tinggi teks dalam unit gambar.
        rotation: putaran dalam darjah.
    """
    sebelum = _doc().ModelSpace.Count
    _hantar('(command "_.text" %s "%s" "%s" %s)'
            % (_pt(x, y), height, rotation, _lstr(text)))
    return "Teks diletak. Entity: %d -> %d" % (sebelum, _doc().ModelSpace.Count)


@mcp.tool()
def acad_draw_polyline(points: list[list[float]], closed: bool = False) -> str:
    """Lukis polyline melalui senarai titik.

    Args:
        points: senarai [x, y], contoh [[0,0], [10,0], [10,10]].
        closed: kalau True, polyline ditutup kembali ke titik pertama.
    """
    if len(points) < 2:
        raise ValueError("Polyline perlu sekurang-kurangnya 2 titik.")
    bahagian = " ".join(_pt(p[0], p[1]) for p in points)
    akhir = '"_c"' if closed else '""'
    sebelum = _doc().ModelSpace.Count
    _hantar('(command "_.pline" %s %s)' % (bahagian, akhir))
    return ("Polyline %d titik%s dilukis. Entity: %d -> %d"
            % (len(points), " (tertutup)" if closed else "",
               sebelum, _doc().ModelSpace.Count))


@mcp.tool()
def acad_plot_points(points: list[dict], layer: str = "SURVEY_PTS",
                     label_height: float = 2.0) -> str:
    """Plot banyak titik survey sekali gus, dengan label pilihan.

    Direka untuk output pengiraan survey (traverse, setting out, koordinat).

    Args:
        points: senarai dict dengan kunci 'x', 'y', dan 'label' (pilihan).
            Contoh: [{"x": 100.5, "y": 200.0, "label": "ST1"}, ...]
        layer: layer untuk titik dan label.
        label_height: tinggi teks label dalam unit gambar.
    """
    if not points:
        raise ValueError("Senarai titik kosong.")
    acad_set_layer(layer, color=2)
    sebelum = _doc().ModelSpace.Count

    arahan = []
    for p in points:
        x, y = p["x"], p["y"]
        arahan.append('(command "_.point" %s)' % _pt(x, y))
        label = p.get("label")
        if label:
            arahan.append(
                '(command "_.text" %s "%s" "0" %s)'
                % (_pt(float(x) + float(label_height), float(y) + float(label_height)),
                   label_height, _lstr(label))
            )
    # Hantar berkelompok supaya tidak membanjiri command line AutoCAD.
    for i in range(0, len(arahan), 40):
        _hantar("(progn %s (princ))" % " ".join(arahan[i:i + 40]))

    _hantar('(command "_.zoom" "_e")')
    return ("%d titik diplot pada layer %s. Entity: %d -> %d"
            % (len(points), layer, sebelum, _doc().ModelSpace.Count))


# --------------------------------------------------------------------------
# Tool: paparan dan fail
# --------------------------------------------------------------------------

@mcp.tool()
def acad_zoom_extents() -> str:
    """Zoom supaya semua entity dalam gambar kelihatan."""
    _hantar('(command "_.zoom" "_e")')
    return "Zoom extents selesai."


@mcp.tool()
def acad_save() -> str:
    """Simpan gambar aktif. Gagal kalau gambar belum pernah disimpan."""
    doc = _doc()
    if not doc.FullName:
        raise RuntimeError(
            "Gambar ini belum pernah disimpan, jadi tiada nama fail. "
            "Simpan sekali secara manual di AutoCAD dahulu."
        )
    doc.Save()
    return "Disimpan: %s" % doc.FullName


if __name__ == "__main__":
    if sys.platform != "win32":
        sys.exit("Server ini Windows sahaja (COM tidak ada di %s)." % sys.platform)
    mcp.run()
