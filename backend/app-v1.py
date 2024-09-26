from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS  # Importando Flask-CORS
import joblib
import numpy as np

# Inicializando a aplicação Flask
app = Flask(__name__)
CORS(app)  # Habilitando CORS para a aplicação
api = Api(app)

# Carregando o modelo salvo
modelo = joblib.load('best_knn_model.pkl')

# Swagger UI setup - ponto de acesso para a documentação
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'  # O arquivo JSON que conterá a especificação da API
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': "Spotify Popularity Predictor"})
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


# Rota para realizar a predição com o modelo
class Predict(Resource):
    def post(self):
        """
        Realiza predição de popularidade baseado em características da música.
        ---
        tags:
          - Prediction
        parameters:
          - in: body
            name: body
            description: Dados da música
            schema:
              type: object
              required:
                - danceability
                - energy
                - tempo
                - loudness
                - acousticness
                - speechiness
                - valence
              properties:
                danceability:
                  type: number
                  example: 0.7
                energy:
                  type: number
                  example: 0.8
                tempo:
                  type: number
                  example: 120.0
                loudness:
                  type: number
                  example: -5.5
                acousticness:
                  type: number
                  example: 0.1
                speechiness:
                  type: number
                  example: 0.05
                valence:
                  type: number
                  example: 0.9
        responses:
          200:
            description: Retorna a predição do modelo
            schema:
              type: object
              properties:
                prediction:
                  type: integer
                  description: Classe da predição (1 para popular, 0 para não popular)
                  example: 1
        """
        # Obter os dados JSON enviados pelo front-end
        dados = request.get_json()

        # Converter os dados recebidos para um array numpy
        entrada = np.array([dados['danceability'], dados['energy'], dados['tempo'],
                            dados['loudness'], dados['acousticness'], dados['speechiness'],
                            dados['valence']]).reshape(1, -1)

        # Fazer a predição usando o modelo carregado
        predicao = modelo.predict(entrada)

        # Retornar a predição em formato JSON
        return jsonify({'prediction': int(predicao[0])})


# Adicionar a rota predict à API RESTful
api.add_resource(Predict, '/predict')

if __name__ == '__main__':
    app.run(debug=True)
