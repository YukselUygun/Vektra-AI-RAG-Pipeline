import os
import logging
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.embeddings import Embeddings
from src.config import Config

# 1. LOGGING AYARLARI
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(log_dir, "embedding.log"), encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def get_embedding_model() -> Embeddings:
    """
    Google Gemini Embedding modelini başlatır ve döndürür.
    Bu model, metinleri sayısal vektörlere çevirir.
    
    Returns:
        Embeddings: LangChain uyumlu embedding modeli nesnesi.
    """
    try:
        model_name = Config.EMBEDDING_MODEL_NAME
        
        logger.info(f"🔌 Embedding modeli hazırlanıyor: {model_name}")
        
        embeddings = GoogleGenerativeAIEmbeddings(
            model=model_name,
            google_api_key=Config.GOOGLE_API_KEY
        )
        
        return embeddings
    
    except Exception as e:
        logger.error(f"❌ Embedding modeli yüklenirken kritik hata: {e}")
        raise e

if __name__ == "__main__":
    # TEST SENARYOSU
    logger.info("🧪 --- EMBEDDING TEST BAŞLANGICI ---")
    
    try:
        embed_model = get_embedding_model()
        
        test_text = "Veri Mühendisliği, geleceği inşa eden meslektir."
        vector = embed_model.embed_query(test_text)
        
        logger.info(f"✅ Test Metni: '{test_text}'")
        logger.info(f"📊 Vektör Boyutu (Dimension): {len(vector)}")
        logger.info(f"🔢 İlk 5 Değer: {vector[:5]}...")
        
        if len(vector) > 0:
            logger.info("🎉 Model başarıyla çalışıyor ve sayısal çıktı üretiyor.")
        else:
            logger.error("⚠️ Model çalıştı ama boş vektör döndürdü!")
            
    except Exception as e:
        logger.error(f"❌ Test sırasında hata oluştu: {e}")
        
    logger.info("🏁 --- TEST BİTİŞİ ---")