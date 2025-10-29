# CRITICAL: This MUST be the very first import to ensure environment is configured
import config

import os
import streamlit as st
from file_tools.file_loader import detect_and_extract
from crew import run_pipeline

# Configure Streamlit page
st.set_page_config(
    page_title="ATS Resume Agent",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main title
st.title("🧠 ATS-Optimized Resume Agent")
st.caption("Powered by CrewAI, Groq & LangSmith")

# Sidebar configuration
with st.sidebar:
    st.subheader("⚙️ Model Configuration")
    
    # Available Groq models
    AVAILABLE_MODELS = [
        "llama-3.1-8b-instant",      # Fast and efficient, good for most tasks
        "llama-3.3-70b-versatile",   # More powerful, better for complex tasks
    ]
    
    selected_model = st.selectbox(
        "Choose a model for this run:",
        AVAILABLE_MODELS,
        index=0,
        help="Select the Groq model to use for processing your resume"
    )
    
    st.divider()
    
    # Connection status display
    st.subheader("📊 System Status")
    
    config_status = config.get_config_status()
    
    st.write(f"**Current Model:** `{selected_model}`")
    st.write(f"**Groq API:** {'✅ Connected' if config_status['groq_configured'] else '❌ Not Configured'}")
    st.write(f"**LangSmith Tracing:** {'✅ Enabled' if config_status['tracing_enabled'] else '❌ Disabled'}")
    
    if config_status['tracing_enabled']:
        st.write(f"**LangSmith Key:** {'✅ Set' if config_status['langsmith_key_set'] else '❌ Missing'}")
        st.write(f"**Project:** `{config_status['langsmith_project']}`")
        st.info("🔍 Traces will be available in your LangSmith project")
    else:
        st.warning("⚠️ LangSmith tracing is disabled. Set LANGCHAIN_API_KEY to enable.")
    
    st.divider()
    
    # Help section
    with st.expander("ℹ️ How to Use"):
        st.markdown("""
        1. **Upload Resume:** PDF, DOCX, or TXT format
        2. **Enter Job Title:** The position you're applying for
        3. **Paste Job Description:** Full job posting text
        4. **Select Model:** Choose based on your needs
        5. **Run Pipeline:** Click the button and wait
        6. **Review Results:** Check all tabs for outputs
        """)

# Main input section
col_left, col_right = st.columns(2)

with col_left:
    uploaded_file = st.file_uploader(
        "1️⃣ Upload Your Resume",
        type=["pdf", "docx", "txt"],
        help="Upload your current resume in PDF, DOCX, or TXT format"
    )

with col_right:
    job_title = st.text_input(
        "2️⃣ Target Job Title",
        placeholder="e.g., Senior Software Engineer",
        help="Enter the exact job title you're applying for"
    )
    
    job_description = st.text_area(
        "3️⃣ Paste the Job Description",
        height=220,
        placeholder="Paste the complete job description here...",
        help="Include all details: responsibilities, requirements, qualifications"
    )

# Run button
run_button = st.button(
    "🚀 Run ATS Agent",
    type="primary",
    use_container_width=True
)

# Process the resume when button is clicked
if run_button:
    # Validation
    if not uploaded_file:
        st.error("❌ Please upload a resume file before running.")
        st.stop()
    
    if not job_title or not job_title.strip():
        st.error("❌ Please enter a target job title before running.")
        st.stop()
    
    if not job_description or not job_description.strip():
        st.error("❌ Please paste the job description before running.")
        st.stop()
    
    try:
        # Configure the model and tracing for this run
        run_config = config.configure_model_for_run(selected_model)
        
        # Display configuration confirmation
        with st.container():
            col1, col2, col3 = st.columns(3)
            with col1:
                st.info(f"🤖 Model: `{run_config['model']}`")
            with col2:
                st.info(f"📊 Tracing: {'✅ On' if run_config['tracing_enabled'] else '❌ Off'}")
            with col3:
                if run_config['tracing_enabled']:
                    st.info(f"📁 Project: `{run_config['project']}`")
        
        # Extract text from uploaded file
        raw_resume_text = detect_and_extract(uploaded_file.name, uploaded_file.read())[1]
        
        if not raw_resume_text or len(raw_resume_text.strip()) < 50:
            st.error("❌ Could not extract sufficient text from the resume. Please check the file.")
            st.stop()
        
        # Create tabs for results
        tab1, tab2, tab3, tab4 = st.tabs([
            "📄 Cleaned Resume",
            "✨ ATS-Optimized",
            "🎯 Final Refined",
            "📊 ATS Evaluation"
        ])
        
        # Run the pipeline with a spinner
        with st.spinner(f"🤖 Processing your resume with `{selected_model}`... This may take 2-3 minutes."):
            cleaned, rewritten, final_resume, evaluation = run_pipeline(
                raw_resume_text=raw_resume_text,
                job_title=job_title.strip(),
                job_description=job_description.strip()
            )
        
        # Display results in tabs
        with tab1:
            st.subheader("Cleaned Resume Text")
            st.markdown("This is your resume with formatting artifacts removed.")
            st.code(cleaned, language="markdown", line_numbers=False)
            st.download_button(
                "📥 Download Cleaned Resume",
                cleaned,
                file_name="cleaned_resume.txt",
                mime="text/plain"
            )
        
        with tab2:
            st.subheader("ATS-Optimized Version")
            st.markdown("Your resume rewritten with ATS-friendly keywords and formatting.")
            st.code(rewritten, language="markdown", line_numbers=False)
            st.download_button(
                "📥 Download ATS Version",
                rewritten,
                file_name="ats_optimized_resume.txt",
                mime="text/plain"
            )
        
        with tab3:
            st.subheader("Final Refined Resume")
            st.markdown("The polished version with high-impact bullet points.")
            st.code(final_resume, language="markdown", line_numbers=False)
            st.download_button(
                "📥 Download Final Resume",
                final_resume,
                file_name="final_resume.txt",
                mime="text/plain"
            )
        
        with tab4:
            st.subheader("ATS Evaluation & Recommendations")
            st.markdown("Detailed scoring and improvement suggestions.")
            st.code(evaluation, language="json", line_numbers=False)
            st.download_button(
                "📥 Download Evaluation",
                evaluation,
                file_name="ats_evaluation.json",
                mime="application/json"
            )
        
        # Success message
        st.success(f"✅ Pipeline completed successfully using `{selected_model}`!")
        
        if run_config['tracing_enabled']:
            st.info(f"🔍 View detailed traces in LangSmith project: **{run_config['project']}**")
    
    except Exception as e:
        st.error(f"❌ An error occurred during processing: {str(e)}")
        st.exception(e)
        st.info("💡 Try using a different model or check your API configuration.")