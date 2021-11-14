# DMS 2021-2022 Frontend service

This frontend serves as the human interface for the other services of the appliance.

## Installation

Run `./install.sh` for an automated installation.

To manually install the service:

```bash
# Install the service itself.
./setup.py install
```

## Configuration

Configuration will be loaded from the default user configuration directory, subpath `dms2122frontend/config.yml`. This path is thus usually `${HOME}/.config/dms2122frontend/config.yml` in most Linux distros.

The configuration file is a YAML dictionary with the following configurable parameters:

- `service_host` (mandatory): The service host.
- `service_port` (mandatory): The service port.
- `debug`: If set to true, the service will run in debug mode.
- `app_secret_key`: A secret used to sign the session cookies.
- `auth_service`: A dictionary with the configuration needed to connect to the authentication service.
  - `host` and `port`: Host and port used to connect to the service.
- `backend_service`: A dictionary with the configuration needed to connect to the backend service.
  - `host` and `port`: Host and port used to connect to the service.

## Running the service

Just run `dms2122frontend` as any other program.

## Services integration

The frontend service is integrated with both the backend and the authentication services. To do so it uses two different API keys (each must be whitelisted in its corresponding service); it is a bad practice to use the same key for different services, as those with access to the whitelist in one can create impostor clients to operate on the other.

## Authentication workflow

Most, if not all operations, require a user session as an authorization mechanism.

Users through this frontend must first log in with their credentials. If they are accepted by the authorization service, a user session token will be generated and returned to the frontend. The frontend will then store the token, encrypted and signed, as a session cookie.

Most of the interactions with the frontend check and refresh this token, so as long as the service is used, the session will be kept open.

If the frontend is kept idle for a long period of time, the session is closed (via a logout), or the token is lost with the cookie (e.g., closing the web browser) the session will be lost and the cycle must start again with a login.

## UI pages and components

The UI has the following templates hierarchy and structure:

- `base.html`: Base page. Blocks defined: `title`, `pagecontent`, `footer`.
  - `login.html`: Login form page. Macros used: `flashedmessages`, `submit_button`.
  - `base_logged_in.html`: Base page when a user is logged in. Blocks used: `pagecontent`. Blocks defined: `contentheading`, `contentsubheading`, `maincontent`. Macros used: `flashedmessages`, `navbar`.
    - `home.html`: Home page/dashboard. Blocks used: `title`, `contentheading`, `maincontent`.
    - `student.html`: Main student panel. Blocks used: `title`, `contentheading`, `maincontent`. Blocks defined: `subtitle`, `studentcontent`.
    - `student/progess.html`: Student progress panel. Blocks used: `contentsubheading`, `studentcontent`.
    - `student/questions.html` : Student questions panel. Blocks used: `contentsubheading`, `studentcontent`.
    - `student/questions/answered.html` : Answered questions panel. Blocks used: `contentsubheading`, `studentcontent`. Macros used: `button`.
    - `student/questions/pending.html` : Pending questions panel. Blocks used: `contentsubheading`, `studentcontent`. Macros used: `button`.
    - `student/questions/answered/view.html` : View answered questions panel. Blocks used: `contentsubheading`, `studentcontent`. Macros used: `button`.
    - `student/questions/pending/answer.html` : Answer pending questions panel. Blocks used: `contentsubheading`, `studentcontent`. Macros used: `button`, `submit_button`.
    - `teacher.html`: Main teacher panel. Blocks used: `title`, `contentheading`, `maincontent`. Blocks defined: `subtitle`, `teachercontent`.
    - `teacher/students.html` : Students progress panel. Blocks used: `contentsubheading`, `teachercontent`.
    - `teacher/questions.html` : Questions panel. Blocks used: `contentsubheading`, `teachercontent`. Macros used: `button`.
    - `teacher/questions/edit.html` : Edit questions panel. Blocks used: `contentsubheading`, `teachercontent`. Macros used: `button`, `submit_button`.
    - `teacher/questions/new.html` : New questions panel. Blocks used: `contentsubheading`, `teachercontent`. Macros used: `button`, `submit_button`.
    - `teacher/questions/preview.html` : Preview questions panel. Blocks used: `contentsubheading`, `teachercontent`. Macros used: `button`.
    - `teacher/questions/stats.html` : Stats questions panel. Blocks used: `contentsubheading`, `teachercontent`. 
    - `admin.html`: Main administration panel. Blocks used: `title`, `contentheading`, `maincontent`. Blocks defined: `subtitle`, `administrationcontent`.
    - `admin/users.html`: Users administration listing. Blocks used: `contentsubheading`, `administrationcontent`. Macros used: `button`.
    - `admin/users/new.html`: User creation form page. Blocks used: `contentsubheading`, `administrationcontent`. Macros used: `button`, `submit_button`.
    - `admin/users/edit.html`: User editing form page. Blocks used: `contentsubheading`, `administrationcontent`. Macros used: `button`, `submit_button`.

