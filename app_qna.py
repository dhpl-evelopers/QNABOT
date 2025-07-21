import streamlit as st
import requests
import uuid
import time

# --- CONFIG ---
st.set_page_config(
    page_title="RingExpert - RINGS & I",
    page_icon="💍",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- UI STYLING ---
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton, .stStatusWidget {display: none !important;}
    
    [data-testid="stChatInput"] {
        border: none !important;
        outline: none !important;
        box-shadow: none !important;
    }

    .stButton>button {
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.02);
    }
    </style>
"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# --- BACKEND URL ---
CHAT_API_URL = "https://ringexpert-backend.azurewebsites.net/ask"

# --- QUICK QUESTIONS ---
QUICK_QUESTIONS = [
    "What is Rings & I?",
    "Do you customize rings?",
    "Where is your studio?",
    "What's the price range?",
    "What metals do you use?"
]

# --- SESSION INIT ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi, I'm your RingExpert! 💍 Ask me anything about diamonds, designs, prices or appointments."}
    ]
if "user_id" not in st.session_state:
    st.session_state.user_id = f"guest_{uuid.uuid4().hex[:8]}"

# --- STREAMING BOT RESPONSE ---
def stream_response(text):
    message_placeholder = st.empty()
    full_response = ""
    for word in text.split():
        full_response += word + " "
        message_placeholder.markdown(full_response + "▌")
        time.sleep(0.05)
    message_placeholder.markdown(full_response)

# --- CACHED API RESPONSE ---
@st.cache_data(show_spinner=False)
def get_cached_response(question):
    response = requests.post(CHAT_API_URL, json={"question": question}, timeout=10)
    response.raise_for_status()
    return response.json().get("answer", "Sorry, I didn't understand that.")

# --- MESSAGE HANDLER ---
def handle_message(message):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": message})

    with st.chat_message("user"):
        st.markdown(message)

    try:
        # Always get from backend
        answer = get_cached_response(message)

        # Directly display without stream delay
        with st.chat_message("assistant"):
            st.markdown(answer)

        # Save response
        st.session_state.messages.append({"role": "assistant", "content": answer})

    except Exception as e:
        error_msg = f"⚠ Error: {str(e)}"
        st.session_state.messages.append({"role": "assistant", "content": error_msg})
        with st.chat_message("assistant"):
            st.error(error_msg)


# --- DISPLAY CHAT HISTORY ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- QUICK QUESTION BUTTONS ---
st.markdown("#### 🔹 Quick Questions:")
cols = st.columns(len(QUICK_QUESTIONS))
for i, question in enumerate(QUICK_QUESTIONS):
    if cols[i].button(question, use_container_width=True, key=f"qq_{i}"):
        handle_message(question)

# --- CHAT INPUT BOX ---
if prompt := st.chat_input("Ask me anything about rings..."):
    handle_message(prompt)
