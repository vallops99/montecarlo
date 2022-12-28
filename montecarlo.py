import numpy as np
import matplotlib.pyplot as plt

from exceptions import (
    CriteriaError, FunctionReturnShapeError, FunctionReturnTypeError, InitializedTypeError, NotCallableException,
    NotImplementedFunctionError, NotInitializedError, NotRunningFunctionError
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
    # Criteria is used to know how to compare two np.ndarray.
    # To have a visual context of criteria usefulness, draw a
    # gaussian function in upper-right quadrant with min_y=0 and max_y=3,
    # when criteria is:
    # minor, hit values are inside the bell, so y < 3
    #   (x is change dynamically based on bell shape);
    # equal, hit values are exactly one of the point of the function;
    # major, hit value are outside the bell, so y > 0
    #   (x is change dynamically based on bell shape).
    # Others can be figured out based on these principles.
    _criteria = 'minor'
 
    # Criteria values is a map of criteria: function pairs.
    _criteria_values = {
        'minor': {
            'function': lambda x, y: x < y,
            'reverse': lambda x, y: x >= y,
        },
        'minor-equal': {
            'function': lambda x, y: x <= y,
            'reverse': lambda x, y: x > y
        },
        'equal': {
            'function': lambda x, y: x == y,
            'reverse': lambda x, y: x != y
        },
        'not-equal': {
            'function': lambda x, y: x != y,
            'reverse': lambda x, y: x == y
        },
        'major-equal': {
            'function': lambda x, y: x >= y,
            'reverse': lambda x, y: x < y
        },
        'major': {
            'function': lambda x, y: x > y,
            'reverse': lambda x, y: x <= y
        }
    }

    # Default criteria is 'minor' as is the most common config.
    def __init__(self, func_to_analyze, criteria='minor'):
        # The function to analyze is assigned to func_to_analyze property.
        # This property has a setter method that evaluate its usability.
        self.func_to_analyze = func_to_analyze
        self.is_initialized = True
        # Criteria has a setter property that checks if the value matches
        # a key in criteria_values map
        self.criteria = criteria

    def _func_to_analyze():
        """Private func_to_analyze mocked to `pass`."""
        pass

    @property
    def is_initialized(self):
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
    def criteria(self):
        return self._criteria
    
    @criteria.setter
    def criteria(self, value):
        if not value in self.criteria_values:
            raise CriteriaError(value, self.criteria_values)
        self._criteria = value

    @property
    def criteria_values(self):
        return self._criteria_values

    @property
    def func_to_analyze(self):
        """
        Function to be analyzed.

        The function must accept a numpy array parameter that represents an
        axis values and return its opposite axis values.
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
        """Test the function before using it in order to handle exceptions."""
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
                raise FunctionReturnShapeError()
        except Exception as error:
            raise NotRunningFunctionError(error)

    # Create random values from uniform probability distribution.
    # Low and high are 0 and 1, the result is multiplied by 
    # (highest - lowest) + lowest in order to have a range [lowest, highest]
    def _create_random_values(self, lowest, highest, n_samples):
        """
        Create n_samples random values of range [lowest, highest]
        from a uniform probability distribution.
        """
        return np.random.uniform(0, 1, n_samples) * (highest - lowest) + lowest

    # Get the random values (X axis) and retrieve the relative Y axis value
    # by feeding the function with our X axis ones.
    def _create_function_values(self, lowest, highest, n_samples):
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
    def hit_or_miss(self, lowest, highest, n_samples):
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
        # for HIT points. Filter will be based on our criteria.
        hit_conditions = self.criteria_values[self.criteria]['function'](
            possibile_hit_values_y,
            random_values_y
        )

        # Get a np.ndarray of true/false value that will filter our values
        # for MISS points. Filter will be based on reverse of our criteria.
        miss_conditions = self.criteria_values[self.criteria]['reverse'](
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
    def average(self, lowest, highest, n_samples):
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
    def plot(simulation):
        """
        Static method that plot a simulation (based on the dictionary that our
        Montecarlo class creates).
    
        Hit or Miss properties:
        - `type`, type of simulation, `hitormiss` in this case;
        - `random_values_x`, np.ndarray of X axis values;
        - `random_values_y`, np.ndarray of Y axis values;
        - `hit_values_x`, np.ndarray of hits of X axis;
        - `hit_values_y`, np.ndarray of hits of Y axis;
        - `miss_values_x`, np.ndarray of miss of X axis;
        - `miss_values_y`, np.ndarray of miss of Y axis;
        - `result`, percentage of success;
        
        Average properties:
        - `type`, type of simulation, `average` in this case;
        - `random_values_x`, np.ndarray of X axis values;
        - `random_values_y`, np.ndarray of Y axis values;
        - `result`, percentage of success;
        """
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
