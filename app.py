import streamlit as st
from resume_role_gen import extract_text_from_resume, resume_based_role, skill_generation
from candidate_response import record_response
from audio_transcription import transcribe_audio
from interview_q import asking_interview_questions, resume_based_questions, evaluate_performance

st.title("Cogniview - AI Interviewer")
st.subheader("Prepare for your next interview with AI")

# Sidebar Note
st.sidebar.markdown("""
### ⚠️ Important Note:

This AI Interview Preparation Assistant is currently optimized for candidates applying to roles in **Data Science**, **Data Engineering**, or **Data Analysis**.

If your background or career interest lies outside these domains, please select **"Based on Resume"**. The system will analyze your resume and ask technical questions relevant to your skills.

🛠️ *Support for additional roles is under development.*

📩 If you encounter any issues while using the application, please inform us. Your feedback helps us improve!
Also While talking please make sure you are loud and clear enough.
Thank you 
""")

# Role Selection
role = st.selectbox("Select a role", [
    "Select", "Data Scientist", "Data Analyst", "Data Engineer", "Based on Resume"
])

resume_text, suggested_role, resume_skills = "", None, ""

# Resume Handling
if role == "Based on Resume":
    resume_text = extract_text_from_resume()
    resume_skills = skill_generation(resume_text)
    if resume_text and st.button("Generate Role from Resume"):
        suggested_role = resume_based_role(resume_text)
        role = suggested_role
        st.success(f"Suggested Role: **{suggested_role}**")

# Start Interview
if st.button("Start Interview"):
    st.session_state.interview_started = True
    st.session_state.question_index = 0

    if "first_question" not in st.session_state:
        if role == "Based on Resume" and resume_text:
            st.session_state.first_question = resume_based_questions(role, resume_skills, "")
        else:
            st.session_state.first_question = asking_interview_questions(role, "")

# Interview Flow
if st.session_state.get("interview_started", False):
    index = st.session_state.get("question_index", 0)
    if index == 0:
        st.subheader(f"Q{index + 1}: {st.session_state.first_question}")

    # Record candidate response
    audio = record_response(key=f"response_{index}")

    # Transcription logic
    if st.button("📝 Transcribe", key=f"transcribe_{index}"):
        if audio:
            transcription = transcribe_audio(audio)
            st.session_state[f"transcription_{index}"] = transcription
            st.markdown("### 📝 Transcribed Response:")
            st.code(transcription)
        else:
            st.warning("Please record your response first.")

    # Next question logic
    if st.button("Next", key=f"next_{index}"):
        transcription = st.session_state.get(f"transcription_{index}", "")
        if transcription:
            if role == "Based on Resume":
                next_question = resume_based_questions(role, resume_skills, transcription)
            else:
                next_question = asking_interview_questions(role, transcription)

            st.session_state.question_index += 1
            next_index = st.session_state.question_index
            st.session_state[f"question_{next_index}"] = next_question
            st.subheader(f"Q{next_index + 1}: {next_question}")

            # Record new response for next question
            audio = record_response(key=f"response_{next_index}")

            if st.button("📝 Transcribe", key=f"transcribe_{next_index}"):
                if audio:
                    transcription = transcribe_audio(audio)
                    st.session_state[f"transcription_{next_index}"] = transcription
                    st.markdown("### 📝 Transcribed Response:")
                    st.code(transcription)
        else:
            st.warning("Please transcribe your response before proceeding.")

# Submit Interview Logic
if st.button("🚀 Submit Interview"):
    index = st.session_state.get("question_index", 0)
    if index < 4:  # i.e., less than 5 questions answered
        st.error("Interview Incomplete. At least 5 questions are required to evaluate your performance.")
    else:
        all_transcriptions = []
        for i in range(index + 1):
            trans_key = f"transcription_{i}"
            all_transcriptions.append(st.session_state.get(trans_key, "No response provided."))

        compiled_transcript = "\n\n".join(all_transcriptions)
        feedback = evaluate_performance(compiled_transcript, role)

        st.success("✅ Interview Evaluation Completed!")
        st.markdown("### 📊 Feedback & Score:")
        st.markdown(feedback)
