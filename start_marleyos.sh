#!/bin/bash
echo "=== Inicializando MarleyOS Engine ==="
cd "$(dirname "$0")"

# Encerrar instâncias antigas
kill -9 $(lsof -t -i:8080) 2>/dev/null || pkill -9 -f "server.py" 2>/dev/null || true

# Executar suíte de testes
echo "[1/3] Executando testes unitários..."
python test_pipeline.py

# Iniciar o servidor do Dashboard
echo "[2/3] Subindo Cockpit Web na porta 8080..."
python dashboard/server.py &

# Exibir status
sleep 1
echo "[3/3] MarleyOS ativo!"
echo "Acesse o Cockpit no navegador: http://localhost:8080"
