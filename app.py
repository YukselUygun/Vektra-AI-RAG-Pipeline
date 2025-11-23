import streamlit as st
import os
import time
import logging
from src.ingestion import load_documents, split_documents
from src.vector_store import create_vector_db
from src.rag_chain import get_rag_chain

logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="Vektra AI | Kurumsal Hafıza",
    page_icon="Vektra_logo.png",  
    layout="wide"
)

st.title(" Vektra AI - Kurumsal Asistan")
st.markdown(
    """
    Bu asistan, yüklediğiniz **PDF, Word, Excel ve CSV** dosyalarını okur, analiz eder 
    ve sorularınıza **dokümanlara dayanarak** cevap verir.
    """
)

#YAN MENÜ- VERİ YÜKLEME ALANI 
with st.sidebar:
    st.image("Vektra_logo.png", width=200)
    st.header("📂 Doküman Yönetimi")
    
    # 1. Dosya Yükleyici 
    uploaded_files = st.file_uploader(
        "Dokümanları buraya sürükleyin",
        accept_multiple_files=True,
        type=["pdf", "docx", "csv", "xlsx"]
    )
    
    # 2. İşle Butonu
    if st.button("🚀 Verileri İşle ve Hafızaya At"):
        if not uploaded_files:
            st.warning("Lütfen önce dosya yükleyin!")
        else:
            with st.spinner("Dokümanlar işleniyor... Bu biraz zaman alabilir ⏳"):
                
                save_dir = "data/source_docs"
                if not os.path.exists(save_dir):
                    os.makedirs(save_dir)
                
                for f in os.listdir(save_dir):
                    os.remove(os.path.join(save_dir, f))

                for uploaded_file in uploaded_files:
                    file_path = os.path.join(save_dir, uploaded_file.name)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                
                st.success(f"✅ {len(uploaded_files)} dosya başarıyla yüklendi!")
                
                st.text("📄 Dosyalar okunuyor...")
                docs = load_documents()
                chunks = split_documents(docs)
                
                st.text("🧠 Bilgiler vektörlere çevriliyor...")
                create_vector_db(chunks)
                
                st.success("🎉 İşlem Tamam! Vektra artık bu dokümanları biliyor.")
                time.sleep(1)
                st.rerun()

#ANA EKRAN

# 1. Sohbet Geçmişini Başlat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Merhaba! Dokümanlarınız hakkında bana soru sorabilirsiniz. 👋"}
    ]

# 2. Geçmiş Mesajları Ekrana Yazdır
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. Kullanıcıdan Girdi Al
if prompt := st.chat_input("Sorunuzu buraya yazın..."):
    
    # A) Kullanıcı mesajını ekrana koy ve hafızaya at
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        
    # B) AI Cevabını Üret
    with st.chat_message("assistant"):
        with st.spinner("Vektra düşünüyor... 🤔"):
            try:
                # RAG Zincirini Çağır
                qa_chain = get_rag_chain()
                
                if qa_chain:
                    # Soruyu sor ve cevabı al
                    response = qa_chain.invoke({"query": prompt})
                    result = response['result']
                    
                    # Kaynakları göster
                    sources = [doc.metadata.get('source', 'Bilinmiyor') for doc in response['source_documents']]
                    sources = list(set(sources))
                    
                    st.markdown(result)
                    
                    if sources:
                        st.caption(f"📚 Kaynaklar: {', '.join([os.path.basename(s) for s in sources])}")
                        
                    st.session_state.messages.append({"role": "assistant", "content": result})
                else:
                    st.error("Hata: RAG Zinciri oluşturulamadı. Lütfen önce veri yükleyin.")

            except Exception as e:
                logger.error(f"🚨 Kritik Hata: {str(e)}", exc_info=True)
                st.error(f"Bir hata oluştu: {e}. Lütfen logları kontrol edin.")