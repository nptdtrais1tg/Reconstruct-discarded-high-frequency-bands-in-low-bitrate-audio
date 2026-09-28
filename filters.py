import numpy as np
from scipy.signal import butter, lfilter

def low_pass_filter(data, cutoff, fs, order=8):
    """ Apply the Butterworth LPF filter to simulate low-quality audio."""
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = lfilter(b, a, data)
    
    return y