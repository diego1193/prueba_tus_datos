import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import json

# Parámetros iniciales para la paginación de la API
page = 1
size = 1000

# Configuración de los encabezados HTTP para simular una solicitud de navegador y evitar bloqueos por parte de la API
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'es-CO,es-US;q=0.9,es-419;q=0.8,es;q=0.7,ja;q=0.6',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Host': 'api.funcionjudicial.gob.ec',
    'Origin': 'https://procesosjudiciales.funcionjudicial.gob.ec',
    'Referer': 'https://procesosjudiciales.funcionjudicial.gob.ec/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Ch-Ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
}

def fetch_data(page, size, document, type_process):

    # Construcción de la URL con parámetros para la consulta
    url = f'https://api.funcionjudicial.gob.ec/EXPEL-CONSULTA-CAUSAS-SERVICE/api/consulta-causas/informacion/buscarCausas?page={page}&size={size}'
    # Datos para la solicitud POST, incluyendo el documento y el tipo de proceso
    data = {
        "numeroCausa": "",
        "actor": {
            "cedulaActor": document if type_process == "actor" else "",
            "nombreActor": ""
        },
        "demandado": {
            "cedulaDemandado": document if type_process == "demandado" else "",
            "nombreDemandado": ""
        },
        "provincia": "",
        "numeroFiscalia": "",
        "recaptcha": "verdad",
        "first": page,
        "pageSize": size
    }

    # Realiza la solicitud POST y maneja la respuesta
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        print(f'Successfully fetched data for document {document} as {type_process}')
        return response.json()  # Retorna los datos como JSON
    else:
        print(f'Failed to fetch data for document {document} as {type_process}. Status code: {response.status_code}')
        return None  # Retorna None si hay error

# Lista de documentos para procesar
documents = [
    {"document": "0968599020001", "type": "actor"},
    {"document": "0992339411001", "type": "actor"},
    {"document": "1791251237001", "type": "demandado"},
    {"document": "0968599020001", "type": "demandado"},
    {"document": "0968599020001", "type": "actor"},
    {"document": "0992339411001", "type": "actor"},
    {"document": "1791251237001", "type": "demandado"},
    {"document": "0968599020001", "type": "demandado"},
    {"document": "0968599020001", "type": "actor"},
    {"document": "0992339411001", "type": "actor"},
    {"document": "1791251237001", "type": "demandado"},
    {"document": "0968599020001", "type": "demandado"},
    {"document": "0968599020001", "type": "actor"},
    {"document": "0992339411001", "type": "actor"},
    {"document": "0968599020001", "type": "actor"}
]


def automate_queries(documents):
    results = []
    print(f"Starting the data fetching process for {len(documents)} documents...")
    with ThreadPoolExecutor(max_workers=15) as executor:
        # Crea feature para cada documento y procesa asincrónicamente
        future_to_doc = {executor.submit(fetch_data, page, size, doc['document'], doc['type']): doc for doc in documents}
        for future in as_completed(future_to_doc):
            data = future.result()
            if data:
                results.append(data)   # Agrega los resultados a una lista si son exitosos
    
    if results:
        print(f"Successfully completed data fetching for all documents. Total documents processed: {len(results)}")
    else:
        print("No data was fetched. Please check the errors above.")
    return results

# Ejecuta la función de automatización para procesar las consultas
results = automate_queries(documents)
