import numpy as np

def add_awgn(signal, mean=0, variance=1):
    noise = np.random.normal(mean, np.sqrt(variance), size=signal.shape)
    y_t = signal + noise
    return y_t, noise