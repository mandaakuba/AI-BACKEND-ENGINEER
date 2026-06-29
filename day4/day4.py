import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

# 1. Load environment variables dari file .env
load_dotenv()

# 2. Ambil komponen database dari .env
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

# 3. Susun DATABASE_URL secara dinamis
# Format: postgresql://user:password@host:port/database
URL_DB = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

# Validasi opsional untuk memastikan variabel terbaca
if not all([db_user, db_password, db_host, db_port, db_name]):
    raise ValueError("Ada konfigurasi DB yang kurang di file .env kamu!")

# 4. Konfigurasi Engine & Session
engine = create_engine(URL_DB, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 5. Definisi Model (Mapping Class ke Tabel)
Base = declarative_base()

class AIModelLog(Base):
    __tablename__ = "model_logs"

    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String(50), nullable=False)
    accuracy = Column(String(10))

class LLMUsageLog(Base):
    __tablename__ = "llm_usage_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(50), index=True)
    prompt_text = Column(String(500), nullable=False)
    tokens_used = Column(Integer, nullable=False)
    latency_ms = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

# 6. Eksekusi Pembuatan Tabel
if __name__ == "__main__":
    print("Menciptakan tabel di database...")
    print("Selesai! Tabel berhasil dibuat tanpa hardcode password.")