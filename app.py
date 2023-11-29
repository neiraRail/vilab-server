import socket, threading
import logging
from flask import Flask
from flask_cors import CORS
from src.database import db as mongo
from src.lecturas import bp as events_blueprint
from src.nodes import bp as nodes_blueprint

# import paho.mqtt.client as mqtt
from src.lecturas import recieve_lectura_udp
# from src.lecturas import recieve_lectura_tcp
# from src.lecturas import recieve_lectura_mqtt

logging.basicConfig(
    filename="logs/vilab_server.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s: %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S",
)

# Crear app con CORS y configuración de base de datos.
app = Flask(__name__)
CORS(app)
app.config["MONGODB_SETTINGS"] = {
    "db": "vibration_db",
    "host": "mongodb",
    "port": 27017,
}

# Registrar los endpoints
app.register_blueprint(events_blueprint, url_prefix="/lectura")
app.register_blueprint(nodes_blueprint, url_prefix="/nodes")

# Iniciar la conexión con la base de datos.
mongo.init_app(app)


@app.route("/status")
def status():
    logging.info("GET status/ request")
    return {"estado": "1", "texto": "OK"}


def udp_server():
    print("udp server")
    UDP_IP = "0.0.0.0"
    UDP_PORT = 8080
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        print("object sock created")
        sock.bind((UDP_IP, UDP_PORT))
        print(f"UDP server listening on {UDP_IP}:{UDP_PORT}")
        recieve_lectura_udp(sock)

# def tcp_server():
#     print("tcp server")
#     TCP_IP = "0.0.0.0"
#     TCP_PORT = 8079
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
#         sock.bind((TCP_IP, TCP_PORT))
#         sock.listen()
#         print(f"UDP server listening on {TCP_IP}:{TCP_PORT}")
#         conn, addr = sock.accept()
#         with conn:
#             recieve_lectura_tcp(conn, addr)


# def mqtt_server():
#     print("mqtt server")
#     client = mqtt.client()
#     def on_connect(client, userdata, flags, rc):
#         client.subscribe("lab/#")
    
#     def on_message(client, userdata, msg):
#         recieve_lectura_mqtt(client, userdata, msg)

#     client.on_connect = on_connect
#     client.on_message = on_message

#     client.connect("localhost", 1883, 60)
#     client.loop_forever()


if __name__ == "__main__":
    logging.info("Servidor funcionando")
    udp_thread = threading.Thread(target=udp_server)
    udp_thread.daemon = True
    udp_thread.start()

    # tcp_thread = threading.Thread(target=tcp_server)
    # tcp_thread.daemon = True
    # tcp_thread.start()

    # mqtt_thread = threading.Thread(target=mqtt_server)
    # mqtt_thread.daemon = True
    # mqtt_thread.start()

    app.run(host="0.0.0.0", port=8080, debug=False)
    logging.info("Servidor finalizado")
