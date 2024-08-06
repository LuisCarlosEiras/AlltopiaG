import os
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai

load_dotenv()

os.getenv("GOOGLE_API_KEY")
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

# Full-width analysis section
st.markdown('<div class="full-width-section">', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Analysis of your utopia</p>', unsafe_allow_html=True)
st.write(f"Average of Values: {average:.2f}")
st.write(f"Classification: {analysis}")

# Function to get the API key securely
def get_google_api_key():
    return os.environ.get("GOOGLE_API_KEY")

# Analysis using Google Generative AI
if st.button("Analyze your society with Google Generative AI"):
    api_key = get_google_api_key()
    if not api_key:
        st.error("Google API key not found. Please configure the GOOGLE_API_KEY in the environment variables.")
        st.info("If you're running this locally, you can set the API key in your system's environment variables.")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-pro')
            
            input_text = (
                f"Analyze the utopian society with the following characteristics: {values}. "
                "Write the analysis with subtitles and 5 paragraphs of text."
            )
            response = model.generate_content(input_text)
            analysis = response.text
            
            # Generate prompt for image
            image_prompt_input = (
                f"Create an image that represents a utopian society with the following characteristics: {values}. "
                "The prompt should have 3 lines of text."
            )
            image_prompt_response = model.generate_content(image_prompt_input)
            image_prompt = image_prompt_response.text
            
            st.subheader("Analysis of your utopia by Google Generative AI")
            
            # Split the analysis into paragraphs and subtitles
            paragraphs = analysis.split('\n\n')
            for paragraph in paragraphs:
                if ': ' in paragraph:
                    subtitle, text = paragraph.split(': ', 1)
                    st.markdown(f"**{subtitle}**")
                    st.write(text)
                else:
                    st.write(paragraph)
            
            st.subheader("Image Prompt")
            st.write(image_prompt)
            st.write("Note: Image generation is not available with Google Generative AI. You may need to use a separate image generation service or provide a placeholder image.")
        
        except Exception as e:
            st.error(f"Error calling the Google Generative AI API: {str(e)}")

st.markdown('</div>', unsafe_allow_html=True)

# Utopia vs Reality section
st.subheader("Utopia vs Reality")

if st.button("Compare your utopia with the best countries' indices"):
    api_key = get_google_api_key()
    if not api_key:
        st.error("Google API key not found. Please configure the GOOGLE_API_KEY in the environment variables.")
        st.info("If you're running this locally, you can set the API key in your system's environment variables.")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-pro')
            
            comparison_prompt = (
                f"Compare the utopian society with these characteristics: {values}\n"
                "to the highest Human Development Index (HDI) of the following countries: "
                "Norway – 0.957, Switzerland and Ireland – 0.955, "
                "Hong Kong (China) and Iceland - 0.949, Germany – 0.947, "
                "Sweden – 0.945, Australia and Netherlands – 0.944, "
                "Denmark -0.940, Singapore and Finland – 0.938, "
                "New Zealand and Belgium – 0.931, Canada – 0.929, United States – 0.926. "
                "Write the comparison in exactly two paragraphs, each with 10 lines."
            )
            
            comparison_response = model.generate_content(comparison_prompt)
            comparison_text = comparison_response.text
            
            st.subheader("Comparison with Real-World Indices")
            
            # Split the comparison text into paragraphs
            paragraphs = comparison_text.split('\n\n')
            
            # Ensure we have exactly two paragraphs
            if len(paragraphs) >= 2:
                st.write(paragraphs[0])
                st.write(paragraphs[1])
            else:
                st.write(comparison_text)
        
        except Exception as e:
            st.error(f"Error calling the Google Generative AI API: {str(e)}")
