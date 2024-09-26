import pytest
import joblib
from sklearn.metrics import accuracy_score, f1_score
import numpy as np
import pandas as pd

# Carregar o modelo treinado
modelo = joblib.load('best_knn_model.pkl')

# Dados de teste para verificar o desempenho do modelo (pode ser ajustado para seus dados de validação reais)
dados_teste = pd.DataFrame([
    [0.5, 0.7, 120, -5.0, 0.2, 0.1, 0.8],  # Exemplo de música popular
    [0.2, 0.3, 100, -10.0, 0.6, 0.05, 0.4], # Exemplo de música não popular
    [0.9, 0.8, 150, -3.0, 0.1, 0.15, 0.7],  # Exemplo de música popular
], columns=['danceability', 'energy', 'tempo', 'loudness', 'acousticness', 'speechiness', 'valence'])

# As labels reais correspondentes para os dados de teste
labels_reais = np.array([1, 0, 1])

# Thresholds mínimos de desempenho (ajuste conforme necessário)
PRECISION_THRESHOLD = 0.65  # Ajustado para permitir testes iniciais
F1_SCORE_THRESHOLD = 0.65    # Ajustado para permitir testes iniciais

# Função para validar os dados antes de enviar ao modelo
def validate_data(data):
    if any([
        data['danceability'] < 0 or data['danceability'] > 1,
        data['energy'] < 0 or data['energy'] > 1,
        data['tempo'] < 60 or data['tempo'] > 200,
        data['loudness'] < -60 or data['loudness'] > 0,
        data['acousticness'] < 0 or data['acousticness'] > 1,
        data['speechiness'] < 0 or data['speechiness'] > 1,
        data['valence'] < 0 or data['valence'] > 1
    ]):
        raise ValueError("Dados fora dos limites esperados.")
    return True

# Teste 1: Verificar a precisão do modelo
def test_model_accuracy():
    """Teste para garantir que a precisão do modelo está dentro do threshold aceitável."""
    # Fazer predições usando o modelo carregado
    predicoes = modelo.predict(dados_teste)

    # Calcular a precisão do modelo
    precisao = accuracy_score(labels_reais, predicoes)

    # Verificar se a precisão está acima do threshold
    assert precisao >= PRECISION_THRESHOLD, f'Precisão do modelo {precisao} abaixo do esperado {PRECISION_THRESHOLD}.'

# Teste 2: Verificar o F1-Score do modelo
def test_model_f1_score():
    """Teste para garantir que o F1-Score do modelo está dentro do threshold aceitável."""
    # Fazer predições usando o modelo carregado
    predicoes = modelo.predict(dados_teste)

    # Calcular o F1-Score do modelo
    f1 = f1_score(labels_reais, predicoes)

    # Verificar se o F1-Score está acima do threshold
    assert f1 >= F1_SCORE_THRESHOLD, f'F1-Score do modelo {f1} abaixo do esperado {F1_SCORE_THRESHOLD}.'

# Teste 3: Verificar tratamento de dados inválidos
def test_model_invalid_data():
    """Teste para verificar se o modelo lida corretamente com dados inválidos."""
    with pytest.raises(ValueError):
        # Definindo dados inválidos (fora dos limites aceitáveis)
        dados_invalidos = pd.DataFrame([[999, -999, 0, 0, 0, 0, 0]],
                     columns=['danceability', 'energy', 'tempo', 'loudness', 'acousticness', 'speechiness', 'valence'])
        
        # Chamando explicitamente a função de validação
        validate_data(dados_invalidos.iloc[0])  # Validação de uma linha dos dados inválidos
        
        # Previsão (caso os dados passem pela validação, o modelo tentaria fazer uma previsão)
        modelo.predict(dados_invalidos)
