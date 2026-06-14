from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

def create_vector_store(text):
    return text

def search_context(vector_store, question, k=15):
    text = vector_store
    
    if not isinstance(text, str):
        text = str(text)
    
    question_lower = question.lower()
    
    paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
    keywords = question_lower.split()
    
    scored = []
    for para in paragraphs:
        para_lower = para.lower()
        score = sum(1 for kw in keywords if kw in para_lower)
        if score > 0:
            scored.append((score, para))
    
    scored.sort(reverse=True)
    top = [p for _, p in scored[:k]]
    
    if not top:
        return text[:4000]
    
    return "\n".join(top)