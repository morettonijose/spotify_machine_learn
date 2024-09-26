# Spotify Machine learning project

Dataset URL : https://raw.githubusercontent.com/morettonijose/spotify_machine_learning/refs/heads/main/spotify_songs.csv 

Google Colab Notebook (Treinamento e escolha do modelo) : https://colab.research.google.com/drive/11iOcSP239T62tirEXc4QXGUOZy1K4mRY#scrollTo=0Quuwcmji3up

# Spotify Popularity Predictor

Este projeto é uma API baseada em Flask para prever a popularidade de músicas usando características como `danceability`, `energy`, `tempo`, entre outras, com base em um  dataset de músicas de sucesso da plataforma  .

## INSTALAÇÃO : 

### 1. Clone o repositório via bash

git clone https://github.com/morettonijose/spotify_machine_learn.git

cd spotify_machine_learn

### 2. Crie e ative um ambiente virtual via bash (opcional, mas recomendado)

python -m venv venv

source venv/bin/activate  # Para Linux/Mac

venv\Scripts\activate  # Para Windows

###  3. Instale as dependências via bash

pip install -r requirements.txt

###  4. Rodando o Backeend  : acesse via terminal a pasta backend e inicie o servidor backend. 

python app.py

###  5. Acesse a interface do Swagger

certifique-se que seu servidor backend está ativo na respectiva URL : http://127.0.0.1:5000/swagger/#/Prediction

###  6. Acesse a URL Do frontend para simular uma nova previsão de popularidade

Uma vez que você teve sucesso em visualizar a interface de documentação do Swagger, acesse o diretório frontend .

Para garantir o funcionamento correto da aplicação execute o seguinte procedimento ao invés de abrir diretamente o arquivo index.html : 

6.1 ) no terminal digite : python3 -m http.server 8100

6.2) então acesse a url : http://localhost:8100/frontend/index.html


