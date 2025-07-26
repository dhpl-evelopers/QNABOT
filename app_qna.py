import streamlit as st
import requests
import uuid
import time

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="AI RingExpert – RINGS & I",
    page_icon="💍",
    layout="centered",
    initial_sidebar_state="collapsed"
)

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
.quick-buttons-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 14px;
    margin-bottom: 20px;
}
.quick-buttons-container button {
    background-color: white;
    color: #000;
    border: 1px solid #000000;
    border-radius: 12px;
    padding: 8px 14px;
    font-size: 13px;
    font-weight: 500;
    box-shadow: 2px 2px 3px rgba(0,0,0,0.2);
    transition: all 0.3s ease;
}
.quick-buttons-container button:hover {
    background-color: #c9a45d;
    color: white;
    border: 1px solid #c9a45d;
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

# --- API CONFIG ---
CHAT_API_URL = "https://ringexpert-backend.azurewebsites.net/ask"

# --- SESSION INITIALIZATION ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi, I'm your RingExpert! 💍\nAsk me anything about diamonds, designs, prices or appointments."}
    ]
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
    return response.json().get("answer", "Sorry, I didn't understand that.")

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
    st.markdown('<div class="helper-text">Tap a button or Start Typing</div>', unsafe_allow_html=True)

    # --- QUICK QUESTIONS ---
    quick_questions = [
        "What Is RINGS & I?", "Where is your studio?",
        "Natural or Lab-Grown Diamonds?", "What’s the price range?",
        "Which metals do you use?", "Which metal purities do you offer?",
        "Ring making & delivery time?", "Can I customize my ring?",
        "Do you have ready-to-buy rings?", "How can I book an appointment?"
    ]

    st.markdown('<div class="quick-buttons-container">', unsafe_allow_html=True)
    cols = st.columns(2)
    for idx, question in enumerate(quick_questions):
        with cols[idx % 2]:
            if st.button(question, key=f"btn_{idx}"):
                handle_message(question)
    st.markdown('</div>', unsafe_allow_html=True)

# --- CHAT HISTORY ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- CHAT INPUT ---
if user_input := st.chat_input("Type Anything..."):
    handle_message(user_input)
