import streamlit as st
import logging
from src.ui.login import render_login
from src.ui.sidebar import render_sidebar
from src.ui.dashboard import render_dashboard
from src.rag_chain import get_rag_chain
from src.utils import get_shared_dirs 

logging.basicConfig(level=logging.INFO)

st.set_page_config(page_title="Vektra AI", page_icon="assets/logo.png", layout="wide")

shared_source_dir, shared_vector_db_dir = get_shared_dirs()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_role = None

if not st.session_state.logged_in:
    render_login()
else:
    role = st.session_state.user_role
    
    render_sidebar(role, shared_source_dir, shared_vector_db_dir)
    
    st.title(f"🤖 Vektra AI ({role} Modu)")
    
    if role == "Admin":
        tab1, tab2 = st.tabs(["💬 Sohbet", "📊 Yönetim Paneli"])
        
        with tab1:
            if "messages" not in st.session_state:
                st.session_state.messages = [{"role": "assistant", "content": "Yönetici modundasınız. Test edebilirsiniz."}]

            for msg in st.session_state.messages:
                st.chat_message(msg["role"]).write(msg["content"])

            if prompt := st.chat_input():
                st.session_state.messages.append({"role": "user", "content": prompt})
                st.chat_message("user").write(prompt)
                
                with st.chat_message("assistant"):
                    # Admin de ortak alandan okur
                    qa_chain = get_rag_chain(shared_vector_db_dir)
                    if qa_chain:
                        res = qa_chain.invoke({"query": prompt})
                        st.write(res['result'])
                        st.session_state.messages.append({"role": "assistant", "content": res['result']})
                    else:
                        st.warning("Bilgi bankası boş.")
        
        with tab2:
            render_dashboard()

    else:
        # USER MODU (ÇALIŞAN)
        st.subheader("💬 Doküman Asistanı")
        
        if "messages" not in st.session_state:
            st.session_state.messages = [{"role": "assistant", "content": "Merhaba! Şirket dokümanları hakkında soru sorabilirsiniz."}]

        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])

        if prompt := st.chat_input():
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)
            
            with st.chat_message("assistant"):
                qa_chain = get_rag_chain(shared_vector_db_dir)
                if qa_chain:
                    res = qa_chain.invoke({"query": prompt})
                    st.write(res['result'])
                    st.session_state.messages.append({"role": "assistant", "content": res['result']})
                else:
                    st.error("Henüz yönetici tarafından sisteme veri yüklenmemiş. Lütfen bekleyiniz.")