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

CREATE INDEX IF NOT EXISTS idx_session_id ON document_logs(session_id);

-- CHAT LOGS TABLOSU
CREATE TABLE IF NOT EXISTS chat_logs (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(255) NOT NULL,       
    user_role VARCHAR(50),                  
    message_role VARCHAR(50),              
    message TEXT,                          
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_chat_session_id 
ON chat_logs(session_id);
