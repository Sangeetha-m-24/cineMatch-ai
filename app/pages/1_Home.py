import streamlit as st
from utils import init_session_state, inject_custom_css, fetch_trending
import random

st.set_page_config(page_title="Home - CineMatch AI", page_icon="🏠", layout="wide")

init_session_state()
if not st.session_state.get('logged_in'):
    st.switch_page("app.py")
    
inject_custom_css()

# Sidebar Music Toggle
with st.sidebar:
    st.markdown("## 🎵 Cinematic Mode")
    music_on = st.toggle("Background Music")
    if music_on:
        st.markdown("""
            <audio autoplay loop controls style="width:100%; border-radius: 10px;">
                <source src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3" type="audio/mpeg">
                Your browser does not support the audio element.
            </audio>
        """, unsafe_allow_html=True)
    
    if st.button("Logout"):
        st.session_state['logged_in'] = False
        st.switch_page("app.py")

# Fetch trending for carousel
trending = fetch_trending()
poster_html = ""
if trending:
    posters = [f"https://image.tmdb.org/t/p/w500/{m.get('poster_path')}" for m in trending[:15] if m.get('poster_path')]
    for p in posters:
        poster_html += f"<img src='{p}' class='carousel-img'>"
    # Duplicate for infinite loop
    for p in posters:
        poster_html += f"<img src='{p}' class='carousel-img'>"

# Quotes
quotes = [
    '"May the Force be with you." - Star Wars',
    '"I am Iron Man." - Avengers',
    '"I will be back." - Terminator',
    '"To infinity and beyond!" - Toy Story',
    '"Why so serious?" - The Dark Knight'
]

