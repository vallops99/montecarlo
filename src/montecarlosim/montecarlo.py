from enum import Enum
from typing import Tuple
from collections.abc import Callable

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.markers import MarkerStyle

from .exceptions import (
    CriteriaError, FunctionReturnShapeError, FunctionReturnTypeError,
    InitializedTypeError, NotCallableException, NotImplementedFunctionError,
    NotInitializedError, NotRunningFunctionError, PlotMissingSimulation
)


class Montecarlo():
    """
        Class that helps using the MonteCarlo methods.

        __init__ parameters:
        - `func_to_analyze`, functions that accepts a np.array and return
            a np.array (x to y);
        - `criteria`, (hit or miss only) it indicates how hit/miss values must be read,
            one of: minor, minor-equal, equal, major-equal, major.
    """

    # Flag that let us understand if the Montecarlo's instance in use
    # has been initialized correctly.
    _initialized = False
    _criteria = lambda x, y: (np.full_like(x, True), np.full_like(y, False))

    class CriteriaValue:
        """
        Singleton class that describes how to use criteria.

        It's composed by static method, each of whom accept a `np.ndarray` and
        return a tuple of `np.ndarray`.
        """
        class Criteria(Enum):
            """Enumeration of the possible CriteriaValues method."""
            MINOR = 'minor'
            MINOR_EQUAL = 'minor_equal'
            EQUAL = 'equal'
            NOT_EQUAL = 'not_equal'
            MAJOR_EQUAL = 'major_equal'
            MAJOR = 'major'


        @staticmethod
        def minor(x, y):
            return (x < y, x >= y)

        @staticmethod
        def minor_equal(x, y):
            return (x <= y, x > y)

        @staticmethod        
        def equal(x, y):
            return (x == y, x != y)

        @staticmethod
        def not_equal(x ,y):
            return (x != y, x == y)

        @staticmethod
        def major_equal(x, y):
            return (x >= y, x < y)

        @staticmethod
        def major(x, y):
            return (x > y, x <= y)


    # Default criteria is 'minor' as is the most common config.
    def __init__(self, func_to_analyze: Callable[[np.ndarray], np.ndarray],
        criteria: str = CriteriaValue.Criteria.MINOR.value):
        # The function to analyze is assigned to func_to_analyze property.
        # This property has a setter method that evaluate its usability.
        self.func_to_analyze = func_to_analyze
        self.is_initialized = True
        # Criteria has a setter property that checks if the value matches a key
        # in criteria_values map
        self.criteria = criteria

    @property
    def is_initialized(self) -> bool:
        """
        Initialized property indicates if a class of the instance is in use
        and if it has been initialized correctly.
        """
        return self._initialized

    @is_initialized.setter
    def is_initialized(self, value):
        if not isinstance(value, bool):
            raise InitializedTypeError(type(value))
        self._initialized = value

    @property
    def criteria(
        self) -> Callable[[np.ndarray, np.ndarray], Tuple[np.ndarray, np.ndarray]]:
        """
        Criteria is used to know how to compare two np.ndarray (Xs and Ys) and understand
        which are HIT and which are MISS points, the property stores the
        function to be used (checkout class `CriteriaValues`).

        To have a visual context of criteria usefulness, draw a
        gaussian function with min (0, 0) and max (3, 3),
        when criteria is:
        minor, hit values are inside the bell, so y < 3 and x is
        dynamic but for sure < 6.
        major, hit value are outside the bell, so y > 0 and x is dynamic
        but for sure > 3 where y <= 3 (not for all y).
        Others can be figured out based on these principles.
        """
        return self._criteria

    @criteria.setter
    def criteria(self, value: str = CriteriaValue.Criteria.MINOR.value):
        print(value)
        print(getattr(self.CriteriaValue, value, None))
        if not getattr(self.CriteriaValue, value, None):
            raise CriteriaError(value, self.CriteriaValue.Criteria)
        self._criteria = getattr(self.CriteriaValue, value)

    @property
    def func_to_analyze(self) -> Callable[[np.ndarray], np.ndarray]:
        """
        Function to be analyzed.

        The function must accept a `np.ndarray` parameter that represents an
        axis values and return and `np.ndarray` representing the opposite
        axis values.
        """
        return self._func_to_analyze

    @func_to_analyze.setter
    def func_to_analyze(self, func):
        self._test_function(func)
        self._func_to_analyze = func

    # Private method that tests the function usability
    # Function must: be callable, accept np.ndarray, return np.ndarray and
    # the shape of accepted array and returned array must be the same
    def _test_function(self, func):
        """
        Method that tests a function correctness, throws
        exceptions if not.
        """
        random_array_x = self._create_random_values(0, 1, 10)

        if not func:
            raise NotImplementedFunctionError()

        if not callable(func):
            raise NotCallableException()

        # EAFP (Easier to Ask Forgiveness than Permission)
        try:
            random_array_y = func(random_array_x)
            if not isinstance(random_array_y, np.ndarray):
                raise FunctionReturnTypeError(type(random_array_y))
            if len(random_array_x) != len(random_array_y):
                raise FunctionReturnShapeError(
                    len(random_array_x),
                    len(random_array_y)
                )
        except (FunctionReturnTypeError, FunctionReturnShapeError) as error:
            raise error
        except Exception as error:
            raise NotRunningFunctionError(error)

    # Create random values from uniform probability distribution.
    # Low and high are 0 and 1, the result is multiplied by 
    # (highest - lowest) + lowest in order to have a range [lowest, highest]
    def _create_random_values(self, lowest, highest, n_samples) -> np.ndarray:
        """
        Create n_samples random values of range [lowest, highest]
        from a uniform probability distribution.
        """
        return np.random.uniform(0, 1, n_samples) * (highest - lowest) + lowest

    # Get the random values (X axis) and retrieve the relative Y axis value
    # by feeding the function with our X axis ones.
    def _create_function_values(self,
        lowest, highest, n_samples) -> Tuple[np.ndarray, np.ndarray]:
        """
        Create random X axis values that will be used to create relatives Y
        axis values with the provided function.

        Parameters:
        - `lowest`, minimum val of X (number);
        - `highest`, maximum val of X (number);
        - `n_samples`, quantity of values on X axis (number).
        """
        random_array_x = self._create_random_values(lowest, highest, n_samples)
        random_array_y = self.func_to_analyze(random_array_x)

        return random_array_x, random_array_y

    # Hit or Miss Montecarlo method.
    # We test a bunch on random values (multiplied by Y's max) against 
    # the results of the function to detect hit and miss values.
    # Then we calculate the percentage of success with the following formula:
    # f_max * (highest - lowest) * len(hit_values_x) / n_samples
    # Checkout the criteria_values to understand how hit and miss values
    # are calculated.
    def hit_or_miss(self, lowest, highest, n_samples) -> dict:
        """
        Hit or Miss Montecarlo methods.

        Parameters:
        - `lowest`, minimum val of X (number);
        - `highest`, maximum val of X (number);
        - `n_samples`, quantity of values (number).
        """
        if not self.is_initialized:
            raise NotInitializedError()

        # Generate random X values and calc Y values with our function
        random_values_x, random_values_y = self._create_function_values(
            lowest,
            highest,
            n_samples
        )

        # Get highest value of the np.ndarray
        f_max = random_values_y.max()
        # Generate possible random Y values to test against the created ones
        possibile_hit_values_y = np.random.uniform(0, 1, n_samples) * f_max

        # Get a np.ndarray of true/false value that will filter our values
        # for HIT points and MISS points. Filter will be based on our criteria.
        hit_conditions, miss_conditions = self.criteria(
            possibile_hit_values_y,
            random_values_y
        )

        # Filter random X values by our true/false array and get hits
        hit_values_x = random_values_x[hit_conditions]
        # Filter possibile Y values by our true/false array and get hits
        hit_values_y = possibile_hit_values_y[hit_conditions]

        # Reverse of above to get misses.
        miss_values_x = random_values_x[miss_conditions]
        miss_values_y = possibile_hit_values_y[miss_conditions]

        # Calculate percentage of success
        result = f_max * (highest - lowest) * len(hit_values_x) / n_samples

        # Return all values, will be useful to draw graphs
        return {
            'type': 'hitormiss',

            'random_values_x': random_values_x,
            'random_values_y': random_values_y,

            'hit_values_x': hit_values_x,
            'hit_values_y': hit_values_y,

            'miss_values_x': miss_values_x,
            'miss_values_y': miss_values_y,

            'f_max': f_max,

            'result': result
        }

    # Average Montecarlo method, we basically apply the formula on
    # random X/Y values.
    def average(self,
        lowest: int|float, highest: int|float, n_samples: int) -> dict:
        """
        Average Montecarlo methods.

        Parameters:
        - `lowest`, minimum val of X (number);
        - `highest`, maximum val of X (number);
        - `n_samples`, quantity of values (number).
        """
        if not self.is_initialized:
            raise NotInitializedError()

        random_values_x, random_values_y = self._create_function_values(
            lowest,
            highest,
            n_samples
        )

        # Return all values, will be useful to draw our function
        return {
            'type': 'average',
            'random_values_x': random_values_x,
            'random_values_y': random_values_y,

            'result': random_values_y.sum() / n_samples * (highest - lowest)
        }

    @staticmethod
    def plot(simulation: dict, test: bool = False):
        """
        Plot a simulation.

        Parameters:
        - `simulation`, dictionary returned after running a simulation;
        - `test`, don't show the plot (OPTIONAL)
        """
        if not simulation:
            raise PlotMissingSimulation()

        plt.figure(figsize=(20, 5))

        result = simulation['result']
        plt.title(f'Average Montecarlo, result: {result}')

        plt.scatter(
            simulation['random_values_x'],
            simulation['random_values_y'],
            marker=MarkerStyle('*'),
            label="My function"
        )

        if simulation['type'] == 'hitormiss':
            plt.title(f'Hit or Miss Montecarlo, result: {result}')
            plt.scatter(
                simulation['miss_values_x'],
                simulation['miss_values_y'],
                marker=MarkerStyle('.'),
                label="Miss points"
            )
            plt.scatter(
                simulation['hit_values_x'],
                simulation['hit_values_y'],
                marker=MarkerStyle(','),
                label='Hit points'
            )

        plt.legend()
        if not test:
            plt.show()
