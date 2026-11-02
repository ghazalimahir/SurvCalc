"""Uji sambungan Python <-> AutoCAD melalui COM.

Jalankan di PC Windows, dengan AutoCAD TERBUKA dan satu gambar aktif:

    py -3 -m pip install pywin32
    py -3 probe_acad.py            # baca sahaja, tidak ubah gambar
    py -3 probe_acad.py --draw     # baca + lukis bentuk ujian

Kalau skrip ini berjaya, MCP server (acad_mcp.py) pasti boleh jalan.
"""

import argparse
import sys

# Command AutoCAD ditulis dengan awalan "_." supaya tidak bergantung bahasa
# antaramuka ("_" = nama antarabangsa, "." = abai redefinition).
TEST_LAYER = "CLAUDE_UJIAN"


def gagal(mesej):
    print("\n[GAGAL] " + mesej)
    sys.exit(1)


def connect():
    """Sambung ke AutoCAD yang SEDANG berjalan (tidak buka instance baru)."""
    try:
        import win32com.client
    except ImportError:
        gagal(
            "pywin32 belum dipasang.\n"
            "        Jalankan: py -3 -m pip install pywin32"
        )

    try:
        acad = win32com.client.GetActiveObject("AutoCAD.Application")
    except Exception as exc:
        gagal(
            "tidak jumpa AutoCAD yang sedang berjalan.\n"
            "        Periksa: (1) AutoCAD sudah dibuka?  (2) AutoCAD penuh, bukan LT?\n"
            "        (3) Python dan AutoCAD sama-sama 64-bit?\n"
            "        Ralat asal: %s" % exc
        )

    try:
        doc = acad.ActiveDocument
    except Exception as exc:
        gagal("AutoCAD berjalan tetapi tiada gambar terbuka. Ralat: %s" % exc)

    return acad, doc


def tunggu_idle(doc):
    """SendCommand gagal kalau AutoCAD sedang dalam command lain."""
    try:
        if int(doc.GetVariable("CMDACTIVE")) != 0:
            gagal(
                "AutoCAD sedang dalam command atau ada dialog terbuka.\n"
                "        Tekan ESC beberapa kali di AutoCAD, kemudian ulang."
            )
    except Exception:
        pass  # sysvar tidak dapat dibaca; teruskan sahaja


def baca(acad, doc):
    print("=" * 58)
    print("  UJIAN 1 - BACA MAKLUMAT")
    print("=" * 58)

    import struct
    bit = struct.calcsize("P") * 8
    print("  %-32s : %d-bit" % ("Python", bit))
    if bit != 64:
        print("    ^ PERHATIAN: AutoCAD 2022 ialah 64-bit. Python 32-bit")
        print("      tidak boleh bercakap dengannya. Pasang Python 64-bit.")

    maklumat = [
        ("Versi AutoCAD", lambda: acad.Version),
        ("Nama gambar", lambda: doc.Name),
        ("Laluan penuh", lambda: doc.FullName or "(belum disimpan)"),
        ("Bilangan entity (model space)", lambda: doc.ModelSpace.Count),
        ("Bilangan layer", lambda: doc.Layers.Count),
        ("Layer aktif", lambda: doc.ActiveLayer.Name),
        ("Unit (INSUNITS)", lambda: doc.GetVariable("INSUNITS")),
    ]
    for label, ambil in maklumat:
        try:
            print("  %-32s : %s" % (label, ambil()))
        except Exception as exc:
            print("  %-32s : [tidak dapat dibaca] %s" % (label, exc))


def ujian_lisp(doc):
    """Hantar LISP, dan ambil balik hasilnya melalui sysvar USERS1.

    Ini saluran dua hala: COM tidak boleh baca pembolehubah LISP terus,
    tetapi LISP boleh (setvar "USERS1" ...) dan COM boleh GetVariable.
    """
    print()
    print("=" * 58)
    print("  UJIAN 2 - HANTAR LISP DAN AMBIL BALIK HASIL")
    print("=" * 58)

    tunggu_idle(doc)
    asal = doc.GetVariable("USERS1")
    cap = "CLAUDE-OK"
    try:
        doc.SendCommand('(setvar "USERS1" "%s")\n' % cap)
    except Exception as exc:
        gagal("SendCommand ditolak. Ralat: %s" % exc)

    balik = doc.GetVariable("USERS1")
    print("  Dihantar  : (setvar \"USERS1\" \"%s\")" % cap)
    print("  Diterima  : %r" % balik)
    if balik == cap:
        print("  -> Saluran dua hala BERFUNGSI.")
    else:
        print("  -> Nilai tidak sepadan; LISP mungkin tidak dijalankan.")

    try:
        doc.SendCommand('(setvar "USERS1" "%s")\n' % asal)  # pulihkan
    except Exception:
        pass


def lukis(doc):
    print()
    print("=" * 58)
    print("  UJIAN 3 - LUKIS BENTUK UJIAN")
    print("=" * 58)

    sebelum = doc.ModelSpace.Count
    tunggu_idle(doc)

    lisp = (
        '(progn'
        '  (if (not (tblsearch "layer" "%(layer)s"))'
        '    (command "_.-layer" "_m" "%(layer)s" "_c" "1" "" ""))'
        '  (setvar "clayer" "%(layer)s")'
        '  (command "_.line" "0,0" "100,100" "")'
        '  (command "_.circle" "50,50" "25")'
        '  (command "_.text" "0,-20" "10" "0" "Claude - ujian COM")'
        '  (command "_.zoom" "_e")'
        '  (princ))\n'
    ) % {"layer": TEST_LAYER}

    try:
        doc.SendCommand(lisp)
    except Exception as exc:
        gagal("SendCommand ditolak semasa melukis. Ralat: %s" % exc)

    selepas = doc.ModelSpace.Count
    print("  Entity sebelum : %d" % sebelum)
    print("  Entity selepas : %d" % selepas)
    print("  Ditambah       : %d  (dijangka 3: garisan, bulatan, teks)" % (selepas - sebelum))
    print("  Layer          : %s (merah)" % TEST_LAYER)
    if selepas > sebelum:
        print("  -> Lukisan BERFUNGSI. Padam dengan: layer %s, ERASE" % TEST_LAYER)
    else:
        print("  -> Tiada entity baru. Periksa command line AutoCAD untuk ralat.")


def main():
    p = argparse.ArgumentParser(description="Uji sambungan Python <-> AutoCAD (COM)")
    p.add_argument("--draw", action="store_true",
                   help="lukis bentuk ujian pada gambar yang terbuka")
    args = p.parse_args()

    if sys.platform != "win32":
        gagal(
            "skrip ini Windows sahaja (COM tidak ada di %s).\n"
            "        Jalankan di PC/laptop Windows yang ada AutoCAD." % sys.platform
        )

    acad, doc = connect()
    print("\nBERJAYA sambung ke AutoCAD yang sedang berjalan.\n")
    baca(acad, doc)
    ujian_lisp(doc)
    if args.draw:
        lukis(doc)
    else:
        print("\n(Tambah --draw untuk uji melukis pada gambar ini.)")
    print("\nSelesai.\n")


if __name__ == "__main__":
    main()
