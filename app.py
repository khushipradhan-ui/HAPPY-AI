import os
from pathlib import Path
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# Load .env from the exact same directory as app.py
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Happy Bot",
    page_icon="🌷",
    layout="centered"
)

# --- CUTE, GIRLY & LIGHT GREEN CUSTOM CSS (DARK-MODE PROOF) ---
st.markdown("""
<style>
    /* Main app background and default text color */
    .stApp {
        background-color: #F0FFF4 !important;
        color: #1B4332 !important;
    }

    /* Top header bar (removes dark black bar) */
    header[data-testid="stHeader"] {
        background-color: #E2F8E9 !important;
        border-bottom: 1px solid #B7E4C7 !important;
    }

    /* Bottom chat input container (removes dark black footer) */
    [data-testid="stBottom"],
    [data-testid="stBottom"] > div {
        background-color: #E2F8E9 !important;
        border-top: 1px solid #B7E4C7 !important;
    }

    /* Sidebar background and readable dark-green text */
    [data-testid="stSidebar"] {
        background-color: #D8F3DC !important;
        border-right: 2px dashed #74C69D !important;
    }
    [data-testid="stSidebar"] * {
        color: #1B4332 !important;
    }

    /* Sidebar selectbox dropdown styling */
    [data-testid="stSidebar"] [data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border: 2px solid #74C69D !important;
        border-radius: 12px !important;
        color: #1B4332 !important;
    }

    /* Inline code tag in sidebar (.env) */
    [data-testid="stSidebar"] code {
        background-color: #B7E4C7 !important;
        color: #081C15 !important;
        padding: 2px 6px;
        border-radius: 6px;
    }

    /* Header title styling */
    h1 {
        color: #2D6A4F !important;
        font-family: 'Comic Sans MS', 'Chalkboard SE', sans-serif;
        text-align: center;
        text-shadow: 1px 1px 2px #B7E4C7;
    }

    /* Chat message bubbles & crisp readable text */
    [data-testid="stChatMessage"] {
        background-color: #FFFFFF !important;
        border-radius: 20px !important;
        padding: 14px 18px !important;
        margin-bottom: 12px !important;
        border: 2px solid #95D5B2 !important;
        box-shadow: 0 4px 8px rgba(116, 198, 157, 0.25) !important;
    }
    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] li,
    [data-testid="stChatMessage"] span {
        color: #1B4332 !important;
        font-size: 15px !important;
    }

    /* Chat input box & placeholder */
    [data-testid="stChatInput"] {
        background-color: #FFFFFF !important;
        border: 2px solid #52B788 !important;
        border-radius: 25px !important;
    }
    [data-testid="stChatInput"] textarea {
        background-color: #FFFFFF !important;
        color: #1B4332 !important;
        -webkit-text-fill-color: #1B4332 !important;
    }
    [data-testid="stChatInput"] textarea::placeholder {
        color: #52796F !important;
        -webkit-text-fill-color: #52796F !important;
    }
    [data-testid="stChatInput"] button {
        background-color: #95D5B2 !important;
        color: #1B4332 !important;
        border-radius: 50% !important;
    }

    /* Cute buttons */
    .stButton > button {
        background-color: #95D5B2 !important;
        color: #1B4332 !important;
        border-radius: 20px !important;
        border: 2px solid #52B788 !important;
        font-weight: bold !important;
        transition: all 0.2s ease-in-out;
    }
    .stButton > button:hover {
        background-color: #52B788 !important;
        color: #FFFFFF !important;
        transform: scale(1.03);
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.title("🌷✨ Happy Bot ✨🌷")
st.markdown(
    "<p style='text-align: center; color: #2D6A4F; font-size: 16px; font-weight: 500;'>"
    "Your cute little AI bestie powered by OpenRouter & LangChain 💚🎀"
    "</p>",
    unsafe_allow_html=True
)

# --- SIDEBAR SETTINGS ---
with st.sidebar:
    st.header("🌸 Cute Settings 🌸")

    free_models = {
        "OpenRouter Auto Free (Recommended)": "openrouter/free",
        "Llama 3.3 70B (Free)": "meta-llama/llama-3.3-70b-instruct:free",
        "Gemma 3 27B (Free)": "google/gemma-3-27b-it:free",
        "Mistral Small 3.1 (Free)": "mistralai/mistral-small-3.1-24b-instruct:free",
    }
    selected_model_label = st.selectbox(
        "Pick a Free Brain 🧠✨:",
        list(free_models.keys())
    )
    selected_model = free_models[selected_model_label]

    st.markdown("---")
    if st.button("🧹 Clear Chat History"):
        st.session_state.messages = [
            SystemMessage(content="You are Happy Bot, a super cute, friendly, bubbly, and helpful AI assistant. Use cheerful language, occasional cute emojis (like 🌸, ✨, 💚, 🎀), and make the user feel happy while giving accurate, easy-to-understand answers.")
        ]
        st.rerun()

    st.markdown("---")
    st.caption("🔒 Security Check: API key is loaded safely from `.env` and hidden from GitHub.")

# --- VERIFY API KEY ---
api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    st.error("🚨 Oopsie! `OPENROUTER_API_KEY` not found! Please make sure your `.env` file is set up properly.")
    st.stop()

# --- INITIALIZE LANGCHAIN LLM (OPENROUTER) ---
llm = ChatOpenAI(
    model=selected_model,
    openai_api_key=api_key,
    openai_api_base="https://openrouter.ai/api/v1",
    temperature=0.7,
)

# --- CHAT HISTORY STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        SystemMessage(content="You are Happy Bot, a super cute, friendly, bubbly, and helpful AI assistant. Use cheerful language, occasional cute emojis (like 🌸, ✨, 💚, 🎀), and make the user feel happy while giving accurate, easy-to-understand answers.")
    ]

# Display initial greeting if chat is empty
if len(st.session_state.messages) == 1:
    with st.chat_message("assistant", avatar="🧚‍♀️"):
        st.markdown("Hii bestie! 🌸 I'm **Happy Bot**! Ask me anything or just chat with me—how can I brighten your day today? ✨💚")

# Render past chat messages
for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user", avatar="🎀"):
            st.markdown(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant", avatar="🧚‍♀️"):
            st.markdown(msg.content)

# --- USER INPUT & RESPONSE ---
if user_prompt := st.chat_input("Type something sweet here... 💌"):
    st.session_state.messages.append(HumanMessage(content=user_prompt))
    with st.chat_message("user", avatar="🎀"):
        st.markdown(user_prompt)

    with st.chat_message("assistant", avatar="🧚‍♀️"):
        with st.spinner("Thinking sparkly thoughts... ✨"):
            try:
                response = llm.invoke(st.session_state.messages)
                st.markdown(response.content)
                st.session_state.messages.append(AIMessage(content=response.content))
            except Exception as e:
                st.error(f"Aw no! Something went wrong: {e}")