import json
import os

from services.gemma_service import consultar_gemma_json


def cargar_json(ruta: str) -> dict:
    """
    Carga un archivo JSON desde disco.
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


def generar_informe(ruta_consolidado: str) -> dict:
    """
    Genera un informe estructurado a partir de la
    información consolidada.
    """

    print("[1/3] Cargando información consolidada...")

    datos = cargar_json(ruta_consolidado)

    datos_json = json.dumps(
        datos,
        ensure_ascii=False,
        indent=2
    )

    print("[2/3] Generando informe con Gemma...")

    prompt = f"""
Eres un agente encargado de generar informes.

Recibirás información consolidada proveniente de
diferentes fuentes.

Tu tarea es elaborar un informe claro, objetivo y
basado exclusivamente en la información proporcionada.

INFORMACIÓN CONSOLIDADA:

{datos_json}

Devuelve únicamente un JSON válido con esta estructura:

{{
    "titulo": "",
    "resumen_ejecutivo": "",
    "hallazgos_principales": [],
    "informacion_por_fuente": {{
        "imagen": [],
        "audio": []
    }},
    "coincidencias_relevantes": [],
    "contradicciones_detectadas": [],
    "conclusion": "",
    "nivel_confianza_general": ""
}}

Reglas:
- No inventes información.
- No agregues datos externos.
- Si no existen contradicciones, devuelve una lista vacía.
- Utiliza un lenguaje claro y objetivo.
- Devuelve únicamente JSON válido.
"""

    resultado = consultar_gemma_json(prompt)

    print("[3/3] Informe generado correctamente.")

    return resultado