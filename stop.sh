#!/data/data/com.termux/files/usr/bin/bash

echo "[*] Encerrando processos do server.py..."
pkill -9 -f "server.py" 2>/dev/null || true

echo "[*] Liberando wake-lock..."
termux-wake-unlock

echo "[+] MarleyOS Cockpit desligado com sucesso."
