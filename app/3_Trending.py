import streamlit as st
from utils import init_session_state, inject_custom_css, fetch_trending, fetch_movie_details

st.set_page_config(page_title="Trending - CineMatch AI", page_icon="🔥", layout="wide")

init_session_state()
if not st.session_state.get('logged_in'):
    st.switch_page("app.py")
    
inject_custom_css()

st.markdown("<h1>🔥 Trending Movies</h1>", unsafe_allow_html=True)
st.markdown("<p>Discover what the world is watching right now.</p>", unsafe_allow_html=True)

st.markdown("""
<style>
    .trending-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 10px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 20px;
        transition: 0.3s;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .trending-card:hover {
        transform: translateX(10px);
        background: rgba(255, 255, 255, 0.1);
        border-color: #00f5d4;
    }
    .rank-badge {
        font-size: 40px;
        font-weight: bold;
        color: #e0aaff;
        min-width: 60px;
        text-align: center;
        text-shadow: 0 0 10px #c77dff;
    }
    .poster-img {
        width: 100px;
        border-radius: 10px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.5);
    }
    .info {
        flex-grow: 1;
    }
    .info h3 {
        margin: 0 0 5px 0 !important;
        font-size: 24px;
        color: white !important;
    }
    .info p {
        margin: 0;
        font-size: 14px;
        color: #aaa;
        display: -webkit-box;
        -webkit-line-clamp: 3;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

with st.spinner("Fetching latest trending data... 📡"):
    trending_movies = fetch_trending()

if trending_movies:
    for index, movie in enumerate(trending_movies[:10]):
        rank = index + 1
        movie_id = movie.get('id')
        title = movie.get('title', movie.get('name', 'Unknown'))
        poster_path = movie.get('poster_path')
        poster_url = f"https://image.tmdb.org/t/p/w500/{poster_path}" if poster_path else "https://via.placeholder.com/100x150?text=No+Poster"
        overview = movie.get('overview', 'No overview available.')
        rating = round(movie.get('vote_average', 0), 1)
        
        st.markdown(f"""
        <div class="trending-card">
            <div class="rank-badge">#{rank}</div>
            <div>
                <img class="poster-img" src="{poster_url}" alt="Poster">
            </div>
            <div class="info">
                <h3>{title} <span style="font-size:16px; color:#00f5d4;">⭐ {rating}/10</span></h3>
                <p>{overview}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.error("Failed to load trending movies or no data available.")
