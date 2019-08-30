fid = fopen('../data/train-000.bin');
FS = 20e6;  % 20 MHz sampling rate
DUR = 10;    % We analyze 10 seconds of data


%+++++++++++++++++++++++++++++++++++++++++++++++++++++++++%
disp("Starting 0-10 seconds");
tic;
iq = fread(fid, FS * DUR * 2, 'int16');
iq = deinterleve(iq);
wf = waterfall(iq, FS, 65536/16);
disp("Converted to waterfall");
fun = @(block_struct) max(max(block_struct.data));
pooled = blockproc(wf, [2 150],fun);
disp("Finished pooling");
save("pool0.mat", 'pooled');
disp("Saved as pool");
toc;
%+++++++++++++++++++++++++++++++++++++++++++++++++++++++++%

%+++++++++++++++++++++++++++++++++++++++++++++++++++++++++%
disp("Starting 10-20 seconds");
tic;
iq = fread(fid, FS * DUR * 2, 'int16');
iq = deinterleve(iq);
wf = waterfall(iq, FS, 65536/16);
disp("Converted to waterfall");
fun = @(block_struct) max(max(block_struct.data));
pooled = blockproc(wf, [2 150],fun);
disp("Finished pooling");
save("pool1.mat", 'pooled');
disp("Saved as pool");
toc;
%+++++++++++++++++++++++++++++++++++++++++++++++++++++++++%


fclose(fid);