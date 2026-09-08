#!/usr/bin/env bash
set -euo pipefail

echo "=== Inicializando MarleyOS Engine ==="
cd "$(dirname "$0")"

PYTHON="${PYTHON:-python3}"
if ! command -v "$PYTHON" >/dev/null 2>&1; then
	PYTHON=python
fi

if ! command -v "$PYTHON" >/dev/null 2>&1; then
	echo "Python não encontrado. Defina PYTHON ou instale Python 3." >&2
	exit 1
fi

# Executar suíte de testes
echo "[1/3] Executando testes unitários..."
"$PYTHON" test_pipeline.py

# Iniciar o servidor do Dashboard
echo "[2/3] Subindo Cockpit Web na porta 8080..."
"$PYTHON" dashboard/server.py &
SERVER_PID=$!

for attempt in {1..20}; do
	if curl --silent --fail http://localhost:8080 >/dev/null 2>&1; then
		break
	fi
	if ! kill -0 "$SERVER_PID" 2>/dev/null; then
		echo "O servidor encerrou antes de ficar disponível." >&2
		exit 1
	fi
	sleep 0.25
done

if ! curl --silent --fail http://localhost:8080 >/dev/null 2>&1; then
	echo "O dashboard não respondeu em http://localhost:8080." >&2
	exit 1
fi

echo "[3/3] MarleyOS ativo!"
echo "Acesse o Cockpit no navegador: http://localhost:8080"
