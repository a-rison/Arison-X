
from src.agents.workflow import run_workflow
from unittest.mock import MagicMock, patch

@patch('src.agents.technical_analyst.ChatOpenAI')
def test_workflow_structure(MockChatOpenAI):
    # Setup mock
    mock_llm = MagicMock()
    mock_llm.bind_tools.return_value.invoke.return_value.content = "Workflow Analysis: STRONG BUY."
    MockChatOpenAI.return_value = mock_llm

    print("Testing Workflow Structure...")
    result = run_workflow("MSFT")
    print(f"Final Report: {result}")
    
    if "STRONG BUY" in result:
        print("✅ Workflow structure verification passed.")
    else:
        print("❌ Workflow did not return expected mocked content.")

if __name__ == "__main__":
    test_workflow_structure()
