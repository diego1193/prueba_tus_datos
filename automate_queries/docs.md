# Caso de prueba consultas paralelas

## Descripción General

El script de Python llamado "automatizacion_consultas.py" está diseñado para automatizar la extracción de datos de procesos judiciales desde una API especifica de sistema judicial ecuatoriano. Utiliza solicitudes HTTP POST para obtener datos basados en documentos identificativos y el tipo de proceso (actor o demandado).

## Módulos y Librerías Utilizados

*  `request`: Para realizar solicitudes HTTP.

* `concurrent.futures`: Permite la ejecución paralela de solicitudes para mejorar la eficiencia y reducir el tiempod de espera.

* `json`: Para la manipulación de datos en formato JSON.

## Cofiguraciones Globales

* `headers`:  Encabezados HTTP configurados para simular solicitudes desde un navegador web.

## Funciones Principales

* `fetch_data(page, size, document, type_process)`: Realiza solicitudes POST para obtener datos según el documento y el tipo de proceso ('actor' o 'demandado'). Retorna los datos en formato JSON o None en caso de error.

* `automate_queries(documents)`: Gestiona múltiples solicitudes concurrentes a la API, procesando una lista de documentos y roles.

## Ejecución y Resultados
El script se ejecuta de la siguiente forma 

```
python automatizacion_consultas.py
```

 y procesa una lista predefinida de documentos. Al finalizar, imprime los resultados de las consultas o un mensaje de error si no se obtuvieron datos.