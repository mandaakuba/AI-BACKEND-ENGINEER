from sqlalchemy import func, desc
from day4 import SessionLocal, LLMUsageLog

def analisa_data_llm():
    session = SessionLocal()
    print("\n=== 📊 HASIL ANALISIS 5000 DATA LOG LLM ===\n")
    
    try:
        # 1. Menghitung Total Request (COUNT)
        total_req = session.query(LLMUsageLog).count()
        print(f"1. Total Request API : {total_req:,} kali")
        
        # 2. Menghitung Total Token (SUM) - Penting buat ngitung cost/biaya LLM!
        total_token = session.query(func.sum(LLMUsageLog.tokens_used)).scalar()
        print(f"2. Total Token Bakar : {total_token:,} tokens")
        
        # 3. Menghitung Rata-rata Kecepatan AI (AVG)
        avg_latency = session.query(func.avg(LLMUsageLog.latency_ms)).scalar()
        print(f"3. Rata-rata Latency : {avg_latency:.2f} ms")
        
        # 4. Mencari 3 User Paling Boros (GROUP BY & ORDER BY)
        print("\n4. Top 3 User Paling Boros Token:")
        top_users = session.query(
            LLMUsageLog.user_id, 
            func.sum(LLMUsageLog.tokens_used).label('total_tokens')
        ).group_by(
            LLMUsageLog.user_id
        ).order_by(
            desc('total_tokens')
        ).limit(3).all()
        
        for i, user in enumerate(top_users, 1):
            print(f"   🏆 Rank {i}: {user.user_id} (Menghabiskan {user.total_tokens:,} tokens)")
            
    except Exception as e:
        print(f"Waduh error bos: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    analisa_data_llm()