The following macros/components are provided:

- `macros/navbar.html`
  - `navbar(roles)`: The top navigation bar.
    - Parameters:
      - `roles`: A list of role names.
- `macros/flashedmessages.html`
  - `flashedmessages()`: The bottom panel with the flashed messages.
- `macros/buttons.html`
  - `button(color_class, href, content, onclick=None)`: A link with the appearance of a button.
    - Parameters:
      - `color_class`: A string with a CSS class to use to colorize it (e.g., `bluebg`, `redbg`, `yellowbg`)
      - `href`: The link to follow when clicked.
      - `content`: The contents (usually a string) to display inside the button.
      - `onclick`: If provided, a JavaScript snippet to be run when clicked.
  - `submit_button(color_class, content)`: Special button that submits the containing form. Uses the `button` macro providing a blank link `'#'` as the `href` and a form-submitting statement as the `onclick` argument.
    - Parameters:
      - `color_class` (See `button`)
      - `content` (See `button`)



## Architecture 

El diseño de frontend de la página web se divide en las siguientes partes: 

- Manejo de endpoints: 

Los endpoints se declaran en el fichero de python dms2122frontend situado en la carpeta bin. Cada uno de estos endpoints tendrá una función que llamará a la función correspondiente de ficheros situados en la carpeta `presentation/web`. Esos ficheros serán `adminendpoints.py`, `commonendpoints.py`, `sessionendpoints.py`, `teacherendpoints.py` y `studentendpoints.py`, cada uno con las funciones correspondientes a su nombre. La estructura es así para poder mantener los principios SOLID de Single Responsibility e Interface Segregation, de modo que cada clase tenga solo sus responsabilidades de una parte concreta de la página web, y que dependa solamente de los métodos y clases necesarios para su funcionamiento. 

- Comunicación con el backend: 

Para las operaciones de creación, listado, edición y similares sobre usuarios, el frontend utiliza dos partes importantes. La primera es la clase `authservice.py` de la carpeta `data/rest`, que utiliza el patrón adaptador para comunicarse con los diferentes métodos del servicio dms2122auth que manejan los usuarios y la base de datos, y adaptarlos para poder ser usados en el frontend. La segunda parte consiste en las clases de la carpeta `presentation/web` llamadas `WebAuth` y `WebUser`, que una vez más son implementación del patrón adaptador para obtener la información de la clase authservice y permitir su uso en los diferentes endpoints de los usuarios. Una vez más, están divididas estas funcionalidades en varias clases para respetar los principios SOLID. 

Como en esta primera entrega solamente había que realizar el frontend sin nada de backend, no lo hemos implementado aún, pero su comunicación para el manejo de preguntas y respuestas seguiría la misma estructura, utilizando esta vez la clase `backendservice.py` y creando nuevas clases en el estilo de WebAuth y WebUser. 

- Ficheros HTML: 

La estructura de templates está dividida por carpetas, en la que cada una de ellas representa un rol dentro de la aplicación (a excepción de macros). Dentro de estas carpetas se divide a su vez en más carpetas según las funcionalidades que vayan necesitando, simulando la estructura de URLs de la página web. En cuanto al formato y estilo de los componentes, se maneja en el fichero `style.css` de la carpeta `static`. En su interior se encuentra definido el estilo que va a tomar la web, indicando los colores y la separación de la parte superior, el menú de navegación, márgenes... Además, también incluye el estilo de las tablas, los botones e incluso el menú de login. 

Por último, indicar que queríamos realizar plantillas para los formularios de responder preguntas y listar preguntas con el fin de evitar repetir código, pero inicialmente hemos centrado nuestros esfuerzos en que cada rol pueda cumplir con los requisitos establecidos y ya en posteriores entregas mejorar este aspecto, pues hay bastantes diferencias de código entre los tres formularios en el momento lo que dificulta el uso de plantillas. 
