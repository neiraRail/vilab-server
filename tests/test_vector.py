from src.app import validar_vector

def test_vector_vacio():
    assert validar_vector({}) == False

def test_vector_sin_atributos_necesarios():
    vector = {
        'hola':1
    }
    assert validar_vector(vector) == False

def test_vector_sin_tipos_correctos():
    vector = {
        'time'  : 'hola',
        'acc_x' : 1,
        'acc_y' : 1,
        'acc_z' : 1,
        'gyro_x': 1,
        'gyro_y': 1,
        'gyro_z': 1,
        'temp'  : 1
    }
    assert validar_vector(vector) == False

