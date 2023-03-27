from src.nodes import validar_nodo


def test_nodo_correcto():
    nodo = {
        "ssid": "DRAGINO_IOT",
        "password": "Jota.2020",
        "serverREST": "http://200.13.5.47:8080/eventos",
        "node": 2,
        "time_event": 2500,
        "delay_sensor": 200,
        "time_reset": 24,
        "token": "108160136",
    }
    assert validar_nodo(nodo) == {"valido": True, "razon": None}