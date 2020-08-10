# Ruiqi Chen
# August 9, 2020

import matplotlib.pyplot as plt
import numpy as np

def plot_scalability():
    num_cores = np.array([1, 2, 4, 8, 16])
    timing = np.array([68.481, 41.116, 27.811, 21.834, 19.619])
    speedup = timing[0] / timing
    # Plot theoretical Amdahl's law
    # T = (1-p)*T0 + p/s*T0
    s = np.linspace(1, 16, 50)
    p = 0.76  # from timing data
    t = (1 - p)*timing[0] + p/s*timing[0]
    speedup_theory = 1/((1 - p) + p/s)
    fig = plt.figure(figsize=(12, 4))
    ax = fig.add_subplot(121)
    ax.plot(num_cores, timing, '-o')
    ax.plot(s, t, '--k')
    ax.set_xlabel('Number of cores')
    ax.set_ylabel('Wall time (s)')
    ax.legend(['Data', "Amdahl's Law (p=0.76)"])
    ax = fig.add_subplot(122)
    ax.plot(num_cores, speedup, '-o')
    ax.plot(s, speedup_theory, '--k')
    ax.set_xlabel('Number of cores')
    ax.set_ylabel('Speed up')
    ax.legend(['Data', "Amdahl's Law (p=0.76)"])
    plt.savefig('benchmarking/30_day_benchmark_scalability.png')

def main():
    plot_scalability()

if __name__ == '__main__':
    main()