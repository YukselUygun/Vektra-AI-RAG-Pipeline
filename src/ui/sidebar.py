import streamlit as st
import os
import time
from src.utils import clear_shared_data
from src.ingestion import load_documents, split_documents
from src.vector_store import create_vector_db
from src.database import insert_document_log

def render_sidebar(user_role, shared_source_dir, shared_vector_db_dir):
    """
    Yan menüyü çizer.
    Eğer Admin ise: Dosya Yükleme butonlarını gösterir.
    Eğer User ise: Sadece Bilgi mesajı gösterir.
    Her ikisi de: Mevcut yüklü dosyaları görebilir.
    """
    with st.sidebar:
        if os.path.exists("assets/logo.png"):
            st.image("assets/logo.png", use_column_width=True)
        
        st.header(f"👤 Rol: {user_role}")
        
        # ORTAK ALAN: MEVCUT DOSYALARI LİSTELE 
        st.subheader("📚 Mevcut Hafıza")
        
        if os.path.exists(shared_source_dir) and len(os.listdir(shared_source_dir)) > 0:
            files = os.listdir(shared_source_dir)
            with st.expander(f"📂 Yüklü Dosyalar ({len(files)})", expanded=True):
                for f in files:
                    st.caption(f"📄 {f}")
        else:
            st.info("📭 Sistemde henüz yüklü belge yok.")
            
        st.divider()

        # ADMIN MODU: YÜKLEME VE İŞLEME 
        if user_role == "Admin":
            st.subheader("➕ Yeni Belge Ekle")
            st.info("Buradan yüklenen dosyalar tüm şirket tarafından erişilebilir.")
            
            uploaded_files = st.file_uploader(
                "Dosyaları seçin veya sürükleyin",
                accept_multiple_files=True,
                type=["pdf", "docx", "csv", "xlsx"]
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🚀 İşle", use_container_width=True):
                    if uploaded_files:
                        with st.spinner("Kurumsal hafıza güncelleniyor..."):
                            try:
                                # 1. Klasör Kontrolü ve Kayıt
                                if not os.path.exists(shared_source_dir):
                                    os.makedirs(shared_source_dir)
                                    
                                for f in uploaded_files:
                                    path = os.path.join(shared_source_dir, f.name)
                                    with open(path, "wb") as wb:
                                        wb.write(f.getbuffer())
                                
                                # 2. Pipeline Çalıştır 
                                start = time.time()
                                docs = load_documents(shared_source_dir)
                                chunks = split_documents(docs)
                                create_vector_db(chunks, shared_vector_db_dir)
                                duration = round(time.time() - start, 2)
                                
                                # 3. Veritabanı Kaydı (Log)
                                session_id = "SHARED_ADMIN"
                                for f in uploaded_files:
                                    insert_document_log(session_id, f.name, f.type, len(chunks), duration)
                                    
                                st.success(f"✅ Tamamlandı ({duration}s)")
                                time.sleep(1)
                                st.rerun() 
                            except Exception as e:
                                st.error(f"Hata: {e}")
                    else:
                        st.warning("Lütfen dosya seçiniz.")

            with col2:
                if st.button("🗑️ Sıfırla", use_container_width=True):
                    clear_shared_data()
                    st.success("Hafıza silindi!")
                    time.sleep(1)
                    st.rerun()

        else:
            st.info("👋 Çalışan modundasınız.\nYukarıdaki listede görünen belgeler hakkında soru sorabilirsiniz.")
            
        st.divider()
        if st.button("Çıkış Yap"):
            st.session_state.clear()
            st.rerun()