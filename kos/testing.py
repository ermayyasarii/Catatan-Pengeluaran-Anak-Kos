# Jalankan: python -m kos.testing
import os
import unittest

from .fileio import baca_data, buat_file, tambah_data
from .processing import Dompet, buat_pengeluaran, hitung_total
from .validasi import PengeluaranError, validasi_jumlah

FILE_UJI = "data_uji.txt"


class TestKos(unittest.TestCase):

    def setUp(self):
        # hapus file uji lama supaya tiap tes mulai dari nol
        if os.path.exists(FILE_UJI):
            os.remove(FILE_UJI)

    def tearDown(self):
        # hapus file uji setelah tes selesai
        if os.path.exists(FILE_UJI):
            os.remove(FILE_UJI)

    def test_total_args(self):
        # hitung_total bisa menerima angka berapa pun
        self.assertEqual(hitung_total(1000, 2000, 3000), 6000)

    def test_jumlah_salah(self):
        # jumlah negatif atau bukan angka harus error
        with self.assertRaises(PengeluaranError):
            validasi_jumlah("-500")
        with self.assertRaises(PengeluaranError):
            validasi_jumlah("abc")

    def test_kwargs(self):
        # kategori terisi default kalau tidak diberikan
        p = buat_pengeluaran("2026-10-01", 5000)
        self.assertEqual(p.kategori, "lainnya")
        p2 = buat_pengeluaran("2026-10-01", 5000, kategori="makan")
        self.assertEqual(p2.kategori, "makan")

    def test_total_per_kategori(self):
        # total dikelompokkan per kategori
        dompet = Dompet()
        dompet.tambah(buat_pengeluaran("2026-10-01", 10000, kategori="makan"))
        dompet.tambah(buat_pengeluaran("2026-10-02", 5000, kategori="makan"))
        dompet.tambah(buat_pengeluaran("2026-10-02", 20000, kategori="kuliah"))
        self.assertEqual(dompet.total_per_kategori(), {"makan": 15000, "kuliah": 20000})
        self.assertEqual(dompet.total(), 35000)

    def test_buat_file_dua_kali(self):
        # mode x: buat file kedua kali tidak boleh menimpa data
        buat_file(FILE_UJI)
        tambah_data(FILE_UJI, buat_pengeluaran("2026-10-01", 5000))
        buat_file(FILE_UJI)
        daftar, rusak = baca_data(FILE_UJI)
        self.assertEqual(len(daftar), 1)

    def test_tambah_dan_baca(self):
        # data yang ditambah bisa dibaca lagi
        tambah_data(FILE_UJI, buat_pengeluaran("2026-10-01", 12000, kategori="makan", keterangan="soto"))
        daftar, rusak = baca_data(FILE_UJI)
        self.assertEqual(daftar[0].jumlah, 12000)
        self.assertEqual(rusak, [])

    def test_baris_rusak_dilewati(self):
        # baris salah dilewati, baris benar tetap terbaca
        with open(FILE_UJI, "w") as f:
            f.write("2026-10-01,makan,soto,12000\n")
            f.write("2026-10-02,makan,bakso,abc\n")
        daftar, rusak = baca_data(FILE_UJI)
        self.assertEqual(len(daftar), 1)
        self.assertEqual(len(rusak), 1)

    def test_file_tidak_ada(self):
        # file belum ada: program tidak crash, hasilnya kosong
        daftar, rusak = baca_data("file_tidak_ada.txt")
        self.assertEqual(daftar, [])


if __name__ == "__main__":
    unittest.main()
