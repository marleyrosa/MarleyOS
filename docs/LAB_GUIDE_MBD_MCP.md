# Laboratory Guide: Simulink Automation with MATLAB MCP Server

**Author:** Eng. Marley Rosa Luciano | **Program:** NexusMBD AI-Native Powertrain Suite

---

## 1. Host Environment Configuration
1. Install **Visual Studio Code** and the **GitHub Copilot Chat** extension.
2. Download the **MATLAB MCP Core Server** binary from MathWorks.
3. Configure the `.vscode/mcp.json` file in the MarleyOS root directory:
```json
{
  "servers": {
    "matlab": {
      "type": "stdio",
      "command": "C:\\MATLAB\\MCP\\server\\matlab-mcp-core-server-win64.exe",
      "args": [
        "--matlab-root=C:\\Program Files\\MATLAB\\R2026a",
        "--initialize-matlab-on-startup=true",
        "--initial-working-folder=C:\\Users\\UsuarioPC\\MarleyOS"
      ]
    },
    "nexusmbd_can": {
      "type": "stdio",
      "command": "python",
      "args": [
        "module_2_mcp/mcp_server.py"
      ]
    }
  }
}
```

---

## 2. Headless Simulation & Agent Execution
To execute autonomous calibration runs without opening the graphical editor:
```bash
python -u dashboard/server.py --host 0.0.0.0 --port 8080
```
Open `http://localhost:8080` and trigger the automated MIL simulator to stream synchronized 4-Mains telemetry.
