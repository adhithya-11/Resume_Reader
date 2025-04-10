import streamlit as st
import fitz  # PyMuPDF
import json
from sentence_transformers import SentenceTransformer, util

# Load sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    text = ""
    with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

# Dummy function to extract skills (you can use real logic with spaCy)
def extract_skills(text):
    # Replace with proper keyword matching or spaCy patterns
    skills_list = ["Python", "SQL", "Machine Learning", "Deep Learning", "NLP", "Data Analysis"]
    found = [skill for skill in skills_list if skill.lower() in text.lower()]
    return found

# Function to calculate similarity between resume skills and job description
def calculate_similarity(skills, job_description):
    resume_text = " ".join(skills)
    embeddings = model.encode([resume_text, job_description], convert_to_tensor=True)
    score = util.pytorch_cos_sim(embeddings[0], embeddings[1]).item()
    return round(score, 2)

# Streamlit UI
st.set_page_config(page_title="AI Resume Skill Matcher", layout="centered")
st.title("🔍 AI Resume Classifier & Skill Extractor")

uploaded_file = st.file_uploader("Upload your resume (PDF)", type="pdf")
job_desc = st.text_area("Paste the Job Description here")

if uploaded_file and job_desc:
    with st.spinner("Processing..."):
        resume_text = extract_text_from_pdf(uploaded_file)
        skills = extract_skills(resume_text)
        match_score = calculate_similarity(skills, job_desc)

        result = {
            "extracted_skills": skills,
            "job_description_match_score": match_score
        }

        st.subheader("📄 Extracted Info")
        st.json(result)

        st.success(f"✅ Match Score: {match_score}")
