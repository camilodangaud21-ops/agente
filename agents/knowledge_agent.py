import json

from services.gemma_service import consultar_gemma_json


def extraer_conocimiento(datos: dict) -> dict:
    """
    Utiliza Gemma para identificar entidades y relaciones
    dentro de la información consolidada.
    """

    datos_json = json.dumps(
        datos,
        ensure_ascii=False,
        indent=2
    )

    prompt = f"""
Eres un agente especializado en extracción de conocimiento.

Analiza la información consolidada que se proporciona
a continuación.

Tu objetivo es identificar:

1. Entidades.
2. Tipo de cada entidad.
3. Relaciones entre las entidades.
4. Tipo de relación.

INFORMACIÓN:

{datos_json}

Debes utilizar exclusivamente la información proporcionada.

No inventes entidades.
No inventes relaciones.
No agregues información externa.

Devuelve únicamente un JSON válido utilizando
exactamente esta estructura:

{{
    "entidades": [
        {{
            "id": "",
            "nombre": "",
            "tipo": ""
        }}
    ],
    "relaciones": [
        {{
            "origen": "",
            "relacion": "",
            "destino": ""
        }}
    ]
}}

Reglas:

- Cada entidad debe tener un identificador único.
- El campo "id" debe ser corto y fácil de utilizar.
- "tipo" debe describir la naturaleza de la entidad.
- "origen" debe corresponder al id de una entidad.
- "destino" debe corresponder al id de una entidad.
- No crees relaciones que no estén respaldadas por los datos.
- Devuelve solamente JSON.
"""

    return consultar_gemma_json(prompt)