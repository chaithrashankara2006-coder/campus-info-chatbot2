from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import CharacterTextSplitter

def create_vector_store(text):
    # Split text into chunks
    splitter = CharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_text(text)
    
    # Create embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )
    
    # Create FAISS vector store
    vector_store = FAISS.from_texts(chunks, embeddings)
    return vector_store

def search_context(vector_store, question, k=5):
    results = vector_store.similarity_search(question, k=k)
    context = "\n".join([doc.page_content for doc in results])
    return context
