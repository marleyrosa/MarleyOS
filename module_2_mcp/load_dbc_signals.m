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
    signalDataset = Simulink.SimulationData.Dataset;
    for index = 1:numel(names)
        sourceName = names(index);
        if sourceName == timeName
            continue;
        end
        outputName = sourceName;
        if isfield(signalMap, char(sourceName))
            outputName = string(signalMap.(char(sourceName)));
        end
        rawCol = sourceTable.(sourceName);
        if iscell(rawCol) || isstring(rawCol)
            [~, ~, numericValues] = unique(string(rawCol));
            values = double(numericValues);
        else
            values = double(rawCol);
        end
        signalDataset = signalDataset.addElement( ...
            timeseries(values(:), time(:), 'Name', char(outputName)), char(outputName));
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