import numpy as np
import matplotlib.pyplot as plt
import random

def infosource(signal_type,f,fs,amp,T):
    """Generate a signal based on `signal_type` ('sine' or 'sinc').
    Returns only the time-domain signal m_t.
    """
    if signal_type == "sine":
        start_time = 0
        stop_time = 1
        t = np.linspace((start_time+T), (stop_time+T), int(fs * (stop_time - start_time)) + 1)
        m_t = amp * np.sin(2 * np.pi * f * t)
             

    elif signal_type == 'multitone': 
        f_1=f
        f_2 = 2 * f_1
        f_max = max(f_1, f_2)
        fs = 10 * f_max
        start_time = 0
        stop_time = 1
        A_1 = 1
        A_2 = 1
        t = np.linspace(start_time+T, stop_time+T, int(fs * (stop_time - start_time)) + 1)

        m_t = A_1 * np.sin(2 * np.pi * f_1 * t) + A_2 * np.sin(2 * np.pi * f_2 * t)
       
    elif signal_type == "sinc":
        
        start_time = -10
        stop_time = 10
        t = np.linspace(start_time+T, stop_time+T, int(fs * (stop_time - start_time)) + 1)
        m_t =  2 * f * np.sinc(2 * f* (t-T))

    elif signal_type == "dial_tone":
        
        start_time = 0
        stop_time = 1
        t = np.linspace(start_time+T, stop_time+T, int(fs * (stop_time - start_time)) + 1)
        amp_tone=0.1
        f1=350
        f2=440
        m_t =  (amp_tone/2)*np.sin(2*np.pi*f1*t) + (amp_tone/2)*np.sin(2*np.pi*f2*t)
        

    elif signal_type == "real_time_song":
        # Write your code to extract samples from .wav
        start_time = 0
        stop_time = 1
        fm = 10  # Maximum frequency component in Hertz for the given spectrum
        fs = 10 * fm
        ts = 1 / fs
               
        t = np.arange(start_time+T, stop_time+T, ts)
        U = random.randint(1, 5)
        m_t = U * np.cos(2 * np.pi * fm * t)

    elif signal_type == "charname":
        text = "Commsys is fun,"
        bits = ''.join(format(ord(char), '08b') for char in text)
        return bits


    else:
        raise ValueError("Unsupported signal type: choose 'sine' or 'sinc'.")

    return m_t, t