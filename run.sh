#!/data/data/com.termux/files/usr/bin/bash

echo "[*] Limpando instâncias anteriores do servidor..."
pkill -9 -f "server.py" 2>/dev/null || true

echo "[*] Ativando termux-wake-lock contra suspensão..."
termux-wake-lock

echo "[*] Iniciando dashboard/server.py em background..."
nohup python dashboard/server.py > server.log 2>&1 &

sleep 1

PID=$(pgrep -f "dashboard/server.py")
if [ -n "$PID" ]; then
    echo "[+] Servidor ativo com PID: $PID"
    echo "[+] Cockpit pronto: http://localhost:8080"
    echo "[i] Para acompanhar logs: tail -f ~/MarleyOS/server.log"
else
    echo "[-] Falha na inicialização. Verifique server.log:"
    cat server.log
fi
