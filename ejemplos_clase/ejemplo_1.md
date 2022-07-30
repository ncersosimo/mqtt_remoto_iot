## Ejemplos de clase

### 1 - Preparar el entorno de trabajo

En esta práctica utilizaremos la librería de python "Paho MQTT" para enviar mensajes

Logearse desde VM y obtener cual es la dirección IP del dispositivo:
```sh
$ ifconfig
```

Conectarse por ssh desde una terminal del host:
```
$ ssh inove@<ip_dispositivo>
```

Crear la carpeta "clase_3" para trabajar sobre los ejemplos de esta clase:
```sh
$ mkdir clase_3
```

Ingresar a la carpeta creada y clonar la carpeta del repositorio de esta clase:
```sh
$ cd clase_3
$ git clone https://github.com/InoveAlumnos/mqtt_remoto_iot
$ cd mqtt_remoto_iot
```

Abrir el Visual Studio Code y conectarse de forma remota al dispositivo. Trabajaremos sobre la carpeta recientemente clonada de repositorio.


### 2 - GPS Mock
Desde el VSC abrir el script de "ejemplo_1_gps_mock.py".

Crear la función de "on_connect" que utilizaremos para verificar que nuestro script pude conectarse exitosamente a la aplicación:
```python
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Mqtt Local conectado")
    else:
        print(f"Mqtt Local connection faild, error code={rc}")
```

Dentro del bloque principal del programa, crear el cliente MQTT y conectarse la IP y puerto definidos en las variables de entorno:
```python
client = paho.Client("gps_mock_local")
client.on_connect = on_connect
client.connect(config["BROKER"], int(config["PORT"]))
client.loop_start()
```

Crear un loop para enviar un mensaje de forma constante. Enviaremos una posición de GPS falsa que evolucionará con el tiempo.
```python
for i in range(4000):
    data["longitude"] += .0001
    data_jsonstr = json.dumps(data)
    ret = client.publish(topico, data_jsonstr) 
    time.sleep(.1)
```

Finalizar el script con la desconexión del publicador y la finalización del cliente MQTT:
```python
client.disconnect()
client.loop_stop()
```

### 3 - Verificación
Verificar con MQTTExplorer que los datos están siendo enviados correctamente.
