import os
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# load the env variables
load_dotenv()  # This os.environ['GROQ_API_KEY'] is replace by this load_dotenv()
# This elimiates the need to put the API key in the code, it automatically reads it from the .env file

#streamlit page setup
st.set_page_config(   # Here we setting up the page configuration
    page_title = "💬 Chatbot",
    page_icon = "🤖", # For this we need to copy some emoji, go to "EmojiDB"
    layout = "centered"
)

st.title("💬 Generative AI Chatbot")
# If we click the run button, it will not get run. The Streamlit applications should be started from the terminal using the command Streamlit
# So, run the name of the script in the VS terminal --> "streamlit run" (makesure the chatbot.py in the same directory)

# Inorder to see the what are the files there in the directory using this command called 'ls'. But it won't show .env file, becoz its a hidden file

# If we still wants to see the .env (hidden file), then use this command called "ls -Force"

# If you want to run this one then use this command --> stramlit run chatbot_groq.py

# Next lets initiate chat history
# chat_history = [] --> just initiating "chat_history" will not remember all the information that whenever we ask one after another question
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [] # This session state will keep all the information until we close the session (re-run the code) 

# show chat history
for message in st.session_state.chat_history: # Chat history is a list and it contains dictionary values
    with st.chat_message(message["role"]):    # It contains two key value pairs. 1) Role & 2) Content
        st.markdown(message["content"])       # It creates human emoji for human response & robot emoji for assistant response

# Initiate the LLM
llm = ChatGroq(
    model = 'llama-3.1-8b-instant',
    temperature = 0.0, # Because we want a similar value
)

# input box
user_prompt = st.chat_input("Ask Chatbot...")

if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    # sending this chat_history to the LLM
    response = llm.invoke(
        input = [{"role": "system", "content": "You are a helpful assitant"}, *st.session_state.chat_history]
    )

    assistant_response = response.content  # This is the LLM response which we will send it to the chat_history
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    with st.chat_message("assistant"):
        st.markdown(assistant_response) # Finally displays an assistant message over here

# Remeber this steps: User_query (input) --> display user_query (at the top) --> save query to chat_history (list of dictionaries) --> 
# --> send the chat_history to LLM (llm.invoke) --> get response from LLM --> save response in chat_history --> diaplay llm reponse

# So the above flow is repetitive until the patient stop giving the response.

