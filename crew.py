import os
from crewai import Crew, Process
from langsmith import traceable
from agents import (
    build_parser_agent,
    build_ats_writer_agent,
    build_evaluator_agent,
    build_refiner_agent
)
from tasks import (
    parse_resume_task,
    rewrite_for_ats_task,
    evaluate_ats_task,
    refine_bullets_task
)

@traceable(run_type="chain", name="ATS Resume Pipeline")
def run_pipeline(raw_resume_text: str, job_title: str, job_description: str):
    """
    Executes the complete ATS resume optimization pipeline.
    
    This function is decorated with @traceable to ensure all operations
    are properly tracked in LangSmith for monitoring and debugging.
    
    Args:
        raw_resume_text: The raw text extracted from the resume file
        job_title: The target job title for optimization
        job_description: The full job description to optimize against
    
    Returns:
        tuple: (cleaned_text, rewritten_text, final_resume, evaluation)
    """
    # Log the model being used for this run
    model_name = os.getenv("OPENAI_MODEL_NAME", "unknown")
    print(f"\n{'='*60}")
    print(f"🚀 Starting ATS Pipeline with model: {model_name}")
    print(f"📊 LangSmith Tracing: {os.getenv('LANGCHAIN_TRACING_V2', 'not set')}")
    print(f"📁 LangSmith Project: {os.getenv('LANGCHAIN_PROJECT', 'not set')}")
    print(f"{'='*60}\n")
    
    # Build all agents
    parser = build_parser_agent()
    writer = build_ats_writer_agent()
    refiner = build_refiner_agent()
    evaluator = build_evaluator_agent()
    
    # Create all tasks with proper context chaining
    t_parse = parse_resume_task(parser, raw_resume_text)
    t_rewrite = rewrite_for_ats_task(writer, job_title, job_description, context=[t_parse])
    t_refine = refine_bullets_task(refiner, context=[t_rewrite])
    t_eval = evaluate_ats_task(evaluator, job_title, job_description, context=[t_refine])
    
    # Create and execute the crew
    # The crew automatically picks up the LLM configuration from environment variables
    crew = Crew(
        agents=[parser, writer, refiner, evaluator],
        tasks=[t_parse, t_rewrite, t_refine, t_eval],
        process=Process.sequential,
        verbose=True
    )
    
    # Execute the crew
    try:
        result = crew.kickoff()
        print(f"\n✅ Pipeline completed successfully with {model_name}\n")
    except Exception as e:
        print(f"\n❌ Pipeline failed with error: {str(e)}\n")
        raise
    
    # Extract outputs from each task
    cleaned = t_parse.output.raw if t_parse.output else "Parsing failed."
    rewritten = t_rewrite.output.raw if t_rewrite.output else "Rewriting failed."
    final_resume = t_refine.output.raw if t_refine.output else "Refining failed."
    evaluation = t_eval.output.raw if t_eval.output else "Evaluation failed."
    
    return cleaned, rewritten, final_resume, evaluation