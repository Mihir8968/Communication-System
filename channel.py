import numpy as np
import matplotlib.pyplot as plt
def channel(channel_type, a=1, B_channel=None, td=0, t=None):
    if channel_type == "bandlimited":
        h_t = a*2*B_channel*np.sinc(2*B_channel*t)

    elif channel_type == "distortionless" :
        idx = (np.abs(t - td)).argmin()
        h_t = np.zeros_like(t)
        h_t[idx] = a
    
    else:
        raise ValueError("Unsupported channel type. Use 'bandlimited' or 'distortionless'.")

    return h_t, t