import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    
    # Google API Anahtarı
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    
    # Model Ayarları
    LLM_MODEL_NAME = "gemini-2.0-flash"
    
    # Embedding (Tercüman): Metni sayıya çeviren model
    EMBEDDING_MODEL_NAME = "models/text-embedding-004"
    
    # PDF İşleme Ayarları (Chunking)
    CHUNK_SIZE = 1000     
    CHUNK_OVERLAP = 200    

    if not GOOGLE_API_KEY:
        raise ValueError("❌ HATA: GOOGLE_API_KEY .env dosyasında bulunamadı!")

