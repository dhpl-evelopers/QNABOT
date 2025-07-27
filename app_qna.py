
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

# --- CUSTOM FONTS & GLOBAL STYLE ---
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
    .button-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 12px;
        max-width: 420px;
        margin: 0 auto 24px auto;
        padding: 0 12px;
    }
    .stButton>button {
        font-family: 'Oregon', serif !important;
        font-size: 10px !important;
        font-weight: 500 !important;
        border-radius: 12px !important;
        padding: 10px 10px !important;
        min-height: 40px !important;
        line-height: 1.3 !important;
        white-space: pre-line !important;
        word-break: break-word !important;
        box-shadow: 2px 2px 0px #aaa !important;
        background-color: white !important;
        color: black !important;
        border: 1px solid #ccc !important;
        text-align: center !important;
    }
    .stButton>button:hover {
        background: #c9a45d !important;
        color: white !important;
        transform: translateY(-1px);
    }
    @media (max-width: 480px) {
        .button-grid {
            grid-template-columns: repeat(2, 1fr);
            gap: 8px !important;
            max-width: 320px !important;
        }
        .stButton>button {
            font-size: 9px !important;
            padding: 6px 4px !important;
        }
    }
    </style>
""", unsafe_allow_html=True)

# --- API CONFIG ---
CHAT_API_URL = "https://ringexpert-backend.azurewebsites.net/ask"

# --- SESSION INIT ---
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
    cleaned = re.sub(r'\[?doc\d+\]?[:.]?', '', answer, flags=re.IGNORECASE)
    return cleaned.strip()

# --- HANDLE CHAT ---
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

# --- UI TITLE ---
st.markdown('<div class="chat-title">Want to know more about RINGS & I?</div>', unsafe_allow_html=True)
st.markdown('<div class="helper-text">Tap a button or Start Typing</div>', unsafe_allow_html=True)

# --- QUESTIONS with \n line breaks ---
# --- Replace your questions array and button grid section with this ---

# Questions with explicit line breaks (using HTML <br> tags)
# --- Replace your questions array and button grid section with this optimized version ---

# Questions with explicit line breaks (using \n for Streamlit)
questions = [
    "What Is\nRINGS & I?", "Where Is\nYour Studio?",
    "Natural or\nLab-Grown Diamonds?", "What's the\nPrice Range?",
    "Which Metals\nDo You Use?", "Which Metal\nPurities Do You Offer?",
    "Ring Making &\nDelivery Time?", "Can I Customize\nMy Ring?",
    "Do You Have\nReady-to-Buy Rings?", "How Can I Book\nan Appointment?"
]

# Button grid implementation
with st.container():
    for i in range(0, len(questions), 2):
        cols = st.columns(2)
        for j in range(2):
            if i + j < len(questions):
                clean_question = questions[i + j].replace("\n", " ")
                if cols[j].button(questions[i + j], key=f"btn_{i+j}"):
                    handle_message(clean_question)

# Enhanced button styling
st.markdown("""
<style>
    /* Base container adjustments */
    .main .block-container {
        padding: 1rem 1rem 0;
        max-width: 420px;
        margin: 0 auto;
    }
    
    /* Title styling */
    .chat-title {
        font-size: 20px;
        margin-bottom: 8px;
    }
    .helper-text {
        font-size: 13px;
        margin-bottom: 20px;
    }
    
    /* Button styling - exact prototype match */
    .stButton>button {
        font-family: 'Oregon', serif !important;
        font-size: 12px !important;
        font-weight: 500 !important;
        border-radius: 12px !important;
        padding: 14px 8px !important;
        min-height: 70px !important;
        line-height: 1.35 !important;
        white-space: pre-line !important;
        box-shadow: 2px 2px 4px rgba(0,0,0,0.1) !important;
        background-color: white !important;
        color: black !important;
        border: 1px solid #ddd !important;
        text-align: center !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        margin: 0 auto 8px auto !important;
        width: 100% !important;
    }

    /* Hover state */
    .stButton>button:hover {
        background: #c9a45d !important;
        color: white !important;
        transform: translateY(-1px);
        box-shadow: 2px 3px 6px rgba(0,0,0,0.15) !important;
    }

    /* Grid layout */
    .stButton {
        padding: 0 6px !important;
    }

    /* Mobile adjustments */
    @media (max-width: 480px) {
        .stButton>button {
            font-size: 11px !important;
            min-height: 60px !important;
            padding: 10px 6px !important;
        }
    }
</style>
""", unsafe_allow_html=True)

is_embedded = st.query_params.get("embed") == "1"



if is_embedded:
    st.markdown('</div>', unsafe_allow_html=True)
# Handle message passing from iframe
if st.query_params.get("embed") == "1":
    from streamlit.components.v1.components import CustomComponent
    class IframeMessenger(CustomComponent):
        def __init__(self):
            super().__init__()
            self.js = """
            window.addEventListener('message', (event) => {
                if (event.data.type === 'buttonClick') {
                    window.parent.postMessage({
                        type: 'buttonClicked',
                        message: event.data.message
                    }, '*');
                }
            });
            """
    IframeMessenger()



# --- CHAT HISTORY ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- INPUT BOX ---
if user_input := st.chat_input("Type Anything..."):
    handle_message(user_input)
