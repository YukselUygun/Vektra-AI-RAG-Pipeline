import streamlit as st
from src.database import get_all_logs

def render_dashboard():
    st.header("📊 Yönetim Paneli")
    df = get_all_logs()
    
    if not df.empty:
        c1, c2, c3 = st.columns(3)
        c1.metric("Dosyalar", len(df))
        c2.metric("Chunklar", int(df['chunk_count'].sum()))
        c3.metric("Ort. Süre", f"{df['processing_time_seconds'].mean():.2f}s")
        
        st.divider()
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("İşlem Süreleri")
            st.bar_chart(df, x="filename", y="processing_time_seconds")
        with col2:
            st.subheader("Chunk Dağılımı")
            st.line_chart(df, x="filename", y="chunk_count")
            
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Henüz veri yok.")