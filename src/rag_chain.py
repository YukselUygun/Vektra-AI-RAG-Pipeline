import logging
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from src.vector_store import load_vector_db
from src.config import Config

# 1. LOGGING AYARLARI
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(log_dir, "rag_chain.log"), encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def get_rag_chain():
    """
    RAG (Retrieval-Augmented Generation) zincirini oluşturur.
    Bu zincir: Soru -> Vektör DB'de Ara -> Bulunanları LLM'e Ver -> Cevap Üret
    akışını yönetir.
    """
    try:
        # A) Hafızayı Yükle
        logger.info("🧠 Hafıza (Vektör DB) yükleniyor...")
        vector_store = load_vector_db()
        
        if not vector_store:
            raise Exception("Vektör veritabanı yüklenemedi!")
            
        retriever = vector_store.as_retriever(search_kwargs={"k": 3})

        # B) Zekayı Hazırla
        logger.info(f"🤖 Yapay Zeka Modeli hazırlanıyor: {Config.LLM_MODEL_NAME}")
        llm = ChatGoogleGenerativeAI(
            model=Config.LLM_MODEL_NAME,
            google_api_key=Config.GOOGLE_API_KEY,
            temperature=0.3  
        )

        # C) Talimatları Hazırla.
        prompt_template = """
        Sen kurumsal bir asistansın. Aşağıdaki bağlamı (context) kullanarak kullanıcının sorusunu cevapla.
        Eğer sorunun cevabı bağlamda yoksa, "Bu konuda bilgim yok" de, uydurma cevap verme.
        Cevabı verirken nazik ve profesyonel ol.

        Bağlam (Context):
        {context}

        Soru:
        {question}

        Cevap:
        """
        
        PROMPT = PromptTemplate(
            template=prompt_template, 
            input_variables=["context", "question"]
        )

        # D) Zinciri (Chain) Kur
        logger.info("🔗 RAG Zinciri (Chain) oluşturuluyor...")
        chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff", 
            retriever=retriever,
            return_source_documents=True, 
            chain_type_kwargs={"prompt": PROMPT}
        )
        
        logger.info("✅ RAG Zinciri hazır!")
        return chain

    except Exception as e:
        logger.error(f"❌ RAG Zinciri oluşturulurken hata: {e}")
        return None

if __name__ == "__main__":
    # TEST SENARYOSU
    logger.info("🧪 --- CHATBOT TESTİ BAŞLIYOR ---")
    
    qa_chain = get_rag_chain()
    
    if qa_chain:
        soru = "Bu doküman ne hakkında?" 
        
        logger.info(f"❓ Soru: {soru}")
        
        # Zinciri Çalıştır
        response = qa_chain.invoke({"query": soru})
        
        print("\n" + "="*50)
        print(f"🤖 CEVAP:\n{response['result']}")
        print("="*50 + "\n")
        
        # Kaynakları Göster 
        print("📚 Kaynaklar:")
        for doc in response['source_documents']:
            print(f"- {doc.metadata.get('source', 'Bilinmeyen Kaynak')}")
            
    logger.info("🏁 --- TEST BİTİŞİ ---")