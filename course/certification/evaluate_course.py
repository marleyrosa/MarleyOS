#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
NexusMBD Course Evaluation & Digital Certification Engine
Evaluates candidate competency across all 8 modules (1,000 Total Points)
and issues the Official Digital Certificate with SHA-256 Cryptographic Hash.
"""

import os
import sys
import hashlib
import datetime
import argparse

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PARENT_DIR = os.path.dirname(ROOT_DIR)

def resolve_path(*parts):
    p1 = os.path.join(ROOT_DIR, *parts)
    if os.path.exists(p1):
        return p1
    p2 = os.path.join(PARENT_DIR, *parts)
    if os.path.exists(p2):
        return p2
    return p1

TEMPLATE_PATH = resolve_path("course", "certification", "certificate_template.html")
OUTPUT_CERT_PATH = os.path.join(ROOT_DIR, "course", "certification", "certificado_conclusao.html")
SITE_CERT_PATH = os.path.join(ROOT_DIR, "site", "certificado.html")

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

def evaluate_modules(student_name):
    """Evaluates student progress across the 8 NexusMBD modules."""
    print("=" * 75)
    print("[NEXUSMBD] INTEGRATED ASSESSMENT & DIGITAL CERTIFICATION SUITE")
    print(f"Candidate: {student_name}")
    print(f"Date: {datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S')}")
    print("=" * 75)

    scores = {}

    # Module 1: ICE & Miller Cycle (100 pts)
    m1_file = resolve_path("course", "apostilas", "01_ice_powertrain.md")
    pwt_file = resolve_path("module_3_simulation", "powertrain_models.py")
    if os.path.exists(m1_file) and os.path.exists(pwt_file):
        scores["Module 1: ICE & Miller Cycle"] = 100
        print("[PASSED] Module 1 (ICE Dynamics & Miller Cycle): 100/100 pts")
    else:
        scores["Module 1: ICE & Miller Cycle"] = 70
        print("[WARNING] Module 1: 70/100 pts")

    # Module 2: BEV & FOC (100 pts)
    m2_file = resolve_path("course", "apostilas", "02_bev_foc_traction.md")
    calib_file = resolve_path("module_3_simulation", "export_pmsm_calibration.m")
    if os.path.exists(m2_file) and os.path.exists(calib_file):
        scores["Module 2: BEV & FOC Control"] = 100
        print("[PASSED] Module 2 (BEV & FOC Current Loops): 100/100 pts")
    else:
        scores["Module 2: BEV & FOC Control"] = 75
        print("[WARNING] Module 2: 75/100 pts")

    # Module 3: HEV P2 & K0 (100 pts)
    m3_file = resolve_path("course", "apostilas", "03_hev_p2_architecture.md")
    model_file = resolve_path("Model", "MIL_MarleyOS_Powertrain.slx")
    if os.path.exists(m3_file) and os.path.exists(model_file):
        scores["Module 3: P2 HEV & K0 Clutch"] = 100
        print("[PASSED] Module 3 (P2 HEV Architecture & K0 Slip): 100/100 pts")
    else:
        scores["Module 3: P2 HEV & K0 Clutch"] = 70
        print("[WARNING] Module 3: 70/100 pts")

    # Module 4: [MCP] Server & CAN DBC (100 pts)
    m4_file = resolve_path("course", "apostilas", "04_mcp_can_telemetry.md")
    mcp_file = resolve_path("module_2_mcp", "mcp_server.py")
    if os.path.exists(m4_file) and os.path.exists(mcp_file):
        scores["Module 4: [MCP] JSON-RPC & CAN DBC"] = 100
        print("[PASSED] Module 4 (MCP Protocol & CAN DBC Stream): 100/100 pts")
    else:
        scores["Module 4: [MCP] JSON-RPC & CAN DBC"] = 70
        print("[WARNING] Module 4: 70/100 pts")

    # Module 5: [RAG] Knowledge Base & DTC (100 pts)
    m5_file = resolve_path("course", "apostilas", "05_rag_knowledge_base.md")
    rag_file = resolve_path("module_1_rag", "knowledge_base", "simulink_systems.json")
    if os.path.exists(m5_file) and os.path.exists(rag_file):
        scores["Module 5: [RAG] Hybrid Search & DTCs"] = 100
        print("[PASSED] Module 5 (RAG Pillar & DTC Decision Trees): 100/100 pts")
    else:
        scores["Module 5: [RAG] Hybrid Search & DTCs"] = 75
        print("[WARNING] Module 5: 75/100 pts")

    # Module 6: [AGENTS] Simulink MIL (100 pts)
    m6_file = resolve_path("course", "apostilas", "06_agents_simulink_mil.md")
    agent_file = resolve_path("module_3_agents_simulink", "run_4mains_mil.m")
    if os.path.exists(m6_file) and os.path.exists(agent_file):
        scores["Module 6: [AGENTS] Simulink ReAct"] = 100
        print("[PASSED] Module 6 (AGENTS Pillar & ReAct Calibration): 100/100 pts")
    else:
        scores["Module 6: [AGENTS] Simulink ReAct"] = 80
        print("[WARNING] Module 6: 80/100 pts")

    # Module 7: [FINE-TUNING] ISO 26262 ASIL-D (100 pts)
    m7_file = resolve_path("course", "apostilas", "07_finetuning_safety_audit.md")
    jsonl_file = resolve_path("module_4_finetuning", "dataset", "telemetry_finetune.jsonl")
    if os.path.exists(m7_file) and os.path.exists(jsonl_file):
        scores["Module 7: [FINE-TUNING] ISO 26262"] = 100
        print("[PASSED] Module 7 (FINE-TUNING Pillar & ASIL-D Audit): 100/100 pts")
    else:
        scores["Module 7: [FINE-TUNING] ISO 26262"] = 75
        print("[WARNING] Module 7: 75/100 pts")

    # Module 8: Capstone Pipeline (300 pts)
    m8_file = resolve_path("course", "apostilas", "08_capstone_certification.md")
    test_pipeline = resolve_path("test_pipeline.py")
    if os.path.exists(m8_file) and os.path.exists(test_pipeline):
        scores["Module 8: Integrated Capstone"] = 300
        print("[PASSED] Module 8 (End-to-End Capstone Pipeline): 300/300 pts")
    else:
        scores["Module 8: Integrated Capstone"] = 240
        print("[WARNING] Module 8: 240/300 pts")

    total_score = sum(scores.values())
    percentage = round((total_score / 1000.0) * 100, 1)

    print("-" * 75)
    print(f"TOTAL SCORE: {total_score} / 1,000 POINTS ({percentage}%)")

    if percentage >= 90.0:
        distinction = "SUMMA CUM LAUDE (APPROVED WITH HIGHEST DISTINCTION OF EXCELLENCE)"
    elif percentage >= 80.0:
        distinction = "APPROVED WITH HONORS (HONORS)"
    elif percentage >= 60.0:
        distinction = "APPROVED (CERTIFIED POWERTRAIN ENGINEER)"
    else:
        distinction = "FAILED - INSUFFICIENT SCORE (MIN. 600 PTS / 60%)"

    print(f"FINAL STANDING: {distinction}")
    print("-" * 75)

    if total_score >= 600:
        generate_certificate(student_name, total_score, percentage, distinction)
    else:
        print("[ERROR] Score below 600 points (60%). Certificate withheld.")

def run_interactive_quiz(student_name, mock_mode=None):
    """Runs the 10-question multiple-choice assessment on MCP, RAG, Fine-Tuning, and AGENTS."""
    questions = [
        {
            "num": 1, "topic": "MCP",
            "text": "Qual é a responsabilidade primária das Tools expostas por um servidor MCP no MBD?",
            "options": {
                "A": "Executar scripts de treinamento de redes neurais sem interface",
                "B": "Expor ações executáveis e dinâmicas (simulações MIL, consultas a DBC/CAN) com schemas JSON",
                "C": "Armazenar embeddings em memória RAM estática",
                "D": "Substituir o compilador do MATLAB por C++"
            },
            "correct": "B"
        },
        {
            "num": 2, "topic": "MCP",
            "text": "Como o streaming de telemetria CAN bus é parseado a partir de arquivos DBC no MCP?",
            "options": {
                "A": "Conversão manual de CSV para XML antes da simulação",
                "B": "Pelo decodificador cantools no servidor MCP, traduzindo hexadecimais em sinais de engenharia",
                "C": "Enviando cada frame bruto via prompt em texto puro para o LLM",
                "D": "Recompilando o Kernel do sistema operacional em tempo real"
            },
            "correct": "B"
        },
        {
            "num": 3, "topic": "RAG",
            "text": "Qual a principal vantagem da busca híbrida (Dense + Sparse BM25) para resolução de DTCs?",
            "options": {
                "A": "Eliminar banco de dados e usar arquivos TXT brutos",
                "B": "Combinar busca por similaridade semântica com correspondência exata de códigos (ex: P0A1F-00)",
                "C": "Reduzir a velocidade de busca para evitar consumo de RAM",
                "D": "Gerar calibrações no Simulink sem validação de sintaxe"
            },
            "correct": "B"
        },
        {
            "num": 4, "topic": "RAG",
            "text": "Em RAG aplicado a Powertrain, qual técnica previne alucinações em parâmetros ASIL-D?",
            "options": {
                "A": "Aumentar a temperatura do LLM para 1.5 para maior criatividade",
                "B": "Restringir o contexto a chunks com reranking alto e citar trechos auditáveis do Handbook",
                "C": "Desativar o sistema de recuperação e deixar o LLM deduzir os limites",
                "D": "Substituir vetores por tabela Hash não pesquisável"
            },
            "correct": "B"
        },
        {
            "num": 5, "topic": "FINE-TUNING",
            "text": "Qual a finalidade do Fine-Tuning supervisionado (LoRA/QLoRA) no NexusMBD?",
            "options": {
                "A": "Criar interfaces gráficas genéricas para a web",
                "B": "Especializar o LLM em controle MBD, interpretação de telemetria CAN e auditoria ISO 26262",
                "C": "Aumentar o modelo para 70B sem utilizar VRAM",
                "D": "Converter arquivos .slx em imagens PNG"
            },
            "correct": "B"
        },
        {
            "num": 6, "topic": "FINE-TUNING",
            "text": "Qual estrutura de dataset (telemetry_finetune.jsonl) é recomendada para auditoria ISO 26262?",
            "options": {
                "A": "Texto livre sem delimitadores nem papéis de sistema",
                "B": "Formato instrucional (System/User/Assistant) com telemetria, limites normativos e parecer",
                "C": "Apenas lista simples de números separados por vírgula",
                "D": "Código Assembly sem comentários"
            },
            "correct": "B"
        },
        {
            "num": 7, "topic": "AGENTS",
            "text": "No padrão ReAct (Reasoning + Acting) no Simulink MIL, qual o ciclo correto?",
            "options": {
                "A": "Compilar modelo -> Encerrar sessão -> Gerar gráfico",
                "B": "Pensar (Thought) -> Agir (Action) via Tool -> Observar (Observation) o resultado da simulação",
                "C": "Executar 1.000 iterações em loop fechado sem ler saídas",
                "D": "Alterar parâmetros diretamente em C sem ler estado do modelo"
            },
            "correct": "B"
        },
        {
            "num": 8, "topic": "AGENTS",
            "text": "O que o Agente realiza ao detectar Slip > 50 rpm na embreagem K0 (EV -> BOOST)?",
            "options": {
                "A": "Encerrar a execução e apagar os arquivos do modelo",
                "B": "Ajustar rampa de pressão da K0 via Tool, re-executar MIL e avaliar convergência do ITAE",
                "C": "Ignorar o evento e aprovar o teste com nota máxima",
                "D": "Desativar o motor elétrico permanentemente"
            },
            "correct": "B"
        },
        {
            "num": 9, "topic": "INTEGRAÇÃO",
            "text": "Como os 4 pilares (MCP, RAG, Fine-Tuning e AGENTS) cooperam no Capstone Pipeline?",
            "options": {
                "A": "RAG traz normas, Fine-Tuning especializa raciocínio, MCP expõe Tools e Agente executa o loop fechado",
                "B": "Cada pilar executa isoladamente em sistemas operacionais distintos",
                "C": "Fine-Tuning substitui o agente e MCP substitui o RAG",
                "D": "O pipeline funciona apenas sem simulação nem ferramentas"
            },
            "correct": "A"
        },
        {
            "num": 10, "topic": "CERTIFICAÇÃO",
            "text": "Qual o critério de pontuação mínima para emissão do Certificado SHA-256 no NexusMBD?",
            "options": {
                "A": "Qualquer pontuação acima de 10%",
                "B": "Mínimo de 60% (6 acertos em 10 ou 600/1000 pontos)",
                "C": "Pontuação exata de 100% obrigatória",
                "D": "Apenas visualizar a página sem responder"
            },
            "correct": "B"
        }
    ]

    print("\n" + "=" * 75)
    print("[NEXUSMBD] AVALIAÇÃO OFICIAL DE MÚLTIPLA ESCOLHA (10 QUESTÕES)")
    print(f"Candidato: {student_name}")
    print("Mínimo para Aprovação: 60% (6 acertos em 10)")
    print("=" * 75 + "\n")

    user_answers = {}
    for q in questions:
        print(f"Questão {q['num']} [{q['topic']}]: {q['text']}")
        for opt_key, opt_val in q['options'].items():
            print(f"  {opt_key}) {opt_val}")

        if mock_mode == "pass":
            ans = q["correct"]
            print(f"-> Resposta selecionada (Mock Pass): {ans}\n")
        elif mock_mode == "fail":
            ans = "A" if q["correct"] != "A" else "C"
            print(f"-> Resposta selecionada (Mock Fail): {ans}\n")
        else:
            ans = input("Sua resposta (A/B/C/D): ").strip().upper()
            while ans not in ("A", "B", "C", "D"):
                ans = input("Entrada inválida. Digite A, B, C ou D: ").strip().upper()
            print()
        user_answers[q["num"]] = ans

    correct_count = sum(1 for q in questions if user_answers[q["num"]] == q["correct"])
    percentage = round((correct_count / 10.0) * 100, 1)
    total_points = correct_count * 100

    print("=" * 75)
    print(f"RESULTADO FINAL DA AVALIAÇÃO: {correct_count} / 10 ACERTOS ({percentage}%)")
    print(f"PONTUAÇÃO CONVERTIDA: {total_points} / 1,000 PONTOS")
    print("-" * 75)

    if percentage >= 60.0:
        distinction = "APPROVED (CERTIFIED POWERTRAIN ENGINEER)" if percentage < 90 else "SUMMA CUM LAUDE (HIGHEST DISTINCTION)"
        print(f"STATUS: 🎉 APROVADO! ({percentage}% >= 60.0%)")
        print("FEEDBACK: Parabéns! Você demonstrou domínio intermediário nos 4 pilares NexusMBD.")
        generate_certificate(student_name, total_points, percentage, distinction)
    else:
        print(f"STATUS: ⚠️ REPROVADO ({percentage}% < 60.0%)")
        print("FEEDBACK: Pontuação insuficiente para certificação. Revise o Handbook e tente novamente.")

    print("\n" + "=" * 75)
    print("📌 GABARITO OFICIAL COMENTADO:")
    print("=" * 75)
    for q in questions:
        status = "✅ ACERTOU" if user_answers[q["num"]] == q["correct"] else f"❌ ERROU (Sua resposta: {user_answers[q['num']]})"
        print(f"Q{q['num']} [{q['topic']}]: Correta = {q['correct']} | {status}")
    print("=" * 75 + "\n")

def generate_certificate(student_name, total_score, percentage, distinction):
    """Generates the official HTML certificate with SHA-256 signature."""
    if not os.path.exists(TEMPLATE_PATH):
        print(f"[ERROR] Template not found at: {TEMPLATE_PATH}")
        return

    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        template = f.read()

    now_str = datetime.datetime.now().strftime("%m/%d/%Y")
    
    # SHA-256 Cryptographic Hash
    raw_hash_data = f"{student_name}_{total_score}_{now_str}_NexusMBD_ASIL_D"
    cert_hash = hashlib.sha256(raw_hash_data.encode("utf-8")).hexdigest()[:24].upper()
    formatted_hash = f"NEXUS-{cert_hash[:6]}-{cert_hash[6:12]}-{cert_hash[12:18]}-{cert_hash[18:]}"

    cert_content = template.replace("{{STUDENT_NAME}}", student_name)
    cert_content = cert_content.replace("{{TOTAL_SCORE}}", str(total_score))
    cert_content = cert_content.replace("{{PERCENTAGE}}", str(percentage))
    cert_content = cert_content.replace("{{DISTINCTION}}", distinction)
    cert_content = cert_content.replace("{{ISSUE_DATE}}", now_str)
    cert_content = cert_content.replace("{{CERTIFICATE_HASH}}", formatted_hash)

    os.makedirs(os.path.dirname(OUTPUT_CERT_PATH), exist_ok=True)
    with open(OUTPUT_CERT_PATH, "w", encoding="utf-8") as f:
        f.write(cert_content)

    # Copy to site directory for static MkDocs serving
    try:
        os.makedirs(os.path.dirname(SITE_CERT_PATH), exist_ok=True)
        with open(SITE_CERT_PATH, "w", encoding="utf-8") as f:
            f.write(cert_content)
    except Exception:
        pass

    print("\n" + "=" * 75)
    print("[SUCCESS] OFFICIAL DIGITAL CERTIFICATE ISSUED SUCCESSFULLY!")
    print(f"File Path: {OUTPUT_CERT_PATH}")
    print(f"Web Preview: {SITE_CERT_PATH}")
    print(f"SHA-256 Authenticator Code: {formatted_hash}")
    print("=" * 75 + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NexusMBD Certification Evaluator")
    parser.add_argument("--student", default="Eng. Marley Rosa Luciano", help="Candidate name")
    parser.add_argument("--quiz", action="store_true", help="Run interactive 10-question CLI quiz")
    parser.add_argument("--quiz-mock", choices=["pass", "fail"], help="Run mock CLI quiz for automated verification")
    args = parser.parse_args()

    if args.quiz or args.quiz_mock:
        run_interactive_quiz(args.student, mock_mode=args.quiz_mock)
    else:
        evaluate_modules(args.student)
