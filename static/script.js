document.addEventListener('DOMContentLoaded', () => {
    // Pega os elementos da página
    const generateBtn = document.getElementById('generate-btn');
    const carInfoInput = document.getElementById('car-info-input');
    const loader = document.getElementById('loader');
    const resultsArea = document.getElementById('results-area');
    const marketplaceOutput = document.getElementById('marketplace-output');
    const socialMediaOutput = document.getElementById('social-media-output');

    // Adiciona o evento de clique no botão principal
    generateBtn.addEventListener('click', async () => {
        const infoCarro = carInfoInput.value;

        if (!infoCarro.trim()) {
            alert('Por favor, insira as informações do veículo.');
            return;
        }

        // Mostra o loader e esconde os resultados antigos
        loader.style.display = 'block';
        resultsArea.style.display = 'none';

        try {
            // Faz a chamada para o nosso back-end
            const response = await fetch('/gerar-descricoes', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ info_carro: infoCarro }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Ocorreu um erro no servidor.');
            }

            const data = await response.json();

            // Coloca os textos gerados nos seus lugares
            marketplaceOutput.textContent = data.marketplace;
            socialMediaOutput.textContent = data.redes_sociais;

            // Esconde o loader e mostra os resultados
            loader.style.display = 'none';
            resultsArea.style.display = 'block';

        } catch (error) {
            loader.style.display = 'none';
            alert(`Erro: ${error.message}`);
            console.error('Erro ao gerar descrições:', error);
        }
    });

    // Adiciona a funcionalidade de "Copiar" para todos os botões
    document.querySelectorAll('.copy-btn').forEach(button => {
        button.addEventListener('click', () => {
            const targetId = button.dataset.target;
            const textToCopy = document.getElementById(targetId).textContent;

            navigator.clipboard.writeText(textToCopy).then(() => {
                // Feedback visual para o usuário
                const originalText = button.textContent;
                button.textContent = 'Copiado!';
                setTimeout(() => {
                    button.textContent = originalText;
                }, 2000); // Volta ao normal depois de 2 segundos
            }).catch(err => {
                console.error('Erro ao copiar texto: ', err);
                alert('Não foi possível copiar o texto.');
            });
        });
    });
});