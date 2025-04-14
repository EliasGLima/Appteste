
import streamlit as st
from googleapiclient.discovery import build
import pandas as pd
import os

# Pega a chave da API do Streamlit Secrets
API_KEY = st.secrets["AIzaSyCRguIGKpbSZ-_iUnV8LYUbTpKbjxVTEUc"]

# Função para buscar vídeos no YouTube
def buscar_videos_por_hashtag(api_key, hashtag, max_results=10):
    youtube = build('youtube', 'v3', developerKey=api_key)

    request = youtube.search().list(
        q=hashtag,
        part='snippet',
        type='video',
        maxResults=max_results
    )
    response = request.execute()

    videos = []
    for item in response['items']:
        videos.append({
            'Título': item['snippet']['title'],
            'Canal': item['snippet']['channelTitle'],
            'Publicado em': item['snippet']['publishedAt'][:10],
            'Link': f"https://www.youtube.com/watch?v={item['id']['videoId']}"
        })
    return videos

# Layout Streamlit
st.set_page_config(page_title="Busca de Hashtags no YouTube", layout="wide")
st.title("🎥 Buscador de Vídeos por Hashtag no YouTube")

hashtag = st.text_input("Digite a hashtag para buscar vídeos (ex: #marketingdigital)")
max_results = st.slider("Número de vídeos", min_value=5, max_value=50, value=10)

if st.button("🔍 Buscar vídeos") and API_KEY and hashtag:
    with st.spinner("Buscando vídeos..."):
        try:
            resultados = buscar_videos_por_hashtag(API_KEY, hashtag, max_results)
            if resultados:
                df = pd.DataFrame(resultados)
                st.success(f"{len(df)} vídeos encontrados com a hashtag {hashtag}")
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("Nenhum vídeo encontrado.")
        except Exception as e:
            st.error(f"Ocorreu um erro: {e}")
