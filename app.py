import streamlit as st
import os
import time
import logging

# Modüllerimiz
from src.ingestion import load_documents, split_documents
from src.vector_store import create_vector_db
from src.rag_chain import get_rag_chain
from src.utils import get_user_dirs, clear_user_data

# LOG AYARI
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="Vektra AI | Kurumsal Hafıza",
    page_icon="assets/logo.png", # Logonun "assets" klasöründe olduğunu varsayıyoruz
    layout="wide"
)

user_source_dir, user_vector_db_dir = get_user_dirs()

if os.path.exists("assets/logo.png"):
    st.image("assets/logo.png", width=100)

st.title("Vektra AI - Kurumsal Asistan")
st.markdown(
    """
    Bu asistan, yüklediğiniz **PDF, Word, Excel ve CSV** dosyalarını okur, analiz eder 
    ve sorularınıza **dokümanlara dayanarak** cevap verir.
    """
)

# YAN MENÜ 
with st.sidebar:
    if os.path.exists("assets/logo.png"):
        st.image("assets/logo.png", use_column_width=True)
        
    st.header("📂 Doküman Yönetimi")
    st.info(f"Oturum ID: {os.path.basename(user_source_dir)}") # Debug için ID gösterelim
    
    uploaded_files = st.file_uploader(
        "PDF, Word, Excel veya CSV yükleyin",
        accept_multiple_files=True,
        type=["pdf", "docx", "csv", "xlsx"]
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        process_btn = st.button("🚀 Verileri İşle")
        
    with col2:
        if st.button("🗑️ Temizle"):
            clear_user_data()
            st.success("Hafıza temizlendi!")
            time.sleep(1)
            st.rerun()

    # İŞLEME BUTONU MANTIĞI
    if process_btn and uploaded_files:
        with st.spinner("Dokümanlar analiz ediliyor... ⏳"):
            try:
                
                if not os.path.exists(user_source_dir):
                    os.makedirs(user_source_dir)

                # 2. Dosyaları Kaydet
                for uploaded_file in uploaded_files:
                    file_path = os.path.join(user_source_dir, uploaded_file.name)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                
                # 3. Ingestion (Okuma & Parçalama)
                st.text("📄 Dosyalar okunuyor...")
                docs = load_documents(user_source_dir)
                chunks = split_documents(docs)
                
                # 4. Vector Store (Kaydetme)
                st.text("🧠 Bilgiler vektörlere çevriliyor...")
                create_vector_db(chunks, user_vector_db_dir)
                
                st.success(f"✅ {len(uploaded_files)} dosya başarıyla öğrenildi!")
                
            except Exception as e:
                st.error(f"Hata oluştu: {e}")
                logger.error(f"UI Error: {e}", exc_info=True)

# CHAT EKRANI

# Sohbet geçmişini başlat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Merhaba! Yüklediğiniz dokümanlarla ilgili ne bilmek istersiniz?"}
    ]

# Mesajları ekrana bas
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcıdan soru al
if prompt := st.chat_input("Sorunuzu buraya yazın..."):
    
    # Kullanıcı mesajını göster
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        
    # AI Cevabı
    with st.chat_message("assistant"):
        with st.spinner("Cevap aranıyor..."):
            try:
                # Kullanıcının ÖZEL veritabanını kullanarak zinciri kur
                qa_chain = get_rag_chain(user_vector_db_dir)
                
                if qa_chain:
                    response = qa_chain.invoke({"query": prompt})
                    result = response['result']
                    
                    # Kaynakları topla
                    sources = [os.path.basename(doc.metadata.get('source', '')) for doc in response['source_documents']]
                    sources = list(set(sources))
                    
                    st.markdown(result)
                    
                    if sources:
                        st.caption(f"📚 Kaynaklar: {', '.join(sources)}")
                        
                    st.session_state.messages.append({"role": "assistant", "content": result})
                else:
                    st.warning("⚠️ Lütfen önce sol taraftan doküman yükleyip 'Verileri İşle' butonuna basın.")
                    
            except Exception as e:
                logger.error(f"Chat Error: {e}", exc_info=True)
                st.error("Bir sorun oluştu. Lütfen doküman yüklediğinizden emin olun.")