import streamlit as st

def render_login():
    # Ortadaki kolona formu sıkıştır
    left, center, right = st.columns([1, 2, 1])

    with center:
        # Logo + başlık
        st.image("assets/logo.png", width=100)

        st.markdown(
            "<h1 style='text-align:center; margin-top:0.8rem;'>Vektra</h1>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<p style='text-align:center; color:#9da6b9; margin-bottom:1.5rem;'>Kurumsal Asistan'a hoş geldiniz</p>",
            unsafe_allow_html=True,
        )

        # Rol seçimi
        role = st.selectbox(
            "Rol Seçin",
            ["Admin (Yönetici)", "User (Çalışan)"],
            index=0,
            key="login_role",
        )

        # Sadece admin için şifre
        password = ""
        if role == "Admin (Yönetici)":
            password = st.text_input(
                "Yönetici Şifresi",
                type="password",
                placeholder="Şifrenizi girin",
                key="login_password",
            )

        # Giriş butonu
        login_btn = st.button("Giriş Yap", use_container_width=True)

        # Giriş mantığı
        if login_btn:
            if role == "Admin (Yönetici)":
                if password == "admin123":
                    st.session_state.logged_in = True
                    st.session_state.user_role = "Admin"
                    st.rerun()
                else:
                    st.error("Hatalı şifre. Lütfen tekrar deneyin.")
            else:
                st.session_state.logged_in = True
                st.session_state.user_role = "User"
                st.rerun()
