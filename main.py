import openai
import streamlit as st
from streamlit_chat import message

# Load the OpenAI key from the environment variables
openai.api_key = st.secrets["general"]["OPENAI_KEY"]

# Set title of browser
st.set_page_config(page_title='ChatGPT in Hausa, Yoruba and Igbo')


# Set a title
st.title("ChatGPT in Nigeria's major languages")

# Set a description
st.markdown("""
This is a multilingual chatbot that can understand and respond in Yoruba, Hausa, and Igbo. 
To start chatting, select a language from the dropdown and type your message in the input box below.
""")

# Initialize the language_choice with an empty string
language_choice = st.selectbox("Select a language", ["", "Yoruba", "Hausa", "Igbo"])

# Initialize conversation with the system message
st.session_state.setdefault("conversation", [])

if language_choice != "" and len(st.session_state.conversation) == 0:
    st.session_state.conversation = [
        {"role": "system", "content": f"You are a multilingual chatbot that speaks {language_choice}. Use accentations when necessary. Never speak english. Only the choice chosen by the user. Your name is Professor Maye"},
    ]


# Function to send a message
def send_message(user_input):
    # Append the user's message to the conversation
    st.session_state.conversation.append({"role": "user", "content": user_input})

    # Show a loading spinner
    with st.spinner("AI is generating a response..."):
        # Generate a response using OpenAI's GPT-4
        response = openai.ChatCompletion.create(
            model="gpt-4-0314",
            messages=st.session_state.conversation,

        )

    # Extract the assistant's message from the response
    assistant_message = response.choices[0].message['content']

    # Append the assistant's message to the conversation
    st.session_state.conversation.append({"role": "assistant", "content": assistant_message})

    st.experimental_rerun()


# Create a placeholder for the chat messages
chat_placeholder = st.empty()

# Display the conversation history
with chat_placeholder.container():
    for i, msg in enumerate(st.session_state.conversation):
        # Skip the first system message
        if i == 0 and msg["role"] == "system":
            continue

        if msg["role"] == "user":
            message(msg["content"], is_user=True)
        else:
            message(msg["content"], is_user=False)

# Create a new container for the input box and button
with st.container():
    user_input = st.text_input("User Input:", key="user_input")

    # Create a 'send' button next to the input field
    if st.button('Send'):
        send_message(user_input)




