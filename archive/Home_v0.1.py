import streamlit as st
import requests
import json

BASE_URL = "https://mentasticappserviceai.azurewebsites.net"
# Set the base URLs for the Blob storage
CONVERSATION_BLOB_URL = "https://mentasticstorageai.blob.core.windows.net/prompt-data/conversation.txt"
WHO5_BLOB_URL = "https://mentasticstorageai.blob.core.windows.net/prompt-data/who-questions.txt"

# Function to fetch the file from Azure Blob Storage
def fetch_blob_file(blob_url):
    response = requests.get(blob_url)
    if response.status_code == 200:
        return response.text
    else:
        st.error("Failed to fetch the file from Blob Storage.")
        return None

# Function to display the selected prompt
def display_prompt(blob_url):
    blob_data = fetch_blob_file(blob_url)
    if blob_data:
        try:
            # Convert to JSON and make it expandable
            blob_json = json.loads(blob_data)
            with st.expander("View JSON File Content"):
                st.json(blob_json)
        except json.JSONDecodeError:
            st.error("The file content is not valid JSON.")
    else:
        st.error("Unable to load the file from Azure Blob Storage.")

# Function to interact with the chatbot
def chatbot_interaction(user_input, user_id, session_id):
    endpoint = f"{BASE_URL}/v0/chatbot"
    data = {
        "response_text": user_input,
        "user_id": user_id,
        "session_id": session_id
    }
    response = requests.post(endpoint, json=data)
    return response.json()

# Function to fetch the JSON file from Azure Blob Storage
def fetch_blob_file(blob_url):
    response = requests.get(blob_url)
    if response.status_code == 200:
        return response.text
    else:
        st.error("Failed to fetch the file from Blob Storage.")
        return None

st.markdown("""
## Mentastic AI Demo

### Instructions
- Describe how you feel.
- Wait for the AI Agent Therapist to respond.
""")
# Hide user and session IDs
user_id = "user123"
session_id = "session456"

user_input = st.text_area("Enter your message to the chatbot:", "Can you help me manage stress?")
if st.button("Send"):
    response = chatbot_interaction(user_input, user_id, session_id)
    st.json(response)

# Markdown documentation for users
