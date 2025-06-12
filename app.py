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
""")

# Role Selection
role = st.selectbox("Select a role", [
    "Select", "Data Scientist", "Data Analyst", "Data Engineer", "Based on Resume"
])

resume_text, suggested_role, resume_skills = "", None, ""

# Handle Resume Upload & Skill Extraction
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
    st.session_state.transcription = ""

    if "first_question" not in st.session_state:
        if role == "Based on Resume" and resume_text:
            st.session_state.first_question = resume_based_questions(role, resume_skills, "")
        else:
            st.session_state.first_question = asking_interview_questions(role, "")

# Main Interview Flow
if st.session_state.get("interview_started", False):
    if st.session_state.get("question_index", 0) == 0:
        st.subheader(st.session_state.first_question)

    audio = record_response(key=f"response_{st.session_state.question_index}")

    if st.button("📝 Transcribe", key=f"transcribe_{st.session_state.question_index}"):
        if audio:
            transcription = transcribe_audio(audio)
            st.session_state.transcription = transcription
            st.markdown("### 📝 Transcribed Response:")
            st.code(transcription)

    if st.button("Next", key=f"next_{st.session_state.question_index}"):
        transcription = st.session_state.get("transcription", "")
        if transcription:
            # Determine the question generator function
            if role == "Based on Resume":
                next_question = resume_based_questions(role, resume_skills, transcription)
            else:
                next_question = asking_interview_questions(role, transcription)

            st.session_state.question_index += 1
            st.subheader(f"Q{st.session_state.question_index + 1}: {next_question}")
            st.session_state.first_question = next_question  # For next flow
            audio = record_response(key=f"response_{st.session_state.question_index}")

            if st.button("📝 Transcribe", key=f"transcribe_{st.session_state.question_index}"):
                if audio:
                    transcription = transcribe_audio(audio)
                    st.session_state.transcription = transcription
                    st.markdown("### 📝 Transcribed Response:")
                    st.code(transcription)
        else:
            st.warning("Please transcribe your response before proceeding to the next question.")
if st.button("🚀 Submit Interview"):
    if st.session_state.get("question_index", 0) >=5:
        st.error("Interview Incomplete. At least 5 questions are required to evaluate your performance.")
    else:
        # Collect all transcriptions
        all_transcriptions = []
        for i in range(st.session_state.question_index + 1):
            trans_key = f"transcription_{i}"
            if trans_key in st.session_state:
                all_transcriptions.append(st.session_state[trans_key])
            else:
                all_transcriptions.append("No response provided.")

        compiled_transcript = "\n\n".join(all_transcriptions)
        feedback = evaluate_performance(compiled_transcript, role)
        st.success("✅ Interview Evaluation Completed!")
        st.markdown("### 📊 Feedback & Score:")
        st.markdown(feedback)