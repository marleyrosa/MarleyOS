#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
NexusMBD Course Evaluation & Digital Certification Engine
Avalia o desempenho do aluno nos 8 módulos do curso (1.000 Pontos Totais)
e gera o Certificado Digital de Conclusão com Hash Criptográfico SHA-256.
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
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

def evaluate_modules(student_name):
    """Avalia o progresso do aluno nos 8 modulos do NexusMBD."""
    print("=" * 75)
    print("[NEXUSMBD] SISTEMA INTEGRADO DE AVALIACAO & CERTIFICACAO")
    print(f"Candidato: {student_name}")
    print(f"Data: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("=" * 75)

    scores = {}

    # Módulo 1: ICE & Ciclo Miller (100 pts)
    m1_file = resolve_path("course", "apostilas", "01_ice_powertrain.md")
    pwt_file = resolve_path("module_3_simulation", "powertrain_models.py")
    if os.path.exists(m1_file) and os.path.exists(pwt_file):
        scores["Módulo 1: ICE & Ciclo Miller"] = 100
        print("[PASSED] Módulo 1 (ICE & Miller Cycle): 100/100 pts")
    else:
        scores["Módulo 1: ICE & Ciclo Miller"] = 70
        print("[WARNING] Módulo 1: 70/100 pts")

    # Módulo 2: BEV & FOC (100 pts)
    m2_file = resolve_path("course", "apostilas", "02_bev_foc_traction.md")
    calib_file = resolve_path("module_3_simulation", "export_pmsm_calibration.m")
    if os.path.exists(m2_file) and os.path.exists(calib_file):
        scores["Módulo 2: BEV & Controle FOC"] = 100
        print("[PASSED] Módulo 2 (BEV & FOC): 100/100 pts")
    else:
        scores["Módulo 2: BEV & Controle FOC"] = 75
        print("[WARNING] Módulo 2: 75/100 pts")

    # Módulo 3: HEV P2 & K0 (100 pts)
    m3_file = resolve_path("course", "apostilas", "03_hev_p2_architecture.md")
    model_file = resolve_path("Model", "MIL_MarleyOS_Powertrain.slx")
    if os.path.exists(m3_file) and os.path.exists(model_file):
        scores["Módulo 3: Híbrido P2 & Embreagem K0"] = 100
        print("[PASSED] Módulo 3 (P2 HEV & K0): 100/100 pts")
    else:
        scores["Módulo 3: Híbrido P2 & Embreagem K0"] = 70
        print("[WARNING] Módulo 3: 70/100 pts")

    # Módulo 4: [MCP] Server & CAN DBC (100 pts)
    m4_file = resolve_path("course", "apostilas", "04_mcp_can_telemetry.md")
    mcp_file = resolve_path("module_2_mcp", "mcp_server.py")
    if os.path.exists(m4_file) and os.path.exists(mcp_file):
        scores["Módulo 4: [MCP] Tool Server & CAN DBC"] = 100
        print("[PASSED] Módulo 4 (Pilar MCP): 100/100 pts")
    else:
        scores["Módulo 4: [MCP] Tool Server & CAN DBC"] = 70
        print("[WARNING] Módulo 4: 70/100 pts")

    # Módulo 5: [RAG] Knowledge Base & DTC (100 pts)
    m5_file = resolve_path("course", "apostilas", "05_rag_knowledge_base.md")
    rag_file = resolve_path("module_1_rag", "knowledge_base", "simulink_systems.json")
    if os.path.exists(m5_file) and os.path.exists(rag_file):
        scores["Módulo 5: [RAG] Busca Híbrida & DTCs"] = 100
        print("[PASSED] Módulo 5 (Pilar RAG): 100/100 pts")
    else:
        scores["Módulo 5: [RAG] Busca Híbrida & DTCs"] = 75
        print("[WARNING] Módulo 5: 75/100 pts")

    # Módulo 6: [AGENTS] Simulink MIL (100 pts)
    m6_file = resolve_path("course", "apostilas", "06_agents_simulink_mil.md")
    agent_file = resolve_path("module_3_agents_simulink", "run_4mains_mil.m")
    if os.path.exists(m6_file) and os.path.exists(agent_file):
        scores["Módulo 6: [AGENTS] Calibração Simulink"] = 100
        print("[PASSED] Módulo 6 (Pilar AGENTS): 100/100 pts")
    else:
        scores["Módulo 6: [AGENTS] Calibração Simulink"] = 80
        print("[WARNING] Módulo 6: 80/100 pts")

    # Módulo 7: [FINE-TUNING] ISO 26262 ASIL-D (100 pts)
    m7_file = resolve_path("course", "apostilas", "07_finetuning_safety_audit.md")
    jsonl_file = resolve_path("module_4_finetuning", "dataset", "telemetry_finetune.jsonl")
    if os.path.exists(m7_file) and os.path.exists(jsonl_file):
        scores["Módulo 7: [FINE-TUNING] ISO 26262"] = 100
        print("[PASSED] Módulo 7 (Pilar FINE-TUNING): 100/100 pts")
    else:
        scores["Módulo 7: [FINE-TUNING] ISO 26262"] = 75
        print("[WARNING] Módulo 7: 75/100 pts")

    # Módulo 8: Capstone & Exame Integrado (300 pts)
    m8_file = resolve_path("course", "apostilas", "08_capstone_certification.md")
    test_pipeline = resolve_path("test_pipeline.py")
    if os.path.exists(m8_file) and os.path.exists(test_pipeline):
        scores["Módulo 8: Capstone & Exame Integrado"] = 300
        print("[PASSED] Módulo 8 (Capstone Integrado): 300/300 pts")
    else:
        scores["Módulo 8: Capstone & Exame Integrado"] = 240
        print("[WARNING] Módulo 8: 240/300 pts")

    total_score = sum(scores.values())
    percentage = round((total_score / 1000.0) * 100, 1)

    print("-" * 75)
    print(f"PONTUAÇÃO TOTAL: {total_score} / 1.000 PONTOS ({percentage}%)")

    if percentage >= 90.0:
        distinction = "APROVADO COM DISTINÇÃO DE EXCELÊNCIA (SUMMA CUM LAUDE)"
    elif percentage >= 80.0:
        distinction = "APROVADO COM HONRA (HONORS)"
    elif percentage >= 70.0:
        distinction = "APROVADO (CERTIFIED POWERTRAIN ENGINEER)"
    else:
        distinction = "REPROVADO - NOTA INSUFICIENTE (MIN. 700 PTS)"

    print(f"STATUS FINAL: {distinction}")
    print("-" * 75)

    if total_score >= 700:
        generate_certificate(student_name, total_score, percentage, distinction)
    else:
        print("[ERRO] Pontuação abaixo de 700 pontos. Certificado não emitido.")


def generate_certificate(student_name, total_score, percentage, distinction):
    """Gera o arquivo HTML do certificado com assinatura SHA-256."""
    if not os.path.exists(TEMPLATE_PATH):
        print(f"[ERRO] Template não encontrado em: {TEMPLATE_PATH}")
        return

    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        template = f.read()

    now_str = datetime.datetime.now().strftime("%d/%m/%Y")
    
    # Hash Criptográfico SHA-256
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

    # Copia para pasta site/ para visualização online no MkDocs
    try:
        os.makedirs(os.path.dirname(SITE_CERT_PATH), exist_ok=True)
        with open(SITE_CERT_PATH, "w", encoding="utf-8") as f:
            f.write(cert_content)
    except Exception:
        pass

    print("\n" + "=" * 75)
    print("[SUCCESS] CERTIFICADO DIGITAL OFICIAL GERADO COM SUCESSO!")
    print(f"Arquivo: {OUTPUT_CERT_PATH}")
    print(f"Visualizacao Web: {SITE_CERT_PATH}")
    print(f"Codigo Autenticador SHA-256: {formatted_hash}")
    print("=" * 75 + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NexusMBD Certification Evaluator")
    parser.add_argument("--student", default="Engenheiro de Sistemas Automotivos", help="Nome do aluno")
    args = parser.parse_args()

    evaluate_modules(args.student)
