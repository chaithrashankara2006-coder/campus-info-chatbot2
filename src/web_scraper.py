import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(
            url,
            timeout=10,
            headers=headers
        )
        soup = BeautifulSoup(response.text, "html.parser")
        
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
            
        text = soup.get_text()
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        return "\n".join(lines[:500])
    except Exception as e:
        return f"Error: {str(e)}"