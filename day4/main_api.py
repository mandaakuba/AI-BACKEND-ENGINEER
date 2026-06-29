from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from day4 import SessionLocal, AIModelLog, engine, Base

Base.metadata.create_all(bind=engine)
app = FastAPI(title= "AI Backend API")

#pydantic_schemas
class LogCreate(BaseModel):
    model_name: str
    accuracy: str
class LogResponse(BaseModel):
    id: int
    model_name: str
    accuracy: str
    class Config:
        from_attributes = True

def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally: 
        db.close()


#CRUD API ENDPOINT
@app.post("/logs/", response_model=LogResponse)
def tambah_log(log_masuk: LogCreate, db: Session = Depends(get_db)):
    log_baru = AIModelLog(model_name=log_masuk.model_name, accuracy=log_masuk.accuracy)
    db.add(log_baru)
    db.commit()
    db.refresh(log_baru)

    return log_baru

# B. Endpoint untuk Read Semua Data (R) dengan Pagination
@app.get("/logs/", response_model=List[LogResponse])
def lihat_semua_log(
    limit: int = 10, # <-- Ini otomatis jadi Query Parameter karena gak ada di path "/logs/"
    skip: int = 0,   # <-- Sama, ini juga Query Parameter
    db: Session = Depends(get_db)
):
    # Terapkan filter pagination ke database
    semua_log = db.query(AIModelLog).offset(skip).limit(limit).all()
    
    return semua_log


# C. Endpoint untuk Update Data (U)
@app.put("/logs/{log_id}", response_model=LogResponse)
def update_log(log_id: int, log_update: LogCreate, db: Session = Depends(get_db)):
    # 1. Cari data di database berdasarkan ID yang dikirim di URL
    log_lama = db.query(AIModelLog).filter(AIModelLog.id == log_id).first()
    
    # 2. Kalau datanya gak ketemu, kasih error 404 Not Found ke user
    if not log_lama:
        raise HTTPException(status_code=404, detail="Waduh, data log tidak ditemukan bos!")
    
    # 3. Kalau ketemu, ubah isinya dengan data baru yang dikirim user (log_update)
    log_lama.model_name = log_update.model_name
    log_lama.accuracy = log_update.accuracy
    
    # 4. Simpan perubahan ke database
    db.commit()
    db.refresh(log_lama)
    
    return log_lama

# D. Endpoint untuk Delete Data (D)
@app.delete("/logs/{log_id}")
def hapus_log(log_id: int, db: Session = Depends(get_db)):
    # 1. Cari data yang mau dihapus
    log_hapus = db.query(AIModelLog).filter(AIModelLog.id == log_id).first()
    
    # 2. Kalau gak ketemu, lempar error
    if not log_hapus:
        raise HTTPException(status_code=404, detail="Data udah gak ada atau emang salah ID.")
    
    # 3. Eksekusi hapus dan commit
    db.delete(log_hapus)
    db.commit()
    
    return {"message": f"Sukses! Log AI dengan ID {log_id} berhasil dihapus dari muka bumi."}