import numpy as np

class Montecarlo():
    randomArrayX = None
    randomArrayY = None

    hitValuesX = None
    hitValuesY = None

    missValuesX = None
    missValuesY = None

    fMax = None

    result = None

    def __init__(self, funcToAnalyze):
        if not funcToAnalyze or not callable(funcToAnalyze):
            raise ValueError('Parameter is not a function')

        self.__func = funcToAnalyze

    # Function to be analyzed, it will be overwritten by the class' constructor
    # when someone will instantiate a Montecarlo object
    def __func():
        pass

    def __cleanValues(self):
        self.randomArrayX = None
        self.randomArrayY = None


        self.hitValuesX = None
        self.hitValuesY = None

        self.missValuesX = None
        self.missValuesY = None

        self.fMax = None

        self.result = None
    
    def __createFunctionValues(self, lowUpRange, n_samples):
        self.randomArrayX = np.random.uniform(0, 1, n_samples) * (lowUpRange[1] - lowUpRange[0]) + lowUpRange[0]
        try:
            self.randomArrayY = self.__func(self.randomArrayX)
        except ValueError:
            raise ValueError('Error in the function to analyze, the function must work on np.array')
    
    def exportValues(self):
        return {
            'randomArrayX': self.randomArrayX,
            'randomArrayY': self.randomArrayY,

            'hitValuesX': self.hitValuesX,
            'hitValuesY': self.hitValuesY,
            
            'missValuesX': self.missValuesX,
            'missValuesY': self.missValuesY,

            'fMax': self.fMax,

            'result': self.result
        }

    def hitOrMissMonteCarlo(self, lowUpRange, n_samples):
        self.__cleanValues()

        self.__createFunctionValues(lowUpRange, n_samples)

        self.fMax = self.randomArrayY.max()

        possibileHitValuesY = np.random.uniform(0, 1, n_samples) * self.fMax

        self.hitValuesX = self.randomArrayX[possibileHitValuesY < self.randomArrayY]
        self.hitValuesY = possibileHitValuesY[possibileHitValuesY < self.randomArrayY]

        self.missValuesX = self.randomArrayX[possibileHitValuesY > self.randomArrayY]
        self.missValuesY = possibileHitValuesY[possibileHitValuesY > self.randomArrayY]

        self.result = self.fMax * (lowUpRange[1] - lowUpRange[0]) * len(self.hitValuesX) / n_samples

    def averageMonteCarlo(self, lowUpRange, n_samples):
        self.__cleanValues()

        self.__createFunctionValues(lowUpRange, n_samples)

        self.result = self.randomArrayY.sum() / n_samples * (lowUpRange[1] - lowUpRange[0])