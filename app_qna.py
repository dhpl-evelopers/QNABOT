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
@import url('https://fonts.googleapis.com/css2?family=Lora:wght@300&display=swap');
html, body {
    font-family: 'Lora', serif;
    background-color: #ffffff;
}
#MainMenu, footer, header {visibility: hidden;}
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
.chat-title {
    font-size: 20px;
    font-weight: 600;
    margin-top: 18px;
    text-align: center;
    color: #000000;
}
.helper-text {
    font-size: 13.5px;
    text-align: center;
    margin-bottom: 18px;
    color: #555555;
}

.stChatMessage {
    font-size: 15px;
    line-height: 1.6;
}
[data-testid="stChatInput"] {
    border: 1px solid #c9a45d !important;
    border-radius: 12px !important;
    padding: 8px;
}
.stTextInput>div>div>input {
    border-radius: 10px;
    padding: 10px;
    border: 1px solid #c9a45d;
}
.block-container {
    padding-top: 0 !important;
}
</style>""", unsafe_allow_html=True)

st.markdown("""
<style>
.button-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);  /* Two buttons side-by-side */
    gap: 10px 10px;
    padding: 0 12px;
    margin-bottom: 20px;
}

/* Button Styling */
button[kind="primary"], button[type="submit"] {
    all: unset;
    display: inline-block;
    background-color: white;
    color: #000;
    border-radius: 16px;
    padding: 6px 10px;
    font-size: 11px;   /* 🟢 Compact font for mobile */
    font-weight: 500;
    font-family: 'Oregon', serif;
    box-shadow: 1.5px 1.5px 3px rgba(0, 0, 0, 0.15);
    cursor: pointer;
    text-align: center;
    line-height: 1.2;
    word-break: break-word;
    width: 100%;
    height: auto;
    transition: background-color 0.2s ease, color 0.2s ease;
}

/* Hover */
button[kind="primary"]:hover, button[type="submit"]:hover {
    background-color: #c9a45d;
    color: white;
}

/* Optional: fallback to 1 column on very narrow phones */
@media screen and (max-width: 330px) {
  .button-grid {
    grid-template-columns: 1fr !important;
  }
}
.button-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 10px;
    padding: 0 14px;
    margin-bottom: 24px;
}

button[kind="primary"], button[type="submit"] {
    all: unset;
    display: inline-block;
    background-color: white;
    color: #000;
    border-radius: 14px;
    padding: 6px 10px;
    font-size: 11px;
    font-weight: 500;
    font-family: 'Oregon', serif;
    box-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    cursor: pointer;
    text-align: center;
    word-break: break-word;
    width: 100%;
    height: auto;
    transition: all 0.2s ease;
}

/* Hover effect */
button[kind="primary"]:hover, button[type="submit"]:hover {
    background-color: #c9a45d;
    color: white;
}

/* Fallback to single column on very small phones */
@media screen and (max-width: 330px) {
    .button-grid {
        grid-template-columns: 1fr !important;
    }
}

           

            /* 🔒 Force light theme across all browsers/devices */
@media (prefers-color-scheme: dark) {
  html, body {
    background-color: #ffffff !important;
    color: #000000 !important;
  }

  button, input, textarea {
    background-color: #ffffff !important;
    color: #000000 !important;
    border-color: #000000 !important;
  }

  ::placeholder {
    color: #888888 !important;
  }
}

            /* 🔒 Force light background even on left input icon container (chat send icon) */
[data-testid="stChatInput"] > div {
    background-color: #ffffff !important;
    border-radius: 12px !important;
}

/* 🔒 Also override the div wrapper around input for some phones */
[data-testid="stChatInput"] div[data-baseweb="input"] {
    background-color: #ffffff !important;
    color: #000000 !important;
    border-radius: 12px !important;
}

/* 🔒 Reset Streamlit input-icon container */
[data-testid="stChatInput"] svg {
    color: #000000 !important;
}

/* Optional: better white border when focusing */
[data-testid="stChatInput"] input:focus {
    outline: none !important;
    border: 1px solid #c9a45d !important;
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







# --- PROMPT TOGGLE STATE ---
# --- PROMPT TOGGLE STATE ---
if "show_all_prompts" not in st.session_state:
    st.session_state.show_all_prompts = False

# --- TITLES ---
st.markdown('<div class="chat-title">Want to know more about RINGS & I?</div>', unsafe_allow_html=True)
st.markdown('<div class="helper-text">Tap a Button or Start Typing</div>', unsafe_allow_html=True)

# --- QUESTION SETS ---
# --- QUESTION SETS ---
all_questions = [
    "What Is RINGS & I?", "Where is your studio?",
    "Natural or Lab-Grown Diamonds?", "What’s the price range?",
    "Which metals do you use?", "Which metal purities do you offer?",
    "Ring making & delivery time?", "Can I customize my ring?",
    "Do you have ready-to-buy rings?", "How can I book an appointment?"
]
initial_questions = all_questions[:5]
extra_questions = all_questions[5:]

# --- QUICK BUTTONS AS GRID ---
def render_buttons(questions, key_prefix="btn"):
    st.markdown('<div class="button-grid">', unsafe_allow_html=True)


    for idx, question in enumerate(questions):
        if st.button(label=question, key=f"{key_prefix}_{idx}_btn"):
             handle_message(question)

    st.markdown('</div>', unsafe_allow_html=True)





    # Listen to button presses
    if "custom_question" in st.session_state:
        handle_message(st.session_state.pop("custom_question"))



# Render buttons
render_buttons(initial_questions)
if not st.session_state.show_all_prompts:
    if st.button("see more..", key="see_more"):
        st.session_state.show_all_prompts = True
else:
    render_buttons(extra_questions, key_prefix="btn_extra")



# --- CHAT HISTORY (Appears below prompt section) ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# --- CHAT INPUT ---
# --- CHAT INPUT ---
if user_input := st.chat_input("Type Anything..."):
    handle_message(user_input)
