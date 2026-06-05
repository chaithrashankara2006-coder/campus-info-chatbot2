import PyPDF2
from langchain_text_splitters import CharacterTextSplitter

def process_pdf(file_path):
    text = ""
    try:
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
        print(f"PDF read successfully: {file_path}")
        print(f"Text length: {len(text)}")
        return text
    except Exception as e:
        print(f"PDF error: {str(e)}")
        return ""

def split_text(text):
    splitter = CharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    return splitter.split_text(text)