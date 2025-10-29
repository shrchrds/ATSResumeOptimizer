# The VERY FIRST import MUST be our config file.
import config
import os
import json
import streamlit as st
from file_tools.file_loader import detect_and_extract
from crew import run_pipeline
from utils import txt_to_docx_bytes

st.set_page_config(page_title="ATS Resume Agent", page_icon="🧠", layout="wide")
st.title("🧠 ATS-Optimized Resume Agent")
st.caption("Powered by CrewAI & Groq")

# --- UPDATED SIDEBAR FOR DETAILED STATUS ---
with st.sidebar:
    st.subheader("⚙️ Configuration Status")
    st.text_input("Model in use:", value=os.getenv("OPENAI_MODEL_NAME"), disabled=True)
    st.write(f"Groq Key Loaded: {'✅ Yes' if os.getenv('GROQ_API_KEY') else '❌ No'}")
    
    # These are the critical checks for LangSmith
    st.write(f"LangSmith Tracing: {'✅ On' if os.getenv('LANGCHAIN_TRACING_V2') == 'true' else '❌ Off'}")
    st.write(f"LangSmith Project: `{os.getenv('LANGCHAIN_PROJECT')}`")
    st.write(f"LangSmith Key Loaded: {'✅ Yes' if os.getenv('LANGCHAIN_API_KEY') else '❌ No'}")

    if not os.getenv("LANGCHAIN_API_KEY"):
        st.error("LangSmith API Key is MISSING. Tracing will fail silently.")
# --- END OF UPDATED SIDEBAR ---

# Main Application UI
colL, colR = st.columns(2)
# ... (rest of your UI code is the same) ...
with colL:
    up = st.file_uploader("1. Upload Your Resume", type=["pdf", "docx", "txt"])
with colR:
    job_title = st.text_input("2. Target Job Title")
    job_desc = st.text_area("3. Paste the Job Description", height=220)
run_btn = st.button("🚀 Run ATS Agent")
# ... (rest of your execution logic is the same) ...
if run_btn:
    # ...
    if not all([up, job_title, job_desc]):
        st.error("Please fill in all fields and upload a resume before running.")
    else:
        raw_text = detect_and_extract(up.name, up.read())[1]
        tabs = st.tabs(["Cleaned Resume", "ATS-Optimized Version", "Final Refined Version", "ATS Evaluation"])
        with st.spinner("Crew at work... Check LangSmith for live traces!"):
            cleaned, rewritten, final_resume, evaluation = run_pipeline(
                raw_resume_text=raw_text,
                job_title=job_title.strip(),
                job_description=job_desc.strip()
            )
        with tabs[0]: st.code(cleaned, language="markdown")
        with tabs[1]: st.code(rewritten, language="markdown")
        with tabs[2]: st.code(final_resume, language="markdown")
        with tabs[3]: st.code(evaluation, language="json")