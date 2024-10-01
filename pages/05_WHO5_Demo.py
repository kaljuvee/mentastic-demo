import streamlit as st
import requests
import json

BASE_URL = "https://mentasticappserviceai.azurewebsites.net"

# Function to interact with the WHO-5 survey
def who5_survey_interaction(user_input, user_id, session_id):
    endpoint = f"{BASE_URL}/v0/who5"
    data = {
        "user_id": user_id,
        "session_id": session_id,
        "user_input": user_input
    }
    response = requests.post(endpoint, json=data)
    return response.json()

st.markdown("""
## Mentastic AI WHO-5 Demo

### Instructions
- You will be prompted to answer WHO5 standard questions.
- Answer to each question on the scale provided.
""")
# Hide user and session IDs
user_id = "user123"
session_id = "session456"

user_input = st.text_input("Enter your WHO-5 survey input:", "I have felt cheerful and in good spirits")
if st.button("Send Survey Response"):
    response = who5_survey_interaction(user_input, user_id, session_id)
    st.json(response)