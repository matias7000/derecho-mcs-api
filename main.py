from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup

app = FastAPI()

# Lista de sitios permitidos
SITIOS_PERMITIDOS = [
    "https://www.bcn.cl",
    "https://www.bibliotecajuridica.cl",
    "https://www.leychile.cl"
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