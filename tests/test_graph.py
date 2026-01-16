
from src.rag.graph_memory import KnowledgeGraph
from langchain_core.documents import Document

def test_graph():
    kg = KnowledgeGraph()
    
    # Mock data
    doc_name = "report.pdf"
    chunks = [
        Document(page_content="Nvidia revenue grew by 50% this quarter.", metadata={}),
        Document(page_content="The CEO mentioned strong demand for AI chips.", metadata={})
    ]
    
    print(f"Adding document: {doc_name}")
    kg.add_document(doc_name, chunks)
    
    stats = kg.get_stats()
    print(f"Graph Stats: {stats}")
    
    # Check structure
    if stats["nodes"] == 3: # 1 Doc + 2 Chunks
        print("✅ Node count correct.")
    else:
        print(f"❌ Unexpected node count: {stats['nodes']}")

    # Test 'Search'
    query = "revenue"
    print(f"Searching for '{query}'...")
    results = kg.search(query)
    
    if len(results) > 0:
        print(f"✅ Found {len(results)} match(es): {results}")
    else:
        print("❌ Search failed.")

if __name__ == "__main__":
    test_graph()
