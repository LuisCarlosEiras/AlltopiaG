import os
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Google Generative AI API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

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

# CSS style for title, subtitles, and centered image
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

# Full-width title
st.markdown('<p class="full-width-title">Alltopia, the game</p>', unsafe_allow_html=True)

# Subtitle
st.markdown('<p class="subtitle">Create your perfect society</p>', unsafe_allow_html=True)

# Function to analyze society based on adjusted values
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

# Split the screen into two equal-sized columns
col1, col2 = st.columns(2)

# Create sliders for each characteristic in the left column
with col1:
    st.markdown('<p class="subtitle">Choose the characteristics</p>', unsafe_allow_html=True)
    for characteristic in characteristics:
        values[characteristic] = st.slider(characteristic, 0.0, 10.0, 5.0)
    
    # Full-width analysis section below the sliders
    st.markdown('<div class="full-width-section">', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Analysis of your utopia</p>', unsafe_allow_html=True)
    average, analysis = analyze_society(values)
    st.write(f"Average of Values: {average:.2f}")
    st.write(f"Classification: {analysis}")
    st.markdown('</div>', unsafe_allow_html=True)

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

# Function to get the Google API key securely
def get_google_api_key():
    return os.environ.get("GOOGLE_API_KEY")

# Analysis using Google Generative AI for text and image
if st.button("Analyze your society with AI"):
    api_key = get_google_api_key()
    if not api_key:
        st.error("Google API key not found. Please configure the GOOGLE_API_KEY in the environment variables.")
        st.info("If you're running this locally, you can set the API key in your system's environment variables.")
    else:
        try:
            genai.configure(api_key=api_key)
            
            # Text analysis
            text_model = genai.GenerativeModel('gemini-pro')
            text_prompt = (
                f"Analyze the utopian society with the following characteristics: {values}. "
                "Write the analysis with 5 paragraphs of text."
            )
            text_response = text_model.generate_content(text_prompt)
            google_analysis = text_response.text
            
            # Image generation
            vision_model = genai.GenerativeModel('gemini-1.5-flash')
            image_prompt = (
                f"Create an image representing a utopian society with the following characteristics: {values}. "
                "The image should be vibrant and detailed, showcasing various aspects of this utopian society. "
                "Use a style that combines realism with elements of fantasy to capture the idealized nature of the society."
            )
            image_response = vision_model.generate_content(image_prompt)
            
            # Display the generated image
            if image_response.parts:
                image = image_response.parts[0].image_bytes
                st.markdown('<div class="centered-image">', unsafe_allow_html=True)
                st.image(image, width=716)  # 70% of 1024 is approximately 716
                st.markdown('</div>', unsafe_allow_html=True)
            
            st.subheader("Analysis of your utopia by Google Generative AI")
            
            # Split the analysis into paragraphs
            paragraphs = google_analysis.split('\n\n')
            for paragraph in paragraphs:
                st.write(paragraph)
        
        except Exception as e:
            st.error(f"Error calling the Google Generative AI API: {str(e)}")

# Final notice
st.markdown("""
<div style="text-align: center; padding: 20px; background-color: #f0f2f6; margin-top: 30px;">
    <p>Adjust the characteristics above to generate a new utopian society</p>
</div>
""", unsafe_allow_html=True)
