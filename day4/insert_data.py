# File: insert_data.py

# Import SessionLocal dan Model dari file day4 lu
from day4 import SessionLocal, AIModelLog

def simpan_log_ai():
    # 1. Buka jalur komunikasi ke database
    session = SessionLocal()

    try:
        # 2. Bikin objek data baru dari class AIModelLog
        log_pertama = AIModelLog(model_name="YOLOv8_Deteksi_Objek", accuracy="95.2%")
        log_kedua = AIModelLog(model_name="BERT_Analisis_Sentimen", accuracy="89.1%")

        # 3. Masukkan objek ke dalam 'keranjang belanja' sesi lu
        session.add(log_pertama)
        session.add(log_kedua)

        # 4. Eksekusi penyimpanan permanen ke database (INSERT)
        session.commit()
        print("Yeay! Data log AI berhasil disimpan ke database.")

    except Exception as e:
        # Kalau ada error di tengah jalan, batalkan semua biar data gak korup
        session.rollback()
        print(f"Waduh, ada error: {e}")

    finally:
        # 5. WAJIB tutup sesi kalau udah selesai biar koneksi database gak penuh
        session.close()

if __name__ == "__main__":
    simpan_log_ai()