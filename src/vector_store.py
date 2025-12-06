import os
import time
import logging
from typing import List, Optional
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from src.embedding import get_embedding_model

# 1. LOGGING
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(log_dir, "vector_store.log"), encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def create_vector_db(chunks: List[Document], save_path: str) -> Optional[FAISS]:
    """
    Gelen tüm parçaları (chunks) alır ve SIFIRDAN bir vektör veritabanı yaratıp kaydeder.
    Bu fonksiyon "Full Refresh" mantığıyla çalışır.
    """
    if not chunks:
        logger.warning("⚠️ Vektörleştirilecek veri yok. İşlem atlandı.")
        return None

    # Klasör yoksa oluştur
    if not os.path.exists(save_path):
        try:
            os.makedirs(save_path)
        except OSError as e:
            logger.error(f"❌ Klasör oluşturulurken hata: {e}")
            return None

    try:
        start_time = time.time()
        logger.info("🔄 Embedding modeli yükleniyor...")
        
        embedding_model = get_embedding_model()
        
        logger.info(f"🚀 {len(chunks)} parça için Vektör DB OLUŞTURULUYOR (Sıfırdan)...")
        
        # FAISS oluşturma (Eskiyi siler, yenisini yazar - Doğrusu budur çünkü tüm klasörü gönderiyoruz)
        vector_store = FAISS.from_documents(
            documents=chunks,
            embedding=embedding_model
        )
        
        # Kaydetme
        vector_store.save_local(save_path)
        
        duration = time.time() - start_time
        logger.info(f"💾 Veritabanı başarıyla kaydedildi: {save_path} (Süre: {duration:.2f}s)")
        return vector_store

    except Exception as e:
        logger.error(f"❌ Vektör DB oluşturulurken kritik hata: {e}")
        raise e

def load_vector_db(load_path: str) -> Optional[FAISS]:
    """
    Veritabanını diskten okur.
    """
    logger.info(f"📂 Vektör Veritabanı yükleniyor: {load_path}")
    
    if not os.path.exists(load_path):
        logger.error(f"❌ Veritabanı bulunamadı: {load_path}")
        return None
        
    try:
        embedding_model = get_embedding_model()
        
        vector_store = FAISS.load_local(
            load_path, 
            embedding_model,
            allow_dangerous_deserialization=True 
        )
        
        logger.info("✅ Veritabanı başarıyla yüklendi.")
        return vector_store
        
    except Exception as e:
        logger.error(f"❌ Yükleme hatası: {e}")
        return None

if __name__ == "__main__":
    pass