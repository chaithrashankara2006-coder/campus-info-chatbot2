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
        if len(buffer) > 150:
            merged.append(buffer.strip())
            buffer = ""
    if buffer:
        merged.append(buffer.strip())

    keywords = [w for w in question_lower.split() if len(w) > 2]

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
        if score > 0:
            scored.append((score, para))

    scored.sort(reverse=True)
    top = [p for _, p in scored[:k]]

    if not top:
        return text[:5000]

    return "\n".join(top)