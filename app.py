import streamlit as st
from recomendador import recomendar_filmes_similares, movies, buscar_poster
st.set_page_config(page_title="Recomendador de Filmes", layout="centered")
st.title("🎬 Recomendador de Filmes (semelhantes)")

# --- Autenticação simples ---
USUARIOS = {"admin": "1234", "user": "filmes"}

st.title("🔐 Login")
usuario = st.text_input("Usuário")
senha = st.text_input("Senha", type="password")

if usuario not in USUARIOS or USUARIOS[usuario] != senha:
    st.warning("Digite usuário e senha válidos.")
    st.stop()

# --- App principal ---
#st.set_page_config(page_title="Recomendador de Filmes", layout="centered")
#st.title("🎬 Recomendador de Filmes (semelhantes)")

filmes_disponiveis = movies["title"].sort_values().tolist()
filme_escolhido = st.selectbox("Escolha um filme:", filmes_disponiveis)

num_recomendacoes = st.slider("Quantos filmes recomendar?", min_value=5, max_value=10, value=5)

if st.button("Recomendar"):
    recomendacoes = recomendar_filmes_similares(filme_escolhido, n=num_recomendacoes)
    if recomendacoes.empty:
        st.warning("Não foi possível encontrar recomendações para este filme.")
    else:
        st.subheader("🎯 Recomendações:")
        for idx, row in recomendacoes.iterrows():
            st.markdown(f"### 🎞️ {row['title']}")
            st.write(f"🔗 Similaridade: {row['correlacao']:.2f} — ⭐ Avaliações: {row['num_avaliacoes']}")
            poster = buscar_poster(row['title'])
            if poster:
                st.image(poster, width=150)
