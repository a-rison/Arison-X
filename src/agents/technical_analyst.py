
from typing import TypedDict, List
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from src.tools.market_data import get_technical_indicators, TechnicalIndicators

# 1. Define State
class AnalystState(TypedDict):
    messages: List[BaseMessage]
    symbol: str
    analysis: str

# 2. Define Tools available to the agent
@tool
def get_indicators_tool(symbol: str) -> str:
    """Fetch technical indicators (RSI, SMA, EMA) for a stock symbol."""
    try:
        data = get_technical_indicators(symbol)
        return str(data.model_dump())
    except Exception as e:
        return f"Error: {str(e)}"

# 3. Define the Node (The Agent's Logic)
def analyst_node(state: AnalystState):
    """
    The node responsible for analyzing the stock.
    """
    symbol = state["symbol"]
    messages = state["messages"]

    # Initialize LLM (assuming Environment variables are set)
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    
    # Bind tools
    llm_with_tools = llm.bind_tools([get_indicators_tool])

    # System prompt to guide behavior
    system_prompt = f"""You are a Technical Analyst. 
    Your goal is to analyze the stock: {symbol}.
    1. Use the `get_indicators_tool` to get fresh data.
    2. Analyze the RSI and Moving Averages.
    3. Provide a recommendation: BUY, SELL, or HOLD based on standard technical analysis rules.
    """

    if not messages:
        messages = [HumanMessage(content=system_prompt)]
    
    response = llm_with_tools.invoke(messages)
    
    # Append response to history
    return {"messages": messages + [response]}

# 4. Define Graph
workflow = StateGraph(AnalystState)
workflow.add_node("analyst", analyst_node)
workflow.set_entry_point("analyst")
workflow.add_edge("analyst", END) # Simple 1-step agent for now

app = workflow.compile()

# Helper function to run it
def run_analysis(symbol: str):
    print(f"--- Starting Analysis for {symbol} ---")
    initial_state = {
        "messages": [],
        "symbol": symbol,
        "analysis": ""
    }
    result = app.invoke(initial_state)
    last_message = result["messages"][-1]
    return last_message.content
