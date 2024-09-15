from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

load_dotenv()

os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, image):
    model = genai.GenerativeModel('gemini-1.5-flash')
    if input != "":
        response = model.generate_content([input, image])
    else:
        response = model.generate_content(image)
    return response.text

st.set_page_config(page_title="Vision Buddy")

st.header("I'm your study buddy, the one with the vision 👀")

if 'history' not in st.session_state:
    st.session_state['history'] = []

input = st.text_input("What's your doubt?: ", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

col1, col2 = st.columns([2, 2])  # Changed column width to make them equal

with col1:
    submit = st.button("Send")

with col2:
    with st.expander("Chat History"):
        if st.session_state['history']:
            for chat in st.session_state['history']:
                st.write(f"**You**: {chat['input']}")
                st.write(f"**StudyBuddy**: {chat['response']}")
    if st.button("Clear History"):  # Moved this inside the same column
        st.session_state['history'] = []

if submit:
    response = get_gemini_response(input, image)
    
    st.session_state['history'].append({
        'input': input,
        'response': response
    })
    
    st.subheader("The Response is")
    st.write(response)
