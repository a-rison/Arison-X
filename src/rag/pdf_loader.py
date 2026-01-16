
from pypdf import PdfReader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List

def load_pdf_chunks(file_path: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[Document]:
    """
    Load a PDF file and split it into chunks.
    
    Args:
        file_path: Path to the PDF file.
        chunk_size: Size of each text chunk.
        chunk_overlap: Overlap between chunks to maintain context.
        
    Returns:
        List[Document]: List of LangChain Document objects.
    """
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
            
        # Split text into chunks
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )
        
        # Create Document objects (simulating what a real loader does)
        # In a real app, we might want to track page numbers per chunk
        chunks = splitter.create_documents([text])
        
        # Add metadata source
        for chunk in chunks:
            chunk.metadata["source"] = file_path
            
        return chunks
        
    except Exception as e:
        print(f"Error loading PDF: {e}")
        return []
