import streamlit as st
import requests

st.set_page_config(page_title="📅 Appointment Booking Agent")

st.title("📅 Appointment Booking Chatbot")
st.markdown("Talk to your calendar assistant. Make sure you [log in with Google](http://localhost:8000/auth) before chatting.")

# Chat history state
if "chat" not in st.session_state:
    st.session_state.chat = [{"role": "assistant", "content": "Hi! I can help you book a meeting. Just type something like 'Book a call tomorrow at 2 PM'."}]

# Chat input
user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state.chat.append({"role": "user", "content": user_input})

    # Send to FastAPI
    response = requests.post("http://localhost:8000/chat", json={"messages": st.session_state.chat})
    
    if response.status_code == 200:
        bot_response = response.json()["messages"][-1]
        st.session_state.chat.append(bot_response)
    else:
        st.session_state.chat.append({"role": "assistant", "content": "⚠️ Something went wrong. Please log in via /auth."})

# Render chat
for msg in st.session_state.chat:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
