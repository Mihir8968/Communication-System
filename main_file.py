from plot_time import plot_time
from infosource import infosource
from spectrum_signal import spectrum_signal
from filter_sinc import filter_sinc
from convo_out import convo_out
import matplotlib.pyplot as plt
import numpy as np
from txmod import txmod
from rxdemod import rxdemod
import random
from scipy.io import wavfile
import sounddevice as sd
from adc import adc
from channel import channel
from add_awgn import add_awgn


def main():
#TASK 1
    bitstream = infosource("charname", 0, 0, 0, 0)
    bitstream = [int(b) for b in bitstream.strip() if b in ('0', '1')]



    fc = 1e3
    samples_per_bit = 100
    total_samples = samples_per_bit * len(bitstream)


    t = np.linspace(0, len(bitstream), total_samples, endpoint=False)


    polar_signal = txmod("polar", bitstream, fc, t)


    plt.ion()
    fig, ax = plt.subplots()
    ax.set_ylim(-1.5, 1.5)
    ax.set_xlim(0, total_samples)
    ax.set_xlabel("Time (samples)")
    ax.set_ylabel("Amplitude")
    ax.set_title("Polar Modulated Bit Transmission")

    line, = ax.plot([], [], color='blue')
    waveform = []


    for i, bit in enumerate(bitstream):
        plt.grid(True)
        start = i * samples_per_bit
        end = start + samples_per_bit


        pulse = np.ones(samples_per_bit) if bit == 1 else -np.ones(samples_per_bit)

        waveform.extend(pulse)


        line.set_data(np.arange(len(waveform)), waveform)
        plt.pause(0.05) 

    plt.ioff()
    plt.show()


    tx_signal = txmod("polar", bitstream, fc, t)
    rx_signal, noise = add_awgn(tx_signal, 0, 1)
    reconstructed_name = rxdemod("TH", rx_signal, fc, 1, t, samples_per_bit)
    print(f"Received Name: {reconstructed_name}")






#TASK 2

    constellation = 2 * np.array(bitstream) - 1 
    constellation_complex = constellation + 0j
    # Scatter plot for TX constellation
    plt.figure()
    plt.scatter(np.real(constellation_complex),
                np.imag(constellation_complex),
                color="red")

    plt.title("2-PAM Transmit Constellation")
    plt.xlabel("In-Phase (I)")
    plt.ylabel("Quadrature (Q)")
    plt.grid(True)
    plt.axis('equal')
    plt.show()

    rx_constellation, noise = add_awgn(constellation, 0, 1)
    rx_constellation_complex = rx_constellation + 0j

    plt.figure()
    plt.scatter(np.real(rx_constellation_complex),
                np.imag(rx_constellation_complex),
                color='blue', alpha=0.5, label="RX noisy")

    plt.scatter(np.real(constellation_complex),
                np.imag(constellation_complex),
                color='red', marker='x', s=80, label="TX ideal")

    plt.title("2-PAM Constellation (TX vs RX with AWGN, variance = 1)")
    plt.xlabel("In-Phase (I)")
    plt.ylabel("Quadrature (Q)")
    plt.grid(True)
    plt.legend()
    plt.axis('equal')
    plt.show()




if __name__ == "__main__":
    main()
