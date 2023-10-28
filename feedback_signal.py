import numpy as np
import matplotlib.pyplot as plt

# Define the number of samples and initialize a noise array
num_samples = 1000
noise = np.random.randn(num_samples)

alpha = 0.9
feedback = np.zeros_like(noise)
for i in range(1, num_samples):
    feedback[i] = alpha * feedback[i-1] + noise[i]

# Apply FFT
fft_values = np.fft.fft(feedback)

# Apply a simple low-pass filter
cutoff = 50  # Cutoff frequency
fft_values[cutoff:-cutoff] = 0

# Apply Inverse FFT
filtered_signal = np.fft.ifft(fft_values)

plt.figure(figsize=(14, 6))
plt.plot(noise, label='Original Noise', alpha=0.7)
plt.plot(feedback, label='Feedback', alpha=0.7)
plt.plot(filtered_signal, label='Filtered Signal', alpha=0.7)
plt.legend()
plt.show()
