import streamlit as st
import random
import time
from utils import init_session_state, inject_custom_css, load_models, fetch_movie_details

st.set_page_config(page_title="AI Recommendations", page_icon="🤖", layout="wide")

init_session_state()
if not st.session_state.get('logged_in'):
    st.switch_page("app.py")
    
inject_custom_css()

# Load models
try:
    movies_df, similarity_matrix = load_models()
except Exception as e:
    st.error(f"Error loading models: {e}. Please check the models directory.")
    st.stop()

st.markdown("<h1>🤖 AI Recommender</h1>", unsafe_allow_html=True)
st.markdown("<p>Find your next cinematic masterpiece based on your favorites.</p>", unsafe_allow_html=True)

# Main container for Search
with st.container():
    
    col1, col2 = st.columns([4, 1])
    with col1:
        movie_list = movies_df['title'].values
        # Add a key so we can update it programmatically
        if 'movie_select' not in st.session_state:
            default_index = list(movie_list).index("Avatar") if "Avatar" in movie_list else 0
            st.session_state['movie_select'] = movie_list[default_index]
            
        selected_movie = st.selectbox(
            "Type or select a movie you like:",
            movie_list,
            key="movie_select"
        )
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Surprise Me 🎲", use_container_width=True):
            st.session_state['movie_select'] = random.choice(movie_list)
            st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

def recommend(movie):
    try:
        movie_index = movies_df[movies_df['title'] == movie].index[0]
        distances = similarity_matrix[movie_index]
        # Get top 5 recommendations
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
        
        recommended_movies = []
        for i in movies_list:
            movie_id = movies_df.iloc[i[0]].movie_id
            title = movies_df.iloc[i[0]].title
            confidence = round(i[1] * 100, 1)
            details = fetch_movie_details(movie_id)
            details['title'] = title
            details['confidence'] = confidence
            recommended_movies.append(details)
        return recommended_movies
    except Exception as e:
        st.error(f"Error generating recommendations: {e}")
        return []

if st.button("Get AI Recommendations ✨", type="primary", use_container_width=True):
    with st.spinner("Analyzing your taste... 🤖"):
        time.sleep(1.5) # Fake loading for effect
        recommendations = recommend(selected_movie)
        
        if recommendations:
            st.markdown(f"### 🎬 Top Matches for **{selected_movie}**")
            
            # CSS for hover flip cards and formatting
            st.markdown("""
            <style>
                .movie-title {
                    font-size: 18px;
                    font-weight: bold;
                    margin-top: 10px;
                    text-align: center;
                    color: #e0aaff;
                    white-space: nowrap;
                    overflow: hidden;
                    text-overflow: ellipsis;
                }
                .confidence-badge {
                    background: #7b2cbf;
                    color: white;
                    padding: 5px 10px;
                    border-radius: 20px;
                    font-size: 14px;
                    font-weight: bold;
                    display: inline-block;
                    margin-top: 5px;
                }
                .img-container img {
                    border-radius: 10px;
                    box-shadow: 0 5px 15px rgba(0,0,0,0.5);
                    transition: transform 0.3s;
                }
                .img-container img:hover {
                    transform: scale(1.05);
                    border: 2px solid #00f5d4;
                }
            </style>
            """, unsafe_allow_html=True)
            
            cols = st.columns(5)
            for idx, col in enumerate(cols):
                movie = recommendations[idx]
                with col:
                    st.markdown(f"<div class='img-container'><img src='{movie['poster']}' width='100%'></div>", unsafe_allow_html=True)
                    st.markdown(f"<div class='movie-title' title='{movie['title']}'>{movie['title']}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='text-align:center;'><span class='confidence-badge'>{movie['confidence']}% Match</span></div>", unsafe_allow_html=True)
                    
                    if st.button(f"❤️ Add", key=f"fav_{idx}", use_container_width=True):
                        if movie['title'] not in [m['title'] for m in st.session_state['favorites']]:
                            st.session_state['favorites'].append(movie)
                            st.toast(f"Added {movie['title']} to Favorites!")
                        else:
                            st.toast(f"{movie['title']} is already in Favorites!")
            
            # AI Explanation section
            st.markdown("<br><hr>", unsafe_allow_html=True)
            st.markdown("### 🧠 Why this recommendation?")
            st.markdown(f"<div class='glass-card'><p>Because you enjoyed <b>{selected_movie}</b>, our AI model identified patterns in genres, keywords, and cast members. The recommendations above share a high cosine similarity score with your selection, ensuring a thematic and cinematic match.</p></div>", unsafe_allow_html=True)

