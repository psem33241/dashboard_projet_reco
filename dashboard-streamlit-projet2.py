import streamlit as st  
import pandas as pd  
import plotly.graph_objects as go  
from PIL import Image  
import requests  
from io import BytesIO  
import random  
import os  # Pour manipuler les chemins de fichiers  
import ast  # Pour une évaluation sécurisée des données
import base64 #Pour encodage en base64

# Configuration de la page  
st.set_page_config(page_title="NETFIX Movies", layout="wide", initial_sidebar_state="expanded")

# Chargement des données  
@st.cache_data  
def load_data():
    # Chemin relatif basé sur le répertoire du script  
    base_dir = os.path.dirname(__file__)  # Obtient le répertoire du script

    try:
        df_reco = pd.read_csv(os.path.join(base_dir, 'df_reco.csv'))  # Utilise le chemin relatif  
        df = pd.read_csv(os.path.join(base_dir, 'df_complet.csv'))  # Utilise le chemin relatif  
    except FileNotFoundError as e:
        st.error(f"Erreur : Le fichier n'a pas été trouvé. Détails : {e}")
        return None, None  
    except pd.errors.EmptyDataError:
        st.error("Erreur : Le fichier est vide.")
        return None, None  
    except pd.errors.ParserError:
        st.error("Erreur : Problème lors de l'analyse du fichier.")
        return None, None  
    return df_reco, df

df_reco, df = load_data()

# Ajouter un identifiant unique si la colonne 'id' n'existe pas  
if df is not None and 'id' not in df.columns:
    df['id'] = df.index

# Récupérer tous les genres, réalisateurs et acteurs disponibles avec caching  
@st.cache_data  
def preprocess_data(df):
    all_genres = set()
    all_directors = set()
    all_actors = set()

    for index, row in df.iterrows():
        if pd.notna(row['genres']):
            genres_list = ast.literal_eval(row['genres'])  # Utiliser ast.literal_eval pour évaluer la chaîne en liste de genres  
            all_genres.update(genres_list)
        if pd.notna(row['directors']):
            directors_list = ast.literal_eval(row['directors'])  # Utiliser ast.literal_eval pour évaluer la chaîne en liste de réalisateurs  
            all_directors.update(directors_list)
        if pd.notna(row['actors']):
            actors_list = ast.literal_eval(row['actors'])  # Utiliser ast.literal_eval pour évaluer la chaîne en liste d'acteurs  
            all_actors.update(actors_list)

    return all_genres, all_directors, all_actors

if df is not None:  # Prendre en compte que df pourrait être None  
    all_genres, all_directors, all_actors = preprocess_data(df)

# Ajouter de styles CSS personnalisés  
st.markdown("""
<style>
/* Styles personnalisés pour l'application */
.stApp {
    background-color: #1a1a1d;
    color: red;
    font-family: 'San Francisco', sans-serif;
}

/* Titre principal avec animation */
.title {
    font-family: 'Archivo Black', sans-serif;
    font-size: 20rem; /* Doubler la taille */
    font-weight: bold;
    text-align: center;
    color: #e50914;
    text-shadow: 0 0 20px #e50914, 0 0 40px #e50914;
    margin-bottom: 10px;
    position: relative;
    overflow: hidden;
}

.title:hover {
    transform: scale(1.1);
    animation: glitch 1s infinite; /* Ajouter l'animation de glitch sur hover */
}

/* Animation de glitch */
@keyframes glitch {
    0% { transform: translate(2px, 2px); }
    20% { transform: translate(-2px, -2px); }
    40% { transform: translate(2px, 0); }
    60% { transform: translate(-2px, 2px); }
    80% { transform: translate(2px, -2px); }
    100% { transform: translate(0); }
}

/* Effet de reflet */
.reflect {
    position: absolute;
    top: 10%; /* Ajustez cette valeur pour définir la position du reflet */
    left: 0;
    right: 0;
    text-align: center;
    color: rgba(233, 9, 20, 0.3); /* Couleur du reflet avec transparence */
    transform: scaleY(-1); /* Retourner verticalement pour simuler le reflet */
    filter: blur(2px); /* Ajouter un flou pour le reflet */
}

/* Position du logo */
.logo {
    position: absolute;
    top: 10px;  /* Ajustez la position verticale */
    left: 10px; /* Ajustez la position horizontale */
    z-index: 10; /* Assurez-vous que le logo est au-dessus des autres éléments */
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
    animation: scroll 30s linear infinite;
    gap: 20px;
}
.movie-carousel-inner:hover {
    animation-play-state: paused;
}
@keyframes scroll {
    0% { transform: translateX(100%); }
    100% { transform: translateX(-100%); }
}

/* Footer */
.footer {
    text-align: center;
    padding: 20px;
    background: rgba(0, 0, 0, 0.9);
    color: #ffffff;
    opacity: 0.7;
    font-size: 0.9rem;
    border-top: 2px solid #e50914;
}

/* Couleur de texte pour les titres */
.mode-clair {
    color: #FFFFFF; /* Titres en blanc */
}
</style>
""", unsafe_allow_html=True)

