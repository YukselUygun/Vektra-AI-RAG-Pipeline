-- 1. DOKÜMAN LOG TABLOSU 
CREATE TABLE IF NOT EXISTS document_logs (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(255) NOT NULL,
    filename VARCHAR(255) NOT NULL,
    file_type VARCHAR(50),
    upload_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processing_time_seconds FLOAT,
    chunk_count INT,
    status VARCHAR(50) DEFAULT 'SUCCESS'
);

CREATE INDEX IF NOT EXISTS idx_doc_session_id ON document_logs(session_id);

-- 2. CHAT LOG TABLOSU 
CREATE TABLE IF NOT EXISTS chat_logs (
    log_id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    session_id VARCHAR(255),
    user_role VARCHAR(50),   
    message_role VARCHAR(50), 
    message TEXT
);

CREATE INDEX IF NOT EXISTS idx_chat_session_id ON chat_logs(session_id);
CREATE INDEX IF NOT EXISTS idx_chat_timestamp ON chat_logs(timestamp);