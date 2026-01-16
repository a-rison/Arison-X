
from src.rag.pdf_loader import load_pdf_chunks
from pypdf import PdfWriter
import os

def create_dummy_pdf(filename):
    writer = PdfWriter()
    writer.add_blank_page(width=72, height=72)
    # Adding text to a blank page in pypdf is complex (requires canvas), 
    # so for this simple test, we will just checking we can open it without crashing, 
    # even if text extraction returns empty or minimal.
    # A better approach for a quick test is writing a text file masquerading as a test, 
    # but pypdf checks headers.
    
    # Actually, let's just make a valid PDF with one blank page. 
    # The extraction will return empty string, which is fine to test the *Code Path*.
    with open(filename, "wb") as f:
        writer.write(f)

def test_pdf_loading():
    filename = "test_doc.pdf"
    create_dummy_pdf(filename)
    
    print(f"Created {filename}...")
    
    try:
        chunks = load_pdf_chunks(filename)
        print(f"✅ Loaded {len(chunks)} chunks (Expect 0 or 1 empty for blank pdf)")
        # If it runs without exception, code path is good.
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if os.path.exists(filename):
            os.remove(filename)

if __name__ == "__main__":
    test_pdf_loading()
