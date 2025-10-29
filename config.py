import os
import sys
from dotenv import load_dotenv

def setup_environment():
    """
    Loads environment variables and sets up all necessary configurations.
    It will load from a .env file ONLY if not running inside a Docker container.
    """
    project_root = os.path.dirname(os.path.abspath(__file__))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    # Only load the .env file if not running inside a Docker container.
    if os.getenv("RUNNING_IN_DOCKER") != "true":
        print("--- Running in local mode. Loading .env file. ---")
        load_dotenv()
    else:
        print("--- Running in Docker mode. Skipping .env file load. ---")

    # Configure the environment for CrewAI to use Groq.
    # os.getenv() will read from the environment variables populated by
    # either load_dotenv() or Docker's --env-file.
    os.environ["OPENAI_API_KEY"] = os.getenv("GROQ_API_KEY")
    os.environ["OPENAI_API_BASE"] = "https://api.groq.com/openai/v1"
    os.environ["OPENAI_MODEL_NAME"] = os.getenv("OPENAI_MODEL_NAME", "llama-3.1-8b-instant")
    
    # Force tracing on and load the necessary LangSmith secrets.
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
    os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")
    os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
    
    # --- THIS LINE HAS BEEN REMOVED ---
    # The LANGSMITH_WORKSPACE_ID is no longer needed with a Personal Access Token.

# Run the setup function immediately when this module is imported.
setup_environment()