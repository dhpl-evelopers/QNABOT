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
# Replace your entire styling section with this:
st.markdown("""
<style>
    @font-face {
        font-family: 'Oregon';
        src: url('https://cdn.shopify.com/s/files/1/0843/6917/8903/files/OregonLDO-Light.woff2') format('woff2');
        font-weight: 300;
        font-style: normal;
    }
    
    /* Reset all elements */
    html, body, div, button {
        font-family: 'Oregon', sans-serif !important;
        margin: 0 !important;
        padding: 0 !important;
        box-sizing: border-box !important;
    }
    
      /* Base container - smaller */
    .main .block-container {
        padding: 8px 8px 12px !important;
        max-width: 360px !important;  /* Reduced from 400px */
    }/* Title styling - smaller */
    .chat-title {
        font-size: 16px !important;  /* Reduced from 18px */
        margin: 0 0 6px 0 !important;
    }
    
    /* Subtitle - smaller */
    .helper-text {
        font-size: 10px !important;  /* Reduced from 12px */
        margin-bottom: 16px !important;
    }
    
    /* Compact buttons */
    .stButton>button {
        font-size: 10px !important;  /* Smaller font */
        min-height: 50px !important;  /* Reduced from 60px */
        padding: 8px 6px !important;  /* Tighter padding */
        margin: 0 0 6px 0 !important;  /* Reduced spacing */
        line-height: 1.3 !important;
    }
    
    /* Tighter grid */
    .stColumns > div {
        flex: 1 1 calc(50% - 4px) !important;  /* Reduced gap */
        min-width: calc(50% - 4px) !important;
    }
    
    /* Mobile adjustments */
    @media (max-width: 480px) {
        .main .block-container {
            padding: 6px 6px 10px !important;
            max-width: 100% !important;
        }
        .stButton>button {
            min-height: 45px !important;
            font-size: 9px !important;
        }
    }

    
    /* Force 2-column layout */
    .stColumns > div {
        flex: 1 1 calc(50% - 6px) !important;
        min-width: calc(50% - 6px) !important;
        max-width: calc(50% - 6px) !important;
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

questions = [
    "What Is\nRINGS & I?", "Where Is\nYour Studio?",
    "Natural or\nLab-Grown Diamonds?", "What's the\nPrice Range?",
    "Which Metals\nDo You Use?", "Which Metal\nPurities Do You Offer?",
    "Ring Making &\nDelivery Time?", "Can I Customize\nMy Ring?",
    "Do You Have\nReady-to-Buy Rings?", "How Can I Book\nan Appointment?"
]


# Update your button rendering code:
with st.container():
    col1, col2 = st.columns(2)
    for i, question in enumerate(questions):
        if i % 2 == 0:
            with col1:
                if st.button(question, key=f"btn_{i}"):
                    handle_message(question.replace("\n", " "))
        else:
            with col2:
                if st.button(question, key=f"btn_{i}"):
                    handle_message(question.replace("\n", " "))

# --- CHAT HISTORY ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- INPUT BOX ---
if user_input := st.chat_input("Type Anything..."):
    handle_message(user_input)
