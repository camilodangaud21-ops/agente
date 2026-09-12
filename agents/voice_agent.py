import json

from services.gemma_service import consultar_gemma_json


# ==========================================
# FILTRO RÁPIDO POR PALABRAS CLAVE
# ==========================================
#
# Antes de gastar tiempo llamando a Gemma, revisamos si el
# texto transcrito contiene alguna pista razonable de una de
# las intenciones válidas. Si no hay ninguna pista, respondemos
# "desconocido" de inmediato, sin pasar por el modelo (mucho
# más rápido, y evita interpretaciones erróneas de audio mal
# transcrito).
#
# El orden importa: se revisan primero las categorías que pueden
# contener varias fuentes (integración), después las específicas
# (imagen, audio, reporte, grafo) y al final la más genérica
# (analizar_informacion).

_PALABRAS_CLAVE_INTENCION = {
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
    Revisa el texto transcrito (en minúsculas) buscando alguna
    palabra clave asociada a una intención conocida.

    Devuelve el nombre de la intención probable, o None si no
    se encontró ninguna pista razonable.
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

    Antes de llamar a Gemma, se aplica un filtro rápido por
    palabras clave: si el texto no tiene ninguna pista razonable
    de alguna intención válida, se responde "desconocido" sin
    gastar tiempo en el modelo.
    """

    if not texto or not texto.strip():
        raise ValueError(
            "No se recibió ningún texto para interpretar."
        )

    categoria_probable = _detectar_categoria_probable(texto)

    if categoria_probable is None:

        print(
            "\n⚡ No se detectó ninguna palabra clave conocida. "
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

- generar_reporte
- consultar_grafo
- analizar_informacion
- procesar_imagen
- procesar_audio
- integrar_informacion
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
9. El usuario puede expresar la misma intención con frases
   muy distintas, informales, con muletillas o errores de
   transcripción. Interpretá el SENTIDO, no busques palabras
   exactas. Ejemplos de variaciones válidas para cada intención:

   - generar_reporte: "genera un reporte", "hazme un informe",
     "quiero el documento final", "arma el PDF", "necesito el
     reporte de Juan"
   - consultar_grafo: "consulta el grafo", "muéstrame las
     relaciones", "qué conexiones hay", "revisa el grafo de
     conocimiento"
   - analizar_informacion: "analiza la información", "extrae
     el conocimiento", "procesa los datos consolidados",
     "quiero saber qué se relaciona con qué"
   - procesar_imagen: "procesa la imagen", "analiza la foto",
     "mira esta imagen", "qué dice la imagen", "aquí tienes
     la imagen, procésala", "imprime la imagen en json",
     "procesa esta imagen", "revisa esta foto"
   - procesar_audio: "procesa el audio", "escucha el archivo",
     "transcribe el audio", "analiza el sonido", "aquí tienes
     el audio, procésalo", "revisa esta grabación"
   - integrar_informacion: "integra la imagen y el audio",
     "consolida la información", "combina los resultados",
     "une el análisis de imagen y audio", "integra la información
     de ambas fuentes"

10. Si el texto tiene errores de transcripción pero el sentido
    general apunta claramente a una de las intenciones permitidas,
    elegí esa intención en vez de "desconocido". Usá "desconocido"
    solo si de verdad no hay ninguna pista razonable.

Ejemplos:

Usuario:
"Genera un reporte del paciente Juan Pérez"

Respuesta:

{{
    "intencion": "generar_reporte",
    "datos": {{
        "paciente": "Juan Pérez"
    }}
}}

Usuario:
"oye analiza la foto que subí"

Respuesta:

{{
    "intencion": "procesar_imagen",
    "datos": {{}}
}}

Usuario:
"quiero ver cómo se conecta todo en el grafo"

Respuesta:

{{
    "intencion": "consultar_grafo",
    "datos": {{}}
}}

Usuario:
"integra la información de la imagen y el audio"

Respuesta:

{{
    "intencion": "integrar_informacion",
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
