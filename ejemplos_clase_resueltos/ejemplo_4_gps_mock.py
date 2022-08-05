import time
import json
import random
import paho.mqtt.client as paho
from dotenv import dotenv_values

config = dotenv_values()

# ----------------------
# Aquí crear los callbacks de MQTT
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Mqtt Local conectado")
    else:
        print(f"Mqtt Local connection faild, error code={rc}")

# ----------------------


if __name__ == "__main__":
    print("GPS Mock: Sensor de posicionamiento gloal")

    # ----------------------
    # Aquí conectarse a MQTT
    random_id = random.randint(1, 999)
    client = paho.Client(f"gps_mock_remoto_{random_id}")
    client.on_connect = on_connect
    # Configurar las credenciales del broker remoto
    client.username_pw_set(config["DASHBOARD_MQTT_USER"], config["DASHBOARD_MQTT_PASSWORD"])
    client.connect(config["DASHBOARD_MQTT_BROKER"], int(config["DASHBOARD_MQTT_PORT"]))
    client.loop_start()
    # ----------------------
    
    # Datos iniciales
    topico = "dashboardiot/<usuario_campus>/" + "sensores/gps"
    data = {"latitude": -34.55, "longitude": -58.498}

    # ----------------------
    # Aquí preparar el blucle para enviar datos
    for i in range(4000):
        data["longitude"] += .0001
        data_jsonstr = json.dumps(data)
        ret = client.publish(topico, data_jsonstr) 
        time.sleep(.1)
    
    # ----------------------

    client.disconnect()
    client.loop_stop()