class NotImplementedFunctionError(NotImplementedError):
    """
    Exception raised when no function is given to Montecarlo class while
    creating an instance.
    """
    def __init__(self):
        super().__init__('Function has not been implemented.')


class NotCallableException(TypeError):
    """Exception raised when the function passed is not callable."""
    def __init__(self):
        super().__init__('Parameter is not a callable function.')


class NotRunningFunctionError(Exception):
    """Exception raised when an issue occurs while running the function."""
    def __init__(self, error):
        message = f'Error while running the function to be anyalized, \
            error: {error}'
        super().__init__(message)


class FunctionReturnTypeError(TypeError):
    """Exception raised when the return type of the function is not an ndarray."""
    def __init__(self, return_type):
        message = f'Return value of function is {return_type} \
            instead of np.array'

        super().__init__(message)


class FunctionReturnShapeError(ValueError):
    """
    Exception raised when the return value of the function has not the same
    shape of the parameter array.
    """
    def __init__(self, x_shape, y_shape):
        super().__init__(f'The shape of the Y axis (returned by the function) \
            differ from the X axis, shapes are: X({x_shape}), Y({y_shape})')


class InitializedTypeError(TypeError):
    """
    Exception raised when a not boolean value is given to
    is_initialied property.
    """
    def __init__(self, initialized_type):
        message = f'Initialized property must be a boolean \
            not {initialized_type}'

        super().__init__(message)

class NotInitializedError(Exception):
    """
    Exception raised when using a Montecarlo's method without an instance
    of it or with a bad instance.
    """
    def __init__(self):
        super().__init__(
            'A not initialized or bad initialized instance is being used. \
                Please assure that you are using a correctly initialized one'
        )

class CriteriaError(ValueError):
    """
    Exception raised when the wrong criteria is given to the criteria property.
    """
    def __init__(self, criteria, good_criterias):
        super().__init__(
            f'{criteria} is not a valid criteria, \
                choose between {", ".join([c.value for c in good_criterias])}'
        )


class PlotMissingSimulation(ValueError):
    """Exception raised when calling plot without passin a simulation."""
    def __init__(self):
        super().__init__("No simulation has been passed to plot method")