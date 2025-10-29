import os
import sys
from dotenv import load_dotenv

def setup_environment():
    """
    Loads and sets up all necessary environment variables for the application to run.
    This is called once when the module is imported.
    """
    project_root = os.path.dirname(os.path.abspath(__file__))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    
    # Load environment variables from .env file (only if not in Docker)
    if os.getenv("RUNNING_IN_DOCKER") != "true":
        load_dotenv()
    
    # Configure Groq API (OpenAI-compatible endpoint)
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        raise ValueError("GROQ_API_KEY is not set in environment variables")
    
    os.environ["OPENAI_API_KEY"] = groq_api_key
    os.environ["OPENAI_API_BASE"] = "https://api.groq.com/openai/v1"
    
    # Set default model (can be overridden by configure_model_for_run)
    os.environ.setdefault("OPENAI_MODEL_NAME", "llama-3.1-8b-instant")
    
    # Configure LangSmith Tracing
    langchain_api_key = os.getenv("LANGCHAIN_API_KEY")
    if not langchain_api_key:
        print("WARNING: LANGCHAIN_API_KEY not set. Tracing will be disabled.")
        os.environ["LANGCHAIN_TRACING_V2"] = "false"
    else:
        os.environ["LANGCHAIN_TRACING_V2"] = "true"
        os.environ["LANGCHAIN_API_KEY"] = langchain_api_key
        os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT", "ats-resume-agent")
        os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
    
    # Remove workspace ID if present (not needed for Personal Access Token)
    if "LANGSMITH_WORKSPACE_ID" in os.environ:
        del os.environ["LANGSMITH_WORKSPACE_ID"]

def configure_model_for_run(model_name: str):
    """
    Reconfigures the environment to use a specific model for the next crew run.
    This MUST be called before running the crew to ensure proper model selection and tracing.
    
    Args:
        model_name: The Groq model name to use (e.g., "llama-3.1-8b-instant")
    """
    # Set the model name
    os.environ["OPENAI_MODEL_NAME"] = model_name
    
    # Re-assert LangSmith tracing configuration to ensure it's active
    # This is critical because CrewAI may reinitialize the LLM
    langchain_api_key = os.getenv("LANGCHAIN_API_KEY")
    if langchain_api_key:
        os.environ["LANGCHAIN_TRACING_V2"] = "true"
        os.environ["LANGCHAIN_API_KEY"] = langchain_api_key
        os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT", "ats-resume-agent")
        os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
    
    return {
        "model": os.environ["OPENAI_MODEL_NAME"],
        "tracing_enabled": os.environ.get("LANGCHAIN_TRACING_V2") == "true",
        "project": os.environ.get("LANGCHAIN_PROJECT"),
    }

def get_config_status():
    """
    Returns the current configuration status for debugging.
    """
    return {
        "groq_configured": bool(os.getenv("OPENAI_API_KEY")),
        "model": os.getenv("OPENAI_MODEL_NAME"),
        "tracing_enabled": os.getenv("LANGCHAIN_TRACING_V2") == "true",
        "langsmith_key_set": bool(os.getenv("LANGCHAIN_API_KEY")),
        "langsmith_project": os.getenv("LANGCHAIN_PROJECT"),
    }

# Initialize environment on module import
setup_environment()