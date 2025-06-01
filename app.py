import streamlit as st
import random
import requests
import json

# Health tips
health_tips = [
    "Get moving", 
    "Eat more whole foods (and less processed food)", 
    "If you drink alcohol, do so responsibly", 
    "Make preventive care a priority", 
    "If you smoke, try to quit", 
    "Make sleep a priority", 
    "Stay hydrated"
]

# Initialize session states
if "user_typing" not in st.session_state:
    st.session_state.user_typing = False
if "conversation" not in st.session_state:
    st.session_state.conversation = []

# CSS loader
with open('styles.css', "r") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Display a header
st.image("logolarge.jpg", use_container_width=False)

if not st.session_state.user_typing and len(st.session_state.conversation) == 0:
    st.title("We Empower You with Timely Healthcare Solutions, Expert Guidance, and Personalized Support for a Healthier Tomorrow.")

# Capture user input
user_input = st.chat_input("Enter your message here...")


OPENROUTER_API_KEY = st.secrets["GOOGLE_API_KEY"]
# Function to get response from OpenRouter
def get_openrouter_response(prompt):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://your-site-url.com", 
        "X-Title": "HealthChat by Debug Dynasty"      
    }

    payload = {
        "model": "meta-llama/llama-3.3-70b-instruct:free",
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, data=json.dumps(payload))
    
    if response.status_code == 200:
        data = response.json()
        return data["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code} - {response.text}"

# Process user input and generate bot response
if user_input:
    st.session_state.user_typing = True
    st.session_state.conversation.append({"role": "user", "content": user_input})

    # Easter eggs
    if user_input.lower().strip() == "creator":
        easter_egg_response = "Whoa! You cracked the code! My creator? Oh, it's none other than Syed Zaid Ali — the genius, the mastermind, the legend... and the man who keeps saying 'I Am The Best!' 😎🎩✨"
        st.session_state.conversation.append({"role": "ai", "content": easter_egg_response})
    elif user_input.lower().strip() == "team":
        team_response = "Made with love by team Debug Dynasty! ❤️ Sheikh Sahil (the leader), Syed Zaid Ali (the mastermind), Dip Banerjee (the support), Mohd Sami Ullah (paani pilane wala 😅). Sorry bhai Sami, I love you! ❤️"
        st.session_state.conversation.append({"role": "ai", "content": team_response})
    else:
        with st.spinner("Thinking..."):
            bot_reply = get_openrouter_response(user_input)
            st.session_state.conversation.append({"role": "ai", "content": bot_reply})

    st.session_state.user_typing = False

# Display conversation timeline
for message in st.session_state.conversation:
    with st.chat_message(message["role"]):
        st.success(message["content"])

# Sidebar
st.sidebar.title("Health Tips")
st.sidebar.subheader(random.choice(health_tips))
