document.getElementById('predictionForm').addEventListener('submit', async function (e) {

    
    // Prevenir o comportamento padrão do formulário
    e.preventDefault();   

    // recupera dados do formulário
    const predictionElement = document.getElementById('prediction');
    //reseta texto de predição
    predictionElement.textContent = '';

    //recupera values do formulário
    const danceability = parseFloat(document.getElementById('danceability').value);
    const energy = parseFloat(document.getElementById('energy').value);
    const tempo = parseFloat(document.getElementById('tempo').value);
    const loudness = parseFloat(document.getElementById('loudness').value);
    const acousticness = parseFloat(document.getElementById('acousticness').value);
    const speechiness = parseFloat(document.getElementById('speechiness').value);
    const valence = parseFloat(document.getElementById('valence').value);

    //monta objeto para envio
    const data = {
        danceability, energy, tempo, loudness, acousticness, speechiness, valence
    };


    //tenta realizar a chamada ao endpoint de predição
    try {
        const response = await fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });


        if (response.ok) {
            const result = await response.json();
          
            // Remover classes anteriores
            predictionElement.classList.remove('popular', 'not-popular');

            console.log('Prediction result:', result.prediction);  // Verifica o valor da predição

            // Verificar se é popular ou não e definir a cor
            if (result.prediction === 1) {
                predictionElement.textContent = 'Música Popular';
                predictionElement.classList.add('popular');  // Aplica a classe popular (azul)
            } else {
                predictionElement.textContent = 'Música Não Popular';
                predictionElement.classList.add('not-popular');  // Aplica a classe not-popular (vermelho)
            }

            console.log('Applied classes:', predictionElement.classList);  // Verifica as classes aplicadas

        } else {
            throw new Error('Erro ao realizar a predição.');
        }
    } catch (error) {
        document.getElementById('predictionError').textContent = 'Erro: ' + error.message;
    }


});





// Função para preencher automaticamente com base na URL da música
document.getElementById('fillButton').addEventListener('click', async function () {
    const musicUrl = document.getElementById('musicUrl').value;
    const fetchErrorElement = document.getElementById('fetchError'); 
    // Limpar mensagens de erro anteriores
    fetchErrorElement.textContent = ''; 
    // Validação para verificar se o campo URL não está vazio e contém o padrão "track/" 
    if ( musicUrl && !musicUrl.includes('track/')) {
        fetchErrorElement.textContent = 'A URL deve estar no formato correto e conter "track/". Exemplo: https://open.spotify.com/track/3QpkDyuXdjxhIyLyKtyC6O';
        return;
    } 
    //tenta realizar a chamada ao endpoint de preenchimento
    try {
        const response = await fetch('http://127.0.0.1:5000/fetch_spotify_data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url: musicUrl })
        });

        if (response.ok) {
            const data = await response.json();
            document.getElementById('danceability').value = data.danceability;
            document.getElementById('energy').value = data.energy;
            document.getElementById('tempo').value = data.tempo;
            document.getElementById('loudness').value = data.loudness;
            document.getElementById('acousticness').value = data.acousticness;
            document.getElementById('speechiness').value = data.speechiness;
            document.getElementById('valence').value = data.valence;
            fetchErrorElement.textContent = '';  // Limpa o erro anterior
        } else {
            throw new Error('Falha ao buscar os dados da música.');
        }
    } catch (error) {
        fetchErrorElement.textContent = 'Erro: ' + error.message;  // Exibe o erro
    }
});