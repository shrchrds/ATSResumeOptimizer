"""
Test suite for config.py
Tests environment configuration and model setup
"""
import os
import pytest
from unittest.mock import patch, MagicMock


class TestEnvironmentSetup:
    """Test environment configuration"""
    
    def test_groq_api_key_is_set(self):
        """Verify GROQ_API_KEY is configured"""
        import config
        assert os.getenv("OPENAI_API_KEY") is not None, "GROQ_API_KEY not set"
    
    def test_openai_api_base_is_groq(self):
        """Verify API base points to Groq"""
        import config
        api_base = os.getenv("OPENAI_API_BASE")
        assert api_base == "https://api.groq.com/openai/v1", f"API base incorrect: {api_base}"
    
    def test_default_model_is_set(self):
        """Verify default model is configured"""
        import config
        model = os.getenv("OPENAI_MODEL_NAME")
        assert model is not None, "Model name not set"
        assert model in ["llama-3.1-8b-instant", "llama-3.3-70b-versatile"], f"Unexpected model: {model}"
    
    def test_langchain_tracing_configured(self):
        """Verify LangChain tracing is configured"""
        import config
        tracing = os.getenv("LANGCHAIN_TRACING_V2")
        # In CI it can be 'false', but it should be set
        assert tracing is not None, "LANGCHAIN_TRACING_V2 not set"
    
    def test_pythonpath_includes_project(self):
        """Verify project root is in PYTHONPATH"""
        import sys
        import config
        # Should be able to import config, which means path is correct
        assert 'config' in sys.modules


class TestConfigFunctions:
    """Test config.py functions"""
    
    def test_get_config_status_returns_dict(self):
        """Verify get_config_status returns proper structure"""
        import config
        status = config.get_config_status()
        
        assert isinstance(status, dict), "Status should be a dictionary"
        assert "groq_configured" in status, "Missing groq_configured key"
        assert "model" in status, "Missing model key"
        assert "tracing_enabled" in status, "Missing tracing_enabled key"
        assert "langsmith_key_set" in status, "Missing langsmith_key_set key"
        assert "langsmith_project" in status, "Missing langsmith_project key"
    
    def test_get_config_status_has_valid_values(self):
        """Verify config status has valid values"""
        import config
        status = config.get_config_status()
        
        # groq_configured should be True (we set dummy key in CI)
        assert status["groq_configured"] is True, "Groq should be configured"
        
        # model should be a string
        assert isinstance(status["model"], str), "Model should be a string"
        
        # tracing_enabled should be a boolean
        assert isinstance(status["tracing_enabled"], bool), "Tracing should be boolean"
    
    def test_configure_model_for_run(self):
        """Test model configuration function"""
        import config
        
        test_model = "llama-3.3-70b-versatile"
        result = config.configure_model_for_run(test_model)
        
        # Should return a dict with config info
        assert isinstance(result, dict), "Should return a dictionary"
        assert "model" in result, "Should contain model key"
        assert result["model"] == test_model, f"Model not set correctly: {result['model']}"
        
        # Verify environment was actually updated
        assert os.getenv("OPENAI_MODEL_NAME") == test_model, "Environment not updated"
    
    def test_configure_model_maintains_tracing(self):
        """Verify configure_model_for_run maintains tracing config"""
        import config
        
        # Set up tracing
        os.environ["LANGCHAIN_API_KEY"] = "test_key"
        os.environ["LANGCHAIN_TRACING_V2"] = "true"
        
        # Configure model
        result = config.configure_model_for_run("llama-3.1-8b-instant")
        
        # Tracing should still be configured
        assert result["tracing_enabled"] is True, "Tracing should remain enabled"
        assert os.getenv("LANGCHAIN_TRACING_V2") == "true", "Tracing env var lost"


class TestAgentBuilders:
    """Test agent builder functions"""
    
    def test_build_parser_agent(self):
        """Test parser agent creation"""
        from agents import build_parser_agent
        
        agent = build_parser_agent()
        assert agent is not None, "Agent should not be None"
        assert agent.role == "Resume Parsing Specialist", "Wrong role"
        assert agent.allow_delegation is False, "Should not allow delegation"
    
    def test_build_ats_writer_agent(self):
        """Test ATS writer agent creation"""
        from agents import build_ats_writer_agent
        
        agent = build_ats_writer_agent()
        assert agent is not None, "Agent should not be None"
        assert agent.role == "ATS Optimization Writer", "Wrong role"
        assert agent.allow_delegation is False, "Should not allow delegation"
    
    def test_build_evaluator_agent(self):
        """Test evaluator agent creation"""
        from agents import build_evaluator_agent
        
        agent = build_evaluator_agent()
        assert agent is not None, "Agent should not be None"
        assert agent.role == "ATS Evaluator", "Wrong role"
        assert agent.allow_delegation is False, "Should not allow delegation"
    
    def test_build_refiner_agent(self):
        """Test refiner agent creation"""
        from agents import build_refiner_agent
        
        agent = build_refiner_agent()
        assert agent is not None, "Agent should not be None"
        assert agent.role == "Bullet Point Refiner", "Wrong role"
        assert agent.allow_delegation is False, "Should not allow delegation"


class TestModelConfiguration:
    """Test model configuration and switching"""
    
    def test_can_switch_models(self):
        """Test switching between available models"""
        import config
        
        models = ["llama-3.1-8b-instant", "llama-3.3-70b-versatile"]
        
        for model in models:
            result = config.configure_model_for_run(model)
            assert result["model"] == model, f"Failed to set {model}"
            assert os.getenv("OPENAI_MODEL_NAME") == model, f"Env not updated for {model}"
    
    def test_model_configuration_is_persistent(self):
        """Verify model config persists in environment"""
        import config
        
        test_model = "llama-3.3-70b-versatile"
        config.configure_model_for_run(test_model)
        
        # Check multiple times
        for _ in range(3):
            assert os.getenv("OPENAI_MODEL_NAME") == test_model, "Model config not persistent"


class TestErrorHandling:
    """Test error handling in configuration"""
    
    def test_handles_missing_groq_key_gracefully(self):
        """Test behavior when GROQ_API_KEY is missing"""
        # Save original value
        original_key = os.getenv("OPENAI_API_KEY")
        
        try:
            # Remove the key
            if "OPENAI_API_KEY" in os.environ:
                del os.environ["OPENAI_API_KEY"]
            
            # Import should handle this gracefully or raise appropriate error
            import config
            status = config.get_config_status()
            
            # In CI, this might be set, so we just check it returns something
            assert isinstance(status, dict), "Should return status dict even with missing key"
            
        finally:
            # Restore original value
            if original_key:
                os.environ["OPENAI_API_KEY"] = original_key
    
    def test_handles_missing_langchain_key(self):
        """Test behavior when LANGCHAIN_API_KEY is missing"""
        original_key = os.getenv("LANGCHAIN_API_KEY")
        
        try:
            # Remove the key
            if "LANGCHAIN_API_KEY" in os.environ:
                del os.environ["LANGCHAIN_API_KEY"]
            
            import config
            status = config.get_config_status()
            
            # Should indicate tracing is disabled
            assert status["tracing_enabled"] is False, "Should disable tracing when key missing"
            
        finally:
            # Restore original value
            if original_key:
                os.environ["LANGCHAIN_API_KEY"] = original_key


@pytest.fixture
def clean_environment():
    """Fixture to provide clean environment for tests"""
    original_env = os.environ.copy()
    yield
    # Restore original environment after test
    os.environ.clear()
    os.environ.update(original_env)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])