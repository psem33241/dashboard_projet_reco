import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from PIL import Image
import requests
from io import BytesIO
import plotly.graph_objects as go
from datetime import datetime
import random

# Chargement des données
df_reco = pd.read_csv('df_reco.csv')
df = pd.read_csv('df_complet.csv')

# Configuration de la page
st.set_page_config(page_title="NETFIX movies", layout="wide", initial_sidebar_state="collapsed")

# Vérification de la période de Noël
def is_christmas_period():
    current_date = datetime.now()
    start_date = datetime(current_date.year, 12, 1)
    end_date = datetime(current_date.year + 1, 1, 1)
    return start_date <= current_date <= end_date

# Ajout de styles CSS
st.markdown("""
<style>
/* Fond principal */
.stApp {
    background-color: #1a1a1d;
    background-image: linear-gradient(315deg, #1a1a1d 0%, #121212 74%);
    color: red;
    font-family: 'San Francisco', sans-serif;
}

/* Carrousel d'affiches */
.movie-carousel {
    width: 100%;
    overflow: hidden;
    height: 200px;
    position: relative;
    margin: 20px 0;
}

.movie-carousel-inner {
    display: flex;
    animation: scroll 60s linear infinite;
    gap: 20px;
}

.movie-carousel-inner:hover {
    animation-play-state: paused; /* Pause l'animation au survol */
}

@keyframes scroll {
    -60% { transform: translateX(100%); }
    60% { transform: translateX(-100%); }
}


/* Titre principal avec animation */
.title {
    font-family: 'Archivo Black', sans-serif;
    font-size: 10.5rem;
    font-weight: bold;
    text-align: center;
    color: #e50914;
    text-shadow: 0 0 20px #e50914, 0 0 40px #e50914;
    margin-bottom: 10px;
    transition: all 0.3s ease;
}

.title:hover {
    transform: scale(1.1);
    text-shadow: 0 0 30px #e50914, 0 0 60px #e50914, 0 0 90px #e50914;
    animation: glow 1s ease-in-out infinite alternate;
}

@keyframes glow {
    from {
        text-shadow: 0 0 20px #e50914, 0 0 40px #e50914;
    }
    to {
        text-shadow: 0 0 30px #ff0000, 0 0 50px #ff0000, 0 0 70px #ff0000;
    }
}

/* Petit logo */
.logo {
    position: fixed;
    top: 70px;
    left: 10px;
    width: 80px;
    height: auto;
    z-index: 100;
}

/* Style pour les labels de recherche */
.search-label {
    color: #e50914 !important;
    font-size: 1.2rem !important;
    font-weight: bold !important;
}

/* Indicateur */
.rating-indicator {
    width: 200px;
    height: 10px;
    margin: auto;
}

/* Fiche descriptive avec layout en colonnes */
.movie-card {
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 10px;
    padding: 0.25rem;
    margin: 1rem 0;
    transition: all 0.3s ease;
    display: grid;
    grid-template-columns: 1fr 2fr 1fr;
    gap: 20px;
}

.movie-card:hover {
    transform: scale(1.02);
    box-shadow: 0 8px 20px rgba(229, 9, 20, 0.7);
}

/* Style pour les affiches de films */
.movie-poster {
    transition: all 0.3s ease;
    cursor: pointer;
    display: inline-block;
}

.movie-poster:hover {
    transform: scale(1.1);
    box-shadow: 0 0 20px #e50914;
}

.movie-poster img {
    border-radius: 8px;
    display: block;
}

/* Footer amélioré */
.footer {
    text-align: center;
    padding: 20px;
    background: rgba(0, 0, 0, 0.9);
    color: #ffffff;
    opacity: 0.7;
    font-size: 0.9rem;
    border-top: 2px solid #e50914;
}

.copyright {
    margin-top: 10px;
    font-style: italic;
}
</style>

""", unsafe_allow_html=True)

# Affichage du petit logo
st.markdown('<img class="logo" src="https://i.ibb.co/2SD6NzT/NF1.webp" alt="Logo">', unsafe_allow_html=True)

# Carrousel d'affiches de films
def create_movie_carousel():
    random_movies = df.sample(n=30)
    carousel_html = '<div class="movie-carousel"><div class="movie-carousel-inner">'
    for _, movie in random_movies.iterrows():
        if isinstance(movie['poster_path'], str) and movie['poster_path']:
            poster_url = f"https://image.tmdb.org/t/p/w500{movie['poster_path']}"
            carousel_html += f'<img src="{poster_url}" alt="{movie["title_fr"]}" style="height: 200px;">'
    carousel_html += '</div></div>'
    st.markdown(carousel_html, unsafe_allow_html=True)

