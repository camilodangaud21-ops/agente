from services.gemma_service import consultar_gemma_json
from services.whisper_service import transcribir_audio


def procesar_audio(ruta_audio: str) -> dict:
    """
    Procesa un audio:

    Audio → Whisper → Transcripción → Gemma → JSON
    """

    print("[1/4] Transcribiendo audio...")

    transcripcion = transcribir_audio(ruta_audio)

    print("[2/4] Transcripción obtenida:")
    print(transcripcion)

    prompt = f"""
Analiza la siguiente transcripción de audio.

TRANSCRIPCIÓN:

{transcripcion}

Extrae la información relevante y devuelve únicamente
un JSON válido con esta estructura:

{{
    "fuente": "audio",
    "transcripcion": "",
    "resumen": "",
    "temas_detectados": [],
    "datos_relevantes": {{}},
    "nivel_confianza": ""
}}

Reglas:

- No inventes información.
- Utiliza únicamente información presente en la transcripción.
- "temas_detectados" debe ser una lista.
- "datos_relevantes" debe ser un objeto JSON.
- Devuelve únicamente JSON válido.
"""

    print("[3/4] Analizando transcripción con Gemma...")

    resultado_gemma = consultar_gemma_json(prompt)

    resultado_gemma["transcripcion"] = transcripcion

    print("[4/4] Análisis de audio completado.")

    return resultado_gemma
