function [pulse] = pulsegen(freq, fs, baud, parity)
    persistent pcode;
    pcode = fliplr([+1, +1, -1, +1, +1, +1, +1, -1, -1, +1, +1, +1, -1, +1, -1, -1 ; -1, -1, +1, -1, -1, -1, -1, +1, -1, +1, +1, +1, -1, +1, -1, -1]);
    
    % Select the proper spreading function depending on if we are on an odd
    % or even numbered pulse in the sweep
    spread = pcode(parity + 1,:);
    
    ts = linspace(0, length(spread) / baud, fs * length(spread) / baud);
    carrier = exp(2 * pi * 1.0j * freq * ts);
    
    % Upsample the pulse by sample-and-hold
    spread = upsample(spread, fs / baud);
    spread = filter(ones(fs / baud, 1), 1, spread);
    
    pulse = spread .* carrier;
end