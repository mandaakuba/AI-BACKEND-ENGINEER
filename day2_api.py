import asyncio
import time
import aiohttp # Sang Kurir Turbo

# 1. Fungsi untuk menembak 1 API
async def ambil_quote(id_kurir, session):
    url = "https://dummyjson.com/quotes/random"
    print(f"🚀 Kurir {id_kurir} berangkat...")
    
    # Membuka pintu ke server dengan 'async with'
    async with session.get(url) as response:
        # Menunggu paket JSON dibongkar
        data = await response.json() 
        print(f"✅ Kurir {id_kurir} pulang bawa quote: {data.get('quote')}")

# 2. Fungsi Manajer Utama
async def main():
    waktu_mulai = time.time()
    
    # Membuat 1 sesi utama (ibarat menyewa 1 truk besar aiohttp untuk semua kurir)
    async with aiohttp.ClientSession() as session:
        print("--- MULAI SPAM API ---")
        
        # Menyuruh 3 kurir berangkat BERSAMAAN pakai gather
        await asyncio.gather(
            ambil_quote(1, session),
            ambil_quote(2, session),
            ambil_quote(3, session),
            ambil_quote(4, session),
            ambil_quote(5, session),
            ambil_quote(6, session),
            ambil_quote(7, session),
            ambil_quote(8, session),
            ambil_quote(9, session),
            ambil_quote(10, session),
            ambil_quote(11, session),
            ambil_quote(12, session),
            ambil_quote(13, session),
            ambil_quote(14, session),
            ambil_quote(15, session),
            ambil_quote(16, session)

        )
        
    waktu_total = time.time() - waktu_mulai
    print(f"--- SELESAI DALAM {waktu_total:.2f} DETIK ---")

# 3. Tombol Start
asyncio.run(main())

