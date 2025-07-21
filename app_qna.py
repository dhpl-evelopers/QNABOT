import streamlit as st
import requests
import uuid

# --- CONFIG ---
st.set_page_config(
    page_title="RingExpert - RINGS & I",
    page_icon="💍",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Hide Streamlit default elements
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton, .stStatusWidget {display: none !important;}
    [data-testid="stChatInput"] {border: 1px solid #c9a45d !important;}
    .stButton>button {
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.02);
    }
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Constants
CHAT_API_URL = "https://ringexpert-backend.azurewebsites.net/ask"

QUICK_QUESTIONS = [
    "What is Rings & I?",
    "Do you customize rings?",
    "Where is your studio?",
    "What's the price range?",
    "What metals do you use?"
]

# --- SESSION INIT ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi, I'm your RingExpert! 💍 Ask me anything about diamonds, designs, prices or appointments."}]
if "user_id" not in st.session_state:
    st.session_state.user_id = f"guest_{uuid.uuid4().hex[:8]}"

# --- CHAT DISPLAY ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- MESSAGE HANDLING (OPTIMIZED) ---
def handle_message(message, from_button=False):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": message})

    # Display user message immediately
    with st.chat_message("user"):
        st.markdown(message)

    try:
        # Get bot response
        response = requests.post(
            CHAT_API_URL,
            json={"question": message},
            timeout=10
        )
        response.raise_for_status()
        answer = response.json().get("answer", "Sorry, I didn't understand that.")

        # Add and display bot response
        st.session_state.messages.append({"role": "assistant", "content": answer})
        with st.chat_message("assistant"):
            st.markdown(answer)

    except Exception as e:
        error_msg = f"⚠ Error: {str(e)}"
        st.session_state.messages.append({"role": "assistant", "content": error_msg})
        with st.chat_message("assistant"):
            st.error(error_msg)

    # ❌ Remove this:
    # if from_button:
    #     st.rerun()

    
   

# --- QUICK QUESTION BUTTONS (OPTIMIZED) ---
st.markdown("#### Quick Questions:")
cols = st.columns(len(QUICK_QUESTIONS))
for i, question in enumerate(QUICK_QUESTIONS):
    if cols[i].button(question, use_container_width=True, key=f"qq_{i}"):
        handle_message(question, from_button=True)

# --- CHAT INPUT ---
if prompt := st.chat_input("Ask me anything about rings..."):
    handle_message(prompt)
