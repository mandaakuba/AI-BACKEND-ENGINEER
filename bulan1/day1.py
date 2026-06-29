from re import S


class Pegawai:
    nama_perusahaan = "PT. Nurrohman Digital Solutions"
    def __init__(self, nama, gaji_pokok):
        self.nama = nama
        self._gaji_pokok = gaji_pokok

    def __str__(self):
        return f"Pegawai dengan Nama: {self.nama}, Memiliki Gaji Pokok: {self._gaji_pokok}"

    @classmethod
    def ubah_nama_perusahaan(cls, nama_baru):
        cls.nama_perusahaan = nama_baru
    @staticmethod
    def cek_hari_kerja(hari):
        """Fungsi helper yang tidak butuh self/cls"""
        if hari.lower() in ['sabtu', 'minggu']:
            return "Hari Libur"
        return "Hari Kerja"

class Manager(Pegawai):
    def __init__(self, nama, gaji_pokok, departemen, tunjangan ):
        super().__init__(nama, gaji_pokok)
        self.departemen = departemen
        self.__tunjangan = tunjangan
    def __str__(self):
        return f"Manajer {self.nama} dengan Gaji Pokok: {self._gaji_pokok}, Departemen: {self.departemen}"
    def hitung_gaji(self):
        return self._gaji_pokok + self.__tunjangan


p1 = Pegawai("Andi", 5000000)
print(p1)  # Output: Pegawai: Andi bekerja di PT Python Sejahtera

Pegawai.ubah_nama_perusahaan ("PT Mencari Cinta Sejati")
print(f"Hari Senin adalah {Pegawai.cek_hari_kerja('senin')}")

m1 = Manager("Budi", 8000000, "IT", 2000000)
print(m1) # Output: Manajer IT: Budi (PT Python Nusantara)
print(f"Total Gaji Budi: Rp {m1.hitung_gaji()}")




from abc import ABC, abstractmethod

#abstraction
class SistemPembayaran(ABC):
    def __init__(self, nama_user, total_tagihan):
        self.nama_user = nama_user
        self.total_tagihan = total_tagihan

    @abstractmethod
    def proses_bayar(self):
        pass

#polymorphoism
class TransferBank(SistemPembayaran):
    def proses_bayar(self):
        return f"Memproses Transfer Bank dari {self.nama_user} sebesar {self.total_tagihan}"

class Ewallet(SistemPembayaran):
    def proses_bayar(self):
        potongan_admin = 20000
        total = self.total_tagihan + potongan_admin
        return f"Memproses Transfer via E-Wallet {self.nama_user} sebesar {total} (Tambahan Biaya Admin E-Wallet)"

class KartuKredit(SistemPembayaran):
    def proses_bayar(self):
        bunga = self.total_tagihan * 0.02
        total = self.total_tagihan + bunga
        return f"Memproses Transfer via Kartu Kredit {self.nama_user} sebesar {total} (Bunga Kartu Kredit 2%)" 

bayar1 = TransferBank("kanjut", 10000)
bayar2 = Ewallet("Puki", 120000)
bayar3 = KartuKredit("Kimak", 90000)

daftar_transaksi = [bayar1, bayar2, bayar3]

for transaksi in daftar_transaksi:
    print (transaksi.proses_bayar())

    

# ==========================================
# 1. CUSTOM EXCEPTION (Membuat Error Sendiri)
# ==========================================
# Mewarisi class Exception bawaan Python
class PromptKasarError(Exception):
    def __init__(self, kata_terlarang):
        super().__init__(f"Sistem menolak! Terdapat kata terlarang: '{kata_terlarang}'")

class SaldoHabisError(Exception):
    def __init__(self):
        super().__init__("Koin tidak cukup untuk generate gambar AI.")


# ==========================================
# 2. CLASS SISTEM AI
# ==========================================
class AIGenerator:
    def __init__(self, koin):
        self.koin = koin
        self.kata_terlarang = ["jelek", "bodoh", "kasar"]

    def generate_gambar(self, prompt):
        print(f"\nMemproses prompt: '{prompt}'...")
        
        # Mengecek apakah koin cukup
        if self.koin <= 0:
            raise SaldoHabisError() # raise digunakan untuk MEMICU/MELEMPAR error
            
        # Mengecek kata terlarang
        for kata in self.kata_terlarang:
            if kata in prompt.lower():
                raise PromptKasarError(kata)
                
        # Jika lolos semua pengecekan
        self.koin -= 1
        return f"✅ Berhasil! Gambar '{prompt}' selesai dibuat. (Sisa koin: {self.koin})"

# ==========================================
# 3. UJI COBA DENGAN TRY-EXCEPT
# ==========================================
mesin_ai = AIGenerator(koin=1)

daftar_prompt_user = [
    "Kucing lucu main bola",
    "Orang bodoh jatuh", 
    "Pemandangan gunung",
    "Robot canggih" # Ini akan gagal karena koin keburu habis
]

for prompt in daftar_prompt_user:
    # TRY: Area berisiko
    try:
        hasil = mesin_ai.generate_gambar(prompt)
        
    # EXCEPT: Menangkap error spesifik
    except PromptKasarError as e:
        print(f"❌ ERROR KEAMANAN: {e}")
        
    except SaldoHabisError as e:
        print(f"❌ ERROR PEMBAYARAN: {e}")
        
    # ELSE: Dijalankan jika try sukses
    else:
        print(hasil)
        
    # FINALLY: Dijalankan apapun yang terjadi
    finally:
        print("-" * 40) # Cetak garis pembatas

import requests
url_tujuan = "https://dummyjson.com/quotes/random"
print(f"Mengirim kurir ke: {url_tujuan}...\n")

try:
    response = requests.get(url_tujuan, timeout= 5)
    if response.status_code == 200:
        data_mentah = response.json()
        teks_quote = data_mentah.get('quote')
        nama_penulis = data_mentah.get('author')
        print("✅ YAY! DAPAT BALASAN DARI SERVER:")
        print(f"\"{teks_quote}\"")
        print(f"- {nama_penulis}")
    else:
        print(f"❌ Server menolak pesanan. Kode status: {response.status_code}")

except requests.exceptions.ConnectionError:
    print("❌ Waduh, gagal koneksi! Cek kabel internetmu, bos.")
except requests.exceptions.Timeout:
    print("❌ Servernya kelamaan balas. Kita tinggalin aja (Timeout).")


import requests
url_tujuan = "https://dummyjson.com/posts/add"
paket_data = {
    "title": "Hari ini saya belajar AI Backend Engineer!",
    "userId": 5
}

print("📦 Mengirim paket (POST Request) ke server...\n")
try:
    response = requests.post(url_tujuan, json=paket_data, timeout=5)
    if response.status_code in [200, 201]:
        data_balasan = response.json()
        print("berhasil")
        print(f"ID Postingan Baru {data_balasan.get('id')}")
        print(f"Judul yang Tersimpan {data_balasan.get('title')}")

    else: 
        print(f"gagal nih, kode status: {response.status_code}")

except requests.exceptions.ConnectionError:
    print ("cek koneksi internet anda")

except requests.exceptions.Timeout:
    print ('Request time out')
