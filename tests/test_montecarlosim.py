import numpy as np

from montecarlosim.functions import gauss
from montecarlosim.montecarlo import Montecarlo
from montecarlosim.exceptions import (
    CriteriaError, NotInitializedError, InitializedTypeError,
    NotCallableException, NotRunningFunctionError, FunctionReturnTypeError,
    FunctionReturnShapeError, NotImplementedFunctionError,
    PlotMissingSimulation
)

class TestSuite():
    min_value = -2
    max_value = 3
    n_samples = 100

    def test_instance_success(self):
        sim = Montecarlo(gauss)
        assert isinstance(sim, Montecarlo)
        assert sim.is_initialized == True

    def test_is_initialized_type_error(self):
        sim = Montecarlo(gauss)
        try:
            sim.is_initialized = 'return error'
        except Exception as err:
            assert isinstance(err, InitializedTypeError)

    def test_instance_function_none(self):
        try:
            Montecarlo(None) # type: ignore
        except Exception as err:
            assert isinstance(err, NotImplementedFunctionError)
    
    def test_instance_function_not_callable(self):
        try:
            Montecarlo('string') # type: ignore
        except Exception as err:
            assert isinstance(err, NotCallableException)
    
    def test_instance_function_no_param(self):
        try:
            Montecarlo(lambda: 1) # type: ignore
        except Exception as err:
            assert isinstance(err, NotRunningFunctionError)

    def test_instance_function_return_error(self):
        try:
            Montecarlo(lambda x: 'string') # type: ignore
        except Exception as err:
            assert isinstance(err, FunctionReturnTypeError)

    def test_instance_function_diff_shape(self):
        try:
            Montecarlo(lambda x: np.array([1, 2]))
        except Exception as err:
            assert isinstance(err, FunctionReturnShapeError)

    def test_instance_criteria_error(self):
        try:
            Montecarlo(gauss, 'not-good')
        except Exception as err:
            assert isinstance(err, CriteriaError)

    def test_create_random_values(self):
        np_array = Montecarlo(gauss)._create_random_values(
            self.min_value,
            self.max_value,
            self.n_samples
        )

        assert len(np_array) == self.n_samples

        is_min_ok = True
        is_max_ok = True
        for value in np_array:
            if value < self.min_value:
                is_min_ok = False
                break
            if value > self.max_value:
                is_max_ok = False
                break

        assert is_min_ok == True
        assert is_max_ok == True

    def test_hit_or_miss_not_initialized(self):
        try:
            sim = Montecarlo(gauss)
            sim.is_initialized = False
            sim.hit_or_miss(
                self.min_value,
                self.max_value,
                self.n_samples
            )
        except Exception as err:
            assert isinstance(err, NotInitializedError)

    def test_average_not_initialized(self):
        try:
            sim = Montecarlo(gauss)
            sim.is_initialized = False
            sim.average(
                self.min_value,
                self.max_value,
                self.n_samples
            )
        except Exception as err:
            print(type(err))
            assert isinstance(err, NotInitializedError)

    def test_hit_or_miss_success(self):
        sim = Montecarlo(gauss).hit_or_miss(
            self.min_value,
            self.max_value,
            self.n_samples
        )

        assert 'type' in sim
        assert 'f_max' in sim
        assert 'result' in sim
        assert 'hit_values_x' in sim
        assert 'hit_values_y' in sim
        assert 'miss_values_x' in sim
        assert 'miss_values_y' in sim
        assert 'random_values_x' in sim
        assert 'random_values_y' in sim

        assert sim['type'] == 'hitormiss'

        assert len(sim['random_values_x']) == self.n_samples
        assert len(sim['random_values_y']) == self.n_samples

        assert len(sim['hit_values_x']) + len(
            sim['miss_values_x']) == self.n_samples
        assert len(sim['hit_values_y']) + len(
            sim['miss_values_y']) == self.n_samples

        assert isinstance(sim['f_max'], np.floating)

    def test_average_success(self):
        sim = Montecarlo(gauss).average(
            self.min_value,
            self.max_value,
            self.n_samples
        )

        assert 'type' in sim
        assert 'result' in sim
        assert 'random_values_x' in sim
        assert 'random_values_y' in sim

        assert sim['type'] == 'average'

        assert len(sim['random_values_x']) == self.n_samples
        assert len(sim['random_values_y']) == self.n_samples

    def test_plot(self):
        sim = Montecarlo(gauss)
        Montecarlo.plot(sim.hit_or_miss(-3, 3, 500), True)

    def test_plot_no_simulation_error(self):
        try:
            Montecarlo.plot({}, True)
        except Exception as err:
            assert isinstance(err, PlotMissingSimulation)