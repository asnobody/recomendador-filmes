import pandas as pd
import tmdbsimple as tmdb
import streamlit as st

# TMDb API Key via secrets
tmdb.API_KEY = st.secrets["tmdb"]["api_key"]

ratings = pd.read_csv("data/ratings.csv")
movies = pd.read_csv("data/movies.csv")

user_movie_matrix = ratings.pivot_table(index="userId", columns="movieId", values="rating")

def recomendar_filmes_similares(titulo_filme, n=10):
    filme_selecionado = movies[movies['title'] == titulo_filme]
    if filme_selecionado.empty:
        return []

    movie_id = filme_selecionado.iloc[0]['movieId']
    
    if movie_id not in user_movie_matrix:
        return []

    filme_ratings = user_movie_matrix[movie_id]
    similares = user_movie_matrix.corrwith(filme_ratings)

    similares = similares.dropna().to_frame(name="correlacao")
    similares = similares.join(movies.set_index("movieId"), on="movieId")
    
    rating_counts = ratings.groupby("movieId")["rating"].count()
    similares = similares.join(rating_counts.rename("num_avaliacoes"), on="movieId")

    recomendados = similares[similares["num_avaliacoes"] >= 50].sort_values("correlacao", ascending=False)
    recomendados = recomendados[recomendados.index != movie_id]

    return recomendados[["title", "correlacao", "num_avaliacoes"]].head(n).reset_index(drop=True)

def buscar_poster(filme):
    search = tmdb.Search()
    response = search.movie(query=filme)
    if response['results']:
        poster_path = response['results'][0].get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
    return None