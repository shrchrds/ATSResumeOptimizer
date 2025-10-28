# streamlit_app.py - THE FINAL, CORRECTED VERSION

import os
import json
import streamlit as st
from dotenv import load_dotenv

# --- START OF THE GUARANTEED FIX ---
# This block MUST be at the very top.
load_dotenv()

# THIS IS THE CRITICAL FIX:
# We tell the OpenAI client to use your REAL GROQ KEY.
os.environ["OPENAI_API_KEY"] = os.getenv("GROQ_API_KEY")

# We still point it to Groq's server endpoint.
os.environ["OPENAI_API_BASE"] = "https://api.groq.com/openai/v1"

# We set the model name.
os.environ["OPENAI_MODEL_NAME"] = "llama-3.3-70b-versatile"
# --- END OF THE GUARANTEED FIX ---


# The rest of the application can now be imported and run.
from file_tools.file_loader import detect_and_extract
from crew import run_pipeline
from utils import txt_to_docx_bytes


st.set_page_config(page_title="ATS Resume Agent (CrewAI)", page_icon="🧠", layout="wide")
st.title("🧠 ATS-Optimized Resume Agent (CrewAI + Groq)")
st.caption("Upload your resume (.pdf or .docx), target a role, and get an ATS-friendly version with scores & quick wins.")

with st.sidebar:
    st.subheader("Groq Settings (via OpenAI endpoint)")
    st.text_input("Model:", value=os.environ["OPENAI_MODEL_NAME"], disabled=True)
    api_key_loaded = "✅ Groq API Key loaded" if os.getenv("GROQ_API_KEY") else "❌ Groq API Key not found"
    st.write(api_key_loaded)

# Inputs and the rest of your UI code is correct...
colL, colR = st.columns([1,1])
with colL:
    up = st.file_uploader("Upload Resume (.pdf or .docx preferred)", type=["pdf", "docx", "txt"])
with colR:
    job_title = st.text_input("Target Job Title (e.g., 'Machine Learning Engineer')")
    job_desc = st.text_area("Paste Job Description", height=220, placeholder="Paste JD here...")

run_btn = st.button("Run ATS Agent")

if run_btn:
    if up is None:
        st.error("Please upload a resume file.")
    elif not job_title or not job_desc.strip():
        st.error("Please provide a target job title and job description.")
    else:
        ext, raw_text = detect_and_extract(up.name, up.read())
        if not raw_text.strip():
            st.error("Could not extract any text from the file.")
        else:
            tabs = st.tabs(["Cleaned Resume", "Rewritten (ATS-optimized)", "Final (Refined Bullets)", "ATS Evaluation"])
            with st.spinner("Running Crew agents..."):
                cleaned, rewritten, final_resume, evaluation = run_pipeline(
                    raw_resume_text=raw_text,
                    job_title=job_title.strip(),
                    job_description=job_desc.strip()
                )
            
            with tabs[0]:
                st.subheader("Cleaned Resume (plain text)")
                st.code(cleaned, language="markdown")
            with tabs[1]:
                st.subheader("Rewritten Resume (ATS-optimized)")
                st.code(rewritten, language="markdown")
            with tabs[2]:
                st.subheader("Final Resume (Refined Bullets)")
                st.code(final_resume, language="markdown")
            with tabs[3]:
                st.subheader("ATS Evaluation & Suggestions")
                st.code(evaluation, language="json")
