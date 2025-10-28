from crewai import Task

# This task is the first in the sequence, so it takes the raw text directly. No changes needed here.
def parse_resume_task(agent, raw_resume_text):
    return Task(
        description=(
            f"Clean and parse the following raw resume text. Remove any formatting artifacts, "
            f"normalize bullet points to use a simple hyphen '-', and ensure all meaningful content "
            f"like contact information, experience, skills, and education is preserved in a clean, "
            f"structured plain text format. Be fast and direct.\n\n"
            f"Raw Resume Text:\n--- START ---\n{raw_resume_text}\n--- END ---"
        ),
        agent=agent,
        expected_output="The full, cleaned, and structured resume text, ready for analysis."
    )

# --- MODIFIED FUNCTION ---
# It no longer takes `cleaned_resume_text`. It now takes `context` which will be the `t_parse` task.
def rewrite_for_ats_task(agent, job_title, job_description, context):
    return Task(
        description=(
            f"Using the cleaned resume text from the previous step, rewrite it to be highly optimized "
            f"for an Applicant Tracking System (ATS) for the job title of '{job_title}'.\n\n"
            f"Here is the target job description:\n--- START ---\n{job_description}\n--- END ---\n\n"
            f"Your task is to strategically integrate relevant keywords from the job description, "
            f"use strong action verbs to start bullet points, and quantify achievements wherever possible. "
            f"The goal is a resume that would score above 80 points in an ATS."
        ),
        agent=agent,
        expected_output="A fully rewritten, ATS-optimized resume in plain text format.",
        # This tells CrewAI that this task depends on the output of the task(s) in the context list.
        context=context
    )

# --- MODIFIED FUNCTION ---
# It no longer takes `rewritten_resume_text`. It now takes `context` which will be the `t_rewrite` task.
def refine_bullets_task(agent, context):
    return Task(
        description=(
            "Review the ATS-optimized resume from the previous step. Your specific goal is to "
            "refine and enhance the bullet points in the 'Work Experience' section. "
            "Transform them into high-impact statements using the STAR (Situation, Task, Action, Result) method where appropriate. "
            "Ensure each bullet point starts with a powerful action verb and includes quantifiable metrics "
            "(e.g., percentages, dollar amounts, time saved) to demonstrate clear achievements. "
            "Return the full resume with only the bullet points improved."
        ),
        agent=agent,
        expected_output="The final version of the resume with polished, metric-driven bullet points.",
        context=context
    )

# --- MODIFIED FUNCTION ---
# It no longer takes `final_resume_text`. It now takes `context` which will be the `t_refine` task.
def evaluate_ats_task(agent, job_title, job_description, context):
    return Task(
        description=(
            f"Evaluate the final, refined resume from the previous step against the job description "
            f"for the role of '{job_title}'. Perform a detailed ATS-style analysis.\n\n"
            f"Target Job Description:\n--- START ---\n{job_description}\n--- END ---\n\n"
            "Your output MUST be a single, clean JSON object. Do not add any text before or after the JSON. "
            "The JSON object must have the following keys:\n"
            "1. 'overall_score': An integer from 0 to 100.\n"
            "2. 'score_breakdown': A JSON object with integer scores (1-5) for 'keyword_match', 'structure', 'metrics_quantification', and 'action_verbs'.\n"
            "3. 'missing_keywords': A list of 5-10 important keywords from the job description that are missing from the resume.\n"
            "4. 'quick_wins': A list of 2-3 specific, actionable recommendations for immediate improvement."
        ),
        agent=agent,
        expected_output="A single JSON object with the complete ATS evaluation, including score, breakdown, and recommendations.",
        context=context
    )