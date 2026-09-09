import csv
import json
import os
import re
import math
from collections import Counter

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCES_CSV_PATH = os.path.join(ROOT_DIR, "module_1_rag", "data", "automotive_sources.csv")
SOURCES_JSONL_PATH = os.path.join(ROOT_DIR, "module_1_rag", "data", "automotive_sources.jsonl")

def tokenize(text):
    return re.findall(r'\w+', text.lower())

def cosine_similarity(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])
    sum1 = sum([val**2 for val in vec1.values()])
    sum2 = sum([val**2 for val in vec2.values()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)
    return float(numerator) / denominator if denominator else 0.0

def load_documents():
    docs = []
    csv_path = os.path.join(ROOT_DIR, "module_1_rag", "data", "obd_dtc_codes.csv")
    manual_path = os.path.join(ROOT_DIR, "module_1_rag", "data", "powertrain_manual.txt")
    
    if os.path.exists(csv_path):
        with open(csv_path, 'r', encoding='utf-8') as f:
            for line in f.readlines()[1:]:
                parts = line.strip().split(',')
                if len(parts) >= 5:
                    docs.append(f"DTC: {parts[0]} | Componente: {parts[1]} | Causa: {parts[2]} | Acao: {parts[4]}")

    if os.path.exists(manual_path):
        with open(manual_path, 'r', encoding='utf-8') as f:
            docs.append(f.read().strip())
            
    return docs


def load_source_registry(csv_path=SOURCES_CSV_PATH, jsonl_path=SOURCES_JSONL_PATH):
    """Load the curated source catalog, preferring CSV and falling back to JSONL."""
    if os.path.exists(csv_path):
        with open(csv_path, 'r', encoding='utf-8', newline='') as source_file:
            sources = list(csv.DictReader(source_file))
        for source in sources:
            source["subdomain"] = [item.strip() for item in source.get("subdomain", "").split(";") if item.strip()]
        return sources

    if os.path.exists(jsonl_path):
        with open(jsonl_path, 'r', encoding='utf-8') as source_file:
            return [json.loads(line) for line in source_file if line.strip()]

    return []


def search_sources(query, max_results=5):
    query_tokens = set(tokenize(query))
    ranked = []
    for source in load_source_registry():
        searchable = " ".join([
            source.get("name", ""),
            source.get("domain", ""),
            " ".join(source.get("subdomain", [])),
            source.get("notes", ""),
        ]).lower()
        score = sum(token in searchable for token in query_tokens)
        if score:
            ranked.append((score, int(source.get("priority", 999)), source))

    ranked.sort(key=lambda item: (-item[0], item[1]))
    return [source for _, _, source in ranked[:max_results]]

def retrieve(query, documents, k=2):
    query_vec = Counter(tokenize(query))
    scored = []
    for doc in documents:
        doc_vec = Counter(tokenize(doc))
        score = cosine_similarity(query_vec, doc_vec)
        scored.append((score, doc))
    scored.sort(reverse=True, key=lambda x: x[0])
    return [doc for score, doc in scored[:k] if score > 0]

if __name__ == "__main__":
    docs = load_documents()
    query = "O veiculo hibrido gerou alerta P0A80. Qual o procedimento de tensao e bancada?"
    
    print(f"[*] Consulta: {query}\n")
    retrieved = retrieve(query, docs, k=2)
    
    print("[+] Contexto Recuperado via RAG:")
    for i, context in enumerate(retrieved, 1):
        print(f"\n--- Documento {i} ---\n{context}")
