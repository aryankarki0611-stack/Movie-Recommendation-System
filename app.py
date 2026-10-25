
import os
import html
import pickle
import requests
import streamlit as st
from dotenv import load_dotenv
load_dotenv()

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Cinevo | Discover Movies",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------- DESIGN SYSTEM ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

:root {
    --bg: #09090f;
    --surface: #12121c;
    --surface2: #191824;
    --border: #292638;
    --text: #f6f4ff;
    --muted: #a6a1b8;
    --purple: #a78bfa;
    --purple2: #7c3aed;
}

.stApp {
    background: var(--bg);
    color: var(--text);
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stMainBlockContainer"] {
    max-width: 1440px;
    padding-top: 1.1rem;
    padding-bottom: 3rem;
}

.block-container {
    max-width: 1440px;
    padding-top: 1.1rem;
    padding-bottom: 3rem;
}

/* Navigation */
.navbar {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 8px 0 22px;
    border-bottom: 1px solid #211f2c;
    margin-bottom: 24px;
}

.logo-mark {
    width: 38px;
    height: 38px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #a78bfa, #6d28d9);
    border-radius: 12px;
    font-size: 20px;
}

.logo-name {
    color: #fff;
    font: 700 20px 'Space Grotesk', sans-serif;
    letter-spacing: -.6px;
}

.logo-name span {
    color: var(--purple);
}

.nav-note {
    margin-left: auto;
    color: #b9a6ff;
    font-size: 13px;
    font-weight: 600;
}

/* Cinematic hero */
.hero {
    position: relative;
    overflow: hidden;
    min-height: 355px;
    display: flex;
    align-items: center;
    border-radius: 23px;
    border: 1px solid #302744;
    margin-bottom: 30px;
    background:
        linear-gradient(90deg,
            rgba(9, 8, 17, .97) 0%,
            rgba(13, 10, 25, .87) 42%,
            rgba(13, 10, 25, .15) 100%),
        linear-gradient(0deg, rgba(9,9,15,.45), transparent 60%),
        url("https://images.unsplash.com/photo-1440404653325-ab127d49abc1?auto=format&fit=crop&w=2000&q=85")
        center 44% / cover no-repeat;
}

.hero-content {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 36px;
    width: 100%;
    box-sizing: border-box;
    padding: 48px 44px;
}

.hero-left {
    flex: 1;
    min-width: 0;
}

.team-card {
    width: 260px;
    flex-shrink: 0;
    padding: 22px;
    border-radius: 18px;
    background: rgba(20, 15, 35, 0.78);
    border: 1px solid rgba(167, 139, 250, 0.35);
    backdrop-filter: blur(10px);
    box-sizing: border-box;
}

.team-card-title {
    color: #c4b5fd;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1.5px;
    margin-bottom: 18px;
}

.team-member {
    display: flex;
    flex-direction: column;
    gap: 4px;
    padding: 11px 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.10);
}

.team-member:last-child {
    border-bottom: none;
    padding-bottom: 0;
}

.team-member strong {
    color: #ffffff;
    font-size: 14px;
}

.team-member span {
    color: #c4b5fd;
    font-size: 12px;
}

.eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    color: #d4c6ff;
    background: rgba(139, 92, 246, .15);
    border: 1px solid rgba(167, 139, 250, .28);
    border-radius: 100px;
    padding: 7px 12px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.2px;
}

.hero h1 {
    color: #fff;
    font: 700 clamp(36px, 4.5vw, 59px)/1.06 'Space Grotesk', sans-serif;
    letter-spacing: -2px;
    margin: 22px 0 14px;
}

.hero p {
    color: #d0ccdc;
    font-size: 15px;
    line-height: 1.8;
    max-width: 430px;
    margin: 0;
}

/* Section headings */
.section-heading {
    color: #f7f5ff;
    font: 600 24px 'Space Grotesk', sans-serif;
    letter-spacing: -.6px;
    margin: 12px 0 4px;
}

.section-subtitle {
    color: var(--muted);
    font-size: 13px;
    margin: 0 0 18px;
}

/* Search controls */
div[data-baseweb="select"] > div {
    background: #15141f;
    border: 1px solid #373044;
    border-radius: 12px;
    min-height: 48px;
}

div[data-baseweb="select"] * {
    color: #f6f4ff;
}

