# Ejemplos de clase

En esta práctica utilizaremos el simulador "drone_iot" junto a la librería de Paho MQTT

En caso que usted no desee user o no pueda usar el simulador "drone_iot" junto a su celular, puede utilizar el simulador "sensores_mock". 

Logearse desde VM y obtener cual es la dirección IP del dispositivo:
```sh
$ ifconfig
```

### 1 - Preparar el entorno de trabajo

Abrir el Visual Studio Code y conectarse de forma remota al dispositivo. Trabajaremos sobre la carpeta recientemente clonada de este repositorio.

Clonar el repositorio del simulador de sensores:
```sh
$ git clone https://github.com/InoveAlumnos/drone_iot
```

Topicos que soporta que utilizaremos de este mock:
|             |             | datos ejemplo
| ----------  | --------    | -----
|  sensores   | gps         | {"latitude": -34.55, "longitude": -58.496}
|  sensores   | inericiales | {"heading": 160, accel: 4.5}


### 2 - Lanzar el simulador drone iot
Desde ssh conectado a la VM, ingresar a la carpeta clonada del "drone_iot" y lanzar la aplicación:
```sh
$ python3 app.py
```

Ingresar a su explorador web e ingresar a al aplicación del drone. Recuerde ingresar con la URL en https y aceptar el ingreso "inseguro" a la app.
```
https://<ip_VM>:5010
```

### 3 - Ensayar que el simulador funcione
Utilizar el MQTTExplorar y verificar de esta manera el correcto funcionamiento de cada sensor disponible del celular.


### 4 - Detección por flanco o pulso
Deberá realizar la detección por flanco o pulso del heading (orietación) basado en lo que ha visto en clase de la detección por flanco por aceleración. Deberá seguir las mismas pautas para encender la luz de su celular y la del dashboard enviando un mensaje MQTT (uno al MQTT local y el otro al MQTT remoto) en caso de que el heading superé un cierto valor por flanco ascendente.

Recomendamos utilizar los siguientes thresholds y estados:
```python
THRESHOLD_INICIO = 60
THRESHOLD_FIN = 80

ESTADO_INICIO = 0
ESTADO_PRESENCIA_FLANCO = 1
ESTADO_FLANCO_CONFIRMADO = 2
```

Cuando el sistema supere la orientación de 80º en sentido flanco ascendente, la luz deberá encenderse.


Utilice todas las herramientas a su disposición (terminal, MQTTExplorer, debugger) para ensayar y testear el funcionamiento de su implementación. En caso que tenga problemas, consulte y continue explorando. Lo más rico de estos ejercicios es que pueda analizar las fallas y aprender de ellas por su cuenta como todo un buen detective.

Una vez finalizado el ejercicio y corroborado el funcionamiento, subir al repositorio el script de python resuelto de este ejercicio en la carpeta de "ejercicios_profundizacion" con el nombre de "profundizacion_1.py".
