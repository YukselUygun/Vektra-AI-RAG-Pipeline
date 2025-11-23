import os
import pandas as pd
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from src.config import Config

def load_documents():
    """
    data/source_docs klasöründeki PDF, DOCX, CSV ve EXCEL dosyalarını okur.
    """
    source_path = "data/source_docs"
    documents = []
    
    print(f"📂 '{source_path}' klasörü taranıyor...")

    for root, dirs, files in os.walk(source_path):
        for file in files:
            file_path = os.path.join(root, file)
            loader = None
            
            try:
                # 1. PDF DOSYALARI
                if file.endswith(".pdf"):
                    print(f"   📄 PDF Okunuyor: {file}")
                    loader = PyPDFLoader(file_path)
                    documents.extend(loader.load())

                # 2. WORD DOSYALARI
                elif file.endswith(".docx"):
                    print(f"   📝 Word Okunuyor: {file}")
                    loader = Docx2txtLoader(file_path)
                    documents.extend(loader.load())

                # 3. CSV DOSYALARI
                elif file.endswith(".csv"):
                    print(f"   📊 CSV Okunuyor: {file}")
                    loader = CSVLoader(file_path, encoding="utf-8")
                    documents.extend(loader.load())

                # 4. EXCEL DOSYALARI (YENİ EKLENDİ!)
                elif file.endswith((".xlsx", ".xls")):
                    print(f"   📗 Excel Okunuyor: {file}")
                    df = pd.read_excel(file_path)
                    text_data = df.to_string(index=False)
                    
                    excel_doc = Document(
                        page_content=text_data,
                        metadata={"source": file_path, "row_count": len(df)}
                    )
                    documents.append(excel_doc)
                    print(f"      ✅ Başarılı: Excel tablosu metne çevrildi.")

                else:
                    continue
                    
            except Exception as e:
                print(f"      ❌ HATA: {file} okunamadı! Sebebi: {e}")
    
    print(f"📚 Toplam {len(documents)} sayfa/parça doküman yüklendi.")
    return documents

def split_documents(documents):
    """
    Okunan dokümanları küçük parçalara (Chunks) böler.
    """
    if not documents:
        print("⚠️  Hiçbir doküman yüklenemedi.")
        return []
        
    print(f"✂️  Dokümanlar parçalanıyor...")
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=Config.CHUNK_SIZE,
        chunk_overlap=Config.CHUNK_OVERLAP
    )
    
    chunks = text_splitter.split_documents(documents)
    
    print(f"🧩 Toplam {len(chunks)} parçaya bölündü.")
    
    if len(chunks) > 0:
        print("-" * 30)
        print(f"👀 Örnek Parça (İlk 200 karakter):\n{chunks[0].page_content[:200]}...")
        print("-" * 30)
        
    return chunks

if __name__ == "__main__":
    docs = load_documents()
    if docs:
        chunks = split_documents(docs)