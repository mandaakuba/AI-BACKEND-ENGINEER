import asyncio
import os
from dotenv import load_dotenv
import dotenv
from pydantic import BaseModel, Field, ValidationError

load_dotenv()
API_KEY = os.getenv("SECRET_API_KEY")
if not API_KEY:
    print("API HILANG")
else:
    print(f"sistem mendeteksi API Key:{API_KEY[:5]}***\n")

#PYDANTIC_BASE_MODEL
class DataSensor(BaseModel):
    nama_sensor: str
    suhu: float = Field(..., ge=-50.0, le=100.0)
    status: str

async def ambil_data_sensor(nama, waktu_tunggu, suhu_dummy):
    print(f"[{nama}] Mulai Ditarik (Tunggu {waktu_tunggu} detik)")
    await asyncio.sleep(waktu_tunggu) 
    print(f"[{nama}] Selesai ditarik!")

    return {
        "nama_sensor": nama,
        "suhu": suhu_dummy,
        "status": "Aktif"

    }

async def main():
    hasil_mentah = await asyncio.gather(
        ambil_data_sensor("Sensor A", 2, 35.5),
        ambil_data_sensor("Sensor B", 3, 105.0), # Sengaja disetting 105 biar validasi Pydantic error
        ambil_data_sensor("Sensor C", 1, -10.0)
    )

    print("proses validasi")
    for data in hasil_mentah:
        try:
            data_valid = DataSensor(**data)
            print(f"DATA VALID: {data_valid.nama_sensor} | Suhu: {data_valid.suhu}°C")
        except ValidationError as e:
            print(f"error pada {data['nama_sensor']}: Suhu {data['suhu']} melanggar aturan")

if __name__ == "__main__":
    asyncio.run(main())