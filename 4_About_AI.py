import streamlit as st
from utils import init_session_state, inject_custom_css

st.set_page_config(page_title="About AI - CineMatch", page_icon="ℹ️", layout="wide")

init_session_state()
if not st.session_state.get('logged_in'):
    st.switch_page("app.py")
    
inject_custom_css()

st.markdown("<h1>ℹ️ How CineMatch AI Works</h1>", unsafe_allow_html=True)
st.markdown("<p>Understanding the intelligence behind your movie recommendations.</p>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="glass-card" style="height: 100%;">
        <h2 style="color:#00f5d4 !important;">🧠 The Engine</h2>
        <p>CineMatch AI utilizes a <b>Content-Based Filtering</b> recommender system. It doesn't rely on what other users watch, but rather analyzes the actual content of the movies themselves.</p>
        <p>We process thousands of data points including:</p>
        <ul>
            <li>📝 <b>Genres</b> (Action, Sci-Fi, Romance)</li>
            <li>🔑 <b>Keywords</b> (Space travel, AI, Future)</li>
            <li>👥 <b>Cast & Crew</b> (Actors, Directors)</li>
            <li>📖 <b>Plot Overviews</b> (Storyline descriptions)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="glass-card" style="height: 100%;">
        <h2 style="color:#00f5d4 !important;">📐 The Math (Cosine Similarity)</h2>
        <p>All text data for a movie is combined into a single "tag" and converted into a numerical vector using <code>CountVectorizer</code>.</p>
        <p>To find similar movies, we calculate the <b>Cosine Similarity</b> between these vectors. It measures the cosine of the angle between two multi-dimensional vectors.</p>
        <ul>
            <li><b>Score 1.0 (100%)</b>: Exact match</li>
            <li><b>Score 0.0 (0%)</b>: Completely different</li>
        </ul>
        <p>The lower the angle between two movie vectors, the higher the recommendation confidence!</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<div class="glass-card">
    <h2 style="text-align:center;">🧩 Tech Stack</h2>
    <div style="display: flex; justify-content: space-around; flex-wrap: wrap; margin-top: 20px;">
        <div style="text-align: center;"><img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" width="60"><br><b>Python</b></div>
        <div style="text-align: center;"><img src="https://streamlit.io/images/brand/streamlit-mark-color.svg" width="60"><br><b>Streamlit</b></div>
        <div style="text-align: center;"><img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/pandas/pandas-original.svg" width="60"><br><b>Pandas</b></div>
        <div style="text-align: center;"><img src="https://upload.wikimedia.org/wikipedia/commons/0/05/Scikit_learn_logo_small.svg" width="60"><br><b>Scikit-Learn</b></div>
        <div style="text-align: center;"><img src="https://www.themoviedb.org/assets/2/v4/logos/v2/blue_square_1-5bdc75aaebeb75dc7ae79426ddd9be3b2be1e342510f8202baf6bffa71d7f5c4.svg" width="60"><br><b>TMDB API</b></div>
    </div>
</div>
""", unsafe_allow_html=True)
