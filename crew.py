from crewai import Crew, Process
# --- THIS IS THE KEY IMPORT FROM THE DOCUMENTATION ---
from langsmith import traceable
from agents import build_parser_agent, build_ats_writer_agent, build_evaluator_agent, build_refiner_agent
from tasks import parse_resume_task, rewrite_for_ats_task, evaluate_ats_task, refine_bullets_task

# --- THIS DECORATOR IS THE SOLUTION ---
@traceable(run_type="chain", name="ATS Resume Pipeline")
def run_pipeline(raw_resume_text: str, job_title: str, job_description: str):
    """
    This function is now decorated to be explicitly traced by LangSmith.
    """
    parser = build_parser_agent()
    writer = build_ats_writer_agent()
    refiner = build_refiner_agent()
    evaluator = build_evaluator_agent()

    t_parse = parse_resume_task(parser, raw_resume_text)
    t_rewrite = rewrite_for_ats_task(writer, job_title, job_description, context=[t_parse])
    t_refine = refine_bullets_task(refiner, context=[t_rewrite])
    t_eval = evaluate_ats_task(evaluator, job_title, job_description, context=[t_refine])

    # The Crew will automatically pick up the LLM configuration from the environment.
    crew = Crew(
        agents=[parser, writer, refiner, evaluator],
        tasks=[t_parse, t_rewrite, t_refine, t_eval],
        process=Process.sequential,
        verbose=True
    )
    
    result = crew.kickoff()
    
    cleaned = t_parse.output.raw if t_parse.output else "Parsing failed."
    rewritten = t_rewrite.output.raw if t_rewrite.output else "Rewriting failed."
    final_resume = t_refine.output.raw if t_refine.output else "Refining failed."
    evaluation = t_eval.output.raw if t_eval.output else "Evaluation failed."
    
    return cleaned, rewritten, final_resume, evaluation