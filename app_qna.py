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
st.markdown("""
<style>
    @font-face {
        font-family: 'Oregon';
        src: url('https://cdn.shopify.com/s/files/1/0843/6917/8903/files/OregonLDO-Light.woff2') format('woff2');
        font-weight: 300;
        font-style: normal;
    }
    
    /* Base container */
    .main .block-container {
        padding: 0.5rem 0.5rem 1rem;
        max-width: 380px;
    }
    
    /* Header styling */
    .chat-title {
        font-size: 16px;
        font-weight: 600;
        margin: 0 0 6px 0;
        text-align: center;
        color: #000;
    }
    
    .helper-text {
        font-size: 11px;
        text-align: center;
        margin-bottom: 16px;
        color: #555;
    }
    
    /* Button styling - compact version */
    .stButton>button {
        font-family: 'Oregon', serif !important;
        font-size: 10px !important;
        font-weight: 500 !important;
        border-radius: 10px !important;
        padding: 8px 6px !important;
        min-height: 50px !important;
        line-height: 1.3 !important;
        white-space: pre-line !important;
        box-shadow: 1px 1px 3px rgba(0,0,0,0.1) !important;
        background: white !important;
        color: black !important;
        border: 1px solid #ddd !important;
        text-align: center !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        margin: 0 auto 6px !important;
        width: 100% !important;
        transition: all 0.2s ease !important;
    }
    
    .stButton>button:hover {
        background: #c9a45d !important;
        color: white !important;
        transform: translateY(-1px);
        box-shadow: 1px 2px 4px rgba(0,0,0,0.15) !important;
    }
    
    /* Grid layout */
    .stButton {
        padding: 0 4px !important;
    }
    
    /* Chat messages */
    .stChatMessage {
        font-size: 12px !important;
        padding: 8px 12px !important;
    }
    
    /* Input box */
    .stTextInput>div>div>input {
        font-size: 12px !important;
        padding: 8px 12px !important;
    }
    
    /* Mobile adjustments */
    @media (max-width: 480px) {
        .main .block-container {
            padding: 0.5rem 0.25rem 0.75rem;
            max-width: 100%;
        }
        
        .stButton>button {
            font-size: 9px !important;
            min-height: 45px !important;
            padding: 6px 4px !important;
        }
        
        .chat-title {
            font-size: 15px;
        }
        
        .helper-text {
            font-size: 10px;
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

# Define questions list BEFORE using it
questions = [
    "What Is\nRINGS & I?", "Where Is\nYour Studio?",
    "Natural or\nLab-Grown Diamonds?", "What's the\nPrice Range?",
    "Which Metals\nDo You Use?", "Which Metal\nPurities Do You Offer?",
    "Ring Making &\nDelivery Time?", "Can I Customize\nMy Ring?",
    "Do You Have\nReady-to-Buy Rings?", "How Can I Book\nan Appointment?"
]

# Now use the questions list
with st.container():
    for i in range(0, len(questions), 2):
        cols = st.columns(2)
        for j in range(2):
            if i + j < len(questions):
                if cols[j].button(questions[i + j], key=f"btn_{i+j}"):
                    handle_message(questions[i + j].replace("\n", " "))

# --- CHAT HISTORY ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- INPUT BOX ---
if user_input := st.chat_input("Type Anything..."):
    handle_message(user_input)
