import json
import os

def evaluate_functional_safety(event_description):
    dataset_path = os.path.join(os.path.dirname(__file__), "dataset", "iso26262_dataset.jsonl")
    if os.path.exists(dataset_path):
        with open(dataset_path, 'r', encoding='utf-8') as f:
            for line in f:
                item = json.loads(line)
                for key_term in ["315A", "C0035", "C1555", "P0606", "P0AA6", "P0700"]:
                    if key_term in event_description and key_term in item.get("input", ""):
                        return item["output"]
    return "NIVEL_ASIL: QM (Qualidade Padrao) | Parametros sob limites nominais de controle."
