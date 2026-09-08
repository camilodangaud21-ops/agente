from typing import Dict, Any


def ejecutar_intencion(
    intencion: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Determina qué agente debe ejecutarse
    según la intención interpretada por el Voice Agent.
    """

    nombre_intencion = intencion.get(
        "intencion",
        "desconocido"
    )

    datos = intencion.get(
        "datos",
        {}
    )

    # ------------------------------------------
    # GENERAR REPORTE
    # ------------------------------------------

    if nombre_intencion == "generar_reporte":

        return {
            "agente": "report_agent",
            "accion": "generar_reporte",
            "datos": datos
        }

    # ------------------------------------------
    # CONSULTAR GRAFO
    # ------------------------------------------

    if nombre_intencion == "consultar_grafo":

        return {
            "agente": "graph_agent",
            "accion": "consultar_grafo",
            "datos": datos
        }

    # ------------------------------------------
    # ANALIZAR INFORMACIÓN
    # ------------------------------------------

    if nombre_intencion == "analizar_informacion":

        return {
            "agente": "knowledge_agent",
            "accion": "analizar_informacion",
            "datos": datos
        }

    # ------------------------------------------
    # PROCESAR IMAGEN
    # ------------------------------------------

    if nombre_intencion == "procesar_imagen":

        return {
            "agente": "image_agent",
            "accion": "procesar_imagen",
            "datos": datos
        }

    # ------------------------------------------
    # PROCESAR AUDIO
    # ------------------------------------------

    if nombre_intencion == "procesar_audio":

        return {
            "agente": "audio_agent",
            "accion": "procesar_audio",
            "datos": datos
        }

    # ------------------------------------------
    # DESCONOCIDO
    # ------------------------------------------

    return {
        "agente": None,
        "accion": "desconocido",
        "datos": datos
    }