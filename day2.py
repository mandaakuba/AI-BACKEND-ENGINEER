import asyncio
import time

async def masak_air():
    print("1. Menyalakan kompor dan air")
    await asyncio.sleep(2)
    print("3. air mendidih")
async def potong_sayur():
    print("2.Memotong Sayur")
    await asyncio.sleep(1)
    print("4. Sayur Siap Dipotong")

async def main():
    catat_waktu_mulai = time.time()

    print("Memulai Sarapan")
    await masak_air()
    await potong_sayur()
    
    waktu_total = time.time() - catat_waktu_mulai
    print(f"memasak selesai dalam {waktu_total:.2f} detik")

asyncio.run(main())

import asyncio
import time
import aiohttp




async def masak_air():
    print("1. Menyalakan kompor dan air")
    await asyncio.sleep(2)
    print("3. air mendidih")
async def potong_sayur():
    print("2.Memotong Sayur")
    await asyncio.sleep(1)
    print("4. Sayur Siap Dipotong")

async def main():
    catat_waktu_mulai = time.time()
    print("memulai masak super cepat")
    await asyncio.gather(
        masak_air(),
        potong_sayur()
        
    )
    waktu_total = time.time() - catat_waktu_mulai

    print (f"memasak selesai dalam waktu {waktu_total:.2f} detik")


asyncio.run(main())










