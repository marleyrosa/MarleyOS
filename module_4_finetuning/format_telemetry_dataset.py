"""Format recorded CAN telemetry rows into instruction/response JSONL pairs for LLM fine-tuning."""
import csv
import json
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_CSV_PATH = os.path.join(ROOT_DIR, "module_2_mcp", "data", "can_telemetry.csv")
DEFAULT_OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "dataset", "telemetry_finetune.jsonl")


def _value(row, *names, default="0"):
    for name in names:
        value = row.get(name)
        if value not in (None, ""):
            return value
    return default


def row_to_pair(row):
    k0_state = _value(row, "k0_state", default="N/A")
    modo = _value(row, "modo_propulsao", default="N/A")
    rpm_em = _value(row, "rpm_em", "EMSpeed")
    soc = _value(row, "soc_pct", "HVBatSOC")
    torque = _value(row, "torque_nm", "EMTrqReq")
    instruction = "Diagnostique o estado do trem de forca P2 a partir da telemetria CAN."
    input_text = (
        f"rpm_em={rpm_em}, torque_nm={torque}, soc_pct={soc}, "
        f"k0_state={k0_state}, modo_propulsao={modo}"
    )
    output_text = f"MODO={modo} | K0_STATE={k0_state} | ACAO=Manter monitoramento nominal do trem de forca."
    return {"instruction": instruction, "input": input_text, "output": output_text}


def format_dataset(csv_path=DEFAULT_CSV_PATH, output_path=DEFAULT_OUTPUT_PATH, max_rows=200):
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Telemetry CSV not found: {csv_path}")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    written = 0
    with open(csv_path, "r", encoding="utf-8") as csv_file, \
            open(output_path, "w", encoding="utf-8") as jsonl_file:
        for row in csv.DictReader(csv_file):
            jsonl_file.write(json.dumps(row_to_pair(row), ensure_ascii=False) + "\n")
            written += 1
            if written >= max_rows:
                break
    return output_path, written


if __name__ == "__main__":
    path, count = format_dataset()
    print(f"[OK] {count} pares instrucao/resposta gravados em {path}")
