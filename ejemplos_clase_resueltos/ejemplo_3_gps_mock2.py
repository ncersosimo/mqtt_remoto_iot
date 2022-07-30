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
    data = {"latitude": -34.54, "longitude": -58.49}
    destino = {"latitude": -31.41, "longitude": -64.18}


    topico = "dashboardiot/origen/" + "sensores/gps"
    data_jsonstr = json.dumps(data)
    ret = client.publish(topico, data_jsonstr)
    topico = "dashboardiot/destino/" + "sensores/gps"
    data_jsonstr = json.dumps(destino)
    ret = client.publish(topico, data_jsonstr)
    topico = "dashboardiot/hcontigiani/" + "sensores/gps"
    # ----------------------
    # Aquí preparar el blucle para enviar datos
    # for i in range(4):
    #     data["longitude"] += .0001
    #     data_jsonstr = json.dumps(data)
    #     ret = client.publish(topico, data_jsonstr) 
    #     time.sleep(.1)
    
    while data != destino:
        if data['latitude'] != destino['latitude']:
            if data['latitude'] > destino['latitude']:
                data['latitude'] -= .01
            else:
                data['latitude'] += .01
        if data['longitude'] != destino['longitude']:
            if data['longitude'] > destino['longitude']:
                data['longitude'] -= .01
            else:
                data['longitude'] += .01
        data_jsonstr = json.dumps(data)
        ret = client.publish(topico, data_jsonstr) 
        time.sleep(.05)
        
    # ----------------------

    client.disconnect()
    client.loop_stop()