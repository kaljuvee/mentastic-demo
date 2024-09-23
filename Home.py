import streamlit as st
import requests
import json

BASE_URL = "https://mentasticappserviceai.azurewebsites.net"
CONVERSATION_BLOB_URL = "https://mentasticstorageai.blob.core.windows.net/prompt-data/conversation.txt"
WHO5_BLOB_URL = "https://mentasticstorageai.blob.core.windows.net/prompt-data/who-questions.txt"

# Hide user and session IDs for simplicity
user_id = "user123"
session_id = "session456"

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

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'current_message' not in st.session_state:
    st.session_state.current_message = ""

def display_chat_history():
    for message in st.session_state.messages:
        if message['type'] == 'user':
            st.markdown(f'<div style="text-align: right;"><strong>{message["content"]}</strong></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="text-align: left;">{message["content"]}</div>', unsafe_allow_html=True)

def send_message():
    if st.session_state.current_message:
        # Add user message to chat history
        st.session_state.messages.append({"type": "user", "content": st.session_state.current_message})
        
        # Get response from chatbot
        response = chatbot_interaction(st.session_state.current_message, user_id, session_id)
        
        # Extract and add model's response to chat history
        model_response = response.get("interpreted_response", "Sorry, I couldn't process that.")
        st.session_state.messages.append({"type": "model", "content": model_response})
        
        # Clear current message
        st.session_state.current_message = ""

# Main Streamlit App Layout
st.title("Mentastic AI Demo")

# Create three columns for sample questions
col1, col2, col3 = st.columns(3)

# Sample questions in each column
with col1:
    if st.button("How would I manage my stress?"):
        st.session_state.current_message = "How would I manage my stress?"
        send_message()

with col2:
    if st.button("Help me understand why I feel tired."):
        st.session_state.current_message = "Help me understand why I feel tired."
        send_message()

with col3:
    if st.button("I often feel lonely, can you help me to solve that?"):
        st.session_state.current_message = "I often feel lonely, can you help me to solve that?"
        send_message()

# Display chat history
display_chat_history()

# Get user input
user_input = st.text_input("Your question / reply:", key="user_input", value=st.session_state.current_message)

# Update current_message in session state when input changes
if user_input != st.session_state.current_message:
    st.session_state.current_message = user_input

# Send button
if st.button("Send"):
    send_message()
    st.rerun()

# Refresh button
if st.button("Refresh"):
    st.session_state.messages = []
    st.session_state.current_message = ""
    st.rerun()
