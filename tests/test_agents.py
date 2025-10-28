import pytest
from crewai import Agent
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents import build_parser_agent

def test_build_parser_agent_creation():
    """
    Tests if the parser agent can be instantiated successfully.
    This is a smoke test to ensure dependencies are correct and the agent definition is valid.
    """
    try:
        parser = build_parser_agent()
        assert isinstance(parser, Agent)
        assert parser.role == "Resume Parsing Specialist"
    except Exception as e:
        pytest.fail(f"Failed to create the parser agent: {e}")
