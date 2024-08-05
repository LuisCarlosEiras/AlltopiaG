from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
import pathlib
import textwrap
from PIL import Image
import google.generativeai as genai

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_response(question):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(question)
    return response.text

def get_gemini_response_image(input,image):
    model = genai.GenerativeModel('gemini-pro-vision')
    if input!="":
       response = model.generate_content([input,image])
    else:
       response = model.generate_content(image)
    return response.text

with st.sidebar:
    st.header("Text as input")
    text_input_prompt =st.text_input("Enter the prompt: ",key="input")
    st.markdown("<h1 style='text-align: center;'>(or)</h1>", unsafe_allow_html=True)
    img_input_prompt =st.text_input("Enter the prompt: ",key="input1")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    image="" 
    submit=st.button("Generate response")


if submit:
    if text_input_prompt:
        response=get_gemini_response(text_input_prompt)
        st.subheader("Generated response:")
        st.write(response)
    elif uploaded_file:
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image.", use_column_width=True)
        st.subheader("Generated response:")
        response=get_gemini_response_image(img_input_prompt,image)
        st.write(response)
