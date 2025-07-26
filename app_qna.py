import streamlit as st
import requests
import uuid
import time
import re

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="AI RingExpert – RINGS & I",
    page_icon="💍",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    @font-face {
        font-family: 'Oregon';
        src: url('https://cdn.shopify.com/s/files/1/0843/6917/8903/files/OregonLDO-Light.woff2') format('woff2');
        font-weight: 300;
        font-style: normal;
    }
    </style>
""", unsafe_allow_html=True)

is_embed = "embed" in st.query_params

# --- CUSTOM CSS FOR UI ---
st.markdown("""
<style>
/* === Reset & Layout === */
#MainMenu, footer, header {visibility: hidden;}
html, body {
    overflow-x: hidden !important;
    background-color: white !important;
    background-image: url("https://cdn.shopify.com/s/files/1/0843/6917/8903/files/your-faded-logo.png");
    background-repeat: no-repeat;
    background-position: center;
    background-size: 70%;
    font-family: 'Oregon', 'Georgia', serif !important;
}
.stButton>button {
    all: unset;
    width: 100% !important;
    min-height: 36px !important;
    padding: 6px 10px !important;
    font-size: 11px !important;
    font-family: 'Oregon', serif !important;
    font-weight: 500 !important;
    color: black !important;
    text-align: center !important;
    background-color: white !important;
    border-radius: 16px !important;
    border: 1.3px solid black !important;
    box-shadow: 2px 2px 0px #444 !important;
    display: flex !important;
    justify-content: center;
    align-items: center;
    transition: 0.15s ease-in-out;
    word-break: break-word;
    line-height: 1.3;
}
.stButton>button:hover {
    background-color: #c9a45d !important;
    color: white !important;
    box-shadow: 2px 2px 0px #c9a45d !important;
}
.chat-title {
    font-size: 17px;
    font-weight: bold;
    margin: 16px 0 4px 0;
    text-align: center;
}
.helper-text {
    font-size: 12px;
    color: #777;
    text-align: center;
    margin-bottom: 16px;
}
.stChatMessage {
    font-size: 13.5px;
    line-height: 1.5;
}
[data-testid="stChatInput"] {
    border: 1px solid #c9a45d !important;
    border-radius: 10px !important;
    padding: 4px !important;
    max-width: 440px;
    margin: 0 auto 10px auto !important;
}
[data-testid="stChatInput"] input {
    padding: 8px 10px !important;
    border-radius: 8px !important;
    font-size: 12px !important;
}
@media (prefers-color-scheme: dark) {
    html, body {
        background-color: white !important;
        color: black !important;
    }
    [data-testid="stChatInput"] > div {
        background-color: white !important;
    }
}
</style>
""", unsafe_allow_html=True)

# --- API CONFIG ---
CHAT_API_URL = "https://ringexpert-backend.azurewebsites.net/ask"

if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_id" not in st.session_state:
    st.session_state.user_id = f"guest_{uuid.uuid4().hex[:8]}"

@st.cache_data(show_spinner=False)
def get_cached_response(question):
    response = requests.post(CHAT_API_URL, json={"question": question}, timeout=10)
    response.raise_for_status()
    answer = response.json().get("answer", "Sorry, I didn't understand that.")
    return re.sub(r'\[?doc\d+\]?[:.]?', '', answer, flags=re.IGNORECASE).strip()

def stream_response(text):
    placeholder = st.empty()
    full = ""
    for word in text.split():
        full += word + " "
        placeholder.markdown(full + "▌")
        time.sleep(0.02)
    placeholder.markdown(full)

def handle_message(msg):
    st.session_state.messages.append({"role": "user", "content": msg})
    with st.chat_message("user"):
        st.markdown(msg)
    try:
        answer = get_cached_response(msg)
        with st.chat_message("assistant"):
            stream_response(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
    except Exception as e:
        err = f"⚠ Error: {str(e)}"
        st.session_state.messages.append({"role": "assistant", "content": err})
        with st.chat_message("assistant"):
            st.error(err)

# --- UI ---
if not is_embed:
    st.markdown("<h5 class='chat-title'>Want to know more about RINGS & I?</h5>", unsafe_allow_html=True)
    st.markdown("<p class='helper-text'>Tap a Button or Start Typing</p>", unsafe_allow_html=True)

    rows = [
        ["What Is RINGS & I?", "Where Is Your Studio?"],
        ["Natural or Lab-Grown Diamonds?", "What's the Price Range?"],
        ["Which Metals Do You Use?", "💍 Ring Styles"],
        ["Ring Making & Delivery Time?", "Can I Customize My Ring?"],
        ["Do You Have Ready-to-Buy Rings?", "How Can I Book an Appointment?"]
    ]

    for r in rows:
        cols = st.columns(2)
        for i in range(2):
            with cols[i]:
                if st.button(r[i], key=f"btn_{r[i]}"):
                    handle_message(r[i])

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if user := st.chat_input("Type anything..."):
    handle_message(user)
