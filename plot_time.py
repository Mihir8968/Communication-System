import matplotlib.pyplot as plt


def plot_time(t, m_t, title="Add title", fig_num=1):
    plt.figure(fig_num)
    plt.plot(t, m_t)
    plt.title(title)
    plt.xlabel("Time")
    plt.ylabel("Signal Amplitude")
    plt.grid(True)  
    plt.show()