
import networkx as nx
from typing import List, Dict
from langchain_core.documents import Document

class KnowledgeGraph:
    def __init__(self):
        # We use a directed graph to show relationships (e.g., Chunk -> extracted from -> Document)
        self.graph = nx.DiGraph()

    def add_document(self, file_path: str, chunks: List[Document]):
        """
        Add a document and its chunks to the graph.
        """
        # Node 1: The Document itself
        self.graph.add_node(file_path, type="document", label=file_path)
        
        for i, chunk in enumerate(chunks):
            # Node 2: The Chunk
            chunk_id = f"{file_path}_chunk_{i}"
            # In a real app, we would embed the 'page_content' into a vector DB
            # Here we just store it in the graph node
            self.graph.add_node(chunk_id, type="chunk", content=chunk.page_content[:50] + "...")
            
            # Edge: Chunk BELONGS_TO Document
            self.graph.add_edge(chunk_id, file_path, relation="extracted_from")

    def search(self, query: str) -> List[Dict]:
        """
        Simulate a semantic search (keyword matching for this simple version).
        In a real app, this would query a Vector DB.
        """
        results = []
        for node, data in self.graph.nodes(data=True):
            if data.get("type") == "chunk":
                # Very naive keyword match
                if query.lower() in data.get("content", "").lower():
                    results.append(data)
        return results

    def get_stats(self):
        return {
            "nodes": self.graph.number_of_nodes(),
            "edges": self.graph.number_of_edges()
        }
