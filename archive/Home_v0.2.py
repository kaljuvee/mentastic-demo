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

# Main Streamlit App Layout
st.title("Mentastic AI Demo")

# Create three columns for sample questions
col1, col2, col3 = st.columns(3)

# Sample questions in each column
with col1:
    if st.button("How would I manage my stress?"):
        st.text_area("Ask me a question:", "How would I manage my stress?")

with col2:
    if st.button("Help me understand why I feel tired"):
        st.text_area("Enter your message to the chatbot:", "Help me understand a technical document.")

with col3:
    if st.button("What's in the news in Tokyo today?"):
        st.text_area("Enter your message to the chatbot:", "What's in the news in Tokyo today?")

# Hide user and session IDs for simplicity
user_id = "user123"
session_id = "session456"

# Get user input
user_input = st.text_area("Enter your message to the chatbot:")

# Send button
if st.button("Send"):
    response = chatbot_interaction(user_input, user_id, session_id)
    st.json(response)
