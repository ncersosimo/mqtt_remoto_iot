# Ejemplos de clase

En esta práctica utilizaremos el MQTT remoto alocado en el servidor de inove, veremos como establecer la IP del broker y las credenciales de acceso.

Logearse desde VM y obtener cual es la dirección IP del dispositivo:
```sh
$ ifconfig
```

Conectarse por ssh desde una terminal del host
```
$ ssh inove@<ip_dispositivo>
```

### 1 - Logearse al dashboard
Utilice su usuario del campus y como contraseña "inoveiot":
```
url: http://inoveiot.herokuapp.com/login
usuario: <usario_campus>
password: inoveiot
```

### 1 - Suscriptor remoto

Suscriberse al tópico "dashboardiot/<usario_campus>/actuadores/luces/1" desde la consola. La consola quedará tomada a la espera de los mensajes provenientes de este tópico. Deberá incluir a su vez incluir las credenciales de MQTT:
```
mqtt_host: 23.92.69.190
mqtt_username: inoveiot
mqtt_password: mqtt
```
```sh
$ mosquitto_sub -h 23.92.69.190 -u "inoveiot" -P "mqtt" -v -t dashboardiot/<usario_campus>/actuadores/luces/1 
```

### 2 - Publicador remoto

Logearse desde otra terminal por ssh. Enviar un mensaje al tópico antes establecido usando las credenciales del MQTT remoto. Al enviar el mensaje deberemos ver en la otra terminal como llega el dato enviado:
```sh
$ mosquitto_pub -h 23.92.69.190 -u "inoveiot" -P "mqtt" -t dashboardiot/<usario_campus>/actuadores/luces/1 -m 1
```

### 3 - Verificación
Veriricar en el dashboard como se prende o apaga la luz

Para ver todos los mensajes que esten llegando al dashboard por diferentes usuarios:
```sh
$ mosquitto_sub -h 23.92.69.190 -u "inoveiot" -P "mqtt" -v -t dashboardiot/#
```