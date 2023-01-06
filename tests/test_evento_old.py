from src.app import validar_evento_old as validar_evento

def test_no_es_dict():
    event1 = ''
    event2 = 2
    event3 = []
    assert validar_evento(event1) == False
    assert validar_evento(event2) == False
    assert validar_evento(event3) == False

def test_sin_filename():
    event = {
        'data': []
    }
    assert validar_evento(event) == False

def test_sin_data():
    event = {
        'filename': ''
    }
    assert validar_evento(event) == False

def test_con_formato_de_vectores_incorrecto():
    event = {
        'data': [{'x':0}],
        'filename': ''
    }
    assert validar_evento(event) == False

def test_data_no_es_array():
    event = {
        'data': 0,
        'filename': ''
    }
    assert validar_evento(event) == False

def test_filename_no_es_string():
    event = {
        'data': [],
        'filename': 1
    }
    assert validar_evento(event) == False

def test_sin_datos_en_data():
    event = {
        'data': [],
        'filename': ''
    }
    assert validar_evento(event) == False

def test_sin_vectores():
    event = {
        'filename': 'nombre',
        'time_start': 'timestamp',
        'data': [
            2,
            3
        ] 
    }
    assert validar_evento(event) == False

def test_con_todo():
    event = {
        'filename': 'nombre',
        'time_start': 'timestamp',
        'data': [
            {
                'time'  : 0.0,
                'acc_x' : 0.0,
                'acc_y' : 0.0,
                'acc_z' : 0.0,
                'gyro_x': 0.0,
                'gyro_y': 0.0,
                'gyro_z': 0.0,
                'temp'  : 0.0
            },
        ] 
    }
    assert validar_evento(event) == True