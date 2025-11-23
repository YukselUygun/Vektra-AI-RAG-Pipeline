CREATE TABLE IF NOT EXISTS document_logs (
    id SERIAL PRIMARY KEY,              -- Kayıt Numarası 
    session_id VARCHAR(255) NOT NULL,   -- Kim yükledi? 
    filename VARCHAR(255) NOT NULL,     -- Dosyanın adı ne?
    file_type VARCHAR(50),              -- Dosya tipi?
    upload_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Ne zaman yüklendi?
    processing_time_seconds FLOAT,      -- İşlem ne kadar sürdü?
    chunk_count INT,                    -- Kaç parçaya bölündü?
    status VARCHAR(50) DEFAULT 'SUCCESS' -- Durum (Başarılı/Hatalı)
);

CREATE INDEX IF NOT EXISTS idx_session_id ON document_logs(session_id);