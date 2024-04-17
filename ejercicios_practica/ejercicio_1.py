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
        client.subscribe("actuadores/luces/1")
        client.subscribe("actuadores/volar")

    else:
        print(f"Mqtt Local connection faild, error code={rc}")


def on_connect_remoto(client, userdata, flags, rc):
    if rc == 0:
        print("Mqtt Remoto conectado")
    else:
        print(f"Mqtt Remoto connection faild, error code={rc}")

# Aquí crear el callback on_message
# ----------------------

def on_message(client, userdata, message):
    client_remoto = userdata["client_remoto"]
    topico = message.topic    
    mensaje = str(message.payload.decode("utf-8"))
    topico_remoto = config["DASHBOARD_TOPICO_BASE"] + topico
    client_remoto.publish(topico_remoto, mensaje)
    print(f"mensaje recibido {mensaje} en topico {topico}")

if __name__ == "__main__":
    print("MQTT Local & Remoto")

    # ----------------------
    # Aquí conectarse a MQTT remoto
    random_id = random.randint(1, 999)
    client_remoto = paho.Client(f"Actuadores_remoto_{random_id}")
    client_remoto.on_connect = on_connect_remoto

    # Configurar las credenciales del broker remoto
    client_remoto.username_pw_set(config["DASHBOARD_MQTT_USER"], config["DASHBOARD_MQTT_PASSWORD"])
    client_remoto.connect(config["DASHBOARD_MQTT_BROKER"], int(config["DASHBOARD_MQTT_PORT"]))
    client_remoto.loop_start()

    # Aquí conectarse a MQTT local
    client_local = paho.Client("Actuadores_local")
    client_local.on_connect = on_connect_local
    client_local.connect(config["BROKER"], int(config["PORT"]))
    client_local.on_message = on_message
    client_local.user_data_set({"client_remoto": client_remoto})
    client_local.loop_start()

    # ----------------------
    
    while True:
        pass
    
    # ----------------------

    client.disconnect()
    client.loop_stop()