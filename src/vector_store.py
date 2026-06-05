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

def search_context(vector_store, question, k=8):
    results = vector_store.similarity_search(question, k=k)
    context = "\n".join([doc.page_content for doc in results])
    return context