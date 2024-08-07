import os
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai
import openai

load_dotenv()

os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
openai.api_key = os.getenv("OPENAI_API_KEY")

# ... (previous code remains unchanged)

# Function to get the API key securely
def get_google_api_key():
    return os.environ.get("GOOGLE_API_KEY")

# Analysis using Google Generative AI and OpenAI DALL-E 3
if st.button("Analyze your society with AI and generate an image"):
    google_api_key = get_google_api_key()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not google_api_key or not openai_api_key:
        st.error("API key(s) not found. Please configure the GOOGLE_API_KEY and OPENAI_API_KEY in the environment variables.")
        st.info("If you're running this locally, you can set the API keys in your system's environment variables.")
    else:
        try:
            genai.configure(api_key=google_api_key)
            model = genai.GenerativeModel('gemini-pro')
            
            # Generate prompt for image
            image_prompt_input = (
                f"Create an image that represents a utopian society with the following characteristics: {values}. "
                "The prompt should have 3 lines of text."
            )
            image_prompt_response = model.generate_content(image_prompt_input)
            image_prompt = image_prompt_response.text
            
            st.subheader("Image Prompt")
            st.write(image_prompt)
            
            # Generate image with DALL-E 3
            try:
                response = openai.Image.create(
                    model="dall-e-3",
                    prompt=image_prompt,
                    size="1024x1024",
                    n=1,
                )
                image_url = response['data'][0]['url']
                
                st.subheader("Generated Image of Your Utopia")
                st.image(image_url, caption="AI-generated representation of your utopia", use_column_width=True)
            except Exception as e:
                st.error(f"Error generating image with DALL-E 3: {str(e)}")
            
            # Generate text analysis
            input_text = (
                f"Analyze the utopian society with the following characteristics: {values}. "
                "Write the analysis with subtitles and 5 paragraphs of text."
            )
            response = model.generate_content(input_text)
            analysis = response.text
            
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
        
        except Exception as e:
            st.error(f"Error calling the AI APIs: {str(e)}")

# ... (rest of the code remains unchanged)
