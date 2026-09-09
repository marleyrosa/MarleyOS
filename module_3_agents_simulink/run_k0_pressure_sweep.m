function results = run_k0_pressure_sweep(modelName, inputDataset, pressureValues)
%RUN_K0_PRESSURE_SWEEP Run a compact K0 sensitivity MIL sweep.

    arguments
        modelName (1,1) string = "MIL_MarleyOS_Powertrain"
        inputDataset = []
        pressureValues (1,:) double = [12 16 20]
    end

    results = table('Size', [numel(pressureValues), 3], ...
        'VariableTypes', {'double', 'double', 'string'}, ...
        'VariableNames', {'pressure_bar', 'peak_residual', 'status'});
    for index = 1:numel(pressureValues)
        calibration = struct('Calib_K0_PressureMax', pressureValues(index));
        runResult = run_4mains_mil(modelName, 1, inputDataset, calibration);
        residual = runResult.logsout.get('deceleration_residual');
        if isa(residual, 'timeseries')
            residualData = residual.Data;
        else
            residualData = residual.Values.Data;
        end
        peakResidual = max(abs(double(residualData(:))));
        results.pressure_bar(index) = pressureValues(index);
        results.peak_residual(index) = peakResidual;
        results.status(index) = "PASS";
    end
end