# Afficher l'image de fond localement  
# Remplacez 'path/to/your/background_image.jpg' par le chemin de votre image  
image_path = os.path.join(os.path.dirname(__file__), './background-pic.avif')
st.markdown(f"""
    <style>
        .stApp {{
            background-image: url(data:image/jpeg;base64,{base64.b64encode(open(image_path, "rb").read()).decode()});
            background-size: cover; /* Ajuste l'image pour couvrir tout l'arrière-plan */
            background-repeat: no-repeat; /* Ne pas répéter l'image */
        }}
    </style>
""", unsafe_allow_html=True)

# Page d'accueil  
def home_page():
    st.markdown('<a id="home"></a>', unsafe_allow_html=True)
    
    # Ajouter le logo en haut à gauche  
    st.markdown('<div class="logo"><img src="https://i.ibb.co/2SD6NzT/NF1.webp" alt="Logo" width="100" /></div>', unsafe_allow_html=True)
    
    st.markdown('<div style="position: relative;">', unsafe_allow_html=True)
    st.markdown('<h1 class="title">NETFIX</h1>', unsafe_allow_html=True)  # Titre  
    st.markdown('<h1 class="reflect">NETFIX</h1>', unsafe_allow_html=True)  # Reflet  
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("### Découvrez les meilleurs films recommandés pour vous.")
    create_movie_carousel()
    st.markdown("<hr>", unsafe_allow_html=True)

# Fonction pour afficher le carrousel d'affiches  
def create_movie_carousel():
    random_movies = df.sample(n=30)
    carousel_html = '<div class="movie-carousel"><div class="movie-carousel-inner">'
    for _, movie in random_movies.iterrows():
        if isinstance(movie['poster_path'], str) and movie['poster_path']:
            poster_url = f"https://image.tmdb.org/t/p/w500{movie['poster_path']}"
            carousel_html += f'<img src="{poster_url}" alt="{movie["title_fr"]}" style="height: 200px;">'
    carousel_html += '</div></div>'
    st.markdown(carousel_html, unsafe_allow_html=True)

