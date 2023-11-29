from collections import deque
import numpy as np
from src.procesado.baseProceso import BaseProceso


class LiveLFilter(BaseProceso):
    def __init__(self, b, a):
        """Inicializa un livefilter basado en los parametros a y b.

        Args:
            b (array-like): numerator coefficients obtained from scipy.
            a (array-like): denominator coefficients obtained from scipy.
        """
        self.b = b
        self.a = a
        self._xs = deque([0] * len(b), maxlen=len(b))
        self._ys = deque([0] * (len(a) - 1), maxlen=len(a)-1)
        
    def _process(self, x):
        """Filter incoming data with standard difference equations.
        """
        self._xs.appendleft(x)
        y = np.dot(self.b, self._xs) - np.dot(self.a[1:], self._ys)
        y = y / self.a[0]
        self._ys.appendleft(y)

        return y
    

import scipy
#definir el filtro, un filtro está definido por 2 coeficientes que pueden ser vectores
b, a = scipy.signal.iirfilter(4, Wn=2.5, fs=30, btype="low", ftype="butter")
lowPassFilter = LiveLFilter(b,a)

b,a = scipy.signal.iirfilter(4, Wn=2.5, fs=30, btype="high", ftype="butter")
highPassFilter = LiveLFilter(b,a)