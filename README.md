# Autoactivar colas de procesos de Business Central.
Script en Python que detecta cuando se cae una cola de Business Central y la activa automáticamente

Manda avisos por telegram cuando hay algún problema. Es necesario crear un fichero **config.py** con los siguientes valores:
- TELEGRAM_TOKEN = "TOKEN_BOT"
- TELEGRAM_GROUP_ID = ID_Grupo_al_que_mandar_avisos

## Uso
Build docker image:
```
docker image build -t colas_bc .
```

Using docker:
```
docker container run -d --rm -it colas_bc
```

or
```
docker container run -d -it colas_bc
```