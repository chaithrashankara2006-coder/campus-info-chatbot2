import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, timeout=10, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
            
        text = soup.get_text()
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        
        # Combine into paragraph-sized chunks instead of single short lines
        combined = []
        buffer = ""
        for line in lines[:500]:
            buffer += " " + line
            if len(buffer) > 200:
                combined.append(buffer.strip())
                buffer = ""
        if buffer:
            combined.append(buffer.strip())
        
        return "\n".join(combined)
    except Exception as e:
        return f"Error: {str(e)}"