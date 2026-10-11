from .processing import baris_ke_pengeluaran
from .validasi import PengeluaranError

HEADER = "tanggal,kategori,keterangan,jumlah"


def buat_file(path):
    # buat file data pertama kali (mode x), kalau sudah ada tidak ditimpa
    try:
        with open(path, "x") as f:
            f.write(HEADER + "\n")
            print("File berhasil dibuat.")
    except FileExistsError:
            print(f"File sudah ada, tidak dibuat ulang.")

def tambah_data(path, pengeluaran):
    # tambah satu baris di akhir file (mode a)
    with open(path, "a") as f:
        f.write(pengeluaran.ke_baris() + "\n")

def baca_data(path):
    # baca file baris demi baris (mode r), baris rusak dilewati
    daftar = []
    rusak = []
    try:
        with open(path, "r") as f:
            for nomor, baris in enumerate(f, start=1):
                baris = baris.strip()
                if baris == "" or baris == HEADER:
                    continue
                try:
                    daftar.append(baris_ke_pengeluaran(baris))
                except PengeluaranError as e:
                    rusak.append((nomor, str(e)))
    except FileNotFoundError:
        print(f"File data belum ada. Buat dulu lewat menu 1.")
    return daftar, rusak

def tulis_laporan(path, teks):
    # tulis laporan ke file (mode w), isi lama diganti
    with open(path, "w") as f:
        f.write(teks + "\n")
