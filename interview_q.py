from resume_role_gen import model,skill_generation

from resume_role_gen import model

def asking_interview_questions(role, transcription):
    questions_prompt = f'''
You are a professional technical interviewer for the role of {role}. Your task is to ask concise, technical screening questions only from the following domains:

1. Core Python (data structures, functions, exception handling, libraries like pandas and numpy)
2. SQL (joins, window functions, subqueries, aggregation)
3. Statistics (descriptive stats, probability, distributions, hypothesis testing)
4. Machine Learning (model types, metrics, overfitting, bias-variance)
5. Exploratory Data Analysis (handling missing values, correlation, feature engineering, outliers)

If the role is **Software Engineer**, also include:
- Algorithms and data structures
- Front-end basics (HTML, CSS, JavaScript, React)

Always follow these rules:
- DO NOT ask behavioral, personal, or coding questions.
- Questions must be explainable verbally (no code writing).
- Use the candidate’s response (transcription below) to tailor the next technical question.
- Avoid repeating topics or asking previously asked questions.
- Also try to cover all the perspects of the interview to cover up in 15 questions. 
Candidate’s prior response:
"{transcription}"

Based on this, ask a relevant technical follow-up question only.
Return just the next question.
'''
    response = model.generate_content(questions_prompt)
    return response.text.strip()



def resume_based_questions(role, skills, transcription):
    skill_prompt = f'''
You are a technical interviewer for the role of {role}. Conduct a technical interview focusing only on the candidate's skills and resume details.

Skills provided:
{skills if skills else "No specific skills extracted from resume."}

Candidate’s prior response:
"{transcription}"

Instructions:
- Start with basic questions and gradually move to advanced ones.
- If skills are missing, generate questions based on the {role}.
- Avoid behavioral, personal, or coding questions.
- Focus only on topics explainable verbally (no code writing).
- Use the {transcription} to create a relevant and progressive follow-up question.
- Do not repeat topics already covered.
- Also try to cover all {skills} in about 10 to 15 questions because I will be giving the feature that the user can submit after 15 questions.

Return only the next technical question.
'''
    response = model.generate_content(skill_prompt)
    return response.text.strip()


    
def evaluate_performance(all_transcriptions, role):
    evaluation_prompt = f"""
    You are an expert interview evaluator. A candidate appeared for an interview for the role of {role}.
    Here are their responses to the interview questions:

    {all_transcriptions}

    Please analyze these responses and provide:
    1. An overall score out of 10 (based on technical accuracy, clarity, and relevance).
    2. Detailed feedback highlighting strengths and areas for improvement.
    3. Suggestions for how the candidate can better prepare in the future.

    Do not include the candidate's response again in the output.
    Be honest, constructive, and professional.
    """
    evaluation = model.generate_content(evaluation_prompt)
    return evaluation.text.strip()