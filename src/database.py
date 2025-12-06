import os
import logging
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
load_dotenv()

def get_db_engine():
    try:
        user = os.getenv("POSTGRES_USER", "postgres") 
        password = os.getenv("POSTGRES_PASSWORD", "mysecretpassword")
        host = "127.0.0.1" 
        port = "5433"     
        dbname = "vektra_dwh"

        url = f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
        engine = create_engine(url)
        return engine
    except Exception as e:
        logger.error(f"❌ DB Hatası: {e}")
        return None

#  DOCUMENT LOG FUNCTIONS
def insert_document_log(session_id, filename, file_type, chunk_count, processing_time):
    """
    document_logs tablosuna yüklenen dosya bilgisi ekler.
    """
    engine = get_db_engine()
    if not engine:
        return

    query = text("""
        INSERT INTO document_logs 
        (session_id, filename, file_type, chunk_count, processing_time_seconds)
        VALUES (:session_id, :filename, :file_type, :chunk_count, :processing_time)
    """)

    try:
        with engine.begin() as conn:
            conn.execute(query, {
                "session_id": session_id,
                "filename": filename,
                "file_type": file_type,
                "chunk_count": chunk_count,
                "processing_time": processing_time
            })
        logger.info(f"📝 document_logs kaydedildi → {filename}")

    except Exception as e:
        logger.error(f"❌ document_logs hata: {e}")


def get_all_logs():
    """
    Tüm document_logs içeriğini döndürür.
    Dashboard için kullanılır.
    """
    engine = get_db_engine()
    if not engine:
        return pd.DataFrame()

    try:
        query = "SELECT * FROM document_logs ORDER BY upload_timestamp DESC"
        with engine.connect() as conn:
            df = pd.read_sql(query, conn)
        return df

    except Exception as e:
        logger.error(f"❌ get_all_logs hata: {e}")
        return pd.DataFrame()

#  CHAT LOG FUNCTIONS
def insert_chat_log(session_id: str, user_role: str, message_role: str, message: str):
    """
    Chat geçmişini chat_logs tablosuna ekler.
    """
    engine = get_db_engine()
    if not engine:
        return

    query = text("""
        INSERT INTO chat_logs (session_id, user_role, message_role, message)
        VALUES (:session_id, :user_role, :message_role, :message)
    """)

    try:
        with engine.begin() as conn:
            conn.execute(query, {
                "session_id": session_id,
                "user_role": user_role,
                "message_role": message_role,
                "message": message
            })

        logger.info(f"💬 Chat log kaydedildi ({user_role}/{message_role})")

    except Exception as e:
        logger.error(f"❌ Chat log hata: {e}")

#  CHAT ANALYTICS 
def get_chat_logs(limit: int = 200):
    """
    Son mesajları döndürür (DESC).
    dashboard → tablo kısmı için.
    """
    engine = get_db_engine()
    if not engine:
        return pd.DataFrame()

    try:
        query = text("""
            SELECT 
                log_id,
                timestamp,
                session_id,
                user_role,
                message_role,
                message
            FROM chat_logs
            ORDER BY timestamp DESC
            LIMIT :limit
        """)

        with engine.connect() as conn:
            df = pd.read_sql(query, conn, params={"limit": limit})
        return df

    except Exception as e:
        logger.error(f"❌ get_chat_logs hata: {e}")
        return pd.DataFrame()


def get_chat_stats():
    """
    Dashboard için tüm özet metrikleri döndürür.
    Veri yoksa boş döner → grafikler çökmez.
    """
    engine = get_db_engine()
    if not engine:
        return {
            "total": 0,
            "today": 0,
            "role_dist": pd.DataFrame(),
            "hourly": pd.DataFrame()
        }

    try:
        with engine.connect() as conn:

            # Toplam mesaj
            total = pd.read_sql(
                text("SELECT COUNT(*) AS cnt FROM chat_logs"),
                conn
            )["cnt"][0]

            # Bugünkü mesaj
            today = pd.read_sql(
                text("""
                    SELECT COUNT(*) AS cnt 
                    FROM chat_logs
                    WHERE DATE(timestamp) = CURRENT_DATE
                """),
                conn
            )["cnt"][0]

            # Rol bazında dağılım
            role_dist = pd.read_sql(
                text("""
                    SELECT user_role, COUNT(*) AS cnt
                    FROM chat_logs
                    GROUP BY user_role
                """),
                conn
            )

            # Saatlik mesaj dağılımı (son 24 saat)
            hourly = pd.read_sql(
                text("""
                    SELECT 
                        TO_CHAR(timestamp, 'HH24') AS hour,
                        COUNT(*) AS cnt
                    FROM chat_logs
                    WHERE timestamp >= NOW() - INTERVAL '24 hours'
                    GROUP BY hour
                    ORDER BY hour
                """),
                conn
            )

        return {
            "total": total,
            "today": today,
            "role_dist": role_dist,
            "hourly": hourly
        }

    except Exception as e:
        logger.error(f"❌ get_chat_stats hata: {e}")
        return {
            "total": 0,
            "today": 0,
            "role_dist": pd.DataFrame(),
            "hourly": pd.DataFrame()
        }
