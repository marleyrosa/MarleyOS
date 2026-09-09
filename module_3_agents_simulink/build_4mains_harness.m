function modelPath = build_4mains_harness(outputDir)
%BUILD_4MAINS_HARNESS Create the minimal 4-Mains MIL Simulink harness.

    arguments
        outputDir (1,1) string = string(fileparts(fileparts(mfilename('fullpath'))))
    end

    modelName = "MIL_MarleyOS_Powertrain";
    modelPath = fullfile(outputDir, modelName + ".slx");
    if bdIsLoaded(modelName)
        close_system(modelName, 0);
    end
    if isfile(modelPath)
        delete(modelPath);
    end

    new_system(modelName);
    set_param(modelName, ...
        'SaveOutput', 'on', ...
        'SaveFormat', 'Dataset', ...
        'SignalLogging', 'on', ...
        'SignalLoggingName', 'logsout', ...
        'LoadExternalInput', 'on', ...
        'ExternalInput', 'CommunicationDataset', ...
        'StopTime', '10');

    mains = { ...
        'COMUNICACAO', 'SOFTECU', 'MDL', 'SISTEMA'};
    positions = [30 80 230 220; 280 80 480 220; 530 80 730 220; 780 80 980 220];
    for index = 1:numel(mains)
        mainPath = modelName + "/" + string(mains{index});
        add_block('built-in/Subsystem', mainPath, ...
            'Position', positions(index, :));
        switch mains{index}
            case 'COMUNICACAO'
                build_communication_main(mainPath);
            case 'SOFTECU'
                build_softecu_main(mainPath);
            case 'MDL'
                build_mdl_main(mainPath);
            case 'SISTEMA'
                build_system_main(mainPath);
        end
    end

    for inputIndex = 1:11
        inputName = "CommunicationInput" + inputIndex;
        inputY = 40 + (inputIndex - 1) * 28;
        add_block('simulink/Ports & Subsystems/In1', modelName + "/" + inputName, ...
            'Position', [1 inputY 31 inputY + 20]);
        if inputIndex == 1
            add_line(modelName, inputName + "/1", 'COMUNICACAO/1');
        else
            terminatorName = "UnusedInputTerminator" + inputIndex;
            add_block('simulink/Sinks/Terminator', modelName + "/" + terminatorName, ...
                'Position', [40 inputY 70 inputY + 20]);
            add_line(modelName, inputName + "/1", terminatorName + "/1");
        end
    end
    add_line(modelName, 'COMUNICACAO/1', 'SOFTECU/1');
    add_line(modelName, 'SOFTECU/1', 'MDL/1');
    add_line(modelName, 'MDL/1', 'SISTEMA/1');
    outputNames = {'iq_a', 'BSFC', 'Gx', 'Gy', 'MIL_Output', 'K0_Pressure', 'deceleration_residual'};
    for outputIndex = 1:numel(outputNames)
        outputName = string(outputNames{outputIndex});
        outputY = 40 + (outputIndex - 1) * 28;
        add_block('simulink/Ports & Subsystems/Out1', modelName + "/" + outputName, ...
            'Position', [1000 outputY 1030 outputY + 20]);
        outputLine = add_line(modelName, "SISTEMA/" + outputIndex, outputName + "/1");
        set_param(outputLine, 'Name', char(outputName));
    end
    systemPorts = get_param(modelName + "/SISTEMA", 'PortHandles');
    for outputIndex = 1:numel(systemPorts.Outport)
        if systemPorts.Outport(outputIndex) ~= -1
            set_param(systemPorts.Outport(outputIndex), 'DataLogging', 'on');
        end
    end

    save_system(modelName, modelPath);
    close_system(modelName, 0);
    fprintf('[OK] 4-Mains harness created: %s\n', modelPath);
end

function build_communication_main(mainPath)
    add_block('simulink/Ports & Subsystems/In1', mainPath + "/In1", 'Position', [30 48 60 62]);
    add_block('simulink/Ports & Subsystems/Out1', mainPath + "/Out1", 'Position', [150 48 180 62]);
    add_block('simulink/Math Operations/Gain', mainPath + "/CommunicationBus", ...
        'Gain', '1', 'Position', [85 42 125 68]);
    add_line(mainPath, 'In1/1', 'CommunicationBus/1');
    add_line(mainPath, 'CommunicationBus/1', 'Out1/1');
end

