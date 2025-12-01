import os
import shutil
import uuid
import streamlit as st

def get_session_id():
    if 'session_id' not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    return st.session_state.session_id

def get_shared_dirs():
    """
    Windows FAISS, Türkçe karakterleri desteklemediği için
    index dizini ASCII karakterli bir klasöre taşındı.
    """

    base_dir = r"C:\vektra_data"

    shared_source_dir = os.path.join(base_dir, "shared_docs")
    shared_vector_db_dir = os.path.join(base_dir, "shared_index")

    os.makedirs(shared_source_dir, exist_ok=True)
    os.makedirs(shared_vector_db_dir, exist_ok=True)

    return shared_source_dir, shared_vector_db_dir

def clear_shared_data():
    """
    SADECE ADMIN ÇAĞIRABİLİR! Tüm şirket hafızasını siler.
    """
    source_dir, db_dir = get_shared_dirs()
    
    if os.path.exists(source_dir):
        shutil.rmtree(source_dir)
        os.makedirs(source_dir)
        
    if os.path.exists(db_dir):
        shutil.rmtree(db_dir)