import streamlit as st
import pickle
import requests
import os

TMDB_API_KEY = "8304d05e8c910e1c0c44b59c617d008b"

@st.cache_resource
def load_models():
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    movies_path = os.path.join(base_path, "notebooks", "movies.pkl")
    similarity_path = os.path.join(base_path, "notebooks", "similarity.pkl")
    
    with open(movies_path, 'rb') as f:
        movies = pickle.load(f)
    with open(similarity_path, 'rb') as f:
        similarity = pickle.load(f)
    return movies, similarity

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
    try:
        response = requests.get(url)
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    except:
        pass
    return "https://via.placeholder.com/500x750?text=No+Poster"

def fetch_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
    try:
        response = requests.get(url)
        data = response.json()
        return {
            'poster': f"https://image.tmdb.org/t/p/w500/{data.get('poster_path')}" if data.get('poster_path') else "https://via.placeholder.com/500x750?text=No+Poster",
            'rating': data.get('vote_average', 'N/A'),
            'overview': data.get('overview', 'No overview available.'),
            'genres': [g['name'] for g in data.get('genres', [])]
        }
    except:
        return {'poster': "https://via.placeholder.com/500x750?text=Error", 'rating': 'N/A', 'overview': '', 'genres': []}

def fetch_trending():
    url = f"https://api.themoviedb.org/3/trending/movie/day?api_key={TMDB_API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()
        return data.get('results', [])
    except:
        return []

def init_session_state():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    if 'favorites' not in st.session_state:
        st.session_state['favorites'] = []
    if 'username' not in st.session_state:
        st.session_state['username'] = ""

