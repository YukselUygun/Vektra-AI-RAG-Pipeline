import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

def render_login():
    # Sayfayı ortalamak için boşluklar
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Kart Görünümü (CSS ile)
        st.markdown("""
        <style>
        .login-card {
            background-color: #1e293b;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
            text-align: center;
            border: 1px solid #334155;
        }
        .login-title {
            color: white;
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 20px;
        }
        </style>
        <div class="login-card">
            <div class="login-title">🔒 Vektra AI Giriş</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("") # Boşluk
        
        role = st.selectbox("Giriş Türü Seçin", ["Seçiniz...", "Admin (Yönetici)", "User (Çalışan)"])
        
        if role == "Admin (Yönetici)":
            password = st.text_input("Yönetici Şifresi", type="password")
            if st.button("Giriş Yap", use_container_width=True):
                valid_pass = os.getenv("ADMIN_PASSWORD", "admin123")
                if password == valid_pass:
                    st.session_state.logged_in = True
                    st.session_state.user_role = "Admin"
                    st.success("Giriş başarılı!")
                    st.rerun()
                else:
                    st.error("Hatalı Şifre!")
                    
        elif role == "User (Çalışan)":
            if st.button("Çalışan Olarak Devam Et", use_container_width=True):
                st.session_state.logged_in = True
                st.session_state.user_role = "User"
                st.rerun()