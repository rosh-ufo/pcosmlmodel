import streamlit as st
import pandas as pd
import numpy as np

# ---- PAGE CONFIG ----
st.set_page_config(page_title="PCOS Early Detection System", layout="wide")

# ---- CUSTOM CSS ----
st.markdown("""
    <style>
    /* Header Styling */
    .header {
        background-color: #ffccd5;
        color: #6a1b4d;
        padding: 20px;
        text-align: center;
        font-size: 30px;
        font-weight: bold;
        border-radius: 10px;
    }
    /* Footer Styling */
    .footer {
        position: fixed;
        bottom: 0;
        width: 100%;
        text-align: center;
        padding: 10px;
        background-color: #ffccd5;
        color: #6a1b4d;
        font-size: 14px;
        border-radius: 10px;
    }
    /* General Container Styling */
    .container {
        background-color: #fff0f3;
        padding: 20px;
        border-radius: 10px;
    }
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #ffdde1;
    }
    </style>
    """, unsafe_allow_html=True)

# ---- HEADER ----
st.markdown('<div class="header">✨ Personalized PCOS Early Detection System ✨</div>', unsafe_allow_html=True)
st.write("")

# ---- SIDEBAR ----
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Test for PCOS", "Know More About PCOS"])

# ---- QUESTIONS DATA ----
questions = [
    ("irregular_periods", "Do you have irregular periods? (yes/no)"),
    ("weight_gain", "Have you experienced sudden weight gain? (yes/no)"),
    ("acne", "Do you have acne or oily skin? (yes/no)"),
    ("hair_growth", "Do you notice excessive hair growth on your body? (yes/no)"),
    ("balding", "Have you experienced hair thinning or balding? (yes/no)"),
    ("fast_food", "Do you consume fast food regularly? (yes/no)"),
    ("skin_darkening", "Have you noticed skin darkening recently? (yes/no)"),
    ("exercise", "Do you exercise frequently? (yes/no)"),
    ("period_len", "How long does your period last? (in days, numeric input)"),
    ("mood_swings", "Do you experience mood swings? (yes/no)")
]

# ---- FUNCTIONS ----
def initialize_session():
    """
    Initialize session variables to track test progress, inputs, and chat history.
    """
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.question_index = 0
        st.session_state.inputs = {key: None for key, _ in questions}
        st.session_state.test_started = False
        st.session_state.test_completed = False


def ask_next_question():
    """
    Returns the next question in sequence.
    """
    if st.session_state.question_index < len(questions):
        return questions[st.session_state.question_index][1]
    return None


def calculate_risk():
    """
    Calculates the PCOS risk score based on the user's responses.
    """
    inputs = st.session_state.inputs
    score = sum(value for value in inputs.values() if isinstance(value, int))

    if score <= 1:
        return "You have a LOW risk of PCOS. Keep monitoring your health and consult a doctor if needed."
    elif score <= 3:
        return "You have a MODERATE risk of PCOS. It is advisable to consult a doctor for further evaluation."
    else:
        return "You have a HIGH risk of PCOS. Please consult a doctor for a detailed diagnosis."


def process_user_input(user_input):
    """
    Handles user input, validates responses, and progresses the questions.
    """
    # Start the test if the user types "start"
    if "start" in user_input.lower() and not st.session_state.test_started:
        st.session_state.test_started = True
        st.session_state.messages.append({"role": "assistant", "content": "Great! Let's start the PCOS test. Please answer 'yes' or 'no' to the following questions."})
        return ask_next_question()

    # If the test hasn't started yet
    if not st.session_state.test_started:
        return "Hello! Type 'start' to begin the test and answer 'yes' or 'no' to the questions."

    # Handle greetings
    if any(greet in user_input.lower() for greet in ["hi", "hello", "hey"]):
        return "Hi! I’m OvaCare 🤖, your PCOS assistant. Shall we start the test? (type 'start')"

    # If test is completed, prompt for restart
    if st.session_state.test_completed:
        if "yes" in user_input.lower():
            reset_test()
            return ask_next_question()
        else:
            return "Thank you for using OvaCare! Stay healthy ❤️"

    # Validate user responses for questions
    current_question = questions[st.session_state.question_index]
    feature_name, question_text = current_question

    if "yes" in user_input.lower():
        st.session_state.inputs[feature_name] = 1
    elif "no" in user_input.lower():
        st.session_state.inputs[feature_name] = 0
    elif feature_name == "period_len" and user_input.isdigit():
        st.session_state.inputs[feature_name] = int(user_input)
    else:
        return "Please respond with 'yes' or 'no'."

    # Move to the next question or finish the test
    st.session_state.question_index += 1
    if st.session_state.question_index < len(questions):
        return ask_next_question()
    else:
        st.session_state.test_completed = True
        return calculate_risk()


def reset_test():
    """
    Resets the test so the user can retake it.
    """
    st.session_state.messages = []
    st.session_state.question_index = 0
    st.session_state.inputs = {key: None for key, _ in questions}
    st.session_state.test_started = False
    st.session_state.test_completed = False

# ---- HOME PAGE ----
if page == "Home":
    st.markdown('<div class="container">', unsafe_allow_html=True)
    st.subheader("Welcome to the Personalized PCOS Early Detection System!")
    st.write("""
        - Polycystic Ovary Syndrome (PCOS) affects 1 in 10 women of reproductive age.
        - Our system helps predict the risk of PCOS using user inputs such as symptoms, medical history, and lifestyle.
        - Navigate to the **PCOS Test Page** to check your PCOS risk.
    """)

# ---- TEST FOR PCOS PAGE ----
elif page == "Test for PCOS":
    st.markdown('<div class="container">', unsafe_allow_html=True)
    st.title("Ovucare! Your personal PCOS predictor")
    st.write("OvuCare will help you to know if you have PCOS or not.say hello to ovuCare")

    # Initialize session state
    initialize_session()

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Get user input
    user_input = st.chat_input("Type your message here...")

    if user_input:
        # Display user message
        with st.chat_message("user"):
            st.markdown(user_input)

        # Process user input
        bot_reply = process_user_input(user_input)

        # Display bot response
        with st.chat_message("assistant"):
            st.markdown(bot_reply)

        # Update chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})

# ---- ABOUT PCOS PAGE ---- 
elif page == "Know More About PCOS":
    st.markdown('<div class="container">', unsafe_allow_html=True)
    st.subheader("📚 What is PCOS?")
    st.write("""
        Polycystic Ovary Syndrome (PCOS) is a hormonal disorder that affects women during their reproductive years.
        
        ### Symptoms:
        - Irregular periods
        - Excessive hair growth (hirsutism)
        - Severe acne
        - Weight gain
        - Thinning hair or hair loss

        ### Causes:
        - Hormonal imbalances
        - Genetic predisposition
        - Insulin resistance

        ### Management:
        - Healthy diet and regular exercise
        - Medications to regulate menstrual cycles and reduce symptoms
        - Consulting a specialist for tailored treatments

        Learn more about managing PCOS and take care of your health! <3
    """)

# ---- FOOTER ----
st.markdown('<div class="footer">Made with ❤️ by Team DataBakers | Empowering Women’s Health</div>', unsafe_allow_html=True)
