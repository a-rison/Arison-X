
from src.agents.workflow import run_workflow
from unittest.mock import MagicMock, patch

@patch('src.agents.technical_analyst.ChatOpenAI')
@patch('src.agents.fundamental_analyst.ChatOpenAI')
def test_full_workflow(MockFundLLM, MockTechLLM):
    # Mock Fundamental Agent
    mock_fund = MagicMock()
    mock_fund.bind_tools.return_value.invoke.return_value.content = "Fundamental Report: Revenue is up 10% per the PDF."
    MockFundLLM.return_value = mock_fund

    # Mock Technical Agent (should not be called for this test, but just in case)
    mock_tech = MagicMock()
    mock_tech.bind_tools.return_value.invoke.return_value.content = "Technical Report: RSI is 50."
    MockTechLLM.return_value = mock_tech

    print("Testing Fundamental Routing...")
    # Trigger routing with "read report"
    result = run_workflow("NVDA", task="read the annual report for")
    
    print(f"Final Report: {result}")
    
    if "Fundamental Report" in result:
        print("✅ Correctly routed to Fundamental Analyst.")
    elif "Technical Report" in result:
        print("❌ Incorrectly routed to Technical Analyst.")
    else:
        print("❌ Workflow failed to produce expected output.")

if __name__ == "__main__":
    test_full_workflow()
