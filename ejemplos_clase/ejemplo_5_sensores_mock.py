import time
import json
import random
import paho.mqtt.client as paho
from dotenv import dotenv_values

config = dotenv_values()

# ----------------------
# Aquí crear los callbacks de MQTT
def on_connect_local(client, userdata, flags, rc):
    if rc == 0:
        print("Mqtt Local conectado")

        # Alumno: Suscribirse a los topicos locales deseados

    else:
        print(f"Mqtt Local connection faild, error code={rc}")


def on_connect_remoto(client, userdata, flags, rc):
    if rc == 0:
        print("Mqtt Remoto conectado")
    else:
        print(f"Mqtt Remoto connection faild, error code={rc}")

# Aquí crear el callback on_message
# ----------------------


if __name__ == "__main__":
    print("MQTT Local & Remoto")

    # ----------------------
    # Aquí conectarse a MQTT remoto


    # Aquí conectarse a MQTT local
    client_local = paho.Client("gps_mock_local")
    client_local.on_connect = on_connect_local
    client_local.connect(config["BROKER"], int(config["PORT"]))
    client_local.loop_start()

    # ----------------------
    
    while True:
        pass
    
    # ----------------------

    client.disconnect()
    client.loop_stop()