div.stButton > button {
    width: 100%;
    min-height: 48px;
    background: linear-gradient(110deg, #8b5cf6, #6d45dc);
    border: 1px solid #9d7af8;
    border-radius: 12px;
    color: #ffffff !important;
    font-size: 14px;
    font-weight: 700;
    transition: all .2s ease;
    outline: none;
    box-shadow: none;
}

div.stButton > button:hover {
    background: linear-gradient(110deg, #9d75ff, #8059ed);
    border-color: #c4b5fd;
    color: #ffffff !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 18px rgba(139, 92, 246, 0.22);
}

div.stButton > button:focus,
div.stButton > button:focus-visible {
    color: #ffffff !important;
    border-color: #a78bfa;
    outline: none;
    box-shadow: 0 0 0 2px rgba(167, 139, 250, 0.2);
}

div.stButton > button:hover {
    background: linear-gradient(110deg, #9d75ff, #8059ed);
    border-color: #c4b5fd;
    color: #ffffff;
    transform: translateY(-1px);
    box-shadow: 0 4px 18px rgba(139, 92, 246, 0.22);
}

div.stButton > button:focus,
div.stButton > button:focus-visible {
    color: #ffffff;
    border-color: #a78bfa;
    outline: none;
    box-shadow: 0 0 0 2px rgba(167, 139, 250, 0.2);
}
/* Poster cards */
.poster-card {
    overflow: hidden;
    background: linear-gradient(180deg, #171622, #111019);
    border: 1px solid #2b2739;
    border-radius: 15px;
    padding: 9px;
    height: 100%;
    transition: transform .2s ease, border-color .2s ease;
}

.poster-card:hover {
    transform: translateY(-4px);
    border-color: #8b5cf6;
}

.poster-card img {
    display: block;
    width: 100%;
    aspect-ratio: 2 / 3;
    object-fit: cover;
    border-radius: 9px;
}

.poster-placeholder {
    width: 100%;
    aspect-ratio: 2 / 3;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 12px;
    border-radius: 9px;
    background: radial-gradient(ellipse at top, #302448, #151420 75%);
    color: #bda8fa;
    font-size: 42px;
}

.poster-placeholder span {
    font: 600 11px 'DM Sans', sans-serif;
    color: #aaa2c1;
}

.poster-title {
    color: #f8f6ff;
    font: 600 14px/1.45 'DM Sans', sans-serif;
    padding: 12px 2px 4px;
    min-height: 54px;
    overflow-wrap: anywhere;
}

.poster-label {
    color: #a99bd2;
    font-size: 11px;
    padding: 0 2px 7px;
}

/* Other components */
div[data-testid="stAlert"] {
    background: #171421;
    border: 1px solid #393047;
    border-radius: 12px;
}

div[data-testid="stCaptionContainer"] {
    color: #a6a1b8;
}

hr {
    border-color: #292638;
    margin: 30px 0;
}

.info-card {
    height: 100%;
    background: #12121c;
    border: 1px solid #292638;
    border-radius: 15px;
    padding: 20px;
}

.info-icon {
    font-size: 22px;
    margin-bottom: 12px;
}

.info-title {
    color: #f4f0ff;
    font: 600 15px 'Space Grotesk', sans-serif;
    margin-bottom: 7px;
}

.info-text {
    color: #aaa5b9;
    font-size: 13px;
    line-height: 1.7;
}

.footer {
    text-align: center;
    color: #777287;
    font-size: 12px;
    padding-top: 20px;
}

@media (max-width: 700px) {
    .hero {
        min-height: 300px;
        background-position: center;
    }
    .hero-content {
        padding: 28px 22px;
    }
    .hero h1 {
        letter-spacing: -1px;
    }
    .section-heading {
        font-size: 21px;
    }
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
@st.cache_resource
def load_movie_data():
    with open("movie_data.pkl", "rb") as file:
        movie_data, similarity = pickle.load(file)
    return movie_data, similarity

try:
    movies, cosine_sim = load_movie_data()
except Exception as error:
    st.error(f"Could not load movie data: {error}")
    st.stop()

# ---------------- RECOMMENDATIONS ----------------
def get_recommendations(title):
    matches = movies.index[movies["title"] == title].tolist()

    if not matches:
        return movies.iloc[0:0][["title", "movie_id"]]

    movie_index = matches[0]
    scores = list(enumerate(cosine_sim[movie_index]))
    scores.sort(key=lambda item: item[1], reverse=True)
    scores = [item for item in scores if item[0] != movie_index][:10]

    indices = [item[0] for item in scores]
    return movies.iloc[indices][["title", "movie_id"]]

# ---------------- POSTERS ----------------


@st.cache_data(ttl=300, show_spinner=False)
def fetch_poster(movie_id, movie_title):
    api_key = os.getenv("TMDB_API_KEY", "").strip()

    if not api_key:
        return None

    base_url = "https://image.tmdb.org/t/p/w500"
    search_url = "https://api.themoviedb.org/3/search/movie"

    for attempt in range(3):
        try:
            response = requests.get(
                search_url,
                params={
                    "api_key": api_key,
                    "query": str(movie_title),
                },
                timeout=15,
            )
            response.raise_for_status()

            results = response.json().get("results", [])

            # Prefer an exact title match when available.
            title_lower = str(movie_title).strip().lower()

            for result in results:
                if (
                    result.get("title", "").strip().lower() == title_lower
                    and result.get("poster_path")
                ):
                    return base_url + result["poster_path"]

            # Otherwise, use the first search result with a poster.
            for result in results:
                if result.get("poster_path"):
                    return base_url + result["poster_path"]

            # A successful search with no posters needs no retry.
            return None

        except (requests.RequestException, ValueError, TypeError):
            continue

    return None

# ---------------- NAVIGATION ----------------
st.markdown("""
<div class="navbar">
    <div class="logo-mark">🎬</div>
    <div class="logo-name">Cinevo</div>
    <div class="nav-note">MOVIE DISCOVERY&nbsp; ✦</div>
</div>
""", unsafe_allow_html=True)

# ---------------- CINEMATIC HERO ----------------
hero_html = """
<section class="hero">
    <div class="hero-content">
        <div class="hero-left">
            <div class="eyebrow">✦ YOUR PERSONAL MOVIE GUIDE</div>
            <h1>Your next movie<br>night starts here.</h1>
            <p>Pick a movie you love. Discover your next favourite with recommendations powered by machine learning.</p>
        </div>
        <div class="team-card">
            <div class="team-card-title">PROJECT TEAM</div>
            <div class="team-member"><strong>Aryan Singh</strong><span>26BCS11427</span></div>
            <div class="team-member"><strong>Mohammad Rehan</strong><span>26BCS11428</span></div>
            <div class="team-member"><strong>Vansh Kataria</strong><span>26BCS11452</span></div>
        </div>
    </div>
</section>
"""

st.markdown(hero_html, unsafe_allow_html=True)
# ---------------- MOVIE SEARCH ----------------
st.markdown(
    '<div class="section-heading">Find your next watch</div>'
    '<div class="section-subtitle">Start with a movie you already love.</div>',
    unsafe_allow_html=True,
)

search_col, button_col = st.columns([4, 1.3], gap="small")

with search_col:
    selected_movie = st.selectbox(
        "Choose a movie",
        options=movies["title"].dropna().tolist(),
        label_visibility="collapsed",
        placeholder="Search for a movie you love...",
    )

with button_col:
    recommend_clicked = st.button(
        "✦ Discover",
        use_container_width=True,
    )

if recommend_clicked:
    st.session_state["selected_for_recommendations"] = selected_movie

chosen = st.session_state.get("selected_for_recommendations")

# ---------------- RECOMMENDATION GRID ----------------
if chosen:
    recommendations = get_recommendations(chosen)

    st.markdown(
        '<div class="section-heading">Made for your taste</div>'
        '<div class="section-subtitle">'
        'Because you like ' + html.escape(str(chosen)) +
        ' · 10 similar picks</div>',
        unsafe_allow_html=True,
    )

    if recommendations.empty:
        st.warning("No recommendations were found for this movie.")
    else:
        for start in range(0, len(recommendations), 5):
            st.markdown("<div style='height: 12px'></div>", unsafe_allow_html=True)
            columns = st.columns(5)

            for column, index in zip(
                columns,
                range(start, min(start + 5, len(recommendations))),
            ):
                movie = recommendations.iloc[index]
                title = str(movie["title"])
                safe_title = html.escape(title)
                movie_id = movie["movie_id"]

                with column:
                    poster_url = fetch_poster(movie_id, title)

                    if poster_url:
                        st.markdown(
                            f"""
                            <div class="poster-card">
                                <img src="{html.escape(poster_url, quote=True)}"
                                     alt="{safe_title}">
                                <div class="poster-title">{safe_title}</div>
                                <div class="poster-label">✦ Recommended for you</div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                    else:
                        st.markdown(
                            f"""
                            <div class="poster-card">
                                <div class="poster-placeholder">
                                    🎞️
                                    <span>POSTER UNAVAILABLE</span>
                                </div>
                                <div class="poster-title">{safe_title}</div>
                                <div class="poster-label">✦ Recommended for you</div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

    st.caption(
        "Recommendations use content-based filtering and precomputed "
        "movie similarity scores."
    )
else:
    st.markdown(
        '<div class="section-subtitle">'
        'Choose a movie above and discover films with a similar feel.'
        '</div>',
        unsafe_allow_html=True,
    )

# ---------------- HOW IT WORKS ----------------
st.markdown("---")
st.markdown(
    '<div class="section-heading">Behind the recommendations</div>'
    '<div class="section-subtitle">'
    'A simple journey from your favourite film to your next watch.'
    '</div>',
    unsafe_allow_html=True,
)

step1, step2, step3 = st.columns(3)

with step1:
    st.markdown("""
    <div class="info-card">
        <div class="info-icon">🎬</div>
        <div class="info-title">01 · Choose</div>
        <div class="info-text">Select a movie you already enjoy
        to set the starting point.</div>
    </div>
    """, unsafe_allow_html=True)

with step2:
    st.markdown("""
    <div class="info-card">
        <div class="info-icon">✦</div>
        <div class="info-title">02 · Analyse</div>
        <div class="info-text">The model compares its precomputed
        similarity scores against other movies.</div>
    </div>
    """, unsafe_allow_html=True)

with step3:
    st.markdown("""
    <div class="info-card">
        <div class="info-icon">🍿</div>
        <div class="info-title">03 · Discover</div>
        <div class="info-text">Explore ten movies ranked by
        similarity to your selected film.</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="footer">
    CINEVO &nbsp;·&nbsp; MADE WITH PYTHON, STREAMLIT & MACHINE LEARNING
</div>
""", unsafe_allow_html=True)
