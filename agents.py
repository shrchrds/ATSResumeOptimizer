from crewai import Agent

# No need to import or create an llm object here anymore.

def build_parser_agent():
    return Agent(role="Resume Parsing Specialist", goal="Extract clean, structured text from a resume.", backstory="You are an expert at cleaning resume text.", allow_delegation=False, verbose=True)
def build_ats_writer_agent():
    return Agent(role="ATS Optimization Writer", goal="Create a high-scoring ATS-optimized resume.", backstory="You are an expert at transforming resumes into ATS-friendly formats.", allow_delegation=False, verbose=True)
def build_evaluator_agent():
    return Agent(role="ATS Evaluator", goal="Provide accurate ATS scores and actionable recommendations.", backstory="You are a precise ATS scoring expert.", allow_delegation=False, verbose=True)
def build_refiner_agent():
    return Agent(role="Bullet Point Refiner", goal="Transform bullet points into high-impact, ATS-optimized statements.", backstory="You excel at creating powerful, quantified bullet points.", allow_delegation=False, verbose=True)