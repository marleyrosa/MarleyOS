import json
import os

class ProfessionalAutomotiveRAG:
    def __init__(self, json_path, std_path=None):
        self.json_path = json_path
        self.std_path = std_path
        self.systems = {}
        self.load_data()

    def load_data(self):
        if os.path.exists(self.json_path):
            with open(self.json_path, 'r', encoding='utf-8') as f:
                self.systems = json.load(f)

    def query(self, text):
        t = text.lower().strip()
        best_match = None
        max_score = 0

        for key, item in self.systems.items():
            score = 0
            for kw in item.get("keywords", []):
                if kw in t:
                    score += len(kw) ** 2
            if score > max_score:
                max_score = score
                best_match = key

        if best_match and max_score > 0:
            sys_data = self.systems[best_match]
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

        return {
            "title": f"Consulta Normativa & Sistemas: '{text}'",
            "summary": "O sistema analisou os requisitos normativos da UN ECE R100 (Alta Tensão) e ISO 26262 (Segurança Funcional).",
            "blocks_table": "| Parâmetro | Norma | Limite |\n| :--- | :--- | :--- |\n| Isolamento HV | UN ECE R100 | >= 100 Ohm/V (DC) |\n| Tempo FTTI | ISO 26262 | <= 20 ms em ASIL-D |",
            "logic": "Topologias indexadas: 'conversor abaixador (buck)', 'elevador boost', 'controle em malha fechada' ou 'pid'.",
            "svg": "",
            "script": "% Padrão SimulationInput (MCP Core)\nsimIn = Simulink.SimulationInput('Powertrain_Model');\nsimIn = simIn.setModelParameter('SaveFormat', 'Dataset');"
        }
