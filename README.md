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


## Pasos para ejecutar el proyecto
Para poder correr el proyecto de manera local seguir los siguientes pasos

1- Hacer build de los servicio
```sh
docker compose build
```
2- Mover el archivo en .env_example a .env
```sh
mv .env_example .env
```
3- Ejecutar el proyecto
```sh
docker compose up
```
## Documentacion de APIs
- http://localhost:8000/docs/
- http://localhost:8000/redocs/

## Crear un superusuario e ingresar al Admin
1- Ejecutar el siguiente comando para crear un superusuario
```sh
docker compose run task-manager python manage.py createsuperuser
```
2- Ingresar al sitio Admin
- http://localhost:8000/admin
## Pasos para ver los emails para el registro de usuario
1- Ejecutar el siguiente comando para determinar el nombre del archivo del email
```sh
docker exec task-manager-local ls /tmp/app-messages
```
2- Ver el contenido del mail y copiar la url de verificion
```sh
docker exec task-manager-local cat /tmp/app-messages/<nombre-del-archivo>
```
## Pasos para correr los tests
1- Ejecutar pytest
```sh
docker compose run task-manager pytest
```
2- Ver el reporte de coverage de codigo
```sh
docker compose run task-manager coverage report
```
## Track de las tareas de celery
1- Para poder monitorear las tareas de celery ingresar a
```sh
http://localhost:8888/
```
