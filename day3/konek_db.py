import os
from re import L
from sqlite3 import Cursor

import dotenv
from yarl import Query
import psycopg2
from dotenv import load_dotenv

load_dotenv()
try:
    connection = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    cursor = connection.cursor()
    print("Python berhasil jebol dan konek ke Postgres Docker!\n")
    query = """
        SELECT first_name, country, total_belanja 
        FROM klasifikasi_sultan 
        WHERE kasta_pelanggan = 'Sultan (VIP)'
        LIMIT 3;
    """
    cursor.execute(query)
    
    para_sultan = cursor.fetchall()
    print("--- 3 SULTAN PERTAMA YANG DITANGKAP PYTHON ---")
    for row in para_sultan:
        print(f"Nama: {row[0]} Negara: {row[1]} Total Belanja {row[2]}")
except Exception as error:
    print(f"anjay gagal {error}")
finally:
    if 'cursor' in locals():
        cursor.close()
    if 'connection' in locals():
        connection.close()
        print("koneksi sudah ditutup")
