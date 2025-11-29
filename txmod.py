import numpy as np
from scipy.signal import hilbert
from scipy.integrate import cumulative_trapezoid

def txmod(mod_type, m_t, fc, t, sideband="USB", kf=1.0):
    if mod_type == "DSB-SC":
        amplitude = 1
        c_t = amplitude * np.cos(2 * np.pi * fc * t)
        x_t = m_t * c_t
    
    elif mod_type == "AM":
        c_t = np.cos(2 * np.pi * fc * t)
        x_t = (1 + m_t) * c_t

    elif mod_type == "SSB":
        m_hilbert_t = np.imag(hilbert(m_t))
        
        if sideband == "USB":
            x_t = m_t * np.cos(2 * np.pi * fc * t) - m_hilbert_t * np.sin(2 * np.pi * fc * t)
        elif sideband == "LSB":
            x_t = m_t * np.cos(2 * np.pi * fc * t) + m_hilbert_t * np.sin(2 * np.pi * fc * t)
        else:
            raise ValueError("sideband must be 'USB' or 'LSB'")
        
    elif mod_type == "FM":
        integral_m_t = cumulative_trapezoid(m_t, t, initial=0)
        
        phase = 2 * np.pi * fc * t + 2 * np.pi * kf * integral_m_t
        x_t = np.cos(phase)

    elif mod_type == "polar":
        samples_per_bit = int(len(t) / len(m_t))
        x_t = np.repeat([1 if bit == 1 else -1 for bit in m_t], samples_per_bit)


    elif mod_type == "2PAM":
        bits = np.asarray(m_t).astype(int)
        if bits.ndim != 1:
            raise ValueError("m_t for 2PAM should be a 1-D array of bits (0 or 1).")

        levels = 2 * bits - 1 
        N_t = len(t)
        N_sym = len(levels)
        if N_sym == 0:
            raise ValueError("m_t must contain at least one bit for 2PAM.")
        repeats = N_t // N_sym 

        if repeats >= 1:
            x_t = np.repeat(levels, repeats)
        else:
            x_t = levels[:N_t]

        if len(x_t) < N_t:
            pad_len = N_t - len(x_t)
            x_t = np.concatenate([x_t, np.full(pad_len, levels[-1])])
        elif len(x_t) > N_t:
            x_t = x_t[:N_t]

    else:
        raise ValueError("Unsupported modulation type")
    
    return x_t