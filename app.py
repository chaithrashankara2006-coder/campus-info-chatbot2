import streamlit as st
from src.chatbot import get_chatbot, ask_question
from src.web_scraper import scrape_website
from src.document_processor import process_pdf, split_text
from src.vector_store import create_vector_store, search_context

st.set_page_config(
    page_title="Campus Info Chatbot",
    page_icon="🎓"
)

st.title("🎓 Campus Info Chatbot")
st.write("Ask me anything about your campus!")

if "llm" not in st.session_state:
    st.session_state.llm = get_chatbot()

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "context" not in st.session_state:
    st.session_state.context = ""

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("📚 Load Campus Info")
    
    url = st.text_input("Enter college website URL:")
    if st.button("Load Website"):
        with st.spinner("Scraping website..."):
            text = scrape_website(url)
            st.session_state.vector_store = create_vector_store(text)
            st.success("Website loaded!")

    st.divider()
    
    uploaded_file = st.file_uploader(
        "Upload College Handbook (PDF)",
        type="pdf"
    )
    if uploaded_file:
        with open("data/uploaded.pdf", "wb") as f:
            f.write(uploaded_file.read())
        with st.spinner("Processing PDF..."):
            pdf_text = process_pdf("data/uploaded.pdf")
            st.session_state.vector_store = create_vector_store(
                pdf_text
            )
            st.success("PDF loaded!")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Ask about campus..."):
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            if st.session_state.vector_store:
                # Search relevant context from entire document
                context = search_context(
                    st.session_state.vector_store,
                    prompt
                )
            else:
                context = st.session_state.context

            response = ask_question(
                st.session_state.llm,
                context,
                prompt
            )
            st.write(response)
            st.session_state.messages.append(
                {"role": "assistant", "content": response}
            )