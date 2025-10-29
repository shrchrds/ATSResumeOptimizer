# test_langsmith.py
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

print("--- Starting LangSmith Sanity Check ---")

# 1. Load environment variables from .env file
load_dotenv()
print("Loaded .env file.")

# 2. Manually set the OpenAI-compatible variables for Groq
os.environ["OPENAI_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["OPENAI_API_BASE"] = "https://api.groq.com/openai/v1"

# 3. Print LangSmith variables to confirm they are loaded
print(f"LANGCHAIN_TRACING_V2: {os.getenv('LANGCHAIN_TRACING_V2')}")
print(f"LANGCHAIN_PROJECT: {os.getenv('LANGCHAIN_PROJECT')}")
print(f"LANGCHAIN_API_KEY is set: {bool(os.getenv('LANGCHAIN_API_KEY'))}")

# 4. Initialize a LangChain object and make one call
# This action is what should trigger the trace.
try:
    print("\nInitializing ChatOpenAI and making a call...")
    llm = ChatOpenAI(model_name="llama-3.3-70b-versatile")
    response = llm.invoke("Hello, world!")
    print("Call successful. Response:", response.content)
    print("\n--- Sanity Check Complete ---")
    print("Check your LangSmith dashboard now for a project named 'ATS Resume Optimizer'.")
except Exception as e:
    print(f"\n--- ERROR DURING SANITY CHECK ---")
    print(f"An error occurred: {e}")
    print("Please double-check your GROQ_API_KEY and all LangSmith variables in the .env file.")