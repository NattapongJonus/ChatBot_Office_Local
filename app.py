import streamlit as st
import anthropic
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the page
st.set_page_config(page_title="AI Chatbot", page_icon="🤖")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Page title and description
st.title("🤖 AI Chatbot")
st.write("Chat with an intelligent AI assistant powered by Claude!")

# Sidebar configuration
st.sidebar.header("Chatbot Settings")
temperature = st.sidebar.slider(
    "Creativity Level", 
    min_value=0.0, 
    max_value=1.0, 
    value=0.7, 
    step=0.1
)
max_tokens = st.sidebar.slider(
    "Response Length", 
    min_value=100, 
    max_value=4000, 
    value=1000, 
    step=100
)

# Chat input and message display
def display_chat_messages():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def generate_ai_response(messages):
    try:
        client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in messages
            ]
        )
        
        return response.content[0].text
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Display chat history
display_chat_messages()

# Chat input
if prompt := st.chat_input("Enter your message"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate and display AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_ai_response(st.session_state.messages)
            st.markdown(response)
    
    # Add AI response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Run the app with: streamlit run app.py