# DMS 2021-2022 Backend Service

This service provides backend logic to the appliance.

## Installation

Run `./install.sh` for an automated installation.

To manually install the service:

```bash
# Install the service itself.
./setup.py install
```

## Configuration

Configuration will be loaded from the default user configuration directory, subpath `dms2122backend/config.yml`. This path is thus usually `${HOME}/.config/dms2122backend/config.yml` in most Linux distros.

The configuration file is a YAML dictionary with the following configurable parameters:

- `db_connection_string` (mandatory): The string used by the ORM to connect to the database.
- `host` (mandatory): The service host.
- `port` (mandatory): The service port.
- `debug`: If set to true, the service will run in debug mode.
- `salt`: A configurable string used to further randomize the password hashing. If changed, existing user passwords will be lost.
- `authorized_api_keys`: An array of keys (in string format) that integrated applications should provide to be granted access to certain REST operations.
- `auth_service`: A dictionary with the configuration needed to connect to the authentication service.
  - `host` and `port`: Host and port used to connect to the service.
  - `apikey_secret`: The API key this service will use to present itself to the authentication service in the requests that require so. Must be included in the authentication service `authorized_api_keys` whitelist.

## Running the service

Just run `dms2122backend` as any other program.

## REST API specification

This service exposes a REST API in OpenAPI format that can be browsed at `dms2122backend/openapi/spec.yml` or in the HTTP path `/api/v1/ui/` of the service.

## Services integration

The backend service requires an API key to ensure that only the whitelisted clients can operate through the REST API.

Requesting clients must include their own, unique API key in the `X-ApiKey-Backend` header.

When a request under that security schema receives a request, the key in this header is searched in the whitelisted API keys at the service configuration (in the `authorized_api_keys` entry). If the header is not included or the key is not in the whitelist, the request will be immediately rejected, before being further processed.

This service also has its own API key to integrate itself with the authentication service. This key must be thus whitelisted in the authentication service in order to operate.

As some operations required in the authentication service require a user session, clients using this backend must obtain and keep a valid user session token, that will be passed in the requests to this service to authenticate and authorize them.


## Comunicaciones entre servicios y arquitectura

El backend contiene una arquitectura de 4 capas, con capas de datos, lógica, servicios y presentación. Esto nos permite mantender las responsabilidades separadas atendiendo al principio SOLID de Single Responsibility, y reducir el número de dependencias de cada clase.

Para poder acceder a los diferentes datos desde el frontend, se especifica en el archivo `openapi/spec.yml` las diferentes rutas que forman este servicio, y los métodos get, post y put de cada una de ellas. Al entrar a una ruta, esta llamará al método correspondiente de la capa de presentación, pasándole los parámetros indicados, ya sea aquellos incluidos en la url o aquellos guardados en un paquete json. 

Los métodos de la capa de presentación estarán almacenados en los ficheros `presentation/rest/question`, `presentation/rest/answer` y `presentation/rest/stats`, correspondientes con las operaciones relacionadas con preguntas, respuestas y estadísticas, respectivamente. Estos métodos se encargan de llamar a los métodos de la capa de servicios, obtener sus datos, y transformarlos en datos que puedan ser utilizados por el frontend. Esto último principalmente conlleva transformar las diferentes excepciones en valores de estado de HTTP, con sus correspondientes mensajes de error, y en caso de que no haya ninguna exepción, devolver los diccionarios o listas de diccionarios que contengan los datos, junto al valor de estado de HTTP.ok indicando que la operación ha sido exitosa.

A continuación, la capa de servicios consiste en los métodos incluidos en los archivos `service/questionservices`, `service/answerservices` y `service/statsservices`, los cuales son los responsables de crear sesiones en la base de datos, llamar a los métodos de la capa de servicios, y guardar los resultados en diccionarios, listas de diccionarios u otros tipos de datos como valores booleanos. Esta transformación se realiza para que, en la comunicación con el frontend, se puedan transformar fácilmente los datos a archivos JSON. También relanzará las excepciones que le lleguen de la capa de datos.

Por otro lado, en la capa de lógica encontramos las clases `questionlogic`, `answerlogic` y `statslogic`. Estas clases contendrán métodos que llamarán a la capa de datos, y en caso necesario, manejarán esos datos realizando las operaciones necesarias para obtener datos más complejos. Dentro de esas operaciones entrará la comprobación de roles del usuario que hace la llamada (cosa que no hemos podido implementar a tiempo, y queda en comentarios para no interferir con la ejecución), la obtención de las diferentes estadísticas sobre los datos, y la obtención de puntuaciones de las respuestas, por ejemplo. También relanzará las excepciones que le lleguen de la capa de datos.

Por último, en cuanto la capa de almacenamiento de los datos, se maneja en `data/db`, la cual contiene las clases correspondientes a las tablas de preguntas (`question`) y respuestas (`answer`), además de las clases que contienen los métodos para modificar estas tablas (`questions` y `answers`).



En cuanto a los diferentes endpoints del backend, serán los siguientes:

 - `/questions`: 
   - `get`: obtendrá una lista de todas las preguntas de la base de datos. Llama a la función `list_questions`.
 - `/questions/{username}/pending`: 
   - `get`: obtendrá una lista de preguntas a las que no ha respondido un usuario. Llama a la función `list_pending_for_user`.
 - `/questions/{username}/answered`: 
   - `get`: obtendrá una lista de preguntas ya respondidas por un usuario. Llama a la función `list_answered_for_user`.
 - `/question/new`:
   - `post`: creará una nueva pregunta. Llama a la función `create_question`.
 - `/question/{id}`:
   - `put`: actualizará la información de una pregunta. Llama a la función `edit_question`.
   - `get`: obtendrá la información de una pregunta dada su id. Llama a la función `get_question_by_id`.
 - `/question/{id}/answers`:
   - `get`: Indicará si una pregunta ha sido respondida por algún alumno o no. Llama a la función `question_has_answers`.
 - `/question/{id}/answer/{username}`:
   - `post`: guardará una nueva respuesta a una pregunta por un alumno. Llama a la función `answer`.
   - `get`: obtendrá la respuesta a la pregunta indicada por el alumno indicado. Llama a la función `get_answer`.
 - `/answers`:
   - `get`: obtendrá todas las respuestas de la base de datos. Llama a la función `list_answers`.
 - `/answers/{id}`:
   - `get`: obtendrá todas las respuestas relacionadas con una pregunta dada su id. Llama a la función `list_all_for_question`.
 - `/answers/{username}`:
   - `get`: obtendrá todas las respuestas relacionadas con un usuario dado su nombre de usuario. Llama a la función `list_all_for_user`.
 - `/stats/questions`:
   - `get`: obtendrá las estadísticas referentes a las diferentes preguntas de la base de datos. Llama a la función `questions_stats`.
 - `/stats/users`:
   - `get`: obtendrá las estadísticas referentes a los diferentes alumnos. Llama a la función `users_stats`.
 - `/stats/{username}`:
   - `get`: obtendrá las estadísticas referentes al alumno indicado. Llama a la función `user_stats`.

