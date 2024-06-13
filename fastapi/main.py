from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import pandas as pd
import numpy as np

# Crea una instancia de FastAPI, que será el núcleo de tu aplicación.
app = FastAPI()

# Configuración de seguridad: define el URL donde los usuarios pueden obtener un token.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Base de datos simulada de usuarios.
users_db = {
    "admin": {
        "username": "admin",
        "hashed_password": "fakehashedsecret"
    }
}

# Función para simular el hashing de contraseñas.
def fake_hash_password(password: str):
    return "fakehashed" + password

# Endpoint para autenticación de usuarios, devuelve un token si las credenciales son válidas.
@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = users_db.get(form_data.username)
    if not user_dict or not fake_hash_password(form_data.password) == user_dict["hashed_password"]:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"access_token": user_dict["username"], "token_type": "bearer"}

# Endpoint para leer los datos de procesos judiciales.
@app.get("/procesos/")
async def read_procesos(token: str = Depends(oauth2_scheme)):
    try:
        # Carga el archivo CSV que contiene los datos de los procesos.
        df = pd.read_csv("../base_de_datos.csv")

        # Reemplaza los valores infinitos y NaN por None para asegurar la compatibilidad con JSON.
        df.replace([np.inf, -np.inf, np.nan], None, inplace=True)

        # Devuelve los datos en formato de diccionario orientado a registros.
        return df.to_dict(orient='records')
    except Exception as e:
        # Si hay un error al cargar o procesar el archivo, devuelve un error 404.
        raise HTTPException(status_code=404, detail=str(e))

# Si el archivo se ejecuta como script principal, inicia el servidor Uvicorn.
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)