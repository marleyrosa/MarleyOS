# MarleyOS — Automotive AI Cockpit & Systems Engineering Engine

Plataforma aberta de Inteligência Artificial aplicada à Engenharia Automotiva, Diagnóstico de Bordo (OBD-II), Protocolo MCP, Sistemas Embarcados e Validação Funcional (ISO 26262).



> [!WARNING]
> ### 📱 Troubleshooting para Ambientes Restritos (ex: Termux no Android / WSL / Containers)
> 1. **Isolamento de Arquivos Temporários (`*.slxc`, `*.csv.tmp`, `slprj/`):**
>    Sessões do Simulink e o feeder de telemetria contínua (`telemetry_feeder.py`) geram caches binários de compilação (`*.slxc`, `slprj/`) e buffers rotativos de telemetria (`*.csv.tmp`). Em sistemas móveis (como emulação FUSE/ext4 do Android no Termux), o acúmulo desses arquivos causa conflito de bloqueio de arquivo (*file lock contention / EBUSY*), esgotamento de inodes e lentidão no controle de versão.
> 2. **Diretório Temporário Dedicado:** Configure `export TMPDIR=$PREFIX/tmp` (Termux) ou `export TMPDIR=/tmp` (Linux/WSL) para isolar arquivos voláteis em RAM/storage temporário.
> 3. **Purga Periódica:** Limpe resíduos temporários executando: `find . -name "*.slxc" -o -name "*.csv.tmp" -o -name "*.pyc" -delete`.
> 4. **Permissões de Execução:** Em sistemas de arquivos móveis, garanta permissão nos scripts shell: `chmod +x *.sh start_marleyos.sh`.

---

## 🚘 Módulos e Subsistemas Monitorados

| Componente | Função Primária | Sinais & Protocolos | Nível ASIL (ISO 26262) |
| :--- | :--- | :--- | :--- |
| **Inversor de Tração** | Controle de ponte trifásica e torque EV | Corrente de Fase, Temperatura IGBT | ASIL-D |
| **Freio Regenerativo (ABS)** | Distribuição de frenagem mecânica/elétrica | Pressão Eletro-Hidráulica (Bar) | ASIL-D |
| **Direção Elétrica (EPS)** | Assistência dinâmica e retorno ativo | Torque de Coluna (Nm), Corrente Motor | ASIL-C |
| **ECM** | Controle de injeção e atuador de borboleta | Posição TPS (%), Pressão MAP (kPa) | ASIL-D |
| **BCM** | Gateway de carroceria e cargas secundárias | Tensão de Barramento (V), Relés | ASIL-B / QM |
| **TCM** | Controle eletro-hidráulico de marchas | Pressão de Linha (Bar), Embreagem | ASIL-C |
| **BPCM (HV BMS)** | Monitoramento de células e segurança de alta tensão | Resistência de Isolamento (kΩ), Pyro-Fuse | ASIL-D |

---

## 🛠️ Arquitetura Técnica de IA

* **RAG Engine (Módulo 1):** Vetorização e recuperação semântica de manuais técnicos e códigos DTC.
* **CAN MCP Server (Módulo 2):** Servidor JSON-RPC expondo telemetria no padrão Model Context Protocol.
* **ReAct Tuning Agent & Simulink (Módulo 3):** Agente integrado ao MATLAB MCP Core Server para calibração autônoma com Simulink.SimulationInput.
* **ASIL Evaluator (Módulo 4):** Validação estruturada sob a norma ISO 26262 com datasets JSONL.
* **CI/CD MLOps (Módulo 5):** Suíte de testes automatizada com auditoria de Pull Requests via GitHub Actions.
* **Cockpit Web Interativo (Módulo 6):** Dashboard com visual glassmorphism, orbe pulsante de status e copilot automotivo.

---

## � Como o Sistema Funciona

O MarleyOS executa um ciclo operacional completo para validar, publicar e consumir dados de engenharia automotiva:

1. `test_pipeline.py` valida a base funcional do projeto e confirma que os módulos principais estão íntegros.
2. `start_marleyos.ps1` inicia o sistema em Windows em três etapas: testes, subida do cockpit web e ativação do feeder de telemetria.
3. `dashboard/server.py` publica a interface em `http://localhost:8080` e consome o arquivo `module_2_mcp/data/can_telemetry.csv` para atualizar o painel em tempo real.
4. `module_2_mcp/telemetry_feeder.py` gera linhas CSV com timestamps, RPM, torque, throttle, corrente e status do motor.
5. `module_2_mcp/mcp_server.py` expõe o protocolo MCP para consultar resumo da telemetria e eventos críticos por JSON-RPC.
6. `.vscode/mcp.json` conecta o VS Code aos servidores `matlab` e `marleyos_can`, permitindo invocar MATLAB e a telemetria diretamente da IDE.
7. O fluxo de calibração usa o MATLAB MCP Server com `Simulink.SimulationInput`, `SaveFormat=Dataset` e `logsout`, permitindo execução e simulação em ambiente controlado.

Em operação, o ciclo é: validação → dashboard web → telemetria em CSV → consulta via MCP → automação MATLAB/Simulink.

## �🚀 Como Executar

### 1. Inicialização Completa
```bash
./start_marleyos.sh
python exports/export_audit.py
