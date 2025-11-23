import os
import time
import logging
from typing import List, Optional
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from src.embedding import get_embedding_model
from src.config import Config

# 1. LOG AYARLARI
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(os.path.join(log_dir, "vector_store.log"), encoding='utf-8'), # Dosyaya yaz
        logging.StreamHandler() # Ekrana yaz
    ]
)
logger = logging.getLogger(__name__)

def create_vector_db(chunks: List[Document]) -> Optional[FAISS]:
    """
    Parçalanmış metinleri vektöre çevirip FAISS veritabanına kaydeder.
    
    Args:
        chunks (List[Document]): Metin parçaları listesi.
        
    Returns:
        Optional[FAISS]: Oluşturulan veritabanı nesnesi veya None.
    """
    # 2. TİP KONTROLÜ VE GÜVENLİK
    if not chunks:
        logger.warning("⚠️ Vektörleştirilecek veri yok. İşlem atlandı.")
        return None

    # 3. KLASÖR KONTROLÜ 
    if not os.path.exists(Config.VECTOR_DB_PATH):
        try:
            os.makedirs(Config.VECTOR_DB_PATH)
            logger.info(f"📁 Klasör oluşturuldu: {Config.VECTOR_DB_PATH}")
        except OSError as e:
            logger.error(f"❌ Klasör oluşturulurken hata: {e}")
            return None

    try:
        # 4. ZAMANLAMA 
        start_time = time.time()
        logger.info("🔄 Embedding modeli yükleniyor...")
        
        embedding_model = get_embedding_model()
        
        logger.info(f"🚀 {len(chunks)} parça için Vektör DB oluşturuluyor (Bu işlem zaman alabilir)...")
        
        # FAISS oluşturma 
        vector_store = FAISS.from_documents(
            documents=chunks,
            embedding=embedding_model
        )
        
        vector_store.save_local(Config.VECTOR_DB_PATH)
        
        end_time = time.time()
        duration = end_time - start_time
        
        logger.info(f"💾 Veritabanı başarıyla kaydedildi! Süre: {duration:.2f} saniye.")
        return vector_store

    # 5.HATA YÖNETİMİ
    except Exception as e:
        logger.error(f"❌ Vektör DB oluşturulurken kritik hata: {e}")
        raise e

def load_vector_db() -> Optional[FAISS]:
    """
    Disktekli veritabanını yükler.
    
    Returns:
        Optional[FAISS]: Yüklenen veritabanı.
    """
    logger.info(f"📂 Vektör Veritabanı yükleniyor: {Config.VECTOR_DB_PATH}")
    
    if not os.path.exists(Config.VECTOR_DB_PATH):
        logger.error(f"❌ Veritabanı bulunamadı: {Config.VECTOR_DB_PATH}. Lütfen önce oluşturun.")
        return None
        
    try:
        embedding_model = get_embedding_model()
        
        vector_store = FAISS.load_local(
            Config.VECTOR_DB_PATH, 
            embedding_model,
            allow_dangerous_deserialization=True 
        )
        
        logger.info("✅ Veritabanı başarıyla yüklendi ve aramaya hazır.")
        return vector_store
        
    except Exception as e:
        logger.error(f"❌ Veritabanı yüklenirken hata: {e}")
        return None

if __name__ == "__main__":
    # Test Senaryosu
    from src.ingestion import load_documents, split_documents
    
    logger.info("🚀 --- VEKTÖR DB TEST BAŞLANGICI ---")

    docs = load_documents()
    chunks = split_documents(docs)
    
    if chunks:
        create_vector_db(chunks)
    
    load_vector_db()
    
    logger.info("🏁 --- TEST BİTİŞİ ---")