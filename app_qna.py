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
    </style>
""", unsafe_allow_html=True)


# --- EMBED MODE DETECTION ---
query_params = st.query_params

is_embed = query_params.get("embed", ["0"])[0] == "1"

# --- CUSTOM CSS FOR UI ---
st.markdown("""<style>


#MainMenu, footer, header {visibility: hidden;}

/* Layout Structure */
.block-container {
    padding-top: 0 !important;
}

/* Header Styles */
.header-bar {
    background-color: #000000;
    color: white;
    font-weight: bold;
    font-size: 18px;
    padding: 14px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-top-left-radius: 14px;
    border-top-right-radius: 14px;
}
.header-bar img {
    height: 20px;
    margin-right: 8px;
}

/* Text Styles */
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

/* Chat Message Styling */
.stChatMessage {
    font-size: 15px;
    line-height: 1.6;
}


/* Button Container */
.button-container {
    width: 100%;
    display: flex;
    justify-content: center;
    margin: 0 auto;
    padding: 0 15px;
}

/* Button Grid */
.button-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 12px;
    width: 100%;
    max-width: 550px;
}

/* Button Styling */
.stButton>button {
    width: 100% !important;
    height: 100% !important;
    min-height: 45px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: white;
    color: black;
    border-radius: 14px;
    padding: 10px 12px;
    font-size: 12px;
    font-weight: 500;
    font-family: 'Oregon', serif;
    box-shadow: 1px 1px 3px rgba(0,0,0,0.1);
    transition: all 0.2s ease;
    border: none;
    margin: 0;
}

.stButton>button:hover {
    background: #c9a45d !important;
    color: white !important;
}

/* Mobile Responsiveness */
@media (max-width: 768px) {
    .button-grid {
        gap: 10px;
    }
    .stButton>button {
        font-size: 11px;
        padding: 8px 6px;
    }
}

@media (max-width: 480px) {
    .button-grid {
        grid-template-columns: 1fr;
        max-width: 300px;
    }
}
            /* Mobile-specific fixes */
@media (max-width: 768px) {
    .button-grid {
        grid-template-columns: repeat(2, 1fr) !important;
        gap: 10px !important;
        padding: 0 10px !important;
    }
    
    .stButton>button {
        font-size: 11px !important;
        padding: 8px 5px !important;
        min-height: 40px !important;
    }
    
    /* Fix viewport scaling */
    @viewport {
        width: device-width;
        zoom: 1.0;
    }
    
    /* Prevent horizontal scrolling */
    html, body {
        overflow-x: hidden !important;
        width: 100% !important;
    }
}

/* Small phones (portrait) */
@media (max-width: 480px) {
    .button-grid {
        gap: 8px !important;
    }
    
    .stButton>button {
        font-size: 10px !important;
        padding: 6px 4px !important;
    }
}

/* Very small phones */
@media (max-width: 320px) {
    .button-grid {
        grid-template-columns: 1fr !important;
        max-width: 280px !important;
    }
}


/* Chat Input Styling */
[data-testid="stChatInput"] {
    border: 1px solid #c9a45d !important;
    border-radius: 12px !important;
    padding: 8px;
    max-width: 600px;
    margin: 0 auto;
}

[data-testid="stChatInput"] input {
    border-radius: 10px !important;
    padding: 10px !important;
}

