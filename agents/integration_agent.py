import json
import os

from services.gemma_service import consultar_gemma_json


def cargar_json(ruta: str) -> dict:
    """
    Carga un archivo JSON.
    """

    if not os.path.exists(ruta):
        raise FileNotFoundError(
            f"No se encontró el archivo: {ruta}"
        )

    with open(
        ruta,
        "r",
        encoding="utf-8"
    ) as archivo:

        return json.load(archivo)


def integrar_informacion(
    ruta_imagen: str,
    ruta_audio: str
) -> dict:
    """
    Lee los resultados de imagen y audio y utiliza
    Gemma para relacionar y consolidar la información.
    """

    print("[1/4] Cargando JSON de imagen...")

    datos_imagen = cargar_json(ruta_imagen)

    print("[2/4] Cargando JSON de audio...")

    datos_audio = cargar_json(ruta_audio)

    print("[3/4] Integrando información con Gemma...")

    # Convertimos los diccionarios nuevamente a texto JSON
    imagen_json = json.dumps(
        datos_imagen,
        ensure_ascii=False,
        indent=2
    )

    audio_json = json.dumps(
        datos_audio,
        ensure_ascii=False,
        indent=2
    )

    prompt = f"""
Eres un agente integrador de información.

Recibirás dos fuentes de información estructurada:

1. Un análisis proveniente de una imagen.
2. Un análisis proveniente de un audio.

Tu tarea es:

- Integrar la información de ambas fuentes.
- Identificar coincidencias.
- Identificar información exclusiva de cada fuente.
- Identificar posibles contradicciones.
- No inventar información.
- Si una relación no es clara, indícalo.
- Generar un único JSON válido.

DATOS DE LA IMAGEN:

{imagen_json}

DATOS DEL AUDIO:

{audio_json}

Devuelve únicamente un JSON con esta estructura:

{{
    "fuentes": [
        "imagen",
        "audio"
    ],
    "resumen_integrado": "",
    "coincidencias": [],
    "informacion_exclusiva": {{
        "imagen": [],
        "audio": []
    }},
    "posibles_contradicciones": [],
    "datos_consolidados": {{}},
    "nivel_confianza": ""
}}

Reglas:
- Devuelve únicamente JSON válido.
- No uses Markdown.
- No escribas explicaciones fuera del JSON.
- No inventes datos.
"""

    resultado = consultar_gemma_json(prompt)

    print("[4/4] Integración completada.")

    return resultado