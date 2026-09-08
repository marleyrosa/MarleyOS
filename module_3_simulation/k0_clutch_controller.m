function [k0_pressure_bar, k0_state, pmsm_torque_offset] = k0_clutch_controller(omega_ice_rpm, omega_em_rpm, mode_req)
% K0_CLUTCH_CONTROLLER - Gerenciamento de Acoplamento Hidráulico da Embreagem K0
% Entradas:
%   omega_ice_rpm      : Velocidade do virabrequim (RPM)
%   omega_em_rpm       : Velocidade do rotor PMSM (RPM)
%   mode_req           : Demanda de modo ('EV_MODE', 'P2_HYBRID_BOOST', 'REGEN_BRAKE')
%
% Saídas:
%   k0_pressure_bar    : Pressão da linha hidráulica do atuador (0 a 18 bar)
%   k0_state           : Estado discreto (0=OPEN, 1=SLIPPING, 2=LOCKED)
%   pmsm_torque_offset : Compensação ativa de torque no PMSM (Nm)

    delta_rpm = abs(omega_ice_rpm - omega_em_rpm);

    switch mode_req
        case 'P2_HYBRID_BOOST'
            if delta_rpm > 150.0
                % Fase 1: Sincronizando (K0 aberta ou encosto suave)
                k0_state = 0;
                k0_pressure_bar = 0.5; % Pressão de pré-carregamento (kiss-point)
                pmsm_torque_offset = 0.0;
            elseif delta_rpm <= 150.0 && delta_rpm > 20.0
                % Fase 2: Escorregamento regulado (Slipping)
                k0_state = 1;
                % Rampa progressiva proporcional à redução da rotação diferencial
                k0_pressure_bar = 2.0 + (1.0 - delta_rpm / 150.0) * 10.0;
                % PMSM compensa o torque de arrasto imposto pelo virabrequim
                pmsm_torque_offset = k0_pressure_bar * 4.2; 
            else
                % Fase 3: Bloqueado (Locked)
                k0_state = 2;
                k0_pressure_bar = 18.0; % Pressão de travamento nominal
                pmsm_torque_offset = 0.0;
            end

        otherwise
            % EV_MODE ou REGEN_BRAKE: K0 Desacoplada
            k0_state = 0;
            k0_pressure_bar = 0.0;
            pmsm_torque_offset = 0.0;
    end
end
