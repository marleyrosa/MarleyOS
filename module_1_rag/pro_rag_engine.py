import json
import os
import re

class ProfessionalAutomotiveRAG:
    def __init__(self, json_path, standards_path):
        self.json_path = json_path
        self.standards_path = standards_path
        self.systems = {}
        self.load_data()

    def load_data(self):
        if os.path.exists(self.json_path):
            with open(self.json_path, 'r', encoding='utf-8') as f:
                self.systems = json.load(f)

    def query(self, text):
        t = text.lower()
        matched_key = None
        highest_score = 0

        # Identificar o sistema técnico exato
        for key, item in self.systems.items():
            score = 0
            for kw in item.get("keywords", []):
                if kw in t:
                    score += len(kw)
            if score > highest_score:
                highest_score = score
                matched_key = key

        if matched_key and highest_score > 0:
            sys_data = self.systems[matched_key]
            blocks_table = "| Bloco Simulink | Caminho na Biblioteca | Parâmetro Crítico |\n| :--- | :--- | :--- |\n"
            for b in sys_data.get("blocks", []):
                blocks_table += f"| **{b['name']}** | `{b['path']}` | {b['param']} |\n"

            return {
                "title": sys_data["title"],
                "summary": sys_data["summary"],
                "blocks_table": blocks_table,
                "logic": sys_data["logic"],
                "svg": sys_data["svg"],
                "script": sys_data["script"]
            }

        # Fallback para normas e conceitos teóricos
        return {
            "title": f"Consulta Normativa & Científica: '{text}'",
            "summary": "O sistema analisou os requisitos normativos da UN ECE R100 (Alta Tensão) e ISO 26262 (Segurança Funcional).",
            "blocks_table": "| Parâmetro | Norma | Limite Técnico |\n| :--- | :--- | :--- |\n| Resistência Isolamento | UN ECE R100 | ≥ 100 Ω/V (DC) e ≥ 500 Ω/V (AC) |\n| Tempo de Contenção (FTTI) | ISO 26262 | ≤ 20 ms para estado seguro em ASIL-D |\n| Isolamento Galvânico | BPCM | Abertura obrigatória de contatores HV |",
            "logic": "Para simulações no Simulink, utilize o padrão Simulink.SimulationInput integrado ao MATLAB MCP Core Server.",
            "svg": "",
            "script": "% Padrão de Simulação Moderna no Simulink (MCP Core)\nsimIn = Simulink.SimulationInput('Powertrain_Control');\nsimIn = simIn.setModelParameter('SaveFormat', 'Dataset');\nsimOut = sim(simIn);"
        }
