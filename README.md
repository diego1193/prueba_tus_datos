# Proyecto de Extracción y Exposición de Datos Judiciales

## Descripción
Este proyecto implementa un sistema de extracción de datos de la página web "Consulta de Procesos Judiciales" utilizando técnicas de Web Scraping con Python. La información extraída es limpiada y almacenada estructuradamente en un archivo CSV. Además, el proyecto incluye una funcionalidad para automatizar y ejecutar hasta 15 consultas en paralelo, lo cual permite probar la capacidad y rendimiento del sistema bajo carga. Esta capacidad es fundamental para asegurar la escalabilidad y eficiencia del sistema en entornos de producción. Además, se expone esta información a través de una API REST construida con FastAPI, que incluye autenticación y autorización para acceso seguro.

## Componentes del Proyecto
- **automate_queries/**: Contiene scripts para automatizar consultas y ejecutar pruebas de carga con 15 consultas paralelas.
- **web_scraping_csv/**: Scripts para realizar web scraping y guardar los datos en `base_de_datos.csv`.
- **fastapi/**: Código fuente para la API REST que sirve los datos extraídos.

## Configuración del Entorno
Se requiere Python 3.6 o superior. Para instalar las dependencias, ejecute:

```bash
pip install -r requirements.txt
```

## Ejecución de Scripts
### Web Scraping  
Para ejecutar el script de web scraping y almacenar los datos:

```bash
python web_scraping_csv/web_scraping.py
```

### Automatización de Consultas
Para ejecutar consultas paralelas y realizar pruebas:

```bash
python automate_queries/automatizacion_consultas.py
```

### Ejecución de Tests
Para ejecutar los tests asociados:

```bash
pytest-3 automate_queries/test.py
```

## API REST con FastAPI
### Iniciar el Servidor

Para iniciar la API, navegue al directorio fastapi/ y ejecute:

```bash
uvicorn main:app --reload
```

### Ejecución de Tests
Para ejecutar los tests asociadosa la API:

```bash
pytest-3 test.py
```

### Documentación y Uso de la API

Acceda a http://127.0.0.1:8000/docs para ver la documentación Swagger de la API, donde puede autenticarse y probar los endpoints disponibles.

### Autenticación (Obtención del Token de Acceso)

Para obtener el token de acceso, que es necesario para autenticarse y acceder a los endpoints protegidos de la API, debes realizar una solicitud POST con tus credenciales de usuario. Este token es parte del sistema de seguridad que implementa JWT (JSON Web Tokens) para mantener segura la comunicación entre el cliente y el servidor.

1. Preparar la Solicitud POST:

   * URL: http://127.0.0.1:8000/token
   * Método: POST
   * Tipo de Contenido: application/x-www-form-urlencoded
   Cuerpo de la 
   * Solicitud: Debes incluir en el cuerpo de la solicitud los parámetros de username y password.


2. Enviar Credenciales:

   * username: Aquí va el nombre de usuario, por ejemplo, "admin".
   * password: Aquí va la contraseña asociada al usuario, por ejemplo, "secret".

3. Respuesta Token

    Recibirás un token de acceso en la respuesta. Este token es un "Bearer token" que necesitas incluir en las cabeceras de las solicitudes subsecuentes para acceder a los endpoints protegidos.

### Hacer Solicitud GET Usando el Token

Una vez que tienes el token, puedes usarlo para hacer solicitudes GET a endpoints que requieren autenticación.

* URL: http://127.0.0.1:8000/procesos/
* Método: GET
* Cabecera de Autorización:
* Key: Authorization
* Value: Bearer <token> (reemplaza <token> con el token real que obtuviste, ejemplo "admin").