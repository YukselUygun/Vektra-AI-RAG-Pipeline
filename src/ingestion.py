import os
import logging
import pandas as pd
from typing import List, Optional
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from src.config import Config

# 1. LOGGING AYARLARI
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(log_dir, "ingestion.log"), encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def load_documents(custom_path: str = None) -> List[Document]:
    """
    Belirtilen klasördeki dosyaları okur.
    """
    source_path = custom_path if custom_path else "data/source_docs"
    
    documents = []
    
    if not os.path.exists(source_path):
        logger.error(f"❌ Kaynak klasör bulunamadı: {source_path}")
        return []

    logger.info(f"📂 '{source_path}' klasörü taranıyor...")

    for root, dirs, files in os.walk(source_path):
        for file in files:
            file_path = os.path.join(root, file)
            loader = None
            
            try:
                if file.endswith(".pdf"):
                    logger.info(f"📄 PDF Okunuyor: {file}")
                    loader = PyPDFLoader(file_path)
                    documents.extend(loader.load())

                elif file.endswith(".docx"):
                    logger.info(f"📝 Word Okunuyor: {file}")
                    loader = Docx2txtLoader(file_path)
                    documents.extend(loader.load())

                elif file.endswith(".csv"):
                    logger.info(f"📊 CSV Okunuyor: {file}")
                    loader = CSVLoader(file_path, encoding="utf-8")
                    documents.extend(loader.load())

                elif file.endswith((".xlsx", ".xls")):
                    logger.info(f"📗 Excel Okunuyor: {file}")
                    df = pd.read_excel(file_path)
                    text_data = df.to_string(index=False)
                    excel_doc = Document(
                        page_content=text_data,
                        metadata={"source": file_path, "row_count": len(df)}
                    )
                    documents.append(excel_doc)
                
                else:
                    # Desteklenmeyen dosyaları sessizce geç (Debug modunda gösterilebilir)
                    logger.debug(f"Atlanan dosya formatı: {file}")
                    
            except Exception as e:
                logger.error(f"❌ HATA: {file} okunamadı! Sebebi: {e}")
    
    logger.info(f"📚 Toplam {len(documents)} sayfa/parça doküman başarıyla yüklendi.")
    return documents

def split_documents(documents: List[Document]) -> List[Document]:
    """
    Dokümanları Config ayarına göre parçalar (Chunking).
    """
    if not documents:
        logger.warning("⚠️  Parçalanacak doküman bulunamadı.")
        return []
        
    logger.info(f"✂️  {len(documents)} adet doküman parçalanıyor (Size: {Config.CHUNK_SIZE}, Overlap: {Config.CHUNK_OVERLAP})...")
    
    try:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=Config.CHUNK_SIZE,
            chunk_overlap=Config.CHUNK_OVERLAP
        )
        
        chunks = text_splitter.split_documents(documents)
        
        logger.info(f"🧩 İşlem Tamam: Toplam {len(chunks)} parçaya bölündü.")
        
        if len(chunks) > 0:
            logger.info(f"👀 Örnek Parça Başlangıcı: {chunks[0].page_content[:100]}...")
            
        return chunks
        
    except Exception as e:
        logger.error(f"❌ Parçalama işlemi sırasında hata: {e}")
        return []

if __name__ == "__main__":
    docs = load_documents()
    if docs:
        chunks = split_documents(docs)