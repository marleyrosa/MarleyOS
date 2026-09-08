# Capítulo 1: Arquitetura Híbrida P2 & Modelagem Eletromecânica Fundamental

## 1.1 Topologia Mecânica P2
Arranjo coaxial entre o motor ICE 1.5L Miller, a embreagem de desconexão K0, o motor síncrono PMSM e a caixa e-DCT.

## 1.2 Modelagem Matemática do PMSM
- Tensões nos eixos d-q: v_d = R_s*i_d + d(lambda_d)/dt - omega_e*lambda_q
- Tensões nos eixos d-q: v_q = R_s*i_q + d(lambda_q)/dt + omega_e*lambda_d
- Torque MTPA (i_d = 0): T_em = 1.5 * p * lambda_pm * i_q
- Constante K_t = 0.48 Nm/A (p = 4, lambda_pm = 0.08 Wb)

## 1.3 Dinâmica Hidráulica de K0
- Fase 1 (Open/Sync): Delta_omega > 150 RPM, P = 0.5 bar
- Fase 2 (Slipping): 20 < Delta_omega <= 150 RPM, P = 2.0 a 12.0 bar progressivo
- Fase 3 (Locked): Delta_omega <= 20 RPM, P = 18.0 bar

## 1.4 Transmissão e-DCT Dual-Shaft
- Eixo Sólido (C1): Marchas 1, 3 e 5
- Eixo Oco (C2): Marchas 2, 4, 6 e Ré
