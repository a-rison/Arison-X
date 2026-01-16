
from src.agents.technical_analyst import run_analysis
from unittest.mock import MagicMock, patch

# Mock OpenAI to avoid needing real keys for this structural test
@patch('src.agents.technical_analyst.ChatOpenAI')
def test_agent_structure(MockChatOpenAI):
    # Setup mock response
    mock_llm = MagicMock()
    mock_llm.bind_tools.return_value.invoke.return_value.content = "Analysis: RSI is 30. BUY."
    MockChatOpenAI.return_value = mock_llm

    print("Testing Agent Structure (Mocked LLM)...")
    result = run_analysis("AAPL")
    print(f"Result: {result}")
    
    if "BUY" in result:
        print("✅ Agent structure verification passed.")
    else:
        print("❌ Agent did not return expected mocked content.")

if __name__ == "__main__":
    test_agent_structure()
