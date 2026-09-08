function [mode_str, k0_clutch, torque_ice, torque_em] = p2_mode_supervisor(throttle_pct, brake_bar, v_veh_kph)
% P2_MODE_SUPERVISOR - Gerenciador de Estados do Trem de Forca HEV P2
% Entradas:
%   throttle_pct : Demanda do condutor (0 a 100%)
%   brake_bar    : Pressao da linha de freio (bar)
%   v_veh_kph    : Velocidade do veiculo (km/h)
%
% Saidas:
%   mode_str     : String com o modo ativo
%   k0_clutch    : Estado da embreagem K0 (0 = Aberta, 1 = Acoplada)
%   torque_ice   : Demanda de torque para motor termico (Nm)
%   torque_em    : Demanda de torque para maquina eletrica (Nm)

    if brake_bar > 1.0
        % Frenagem Regenerativa: Desacopla ICE para evitar arrasto termico
        mode_str   = 'REGEN_BRAKE';
        k0_clutch  = 0;
        torque_ice = 0.0;
        torque_em  = -min(80.0, brake_bar * 4.0); % Regeneracao limitada
    elseif throttle_pct <= 35.0 && v_veh_kph < 60.0
        % Modo Eletrico: K0 aberta, ICE em repouso
        mode_str   = 'EV_MODE';
        k0_clutch  = 0;
        torque_ice = 0.0;
        torque_em  = throttle_pct * 3.5;
    else
        % Modo Hibrido Boost: K0 acoplada, soma de torques
        mode_str   = 'P2_HYBRID_BOOST';
        k0_clutch  = 1;
        torque_ice = throttle_pct * 2.8;
        torque_em  = min(180.0, throttle_pct * 2.2);
    end
end
