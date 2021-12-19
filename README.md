![pylint score](https://github.com/eca1001/practica-dms-2021-2022/workflows/pylint%20score/badge.svg)
![mypy typechecking](https://github.com/eca1001/practica-dms-2021-2022/workflows/mypy%20typechecking/badge.svg)

# DMS course project codebase, academic year 2021-2022

The goal of this project is to implement a basic online evaluation appliance deployed across several interconnected services.


## Authors
- [Diego García Muñoz](https://github.com/dgm1003)
- [Ismael Franco Hernando](https://github.com/ifh1001)
- [Enrique Camarero Alonso](https://github.com/eca1001)

## MANUAL DE INSTALACIÓN
Para descargar el repositorio en nuestro ordenador, debemos descargarlo desde la ventana inicial del propio repositorio en github. 
Pinchando en el botón Code, el cual se encuentra coloreado en verde, se abrirá una ventana habilitándose una opción de descargar en forma de zip la cual empezará la descarga una vez se pinche.
 
![image](https://user-images.githubusercontent.com/56863859/144721061-f6e80329-70be-40aa-912f-7f23ca8e2bc7.png)

Una vez descargado, nos dirigimos a la ruta en la cual se encuentra y descomprimimos el zip. Esto permite ya que se pueda utilizar el programa ejecutándose desde el terminal.

## MANUAL DE EJECUCIÓN
Para poder ejecutar el programa debemos acceder a la carpeta con los siguientes pasos:
- Abrir el terminal de Ubuntu
-	Ir a la ruta en la cual se encuentra el programa con la opción cd
-	Entrar en la carpeta con el comando 
```bash
cd practica-dms-2021-2022
```
 
![image](https://user-images.githubusercontent.com/56863859/144721055-66581532-f3f2-499d-b66a-2d2a75ec3610.png)

Una vez nos encontremos en la carpeta tendremos 3 comandos:
-	Si es la primera vez que se descarga el programa en el ordenador se debe ejecutar el comando:
```bash
docker-compose -f docker/config/dev.yml build
```
-	Una vez instalado para ejecutar la aplicación utilizando Docker se utiliza el comando:
```bash
docker-compose -f docker/config/dev.yml up -d
```
-	Para detener la ejecución una vez se ha lanzado el programa se utiliza el comando:
```bash
docker-compose -f docker/config/dev.yml rm -sfv 
```
Para comprobar que el programa ha sido lanzado y parado exitosamente los servicios de auth, backend y frontend deben aparecer junto a un done en color verde.

![image](https://user-images.githubusercontent.com/56863859/144721052-0e4ba5f4-1cf2-4a62-af89-69643eb55196.png)

## MANUAL DE USO
En el buscador se debe acceder a la página 127.10.1.30/login, y acceder con un usuario y contraseña válidos (usuario: admin, contraseña: admin).
En la parte superior tenemos las posibles ventanas a las que puede acceder cada usuario. Estas son: Home (común a todos), Student (para estudiantes), Teacher (para profesores) y Admin (para administradores).
Los permisos a cada usuario deben darse desde Admin, seleccionando el usuario al que queremos cambiar desde “Edit” y seleccionando los permisos que deseamos que tenga.

![image](https://user-images.githubusercontent.com/56863859/144721042-2d5e14c3-b358-44dc-b955-b5807938355b.png)
 
Los profesores, desde la ventana “Teacher” puede ver y crear preguntas desde “Question management” o ver el progreso de los alumnos desde “Student progress”. La primera opción nos permite ver una pregunta como si fuésemos un estudiante y contestarla (no cuanta para las estadísticas) con la opción “Preview”, editar una pregunta si todavía no ha sido contestado con la opción “Edit” y crear nuevas preguntas con “Create new question”.

![image](https://user-images.githubusercontent.com/56863859/144721035-30eb9f31-59cd-4cb8-b2ca-916a99e200d2.png)
 
Para crear una pregunta se deben rellenar todos los campos, los cuales son: un título, el cuerpo de la pregunta, 3 opciones, indicador de la opción correcta, puntuación de la pregunta, y penalización de esta.

Desde el botón "View Statistics" el profesor podrá ver todas las preguntas que ha creado, junto con el número de respuestas que tiene, las veces que se ha seleccionado cada opción y la media de puntuación de esa pregunta.
### Foto

Por otro lado, el profesor desde la ventana de “Student progress” podrá ver una tabla donde se muestran todos los usuarios que han respondido alguna pregunta. Además, pordrá ver información sobre el total de preguntas que ha respondido, su puntuación total o su puntuación sobre 10 de las preguntas que lleva responddias y su nota sobre 10 teniendo en cuanta todas la preguntas (tanto las respondidas como las que no lo estan).
### Foto

Los alumnos, pueden acceder a “Questions” donde pueden contestar las preguntas y “Student progress” para consultar su progreso. La primera opción nos permite ver que preguntas faltan por contestar y cuales han sido contestadas. Para contestar una pregunta pincharemos en “Answer”.
 
![image](https://user-images.githubusercontent.com/56863859/144721023-8e219f3c-7ee9-4568-9d96-375df559a6b6.png)

En la ventana de "Student progress” el usuario podrá ver información a cerca de las preguntas que ha respondido, su puntuación total y su puntuación en base 10 de aquellas preguntas que ha respondido, y por último, la nota sobre 10 con respectoa todas la preguntas que tiene que respondeer.
### Foto

## Components

The source code of the components is available under the `components` direcotry.

### Services

The services comprising the appliance are:

#### `dms2122auth`

This is the authentication service. It provides the user credentials, sessions and rights functionalities of the application.

See the `README.md` file for further details on the service.

#### `dms2122backend`

This service provides the evaluation logic (definition of questions, grading, etc.)

See the `README.md` file for further details on the service.

#### `dms2122frontend`

A frontend web service that allows to interact with the other services through a web browser.

See the `README.md` file for further details on the application.

### Libraries

These are auxiliar components shared by several services.

#### `dms2122core`

The shared core functionalities.

See the `README.md` file for further details on the component.

## Docker

The application comes with a pre-configured Docker setup to help with the development and testing (though it can be used as a base for more complex deployments).

To run the application using Docker Compose:

```bash
docker-compose -f docker/config/dev.yml up -d
```

When run for the first time, the required Docker images will be built. Should images be rebuilt, do it with:

```bash
docker-compose -f docker/config/dev.yml build
```

To stop and remove the containers:

```bash
docker-compose -f docker/config/dev.yml rm -sfv
```

By default data will not be persisted across executions. The configuration file `docker/config/dev.yml` can be edited to mount persistent volumes and use them for the persistent data.

To see the output of a container:

```bash
docker logs CONTAINER_NAME
# To keep printing the output as its streamed until interrupted with Ctrl+C:
# docker logs CONTAINER_NAME -f
```

To enter a running service as another subprocess to operate inside through a terminal:

```bash
docker exec -it CONTAINER_NAME /bin/bash
```

To see the status of the different containers:

```bash
docker container ps -a
```

## Helper scripts

The directory `scripts` contain several helper scripts.

- `verify-style.sh`: Runs linting (using pylint) on the components' code. This is used to verify a basic code quality. On GitHub, this CI pass will fail if the overall score falls below 7.00.
- `verify-type-correctness.sh`: Runs mypy to assess the type correctness in the components' code. It is used by GitHub to verify that no typing rules are broken in a commit.
- `verify-commit.sh`: Runs some validations before committing a changeset. Right now enforces type correctness (using `verify-type-correctness.sh`). Can be used as a Git hook to avoid committing a breaking change:
  Append at the end of `.git/hooks/pre-commit`:

  ```bash
  scripts/verify-commit.sh
  ```

## GitHub workflows and badges

This project includes some workflows configured in `.github/workflows`. They will generate the badges seen at the top of this document, so do not forget to update the URLs in this README file if the project is forked!
