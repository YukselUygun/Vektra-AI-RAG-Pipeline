import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    
    # 1. Google API Anahtarı
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    
    # 2. Model Ayarları
    LLM_MODEL_NAME = "gemini-2.0-flash"
    
    # Embedding (Tercüman): Metni sayıya çeviren model
    EMBEDDING_MODEL_NAME = "models/text-embedding-004"
    
    # 3. Vektör Veritabanı Ayarları
    VECTOR_DB_PATH = "faiss_index"
    
    # 4. PDF İşleme Ayarları (Chunking)
    CHUNK_SIZE = 1000     
    CHUNK_OVERLAP = 200    

    if not GOOGLE_API_KEY:
        raise ValueError("❌ HATA: GOOGLE_API_KEY .env dosyasında bulunamadı!")

