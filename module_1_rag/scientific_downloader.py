import urllib.request
import xml.etree.ElementTree as ET
import os

def fetch_arxiv_automotive_papers(topic="electric vehicle battery insulation ISO 26262", max_results=3):
    """Busca publicações científicas reais no arXiv e indexa na knowledge base."""
    base_url = "http://export.arxiv.org/api/query?"
    query = f"search_query=all:{urllib.parse.quote(topic)}&start=0&max_results={max_results}"
    
    print(f"[RAG Crawler] Consultando literatura científica no arXiv para: '{topic}'...")
    try:
        req = urllib.request.Request(base_url + query, headers={'User-Agent': 'MarleyOS/2.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            xml_data = response.read()
        
        root = ET.fromstring(xml_data)
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        
        kb_path = os.path.join(os.path.dirname(__file__), "knowledge_base", "arxiv_scientific_papers.txt")
        os.makedirs(os.path.dirname(kb_path), exist_ok=True)
        
        saved = 0
        with open(kb_path, "w", encoding="utf-8") as f:
            for entry in root.findall('atom:entry', ns):
                title = entry.find('atom:title', ns).text.strip().replace("\n", " ")
                summary = entry.find('atom:summary', ns).text.strip().replace("\n", " ")
                f.write(f"[ARTIGO CIENTÍFICO: {title}]\n{summary}\n\n")
                saved += 1
                
        print(f"[RAG Crawler] {saved} artigos científicos reais indexados em {kb_path}!")
    except Exception as e:
        print(f"[RAG Crawler] Aviso: Falha na conexão externa ({e}). Usando literatura padrão.")

if __name__ == "__main__":
    fetch_arxiv_automotive_papers()
