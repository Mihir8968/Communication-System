import matplotlib.pyplot as plt
import numpy as np
from filter_sinc import filter_sinc
from convo_out import convo_out
from scipy.signal import convolve
from scipy.signal import hilbert
import matplotlib.pyplot as plt

def rxdemod(demod_type, x_t, fc, fs, t, samples_per_bit=100):
    if demod_type == "SD":
        amplitude = 1
        c_t = amplitude * np.cos(2 * np.pi * fc * t)
        y_t = x_t * c_t
        B = 500
        g_t = filter_sinc(B, fs)
        m_hat_t = convolve(y_t, g_t, mode='same')

    elif demod_type == "ED":
        m_hat_t = np.abs(hilbert(x_t)) - 1

    elif demod_type == "EDFM":
        dt = t[1] - t[0]
        differentiated_x_t = np.diff(x_t) / dt
        differentiated_x_t = np.insert(differentiated_x_t, 0, 0)
        envelope = np.abs(hilbert(differentiated_x_t))
        m_hat_t = envelope - np.mean(envelope)

    elif demod_type == "TH":
        pulse = np.ones(samples_per_bit)
        h_matched = np.flip(pulse)

        mf_output = convo_out(x_t, h_matched)
        plt.plot(x_t)
        plt.title("x_t")
        plt.show()
        plt.plot(h_matched)
        plt.title("h_matched")
        plt.show()
        plt.plot(mf_output)
        plt.title("mf_output")
        plt.show()

        num_bits = int(len(x_t) / samples_per_bit)
        received_bits = []

        for i in range(num_bits):
            start = i * samples_per_bit
            end = start + samples_per_bit
        
            sample = np.mean(mf_output[start:end])
            bit = 1 if sample > 0 else 0
            received_bits.append(bit)

        received_bits_str = ''.join(str(b) for b in received_bits)

        chars = [
            chr(int(received_bits_str[i:i+8], 2))
            for i in range(0, len(received_bits_str), 8)
        ]
        m_hat_t = ''.join(chars)


    else:
        raise ValueError("Unsupported demodulation type")

    return m_hat_t
