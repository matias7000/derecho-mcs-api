from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import requests
from bs4 import BeautifulSoup
import os

app = FastAPI()

# Lista de sitios permitidos
SITIOS_PERMITIDOS = [
    "https://www.bcn.cl",
    "https://www.bibliotecajuridica.cl",
    "https://www.leychile.cl",
    "https://www.pjud.cl/biblioteca-poder-judicial"
]

@app.get("/buscar")
def buscar_derecho_chileno(palabra: str):
    resultados = []

    for sitio in SITIOS_PERMITIDOS:
        try:
            respuesta = requests.get(sitio)
            sopa = BeautifulSoup(respuesta.text, "html.parser")
            if palabra.lower() in sopa.text.lower():
                resultados.append({"sitio": sitio, "contiene": True})
            else:
                resultados.append({"sitio": sitio, "contiene": False})
        except Exception as e:
            resultados.append({"sitio": sitio, "error": str(e)})

    return {"palabra_buscada": palabra, "resultados": resultados}

# Montar la carpeta .well-known para servir ai-plugin.json
os.makedirs(".well-known", exist_ok=True)
app.mount("/.well-known", StaticFiles(directory=".well-known"), name="static")
from fastapi.staticfiles import StaticFiles
import os

# Asegúrate de que el directorio exista
os.makedirs(".well-known", exist_ok=True)

# Montar la carpeta .well-known como estática
app.mount("/.well-known", StaticFiles(directory=".well-known"), name="static")
