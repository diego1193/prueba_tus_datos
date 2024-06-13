import requests
import json
import pandas as pd

page = 1
size = 1000

# Headers necesarios para la solicitud
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

def response_api(page, size, document, type_process):
    # URL del endpoint correcto
    url = f'https://api.funcionjudicial.gob.ec/EXPEL-CONSULTA-CAUSAS-SERVICE/api/consulta-causas/informacion/buscarCausas?page={ page }&size={ size}'

    # Datos a enviar en el body de la solicitud POST en formato JSON
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

    json_data = json.dumps(data)
    response = requests.post(url, headers=headers, data=json_data)
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data)  # Asumiendo que los datos están bajo la clave 'datos'
        df["proceso"] = type_process
        return "ok", df
    return "error", None

documents = [
    {"document": "0968599020001", "type": "actor"},
    {"document": "0992339411001", "type": "actor"},
    {"document": "1791251237001", "type": "demandado"},
    {"document": "0968599020001", "type": "demandado"}
]
df_base = pd.DataFrame()
for doc in documents:
  # Extrae el documento y el tipo de proceso del diccionario
  document = doc['document']
  type_process = doc['type']
  status, df = response_api(page, size, document, type_process)
  size = 1000  # Establece el tamaño inicial de página

  while df is not None and status == "ok":
    df_base = pd.concat([df_base, df], axis=0, ignore_index=True)
    if len(df) < size:
      break
    else:
      size += 1000
      status, df = response_api(page, size, document, type_process)

df_base.reset_index(drop=False, inplace=True)
df_base.rename(columns={'index': 'id'}, inplace=True)
df_base['id'] += 1  # Si deseas que los IDs comiencen en 1 en lugar de 0

df_base.to_csv("base_de_datos.csv", sep=',', index=False, encoding='utf-8')