# Huge CSS block for advanced animations
st.markdown(f"""
<style>
    /* Floating Quotes */
    .floating-quote {{
        position: fixed;
        color: rgba(255, 255, 255, 0.15);
        font-size: 24px;
        font-style: italic;
        z-index: -1;
        animation: floatQuote 20s infinite ease-in-out;
        white-space: nowrap;
    }}
    @keyframes floatQuote {{
        0% {{ transform: translate(-100%, 80vh); opacity: 0; }}
        20% {{ opacity: 1; }}
        80% {{ opacity: 1; }}
        100% {{ transform: translate(100vw, 20vh); opacity: 0; }}
    }}

    /* Hero Container */
    .hero-container {{
        position: relative;
        text-align: center;
        padding: 120px 20px;
        border-radius: 20px;
        overflow: hidden;
        margin-bottom: 40px;
        border: 1px solid rgba(0, 212, 255, 0.2);
        box-shadow: 0 10px 40px rgba(106, 13, 173, 0.5);
        background: rgba(10, 0, 21, 0.6);
    }}
    
    .hero-bg {{
        position: absolute;
        top: -50px; left: -50px; right: -50px; bottom: -50px;
        background: url('https://images.unsplash.com/photo-1489599849927-2ee91cede3ba') no-repeat center center/cover;
        filter: brightness(0.2) blur(5px);
        z-index: -1;
        animation: parallaxMove 30s infinite alternate ease-in-out;
    }}
    
    @keyframes parallaxMove {{
        0% {{ transform: scale(1) translate(0, 0); }}
        100% {{ transform: scale(1.1) translate(-20px, -20px); }}
    }}
    
    .typewriter h1 {{
        overflow: hidden; 
        white-space: nowrap; 
        margin: 0 auto; 
        letter-spacing: .1em;
        animation: typing 3s steps(30, end), blink-caret .75s step-end infinite;
        font-size: 70px;
        color: #ff4ecd;
        text-shadow: 0 0 20px #ff4ecd, 0 0 40px #6a0dad;
    }}
    
    .fade-up {{
        animation: fadeUp 2s ease-out forwards;
        animation-delay: 3s;
        opacity: 0;
        font-size: 24px;
        color: #00d4ff;
    }}
    
    @keyframes typing {{ from {{ width: 0 }} to {{ width: 100% }} }}
    @keyframes blink-caret {{ from, to {{ border-color: transparent }} 50% {{ border-color: #00d4ff; }} }}
    @keyframes fadeUp {{
        from {{ opacity: 0; transform: translateY(30px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    /* Pulse CTA Button */
    .pulse-btn {{
        background: linear-gradient(90deg, #ff4ecd, #6a0dad);
        color: white;
        padding: 15px 40px;
        font-size: 20px;
        font-weight: bold;
        border-radius: 50px;
        border: none;
        cursor: pointer;
        text-decoration: none;
        display: inline-block;
        margin-top: 30px;
        animation: pulseGlow 2s infinite;
        transition: 0.3s;
    }}
    
    .pulse-btn:hover {{
        transform: scale(1.1);
        background: linear-gradient(90deg, #00d4ff, #ff4ecd);
    }}
    
    @keyframes pulseGlow {{
        0% {{ box-shadow: 0 0 10px #ff4ecd; }}
        50% {{ box-shadow: 0 0 30px #ff4ecd, 0 0 50px #6a0dad; }}
        100% {{ box-shadow: 0 0 10px #ff4ecd; }}
    }}

    /* Infinite Carousel */
    .carousel-container {{
        width: 100%;
        overflow: hidden;
        white-space: nowrap;
        position: relative;
        padding: 20px 0;
        background: rgba(0,0,0,0.3);
        border-top: 1px solid rgba(0, 212, 255, 0.2);
        border-bottom: 1px solid rgba(0, 212, 255, 0.2);
        margin: 40px 0;
    }}
    .carousel-track {{
        display: inline-block;
        animation: scroll 40s linear infinite;
    }}
    .carousel-container:hover .carousel-track {{
        animation-play-state: paused;
    }}
    @keyframes scroll {{
        0% {{ transform: translateX(0); }}
        100% {{ transform: translateX(-50%); }}
    }}
    .carousel-img {{
        width: 200px;
        height: 300px;
        object-fit: cover;
        border-radius: 10px;
        margin: 0 10px;
        display: inline-block;
        transition: 0.4s;
        box-shadow: 0 5px 15px rgba(0,0,0,0.5);
        border: 2px solid transparent;
    }}
    .carousel-img:hover {{
        transform: scale(1.15) translateY(-10px);
        border: 2px solid #00d4ff;
        box-shadow: 0 15px 30px rgba(0, 212, 255, 0.5);
        z-index: 10;
        position: relative;
    }}

    /* 3D Glass Cards */
    .explore-card {{
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 78, 205, 0.3);
        border-radius: 20px;
        padding: 30px 20px;
        text-align: center;
        height: 100%;
        transition: transform 0.5s, box-shadow 0.5s, border 0.5s;
        transform-style: preserve-3d;
        perspective: 1000px;
    }}
    .explore-card:hover {{
        transform: rotateX(10deg) rotateY(-10deg) translateZ(20px);
        box-shadow: -10px 10px 30px rgba(106, 13, 173, 0.6);
        border: 1px solid #00d4ff;
    }}
    .explore-card h2 {{
        font-size: 30px;
        margin-bottom: 10px;
        animation: bounce 2s infinite ease-in-out;
    }}
    @keyframes bounce {{
        0%, 100% {{ transform: translateY(0); }}
        50% {{ transform: translateY(-5px); }}
    }}

    /* Mood Bubble */
    .mood-bubble {{
        background: linear-gradient(135deg, rgba(255, 78, 205, 0.2), rgba(106, 13, 173, 0.2));
        border: 1px solid #ff4ecd;
        border-radius: 50px;
        padding: 10px 30px;
        display: inline-block;
        margin-top: 20px;
        animation: floatBubble 4s infinite ease-in-out;
    }}
    @keyframes floatBubble {{
        0%, 100% {{ transform: translateY(0); }}
        50% {{ transform: translateY(-10px); }}
    }}
</style>

<!-- Background Floating Quote -->
<div class="floating-quote" style="top: 30%; animation-delay: 0s;">{random.choice(quotes)}</div>
<div class="floating-quote" style="top: 70%; animation-delay: 10s;">{random.choice(quotes)}</div>

<div class="hero-container"><div class="hero-bg"></div><div class="typewriter"><h1>🎬 CineMatch AI</h1></div><div class="fade-up">Your AI-powered Movie Universe</div><div class="mood-bubble"><span style="color:#e0f7fa;">Today's Mood Match 🎭: <b>{random.choice(["Epic Sci-Fi", "Dark Thriller", "Cyberpunk", "Neon Action"])}</b></span></div><br></div>
""", unsafe_allow_html=True)


col_a, col_b, col_c = st.columns([1, 1, 1])
with col_b:
    if st.button("Explore Movies 🚀", use_container_width=True, type="primary"):
        st.switch_page("pages/2_Recommendations.py")

# Featured Carousel
if poster_html:
    st.markdown("<h2>🔥 Trending Now</h2>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="carousel-container"><div class="carousel-track">{poster_html}</div></div>
    """, unsafe_allow_html=True)

# Explore Section
st.markdown("<h2 style='text-align:center;'>🌌 Explore The Universe</h2><br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class="explore-card"><h2>🤖</h2><h3 style="color:#00d4ff !important;">AI Recommendations</h3><p>State-of-the-art NLP engine matches your exact cinematic taste.</p></div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="explore-card"><h2>🔥</h2><h3 style="color:#ff4ecd !important;">Trending Movies</h3><p>Live global data pulling the hottest releases directly from TMDB.</p></div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class="explore-card"><h2>❤️</h2><h3 style="color:#00d4ff !important;">Your Favorites</h3><p>Save and build your personalized movie collection in the cloud.</p></div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)
col_bottom1, col_bottom2, col_bottom3 = st.columns([1, 2, 1])
with col_bottom2:
    if st.button("Start Your AI Movie Journey 🍿", use_container_width=True, type="primary"):
        st.switch_page("pages/2_Recommendations.py")
