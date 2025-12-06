import streamlit as st
import pandas as pd
import altair as alt
from src.database import get_all_logs, get_chat_stats, get_chat_logs

def render_dashboard():
    st.header("📊 Yönetim Paneli")
    
    doc_logs = get_all_logs()
    chat_stats = get_chat_stats()
    recent_chats = get_chat_logs(limit=50) # Son 50 mesaj
    
    st.subheader("📈 Genel Bakış")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Toplam Doküman", len(doc_logs) if not doc_logs.empty else 0)
    with col2:
        total_chunks = int(doc_logs['chunk_count'].sum()) if not doc_logs.empty else 0
        st.metric("Toplam Chunk", total_chunks)
    with col3:
        st.metric("Toplam Soru", chat_stats.get("total", 0))
    with col4:
        st.metric("Bugünkü Sorular", chat_stats.get("today", 0))
        
    st.markdown("---")

    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("🧩 Doküman Analizi")
        if not doc_logs.empty:
            chart = alt.Chart(doc_logs).mark_bar().encode(
                x=alt.X('filename', sort=None, title='Dosya Adı'),
                y=alt.Y('processing_time_seconds', title='İşlem Süresi (sn)'),
                color='file_type',
                tooltip=['filename', 'processing_time_seconds', 'chunk_count']
            ).properties(height=300)
            st.altair_chart(chart, use_container_width=True)
        else:
            st.info("Henüz doküman verisi yok.")

    with col_right:
        st.subheader("💬 Sohbet Analizi")
        hourly_data = chat_stats.get("hourly", pd.DataFrame())
        if not hourly_data.empty:
            chart_chat = alt.Chart(hourly_data).mark_line(point=True).encode(
                x=alt.X('hour', title='Saat'),
                y=alt.Y('cnt', title='Mesaj Sayısı'),
                tooltip=['hour', 'cnt']
            ).properties(height=300)
            st.altair_chart(chart_chat, use_container_width=True)
        else:
            st.info("Henüz sohbet verisi yok.")

    st.markdown("---")

    tab_docs, tab_chats = st.tabs(["📄 Doküman Kayıtları", "💬 Sohbet Geçmişi"])
    
    with tab_docs:
        if not doc_logs.empty:
            st.dataframe(
                doc_logs[['filename', 'file_type', 'upload_timestamp', 'processing_time_seconds', 'status']],
                use_container_width=True
            )
        else:
            st.info("Kayıt yok.")
            
    with tab_chats:
        if not recent_chats.empty:
            st.dataframe(
                recent_chats[['timestamp', 'user_role', 'message_role', 'message']],
                use_container_width=True
            )
        else:
            st.info("Sohbet geçmişi yok.")