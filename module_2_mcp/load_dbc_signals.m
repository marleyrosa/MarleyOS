function signalDataset = load_dbc_signals(inputFile, signalMap)
%LOAD_DBC_SIGNALS Convert CSV signals to a SimulationData.Dataset.
%   CSV input must contain timestamp_s, time_s, or time.

    arguments
        inputFile (1,1) string
        signalMap (1,1) struct = struct()
    end

    [~, ~, extension] = fileparts(inputFile);
    if ~strcmpi(extension, '.csv')
        error('load_dbc_signals:UnsupportedInput', ...
            'Convert DBC/BLF captures to CSV with Vehicle Network Toolbox first.');
    end

    sourceTable = readtable(inputFile, 'VariableNamingRule', 'preserve');
    names = string(sourceTable.Properties.VariableNames);
    timeName = first_matching_name(names, ["timestamp_s", "time_s", "time"]);
    if strlength(timeName) == 0
        error('load_dbc_signals:MissingTime', ...
            'Input must contain timestamp_s, time_s, or time.');
    end

    time = double(sourceTable.(timeName));

    expectedSignals = { ...
        'vehicle_speed', 'engine_speed', 'throttle_pedal', 'brake_pedal', ...
        'gear_active', 'trans_oil_temp', 'inverter_temp', 'battery_temp', ...
        'k0_status', 'driving_mode', 'p2_torque_demand' ...
    };

    signalDataset = Simulink.SimulationData.Dataset;
    for i = 1:numel(expectedSignals)
        sigName = expectedSignals{i};
        sourceCol = resolve_signal_column(sigName, names, signalMap);

        if strlength(sourceCol) > 0 && ismember(sourceCol, names)
            rawCol = sourceTable.(sourceCol);
            if iscell(rawCol) || isstring(rawCol) || iscategorical(rawCol)
                [~, ~, numericValues] = unique(string(rawCol));
                values = double(numericValues);
            else
                values = double(rawCol);
            end
        else
            values = zeros(numel(time), 1);
        end

        signalDataset = signalDataset.addElement( ...
            timeseries(values(:), time(:), 'Name', char(sigName)), char(sigName));
    end
end

function colName = resolve_signal_column(targetName, names, signalMap)
    colName = "";
    if isfield(signalMap, char(targetName))
        candidate = string(signalMap.(char(targetName)));
        match = find(strcmpi(names, candidate), 1);
        if ~isempty(match)
            colName = names(match);
            return;
        end
    end

    fields = fieldnames(signalMap);
    for k = 1:numel(fields)
        f = string(fields{k});
        if strcmpi(string(signalMap.(char(f))), targetName)
            match = find(strcmpi(names, f), 1);
            if ~isempty(match)
                colName = names(match);
                return;
            end
        end
    end

    aliases = get_signal_aliases(targetName);
    for k = 1:numel(aliases)
        match = find(strcmpi(names, aliases(k)), 1);
        if ~isempty(match)
            colName = names(match);
            return;
        end
    end
end

function aliases = get_signal_aliases(sigName)
    switch lower(sigName)
        case 'vehicle_speed'
            aliases = ["vehicle_speed", "speed_kmh", "VehicleSpeed", "speed"];
        case 'engine_speed'
            aliases = ["engine_speed", "rpm_ice", "EngineSpeed", "rpm", "rpm_em"];
        case 'throttle_pedal'
            aliases = ["throttle_pedal", "throttle_pct", "Throttle", "throttle"];
        case 'brake_pedal'
            aliases = ["brake_pedal", "brake_pct", "BrakeTorque", "brake"];
        case 'gear_active'
            aliases = ["gear_active", "gear", "TransmissionRatio", "active_gear"];
        case 'trans_oil_temp'
            aliases = ["trans_oil_temp", "oil_temp", "transmission_oil_temp"];
        case 'inverter_temp'
            aliases = ["inverter_temp", "temp_inv_c", "temp_inv", "inverter_temperature"];
        case 'battery_temp'
            aliases = ["battery_temp", "temp_bat_c", "temp_bat", "battery_temperature"];
        case 'k0_status'
            aliases = ["k0_status", "k0_state", "k0_press_bar"];
        case 'driving_mode'
            aliases = ["driving_mode", "modo_propulsao", "mode", "status_motor"];
        case 'p2_torque_demand'
            aliases = ["p2_torque_demand", "torque_nm", "EMTrqReq", "torque"];
        otherwise
            aliases = string(sigName);
    end
end

function name = first_matching_name(names, candidates)
    name = "";
    for candidate = candidates
        match = find(strcmpi(names, candidate), 1);
        if ~isempty(match)
            name = names(match);
            return;
        end
    end
end