/* Force Light Theme */
@media (prefers-color-scheme: dark) {
    html, body, button, input, textarea {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    [data-testid="stChatInput"] > div {
        background-color: #ffffff !important;
    }
}

/* Responsive Adjustments */
@media (max-width: 768px) {
    .block-container {
        padding-left: 12px;
        padding-right: 12px;
    }
    
    /* Hide scrollbars if present */
    html, body {
        overflow-x: hidden;
    }
}

@media (min-width: 769px) {
    .button-grid {
        max-width: 600px;
    }
    
    button[kind="primary"] {
        font-size: 12px;
        padding: 10px 8px;
    }
}

@media (max-width: 400px) {
    button[kind="primary"] {
        font-size: 10px;
        padding: 6px 4px;
    }
}

@media (max-width: 320px) {
    .button-grid {
        grid-template-columns: 1fr !important;
        max-width: 280px !important;
    }
}
            @media only screen and (max-width: 600px) {
  .your-container-class {
    font-size: 14px; /* Adjust as needed */
    padding: 10px; /* Adjust spacing */
  }
  
  /* If it's a list, you might want to stack items vertically */
  .your-list-class {
    flex-direction: column;
  }
}
            .your-text-elements {
  font-size: clamp(14px, 3vw, 18px); /* Min 14px, scales with viewport, max 18px */
}
            @media (max-width: 600px) {
    body {
        font-size: 14px;  /* Smaller font for mobile */
        line-height: 1.4;  /* Better spacing */
    }
    /* Ensure text containers don’t overflow */
    .text-container {
        padding: 0 10px;
        word-wrap: break-word;
    }
}
</style>""", unsafe_allow_html=True)




# --- API CONFIG ---
CHAT_API_URL = "https://ringexpert-backend.azurewebsites.net/ask"

# --- SESSION INITIALIZATION ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_id" not in st.session_state:
    st.session_state.user_id = f"guest_{uuid.uuid4().hex[:8]}"

# --- CHAT RESPONSE STREAM ---
def stream_response(text):
    message_placeholder = st.empty()
    full_response = ""
    for word in text.split():
        full_response += word + " "
        message_placeholder.markdown(full_response + "▌")
        time.sleep(0.02)
    message_placeholder.markdown(full_response)

# --- CACHED API CALL ---
@st.cache_data(show_spinner=False)
def get_cached_response(question):
    response = requests.post(CHAT_API_URL, json={"question": question}, timeout=10)
    response.raise_for_status()
    

@st.cache_data(show_spinner=False)
def get_cached_response(question):
    response = requests.post(CHAT_API_URL, json={"question": question}, timeout=10)
    response.raise_for_status()
    answer = response.json().get("answer", "Sorry, I didn't understand that.")

    # 🧼 Clean out "doc1", "[doc2]", "doc3." etc.
    cleaned = re.sub(r'\[?doc\d+\]?[.:]?', '', answer, flags=re.IGNORECASE)
    return cleaned.strip()


# --- HANDLING CHAT FLOW ---
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









# --- TITLES ---
st.markdown('<div class="chat-title">Want to know more about RINGS & I?</div>', unsafe_allow_html=True)
st.markdown('<div class="helper-text">Tap a Button or Start Typing</div>', unsafe_allow_html=True)


 



# --- BUTTON RENDERING ---
# --- BUTTON RENDERING ---
# --- BUTTON RENDERING ---
questions = [
    "What Is RINGS & I?", "Where Is Your Studio?",
    "Natural or Lab-Grown Diamonds?", "What's the Price Range?",
    "Which Metals Do You Use?", "Which Metal Purities Do You Offer?",
    "Ring Making & Delivery Time?", "Can I Customize My Ring?",
    "Do You Have Ready-to-Buy Rings?", "How Can I Book an Appointment?"
]

# Create columns for the button grid
col1, col2 = st.columns(2)

with st.container():
    st.markdown('<div class="button-container">', unsafe_allow_html=True)
    st.markdown('<div class="button-grid">', unsafe_allow_html=True)
    
    for i, question in enumerate(questions):
        if i % 2 == 0:
            with col1:
                if st.button(question, key=f"btn_{i}"):
                    handle_message(question)
        else:
            with col2:
                if st.button(question, key=f"btn_{i}"):
                    handle_message(question)
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)



# --- CHAT HISTORY (Appears below prompt section) ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# --- CHAT INPUT ---
# --- CHAT INPUT ---
if user_input := st.chat_input("Type Anything..."):
    handle_message(user_input)
