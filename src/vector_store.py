from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import CharacterTextSplitter

def create_vector_store(text):
    splitter = CharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = splitter.split_text(text)
    
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )
    
    vector_store = FAISS.from_texts(chunks, embeddings)
    return vector_store

def search_context(vector_store, question, k=10):
    # Search with original question
    results = vector_store.similarity_search(question, k=k)
    
    # Also search with keywords
    keywords = ["HOD", "Head of Department", "contact", "faculty", "professor"]
    for keyword in keywords:
        if keyword.lower() in question.lower():
            extra = vector_store.similarity_search(keyword, k=3)
            results += extra
    
    context = "\n".join([doc.page_content for doc in results])
    return context