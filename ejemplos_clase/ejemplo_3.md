# Ejemplos de clase

### 1 - Preparar el entorno de trabajo

Abrir el Visual Studio Code y conectarse de forma remota al dispositivo. Trabajaremos sobre la carpeta recientemente clonada de este repositorio.


### 2 - GPS Mock
Desde el VSC abrir el script de "ejemplo_3_gps_mock.py". Este archivo posee la solución realizada para el ejemplo_1, el cual reporta la posición de GPS al MQTT local.

Dentro del bloque principal del programa, modificar como el cliente se conecta al MQTT remoto del dashboardiot:
```python
random_id = random.randint(1, 999)
client = paho.Client(f"gps_mock_remoto_{random_id}")
client.on_connect = on_connect
# Configurar las credenciales del broker remoto
client.username_pw_set(config["DASHBOARD_MQTT_USER"], config["DASHBOARD_MQTT_PASSWORD"])
client.connect(config["DASHBOARD_MQTT_BROKER"], int(config["DASHBOARD_MQTT_PORT"]))
client.loop_start()
```

Modificar el topico para que sea enviado según como el dashboard lo espera:
```python
topico = "dashboardiot/<usuario_campus>/" + "sensores/gps"
```

Cada alumno puede proponer modificar como evoluciona la posición de GPS o la posición de GPS inicial en la variable data. Ingresar a google maps y mostrar como obtener una posición de GPS.


### 3 - Verificación
- Verificar con MQTTExplorer que los datos están siendo enviados correctamente al MQTT remoto.
- Observar en el dashboard como evoluciona la posición de GPS de cada alumno.
