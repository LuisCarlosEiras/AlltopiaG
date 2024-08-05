import os
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai
from PIL import Image
import base64
from io import BytesIO

load_dotenv()

# Retrieve the API key from the environment variables
google_api_key = os.getenv("GOOGLE_API_KEY")

if google_api_key:
    genai.configure(api_key=google_api_key)
else:
    st.error("Google API key not found. Please configure the GOOGLE_API_KEY in the environment variables.")
    st.stop()

# Characteristics of a utopian society
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

# CSS style (unchanged)
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
        max-width: 50%;
        height: auto;
    }
</style>
""", unsafe_allow_html=True)

# Full-width title
st.markdown('<p class="full-width-title">Alltopia, the game</p>', unsafe_allow_html=True)

# Subtitle
st.markdown('<p class="subtitle">Create your perfect society</p>', unsafe_allow_html=True)

# Function to analyze the society based on adjusted values
def analyze_society(values):
    average = sum(values.values()) / len(values)
    
    if average >= 7:
        analysis = "High Utopia"
    elif average >= 4:
        analysis = "Moderate Utopia"
    else:
        analysis = "Low Utopia"
    
    return average, analysis

# Initialize the values dictionary
values = {characteristic: 5.0 for characteristic in characteristics}

# Split the screen into two equal columns
col1, col2 = st.columns(2)

# Create sliders for each characteristic in the left column
with col1:
    st.markdown('<p class="subtitle">Choose the characteristics</p>', unsafe_allow_html=True)
    for characteristic in characteristics:
        values[characteristic] = st.slider(characteristic, 0.0, 10.0, 5.0)

# Display the bar chart in the right column
with col2:
    st.markdown('<p class="subtitle">Characteristic Values</p>', unsafe_allow_html=True)
    
    # Create a DataFrame for the chart
    df = pd.DataFrame(list(values.items()), columns=['Characteristic', 'Value'])
    
    # Define a custom color palette
    color_palette = px.colors.qualitative.Prism

    # Create the bar chart using Plotly Express with different colors
    fig = px.bar(df, x='Characteristic', y='Value', 
                 labels={'Value': 'Score', 'Characteristic': ''},
                 height=400,
                 color='Characteristic',
                 color_discrete_sequence=color_palette)
    
    fig.update_layout(xaxis_tickangle=-45, showlegend=False)
    
    # Display the chart
    st.plotly_chart(fig, use_container_width=True)

# Analyze the society
average, analysis = analyze_society(values)

def get_gemini_response(prompt, image_prompt=None):
    model = genai.GenerativeModel('gemini-pro')
    if image_prompt:
        response = model.generate_content([prompt, image_prompt])
    else:
        response = model.generate_content(prompt)
    return response.text

def generate_image(prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content(
        ["Generate an image based on this description:", prompt],
        generation_config=genai.types.GenerationConfig(
            max_output_tokens=2048,
        )
    )
    # Extract the base64-encoded image data from the response
    for part in response.parts:
        if part.mime_type.startswith('image/'):
            image_data = part.data
            image = Image.open(BytesIO(base64.b64decode(image_data)))
            return image
    return None

# Full-width analysis section
st.markdown('<div class="full-width-section">', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Analysis of your utopia</p>', unsafe_allow_html=True)
st.write(f"Average of Values: {average:.2f}")
st.write(f"Classification: {analysis}")

# Analysis using Google Generative AI
if st.button("Analyze your society with Google Generative AI"):
    try:
        # Generate image prompt
        image_prompt_input = (
            f"Create a prompt for an image that represents a utopian society with the following characteristics: {values}. "
            "The prompt should be detailed and suitable for an AI image generation model."
        )
        image_prompt = get_gemini_response(image_prompt_input)
        
        # Generate and display the image
        st.subheader("Generated Image of Utopian Society")
        image = generate_image(image_prompt)
        if image:
            st.image(image, caption="Generated Image of Utopian Society", use_column_width=True)
        else:
            st.warning("Failed to generate image. Proceeding with text analysis.")
        
        # Generate text analysis
        input_text = (
            f"Analyze the utopian society with the following characteristics: {values}. "
            "Write the analysis with subtitles and 5 paragraphs of text."
        )
        response = get_gemini_response(input_text, image_prompt)
        
        st.subheader("Analysis of your utopia by Google Generative AI")
        
        # Split the analysis into paragraphs and subtitles
        paragraphs = response.split('\n\n')
        for paragraph in paragraphs:
            if ': ' in paragraph:
                subtitle, text = paragraph.split(': ', 1)
                st.markdown(f"**{subtitle}**")
                st.write(text)
            else:
                st.write(paragraph)
    
    except Exception as e:
        st.error(f"Error in analysis or image generation: {str(e)}")

st.markdown('</div>', unsafe_allow_html=True)
