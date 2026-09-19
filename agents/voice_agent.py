import json

from services.gemma_service import consultar_gemma_json


# ==========================================
# FILTRO RÁPIDO POR PALABRAS CLAVE
# ==========================================

_PALABRAS_CLAVE_INTENCION = {
    "procesar_informacion_completa": [
        "procesa todo", "procesar todo", "procesar toda la información",
        "procesar toda la informacion", "flujo completo",
        "flujo multimodal", "genera el conocimiento",
        "generar el conocimiento", "construye el conocimiento",
        "construir el conocimiento", "procesa imagen y audio",
        "procesar imagen y audio", "haz todo el proceso",
        "hacer todo el proceso"
    ],
    "integrar_informacion": [
        "integrar", "integra", "integración", "integracion",
        "consolidar", "consolida", "combinar", "combina",
        "unir información", "unir informacion", "información conjunta",
        "informacion conjunta"
    ],
    "procesar_imagen": [
        "imagen", "imágen", "foto", "fotografia", "fotografía",
        "ilustracion", "ilustración", "captura", "screenshot"
    ],
    "procesar_audio": [
        "audio", "sonido", "grabacion", "grabación",
        "mp3", "wav", "voz grabada", "escucha el"
    ],
    "generar_reporte": [
        "reporte", "informe", "documento final", "pdf",
        "resumen final"
    ],
    "consultar_grafo": [
        "grafo", "relaciones", "conexiones", "conectado",
        "conecta"
    ],
    "analizar_informacion": [
        "analiza", "analizar", "informacion", "información",
        "conocimiento", "consolidado", "consolidada",
        "extrae", "extraer"
    ],
}


def _detectar_categoria_probable(texto: str):
    """
    Revisa el texto transcrito buscando una intención conocida.
    Las frases del flujo completo se revisan primero para evitar
    que palabras como "imagen" o "audio" las clasifiquen antes.
    """

    texto_normalizado = texto.lower()

    for intencion, palabras_clave in _PALABRAS_CLAVE_INTENCION.items():
        for palabra in palabras_clave:
            if palabra in texto_normalizado:
                return intencion

    return None


def interpretar_comando(texto: str) -> dict:
    """
    Interpreta un comando de voz transcrito y lo convierte
    en una intención estructurada mediante Gemma.
    """

    if not texto or not texto.strip():
        raise ValueError(
            "No se recibió ningún texto para interpretar."
        )

    categoria_probable = _detectar_categoria_probable(texto)

    if categoria_probable is None:
        print(
            "\n[INFO] No se detectó ninguna palabra clave conocida. "
            "Se omite la consulta a Gemma."
        )
        return {
            "intencion": "desconocido",
            "datos": {}
        }

    prompt = f"""
Eres un agente especializado en interpretar comandos
de voz de un sistema multimodal.

El usuario ha dicho:

"{texto}"

Tu tarea es identificar qué quiere hacer el usuario.

Las intenciones permitidas son exclusivamente:

- procesar_informacion_completa
- generar_reporte
- consultar_grafo
- analizar_informacion
- procesar_imagen
- procesar_audio
- integrar_informacion
- desconocido

Devuelve únicamente un JSON válido con esta estructura:

{{
    "intencion": "",
    "datos": {{}}
}}

Reglas:
1. No inventes información.
2. Extrae del texto los datos relevantes.
3. Si menciona una persona, conserva su nombre.
4. Si menciona algún dato específico, inclúyelo.
5. Si no puedes determinar la intención, utiliza "desconocido".
6. No ejecutes ninguna acción.
7. No expliques tu respuesta.
8. Devuelve únicamente JSON.
9. "procesar_informacion_completa" significa ejecutar el flujo
   completo: procesar imagen y audio, integrar ambas fuentes,
   extraer conocimiento, generar el grafo de conocimiento y
   exportarlo a Obsidian.
10. Usa "integrar_informacion" solamente cuando el usuario
    quiera unir resultados que ya fueron procesados.
11. Si hay errores de transcripción, interpreta el sentido general.

Ejemplos:

Usuario:
"procesa toda la información y genera el conocimiento"

Respuesta:
{{
    "intencion": "procesar_informacion_completa",
    "datos": {{}}
}}

Usuario:
"integra la información de la imagen y el audio"

Respuesta:
{{
    "intencion": "integrar_informacion",
    "datos": {{}}
}}

Usuario:
"genera un reporte"

Respuesta:
{{
    "intencion": "generar_reporte",
    "datos": {{}}
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
