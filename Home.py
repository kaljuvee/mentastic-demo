import streamlit as st
import requests
import uuid

BASE_URL = "https://mentasticappserviceai.azurewebsites.net"

# Hard-coded questions and answer choices
QUESTIONS = [
    {
        "question": "I'm interested in (select from options):",
        "answer_choice": [
            "Tranquillity",
            "A sense of increased personal value",
            "Bolder communication",
            "Being more alert",
            "Being more interested",
            "Being more relaxed",
            "Better focus",
            "Better self-esteem",
            "Confidence",
            "Greater willpower",
            "I have no such expectations"
        ]
    },
    {
        "question": "Do you have a concern you are looking for a solution to?",
        "answer_choice": [
            "Anxiety",
            "Relationship ending",
            "Sleeping disorders",
            "Restlessness, anxiety",
            "Grief",
            "Difficulties in focusing",
            "Lack of interest",
            "Fear of speaking or communicating",
            "None of these"
        ]
    }
]

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
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'answers' not in st.session_state:
    st.session_state.answers = {}

# Main Streamlit App Layout
st.title("Mentastic AI")

if st.session_state.user_id is None:
    email = st.text_input("Please enter your email to start:")
    if st.button("Start"):
        if email:
            st.session_state.user_id = email
            st.rerun()
        else:
            st.error("Please enter a valid email address.")
else:
    st.write(f"Welcome, {st.session_state.user_id}!")

    if st.session_state.current_question < len(QUESTIONS):
        question = QUESTIONS[st.session_state.current_question]
        st.write(question["question"])
        
        answer = st.radio("Choose an answer:", question["answer_choice"], key=f"q_{st.session_state.current_question}")
        
        if st.button("Next"):
            st.session_state.answers[question["question"]] = answer
            st.session_state.current_question += 1
            st.rerun()
    else:
        if st.session_state.answers:
            st.write("Thank you for answering all the questions!")
            if st.button("Submit Answers"):
                response = submit_answers(st.session_state.user_id, st.session_state.answers)
                st.success("Answers submitted successfully!")
        else:
            st.write("No answers to submit.")

    # Add a logout button
    if st.button("Logout"):
        st.session_state.user_id = None
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.current_question = 0
        st.session_state.answers = {}
        st.rerun()
