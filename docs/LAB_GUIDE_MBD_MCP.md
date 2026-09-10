# Guia de Laboratório: Automação Simulink com MATLAB MCP Server
**Autor:** Eng. Marley Rosa Luciano | **Formação:** NexusMBD AI-Native Powertrain Suite

## 1. Configuração do Ambiente Host
1. Instalar o **Visual Studio Code** e a extensão **GitHub Copilot Chat**[span_3](start_span)[span_3](end_span).
2. Baixar o executável do **MATLAB MCP Core Server** do repositório oficial da MathWorks[span_4](start_span)[span_4](end_span).
3. Configurar o arquivo `.vscode/mcp.json` na raiz do repositório MarleyOS com a diretiva de persistência[span_5](start_span)[span_5](end_span):
```json
{
  "servers": {
    "matlab": {
      "type": "stdio",
      "command": "C:\\MATLAB\\MCP\\server\\matlab-mcp-core-server-win64.exe",
      "args": [
        "--matlab-root=C:\\MATLAB\\R2024b",
        "--initialize-matlab-on-startup=true",
        "--initial-working-folder=C:\\Workspace\\MarleyOS"
      ]
    }
  }
}

