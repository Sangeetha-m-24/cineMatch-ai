import streamlit as st
from utils import init_session_state, inject_custom_css
import time

# Must be the first Streamlit command
st.set_page_config(
    page_title="CineMatch AI - Login",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

init_session_state()
inject_custom_css()

# Sidebar is collapsed by default via set_page_config, 
# so we don't need to forcefully hide the CSS (which causes it to disappear on other pages).
# Massive custom CSS injection specifically for the Login Page to make it a "Super App"



st.markdown("""
<style>
    /* Full-screen cinematic background */
    .stApp {
        background: url('https://images.unsplash.com/photo-1536440136628-849c177e76a1?q=80&w=2025&auto=format&fit=crop') no-repeat center center fixed !important;
        background-size: cover !important;
    }
    
    /* Dark gradient overlay to make text readable */
    .stApp::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: linear-gradient(135deg, rgba(10, 0, 21, 0.9) 0%, rgba(106, 13, 173, 0.6) 100%);
        z-index: 0;
    }
    
    /* Ensure Streamlit content sits above the overlay */
    .block-container {
        z-index: 1;
        position: relative;
    }
    
    /* The Login Card */
    .login-wrapper {
        background: rgba(10, 0, 21, 0.6);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(0, 212, 255, 0.3);
        border-radius: 20px;
        padding: 50px 40px;
        box-shadow: 0 15px 50px rgba(0, 0, 0, 0.8), 0 0 20px rgba(106, 13, 173, 0.5);
        margin-top: 5vh;
        text-align: center;
        animation: glowPulse 4s infinite alternate;
    }
    
    @keyframes glowPulse {
        0% { box-shadow: 0 15px 50px rgba(0, 0, 0, 0.8), 0 0 20px rgba(106, 13, 173, 0.5); }
        100% { box-shadow: 0 15px 50px rgba(0, 0, 0, 0.8), 0 0 40px rgba(255, 78, 205, 0.6); }
    }
    
    /* Title Styling */
    .login-title {
        font-size: 60px;
        font-weight: 900;
        color: white;
        margin-bottom: 5px;
        text-shadow: 0 0 15px #ff4ecd, 0 0 30px #6a0dad;
        letter-spacing: 2px;
    }
    
    .login-subtitle {
        font-size: 18px;
        color: #00d4ff;
        margin-bottom: 40px;
        letter-spacing: 1px;
    }
</style>
""", unsafe_allow_html=True)

# Main Login UI
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("""
    <div class="login-wrapper">
        <div class="login-title">🎬 CineMatch AI</div>
        <div class="login-subtitle">ENTER THE UNIVERSE</div>
    </div>
    """, unsafe_allow_html=True)
    
    # We place the inputs right below the custom HTML header but still inside the column.
    # To make it look like it's inside the card, we style the inputs globally via utils.py.
    st.markdown("<br>", unsafe_allow_html=True)
    
    username = st.text_input("Username", placeholder="e.g. cinephile99")
    password = st.text_input("Password", type="password", placeholder="••••••••")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("Unlock Cinematic Experience 🚀", use_container_width=True, type="primary"):
        if username:
            st.session_state['username'] = username
            with st.spinner("Connecting to neural network... 🧠"):
                time.sleep(1.5)
            st.session_state['logged_in'] = True
            st.success(f"Access Granted, {username}! Welcome.")
            time.sleep(1)
            st.switch_page("pages/1_Home.py")
        else:
            st.error("Authentication failed: Username required.")
