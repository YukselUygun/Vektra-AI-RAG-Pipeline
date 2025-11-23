import os
import shutil
import uuid
import streamlit as st

def get_session_id():
    """
    Her kullanıcıya (veya tarayıcı sekmesine) özel benzersiz bir kimlik (ID) oluşturur.'
    """
    if 'session_id' not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    return st.session_state.session_id

def get_user_dirs():
    session_id = get_session_id()
    
    # Ana veri klasörü
    base_data_dir = "data"
    
    # Kullanıcıya özel ham veri klasörü
    user_source_dir = os.path.join(base_data_dir, "source_docs", f"user_{session_id}")
    
    # Kullanıcıya özel veritabanı klasörü
    user_vector_db_dir = os.path.join("faiss_index", f"user_{session_id}")
    
    if not os.path.exists(user_source_dir):
        os.makedirs(user_source_dir)
               
    return user_source_dir, user_vector_db_dir

def clear_user_data():
    """
    Kullanıcı çıkış yaparsa veya 'Temizle' derse, sadece ONUN dosyalarını siler.
    """
    source_dir, db_dir = get_user_dirs()
    
    # Kaynak dosyaları sil
    if os.path.exists(source_dir):
        shutil.rmtree(source_dir)
        os.makedirs(source_dir)   
        
    # Vektör DB'yi sil 
    if os.path.exists(db_dir):
        shutil.rmtree(db_dir)