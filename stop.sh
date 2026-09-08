#!/data/data/com.termux/files/usr/bin/bash
echo "[*] Encerrando processos do MarleyOS..."
pkill -9 -f "python.*server.py" 2>/dev/null
pkill -9 -f "python.*telemetry_feeder.py" 2>/dev/null
fuser -k 8080/tcp 2>/dev/null
termux-wake-unlock 2>/dev/null
echo "[+] MarleyOS Cockpit e Feeder desligados com sucesso."
