import streamlit as st
import requests

BASE_URL = "https://mentasticappserviceai.azurewebsites.net"
language = "en"

def get_questions(language="en"):
    endpoint = f"{BASE_URL}/v0/questions"
    params = {"language": language}
    response = requests.get(endpoint, params=params)
    return response.json()

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
if 'questions' not in st.session_state:
    st.session_state.questions = get_questions(language)['questions']
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
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
        response = chatbot_interaction(st.session_state.current_message, "user123", "session456")
        
        # Extract and add model's response to chat history
        model_response = response.get("interpreted_response", "Sorry, I couldn't process that.")
        st.session_state.messages.append({"type": "model", "content": model_response})
        
        # Move to next question if not at the end
        if st.session_state.current_question < len(st.session_state.questions) - 1:
            st.session_state.current_question += 1
        
        # Clear current message
        st.session_state.current_message = ""

# Main Streamlit App Layout
st.title("Mentastic AI Balanced Plan Demo")

if st.session_state.current_question < len(st.session_state.questions):
    question = st.session_state.questions[st.session_state.current_question]
    st.subheader(f"Question {st.session_state.current_question + 1} of {len(st.session_state.questions)}:")
    st.write(question['question'])
    st.write("Answer options:")
    for i, answer in enumerate(question['answers']):
        st.write(f"{i + 1}. {answer}")
else:
    st.success("All questions have been presented.")

# Display progress
progress = st.session_state.current_question / len(st.session_state.questions)
st.progress(progress)

# Reset button for questionnaire
if st.button("Refresh questions"):
    st.session_state.current_question = 0
    st.rerun()

# Display chat history
display_chat_history()

# Get user input
user_input = st.text_input("Your reply:", key="user_input", value=st.session_state.current_message)

# Update current_message in session state when input changes
if user_input != st.session_state.current_message:
    st.session_state.current_message = user_input

# Send and Clear Chat buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("Reply"):
        send_message()
        st.rerun()

with col2:
    if st.button("Clear"):
        st.session_state.messages = []
        st.session_state.current_message = ""
        st.rerun()