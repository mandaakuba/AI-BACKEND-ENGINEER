class Pegawai:
    # 1. __init__ (Constructor) & Encapsulation
    def __init__(self, nama, jabatan, gaji):
        self.nama = nama
        self.jabatan = jabatan
        # Pake underscore di depan tandanya "private" (Encapsulation)
        # Nggak boleh diakses langsung dari luar class
        self._gaji = gaji 

    # 2. __str__ (Biar kalau di-print langsung rapi)
    def __str__(self):
        return f"Pegawai: {self.nama} - {self.jabatan}"

    # Getter untuk ngambil nilai gaji yang di-private
    def cek_gaji(self):
        return f"Gaji {self.nama}: Rp {self._gaji}"

    # 3. @staticmethod (Method yang mandiri, nggak butuh parameter 'self')
    @staticmethod
    def cek_jam_kerja(jam):
        if jam > 8:
            return "Lembur"
        return "Normal"

    # 4. @classmethod (Bikin objek baru dari string, pengganti __init__)
    @classmethod
    def dari_string(cls, data_string):
        # Misal stringnya: "Budi-Staff-5000000"
        nama, jabatan, gaji = data_string.split('-')
        # cls() itu sama kayak manggil Pegawai()
        return cls(nama, jabatan, int(gaji))


# 5. Inheritance (Pewarisan) & super()
class Manager(Pegawai):
    def __init__(self, nama, jabatan, gaji, tunjangan):
        # super() manggil __init__ milik Pegawai, jadi nggak perlu nulis ulang
        super().__init__(nama, jabatan, gaji)
        self.tunjangan = tunjangan
        
    def total_pendapatan(self):
        # Manager bisa akses _gaji karena dia anaknya Pegawai
        return self._gaji + self.tunjangan


# ==========================================
# TEST LOGIC TUGAS 1
# ==========================================
if __name__ == "__main__":
    # Test Class Method (Bikin pegawai dari string)
    pegawai1 = Pegawai.dari_string("Andi-IT Support-6000000")
    print(pegawai1) # Manggil __str__
    
    # Test Static Method
    print(f"Jam kerja 10 jam = {Pegawai.cek_jam_kerja(10)}")
    
    # Test Inheritance & Encapsulation
    bos = Manager("Sarah", "Direktur", 15000000, 5000000)
    print(f"Total Pendapatan Bos: Rp {bos.total_pendapatan()}")



