import streamlit as st
import requests
import json

BASE_URL = "https://mentasticappserviceai.azurewebsites.net"

# Function to retrieve questions
def get_questions(language="en"):
    endpoint = f"{BASE_URL}/v0/questions"
    params = {"language": language}
    response = requests.get(endpoint, params=params)
    return response.json()

st.markdown("""
## Mentastic AI Mental Wellbeing Balanced Plan Demo

### Instructions
- You will be prompted to answer a series of questions.
- Answer to each question on the format provided.
""")

# Hide user and session IDs
user_id = "user123"
session_id = "session456"

language = st.text_input("Language Code (default is 'en')", "en")
if st.button("Fetch Questions"):
    response = get_questions(language)
    st.json(response)