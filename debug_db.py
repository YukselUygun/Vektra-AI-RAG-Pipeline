import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

def test_connection():
    print("🕵️‍♂️ Veritabanı Bağlantı Testi Başlıyor...")
    
    # .env'den bilgileri al
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST", "127.0.0.1")
    port = os.getenv("DB_PORT", "5433") # Localden bağlanırken 5433 olmalı!
    dbname = os.getenv("DB_NAME", "vektra_dwh")
    
    print(f"📡 Ayarlar: {host}:{port} | Kullanıcı: {user} | DB: {dbname}")
    
    url = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
    
    try:
        engine = create_engine(url)
        with engine.connect() as conn:
            print("✅ BAŞARILI! Veritabanına giriş yapıldı.")
            
            # Tablo var mı?
            result = conn.execute(text("SELECT count(*) FROM document_logs"))
            count = result.fetchone()[0]
            print(f"📊 Mevcut Kayıt Sayısı: {count}")
            
            if count == 0:
                print("⚠️ Tablo var ama içi boş. Kayıt atılmamış.")
            else:
                print("🎉 Tabloda veri var! Dashboard'da görünmesi lazım.")
                
    except Exception as e:
        print("❌ HATA! Bağlantı kurulamadı.")
        print(f"Hata Detayı: {e}")

if __name__ == "__main__":
    test_connection()