import os
import unittest
from datetime import date

from kos.fileio import baca_data, buat_file, tambah_data, tulis_laporan
from kos.processing import Dompet, buat_pengeluaran
from kos.validasi import (KATEGORI, PengeluaranError, validasi_jumlah, validasi_kategori, validasi_keterangan, validasi_tanggal)

FILE_DATA = "data/pengeluaran.txt"
FILE_LAPORAN = "data/laporan_pengeluaran.txt"


def ambil_dompet():
    # baca file, tampilkan baris rusak, lalu masukkan semua transaksi ke Dompet
    daftar, rusak = baca_data(FILE_DATA)
    for nomor, alasan in rusak:
        print(f"Baris {nomor} dilewati: {alasan}")
    dompet = Dompet()
    for p in daftar:
        dompet.tambah(p)
    return dompet


def menu_tambah():
    # minta input sampai semuanya valid, lalu simpan ke file
    while True:
        try:
            tanggal = validasi_tanggal(input("Tanggal (YYYY-MM-DD, kosong = hari ini): ") or date.today().isoformat())
            kategori = validasi_kategori(input(f"Kategori ({', '.join(KATEGORI)}): "))
            keterangan = validasi_keterangan(input("Keterangan: "))
            jumlah = validasi_jumlah(input("Jumlah (Rp): "))
            break
        except PengeluaranError as e:
            print("Input salah:", e)
    p = buat_pengeluaran(tanggal, jumlah, kategori=kategori, keterangan=keterangan)
    tambah_data(FILE_DATA, p)
    print("Tersimpan!", "(termasuk pengeluaran mahal)" if p.apakah_mahal() else "")


def menu_lihat():
    # tampilkan semua data, dari jumlah terbesar
    dompet = ambil_dompet()
    for p in dompet.urutkan(terbalik=True):
        print(p)


def menu_laporan():
    # hitung analisis, tampilkan, dan simpan ke file
    dompet = ambil_dompet()
    while True:
        try:
            uang_saku = validasi_jumlah(input("Uang saku bulan ini (Rp): "))
            break
        except PengeluaranError as e:
            print("Input salah:", e)
    laporan = dompet.buat_laporan(uang_saku)
    print(laporan)
    tulis_laporan(FILE_LAPORAN, laporan)
    print(f"Laporan disimpan ke {FILE_LAPORAN}")


def menu_uji():
    # jalankan unit test dari dalam program
    suite = unittest.defaultTestLoader.loadTestsFromName("kos.testing")
    unittest.TextTestRunner(verbosity=1).run(suite)


def main():
    # menu utama
    os.makedirs("data", exist_ok=True)  # pastikan folder data ada
    menu = {"1": lambda: buat_file(FILE_DATA), "2": menu_tambah, "3": menu_lihat,
            "4": menu_laporan, "5": menu_uji}
    while True:
        print("\n=== CATATAN PENGELUARAN ANAK KOS ===")
        print("1. Buat file data\n2. Tambah pengeluaran\n3. Lihat data")
        print("4. Laporan\n5. Jalankan unit test\n0. Keluar")
        pilihan = input("Pilih: ").strip()
        if pilihan == "0":
            print("Sampai jumpa!")
            break
        if pilihan in menu:
            menu[pilihan]()
        else:
            print("Menu tidak ada.")


if __name__ == "__main__":
    main()
