import PyPDF2
from langchain_text_splitters import RecursiveCharacterTextSplitter

def process_pdf(file_path):
    text = ""
    try:
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n\n"
        return text
    except Exception as e:
        print(f"PDF error: {str(e)}")
        return ""

def split_text(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ".", " "]
    )
    return splitter.split_text(text)