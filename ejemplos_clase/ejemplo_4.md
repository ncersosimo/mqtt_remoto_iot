# Ejemplos de clase

En esta práctica utilizaremos el simulador de drone "sensores_mock" junto a la librería de Paho MQTT

Logearse desde VM y obtener cual es la dirección IP del dispositivo:
```sh
$ ifconfig
```

### 1 - Preparar el entorno de trabajo

Abrir el Visual Studio Code y conectarse de forma remota al dispositivo. Trabajaremos sobre la carpeta recientemente clonada de este repositorio.

Clonar el repositorio del simulador de sensores:
```sh
$ git clone https://github.com/InoveAlumnos/sensores_mock_iot
```

Topicos que soporta este mock drone emulado:
|             |             | datos ejemplo
| ----------  | --------    | -----
|  sensores   | gps         | {"latitude": -34.55, "longitude": -58.496}
|  sensores   | inericiales | {"heading": 160, accel: 4.5}


### 2 - Lanzar el simulador sensores mock
Desde ssh conectado a la VM, ingresar a la carpeta clonada del "sensores_mock_iot" y lanzar la aplicación:
```sh
$ python3 app.py
```

Ingresar a su explorador web e ingresar a al aplicación del drone:
```
http://<ip_VM>:5008
```

### 3 - Ensayar que el simulador funcione
Utilizar el MQTTExplorar y verificar de esta manera el correcto funcionamiento de cada sensor disponible. 


### 4 - Script capturador de sensores
Tome el script "ejemplo_4_sensores_mock.py" el cual viene con la conectividad a MQTT resuelta. Observe como se ha creado un cliente que utilizaremos para el MQTT local (cliente_local) y funciones de "on_connect" tanto para el cliente local como el cliente remoto.

Dentro de la función "on_connect_local" agregar las lineas requeridas para suscribirse a los tópicos de gps e inerciales:
```python
client.subscribe("sensores/gps")
client.subscribe("sensores/inerciales")
```

Crear la función de "on_message" que utilizaremos para capturar los mensajes que llegan a los topicos suscriptos al MQTT local:
```python
def on_message(client, userdata, message):
    topico = message.topic
    mensaje = str(message.payload.decode("utf-8"))
    print(f"mensaje recibido {mensaje} en topico {topico}")
```

### 5 - Enviar datos a remoto
Antes de comenzar, editar el archivo .env la variable "DASHBOARD_TOPICO_BASE" con su usuario de alumno del campus.

Dentro del bloque principal del programa, antes de la conexión al cliente local agregar un cliente que se conecte al MQTT remoto del dashboardiot:
```python
random_id = random.randint(1, 999)
client_remoto = paho.Client(f"gps_mock_remoto_{random_id}")
client_remoto.on_connect = on_connect_remoto
# Configurar las credenciales del broker remoto
client_remoto.username_pw_set(config["DASHBOARD_MQTT_USER"], config["DASHBOARD_MQTT_PASSWORD"])
client_remoto.connect(config["DASHBOARD_MQTT_BROKER"], int(config["DASHBOARD_MQTT_PORT"]))
client_remoto.loop_start()
```

Agregar la variable de "cliente_remoto" dentro de las "user_data" del cliente local, utilizando "user_data_set":
```python
client_local = paho.Client("gps_mock_local")
client_local.on_connect = on_connect_local
client_local.on_message = on_message
client_local.user_data_set({"client_remoto": client_remoto})
```

En la función "on_message" obtener nuevamente la variable "cliente_remoto" de "user_data":
```python
client_remoto = userdata["client_remoto"]
```

Enviar el dato recibido en "on_message" al MQTT remoto, transformando el tópico agregando "DASHBOARD_TOPICO_BASE" al comienzo del tópico recibido.
```python
topico_remoto = config["DASHBOARD_TOPICO_BASE"] + topico
client_remoto.publish(topico_remoto, mensaje)
```

En el caso de recibir datos en "sensores/gps", el resultado final será:
```
topico_remoto = dashboardiot/<usuario_campus>/sensores/gps
```



