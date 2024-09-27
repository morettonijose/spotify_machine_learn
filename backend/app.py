import joblib
import numpy as np
import requests
from flask import Flask, request, jsonify, make_response
from flask_restful import Api, Resource
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
import random
import base64
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://localhost:8100", "http://127.0.0.1"]}})  # Permite requisições de localhost:8100 e 127.0.0.1
api = Api(app)

# Carregar o modelo salvo
modelo = joblib.load('best_knn_model.pkl')

# Configuração do Swagger UI
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': "Spotify Popularity Predictor"})
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Função para gerar valores aleatórios
def gerar_valores_randomicos():
    return {
        'danceability': round(random.uniform(0, 1), 2),
        'energy': round(random.uniform(0, 1), 2),
        'tempo': random.randint(60, 200),
        'loudness': round(random.uniform(-60, 0), 2),
        'acousticness': round(random.uniform(0, 1), 2),
        'speechiness': round(random.uniform(0, 1), 2),
        'valence': round(random.uniform(0, 1), 2)
    }

# Função para obter token do Spotify
def get_spotify_access_token():
    # Recuperar as chaves do Spotify do ambiente
    SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
    SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

    # Verificar se as variáveis de ambiente estão definidas
    if not SPOTIFY_CLIENT_ID or not SPOTIFY_CLIENT_SECRET:
        # Retornar valores randômicos se as variáveis de ambiente não estiverem configuradas corretamente
        print("Variáveis de ambiente não configuradas corretamente. Gerando valores randômicos.")
        return None

    # Caso as variáveis estejam presentes, gerar o token
    credentials = f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}"
    credentials_bytes = credentials.encode("utf-8")
    base64_credentials = base64.b64encode(credentials_bytes).decode("utf-8")

    auth_response = requests.post(
        "https://accounts.spotify.com/api/token",
        headers={
            "Authorization": f"Basic {base64_credentials}",
        },
        data={
            "grant_type": "client_credentials"
        }
    )

    return auth_response.json().get("access_token")

# Token do Spotify (gerado automaticamente)
SPOTIFY_ACCESS_TOKEN = get_spotify_access_token()

def get_spotify_track_id(url):
    """Extrai o ID da música a partir da URL do Spotify."""
    import re
    track_id_match = re.search(r'track/([a-zA-Z0-9]+)', url)
    return track_id_match.group(1) if track_id_match else None

def get_audio_features(track_id):
    """Consulta a API do Spotify para obter os dados da música."""
    if not SPOTIFY_ACCESS_TOKEN:
        # Retornar valores randômicos se o token não foi gerado
        return gerar_valores_randomicos()

    url = f"https://api.spotify.com/v1/audio-features/{track_id}"
    headers = {
        'Authorization': f'Bearer {SPOTIFY_ACCESS_TOKEN}'
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Falha ao consultar a API do Spotify")

class Predict(Resource):
    def post(self):
        """
        Realiza a predição da popularidade da música baseado nas características enviadas.
        """
        dados = request.get_json()
        entrada = np.array([dados['danceability'], dados['energy'], dados['tempo'],
                            dados['loudness'], dados['acousticness'], dados['speechiness'],
                            dados['valence']]).reshape(1, -1)
        predicao = modelo.predict(entrada)
        return jsonify({'prediction': int(predicao[0])})

class FetchSpotifyData(Resource):
    def post(self):
        """
        Busca as características da música no Spotify a partir da URL.
        """
        try:
            body = request.get_json()
            track_url = body.get("url")
            track_id = get_spotify_track_id(track_url)

            if not track_id:
                return jsonify({'error': 'URL inválida'}), 400

            # Buscar os dados da música via API do Spotify ou gerar valores aleatórios
            audio_features = get_audio_features(track_id)

            # Extrair as características relevantes
            response_data = {
                'danceability': audio_features['danceability'],
                'energy': audio_features['energy'],
                'tempo': audio_features['tempo'],
                'loudness': audio_features['loudness'],
                'acousticness': audio_features['acousticness'],
                'speechiness': audio_features['speechiness'],
                'valence': audio_features['valence']
            }
            return response_data, 200

        except Exception as e:
            # Retornar valores randômicos no caso de falha
            return make_response(gerar_valores_randomicos(), 500)

# Adicionar rotas à API
api.add_resource(Predict, '/predict')
api.add_resource(FetchSpotifyData, '/fetch_spotify_data')

if __name__ == '__main__':
    app.run(debug=True)