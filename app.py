import streamlit as st
from groq import Groq

# Title and Description
st.title("Educational Chatbot with Groq API")
st.markdown(
    "This chatbot is designed to help students explore career paths and make informed decisions. "
    "Enter your API key below to start interacting."
)

# Sidebar for API Key Input
api_key = st.sidebar.text_input(
    "Enter your Groq API Key", 
    type="password", 
    placeholder="Your API Key here"
)

# Function to interact with Groq API
def chat_with_groq(user_message, api_key):
    try:
        client = Groq(api_key=api_key)  # Initialize Groq client with user-provided API key
        completion = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are the chatbot for educational purposes, and you will guide students with their career paths."
                },
                {"role": "user", "content": user_message},
            ],
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=True,
            stop=None,
        )
        
        # Collect response chunks
        response = ""
        for chunk in completion:
            response += chunk.choices[0].delta.content or ""
        return response

    except Exception as e:
        return f"Error: {e}"

# Main Chat Interface
if api_key:
    st.subheader("Chat Interface")
    
    # Input box for user query
    user_message = st.text_input("Your question:", placeholder="Type your question here...")
    
    # Send Button
    if st.button("Send"):
        if user_message.strip():
            with st.spinner("Chatbot is responding..."):
                response = chat_with_groq(user_message, api_key)
            st.markdown(f"**Chatbot:** {response}")
        else:
            st.warning("Please enter a valid message.")
else:
    st.warning("Please enter your Groq API key in the sidebar to continue.")

# Footer
st.markdown("---")
st.markdown("**Powered by Groq API**")