# -*- coding: utf-8 -*-
"""app.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1kom8fNMLLlkz9UDkedBUWQ8Ne0pc6tm5
"""

import streamlit as st
import openai
import os
from sympy import symbols, Eq, solve
import random
from dotenv import load_dotenv

# Load API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client with the new SDK
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ---- Page Config ----
st.set_page_config(
    page_title="AI Chatbot Tutor",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---- Custom CSS Styling ----
st.markdown("""
    <style>
    .main {background-color: #f5f7fa;}
    .sidebar .sidebar-content {background-color: #1f77b4;}
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 10px 24px;
        margin-top: 10px;
    }
    .stRadio > div {flex-direction: row;}
    </style>
""", unsafe_allow_html=True)

# ---- Helper Functions ----
def explain_concept(concept):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # or "gpt-4" if available
        messages=[
            {"role": "system", "content": "You are a helpful electronics tutor."},
            {"role": "user", "content": f"Explain the concept of {concept} in Electronics Device and Circuit."}
        ],
        max_tokens=250,
        temperature=0.5
    )
    return response.choices[0].message.content.strip()


def solve_ohms_law(voltage=None, current=None, resistance=None):
    V, I, R = symbols('V I R')
    equation = Eq(V, I * R)
    if voltage is None:
        result = solve(equation.subs({I: current, R: resistance}), V)
        return f"Calculated Voltage: {result[0]} V"
    elif current is None:
        result = solve(equation.subs({V: voltage, R: resistance}), I)
        return f"Calculated Current: {result[0]} A"
    elif resistance is None:
        result = solve(equation.subs({V: voltage, I: current}), R)
        return f"Calculated Resistance: {result[0]} Ω"
    else:
        return "Please provide at least one missing value."

def generate_quiz():
    questions = [
        {"question": "What is the function of a diode?",
         "options": ["Amplify signals", "Allow current in one direction", "Store charge", "Convert AC to DC"],
         "answer": "Allow current in one direction"},
        {"question": "Which component amplifies signals?",
         "options": ["Resistor", "Capacitor", "Transistor", "Inductor"],
         "answer": "Transistor"}
    ]
    return random.choice(questions)

def design_circuit(component):
    try:
        response = client.completions.create(
            model="text-davinci-003",  # Use the appropriate model
            prompt=f"Design a simple circuit using {component}.",
            max_tokens=250,
            temperature=0.5
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"⚠️ Error: {e}"

# ---- Sidebar Navigation ----
with st.sidebar:
    st.image("https://miro.medium.com/v2/resize:fit:1100/format:webp/1*jMIid8wkWhV2b0dKWZ-wKw.jpeg", width=100)
    st.title("📚 AI Chatbot Tutor")
    menu = ["🏠 Home", "📖 Concept Explanation", "🧮 Numerical Solver", "📝 Interactive Quiz", "🔧 Circuit Design", "📂 Study Resources"]
    choice = st.radio("Navigate", menu)

# ---- Main Content ----
if choice == "🏠 Home":
    st.markdown("## 👋 Welcome to the AI Chatbot Tutor!")
    st.info("This interactive tool helps you learn Electronics Devices and Circuits with explanations, quizzes, and problem-solving features.")
    st.image("https://miro.medium.com/v2/resize:fit:1100/format:webp/1*jMIid8wkWhV2b0dKWZ-wKw.jpeg", caption="Learn Electronics Effectively")

elif choice == "📖 Concept Explanation":
    st.header("📘 Concept Explanation")
    concept = st.text_input("Enter a concept (e.g., diode, transistor):")
    if st.button("Explain"):
        with st.spinner("Fetching explanation..."):
            st.success(explain_concept(concept))
            st.progress(100)

elif choice == "🧮 Numerical Solver":
    st.header("🔢 Ohm's Law Calculator")
    voltage = st.number_input("Voltage (V):", value=0.0)
    current = st.number_input("Current (I):", value=0.0)
    resistance = st.number_input("Resistance (R):", value=0.0)
    if st.button("Calculate"):
        with st.spinner("Calculating..."):
            result = solve_ohms_law(
                voltage if voltage != 0 else None,
                current if current != 0 else None,
                resistance if resistance != 0 else None
            )
            st.success(result)

elif choice == "📝 Interactive Quiz":
    st.header("📝 Quick Quiz")
    quiz = generate_quiz()
    st.write(quiz["question"])
    selected_option = st.radio("Select your answer:", quiz["options"])
    if st.button("Submit Answer"):
        if selected_option == quiz["answer"]:
            st.success("Correct! 🎉")
        else:
            st.error(f"Incorrect. The correct answer is: {quiz['answer']}")

elif choice == "🔧 Circuit Design":
    st.header("🔧 Circuit Design Guidance")
    component = st.text_input("Enter a component for guidance (e.g., amplifier):")
    if st.button("Guide Me"):
        with st.spinner("Generating design steps..."):
            st.info(design_circuit(component))

elif choice == "📂 Study Resources":
    st.header("📚 Study Materials")
    st.write("Here are some useful resources:")
    st.markdown("""
    - [All About Circuits](https://www.allaboutcircuits.com/)
    - [Electronics Tutorials](https://www.electronics-tutorials.ws/)
    - [Basic Electronics YouTube Playlist](https://www.youtube.com/playlist?list=PLJvKqQx2AtfRKsH0spkn9Aqhl9P7ULwl-)
    """)

# ---- Footer ----
st.markdown("---")
st.markdown("Developed with ❤️ for Electronics Students by **Mohammed Sazzad Yousuf**")