# Diretrizes de IA para Modelagem e Simulação em MATLAB / Simulink

Ao sintetizar código MATLAB para o projeto MarleyOS via MATLAB MCP Core Server ou GitHub Copilot, siga estritamente estas diretrizes:

1. Simulação Moderna:
   - Utilize a classe Simulink.SimulationInput em vez da sintaxe legada no comando sim().
   - Configure parâmetros do modelo via .setModelParameter('ParamName', 'Value').
   - Ajuste variáveis de calibração via .setVariable('VarName', value).

2. Entradas Externas:
   - Nunca use arrays simples concatenados [t, u] sem ativar LoadExternalInput.
   - Dê preferência a estruturas Simulink.SimulationData.Dataset.

3. Carregamento e Extração:
   - Não use load_system de forma redundante se o objeto de simulação gerencia o carregamento.
   - Extraia logs de sinais a partir de simOut.logsout ou simOut.yout no formato Dataset.
