# Ejemplos de clase

En esta práctica utilizaremos el simulador de celular drone "drone_iot" para realizar análisis de señales sobre los valores reales informados por el celular.

En caso que usted no desee user o no pueda usar el simulador "drone_iot" junto a su celular, puede utilizar el simulador "sensores_mock" y enviar por su cuenta los datos deseados de los sensores inerciales. 

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


### 4 - Detección por threshold
Tome el script "ejemplo_4_sensores_mock.py" el cual viene con la conectividad a MQTT resuelta del ejemplo anterior (tanto para local como para el MQTT remoto)

Dentro de la función "on_message" identificar cuando llega un nuevo mensaje del acelerómetro. Establecer un threshold de valor (entre 2 y 10), __si el valor del acelerómetro supera ese valor__ prender la luz del drone enviando un "publish" al dashboard (topico MQTT remoto).

Observar cuantos mensajes de "prender luz" se envian cuando ocurre un movimiento del celular. ¿No creé que se envian demasiados mensajes?

### 4 - Detección por flanco o pulso
Modificar el comportamiento anterior del sistema de análisis del acelerómetro, ahora utilizaremos dos threshold para identificar el concepto de flanco.

- Establecer el threshold de inicio de flanco (entre 2 y 5)
- Establecer el threshold de fin de flanco (entre 6 y 10)
- Deberá también crear una variable de estado que indique en que proceso del flanco nos encontramos.

- Comenzaremos con la variable de estado en 0, indicando que no ha ocurrido ningún evento.
- Si el valor leido del acelerómetro supera el threshold de inicio flanco, colocar la variable en estado 1. Con esto indicaremos que estamos en presencia de un posible flanco (aún no confirmado)
- Si en una próxima lectura el valor baja por debajo del threshold de inicio, diremos que se cancela el flanco volviendo al estado inicial 0.
- Si en una próxima lectura el valor continua siendo mayor al threshold inicial, nos mantendremos en el estado 1 (en presencia de un posible flanco), hasta que el valor del acelerómetro supere al threshold de fin de flanco, pasando entonces al estado 2 indicando que estamos en presencia de un flanco confirmado.
- Si nos encontramos en estado 2, enviamos el mensaje de enceder luz y pasamos el estado a valor 3, indicando que nos encontramos a la espera de que el flanco desaparezca.
- Si el valor del acelerómetro vuele a quedar por debajo del threshold de inicio de flanco, el estado vuelve a su valor inicial 0 permitiendo que vuelva a comenzar el proceso de detección de flanco.