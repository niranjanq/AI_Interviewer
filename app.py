# app.py

import streamlit as st

# Initialize session variables
if "step" not in st.session_state:
    st.session_state.step = 1
if "role" not in st.session_state:
    st.session_state.role = None
if "difficulty" not in st.session_state:
    st.session_state.difficulty = None

st.set_page_config(page_title="AI Interview Assistant", layout="centered")
st.title("🤖 AI Interview Preparation Assistant")

# Step 1: Choose role
if st.session_state.step == 1:
    st.subheader("Step 1: Choose a role to prepare for")
    role = st.selectbox("Select a role", ["Select","Data Scientist" ,"Data Analyst", "Software Engineer", "Product Manager"])
    if st.button("Next") and role != "Select":
        st.session_state.role = role
        st.session_state.step = 2

# Step 2: Choose difficulty
elif st.session_state.step == 2:
    st.subheader(f"Step 2: Select difficulty level for {st.session_state.role}")
    level = st.radio("Choose a difficulty level", ["Easy", "Medium", "Hard"])
    if st.button("Start Interview"):
        st.session_state.difficulty = level
        st.session_state.step = 3

# Step 3: Confirmation before questions
elif st.session_state.step == 3:
    st.subheader("✅ Ready to start?")
    st.markdown(f"**Role:** {st.session_state.role}  \n**Level:** {st.session_state.difficulty}")
    if st.button("Begin Interview"):
        st.write("👉 (Here we will load and ask the first question...)")
        # Next steps will load the question list and start the Q&A loop
