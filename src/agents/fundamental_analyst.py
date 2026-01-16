
from typing import TypedDict, List
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from src.rag.pdf_loader import load_pdf_chunks
from src.rag.graph_memory import KnowledgeGraph

# Global Memory for this educational example (Persists while server is running)
# In production, this would be an external database.
MEMORY = KnowledgeGraph()

# 1. Define State
class FundamentalState(TypedDict):
    messages: List[BaseMessage]
    file_path: str
    query: str
    analysis: str

# 2. Define Tools
@tool
def ingest_file_tool(file_path: str) -> str:
    """Read a PDF file and store it in memory."""
    try:
        chunks = load_pdf_chunks(file_path)
        if not chunks:
            return "No text found in PDF."
        MEMORY.add_document(file_path, chunks)
        return f"Successfully ingested {len(chunks)} text chunks from {file_path}."
    except Exception as e:
        return f"Error ingesting file: {str(e)}"

@tool
def query_memory_tool(query: str) -> str:
    """Search the knowledge graph for relevant information."""
    results = MEMORY.search(query)
    if not results:
        return "No relevant information found in memory."
    
    # Format results for the LLM
    context = "\n".join([f"- {r.get('content')}" for r in results[:5]]) # Limit to 5 chunks
    return context

# 3. Define Node
def fundamental_agent_node(state: FundamentalState):
    """
    Agent that reads files and answers questions.
    """
    messages = state["messages"]
    
    # Initialize LLM
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    llm_with_tools = llm.bind_tools([ingest_file_tool, query_memory_tool])
    
    # System Prompt
    system_prompt = """You are a Fundamental Analyst.
    Your goal is to answer questions based on the documents you have read.
    1. If the user asks you to read a file, use `ingest_file_tool`.
    2. If the user asks a question, use `query_memory_tool` to find the answer.
    3. Synthesize the findings into a clear answer.
    """
    
    if not messages:
        messages = [HumanMessage(content=system_prompt)]
        
    response = llm_with_tools.invoke(messages)
    return {"messages": messages + [response]}
