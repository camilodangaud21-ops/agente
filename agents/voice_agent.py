import json

from services.gemma_service import consultar_gemma_json


def interpretar_comando(texto: str) -> dict:
    """
    Interpreta un comando de voz transcrito y lo convierte
    en una intención estructurada mediante Gemma.
    """

    if not texto or not texto.strip():
        raise ValueError(
            "No se recibió ningún texto para interpretar."
        )

    prompt = f"""
Eres un agente especializado en interpretar comandos
de voz de un sistema multimodal.

El usuario ha dicho:

"{texto}"

Tu tarea es identificar qué quiere hacer el usuario.

Las intenciones permitidas son exclusivamente:

- generar_reporte
- consultar_grafo
- analizar_informacion
- procesar_imagen
- procesar_audio
- desconocido

Devuelve únicamente un JSON válido.

Utiliza exactamente esta estructura:

{{
    "intencion": "",
    "datos": {{}}
}}

Reglas:

1. No inventes información.
2. Extrae del texto los datos relevantes.
3. Si el usuario menciona una persona, conserva su nombre.
4. Si menciona algún dato específico, inclúyelo.
5. Si no puedes determinar la intención, utiliza "desconocido".
6. No ejecutes ninguna acción.
7. No expliques tu respuesta.
8. Devuelve únicamente JSON.

Ejemplo:

Usuario:
"Genera un reporte del paciente Juan Pérez"

Respuesta:

{{
    "intencion": "generar_reporte",
    "datos": {{
        "paciente": "Juan Pérez"
    }}
}}
"""

    resultado = consultar_gemma_json(
        prompt,
        opciones={
            "temperature": 0,
            "num_predict": 128
        }
    )

    return resultado