# DeathTerminal

# Instrucciones para levantar el sistema
- docker-compose -f compose.yaml up giadachbus (para verificar: docker logs giadachbus)
- docker-compose -f compose.yaml up postgresdb (para verificar docker logs postgresdb)
- docker-compose -f compose.yaml up uservice (debe salir con código 0 si no hay errores)
- docker-compose -f compose.yaml up penalization_service
- docker-compose -f compose.yaml up instance_reset_service
- docker-compose -f compose.yaml up progress_service
- docker-compose -f compose.yaml up frontend

o levantar todos los servicios juntos: docker-compose -f compose.yaml up

- Revisar contenedores arriba: sudo docker ps
- Bajar todos los contenedores: sudo docker-compose -f compose.yaml down 
 
## ¿Que es esto?

Historia del lore del juego, ponganse creativos!

## ¿Cómo funciona?

Una descripción de como levantar el servicio.

### ¿Cómo iniciar el juego?

Pasos para iniciar el juego.

### Servicios Creados

Listado rapido de los servicios. Nada engorroso. Insertar Imagen!

### Contenido de las bases de datos

Insertar imagen!

### ¿Cómo añado mi propio contenido?

Comentarios bonitos y motivacionales

### ¿Por qué SOA?

No se vale porque el profe lo dijo. (Ponéle voluntad).

## Fuentes y Agradecimientos

- [GodotServer-Docker](https://github.com/GodotNuts/GodotServer-Docker) -> No utilizado
- [Ninjarobot](https://github.com/ninjarobot/mono-in-docker) -> Utilizado
- [MonoGameBaseImage](https://github.com/mikescandy/MonoGameBaseImage/blob/main/Dockerfile) -> Utilizado
- [Servicio SOA](https://github.com/nicobrch/arqui-sw)  -> Utilizado
- [Contenedor C++ Docker](https://github.com/dockersamples/c-plus-plus-docker)