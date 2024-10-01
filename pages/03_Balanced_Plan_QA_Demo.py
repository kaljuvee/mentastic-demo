import streamlit as st
import requests
import uuid

BASE_URL = "https://mentasticappserviceai.azurewebsites.net"

def get_questions(language="en"):
    endpoint = f"{BASE_URL}/v0/questions"
    params = {"language": language}
    response = requests.get(endpoint, params=params)
    return response.json().get("questions", [])

def submit_answers(user_id, answers):
    endpoint = f"{BASE_URL}/v0/submit-answers"
    data = {
        "user_id": user_id,
        "answers": answers
    }
    response = requests.post(endpoint, json=data)
    return response.json()

# Initialize session state
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'answers' not in st.session_state:
    st.session_state.answers = {}

# Main Streamlit App Layout
st.title("Mentastic AI Demo")

if st.session_state.user_id is None:
    email = st.text_input("Please enter your email to start:")
    if st.button("Start"):
        if email:
            st.session_state.user_id = email
            st.session_state.questions = get_questions()
            st.rerun()
        else:
            st.error("Please enter a valid email address.")
else:
    st.write(f"Welcome, {st.session_state.user_id}!")

    if st.session_state.current_question < len(st.session_state.questions):
        question = st.session_state.questions[st.session_state.current_question]
        st.write(question["question"])
        
        answer = st.radio("Choose an answer:", question["answers"], key=f"q_{st.session_state.current_question}")
        
        if st.button("Next"):
            st.session_state.answers[question["question"]] = answer
            st.session_state.current_question += 1
            st.rerun()
    else:
        if st.session_state.answers:
            st.write("Thank you for answering all the questions!")
            if st.button("Submit Answers"):
                response = submit_answers(st.session_state.user_id, st.session_state.answers)
                st.write("Answers submitted successfully!")
                st.json(response)
        else:
            st.write("No answers to submit.")

    # Add a logout button
    if st.button("Logout"):
        st.session_state.user_id = None
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.questions = []
        st.session_state.current_question = 0
        st.session_state.answers = {}
        st.rerun()
