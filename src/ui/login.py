import streamlit as st

def render_login():
    st.title("🔒 Vektra AI - Giriş")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("Devam etmek için bir rol seçin:")

        role = st.selectbox("Giriş Türü", ["Seçiniz...", "Admin (Yönetici)", "User (Çalışan)"])
        
        if role == "Admin (Yönetici)":
            password = st.text_input("Yönetici Şifresi", type="password")
            if st.button("Giriş Yap"):
                if password == "admin123": # Basit şifre
                    st.session_state.logged_in = True
                    st.session_state.user_role = "Admin"
                    st.rerun()
                else:
                    st.error("Hatalı Şifre!")
                    
        elif role == "User (Çalışan)":
            if st.button("Çalışan Olarak Gir"):
                st.session_state.logged_in = True
                st.session_state.user_role = "User"
                st.rerun()