function build_softecu_main(mainPath)
    add_block('simulink/Ports & Subsystems/In1', mainPath + "/In1", 'Position', [30 48 60 62]);
    add_block('simulink/User-Defined Functions/MATLAB Function', mainPath + "/SOFTECU_Logic", ...
        'Position', [90 30 220 80]);
    set_matlab_function_script(mainPath + "/SOFTECU_Logic", [ ...
        "function y = sofecu_logic(u)" newline ...
        "% K0: OPEN -> SYNC -> SLIP -> LOCKED, pressure limited to 18 bar." newline ...
        "y = zeros(5,1,'double');" newline ...
        "speed = double(u(1));" newline ...
        "deltaOmega = abs(speed * 0.1);" newline ...
        "if deltaOmega > 20" newline ...
        "    k0State = 0; k0Pressure = 0;" newline ...
        "elseif deltaOmega > 8" newline ...
        "    k0State = 1; k0Pressure = 6;" newline ...
        "elseif deltaOmega > 1" newline ...
        "    k0State = 2; k0Pressure = min(Calib_K0_PressureMax, 6 + (8-deltaOmega)*2);" newline ...
        "else" newline ...
        "    k0State = 3; k0Pressure = Calib_K0_PressureMax;" newline ...
        "end" newline ...
        "gear = min(6, max(1, floor(abs(speed)/10)+1));" newline ...
        "clutch = 1 + mod(gear, 2);" newline ...
        "iq = max(-200, min(200, speed * 0.5));" newline ...
        "y = [iq; k0Pressure; k0State; clutch; gear];" newline ...
        "end" ]);
    configure_chart_symbols(mainPath + "/SOFTECU_Logic", 1, 5, "Calib_K0_PressureMax");
    add_block('simulink/Ports & Subsystems/Out1', mainPath + "/Out1", 'Position', [260 48 290 62]);
    add_line(mainPath, 'In1/1', 'SOFTECU_Logic/1');
    add_line(mainPath, 'SOFTECU_Logic/1', 'Out1/1');
end

function build_mdl_main(mainPath)
    add_block('simulink/Ports & Subsystems/In1', mainPath + "/In1", 'Position', [30 48 60 62]);
    add_block('simulink/User-Defined Functions/MATLAB Function', mainPath + "/MDL_Logic", ...
        'Position', [90 30 220 80]);
    set_matlab_function_script(mainPath + "/MDL_Logic", [ ...
        "function y = mdl_logic(u)" newline ...
        "% PMSM torque and simplified vehicle inertial dynamics." newline ...
        "y = zeros(8,1,'double');" newline ...
        "p = 4; lambda_pm = 0.08; J = 120;" newline ...
        "iq = double(u(1));" newline ...
        "Tem = 1.5 * p * lambda_pm * iq;" newline ...
        "accel = Tem / J;" newline ...
        "gx = accel / 9.81; gy = 0;" newline ...
        "vehicleSpeed = max(0, double(u(5)));" newline ...
        "engineRpm = vehicleSpeed * 42;" newline ...
        "bsfc = 250 + abs(Tem) * 0.05;" newline ...
        "y = [iq; bsfc; gx; gy; Tem; vehicleSpeed; engineRpm; double(u(2))];" newline ...
        "end" ]);
    configure_chart_symbols(mainPath + "/MDL_Logic", 8, 8, "");
    add_block('simulink/Ports & Subsystems/Out1', mainPath + "/Out1", 'Position', [260 48 290 62]);
    add_line(mainPath, 'In1/1', 'MDL_Logic/1');
    add_line(mainPath, 'MDL_Logic/1', 'Out1/1');
end

function build_system_main(mainPath)
    add_block('simulink/Ports & Subsystems/In1', mainPath + "/In1", 'Position', [30 48 60 62]);
    add_block('simulink/User-Defined Functions/MATLAB Function', mainPath + "/SISTEMA_Metrics", ...
        'Position', [90 30 240 80]);
    set_matlab_function_script(mainPath + "/SISTEMA_Metrics", [ ...
        "function [iq_a, BSFC, Gx, Gy, MIL_Output, K0_Pressure, deceleration_residual] = sistema_metrics(u)" newline ...
        "iq_a = u(1); BSFC = u(2); Gx = u(3); Gy = u(4);" newline ...
        "MIL_Output = u(5); K0_Pressure = u(8); deceleration_residual = abs(u(3));" newline ...
        "end" ]);
    outputNames = {'iq_a', 'BSFC', 'Gx', 'Gy', 'MIL_Output', 'K0_Pressure', 'deceleration_residual'};
    for outputIndex = 1:numel(outputNames)
        outputName = string(outputNames{outputIndex});
        outputY = 30 + (outputIndex - 1) * 24;
        add_block('simulink/Ports & Subsystems/Out1', mainPath + "/" + outputName, ...
            'Position', [300 outputY 330 outputY + 16]);
        add_line(mainPath, "SISTEMA_Metrics/" + outputIndex, outputName + "/1");
    end
    add_line(mainPath, 'In1/1', 'SISTEMA_Metrics/1');
end

function set_matlab_function_script(blockPath, scriptText)
    chart = find(sfroot, '-isa', 'Stateflow.EMChart', 'Path', char(blockPath));
    if isempty(chart)
        error('build_4mains_harness:MissingChart', ...
            'MATLAB Function chart not found: %s', blockPath);
    end
    chart.Script = char(scriptText);
end

function configure_chart_symbols(blockPath, inputSize, outputSize, parameterName)
    chart = find(sfroot, '-isa', 'Stateflow.EMChart', 'Path', char(blockPath));
    data = find(chart, '-isa', 'Stateflow.Data');
    if strlength(parameterName) > 0 && isempty(find(data, 'Name', char(parameterName)))
        parameter = Stateflow.Data(chart);
        parameter.Name = char(parameterName);
        parameter.Scope = 'Parameter';
        parameter.DataType = 'double';
    end
end
