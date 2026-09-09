function result = run_4mains_mil(modelName, stopTime, inputDataset, calibrations)
%RUN_4MAINS_MIL Execute the 4-Mains MIL contract through MATLAB MCP.

    arguments
        modelName (1,1) string
        stopTime (1,1) double {mustBePositive}
        inputDataset = []
        calibrations (1,1) struct = struct()
    end

    simIn = Simulink.SimulationInput(modelName);
    simIn = simIn.setModelParameter( ...
        'StopTime', num2str(stopTime), ...
        'SaveOutput', 'on', ...
        'SaveFormat', 'Dataset', ...
        'SignalLogging', 'on', ...
        'SignalLoggingName', 'logsout');

    if ~isfield(calibrations, 'Calib_K0_PressureMax')
        simIn = simIn.setVariable('Calib_K0_PressureMax', 18.0);
    end

    if ~isempty(inputDataset)
        simIn = simIn.setVariable('CommunicationDataset', inputDataset);
        simIn = simIn.setModelParameter( ...
            'LoadExternalInput', 'on', ...
            'ExternalInput', 'CommunicationDataset');
    end

    calibrationNames = fieldnames(calibrations);
    for index = 1:numel(calibrationNames)
        simIn = simIn.setVariable( ...
            calibrationNames{index}, calibrations.(calibrationNames{index}));
    end

    simOut = sim(simIn);
    if ~isprop(simOut, 'logsout') || isempty(simOut.logsout)
        error('run_4mains_mil:MissingLogsout', ...
            'MIL model did not produce logsout. Mark at least one SISTEMA signal for logging.');
    end
    logsout = simOut.logsout;
    result = struct('modelName', modelName, 'stopTime', stopTime, ...
        'logsout', logsout, 'metrics', collect_metrics(logsout));
    fprintf('MARLEYOS_METRICS=%s\n', jsonencode(result.metrics));
end

function metrics = collect_metrics(logsout)
    metrics = struct();
    metrics.signalCount = logsout.numElements;
    metrics.signalNames = strings(logsout.numElements, 1);
    for index = 1:logsout.numElements
        metrics.signalNames(index) = string(logsout.getElement(index).Name);
    end
    metrics.peakIqA = metric_max(logsout, {'iq_a', 'Iq', 'iq'});
    metrics.peakGx = metric_max(logsout, {'Gx', 'gx'});
    metrics.peakGy = metric_max(logsout, {'Gy', 'gy'});
    metrics.bsfcGPerKwh = metric_max(logsout, {'BSFC', 'bsfc_g_kwh'});
    metrics.peakDecelerationResidual = metric_max(logsout, {'deceleration_residual'});
end

function value = metric_max(logsout, candidates)
    value = NaN;
    for candidate = candidates
        try
            element = logsout.get(candidate{1});
            if isa(element, 'timeseries')
                data = element.Data;
            else
                data = element.Values.Data;
            end
            value = max(abs(double(data(:))));
            return;
        catch
        end
    end
end