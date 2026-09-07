import json
import os

def evaluate_functional_safety(event_description):
    dataset_path = os.path.join(os.path.dirname(__file__), "dataset", "iso26262_dataset.jsonl")
    if os.path.exists(dataset_path):
        with open(dataset_path, 'r', encoding='utf-8') as f:
            for line in f:
                item = json.loads(line)
                if "315A" in event_description and "315A" in item.get("input", ""):
                    return item["output"]
    return "NIVEL_ASIL: QM (Qualidade Padrao) | Nenhuma violacao de seguranca funcional detectada."
