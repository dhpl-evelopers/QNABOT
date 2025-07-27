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

# --- CUSTOM STYLING ---
# --- CUSTOM STYLING ---
# --- CUSTOM STYLING ---
# --- CUSTOM STYLING ---
st.markdown("""
<style>
    @font-face {
        font-family: 'Oregon';
        src: url('https://cdn.shopify.com/s/files/1/0843/6917/8903/files/OregonLDO-Light.woff2') format('woff2');
        font-weight: 300;
        font-style: normal;
    }
    
    /* Base container - strict width control */
    .main .block-container {
        padding: 4px !important;
        width: 320px !important;
        min-width: 320px !important;
        max-width: 320px !important;
        margin: 0 auto !important;
    }
    
    /* Nuclear column lock */
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        width: 100% !important;
    }
    
    div[data-testid="column"] {
        flex: 0 0 50% !important;
        min-width: 50% !important;
        max-width: 50% !important;
        width: 50% !important;
        box-sizing: border-box !important;
        padding: 0 3px !important;
    }
    
    /* Button styling */
    .stButton {
        width: 100% !important;
        margin: 0 !important;
    }
    
    .stButton > button {
        font-size: 8px !important;
        min-height: 32px !important;
        padding: 2px !important;
        margin: 2px 0 !important;
        white-space: normal !important;
        word-break: break-word !important;
        width: 100% !important;
    }
    
    /* Mobile adjustments */
    @media (max-width: 480px) {
        .stButton > button {
            font-size: 7px !important;
            min-height: 28px !important;
        }
    }
</style>
""", unsafe_allow_html=True)



# --- UI COMPONENTS ---
# Shortened questions for mobile compatibility

# --- API CONFIG ---
CHAT_API_URL = "https://ringexpert-backend.azurewebsites.net/ask"

# --- SESSION INIT ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_id" not in st.session_state:
    st.session_state.user_id = f"guest_{uuid.uuid4().hex[:8]}"

# --- MESSAGE HANDLING ---
def stream_response(text):
    message_placeholder = st.empty()
    full_response = ""
    for word in text.split():
        full_response += word + " "
        message_placeholder.markdown(full_response + "▌")
        time.sleep(0.02)
    message_placeholder.markdown(full_response)

@st.cache_data(show_spinner=False)
def get_cached_response(question):
    response = requests.post(CHAT_API_URL, json={"question": question}, timeout=10)
    response.raise_for_status()
    answer = response.json().get("answer", "Sorry, I didn't understand that.")
    return re.sub(r'\[?doc\d+\]?[:.]?', '', answer, flags=re.IGNORECASE).strip()

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
        st.session_state.messages.append({"role": "assistant", "content": str(e)})
        st.error(str(e))

# --- UI COMPONENTS ---
st.markdown('<div class="chat-title">Want to know more about RINGS & I?</div>', unsafe_allow_html=True)
st.markdown('<div class="helper-text">Tap a button or Start Typing</div>', unsafe_allow_html=True)

# Ultra-compact questions
questions = [
    "About", "Location",
    "Diamonds", "Prices", 
    "Metals", "Options",
    "Time", "Custom",
    "Ready", "Book"
]

# Create columns with forced layout
col1, col2 = st.columns(2)
for i, question in enumerate(questions):
    with (col1 if i % 2 == 0 else col2):
        if st.button(question, key=f"btn_{i}"):
            handle_message(question)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- INPUT BOX ---
if user_input := st.chat_input("Type Anything..."):
    handle_message(user_input)
