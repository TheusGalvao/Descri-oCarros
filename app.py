import os
import json
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
from dotenv import load_dotenv

# Carrega a variável de ambiente (sua chave de API) do arquivo .env
load_dotenv()

# Configura o Flask
app = Flask(__name__)

# Configura a API do Gemini com a chave
try:
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
except Exception as e:
    print(f"Erro ao configurar a API do Gemini. Verifique sua chave de API no arquivo .env. Erro: {e}")

# Rota principal que exibe a página HTML
@app.route('/')
def index():
    return render_template('index.html')

# Rota que vai gerar as descrições
@app.route('/gerar-descricoes', methods=['POST'])
def gerar_descricoes():
    # Pega as informações do carro enviadas pelo front-end
    dados_carro = request.json['info_carro']

    # Se a entrada estiver vazia, retorna um erro
    if not dados_carro:
        return jsonify({'error': 'Por favor, insira as informações do veículo.'}), 400

    # Monta o prompt para o Gemini
    # Esta é a parte mais importante: damos instruções claras para a IA
    prompt = f"""
    Você é um assistente especialista em criar descrições de carros para vendas em uma loja chamada Guaru Prime.
    Analise as informações do carro a seguir e gere dois textos, um para "Marketplace" e outro para "Redes Sociais", seguindo EXATAMENTE os modelos fornecidos abaixo.
    Extraia todas as informações necessárias do texto de entrada. Se alguma informação específica não for fornecida (ex: número de portas, cor), deixe o campo correspondente como "[não informado]".

    **Informações do carro fornecidas pelo usuário:**
    ---
    {dados_carro}
    ---

    **MODELO PARA MARKETPLACE:**
    ---
    [Marca e Modelo] [Versão] [Ano] | [Combustível] | [Câmbio]

    [Breve descrição chamativa com pontos fortes do veículo. Ex: Hatch compacto, econômico e ideal para o dia a dia. Ótima opção para quem busca conforto e baixo custo de manutenção.]

    Informações do veículo:

    Ano: [Ano]
    Cor: [Cor]
    Combustível: [Combustível]
    Quilometragem: [XX.XXX] km
    Câmbio: [Manual ou Automático]
    Motorização: [1.X]
    Número de portas: [4]
    Final da placa: [XX]

    Principais equipamentos:

    Ar-condicionado
    Direção elétrica/hidráulica
    Vidros elétricos
    Travas elétricas
    Retrovisores elétricos
    Central multimídia
    Câmera de ré
    Sensores de estacionamento
    Bancos em couro
    Rodas de liga leve
    Faróis de neblina
    Airbags
    Freios ABS

    [Frase final de reforço. Ex: Veículo em ótimo estado de conservação, ideal para quem busca economia, conforto e segurança.]
    ---

    **MODELO PARA REDES SOCIAIS:**
    ---
    [Marca e Modelo] - [Versão] [Motor]

    Ano: [Ano]
    [Quilometragem] Km Rodados
    WhatsApp: 11 2440-2166

    Os melhores seminovos de Guarulhos - SP 🚗
    Olha que incrível esse [tipo de carro], completíssimo, um SONHO!! 💙✨

    ✔ Flex
    ✔ Central Multimídia
    ✔ Motor [1.X]
    ✔ Câmbio [Automático ou Manual]
    ✔ Ar-condicionado
    ✔ Direção [Elétrica ou Hidráulica]
    ✔ Câmera de Ré
    ✔ Sensores de Estacionamento
    ✔ Vidros Elétricos
    ✔ Travas Elétricas
    ✔ Airbags
    ✔ Freios ABS
    ✔ Rodas de Liga Leve

    Também aceitamos carros na troca 🚗
    Agende sua visita agora! 🏃‍♂️

    📍 AutoShopping Internacional Guarulhos | R. Anton Philips, 186 | Prédio B, Vila Hermínia - Guarulhos/SP (Localizado no 2° piso próximo à Wincar)

    Mais informações no link da nossa bio 🔥

    #guaruprime #carros #guarulhos #autoshoppinginternacional #multimarcas #seucarronovo #carrobarato #[marca] #[modelo] #[versao] #fotosdecarros
    ---

    Retorne a resposta em formato JSON com duas chaves: "marketplace" e "redes_sociais".
    """

    try:
        # Inicializa o modelo do Gemini
        model = genai.GenerativeModel('gemini-1.5-flash')
        # Gera o conteúdo
        response = model.generate_content(prompt)
        
        # Limpa e converte a resposta para JSON
        # Às vezes a IA retorna o JSON dentro de um bloco de código, então limpamos isso.
        cleaned_response = response.text.strip().replace("```json", "").replace("```", "")
        parsed_json = json.loads(cleaned_response)

        # Retorna o JSON para o front-end
        return jsonify(parsed_json)

    except Exception as e:
        # Em caso de erro na API
        print(f"Erro ao chamar a API do Gemini: {e}")
        return jsonify({'error': f'Ocorreu um erro ao gerar as descrições: {e}'}), 500

# Roda o aplicativo
if __name__ == '__main__':
    app.run(debug=True)