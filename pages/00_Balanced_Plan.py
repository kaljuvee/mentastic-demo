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

# Streamlit UI
st.title("Mentastic AI Retrieve Questions")

# Hide user and session IDs
user_id = "user123"
session_id = "session456"

language = st.text_input("Language Code (default is 'en')", "en")
if st.button("Fetch Questions"):
    response = get_questions(language)
    st.json(response)