import os
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
import plotly.express as px
import openai
import google.generativeai as genai

# Carregar variáveis de ambiente
load_dotenv()

# Configurar chave da API do OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Configurar chave da API do Google Generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Características de uma sociedade utópica
characteristics = [
    "Social Equality",
    "Justice and Equity",
    "General Well-being",
    "Peace and Harmony",
    "Sustainability",
    "Freedom",
    "Technology and Innovation",
    "Participatory Governance",
    "Community and Solidarity",
    "Happiness and Personal Fulfillment"
]

# Estilo CSS para título, subtítulos e imagem centralizada
st.markdown("""
<style>
    .full-width-title {
        font-size: 50px;
        font-weight: bold;
        text-align: center;
        color: #333333;
        padding: 20px 0;
        margin: 0;
        width: 100%;
    }
    .subtitle {
        font-size: 24px;
        text-align: center;
        color: #333333;
        margin-top: -20px;
        padding-bottom: 20px;
    }
    div.stButton > button:first-child {
        background-color: #0066cc;
        color: white;
        font-size: 20px;
        font-weight: bold;
        padding: 14px 20px;
        border-radius: 10px;
        border: 2px solid #0066cc;
        transition: all 0.3s;
    }
    div.stButton > button:first-child:hover {
        background-color: #0052a3;
        border-color: #0052a3;
    }
    .full-width-section {
        padding: 20px;
        margin-top: 30px;
    }
    .centered-image {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 20px 0;
    }
    .centered-image img {
        max-width: 70%;
        height: auto;
    }
</style>
""", unsafe_allow_html=True)

# Título em largura total
st.markdown('<p class="full-width-title">Alltopia, the game</p>', unsafe_allow_html=True)

# Subtítulo
st.markdown('<p class="subtitle">Create your perfect society</p>', unsafe_allow_html=True)

# Função para analisar a sociedade com base nos valores ajustados
def analyze_society(values):
    average = sum(values.values()) / len(values)
    
    if average >= 7:
        analysis = "High Utopia"
    elif average >= 4:
        analysis = "Moderate Utopia"
    else:
        analysis = "Low Utopia"
    
    return average, analysis

# Inicializar o dicionário de valores
values = {characteristic: 5.0 for characteristic in characteristics}

# Dividir a tela em duas colunas do mesmo tamanho
col1, col2 = st.columns(2)

# Criação de sliders para cada característica na coluna da esquerda
with col1:
    st.markdown('<p class="subtitle">Choose the characteristics</p>', unsafe_allow_html=True)
    for characteristic in characteristics:
        values[characteristic] = st.slider(characteristic, 0.0, 10.0, 5.0)

# Exibir o gráfico de barras na coluna da direita
with col2:
    st.markdown('<p class="subtitle">Characteristic Values</p>', unsafe_allow_html=True)
    
    # Criar um DataFrame para o gráfico
    df = pd.DataFrame(list(values.items()), columns=['Characteristic', 'Value'])
    
    # Definir uma paleta de cores personalizada
    color_palette = px.colors.qualitative.Prism

    # Criar o gráfico de barras usando Plotly Express com cores diferentes
    fig = px.bar(df, x='Characteristic', y='Value', 
                 labels={'Value': 'Score', 'Characteristic': ''},
                 height=400,
                 color='Characteristic',
                 color_discrete_sequence=color_palette)
    
    fig.update_layout(xaxis_tickangle=-45, showlegend=False)
    
    # Exibir o gráfico
    st.plotly_chart(fig, use_container_width=True)

# Analisar a sociedade
average, analysis = analyze_society(values)

# Função para obter a chave da API do Google de forma segura
def get_google_api_key():
    return os.environ.get("GOOGLE_API_KEY")

# Análise usando Google Generative AI e OpenAI para imagem
if st.button("Analyze your society with AI"):
    api_key = get_google_api_key()
    if not api_key:
        st.error("Google API key not found. Please configure the GOOGLE_API_KEY in the environment variables.")
        st.info("If you're running this locally, you can set the API key in your system's environment variables.")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('google-generative-ai')
            
            input_text = (
                f"Analyze the utopian society with the following characteristics: {values}. "
                "Write the analysis with subtitles and 5 paragraphs of text."
            )
            response = model.generate_content(input_text)
            analysis = response.text
            
            # Gerar prompt para imagem usando OpenAI
            image_prompt_input = (
                f"Crie uma imagem que represente uma sociedade utópica com as seguintes características: {values}. "
                "O prompt deve ter 3 linhas de texto, em português do Brasil."
            )
            image_prompt_response = openai.Completion.create(
                engine="gpt-3.5-turbo-instruct",
                prompt=image_prompt_input,
                max_tokens=150,
                n=1,
                stop=None,
                temperature=1.0
            )
            image_prompt = image_prompt_response.choices[0].text.strip()
            
            # Gerar imagem automaticamente com o prompt
            response = openai.Image.create(
                model="dall-e-3",
                prompt=image_prompt,
                size="1024x1024",
                n=1,
            )
            image_url = response['data'][0]['url']
            
            # Exibir a imagem centralizada
            st.markdown('<div class="centered-image">', unsafe_allow_html=True)
            st.image(image_url, width=716)  # 70% de 1024 é aproximadamente 716
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.subheader("Analysis of your utopia by Google Generative AI")
            
            # Dividir a análise em parágrafos e subtítulos
            paragraphs = analysis.split('\n\n')
            for paragraph in paragraphs:
                if ': ' in paragraph:
                    subtitle, text = paragraph.split(': ', 1)
                    st.markdown(f"**{subtitle}**")
                    st.write(text)
                else:
                    st.write(paragraph)
        
        except Exception as e:
            st.error(f"Error calling the Google Generative AI API: {str(e)}")

# Seção de análise em largura total
st.markdown('<div class="full-width-section">', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Analysis of your utopia</p>', unsafe_allow_html=True)
st.write(f"Average of Values: {average:.2f}")
st.write(f"Classification: {analysis}")
st.markdown('</div>', unsafe_allow_html=True)

# Aviso final
st.markdown("""
<div style="text-align: center; padding: 20px; background-color: #f0f2f6; margin-top: 30px;">
    <p>Adjust the characteristics above to generate a new utopian society</p>
</div>
""", unsafe_allow_html=True)
