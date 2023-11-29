import numpy as np

class BaseProceso:
    """
    Base class for live filters.
    """
    def process(self, x):
        # do not process NaNs
        if np.isnan(x):
            return x

        return self._process(x)

    def __call__(self, x):
        return self.process(x)

    def _process(self, x):
        raise NotImplementedError("Derived class must implement _process")


from src.procesado import filtrado

subtipo2class = {
    "lowpass": filtrado.lowPassFilter,
    "highpass": filtrado.highPassFilter,
}

from src.models.node import Node
def getConfig(node_id):
    node = Node.objects(node=node_id).first()
    return node.proccess_config

def procesar_segun_config(vector):
    config = getConfig(vector.node)
    for operacion in config:
        if operacion.tipo == "filtrado":
            vector = subtipo2class[operacion.subtipo](vector)
            #Guardar vector
        else:
            res = subtipo2class[operacion.subtipo](vector)
            #Guardar res