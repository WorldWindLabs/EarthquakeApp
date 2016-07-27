function freqtest(x,y,z, filename)
%%code to produce a plot for the frequency response of data previously
%stored in x,y,z variables.

%for the x data
Fs = 60;    %sampling frequency
NFFT = length(x);
X = fft(x,NFFT);
F = ((0:1/NFFT:1-1/NFFT)*Fs).';
Xmag = abs(X);        % Magnitude of the FFT
Xangle = unwrap(angle(X));  % Phase of the FFT



scrsz = get(groot,'ScreenSize');
figure('Name',strcat(filename,' plot'),'NumberTitle','off', 'OuterPosition',scrsz)  %creates a full screen figure with the name of the csv file
subplot(2,3,1)
plot(F(1:NFFT/2),20*log10(Xmag(1:NFFT/2)));
title('Magnitude response of the x data')
xlabel('Frequency in Hz')
ylabel('dB')
grid on;
axis tight 
xlim([0,10])


subplot(2,3,4)
plot(F(1:NFFT/2),Xangle(1:NFFT/2));
title('Phase response of the x data')
xlabel('Frequency in Hz')
ylabel('radians')
grid on;
axis tight
xlim([0,10])

%for the y data
Fs = 60;
NFFT = length(y);
Y = fft(y,NFFT);
F = ((0:1/NFFT:1-1/NFFT)*Fs).';
Ymag = abs(Y);        % Magnitude of the FFT
Yangle = unwrap(angle(Y));  % Phase of the FFT


subplot(2,3,2)
plot(F(1:NFFT/2),20*log10(Ymag(1:NFFT/2)));
title('Magnitude response of the y data')
xlabel('Frequency in Hz')
ylabel('dB')
grid on;
axis tight 
xlim([0,10])

subplot(2,3,5)
plot(F(1:NFFT/2),Yangle(1:NFFT/2));
title('Phase response of the y data')
xlabel('Frequency in Hz')
ylabel('radians')
grid on;
axis tight
xlim([0,10])

%for the z data
Fs = 60;
NFFT = length(z);
Z = fft(z,NFFT);
F = ((0:1/NFFT:1-1/NFFT)*Fs).';
Zmag = abs(Z);        % Magnitude of the FFT
Zangle = unwrap(angle(Z));  % Phase of the FFT


subplot(2,3,3)
plot(F(1:NFFT/2),20*log10(Zmag(1:NFFT/2)));
title('Magnitude response of the z data')
xlabel('Frequency in Hz')
ylabel('dB')
grid on;
axis tight 
xlim([0,10])


subplot(2,3,6)
plot(F(1:NFFT/2),Zangle(1:NFFT/2));
title('Phase response of the z data')
xlabel('Frequency in Hz')
ylabel('radians')
grid on;
axis tight
xlim([0,10])


end