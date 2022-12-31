import numpy as np
import matplotlib.pyplot as plt

from montecarlo import Montecarlo

# Function that will be used to run the simulation.
# Undefined integral
# e to the power of -(x to the power of 2) / 2
def gauss(x):
    return np.exp(-np.power(x, 2)/2)

# Function that plots the simulation results
def plot(simulation):
    plt.figure(figsize=(20, 5))

    result = simulation['result']
    plt.title(f'Average Montecarlo, result: {result}')

    plt.scatter(
        simulation['random_values_x'],
        simulation['random_values_y'],
        marker="*",
        label="My function"
    )

    if simulation['type'] == 'hitormiss':
        plt.title(f'Hit or Miss Montecarlo, result: {result}')
        plt.scatter(
            simulation['miss_values_x'],
            simulation['miss_values_y'],
            marker="*",
            label="Miss points"
        )
        plt.scatter(
            simulation['hit_values_x'],
            simulation['hit_values_y'],
            marker="*",
            label='Hit points'
        )

    plt.legend()
    plt.show()

def main():
    # Instantiate our Montecarlo by passing our function
    # and the criteria to use in case of hitormiss simulation
    simulation = Montecarlo(gauss, criteria='minor')
    # Run hitormiss simulation
    hit_or_miss = simulation.hit_or_miss(-10, 10, 1000)
    # Run average simulation
    average = simulation.average(-3, 3, 1000)

    # Plot our results
    plot(hit_or_miss)
    plot(average)


if __name__ == "__main__":
    main()