def inject_custom_css():
    st.markdown("""
    <style>
    /* Global Styles & Background */
    .stApp {
        background: #0a0015; /* deep black-purple */
        background-image: 
            radial-gradient(circle at 15% 50%, rgba(106, 13, 173, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 85% 30%, rgba(0, 212, 255, 0.15) 0%, transparent 50%);
        color: white;
        font-family: 'Inter', sans-serif;
        background-attachment: fixed;
    }
    
    /* Transparent Header for Premium Look but keep Navigation Menu */
    header[data-testid="stHeader"] {
        background-color: transparent !important;
        pointer-events: none; /* Let clicks pass through the transparent header... */
    }
    
    [data-testid="collapsedControl"] {
        pointer-events: auto !important; /* ...but keep the hamburger menu clickable! */
        z-index: 999999 !important;
    }
    
    [data-testid="stToolbar"] {
        display: none !important; /* Hides the Deploy and generic Streamlit buttons */
    }
    footer {
        display: none !important;
    }
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
        max-width: 95% !important;
    }
    
    /* Custom Cursor Glow */
    body {
        cursor: url('https://cdn-icons-png.flaticon.com/32/73/73256.png'), auto;
    }

    /* Typography */
    h1, h2, h3 {
        color: #ff4ecd !important; /* pink neon */
        text-shadow: 0 0 15px #ff4ecd, 0 0 30px #6a0dad;
    }
    
    p {
        color: #e0f7fa;
    }

    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(0, 212, 255, 0.2);
        border-radius: 20px;
        padding: 25px;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 8px 32px 0 rgba(106, 13, 173, 0.37);
    }
    
    .glass-card:hover {
        transform: translateY(-10px) rotateX(5deg) rotateY(-5deg);
        box-shadow: 0 15px 35px rgba(0, 212, 255, 0.4);
        border: 1px solid #00d4ff;
    }
    
    /* Input Search Bar with Glowing Border */
    .stSelectbox > div > div, .stTextInput > div > div {
        background-color: rgba(10, 0, 21, 0.6) !important;
        border: 2px solid #6a0dad !important;
        border-radius: 12px !important;
        color: white !important;
    }
    .stSelectbox > div > div:focus-within, .stTextInput > div > div:focus-within {
        border-color: #00d4ff !important;
        box-shadow: 0 0 20px #00d4ff !important;
    }
    
    /* Neon Glowing Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(10, 0, 21, 0.95), rgba(106, 13, 173, 0.8)) !important;
        border-right: 2px solid #ff4ecd;
        box-shadow: 5px 0 20px rgba(255, 78, 205, 0.4);
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #6a0dad, #ff4ecd);
        border: none;
        border-radius: 30px;
        color: white;
        font-weight: bold;
        padding: 12px 28px;
        transition: 0.4s;
        box-shadow: 0 0 15px rgba(106, 13, 173, 0.6);
    }
    
    .stButton > button:hover {
        background: linear-gradient(90deg, #ff4ecd, #00d4ff);
        box-shadow: 0 0 25px #00d4ff;
        transform: scale(1.08);
        color: white !important;
    }

    /* Floating Particles - CSS only approach */
    .particles-bg {
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        z-index: 0;
        overflow: hidden;
        pointer-events: none;
    }
    
    .particle {
        position: absolute;
        width: 3px;
        height: 3px;
        background: #00d4ff;
        border-radius: 50%;
        box-shadow: 0 0 15px #00d4ff, 0 0 30px #00d4ff;
        animation: floatUp infinite linear;
        opacity: 0.6;
    }
    
    @keyframes floatUp {
        0% { transform: translateY(100vh) scale(0); opacity: 0; }
        50% { opacity: 1; }
        100% { transform: translateY(-10vh) scale(1.5); opacity: 0; }
    }
    
    /* Starfield */
    .star {
        position: absolute;
        background: white;
        border-radius: 50%;
        animation: twinkle infinite ease-in-out;
    }
    @keyframes twinkle {
        0%, 100% { opacity: 0.2; transform: scale(0.8); }
        50% { opacity: 1; transform: scale(1.2); box-shadow: 0 0 10px white; }
    }
    </style>
    
<!-- Floating Particles & Stars HTML -->
<div class="particles-bg">
<!-- Stars (Twinkling) -->
<div class="star" style="width:2px; height:2px; left:10%; top:20%; animation-duration:3s;"></div>
<div class="star" style="width:3px; height:3px; left:80%; top:15%; animation-duration:4s; animation-delay:1s;"></div>
<div class="star" style="width:2.5px; height:2.5px; left:45%; top:70%; animation-duration:2.5s; animation-delay:2s;"></div>
<div class="star" style="width:1px; height:1px; left:60%; top:10%; animation-duration:5s;"></div>
<div class="star" style="width:2px; height:2px; left:25%; top:80%; animation-duration:3.5s; animation-delay:0.5s;"></div>
<div class="star" style="width:3px; height:3px; left:90%; top:60%; animation-duration:2s; animation-delay:1.5s;"></div>
<div class="star" style="width:1.5px; height:1.5px; left:5%; top:40%; animation-duration:4.5s;"></div>
<div class="star" style="width:2px; height:2px; left:70%; top:85%; animation-duration:3s; animation-delay:2.5s;"></div>
<div class="star" style="width:2.5px; height:2.5px; left:35%; top:30%; animation-duration:2s; animation-delay:0.8s;"></div>
<div class="star" style="width:1px; height:1px; left:50%; top:50%; animation-duration:6s;"></div>

<!-- Floating Particles (Cyan and Pink) -->
<div class="particle" style="left:5%; animation-duration:14s;"></div>
<div class="particle" style="left:15%; animation-duration:18s; animation-delay:3s; background:#ff4ecd; box-shadow: 0 0 15px #ff4ecd;"></div>
<div class="particle" style="left:25%; animation-duration:12s; animation-delay:7s;"></div>
<div class="particle" style="left:35%; animation-duration:20s; animation-delay:1s; background:#ff4ecd; box-shadow: 0 0 15px #ff4ecd;"></div>
<div class="particle" style="left:45%; animation-duration:15s; animation-delay:5s;"></div>
<div class="particle" style="left:55%; animation-duration:19s; animation-delay:2s;"></div>
<div class="particle" style="left:65%; animation-duration:13s; animation-delay:8s; background:#ff4ecd; box-shadow: 0 0 15px #ff4ecd;"></div>
<div class="particle" style="left:75%; animation-duration:17s; animation-delay:4s;"></div>
<div class="particle" style="left:85%; animation-duration:16s; animation-delay:1.5s; background:#ff4ecd; box-shadow: 0 0 15px #ff4ecd;"></div>
<div class="particle" style="left:95%; animation-duration:14s; animation-delay:6s;"></div>
<div class="particle" style="left:10%; animation-duration:22s; animation-delay:4s;"></div>
<div class="particle" style="left:40%; animation-duration:16s; animation-delay:9s; background:#ff4ecd; box-shadow: 0 0 15px #ff4ecd;"></div>
<div class="particle" style="left:80%; animation-duration:19s; animation-delay:11s;"></div>
</div>
    """, unsafe_allow_html=True)
