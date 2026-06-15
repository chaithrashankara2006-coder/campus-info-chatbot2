from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

def create_vector_store(text):
    return text

def search_context(vector_store, question, k=20):
    text = vector_store
    if not isinstance(text, str):
        text = str(text)

    question_lower = question.lower()

    # Split into paragraphs by double newline (better grouping)
    raw_paragraphs = text.split('\n')
    paragraphs = [p.strip() for p in raw_paragraphs if p.strip()]

    # Merge short lines with next line for better context
    merged = []
    buffer = ""
    for p in paragraphs:
        buffer += " " + p
        if len(buffer) > 80:
            merged.append(buffer.strip())
            buffer = ""
    if buffer:
        merged.append(buffer.strip())

    import string
    keywords = [w.strip(string.punctuation) for w in question_lower.split()]
    keywords = [w for w in keywords if len(w) > 2]
    # Add synonym expansion for common terms
    synonym_map = {
        "hod": ["head of department", "hod", "head"],
        "head": ["head of department", "hod"],
        "contact": ["email", "phone", "mobile", "contact"],
        "faculty": ["professor", "assistant professor", "associate professor", "faculty"],
    }
    expanded_keywords = set(keywords)
    for kw in keywords:
        if kw in synonym_map:
            expanded_keywords.update(synonym_map[kw])

    scored = []
    for para in merged:
        para_lower = para.lower()
        score = sum(1 for kw in expanded_keywords if kw in para_lower)

        
        # Strong boost for HOD-related queries
        if "hod" in expanded_keywords or "head" in expanded_keywords:
            has_hod_term = "head of department" in para_lower or "hod" in para_lower
            has_name = "dr." in para_lower or para_lower.strip().startswith("hod")
            if has_hod_term and has_name:
                score += 25
            elif has_hod_term:
                score += 5

        if score > 0:
            scored.append((score, para))

    scored.sort(reverse=True)
    top = [p for _, p in scored[:k]]

    if not top:
        return text[:5000]

    return "\n".join(top)