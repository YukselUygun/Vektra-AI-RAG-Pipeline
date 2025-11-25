import os
import logging
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

load_dotenv()

def get_db_engine():
    """
    Veritabanı bağlantı motorunu oluşturur.
    Hem Localhost'ta hem Docker'da çalışacak şekilde dinamik ayarlanmıştır.
    """
    try:
        user = os.getenv("DB_USER", "postgres")
        password = os.getenv("DB_PASSWORD", "mysecretpassword")
        host = os.getenv("DB_HOST", "localhost")
        port = os.getenv("DB_PORT", "5433") 
        dbname = os.getenv("DB_NAME", "vektra_dwh")
        
        url = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
        
        engine = create_engine(url)
        return engine
    except Exception as e:
        logger.error(f"❌ Veritabanı motoru oluşturulamadı: {e}")
        return None

def insert_document_log(session_id, filename, file_type, chunk_count, processing_time):
    """
    Yüklenen dosyanın bilgilerini 'document_logs' tablosuna yazar.
    """
    engine = get_db_engine()
    if not engine:
        return

    insert_query = text("""
        INSERT INTO document_logs (session_id, filename, file_type, chunk_count, processing_time_seconds)
        VALUES (:session_id, :filename, :file_type, :chunk_count, :processing_time)
    """)
    
    try:
        with engine.begin() as conn:
            conn.execute(insert_query, {
                "session_id": session_id,
                "filename": filename,
                "file_type": file_type,
                "chunk_count": chunk_count,
                "processing_time": processing_time
            })
        logger.info(f"📝 Veritabanına kaydedildi: {filename}")
    except Exception as e:
        logger.error(f"❌ Kayıt sırasında hata oluştu: {e}")

def get_all_logs():
    """
    Dashboard için tüm kayıtları çeker ve Pandas DataFrame olarak döndürür.
    """
    engine = get_db_engine()
    if not engine:
        return pd.DataFrame() 

    try:
        query = "SELECT * FROM document_logs ORDER BY upload_timestamp DESC"
        df = pd.read_sql(query, engine)
        return df
    except Exception as e:
        logger.error(f"❌ Veri çekilirken hata: {e}")
        return pd.DataFrame()