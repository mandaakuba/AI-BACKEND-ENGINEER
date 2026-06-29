# Import SessionLocal dan Model dari file day4
from day4 import SessionLocal, AIModelLog

def lihat_data():
    # Buka sesi
    session = SessionLocal()
    
    try:
        # 1. Mengambil SEMUA data (Sama kayak: SELECT * FROM model_logs)
        semua_log = session.query(AIModelLog).all()
        
        print("--- Semua Data Log AI ---")
        for log in semua_log:
            # Karena SQLAlchemy itu ORM, datanya udah jadi objek Python
            # Lu bisa panggil atributnya pakai titik (.)
            print(f"ID: {log.id} | Model: {log.model_name} | Akurasi: {log.accuracy}")
            
        # 2. Mengambil data dengan FILTER (Sama kayak: SELECT * FROM model_logs WHERE id = 1)
        log_spesifik = session.query(AIModelLog).filter(AIModelLog.id == 1).first()
        
        print("\n--- Pencarian Spesifik (ID = 1) ---")
        if log_spesifik:
            print(f"Ketemu nih! Model dengan ID 1 adalah {log_spesifik.model_name}")
        else:
            print("Data tidak ditemukan.")
            
    except Exception as e:
        print(f"Waduh, ada error: {e}")
    finally:
        # Selalu tutup sesi
        session.close()

if __name__ == "__main__":
    lihat_data()