import time
import json
import random
import paho.mqtt.client as paho
from dotenv import dotenv_values

config = dotenv_values()

# ----------------------
# Aquí crear los callbacks de MQTT


# ----------------------


if __name__ == "__main__":
    print("GPS Mock: Sensor de posicionamiento gloal")

    # ----------------------
    # Aquí conectarse a MQTT


    # ----------------------
    
    # Datos iniciales
    topico = "sensores/gps"
    data = {"latitude": -34.55, "longitude": -58.498}

    # ----------------------
    # Aquí preparar el blucle para enviar datos

    
    # ----------------------
