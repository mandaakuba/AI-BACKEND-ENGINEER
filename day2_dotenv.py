import asyncio
import aiohttp
import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field

# ==========================================
# 1. BUKA BRANKAS (DOTENV)
# ==========================================
# Memuat semua isi file .env ke dalam sistem
load_dotenv()

# Mengambil URL rahasia dari brankas
API_URL = os.getenv("URL_TARGET")

# ==========================================
# 2. BIKIN BLUEPRINT SATPAM (PYDANTIC)
# ==========================================
# Satpam Lapis 1: Memeriksa data Alamat
class Alamat(BaseModel):
    city: str
    state: str
    country: str

# Satpam Lapis 2: Memeriksa data Karyawan
class Karyawan(BaseModel):
    id_karyawan: int = Field(alias="id") # Mengubah nama kunci 'id' dari API jadi 'id_karyawan'
    nama_depan: str = Field(alias="firstName")
    email: str
    umur: int = Field(alias="age")
    alamat: Alamat = Field(alias="address")# MENGGUNAKAN SATPAM LAPIS 1 DI DALAM SINI (Nested Model)

# Satpam Lapis 3: Memeriksa struktur utama paket API
class ResponAPI(BaseModel):
    users: list[Karyawan] # Memastikan isinya adalah daftar (list) Karyawan

# ==========================================
# 3. MESIN TURBO BERAKSI
# ==========================================
async def narik_data_perusahaan():
    print(f"🔐 Mengambil data rahasia dari: {API_URL}")
    print("🚀 Kurir Turbo berangkat...\n")
    
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL) as response:
            data_mentah_json = await response.json()
            
            # --- DI SINI MAGIC-NYA TERJADI! ---
            # Melempar JSON berantakan ke Satpam Pydantic
            try:
                data_bersih = ResponAPI(**data_mentah_json)
                
                print("✅ VALIDASI PYDANTIC SUKSES! Data langsung dirapikan:\n")
                print("-" * 50)
                # Sekarang data_bersih bukan sekadar dictionary/JSON biasa,
                # melainkan Objek Python utuh yang bisa dipanggil pakai titik (.)
                for karyawan in data_bersih.users:
                    print(f"🆔 ID    : {karyawan.id_karyawan}")
                    print(f"👤 Nama  : {karyawan.nama_depan}")
                    print(f"📧 Email : {karyawan.email}")
                    print(f"🏢 Kota  : {karyawan.alamat.city}, {karyawan.alamat.state}")
                    print("-" * 50)
                    
            except Exception as e:
                print(f"🚨 ALARM! DATA DARI SERVER TIDAK SESUAI ATURAN: {e}")

# Tombol Start
if __name__ == "__main__":
    asyncio.run(narik_data_perusahaan())