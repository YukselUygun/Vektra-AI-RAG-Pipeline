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
                            
                                if not os.path.exists(shared_source_dir):
                                    os.makedirs(shared_source_dir)
                                    
                                saved_paths = []
                                for f in uploaded_files:
                                    path = os.path.join(shared_source_dir, f.name)
                                    with open(path, "wb") as wb:
                                        wb.write(f.getbuffer())
                                    saved_paths.append(path)
                                
                                start = time.time()
                                docs = load_documents(shared_source_dir)
                                chunks = split_documents(docs)
                                create_vector_db(chunks, shared_vector_db_dir)
                                duration = round(time.time() - start, 2)

                                chunk_counts = {}
                                for ch in chunks:
                                    src = ch.metadata.get("source")
                                    if src:
                                        chunk_counts[src] = chunk_counts.get(src, 0) + 1
                                
                                session_id = "SHARED_ADMIN"
                                for f, path in zip(uploaded_files, saved_paths):
                                    file_chunk_count = chunk_counts.get(path, 0)
                                    insert_document_log(
                                        session_id=session_id,
                                        filename=f.name,
                                        file_type=f.type,
                                        chunk_count=file_chunk_count,
                                        processing_time=duration
                                    )
                                    
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

        st.divider()
        if st.button("Çıkış Yap"):
            st.session_state.clear()
            st.rerun()