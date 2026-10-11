from .validasi import KATEGORI, PengeluaranError, validasi_baris

BATAS_MAHAL = 50000

def hitung_total(*angka): #*args menjumlahkan angka sebanyak apapun
    return sum(angka)

def rupiah(angka):
    return f"Rp{angka:,}" #mengbah jadi format Rp

def buat_pengeluaran(tanggal, jumlah, **kwargs):
    # **kwargs: kategori dan keterangan boleh tidak diisi
    kategori = kwargs.get("kategori", "lainnya")
    keterangan = kwargs.get("keterangan", "tanpa keterangan")
    return Pengeluaran(tanggal, kategori, keterangan, jumlah)

def baris_ke_pengeluaran(baris):
    # ubah satu baris file jadi objek Pengeluaran
    tanggal, kategori, keterangan, jumlah = validasi_baris(baris)
    return Pengeluaran(tanggal, kategori, keterangan, jumlah)

class Pengeluaran: #satu transaksi pengeluaran
    def __init__(self, tanggal, kategori, keterangan, jumlah):
        self.tanggal = tanggal
        self.kategori = kategori
        self.keterangan = keterangan
        self.jumlah = jumlah

    def apakah_mahal(self):
        return self.jumlah > BATAS_MAHAL

    def format_jumlah(self):
        return rupiah(self.jumlah)

    def ke_baris(self):
        # ubah jadi satu baris untuk disimpan ke file
        return f"{self.tanggal},{self.kategori},{self.keterangan},{self.jumlah}"

    def __str__(self):
        # tampilan satu transaksi di layar
        return f"{self.tanggal} | {self.kategori} | {self.keterangan} | {self.format_jumlah()}"


class Dompet: #kumpulan pengeluaran dan perhitungannya
    def __init__(self):
        self.daftar = []

    def tambah(self, pengeluaran):
        self.daftar.append(pengeluaran)

    def total(self): #hitung total semua pengeluaran 
        return hitung_total(*[p.jumlah for p in self.daftar])
    
    def total_per_kategori(self):
        hasil = {}
        for p in self.daftar:
            hasil[p.kategori] = hasil.get(p.kategori, 0) + p.jumlah
        return hasil

    def filter_kategori(self, kategori):
        # ambil transaksi dari satu kategori saja
        assert kategori in KATEGORI, f"Kategori {kategori} tidak dikenal"
        return list(filter(lambda p: p.kategori == kategori, self.daftar))

    def urutkan(self, terbalik=False):
        # urutkan berdasarkan jumlah (lambda sebagai key)
        return sorted(self.daftar, key=lambda p: p.jumlah, reverse=terbalik)

    def termahal(self):
        # transaksi dengan jumlah terbesar
        if not self.daftar:
            raise PengeluaranError("Belum ada data")
        return max(self.daftar, key=lambda p: p.jumlah)

    def jumlah_hari(self):
        # banyaknya hari yang ada catatannya
        return len(set(map(lambda p: p.tanggal, self.daftar)))

    def rata_rata_harian(self):
        # rata-rata pengeluaran per hari
        if self.jumlah_hari() == 0:
            return 0
        return self.total() // self.jumlah_hari()

    def sisa_uang(self, uang_saku):
        # sisa uang saku setelah dikurangi pengeluaran
        return uang_saku - self.total()

    def buat_laporan(self, uang_saku):
        # susun teks laporan
        if not self.daftar:
            return "Belum ada data pengeluaran."
        mahal = self.termahal()
        sisa = self.sisa_uang(uang_saku)
        baris = [
            "===== LAPORAN PENGELUARAN ANAK KOS =====",
            f"Jumlah transaksi     : {len(self.daftar)}",
            f"Total pengeluaran    : {rupiah(self.total())}",
            f"Rata-rata per hari   : {rupiah(self.rata_rata_harian())}",
            f"Pengeluaran termahal : {mahal.keterangan} ({mahal.format_jumlah()}) tgl {mahal.tanggal}"
        ]
        for kategori, jumlah in sorted(self.total_per_kategori().items()):
            persen = jumlah * 100 // self.total()
            baris.append(f"  - {kategori}: {rupiah(jumlah)} ({persen}%)")
        baris.append(f"Uang saku: {rupiah(uang_saku)}")
        if sisa >= 0:
            baris.append(f"Sisa uang: {rupiah(sisa)}")
        else:
            baris.append(f"Uang saku KURANG: {rupiah(-sisa)}")
        return "\n".join(baris)

if __name__ == "__main__":     # uji lokal tanpa file
    contoh = Dompet()
    contoh.tambah(buat_pengeluaran("2026-10-01", 15000, kategori="makan", keterangan="nasi ayam"))
    contoh.tambah(buat_pengeluaran("2026-10-01", 20000, kategori="transport", keterangan="ojol"))
    contoh.tambah(buat_pengeluaran("2026-10-02", 75000, kategori="kuliah", keterangan="fotokopi modul"))
    print(contoh.buat_laporan(uang_saku=500000))