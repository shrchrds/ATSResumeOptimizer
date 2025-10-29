from crewai import Agent

def build_parser_agent():
    """
    Creates a Resume Parsing Specialist agent.
    
    This agent extracts and cleans text from resumes, removing formatting
    artifacts and ensuring the content is properly structured.
    """
    return Agent(
        role="Resume Parsing Specialist",
        goal="Extract clean, structured text from a resume.",
        backstory="You are an expert at cleaning resume text and removing formatting artifacts.",
        allow_delegation=False,
        verbose=True
    )

def build_ats_writer_agent():
    """
    Creates an ATS Optimization Writer agent.
    
    This agent rewrites resumes to be ATS-friendly by incorporating
    relevant keywords and optimizing formatting for applicant tracking systems.
    """
    return Agent(
        role="ATS Optimization Writer",
        goal="Create a high-scoring ATS-optimized resume.",
        backstory="You are an expert in ATS formats and keyword optimization for applicant tracking systems.",
        allow_delegation=False,
        verbose=True
    )

def build_evaluator_agent():
    """
    Creates an ATS Evaluator agent.
    
    This agent scores resumes based on ATS criteria and provides
    actionable recommendations for improvement.
    """
    return Agent(
        role="ATS Evaluator",
        goal="Provide accurate ATS scores and actionable recommendations.",
        backstory="A precise ATS scoring expert with deep knowledge of applicant tracking systems.",
        allow_delegation=False,
        verbose=True
    )

def build_refiner_agent():
    """
    Creates a Bullet Point Refiner agent.
    
    This agent transforms bullet points into high-impact statements
    using action verbs, quantified achievements, and compelling language.
    """
    return Agent(
        role="Bullet Point Refiner",
        goal="Transform bullet points into high-impact statements.",
        backstory="Expert in creating powerful, quantified bullet points that showcase achievements and drive results.",
        allow_delegation=False,
        verbose=True
    )