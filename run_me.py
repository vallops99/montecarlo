import numpy as np

from montecarlo import Montecarlo

# Function that will be used to run the simulation.
# Undefined integral
# e to the power of -(x to the power of 2) / 2
def gauss(x):
    return np.exp(-np.power(x, 2)/2)

def main():
    # Instantiate our Montecarlo by passing our function
    # and the criteria to use in case of hitormiss simulation
    simulation = Montecarlo(gauss, criteria='minor')
    # Run hitormiss simulation
    hit_or_miss = simulation.hit_or_miss(-10, 10, 1000)
    # Run average simulation
    average = simulation.average(-3, 3, 1000)

    # Plot our results
    Montecarlo.plot(hit_or_miss)
    Montecarlo.plot(average)


if __name__ == "__main__":
    main()