import os
import psycopg2
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

# ---------------------------------------------------------
# GET: Cari Sultan Berdasarkan Negara
# ---------------------------------------------------------
@app.get("/sultans/{nama_negara}")
def get_sultans_by_country(nama_negara: str):
    try:
        connection = psycopg2.connect(
            host=os.getenv("DB_HOST"), port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"), user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        cursor = connection.cursor()
        
        query = """
            SELECT first_name, country, total_belanja 
            FROM klasifikasi_sultan 
            WHERE kasta_pelanggan = 'Sultan (VIP)' AND country = %s
            ORDER BY total_belanja DESC;
        """
        
        # FIX 1: Tadi lu nulis query_insert dan ( ... ), harusnya query dan (nama_negara,)
        cursor.execute(query, (nama_negara,))
        data = cursor.fetchall()
        
        hasil_json = []
        for row in data:
            hasil_json.append({
                "nama": row[0],
                "negara": row[1],
                "total_belanja": float(row[2])
            })
        
        return {
            "status": f"Sukses narik data sultan dari {nama_negara}!", 
            "total_data": len(hasil_json),
            "data": hasil_json
        }

    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Database error: {error}")
        
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'connection' in locals(): connection.close()

# ---------------------------------------------------------
# POST: Pendaftaran Pelanggan Baru
# ---------------------------------------------------------
class FormulirPelanggan(BaseModel):
    first_name: str
    last_name: str
    email: str
    country: str

@app.post("/customers/baru")
def tambah_pelanggan(data_masuk: FormulirPelanggan):
    try:
        connection = psycopg2.connect(
            host=os.getenv("DB_HOST"), port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"), user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        cursor = connection.cursor()
        
        query_insert = """
            INSERT INTO customers (first_name, last_name, email, country)
            VALUES (%s, %s, %s, %s)
            RETURNING customer_id; 
        """
        
        cursor.execute(query_insert, (
            data_masuk.first_name,
            data_masuk.last_name,
            data_masuk.email, 
            data_masuk.country
        ))
        
        id_baru = cursor.fetchone()[0]
        connection.commit()
        
        # FIX 2: Tadi lu kurang titik dua (:) dan koma (,) di dalam return ini
        return {
            "status": "Sukses Mendaftar!",
            "pesan": f"Halo {data_masuk.first_name}, data anda sudah tercatat",
            "id_pelanggan_lu": id_baru
        }
        
    except Exception as error:
        if 'connection' in locals():
            connection.rollback()
        raise HTTPException(status_code=500, detail=f"Gagal memasukkan data: {error}")
        
    finally:
        if 'cursor' in locals(): cursor.close()
        if 'connection' in locals(): connection.close()