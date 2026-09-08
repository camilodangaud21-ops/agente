import os
import base64

from services.gemma_service import consultar_gemma_imagen


def procesar_imagen(ruta_imagen: str) -> dict:
    """
    Envía una imagen a Gemma 3 mediante Ollama y devuelve
    la información analizada en formato JSON.
    """

    if not os.path.exists(ruta_imagen):
        raise FileNotFoundError(
            f"No se encontró la imagen: {ruta_imagen}"
        )

    # Leer y convertir la imagen a Base64
    with open(ruta_imagen, "rb") as archivo:
        imagen_base64 = base64.b64encode(
            archivo.read()
        ).decode("utf-8")

    prompt = """
Analiza cuidadosamente la imagen proporcionada.

Extrae únicamente información que realmente esté presente
en la imagen.

Devuelve exclusivamente un JSON válido con esta estructura:

{
    "fuente": "imagen",
    "tipo_contenido": "",
    "descripcion_general": "",
    "texto_detectado": [],
    "objetos_detectados": [],
    "datos_relevantes": {},
    "nivel_confianza": ""
}

Reglas:
- No inventes información.
- Si no puedes identificar un dato, usa null.
- texto_detectado debe ser una lista.
- objetos_detectados debe ser una lista.
- Devuelve únicamente JSON.
"""

    return consultar_gemma_imagen(
        prompt,
        imagen_base64
    )
