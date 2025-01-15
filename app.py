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
import math

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

def ohms_law(voltage=None, current=None, resistance=None):
    if voltage is None:
        return f"Voltage (V) = {current} A × {resistance} Ω = {current * resistance} V"
    elif current is None:
        return f"Current (I) = {voltage} V ÷ {resistance} Ω = {voltage / resistance} A"
    elif resistance is None:
        return f"Resistance (R) = {voltage} V ÷ {current} A = {voltage / current} Ω"
    else:
        return "Please leave one value as None to calculate it."

def rc_time_constant(resistance, capacitance):
    tau = resistance * capacitance
    return f"Time Constant (τ) = {resistance} Ω × {capacitance} F = {tau} seconds"

def resonant_frequency(inductance, capacitance):
    f0 = 1 / (2 * math.pi * math.sqrt(inductance * capacitance))
    return f"Resonant Frequency (f₀) = {f0:.2f} Hz"

def power_dissipation(current=None, voltage=None, resistance=None):
    if current is not None and resistance is not None:
        power = current ** 2 * resistance
        return f"Power (P) = {current}² × {resistance} = {power} W"
    elif voltage is not None and resistance is not None:
        power = (voltage ** 2) / resistance
        return f"Power (P) = {voltage}² ÷ {resistance} = {power} W"
    else:
        return "Provide either (current & resistance) or (voltage & resistance)."

def voltage_divider(v_in, r1, r2):
    v_out = v_in * (r2 / (r1 + r2))
    return f"Output Voltage (Vout) = {v_out:.2f} V"

def capacitor_charging(voltage_max, resistance, capacitance, time):
    voltage = voltage_max * (1 - math.exp(-time / (resistance * capacitance)))
    return f"Voltage at {time} sec = {voltage:.2f} V"

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
  solver_option = st.selectbox("Select a Numerical Solver", [
    "Ohm's Law Calculator",
    "RC Circuit Time Constant",
    "Resonant Frequency of LC Circuit",
    "Power Dissipation in Resistors",
    "Voltage Divider Calculator",
    "Capacitor Charging Voltage"
])

if solver_option == "Ohm's Law Calculator":
    voltage = st.number_input("Voltage (V)", value=0.0)
    current = st.number_input("Current (A)", value=0.0)
    resistance = st.number_input("Resistance (Ω)", value=0.0)
    if st.button("Calculate"):
        result = ohms_law(voltage if voltage != 0 else None,
                          current if current != 0 else None,
                          resistance if resistance != 0 else None)
        st.success(result)

elif solver_option == "RC Circuit Time Constant":
    resistance = st.number_input("Resistance (Ω)", value=0.0)
    capacitance = st.number_input("Capacitance (F)", value=0.0)
    if st.button("Calculate"):
        st.success(rc_time_constant(resistance, capacitance))

elif solver_option == "Resonant Frequency of LC Circuit":
    inductance = st.number_input("Inductance (H)", value=0.0)
    capacitance = st.number_input("Capacitance (F)", value=0.0)
    if st.button("Calculate"):
        st.success(resonant_frequency(inductance, capacitance))

elif solver_option == "Power Dissipation in Resistors":
    current = st.number_input("Current (A)", value=0.0)
    voltage = st.number_input("Voltage (V)", value=0.0)
    resistance = st.number_input("Resistance (Ω)", value=0.0)
    if st.button("Calculate"):
        st.success(power_dissipation(current if current != 0 else None,
                                      voltage if voltage != 0 else None,
                                      resistance if resistance != 0 else None))

elif solver_option == "Voltage Divider Calculator":
    v_in = st.number_input("Input Voltage (V)", value=0.0)
    r1 = st.number_input("Resistor R1 (Ω)", value=0.0)
    r2 = st.number_input("Resistor R2 (Ω)", value=0.0)
    if st.button("Calculate"):
        st.success(voltage_divider(v_in, r1, r2))

elif solver_option == "Capacitor Charging Voltage":
    voltage_max = st.number_input("Maximum Voltage (V)", value=0.0)
    resistance = st.number_input("Resistance (Ω)", value=0.0)
    capacitance = st.number_input("Capacitance (F)", value=0.0)
    time = st.number_input("Time (s)", value=0.0)
    if st.button("Calculate"):
        st.success(capacitor_charging(voltage_max, resistance, capacitance, time))


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
    - [Basic Electronics YouTube Playlist](https://www.youtube.com/playlist?list=PL0o_zxa4K1BV9E-N8tSExU1djL6slnjbL)
    """)

# ---- Footer ----
st.markdown("---")
st.markdown("Developed with ❤️ for Electronics Students by **Mohammed Sazzad Yousuf**")