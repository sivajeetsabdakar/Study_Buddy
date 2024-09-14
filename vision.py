from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

load_dotenv()

os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get the gemini response
def get_gemini_response(input, image):
    model = genai.GenerativeModel('gemini-1.5-flash')
    if input != "":
        response = model.generate_content([input, image])
    else:
        response = model.generate_content(image)
    return response.text

# Streamlit page configuration
st.set_page_config(page_title="AI Image Chatbot")

st.header("I'm your study buddy :)")

# Load chat history from session state
if 'history' not in st.session_state:
    st.session_state['history'] = []

# Input field for text and file upload for image
input = st.text_input("What is your doubt?: ", key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Initialize image variable
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

# Create two side-by-side columns for "Send" button and "Chat History" dropdown
col1, col2 = st.columns([3, 1])

# Submit button
with col1:
    submit = st.button("Send")

# Chat history dropdown (expander)
with col2:
    with st.expander("Chat History"):
        if st.session_state['history']:
            for chat in st.session_state['history']:
                st.write(f"**You**: {chat['input']}")
                st.write(f"**StudyBuddy**: {chat['response']}")

# When the submit button is clicked
if submit:
    response = get_gemini_response(input, image)
    
    # Store the question and response in session state
    st.session_state['history'].append({
        'input': input,
        'response': response
    })
    
    # Display the response
    st.subheader("The Response is")
    st.write(response)
