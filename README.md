# Invera ToDo-List Challenge (Python/Django Jr-SSr)

El propósito de esta prueba es conocer tu capacidad para crear una pequeña aplicación funcional en un límite de tiempo. A continuación, encontrarás las funciones, los requisitos y los puntos clave que debés tener en cuenta durante el desarrollo.

## Qué queremos que hagas:

- El Challenge consiste en crear una aplicación web sencilla que permita a los usuarios crear y mantener una lista de tareas.
- La entrega del resultado será en un nuevo fork de este repo y deberás hacer una pequeña demo del funcionamiento y desarrollo del proyecto ante un super comité de las más grandes mentes maestras de Invera, o a un par de devs, lo que sea más fácil de conseguir.
- Podes contactarnos en caso que tengas alguna consulta.

## Objetivos:

El usuario de la aplicación tiene que ser capaz de:

- Autenticarse
- Crear una tarea
- Eliminar una tarea
- Marcar tareas como completadas
- Poder ver una lista de todas las tareas existentes
- Filtrar/buscar tareas por fecha de creación y/o por el contenido de la misma

## Qué evaluamos:

- Desarrollo utilizando Python, Django. No es necesario crear un Front-End, pero sí es necesario tener una API que permita cumplir con los objetivos de arriba.
- Uso de librerías y paquetes estandares que reduzcan la cantidad de código propio añadido.
- Calidad y arquitectura de código. Facilidad de lectura y mantenimiento del código. Estándares seguidos.
- [Bonus] Manejo de logs.
- [Bonus] Creación de tests (unitarias y de integración)
- [Bonus] Unificar la solución propuesta en una imagen de Docker por repositorio para poder ser ejecutada en cualquier ambiente (si aplica para full stack).

## Requerimientos de entrega:

- Hacer un fork del proyecto y pushearlo en github. Puede ser privado.
- La solución debe correr correctamente.
- El Readme debe contener todas las instrucciones para poder levantar la aplicación, en caso de ser necesario, y explicar cómo se usa.
- Disponibilidad para realizar una pequeña demo del proyecto al finalizar el challenge.
- Tiempo para la entrega: Aproximadamente 7 días.


## Pasos para ejecutar el proyecto con docker compose
Para poder correr el proyecto de manera local seguir los siguientes pasos

1- Copiar archivo .env
```sh
cp .env_example .env
```
2- Hacer build de los servicios
```sh
docker compose build
```
3- Ejecutar el proyecto
```sh
docker compose up
```
## Documentacion de APIs url
```sh
http://localhost:8000/docs/
```
## Crear super usuario e ingresar a Admin
1- Ejecutar el siguiente comando para crear un super usuario. Completar los datos solicitados
```sh
docker compose run task-manager python manage.py createsuperuser
```
2- Ingresar al sitio Admin e ingresar los datos de super usuario creado en el paso anterior
```sh
http://localhost:8000/admin
```
## Ver los emails de verificacion de registro de usuarios
1- Ejecutar el siguiente comando para determinar el nombre del archivo de email de verificacion
```sh
docker exec task-manager-local ls /tmp/app-messages
```
2- Ver el contenido del archivo de email verificacion y copiar url de verificion
```sh
docker exec task-manager-local cat /tmp/app-messages/<nombre-del-archivo>
```
3- Ingresar a la url de verificacion en el navegador para confirmar email
## Ejecutar tests
1- Ejecutar el siguiente comando para ejecutar los tests
```sh
docker compose run task-manager pytest
```
2- Ejecutar el siguiente comando para generar reporte de coverage de codigo
```sh
docker compose run task-manager coverage report
```
## Monitorear tareas de celery
1- Ingresar a la siguiente url para monitorear las tareas de celery
```sh
http://localhost:8888/
```
## Dockerhub repositorio
Repositorio url
```sh
https://hub.docker.com/r/mikerg/invera-challenge-docker
```
Obtener imagen docker
```sh
docker pull mikerg/invera-challenge-docker
```
Ejecutar 'docker' con un archivo de variables de entorno
```sh
$ docker run -env-file <path-dir>/.env --entrypoint /app/entrypoint -p 8000:8000 mikerg/invera-challenge-docker
```
## Github repositorio
Repositorio url
```sh
https://github.com/mike-rg/todo-challenge
```
## Site url
```sh
http://invera.mike-rg-challenges.com/
```