# Fonction de recherche avancée de films  
def search_page():
    st.markdown('<a id="search"></a>', unsafe_allow_html=True)
    st.header("Recherche de Films")
    search_term = st.text_input("🔍 Rechercher un film", "")
    
    # Filtrer les genres uniques  
    sorted_genres = sorted(list(all_genres))
    # Filtres supplémentaires  
    genre_filter = st.multiselect("Filtres de genre", sorted_genres)
    year_filter = st.slider("Filtrer par année", min_value=int(df['startYear'].min()), max_value=int(df['startYear'].max()), value=(int(df['startYear'].min()), int(df['startYear'].max())))
    
    # Ajouter des filtres pour les réalisateurs et acteurs  
    director_filter = st.multiselect("Filtres de réalisateur", sorted(list(all_directors)))
    actor_filter = st.multiselect("Filtres d'acteur", sorted(list(all_actors)))

    # Appliquer les filtres  
    mask = df['title_fr'].str.contains(search_term, case=False, na=False)
    if genre_filter:
        mask &= df['genres'].apply(lambda x: any(genre in genre_filter for genre in eval(x)))  # Comparaison avec plusieurs genres  
    mask &= (df['startYear'] >= year_filter[0]) & (df['startYear'] <= year_filter[1])

    # Appliquer le filtre par réalisateur  
    if director_filter:
        mask &= df['directors'].apply(lambda x: any(director in director_filter for director in eval(x)))
    
    # Appliquer le filtre par acteur  
    if actor_filter:
        mask &= df['actors'].apply(lambda x: 
            any(actor in actor_filter for actor in eval(x) if isinstance(x, str) and x)  # Évaluation conditionnelle  
            if isinstance(x, str) else []  # Si x n'est pas une chaîne, renvoyez une liste vide  
        )

    filtered_df = df[mask]
    if not filtered_df.empty:
        selected_title = st.selectbox("Sélectionnez un film", filtered_df['title_fr'].tolist())
        if selected_title:
            selected_index = df[df['title_fr'] == selected_title].index[0]
            selected_film = df.iloc[selected_index]
            afficher_fiche_film(selected_film)
            display_recommendations(selected_film, df, df_reco)
    else:
        st.warning("Aucun film trouvé avec ce titre ou ces critères.")

# Footer  
def footer():
    st.markdown("""
    <div class="footer">
        <p>© 2024 NETFIX - Votre plateforme futuriste de recommandation de films</p>
    </div>
    """, unsafe_allow_html=True)

# Fonction pour afficher la fiche descriptive d'un film  
def afficher_fiche_film(film_details):
    st.markdown('<div class="movie-card">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([2, 4, 1])
    
    with col1:
        img = afficher_affiche(film_details['poster_path'], size=250)
        if img is not None:
            st.image(img, width=250)
        else:
            st.markdown("🎬 Affiche non disponible")
    
    with col2:
        st.subheader(f"{film_details['title_fr']}")
        st.text(f"Année : {film_details['startYear']}")
        st.text(f"Durée : {film_details['duration']} minutes")
        st.text(f"Note moyenne : {film_details['averageRating']} / 10 ⭐ ({film_details['numVotes']} votes)")
        st.text(f"Genres : {', '.join(eval(film_details['genres']))}")
        st.text(f"Réalisateur(s) : {', '.join(eval(film_details['directors']))}")
        
        # Vérification de la validité avant d'évaluer les acteurs  
        if isinstance(film_details['actors'], str):
            try:
                acteurs = eval(film_details['actors'])
                st.text(f"Acteur(s) : {', '.join(acteurs)}")
            except Exception as e:
                st.text("Acteur(s) : Données non disponibles")
        else:
            st.text("Acteur(s) : Données non disponibles")
    
    with col3:
        if pd.notna(film_details['averageRating']):
            afficher_indicateur_de_note(film_details['averageRating'], film_details['id'], size=100)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Fonction pour afficher les recommandations  
def display_recommendations(selected_film, df, df_reco):
    st.markdown("### Films recommandés")
    reco_row = df_reco.loc[selected_film.name]
    
    for i in range(5):
        reco_index = reco_row[f'reco_{i+1}']
        if pd.notna(reco_index):
            reco_film = df.loc[reco_index]
            afficher_fiche_film(reco_film)
        else:
            st.warning("Aucun film trouvé.")

# Fonction pour afficher une affiche de film  
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

# Fonction pour afficher l'indicateur de la note  
def afficher_indicateur_de_note(note, film_id, size=100):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=note,
        title={'text': "Note moyenne", 'font': {'color': '#ff6f61', 'size': 14}},
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [0, 10], 'tickcolor': "white"},
            'bar': {'color': "#ff6f61"},
            'steps': [
                {'range': [0, 3], 'color': "#d3d3d3"},
                {'range': [3, 7], 'color': "#f2b40f"},
                {'range': [7, 10], 'color': "#1fae2d"}
            ]
        }
    ))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(color="white", size=10))
    st.plotly_chart(fig, use_container_width=False, key=f"gauge_{film_id}_rating", width=size)

# Affichage des pages  
home_page()
search_page()

# Footer : à afficher après toutes les sections principales  
footer()