from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
DEFAULT_DBC_PATH = ROOT_DIR / "data" / "marleyos_default.dbc"

DBC_TEXT = """VERSION \"\"\n\nNS_ :\n    NS_DESC_\n    CM_\n    BA_DEF_\n    BA_\n    VAL_\n\nBS_:\n\nBU_: ECU_EM ECU_ICE VEH_DYNAMICS\n\nBO_ 257 ECU_EM: 8 ECU_EM\n SG_ iq_a : 0|16@1+ (0.1,0) [-3276.8|3276.7] \"A\" ECU_EM\n SG_ rpm : 16|16@1+ (1,0) [0|65535] \"rpm\" ECU_EM\n SG_ temp_c : 32|16@1- (0.1,0) [-3276.8|3276.7] \"degC\" ECU_EM\n\nBO_ 258 ECU_ICE: 8 ECU_ICE\n SG_ rpm : 0|16@1+ (1,0) [0|65535] \"rpm\" ECU_ICE\n SG_ k0_status : 16|8@1+ (1,0) [0|255] \"state\" ECU_ICE\n SG_ k0_pressure_bar : 24|16@1+ (0.1,0) [0|6553.5] \"bar\" ECU_ICE\n\nBO_ 259 VEH_DYNAMICS: 8 VEH_DYNAMICS\n SG_ speed_kmh : 0|16@1+ (0.01,0) [0|655.35] \"km/h\" VEH_DYNAMICS\n SG_ tps_pct : 16|8@1+ (0.5,0) [0|127.5] \"pct\" VEH_DYNAMICS\n SG_ brake_pct : 24|8@1+ (0.5,0) [0|127.5] \"pct\" VEH_DYNAMICS\n SG_ gx : 32|8@1- (0.01,0) [-1.28|1.27] \"g\" VEH_DYNAMICS\n SG_ gy : 40|8@1- (0.01,0) [-1.28|1.27] \"g\" VEH_DYNAMICS\n"""


def generate_default_dbc(output_path=DEFAULT_DBC_PATH):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(DBC_TEXT, encoding="ascii")
    return output_path


if __name__ == "__main__":
    print(generate_default_dbc())
