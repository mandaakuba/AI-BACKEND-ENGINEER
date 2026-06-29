import requests
from abc import ABC, abstractmethod

# ==========================================
# 1. CUSTOM EXCEPTION (Day 3)
# ==========================================
class KoneksiAPIError(Exception):
    def __init__(self, pesan=""):
        super().__init__(f"Gagal terhubung ke API Notifikasi! {pesan}")


# ==========================================
# 2. ABSTRACTION (Day 2)
# ==========================================
class NotifikasiSistem(ABC):
    
    # Kontrak wajib untuk semua anak class
    @abstractmethod
    def kirim_notif(self):
        pass


# ==========================================
# 3. INHERITANCE & ENCAPSULATION (Day 1)
# ==========================================
class NotifikasiDiscord(NotifikasiSistem):
    def __init__(self, pesan_alert):
        # Menyimpan data public
        self.pesan_alert = pesan_alert
        
        # Menyimpan URL sebagai Private Variable (hanya bisa dipakai di class ini)
        self.__url_api = "https://dummyjson.com/posts/add"

    # ==========================================
    # 4. API POST REQUEST & TRY-EXCEPT (Day 4 & 3)
    # ==========================================
    def kirim_notif(self):
        print(f"Mencoba mengirim alert: '{self.pesan_alert}'...\n")
        
        # Menyiapkan payload/paket JSON
        paket_data = {
            "title": self.pesan_alert,
            "userId": 1
        }

        try:
            # Memanggil API rahasia kita pakai POST
            response = requests.post(self.__url_api, json=paket_data, timeout=5)
            
            if response.status_code in [200, 201]:
                data = response.json()
                print("✅ NOTIFIKASI BERHASIL DIKIRIM!")
                print(f"ID Log: {data.get('id')} | Pesan: {data.get('title')}")
            else:
                print(f"❌ Gagal mengirim. Kode: {response.status_code}")

        # Jika internet putus, tangkap error aslinya, lalu LEMPAR error buatan kita!
        except requests.exceptions.ConnectionError:
            raise KoneksiAPIError("Cek kabel LAN atau WiFi kamu!")
            
        except requests.exceptions.Timeout:
            print("❌ Server Timeout, coba lagi nanti.")


# ==========================================
# 5. UJI COBA KODE (Eksekusi)
# ==========================================

# Membuat objek dari class yang sudah kita rancang
bot_discord = NotifikasiDiscord("SERVER DOWN!")

# Kita bungkus dengan try-except agar kalau KoneksiAPIError terpicu (saat offline), 
# terminal tidak dipenuhi tulisan merah error yang jelek.
try:
    bot_discord.kirim_notif()
except KoneksiAPIError as e:
    print(f"🚨 ALARM DARURAT: {e}")