import streamlit as st
import logging
import os

from src.ui.login import render_login
from src.ui.sidebar import render_sidebar
from src.ui.dashboard import render_dashboard
from src.rag_chain import get_rag_chain
from src.utils import get_shared_dirs, get_session_id
from src.database import insert_document_log

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="Vektra AI | Kurumsal Hafıza",
    page_icon="assets/logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_role = None

if not st.session_state.logged_in:
    render_login()
    st.stop() 

# --- KULLANICI VE YOL BİLGİLERİ ---
role = st.session_state.user_role
shared_source_dir, shared_vector_db_dir = get_shared_dirs()
session_id = get_session_id()

render_sidebar(role, shared_source_dir, shared_vector_db_dir)

# --- BAŞLIK ---
col_logo, col_title = st.columns([1, 15])
with col_logo:
    if os.path.exists("assets/logo.png"):
        st.image("assets/logo.png", width=60)
with col_title:
    st.title(f"Vektra AI ({role} Modu)")
    st.caption("Kurumsal dokümanlarınız üzerinde akıllı arama ve soru-cevap asistanı.")

if "messages" not in st.session_state:
    welcome_msg = "Yönetici modundasınız. Test edebilirsiniz." if role == "Admin" else "Merhaba! Şirket dokümanları hakkında soru sorabilirsiniz."
    st.session_state.messages = [{"role": "assistant", "content": welcome_msg}]

# SEKME YAPISI (Admin vs User Farkı)
if role == "Admin":
    tab_chat, tab_dashboard = st.tabs(["💬 Sohbet", "📊 Yönetim Paneli"])
else:
    tab_chat = st.container()
    tab_dashboard = None

# 1. SOHBET EKRANI 

with tab_chat:
    
    chat_container = st.container(height=600, border=True)

    with chat_container:
        for message in st.session_state.messages:
            avatar_icon = "assets/logo.png" if message["role"] == "assistant" and os.path.exists("assets/logo.png") else None
            
            with st.chat_message(message["role"], avatar=avatar_icon):
                st.markdown(message["content"])

    # --- SABİT INPUT ALANI
    if prompt := st.chat_input("Sorunuzu buraya yazın..."):
        
        # A) Kullanıcı mesajını ekle
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_container:
            with st.chat_message("user"):
                st.markdown(prompt)
        
        # B) AI Cevabını Üret
        with chat_container:
            with st.chat_message("assistant", avatar="assets/logo.png" if os.path.exists("assets/logo.png") else None):
                with st.spinner("Vektra düşünüyor..."):
                    try:
                        qa_chain = get_rag_chain(shared_vector_db_dir)
                        
                        if qa_chain:
                            response = qa_chain.invoke({"query": prompt})
                            result = response['result']
                            
                            sources = [os.path.basename(doc.metadata.get('source', '')) for doc in response['source_documents']]
                            sources = list(set(sources))
                            
                            st.markdown(result)
                            
                            if sources:
                                st.caption(f"📚 Kaynaklar: {', '.join(sources)}")
                            
                            st.session_state.messages.append({"role": "assistant", "content": result})
                            
                        else:
                            error_msg = "⚠️ Bilgi bankası boş veya yüklenemedi. Yönetici veri yüklememiş olabilir."
                            st.warning(error_msg)
                            st.session_state.messages.append({"role": "assistant", "content": error_msg})

                    except Exception as e:
                        logger.error(f"Chat Error: {e}", exc_info=True)
                        st.error("Bir hata oluştu. Lütfen daha sonra tekrar deneyin.")

# 2. YÖNETİM PANELİ 
if role == "Admin" and tab_dashboard:
    with tab_dashboard:
        render_dashboard()