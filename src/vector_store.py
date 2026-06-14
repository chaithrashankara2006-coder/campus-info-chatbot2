from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

def create_vector_store(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ".", " "]
    )
    chunks = splitter.split_text(text)
    if not chunks:
        chunks = [text[:1000]]

    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )

    vector_store = FAISS.from_texts(chunks, embeddings)
    return vector_store

def search_context(vector_store, question, k=15):
    text = vector_store
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
    
    # Fallback: if nothing matched, send first 4000 chars of full text
    if not top:
        return text[:4000]
    
    return "\n".join(top)