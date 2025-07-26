import streamlit as st
import requests
import uuid
import time
import re

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="AI RingExpert – RINGS & I",
    page_icon="💍",
    layout="wide",  # 👈 changed from "centered"
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
st.markdown("""
    <style>
    /* === Base Reset & Hide Elements === */
    #MainMenu, footer, header {visibility: hidden;}
    html, body {
        overflow-x: hidden !important;
        width: 100% !important;
    }
    
    /* === Layout Structure === */
    .block-container {
        padding-top: 0 !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
    
    /* === Typography === */
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
    
    /* === Button Grid System === */
    .button-container {
        width: 100%;
        display: flex;
        justify-content: center;
        margin: 0 auto 20px auto;
    }
    
    .button-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 16px;
        max-width: 520px;
        margin: 0 auto 30px auto;
        padding: 0 10px;
    }
    
    /* === Button Design === */
    .stButton>button {
        font-family: 'Oregon', serif !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        border-radius: 12px !important;
        padding: 12px 10px !important;
        background-color: white !important;
        color: black !important;
        border: 1px solid #ccc !important;
        box-shadow: 3px 3px 0px #ccc !important;
        transition: 0.2s ease-in-out;
    }
         /* ✅ Override mobile stacking — force 2 columns always */
@media screen and (max-width: 480px) {
  .button-grid {
    grid-template-columns: repeat(2, 1fr) !important;
    max-width: 100% !important;
    padding: 0 12px !important;
  }
}
    
    .stButton>button:hover {
        background: #c9a45d !important;
        color: white !important;
        transform: translateY(-1px);
    }
    
    /* === Mobile Responsiveness === */
    /* Tablets & Large Phones */
    @media (max-width: 768px) {
        .button-grid {
            gap: 10px !important;
            padding: 0 8px !important;
        }
        .stButton>button {
            font-size: 11px !important;
            padding: 8px 6px !important;
            min-height: 42px !important;
        }
    }
    
    /* Small Phones */
    @media (max-width: 480px) {
        .button-grid {
            gap: 8px !important;
        }
        .stButton>button {
            font-size: 10px !important;
            padding: 8px 4px !important;
            min-height: 40px !important;
        }
    }
    
    /* Very Small Phones (Single Column) */
    @media (max-width: 350px) {
        .button-grid {
            grid-template-columns: 1fr !important;
            max-width: 300px !important;
            gap: 6px !important;
        }
    }
    
    /* === Chat Input === */
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
    
    /* === Dark Mode Override === */
    @media (prefers-color-scheme: dark) {
        html, body, button, input, textarea {
            background-color: #ffffff !important;
            color: #000000 !important;
        }
        [data-testid="stChatInput"] > div {
            background-color: #ffffff !important;
        }
    }


.stButton>button {
    font-size: 11px !important;
    padding: 6px 8px !important;
    min-height: 38px !important;
    line-height: 1.2 !important;
    border-radius: 10px !important;
    white-space: normal !important;
    word-break: break-word !important;
    box-shadow: 2px 2px 0px #aaa !important;
    text-align: center !important;
}

/* Force 2 columns even on small screens */
.button-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 10px;
    max-width: 520px;
    margin: 0 auto 24px auto;
    padding: 0 8px;
}

@media (max-width: 480px) {
  .button-grid {
    grid-template-columns: repeat(2, 1fr) !important;
    gap: 8px !important;
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

# --- QUESTIONS LIST ---
questions = [
    "What Is RINGS & I?", "Where Is Your Studio?",
    "Natural or Lab-Grown Diamonds?", "What's the Price Range?",
    "Which Metals Do You Use?", "Which Metal Purities Do You Offer?",
    "Ring Making & Delivery Time?", "Can I Customize My Ring?",
    "Do You Have Ready-to-Buy Rings?", "How Can I Book an Appointment?"
]

# --- FINAL BUTTON LAYOUT (Center-aligned 2-column) ---

with st.container():
    st.markdown('<div class="button-grid">', unsafe_allow_html=True)
    cols = st.columns(2)
    for i, question in enumerate(questions):
        with cols[i % 2]:
            if st.button(question, key=f"btn_{i}"):
                handle_message(question)
    st.markdown('</div>', unsafe_allow_html=True)






# --- CHAT HISTORY (Appears below prompt section) ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# --- CHAT INPUT ---
# --- CHAT INPUT ---
if user_input := st.chat_input("Type Anything..."):
    handle_message(user_input)
