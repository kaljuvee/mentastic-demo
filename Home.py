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

# Function to retrieve questions
def get_questions(language="en"):
    endpoint = f"{BASE_URL}/v0/questions"
    params = {"language": language}
    response = requests.get(endpoint, params=params)
    return response.json()

# Function to update metadata
def update_metadata(user_id, metadata):
    endpoint = f"{BASE_URL}/v0/metadata"
    data = {"user_id": user_id, "metadata": metadata}
    response = requests.post(endpoint, json=data)
    return response.json()

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

# Function to fetch the JSON file from Azure Blob Storage
def fetch_blob_file(blob_url):
    response = requests.get(blob_url)
    if response.status_code == 200:
        return response.text
    else:
        st.error("Failed to fetch the file from Blob Storage.")
        return None

# Streamlit UI
st.title("Mentastic AI Chatbot Interaction")

# Hide user and session IDs
user_id = "user123"
session_id = "session456"

user_input = st.text_area("Enter your message to the chatbot:", "Can you help me manage stress?")
if st.button("Send"):
    response = chatbot_interaction(user_input, user_id, session_id)
    st.json(response)

# Markdown documentation for users
st.markdown("""
## Sample Instructions

### 1. Chatbot Interaction
- **Description:** Send a message to the chatbot and receive a response.
- **Sample Inputs:**
  - **response_text:** "Can you help me manage stress?"
  - **user_id:** "user123"
  - **session_id:** "session456"
  - This will initiate a conversation with the chatbot.
  
### 2. Retrieve Questions
- **Description:** Fetch a list of questions and possible answers.
- **Sample Inputs:**
  - **language:** "en" (default) or "ee" for Estonian
  - This will return questions and potential answers in the selected language.

### 3. Update Metadata
- **Description:** Update or store user-specific metadata.
- **Sample Inputs:**
  - **user_id:** "user123"
  - **metadata:** `{"preferences": {"language": "en", "theme": "dark"}}`
  - This will update the metadata for the user.

### 4. WHO-5 Survey Interaction
- **Description:** Interact with the WHO-5 well-being survey.
- **Sample Inputs:**
  - **user_input:** "I have felt cheerful and in good spirits"
  - **user_id:** "user123"
  - **session_id:** "session456"
  - This will initiate or continue the WHO-5 survey.
            
### API Reference
 - [Mentastic AI API Documentation - Confluence](https://nga.atlassian.net/wiki/spaces/HeBa/pages/3009871873/Mentastic+AI+API+Documentation+for+Front-End+Developers)
""")

st.sidebar.title("Select API Endpoint")
option = st.sidebar.selectbox("Choose endpoint to test", 
                              ["Chatbot Interaction", "Retrieve Questions", "Update Metadata", "WHO-5 Survey"])

user_id = st.text_input("User ID", "user123")
session_id = st.text_input("Session ID", "session456")

if option == "Chatbot Interaction":
    user_input = st.text_area("Enter your message to the chatbot:", "Can you help me manage stress?")
    if st.button("Send"):
        response = chatbot_interaction(user_input, user_id, session_id)
        st.json(response)

elif option == "Retrieve Questions":
    language = st.text_input("Language Code (default is 'en')", "en")
    if st.button("Fetch Questions"):
        response = get_questions(language)
        st.json(response)

elif option == "Update Metadata":
    metadata_input = st.text_area("Enter metadata as JSON:", '{"preferences": {"language": "en", "theme": "dark"}}')
    if st.button("Update Metadata"):
        metadata = eval(metadata_input)  # Convert string input to dictionary
        response = update_metadata(user_id, metadata)
        st.json(response)

elif option == "WHO-5 Survey":
    user_input = st.text_input("Enter your WHO-5 survey input:", "I have felt cheerful and in good spirits")
    if st.button("Send Survey Response"):
        response = who5_survey_interaction(user_input, user_id, session_id)
        st.json(response)

# Fetch and display the file from Azure Blob Storage
# Prompt selection
st.markdown("## Select Prompt File to View")
prompt_option = st.radio(
    "Choose which prompt file to display:",
    ("Conversation Prompt", "WHO5 Prompt")
)

# Display the selected prompt file
if prompt_option == "Conversation Prompt":
    st.markdown("### Conversation Prompt")
    blob_data = fetch_blob_file(CONVERSATION_BLOB_URL)
    if blob_data:
        with st.expander("View Prompt File Content (Markdown)"):
            st.markdown(blob_data)  # Render as markdown
elif prompt_option == "WHO5 Prompt":
    st.markdown("### WHO5 Prompt")
    blob_data = fetch_blob_file(WHO5_BLOB_URL)
    if blob_data:
        with st.expander("View Prompt File Content (Markdown)"):
            st.markdown(blob_data)  # Render as markdown