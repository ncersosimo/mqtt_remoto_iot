import time
import json
import random
import paho.mqtt.client as paho
from dotenv import dotenv_values

config = dotenv_values()

THRESHOLD_INICIO = 3
THRESHOLD_FIN = 10

ESTADO_INICIO = 0
ESTADO_PRESENCIA_FLANCO = 1
ESTADO_FLANCO_CONFIRMADO = 2

# ----------------------
# Aquí crear los callbacks de MQTT
def on_connect_local(client, userdata, flags, rc):
    if rc == 0:
        print("Mqtt Local conectado")

        # Alumno: Suscribirse a los topicos locales deseados
        client.subscribe("sensores/gps")
        client.subscribe("sensores/inerciales")
    else:
        print(f"Mqtt Local connection faild, error code={rc}")


def on_connect_remoto(client, userdata, flags, rc):
    if rc == 0:
        print("Mqtt Remoto conectado")
    else:
        print(f"Mqtt Remoto connection faild, error code={rc}")

# Aquí crear el callback on_message
def on_message(client, userdata, message):
    client_remoto = userdata["client_remoto"]
    estado_sistema = userdata["estado_sistema"]
    topico = message.topic
    mensaje = str(message.payload.decode("utf-8"))

    topico_remoto = config["DASHBOARD_TOPICO_BASE"] + topico
    client_remoto.publish(topico_remoto, mensaje)

    # Consultar si el tópico es de los sensores inerciales
    if topico == "sensores/inerciales":
        data = json.loads(mensaje)
        accel = float(data["accel"])
        print(f"Accel {accel}")

        # Máquina de estados
        if estado_sistema == ESTADO_INICIO:
            if accel > THRESHOLD_INICIO:
                # Se ha detectado una aceleración
                # mayor al threshold de inicio, se pasa
                # al estado "en presencia de posible flanco"
                estado_sistema = ESTADO_PRESENCIA_FLANCO
                print(f"ESTADO_PRESENCIA_FLANCO {accel}")

        elif estado_sistema == ESTADO_PRESENCIA_FLANCO:
            if accel < THRESHOLD_INICIO:
                # La aceleración a disminuido,
                # se pasa al estado de inicio
                estado_sistema = ESTADO_INICIO
                print(f"ESTADO_INICIO {accel}")

            elif accel > THRESHOLD_FIN:
                # Se ha detectado una aceleración
                # mayor al threshold de fin de flanco, se pasa
                # al estado "flanco confirmado" y se prende la luz
                estado_sistema = ESTADO_FLANCO_CONFIRMADO

                topico = "actuadores/luces/1"
                topico_remoto = config["DASHBOARD_TOPICO_BASE"] + topico
                client.publish(topico, "1")
                client_remoto.publish(topico_remoto, "1")
                print(f"THRESHOLD_FIN {accel}")

        elif estado_sistema == ESTADO_FLANCO_CONFIRMADO:
            # Se espera a que la aceleración disminuya
            # y se termine el flanco ascendente
            if accel < THRESHOLD_INICIO:
                # La aceleración a disminuido,
                # se pasa al estado de inicio
                estado_sistema = ESTADO_INICIO
                print(f"ESTADO_INICIO {accel}")
            
        # Almacenar el nuevo valor de estado
        userdata["estado_sistema"] = estado_sistema

# ----------------------


if __name__ == "__main__":
    print("GPS Mock: Sensor de posicionamiento gloal")
    estado_sistema = ESTADO_INICIO

    # ----------------------
    # Aquí conectarse a MQTT remoto
    random_id = random.randint(1, 999)
    client_remoto = paho.Client(f"gps_mock_remoto_{random_id}")
    client_remoto.on_connect = on_connect_remoto
    # Configurar las credenciales del broker remoto
    client_remoto.username_pw_set(config["DASHBOARD_MQTT_USER"], config["DASHBOARD_MQTT_PASSWORD"])
    client_remoto.connect(config["DASHBOARD_MQTT_BROKER"], int(config["DASHBOARD_MQTT_PORT"]))
    client_remoto.loop_start()


    # Aquí conectarse a MQTT local
    client_local = paho.Client("gps_mock_local")
    client_local.on_connect = on_connect_local
    client_local.on_message = on_message
    client_local.user_data_set( {"client_remoto": client_remoto, "estado_sistema": estado_sistema})

    client_local.connect(config["BROKER"], int(config["PORT"]))
    client_local.loop_start()

    # ----------------------
    while True:
        pass
    
    # ----------------------

    client.disconnect()
    client.loop_stop()