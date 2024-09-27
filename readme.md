# Spotify Machine learning project

Dataset URL : https://raw.githubusercontent.com/morettonijose/spotify_machine_learning/refs/heads/main/spotify_songs.csv 

Google Colab Notebook (Treinamento e escolha do modelo) : https://colab.research.google.com/drive/11iOcSP239T62tirEXc4QXGUOZy1K4mRY#scrollTo=0Quuwcmji3up

# Spotify Popularity Predictor

Este projeto é uma API baseada em Flask para prever a popularidade de músicas usando características como `danceability`, `energy`, `tempo`, entre outras, com base em um  dataset de músicas de sucesso da plataforma  .

## INSTALAÇÃO : 

### 1. Clone o repositório via bash

git clone https://github.com/morettonijose/spotify_machine_learn.git

cd spotify_machine_learn

cd backend

### 2. Crie e ative um ambiente virtual via bash (opcional, mas recomendado)

Observação : Em algumas configurações de ambiente você deverá usar os códigos de comando pip3 e python3 ao invés de pip e python. 

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

Uma vez que você teve sucesso em visualizar a interface de documentação do Swagger, abra uma nova janela do terminal e acesse novamente o diretório spotify_machine_learn, e então o diretório frontend do projeto . No terminal digite :

cd frontend


###  6.1 ) no terminal digite : python -m http.server 8100

###  6.2) então acesse a url : http://localhost:8100/ 



###  Extras : 


Observação 1 )  Para fins de simplificação e facilitação  de testes  serão retornado  valores aleatórios para as caracteristicas das músicas de qualquer URL inserida no campo de texto corrrespondente a URL . 
    

Observação 2 ) Se você deseja testar esta função usando a  API oficial do Spotify, basta configurar o arquivo .env com suas credenciais do Spotify Developes, substituindo XXX pelas respectivas credenciais conforme exemplo a seguir : 

SPOTIFY_CLIENT_ID=XXX

SPOTIFY_CLIENT_SECRET=XXX


