function [pulse] = pulsegen(freq, fs, baud, parity)
    persistent pcode;
    pcode = fliplr([+1, +1, -1, +1, +1, +1, +1, -1, -1, +1, +1, +1, -1, +1, -1, -1 ; -1, -1, +1, -1, -1, -1, -1, +1, -1, +1, +1, +1, -1, +1, -1, -1]);
    
    % Select the proper spreading function depending on if we are on an odd
    % or even numbered pulse in the sweep
    spread = pcode(parity + 1,:);
    
    ts = linspace(0, length(spread) / baud, ceil(fs * length(spread) / baud));
    carrier = exp(2 * pi * 1.0j * freq * ts);
    
    % Upsample the pulse by sample-and-hold
    [p, q] = rat(fs / baud);
    spread = resample(spread, p, q);
    spread = filter(ones(round(fs / baud), 1), 1, spread);
    
    pulse = spread .* carrier;
end