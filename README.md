# APP MONITORING - Gestión y Calidad del Software

Este documento proporciona instrucciones para configurar y ejecutar el proyecto Django utilizando **pipenv**, así como la configuración necesaria para depurar con **Visual Studio Code**.

## Requisitos Previos

- Python +3.12 instalado en tu sistema.
- [Pipenv](https://pipenv.pypa.io/en/latest/) instalado.
- [Visual Studio Code](https://code.visualstudio.com/) instalado.
- (Opcional) [Extensión de Python para Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-python.python).

## Configuración del Entorno

### Clonar el Repositorio

```bash
git clone https://github.com/EstebanP-dev/gcs_clean_data
cd gcs_clean_data
```

### Configurar Variables de Entorno

Crea un archivo llamado `.env` en la raíz del proyecto y define las siguientes variables:

```ini
DEBUG=True
SECRET_KEY='tu_clave_secreta'
DATABASE_NAME='nombre_de_la_base_de_datos'
DATABASE_USER='usuario_de_la_base_de_datos'
DATABASE_PASSWORD='contraseña_de_la_base_de_datos'
DATABASE_HOST='localhost'
DATABASE_PORT='5432'
```

**Nota:** Ajusta los valores de las variables según tu configuración.

### Instalación de Dependencias

Inicia el entorno virtual y instala las dependencias:

```bash
pipenv shell
pipenv install --dev
```

Esto instalará todas las dependencias especificadas en el `Pipfile`.

## Migraciones de Base de Datos

Ejecuta las migraciones de la base de datos:

```bash
pipenv run python manage.py migrate
```

## Crear usuario para Log In

```bash
python manage.py createsuperuser
```

## Ejecución del Servidor de Desarrollo

Para iniciar el servidor de desarrollo de Django:

```bash
pipenv run python manage.py runserver
```

## Inserción de datos aleatorios

```bash
python manage.py start_scheduler --interval 3
```

Siendo `3` el numero de segundos en los que queremos que se ejecute la tarea en bakground.

## Configuración para Depuración con Visual Studio Code

Para depurar el proyecto con Visual Studio Code, agrega el siguiente contenido al archivo `.vscode/launch.json`:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Django",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/manage.py",
            "args": [
                "runserver",
                "9000"
            ],
            "django": true,
            "envFile": "${workspaceFolder}/.env",
            "console": "integratedTerminal"
        }
    ]
}
```

**Nota:** Asegúrate de que la extensión de Python esté instalada en Visual Studio Code.

## Uso de Variables de Entorno en Django

En tu proyecto Django, puedes acceder a las variables de entorno utilizando la biblioteca `os` o paquetes como `python-decouple` o `django-environ`.

Ejemplo utilizando `os`:

```python
import os

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG') == 'True'
```

## Ejecutar Pruebas

Para ejecutar las pruebas del proyecto:

```bash
pipenv run python manage.py test
```

## Base de Datos

Para hacer la conexión con la base de datos MYSQL, hay dos alternativas o creas la base de datos con el docker-compose o cambias los valores en el .env del proyecto para apuntar a tu base de datos local.

### Docker

```bash
docker-compose build
```

```bash
docker-compose up -d
```

## Recursos Adicionales

- [Documentación de Django](https://docs.djangoproject.com/es/)
- [Documentación de Pipenv](https://pipenv.pypa.io/en/latest/)
- [Depuración en VS Code](https://code.visualstudio.com/docs/python/debugging)
