
import streamlit as st
import requests
import uuid
import time
import re

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="AI RingExpert – RINGS & I",
    page_icon="💍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- EMBED DETECTION ---
query_params = st.query_params
is_embed = query_params.get("embed", ["0"])[0] == "1"

# --- CUSTOM STYLES ---
st.markdown("""
<style>
    @font-face {
        font-family: 'Oregon';
        src: url('https://cdn.shopify.com/s/files/1/0843/6917/8903/files/OregonLDO-Light.woff2') format('woff2');
        font-weight: 300;
        font-style: normal;
    }
    html, body, div, input, textarea, button {
        font-family: 'Oregon', 'Georgia', serif !important;
        background-color: #ffffff;
        color: #000000;
    }
    .chat-title, .helper-text, .stChatMessage {
        font-family: 'Oregon', serif !important;
    }
    [data-testid="stChatInput"] input {
        font-family: 'Oregon', serif;
        border-radius: 10px;
        border: 1px solid #c9a45d !important;
    }
    #MainMenu, footer, header {visibility: hidden;}
    html, body {
        overflow-x: hidden !important;
        width: 100% !important;
    }
    .block-container {
        padding-top: 0 !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
    .chat-title {
        font-size: 20px;
        font-weight: 600;
        margin: 16px 0 8px 0;
        text-align: center;
    }
    .helper-text {
        font-size: 13px;
        text-align: center;
        margin-bottom: 20px;
        color: #555555;
    }
    .stChatMessage {
        font-size: 15px;
        line-height: 1.6;
    }
    [data-testid="stChatInput"] {
        border: 1px solid #c9a45d !important;
        border-radius: 12px !important;
        padding: 8px !important;
        max-width: 600px !important;
        margin: 0 auto !important;
    }
    [data-testid="stChatInput"] input {
        border-radius: 10px !important;
        padding: 10px 12px !important;
    }
    @media (prefers-color-scheme: dark) {
        html, body, button, input, textarea {
            background-color: #ffffff !important;
            color: #000000 !important;
        }
        [data-testid="stChatInput"] > div {
            background-color: #ffffff !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# --- API CONFIG ---
CHAT_API_URL = "https://ringexpert-backend.azurewebsites.net/ask"

# --- SESSION INITIALIZATION ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_id" not in st.session_state:
    st.session_state.user_id = f"guest_{uuid.uuid4().hex[:8]}"

# --- STREAM RESPONSE ---
def stream_response(text):
    message_placeholder = st.empty()
    full_response = ""
    for word in text.split():
        full_response += word + " "
        message_placeholder.markdown(full_response + "▌")
        time.sleep(0.02)
    message_placeholder.markdown(full_response)

# --- API CALL ---
@st.cache_data(show_spinner=False)
def get_cached_response(question):
    response = requests.post(CHAT_API_URL, json={"question": question}, timeout=10)
    response.raise_for_status()
    answer = response.json().get("answer", "Sorry, I didn't understand that.")
    cleaned = re.sub(r'\[?doc\d+\]?[.:]?', '', answer, flags=re.IGNORECASE)
    return cleaned.strip()

# --- MESSAGE HANDLER ---
def handle_message(message):
    st.session_state.messages.append({"role": "user", "content": message})
    with st.chat_message("user"):
        st.markdown(message)

    try:
        answer = get_cached_response(message)
        with st.chat_message("assistant"):
            stream_response(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
    except Exception as e:
        error_msg = f"⚠ Error: {str(e)}"
        st.session_state.messages.append({"role": "assistant", "content": error_msg})
        with st.chat_message("assistant"):
            st.error(error_msg)

# --- UI HEADINGS ---
st.markdown('<div class="chat-title">Want to know more about RINGS & I?</div>', unsafe_allow_html=True)
st.markdown('<div class="helper-text">Tap a Button or Start Typing</div>', unsafe_allow_html=True)

# --- QUESTION BUTTONS (CSS grid layout) ---
questions = [
    "What Is RINGS & I?", "Where Is Your Studio?",
    "Natural or Lab-Grown Diamonds?", "What's the Price Range?",
    "Which Metals Do You Use?", "Which Metal Purities Do You Offer?",
    "Ring Making & Delivery Time?", "Can I Customize My Ring?",
    "Do You Have Ready-to-Buy Rings?", "How Can I Book an Appointment?"
]

st.markdown('<div class="grid-container">', unsafe_allow_html=True)
for i, question in enumerate(questions):
    if st.button(question, key=f"btn_{i}"):
        handle_message(question)
st.markdown('</div>', unsafe_allow_html=True)

# --- CHAT HISTORY ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- EMBED CSS FIX ---
if is_embed:
    st.markdown("""
        <style>
        .block-container {
            padding: 1rem !important;
            max-width: 440px !important;
            margin: 0 auto !important;
        }
        .grid-container {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 12px;
            max-width: 440px;
            margin: 0 auto 24px auto;
        }
        .stButton>button {
            width: 100% !important;
            font-family: 'Oregon', serif !important;
            font-size: 11.5px !important;
            font-weight: 500 !important;
            padding: 10px 12px !important;
            border-radius: 12px !important;
            box-shadow: 2px 2px 0px #aaa !important;
            white-space: normal !important;
            background-color: white !important;
            color: black !important;
            border: 1px solid #ccc !important;
        }
        .stButton>button:hover {
            background-color: #c9a45d !important;
            color: white !important;
        }
        </style>
    """, unsafe_allow_html=True)

# --- CHAT INPUT ---
if user_input := st.chat_input("Type Anything..."):
    handle_message(user_input)
