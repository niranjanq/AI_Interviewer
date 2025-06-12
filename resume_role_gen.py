import streamlit as st

import os
import google.generativeai as genai
import PyPDF2
from dotenv import load_dotenv
load_dotenv()
# from app import transcription
# from extract_text_from_resume import resume_text
# from app import audio_text
# Set your API key via environment variable before running
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-2.0-flash")

def extract_text_from_resume():
    resume = st.file_uploader("Upload your resume", type=['pdf'])
    if resume:
        st.success("Resume uploaded successfully!")
        pdf_reader = PyPDF2.PdfReader(resume)
        resume_text = ""
        for page in pdf_reader.pages:
            resume_text += page.extract_text()
        return resume_text
    # else:
    #     st.warning("Please upload your resume in PDF format.")
    return ""

def resume_based_role(resume_text):
    prompt = f'''On the basis of the resume text below, generate a job role that best fits the candidate:
    {resume_text}, just give the role name without any additional text.
    '''
    if not resume_text:
        return "Please upload a resume to generate a role."
    response = model.generate_content(prompt)
    return response.text.strip()


def asking_questions(role,resume_text):
    intro_prompt=f'''Act as a professional interviewer in the field of {role} and you are taking an 
    interview of a cadidate for the role of {role}
    Ask the candidate a question to start the interview, and then ask follow-up questions based on the candidate's response.
    Start with a question with the introduction of the candidate, and then ask questions based on the {role}.
    Also store the questions and response of the candidate also store your remarks on the candidate's response and at the end of the interview
    provide a summary of the interview and your remarks on the candidate's response.
    do not produce so much text, just give the question and then wait for the candidate's response.
    Ask questions according to the {resume_text}
    only ask the introduction question. No other behavioural or personal questions.
    '''
    response=model.generate_content(intro_prompt)
    return response.text.strip()

# def asking_interview_questions():
#     prompt = f"""Act as a professional interviewer in the field of {role}.
# Based on the candidate's response: "{audio_text}", ask a relevant follow-up question.
# Only return the next question if {audio_text} is present else tell to attempt the previous question .
# Also ask questions from python,mysql and {role} related questions from a range of basic to advanced.
# """
#     response = model.generate_content(prompt)
#     return response.text.strip()
def skill_generation(resume_text):
    prompt = f'''On the basis of the resume text below, generate a list of skills that the candidate has:
    {resume_text}, just give the skills in a comma separated format without any additional text.
    '''
    if not resume_text:
        return "Please upload a resume to generate skills."
    response = model.generate_content(prompt)
    return response.text.strip()