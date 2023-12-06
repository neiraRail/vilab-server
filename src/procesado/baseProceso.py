import logging
import numpy as np


class BaseProceso:
    """
    Base class for live filters.
    """

    def process(self, x):
        # do not process NaNs
        if len(x) == 0:
            return x

        return self._process(x)

    def __call__(self, x):
        return self.process(x)

    def _process(self, x):
        raise NotImplementedError("Derived class must implement _process")


from src.procesado import filtrado
from src.procesado import extraccion

subtipo2class = {
    "lowpass": filtrado.lowPassFilter,
    "highpass": filtrado.highPassFilter,
    "peakvalue": extraccion.peakValue,
    "mean": extraccion.mean,
    "standarddeviation": extraccion.standardDeviation,
    "rootmeansquare": extraccion.rootMeanSquare,
    "skewness": extraccion.skewness,
    "kurtosis": extraccion.kurtosis,
    "crestfactor": extraccion.crestFactor,
}

from src.models.node import Node


def getConfig(node_id):
    node = Node.objects(node=node_id).first()
    return node["operaciones"]


def procesar_segun_config(identifier):
    config = getConfig(identifier["node"])
    batch = identifier["batch"]
    for operacion in config:
        if operacion.tipo == "filtrado":
            vector = subtipo2class[operacion.subtipo](batch)
            # Guardar vector
        else:
            res = subtipo2class[operacion.subtipo](batch)
            res["node"] = identifier["node"]
            res["start"] = identifier["start"]
            res["batch_id"] = identifier["batch_id"]
            logging.info("{}: {}".format(operacion["subtipo"], res))
            # Guardar res
