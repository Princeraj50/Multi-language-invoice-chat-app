import warnings
warnings.filterwarnings("ignore")

from dotenv import load_dotenv
load_dotenv()  # Take environment variables from .env.

import streamlit as st
import os
import textwrap
from PIL import Image
import google.generativeai as genai

os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load OpenAI model and get responses
def get_gemini_response(input, image, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, image[0], prompt])
    return response.text

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

## Initialize our Streamlit app
st.set_page_config(page_title="Invoice Extractor")

st.markdown(
    """
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .stButton > button {
        width: 100%;
        height: 3em;
        background-color: #007bff;
        color: white;
        font-size: 16px;
        border-radius: 8px;
        border: none;
    }
    .stButton > button:hover {
        background-color: #0056b3;
    }
    .stFileUploader input {
        width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.header("Invoice Reader")

# File uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Display uploaded image
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

# Text input for prompt
input_prompt = st.text_input("Input Prompt:", key="input")

# Submit button
submit = st.button("Submit")

# Image analysis prompt
analysis_prompt = """
               You are an expert in understanding invoices.
               You will receive input images as invoices &
               you will have to answer questions based on the input image.
               """

# Handle form submission
if submit and uploaded_file and input_prompt:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt, image_data, analysis_prompt)
    st.subheader("The Response is")
    st.write(response)
elif submit:
    st.error("Please upload an image and enter a prompt.")
