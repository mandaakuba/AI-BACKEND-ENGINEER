import random
from faker import Faker
from day4 import SessionLocal, LLMUsageLog

# Inisiasi Faker dengan bahasa Indonesia
fake = Faker('id_ID')

def suntik_data_ribuan():
    session = SessionLocal()
    print("Menyiapkan 5.000 data log LLM... Tunggu sebentar ya bos!")
    
    try:
        data_batch = []
        
        # Looping 5000 kali
        for _ in range(5000):
            # Bikin log bohongan
            log_baru = LLMUsageLog(
                user_id=f"user_{fake.random_int(min=100, max=999)}",
                prompt_text=fake.sentence(nb_words=8),
                tokens_used=random.randint(50, 2000),
                latency_ms=round(random.uniform(200.0, 3500.0), 2)
            )
            data_batch.append(log_baru)
            
        # Pake add_all biar langsung masukin rombongan (lebih cepat dari add satu-satu)
        session.add_all(data_batch)
        session.commit()
        
        print("BOOM! 5.000 data berhasil mendarat dengan selamat di PostgreSQL.")
        
    except Exception as e:
        session.rollback()
        print(f"Error bos: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    suntik_data_ribuan()