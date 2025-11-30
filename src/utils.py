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
    TÜM ŞİRKETİN ORTAK KULLANDIĞI KLASÖRLER.
    Yolları 'Absolute Path' (Tam Yol) olarak verir, böylece Docker/Airflow şaşırmaz.
    """

    current_file_path = os.path.abspath(__file__) 
    
    src_dir = os.path.dirname(current_file_path)
    
    project_root = os.path.dirname(src_dir)
    
    shared_source_dir = os.path.join(project_root, "data", "shared_docs")
    
    shared_vector_db_dir = os.path.join(project_root, "faiss_index", "shared_index")
    
    if not os.path.exists(shared_source_dir):
        os.makedirs(shared_source_dir)
        
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