create_movie_carousel()

# Titre avec classe conditionnelle pour Noël
christmas_class = "christmas" if is_christmas_period() else ""
st.markdown(f'<h1 class="title {christmas_class}">NETFIX</h1>', unsafe_allow_html=True)

# Fonction pour afficher une image de film avec taille ajustable
def afficher_affiche(poster_path, size=300):
    if isinstance(poster_path, str) and poster_path:
        try:
            if not poster_path.startswith("http"):
                poster_path = f"https://image.tmdb.org/t/p/w500{poster_path}"
            response = requests.get(poster_path)
            img = Image.open(BytesIO(response.content))
            return img
        except:
            return None
    return None

# Fiche descriptive détaillée
def afficher_fiche_film(film_details):
    st.markdown('<div class="movie-card">', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 3])

    with col1:
        img = afficher_affiche(film_details['poster_path'])
        if img is not None:
            st.image(img, width=150)
        else:
            st.markdown("🎬 Affiche non disponible")

    with col2:
        st.subheader(film_details['title_fr'])
        st.text(f"Année : {film_details['startYear']}")
        st.text(f"Durée : {film_details['duration']} minutes")
        st.text(f"Note moyenne : {film_details['averageRating']} ⭐ ({film_details['numVotes']} votes)")
        st.text(f"Genres : {', '.join(eval(film_details['genres']))}")
        st.text(f"Réalisateur(s) : {', '.join(eval(film_details['directors']))}")
        st.text(f"Acteur(s) : {', '.join(eval(film_details['actors']))}")

    st.markdown('</div>', unsafe_allow_html=True)

# Fonction pour créer un indicateur de note
def afficher_indicateur_de_note(note):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=note,
        title={'text': "Note moyenne", 'font': {'color': '#ff6f61', 'size': 16}},
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [0, 10], 'tickcolor': "white"},
            'bar': {'color': "#ff6f61"},
            'steps': [
                {'range': [0, 5], 'color': "#333"},
                {'range': [5, 7], 'color': "#777"},
                {'range': [7, 10], 'color': "#ff6f61"}
            ]
        }
    ))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(color="white"))
    st.plotly_chart(fig, use_container_width=False)


# Fonction améliorée pour créer un indicateur de votes_count  
def afficher_indicateur_de_votecount(votes_count, max_votes=3000000, title="Nombre de votes", color_bar="#ff6f61"):
    # Validation des votes_count  
    if votes_count < 0:
        votes_count = 0  
    elif votes_count > max_votes:
        votes_count = max_votes

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=votes_count,
        title={'text': title, 'font': {'color': color_bar, 'size': 16}},
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [0, max_votes], 'tickcolor': "white"},
            'bar': {'color': color_bar},
            'steps': [
                {'range': [0, max_votes * 0.33], 'color': "#333"},
                {'range': [max_votes * 0.33, max_votes * 0.66], 'color': "#777"},
                {'range': [max_votes * 0.66, max_votes], 'color': color_bar}
            ]
        }
    ))

    fig.add_annotation(x=0.5, y=0.5, text=f"{votes_count:,} votes", showarrow=False, font=dict(size=20, color='white'))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(color="white"))
    st.plotly_chart(fig, use_container_width=False)




# Barre de recherche
search_term = st.text_input("🔍 Rechercher un film", "")
if search_term:
    mask = df['title_fr'].str.contains(search_term, case=False, na=False)
    filtered_df = df[mask]
    if not filtered_df.empty:
        selected_title = st.selectbox("Sélectionnez un film", filtered_df['title_fr'].tolist())
        if selected_title:
            selected_index = df[df['title_fr'] == selected_title].index[0]
            selected_film = df.loc[selected_index]
            
            # Fiche du film
            afficher_fiche_film(selected_film)
            
            # Affichage de l'indicateur
            if pd.notna(selected_film['averageRating']):
                st.markdown('<div class="rating-indicator">', unsafe_allow_html=True)
                afficher_indicateur_de_note(selected_film['averageRating'])
                afficher_indicateur_de_votecount(selected_film['numVotes'])
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Films recommandés
            st.markdown("### Films recommandés")
            reco_row = df_reco.loc[selected_index]
            for i in range(5):
                reco_index = reco_row[f'reco_{i+1}']
                if pd.notna(reco_index):
                    reco_film = df.loc[reco_index]
                    afficher_fiche_film(reco_film)
    else:
        st.warning("Aucun film trouvé.")

# Footer
st.markdown("""
<div class="footer">
    <p>© 2024 NETFIX - Votre plateforme futuriste de recommandation de films</p>
</div>
""", unsafe_allow_html=True)
