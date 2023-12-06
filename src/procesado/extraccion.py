from src.procesado.baseProceso import BaseProceso
import numpy as np
from scipy.stats import skew
from scipy.stats import kurtosis as kurt

keys = ["acc_x", "acc_y", "acc_z", "gyr_x", "gyr_y", "gyr_z", "mag_x", "mag_y", "mag_z"]
# Implement time domain features
class PeakValue(BaseProceso):
    def _process(self, batch):
        return {key: np.max([item[key] for item in batch]) for key in keys}
    
class Mean(BaseProceso):
    def _process(self, batch):
        import numpy as np
        return {key: np.mean([item[key] for item in batch]) for key in keys}
    
class StandardDeviation(BaseProceso):
    def _process(self, batch):
        return {key: np.std([item[key] for item in batch]) for key in keys}
    
class RootMeanSquare(BaseProceso):
    def _process(self, batch):
        return {key: np.sqrt(np.mean([item[key]**2 for item in batch])) for key in keys}
    
class Skewness(BaseProceso):
    def _process(self, batch):
        return {key: skew([item[key] for item in batch]) for key in keys}

class Kurtosis(BaseProceso):
    def _process(self, batch):
        return {key: kurt([item[key] for item in batch]) for key in keys}

class CrestFactor(BaseProceso):
    def _process(self, batch):
        return {key: np.max([item[key] for item in batch]) / skew([item[key] for item in batch]) for key in keys}

peakValue = PeakValue()
mean = Mean()
standardDeviation = StandardDeviation()
rootMeanSquare = RootMeanSquare()
skewness = Skewness()
kurtosis = Kurtosis()
crestFactor = CrestFactor()


# Implement frequency domain features

# Implement time-frequency domain features