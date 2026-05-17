import streamlit as st
from utils import init_session_state, inject_custom_css

st.set_page_config(page_title="Favorites - CineMatch", page_icon="❤️", layout="wide")

init_session_state()
if not st.session_state.get('logged_in'):
    st.switch_page("app.py")
    
inject_custom_css()

st.markdown("<h1>❤️ Your Favorites</h1>", unsafe_allow_html=True)
st.markdown("<p>Your personalized cinematic universe.</p>", unsafe_allow_html=True)

favorites = st.session_state.get('favorites', [])

if not favorites:
    st.info("You haven't added any movies to your favorites yet. Go to the Recommendations page to find some!")
else:
    st.markdown("""
    <style>
        .fav-card {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 15px;
            padding: 10px;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: 0.3s;
        }
        .fav-card:hover {
            transform: translateY(-5px);
            border-color: #ff007f;
            box-shadow: 0 5px 15px rgba(255, 0, 127, 0.3);
        }
        .fav-poster {
            width: 100%;
            border-radius: 10px;
        }
    </style>
    """, unsafe_allow_html=True)
    
    cols = st.columns(5)
    for idx, movie in enumerate(favorites):
        col_idx = idx % 5
        with cols[col_idx]:
            st.markdown(f"""
            <div class="fav-card">
                <img class="fav-poster" src="{movie['poster']}" alt="Poster">
                <h4 style="margin-top:10px; color:#f1e4ff; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">{movie['title']}</h4>
            </div>
            <br>
            """, unsafe_allow_html=True)
            
            if st.button("❌ Remove", key=f"remove_{idx}", use_container_width=True):
                st.session_state['favorites'].remove(movie)
                st.rerun()
