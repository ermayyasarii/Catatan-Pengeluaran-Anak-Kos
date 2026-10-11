from datetime import datetime

KATEGORI = ("makan", "transport", "kuliah", "hiburan", "kos", "lainnya")

class PengeluaranError(Exception):   #Exception buatan sendiri untuk data yang salah 
    pass

def validasi_tanggal(teks):
    #format tanggal harus YYYY-MM-DD
    teks = teks.strip()
    try:
        datetime.strptime(teks, "%Y-%m-%d")
    except ValueError:
        raise PengeluaranError("Format tanggal harus YYYY-MM-DD")
    return teks

def validasi_kategori(teks):
    # kategori harus ada di daftar KATEGORI
    teks = teks.strip().lower()
    if teks not in KATEGORI:
        raise PengeluaranError("Kategori tidak valid")
    return teks

def validasi_keterangan(teks):
    # keterangan tidak boleh kosong
    teks = teks.replace(",", " ").strip()
    if not teks:
        raise PengeluaranError("Keterangan tidak boleh kosong")
    return teks

def validasi_jumlah(teks):
    # jumlah harus bilangan bulat lebih dari 0
    try:
        jumlah = int(teks)
    except ValueError:
        raise PengeluaranError(f"Jumlah '{teks}' harus berupa angka bulat")
    if jumlah <= 0:
        raise PengeluaranError("Jumlah harus lebih dari 0")
    return jumlah

def validasi_baris(baris):
    # cek satu baris file (4 kolom), hasilnya tuple
    bagian = baris.strip().split(",")
    if len(bagian) != 4:
        raise PengeluaranError("Data harus terdiri dari 4 kolom.")
    tanggal, kategori, keterangan, jumlah = bagian
    return (
        validasi_tanggal(tanggal),
        validasi_kategori(kategori),
        validasi_keterangan(keterangan),
        validasi_jumlah(jumlah)
    )