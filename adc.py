import numpy as np

def adc(type, m_t,fs,N,v_ref):
    if type == "PCM" :
        L = 2**N
        m_norm = (m_t + v_ref/2) * (L - 1) / v_ref  
        m_quant = np.round(m_norm).astype(int)
        m_quant = np.clip(m_quant, 0, L - 1)
        bit_stream = [format(sample, f'0{N}b') for sample in m_quant]


    elif type == "DM":
        pass


    
    return bit_stream