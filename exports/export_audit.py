import csv
import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from module_4_finetuning.iso_safety_validator import evaluate_functional_safety

def export_audit_log():
    telemetry_path = os.path.join(ROOT_DIR, "module_2_mcp", "data", "can_telemetry.csv")
    output_audit = os.path.join(ROOT_DIR, "exports", "relatorio_auditoria_iso26262.txt")

    if not os.path.exists(telemetry_path):
        print("Arquivo de telemetria não encontrado.")
        return

    with open(telemetry_path, 'r', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))

    with open(output_audit, 'w', encoding='utf-8') as f:
        f.write("="*70 + "\n")
        f.write("RELATÓRIO TÉCNICO DE AUDITORIA VEICULAR - MARLEYOS\n")
        f.write("="*70 + "\n\n")
        
        for r in rows:
            ts = r.get('timestamp_s')
            falha = r.get('status_falha')
            f.write(f"Timestamp: {ts}s | RPM: {r.get('rpm_motor')} | Corrente: {r.get('corrente_pack_a')} A | BPCM: {r.get('bpcm_isolamento_kohm')} kOhm\n")
            if falha != "NORMAL":
                parecer = evaluate_functional_safety(f"Falha: {falha}")
                f.write(f" -> ALERTA REGISTRADO: {falha}\n")
                f.write(f" -> METAS DE SEGURANÇA: {parecer}\n")
            f.write("-" * 50 + "\n")

    print(f"[OK] Auditoria exportada com sucesso em: {output_audit}")

if __name__ == "__main__":
    export_audit_log()
