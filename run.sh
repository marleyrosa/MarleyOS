#!/data/data/com.termux/files/usr/bin/bash
PROJECT_DIR="$HOME/MarleyOS"
cd "$PROJECT_DIR" || exit 1

pkill -9 -f "python.*server.py" 2>/dev/null
pkill -9 -f "python.*telemetry_feeder.py" 2>/dev/null
fuser -k 8080/tcp 2>/dev/null

mkdir -p module_2_mcp/data
if [ ! -f module_2_mcp/data/can_telemetry.csv ]; then
  echo "timestamp_s,rpm,torque_nm,throttle_pct,iq_a,modo_propulsao,status_motor" > module_2_mcp/data/can_telemetry.csv
  echo "0.0,0,0.0,0.0,0.0,EV_MODE,NOMINAL" >> module_2_mcp/data/can_telemetry.csv
fi

termux-wake-lock 2>/dev/null

nohup python dashboard/server.py > server.log 2>&1 &
SERVER_PID=$!

nohup python module_2_mcp/telemetry_feeder.py > feeder.log 2>&1 &
FEEDER_PID=$!

echo "[+] Servidor Cockpit ativo (PID: $SERVER_PID)"
echo "[+] Telemetry Feeder ativo (PID: $FEEDER_PID)"
echo "[+] Cockpit pronto: http://localhost:8080"
