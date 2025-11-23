from langchain_google_genai import GoogleGenerativeAIEmbeddings
from src.config import Config

def get_embedding_model():

    try:
        embeddings = GoogleGenerativeAIEmbeddings(
            model=Config.EMBEDDING_MODEL_NAME, # models/embedding-001
            google_api_key=Config.GOOGLE_API_KEY
        )
        return embeddings
    except Exception as e:
        raise Exception(f"❌ Embedding modeli yüklenirken hata oluştu: {e}")

if __name__ == "__main__":
    # TEST BLOĞU
    print("🧪 Embedding Modeli Test Ediliyor...")
    
    embed_model = get_embedding_model()
    
    test_text = "Veri Mühendisliği harika bir meslek!"
    vector = embed_model.embed_query(test_text)
    
    print(f"✅ Test Metni: '{test_text}'")
    print(f"📊 Vektör Boyutu (Dimension): {len(vector)}")
    print(f"🔢 İlk 5 Sayısal Değer: {vector[:5]}...")
    print("🎉 Model başarıyla çalışıyor!")