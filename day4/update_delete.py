from day4 import SessionLocal, AIModelLog

def update_dan_delete():
    session = SessionLocal()
    
    try:
        # ==========================================
        # 1. UPDATE DATA (Mengubah akurasi ID 2)
        # ==========================================
        print("--- Memulai Update ---")
        
        # A. Cari datanya
        log_update = session.query(AIModelLog).filter(AIModelLog.id == 2).first()
        
        if log_update:
            print(f"Akurasi awal {log_update.model_name} adalah {log_update.accuracy}")
            
            # B. Ubah nilainya (kayak ngubah variabel Python biasa)
            log_update.accuracy = "92.5%"
            
            # C. Simpan perubahan ke database
            session.commit()
            print(f"Sukses! Akurasi di-update jadi {log_update.accuracy}\n")
        
        # ==========================================
        # 2. DELETE DATA (Menghapus model ID 1)
        # ==========================================
        print("--- Memulai Delete ---")
        
        # A. Cari datanya
        log_delete = session.query(AIModelLog).filter(AIModelLog.id == 1).first()
        
        if log_delete:
            # B. Tandai untuk dihapus
            session.delete(log_delete)
            
            # C. Eksekusi penghapusan di database
            session.commit()
            print(f"Sukses! Model {log_delete.model_name} berhasil dihapus dari database.")

    except Exception as e:
        session.rollback()
        print(f"Waduh, ada error: {e}")
        
    finally:
        session.close()

if __name__ == "__main__":
    update_dan_delete()