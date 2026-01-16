
from typing import TypedDict, List
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import StateGraph, END
from src.agents.technical_analyst import analyst_node, AnalystState
from src.agents.fundamental_analyst import fundamental_agent_node, FundamentalState

# For this educational implementation, we will build a simple "Team"
# Supervisor -> Analyst -> End
# In a real app, the supervisor would route to different agents (Fundamental, Sentiment, etc.)

class AgentState(TypedDict):
    messages: List[BaseMessage]
    symbol: str
    final_report: str

def supervisor_node(state: AgentState):
    """
    The Supervisor determines what to do next.
    In this simple version, it just acts as a router based on existing state.
    """
    # We do NOT want to overwrite the user's initial message here.
    return {}

def report_node(state: AnalystState):
    """
    Format the final output.
    """
    last_message = state["messages"][-1]
    return {"final_report": last_message.content}

# Create the graph
workflow = StateGraph(AgentState)

# Add Nodes
workflow.add_node("supervisor", supervisor_node)
workflow.add_node("technical_analyst", analyst_node)
workflow.add_node("fundamental_analyst", fundamental_agent_node)
workflow.add_node("reporter", report_node)

# Conditional Logic
def route_supervisor(state: AgentState):
    # Simple keyword-based routing for demo
    # In reality, this would be an LLM call deciding the path
    msg = state['messages'][-1].content.lower() if state['messages'] else ""
    if "read" in msg or "report" in msg or "fundamental" in msg:
        return "fundamental_analyst"
    else:
        return "technical_analyst"

# Add Edges
workflow.set_entry_point("supervisor")
workflow.add_conditional_edges(
    "supervisor",
    route_supervisor,
    {
        "technical_analyst": "technical_analyst",
        "fundamental_analyst": "fundamental_analyst"
    }
)
workflow.add_edge("technical_analyst", "reporter")
workflow.add_edge("fundamental_analyst", "reporter")
workflow.add_edge("reporter", END)

app = workflow.compile()

def run_workflow(symbol: str, task: str = "analyze"):
    print(f"--- Starting Workflow for {symbol} ---")
    
    # Pre-seed the conversation with the user's intent
    initial_content = f"Please {task} {symbol}"
    
    initial_state = {
        "messages": [HumanMessage(content=initial_content)],
        "symbol": symbol,
        "final_report": ""
    }
    result = app.invoke(initial_state)
    return result["final_report"]
