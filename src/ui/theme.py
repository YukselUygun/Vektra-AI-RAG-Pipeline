import streamlit as st

def load_theme():
    """
    Vektra kurumsal dark temasını yükler.
    Renkler ve görünümler Tailwind tasarımına yakın olacak şekilde ayarlandı.
    """
    custom_css = """
    <style>
    :root {
        --vektra-bg: #101622;
        --vektra-sidebar-bg: #161D2B;
        --vektra-card-bg: #111827;
        --vektra-card-soft: rgba(30, 64, 175, 0.08);
        --vektra-border-subtle: rgba(148, 163, 184, 0.25);
        --vektra-text-main: #e5e7eb;
        --vektra-text-muted: #9da6b9;
        --vektra-primary: #135bec;
    }

    .stApp {
        background-color: var(--vektra-bg);
        color: var(--vektra-text-main);
        font-family: "Inter", system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }

    /* Sidebar genel görünüm */
    section[data-testid="stSidebar"] {
        background-color: var(--vektra-sidebar-bg);
        border-right: 1px solid rgba(30, 64, 175, 0.3);
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label {
        color: var(--vektra-text-main) !important;
    }

    /* Ana başlıklar */
    h1, h2, h3 {
        color: var(--vektra-text-main);
    }

    /* Kart stili (sidebar ve main) */
    .vektra-card {
        background: #020617;
        border-radius: 0.75rem;
        border: 1px solid var(--vektra-border-subtle);
        padding: 1rem 1.1rem;
        margin-bottom: 0.75rem;
    }

    .vektra-card-soft {
        background: rgba(15, 23, 42, 0.75);
        border-radius: 0.75rem;
        border: 1px solid rgba(30, 64, 175, 0.35);
        padding: 1rem 1.1rem;
        margin-bottom: 0.75rem;
    }

    /* Sidebar "Yüklü Dosyalar" listesi için */
    .vektra-file-pill {
        background: rgba(15, 23, 42, 0.9);
        border-radius: 0.6rem;
        border: 1px solid rgba(51, 65, 85, 0.7);
        padding: 0.55rem 0.8rem;
        font-size: 0.85rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 0.5rem;
        margin-bottom: 0.3rem;
    }

    .vektra-file-pill span {
        color: var(--vektra-text-main);
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    /* Chat mesajları */
    [data-testid="stChatMessage"] {
        margin-bottom: 0.5rem;
    }

    [data-testid="stChatMessage"] > div {
        max-width: 720px;
    }

    /* Asistan mesajları */
    [data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatar"]:not(:has(img))) div:nth-child(2) {
        background: rgba(30, 64, 175, 0.12);
        border-radius: 0.9rem;
        padding: 0.8rem 1rem;
        border: 1px solid rgba(148, 163, 184, 0.35);
    }

    /* Kullanıcı mesajı (role="user") */
    [data-testid="stChatMessage"][data-testid*="user"] div:nth-child(2) {
        background: var(--vektra-primary);
        border-radius: 0.9rem;
        padding: 0.8rem 1rem;
        color: white;
    }

    /* Input ve butonlar */
    .stTextInput > div > div > input,
    .stTextArea textarea,
    .stSelectbox > div > div {
        background: rgba(15, 23, 42, 0.9) !important;
        border-radius: 0.7rem !important;
        border: 1px solid rgba(148, 163, 184, 0.45) !important;
        color: var(--vektra-text-main) !important;
    }

    .stTextInput > div > div > input::placeholder,
    .stTextArea textarea::placeholder {
        color: var(--vektra-text-muted) !important;
    }

    .stButton > button {
        background: var(--vektra-primary);
        border-radius: 0.7rem;
        border: 1px solid rgba(37, 99, 235, 0.8);
        padding: 0.5rem 1rem;
        font-weight: 600;
        color: white;
    }

    .stButton > button:hover {
        background: #1d4ed8;
        border-color: #1d4ed8;
    }

    /* Login kartı için yardımcı sınıf */
    .vektra-login-card {
        max-width: 420px;
        margin: 4rem auto 0 auto;
        background: #020617;
        border-radius: 1rem;
        border: 1px solid var(--vektra-border-subtle);
        padding: 2rem 2rem 1.75rem 2rem;
        box-shadow: 0 24px 40px rgba(15, 23, 42, 0.7);
    }

    .vektra-login-title {
        text-align: center;
        margin-bottom: 0.5rem;
        font-size: 1.9rem;
        font-weight: 700;
    }

    .vektra-login-subtitle {
        text-align: center;
        font-size: 0.9rem;
        color: var(--vektra-text-muted);
        margin-bottom: 1.4rem;
    }

    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)
