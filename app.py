import streamlit as st
import random
import google.generativeai as genai

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

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
    st.session_state.conversation = []  # Single list to maintain the timeline

# CSS loader
with open('styles.css', "r") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Google API Key and Generative Model setup
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-pro-001")

# Display a header
st.image("logolarge.jpg", use_container_width=False)

# Display the tagline only if no user message has been entered yet
if not st.session_state.user_typing and len(st.session_state.conversation) == 0:
    st.title("We Empower You with Timely Healthcare Solutions, Expert Guidance, and Personalized Support for a Healthier Tomorrow.")

# Capture user input
user_input = st.chat_input("Enter your message here...")

# Process user input and generate bot response
if user_input:
    # Update user typing state
    st.session_state.user_typing = True

    # Add user's message to the conversation
    st.session_state.conversation.append({"role": "user", "content": user_input})

    # Easter egg: Check for specific triggers
    if user_input.lower().strip() == "creator":
        easter_egg_response = "Whoa! You cracked the code! My creator? Oh, it's none other than Syed Zaid Ali — the genius, the mastermind, the legend... and the man who keeps saying 'I Am The Best!' 😎🎩✨"
        st.session_state.conversation.append({"role": "ai", "content": easter_egg_response})
    elif user_input.lower().strip() == "team":
        team_response = "Made with love by team Debug Dynasty! \u2764 Sheikh Sahil(the leader) Syed Zaid Ali(the mastermind) Dip Banerjee(the support) Mohd Sami Ullah(well, yeh bas paani pila raha tha lakar) Sorry yr sami bhai i love you i am sorry"
        st.session_state.conversation.append({"role": "ai", "content": team_response})
    else:
        # Use a spinner while generating the bot's response
        with st.spinner("Thinking..."):
            response = model.generate_content(user_input)
            if response and response.text:
                # Add bot's response to the conversation
                st.session_state.conversation.append({"role": "ai", "content": response.text})

    # Reset user typing state after response generation
    st.session_state.user_typing = False

# Display messages in an alternate fashion (timeline)
for message in st.session_state.conversation:
    with st.chat_message(message["role"]):
       st.success(message["content"])

# Sidebar with health tips
st.sidebar.title("Health Tips")
st.sidebar.subheader(random.choice(health_tips))
