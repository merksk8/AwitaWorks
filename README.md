# AwitaWorks
Chatbot para Discord para gestionar turnos de trabajo para juegos on-line

### Comandos por defecto

***Los nombres de comandos se pueden cambiar en el archivo de config.py***

**Por defecto, los comandos siempre se activan escribiendo "!" delante, ejemplo: !ayuda**

#### Sólo administradores de servidor de Discord
```
configurarhorario -> Activa el bot en el canal indicado. El bot tiene que tener permisos para el canal.
desconfigurarhorario -> Desactiva el bot en el canal indicado.
maximo [número] -> Activa el límite de trabajadores activos en [número] indicado.
pagar [@usuario] [preciohora] -> Lista las jornadas del [@usuario] y calcula los totales a pagar en relación al [preciohora] ( la respuesta se envía en mensaje privado ) 
reiniciar [@usuario] -> Reinicia las horas del usuario.
eliminar [id] -> Elimina el registro por número [id].
restaurar [id] -> Restaura el registro por número [id].
clean [número-de-filas] -> Se eliminan [número-de-filas] mensajes en la sala.
```
#### Comandos de usuario
```
ayuda -> Muestra la lista de comandos.
entrar -> Entrar en servicio
comprobar -> Muestra el tiempo que llevas en el servicio actual
salir -> Dejas de estar en servicio
total -> Ver el total de horas de todos los servicios ( la respuesta se envía en mensaje privado )
reiniciar -> (CUIDADO!) Reinicias todos los servicios, pasados y actuales
```
### Comandos por reacción
Una vez el bot responde a los comandos de entrada o salida, puedes reaccionar al mensaje para hacer acciones:
```
❌ -> Elimina el registro.
✔ -> El registro se restaura de nuevo.
```

### Configuración
El archivo config.py contiene varias configuraciones:
```
statusText -> Nombre que aparece debajo del nombre de tu usuario que va a actuar de chatbot en Discord.
commandPrefix -> Prefijo para los comandos. Por defecto "!"
discordBotToken -> Token de tu usuario bot de Discord.
databaseUrl -> Enlace para la base de datos MySQL (si es en el mismo servidor, localhost)
databaseUser -> Nombre de usuario para la conexión a la base de datos MySQL
databasePassword -> Contraseña del usuario para la conexión a la base de datos MySQL
databaseName -> Nombre de la base de datos MySQL
```

Además, se pueden configurar todos los comandos.
```
commandEnable = "configurarhorario"
commandDisable = "desconfigurarhorario"
commandEnter = "entrada"
commandCheck = "comprobar"
commandExit = "salida"
commandTotal = "total"
commandPagar = "pagar"
commandHelp = "ayuda"
commandReset = "reiniciar"
commandPrice = "precio"
commandMax = "maximo"
commandDelete = "eliminar"
commandRestore = "restaurar"
```

### Requisitos
- **Cuenta de bot de Discord ([+info](https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token))**
- **Base de datos MySQL**

### Enlaces
[Reportar errores](https://github.com/merksk8/AwitaWorks/issues)
