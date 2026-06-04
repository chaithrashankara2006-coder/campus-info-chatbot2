# 🎓 Campus Info Chatbot — PESCE

AI-powered campus information assistant for
PES College of Engineering, Mandya.

## Features
- Department-wise information for 16 departments
- PDF document processing
- Web scraping from college website
- FAISS vector search
- Library, Canteen, Hostel, Transport info
- Location and contact directory
- Dynamic quick question buttons

## Tech Stack
- Frontend: Streamlit
- AI: Groq LLaMA 3.3
- Vector DB: FAISS
- Embeddings: HuggingFace
- Web Scraping: BeautifulSoup
- PDF Processing: PyPDF2
- Framework: LangChain

## Setup Instructions

1. Clone repository:
   git clone https://github.com/chaithrashankara2006-coder/campus-info-chatbot

2. Create virtual environment:
   python -m venv venv
   venv\Scripts\activate

3. Install libraries:
   pip install -r requirements.txt

4. Create .env file:
   GROQ_API_KEY=your_key_here

5. Add PDFs to data/pdfs/ folder

6. Run:
   streamlit run app.py

## Project Structure
campus-chatbot/
├── app.py
├── requirements.txt
├── .env
├── README.md
├── data/
│   └── pdfs/
│       ├── CSE.pdf
│       ├── ECE.pdf
│       └── ...
└── src/
    ├── chatbot.py
    ├── document_processor.py
    ├── vector_store.py
    └── web_scraper.py

## Team Members
- Chaithra M S
- Afeefa Eram
- NithyaShree A H
- Prakruthi K T

## College
PES College of Engineering, Mandya, Karnataka
pesce.ac.in

## Architecture

User Query
    ↓
Streamlit UI
    ↓
FAISS Vector Search
    ↓
Context Retrieval
    ↓
Groq LLaMA 3.3 AI
    ↓
Answer displayed to user

Data Sources:
- Department PDFs → PyPDF2 → FAISS
- College Website → BeautifulSoup → FAISS