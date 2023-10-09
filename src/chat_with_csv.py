import streamlit as st
import tempfile
from dataclasses import dataclass
from typing import Literal
from langchain.llms import OpenAI
from langchain.agents import create_csv_agent
from constants import CURRENT_PATH

@dataclass
class Message:
    """Class for keeping track of a chat message."""
    origin: Literal["human", "ai"]
    message: str

def load_css():
    with open("static/styles.css", "r") as f:
        css = f"<style>{f.read()}</style>"
        st.markdown(css, unsafe_allow_html=True)

def initialize_session_state(agent: OpenAI):
    if "history" not in st.session_state:
        st.session_state.history = []
    if "conversation" not in st.session_state:
        st.session_state.conversation = agent

def on_click_callback(agent: OpenAI):
    human_prompt = st.session_state.human_prompt
    llm_response = st.session_state.conversation.run(human_prompt)
    st.session_state.history.append(
        Message("human", human_prompt)
    )
    st.session_state.history.append(
        Message("ai", llm_response)
    )

def create_temporary_file(file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_file:
        temp_file.write(file.getvalue())
    return temp_file.name

def create_agent(tempFile):
    agent = create_csv_agent(
        llm=OpenAI(temperature=0, openai_api_key=st.secrets["openai_api_key"]), path=tempFile,
        verbose=True
    )
    return agent

def chatWithCSV(csv_file):
    tempFile = create_temporary_file(csv_file)
    agent = create_agent(tempFile=tempFile)

    load_css()
    initialize_session_state(agent=agent)

    chat_placeholder = st.container()
    prompt_placeholder = st.form("chat-form")

    with chat_placeholder:
        for chat in st.session_state.history:
            div = f"""
    <div class="chat-row 
        {'' if chat.origin == 'ai' else 'row-reverse'}">
        <img class="chat-icon" src="{CURRENT_PATH}/assets/{
            'bot.png' if chat.origin == 'ai' 
                        else 'user.png'}"
            width=32 height=32>
        <div class="chat-bubble
        {'ai-bubble' if chat.origin == 'ai' else 'human-bubble'}">
            &#8203;{chat.message}
        </div>
    </div>
            """
            st.markdown(div, unsafe_allow_html=True)
        
        for _ in range(3):
            st.markdown("")

    with prompt_placeholder:
        st.markdown("**Chat**")
        cols = st.columns((6, 1))
        cols[0].text_input(
            "Chat",
            value="",
            label_visibility="collapsed",
            key="human_prompt",
        )
        cols[1].form_submit_button(
            "Submit", 
            type="primary", 
            on_click=lambda: on_click_callback(agent)
        )

