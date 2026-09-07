import os
import re
import math
from collections import Counter

class AutomotiveEngineeringAI:
    def __init__(self, kb_path):
        self.kb_path = kb_path
        self.chunks = []
        self.tokenized_chunks = []
        self.load_knowledge_base()

    def tokenize(self, text):
        return re.findall(r'\w+', text.lower())

    def load_knowledge_base(self):
        if not os.path.exists(self.kb_path):
            return
        with open(self.kb_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Divide o repositório em blocos lógicos por seções
        raw_blocks = content.split("\n\n")
        self.chunks = [b.strip() for b in raw_blocks if len(b.strip()) > 30]
        self.tokenized_chunks = [self.tokenize(c) for c in self.chunks]

    def retrieve_context(self, query):
        q_tokens = self.tokenize(query)
        scores = []
        for idx, doc_tokens in enumerate(self.tokenized_chunks):
            common = set(q_tokens).intersection(set(doc_tokens))
            score = sum(doc_tokens.count(t) for t in common)
            scores.append((score, self.chunks[idx]))
        scores.sort(key=lambda x: x[0], reverse=True)
        return [c for s, c in scores[:2] if s > 0]

    def answer_query(self, user_query):
        query_lower = user_query.lower()
        context = self.retrieve_context(user_query)

        # 1. Se o usuário pedir para gerar, modelar ou explicar simulação/Simulink
        if any(w in query_lower for w in ["modelo", "modelar", "simulink", "script", "matlab", "codigo"]):
            return (
                "🎯 **Síntese de Engenharia: Modelo Simulink & Padrão MCP**\n\n"
                "Para modelar e simular sistemas automotivos (ex: Inversor ou BPCM) utilizando agentes modernos sem erros de execução, "
                "aplica-se a classe `Simulink.SimulationInput` compatível com o **MATLAB MCP Core Server**:\n\n"
                "```matlab\n"
                "% 1. Definir o modelo de trem de força\n"
                "modelName = 'EV_Powertrain_Control';\n"
                "\n"
                "% 2. Inicializar objeto de simulação isolado\n"
                "simIn = Simulink.SimulationInput(modelName);\n"
                "simIn = simIn.setModelParameter('StopTime', '10.0');\n"
                "simIn = simIn.setModelParameter('SaveFormat', 'Dataset');\n"
                "\n"
                "% 3. Injetar limites físicos e calibração de bancada\n"
                "simIn = simIn.setVariable('MaxPhaseCurrent', 285.0);\n"
                "simIn = simIn.setVariable('R_Isolation_Min', 100); % Ohm/V (UN ECE R100)\n"
                "\n"
                "% 4. Executar e extrair telemetria\n"
                "simOut = sim(simIn);\n"
                "loggedSignals = simOut.logsout;\n"
                "```\n\n"
                "💡 **Boas Práticas de Engenharia:**\n"
                "- Nunca utilize strings concatenadas legadas para o comando `sim()`.\n"
                "- O uso de `SimulationInput` protege o workspace do MATLAB contra poluição de variáveis durante testes em lote."
            )

        # 2. Se houver contexto normativo / científico recuperado
        if context:
            ctx_text = "\n\n".join(context)
            return (
                f"🔬 **Parecer Técnico Baseado em Evidências Científicas & Normas**\n\n"
                f"**Fundamentação Teórica e Normativa Recuperada:**\n{ctx_text}\n\n"
                f"📋 **Diretrizes de Implementação no Sistema:**\n"
                f"- **Critério de Aceitação:** Validar os dados de telemetria CAN contra as equações nominais de dissipação e isolamento.\n"
                f"- **Mitigação de Risco:** Caso um sinal ultrapasse o limiar operacional, acionar a rotina ASIL de isolamento galvânico e registrar a ocorrência para auditoria."
            )

        # 3. Resposta técnica analítica aberta para qualquer outro termo
        return (
            f"⚙️ **Análise de Engenharia para:** *'{user_query}'*\n\n"
            "O repositório científico do **MarleyOS** está monitorando os seguintes eixos:\n"
            "- **UN ECE R100:** Limiares de isolamento elétrico (100 Ω/V DC, 500 Ω/V AC).\n"
            "- **ISO 26262:** Metas de segurança funcional e tempo de contenção FTTI (<20ms) para ASIL-D.\n"
            "- **Simulink & MCP:** Geração de rotinas modernas com `Simulink.SimulationInput`.\n\n"
            "Para uma resposta detalhada, pergunte sobre isolamento de bateria, sobrecorrente do inversor ou solicite um modelo de simulação."
        )
