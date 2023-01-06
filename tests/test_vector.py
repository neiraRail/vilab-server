from src.app import validar_vector

def test_vector_correcto():
    vector = {
        'time_lap': 665903, 
        'node': 1, 
        'event': 4, 
        'acc_x': -0.39, 
        'acc_y': 1.89, 
        'acc_z': -10.41, 
        'gyr_x': 13.17, 
        'gyr_y': -1.13, 
        'gyr_z': -1.33, 
        'mag_x': -150.9, 
        'mag_y': 12.3, 
        'mag_z': -86.1, 
        'temp': 33.94
    }
    assert validar_vector(vector) == True
