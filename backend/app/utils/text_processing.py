import tiktoken
from typing import List
import io

def count_tokens(text: str, model: str = "gpt-3.5-turbo") -> int:
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 150) -> List[str]:
    words = text.split()
    chunks = []
    
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk.strip():
            chunks.append(chunk)
        
        if i + chunk_size >= len(words):
            break
    
    return chunks

def extract_text_from_pdf(file_content: bytes) -> str:
    try:
        from pypdf import PdfReader
        reader = PdfReader(io.BytesIO(file_content))
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except ImportError:
        try:
            import PyPDF2
            reader = PyPDF2.PdfReader(io.BytesIO(file_content))
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
        except ImportError:
            return "PDF processing unavailable"
    except Exception as e:
        return f"PDF error: {str(e)}"

def extract_text_from_docx(file_content: bytes) -> str:
    try:
        from docx import Document
        doc = Document(io.BytesIO(file_content))
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except ImportError:
        return "DOCX processing unavailable"
    except Exception as e:
        return f"DOCX error: {str(e)}"

def extract_text_from_file(file_content: bytes, filename: str) -> str:
    ext = filename.lower()
    
    if ext.endswith('.pdf'):
        return extract_text_from_pdf(file_content)
    elif ext.endswith('.docx'):
        return extract_text_from_docx(file_content)
    elif ext.endswith(('.txt', '.md')):
        return file_content.decode('utf-8')
    else:
        try:
            return file_content.decode('utf-8')
        except UnicodeDecodeError:
            return file_content.decode('utf-8', errors='ignore')