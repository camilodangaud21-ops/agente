from typing import Dict, Any

from agents.report_agent import generar_informe
from agents.graph_agent import ejecutar_graph_agent
from agents.knowledge_agent import extraer_conocimiento
from agents.image_agent import procesar_imagen
from agents.audio_agent import procesar_audio

from services.pdf_service import generar_pdf
from services.file_service import guardar_json
from services.graph_service import (
    cargar_json,
    construir_grafo_conocimiento,
    guardar_grafo
)

from services.agent_result import (
    resultado_exitoso,
    resultado_error
)

from config.settings import (
    CONSOLIDADO_JSON_PATH,
    REPORT_OUTPUT,
    GRAFO_SIMPLE_PATH,
    KNOWLEDGE_JSON_PATH,
    GRAFO_CONOCIMIENTO_PATH,
    IMAGEN_JSON_PATH,
    AUDIO_JSON_PATH,
    DEFAULT_IMAGE_INPUT,
    DEFAULT_AUDIO_INPUT
)


def ejecutar_agente(
    agente: str,
    accion: str,
    datos: Dict[str, Any]
) -> Dict[str, Any]:

    datos = datos or {}

    # ==========================================
    # REPORT AGENT
    # ==========================================

    if agente == "report_agent":

        print("\n📄 Ejecutando Report Agent...")

        try:
            informe = generar_informe(
                CONSOLIDADO_JSON_PATH
            )

            generar_pdf(
                informe,
                REPORT_OUTPUT
            )

            return resultado_exitoso(
                agente="report_agent",
                accion=accion,
                datos=datos,
                resultado={
                    "archivo": REPORT_OUTPUT
                }
            )

        except Exception as e:

            return resultado_error(
                agente="report_agent",
                accion=accion,
                error=str(e),
                datos=datos
            )

    # ==========================================
    # GRAPH AGENT
    # ==========================================

    if agente == "graph_agent":

        print("\n🕸️ Ejecutando Graph Agent...")

        try:
            # NOTA: el proyecto aún no implementa un motor de
            # consultas sobre el grafo. Por ahora, "consultar_grafo"
            # reconstruye el grafo simple a partir del consolidado
            # más reciente y reporta su tamaño. Cuando exista una
            # capacidad real de consulta, esta rama debe actualizarse
            # para usarla en vez de reconstruir el grafo.
            grafo = ejecutar_graph_agent(
                CONSOLIDADO_JSON_PATH,
                GRAFO_SIMPLE_PATH
            )

            return resultado_exitoso(
                agente="graph_agent",
                accion=accion,
                datos=datos,
                resultado={
                    "archivo": GRAFO_SIMPLE_PATH,
                    "nodos": grafo.number_of_nodes(),
                    "relaciones": grafo.number_of_edges()
                }
            )

        except Exception as e:

            return resultado_error(
                agente="graph_agent",
                accion=accion,
                error=str(e),
                datos=datos
            )

    # ==========================================
    # KNOWLEDGE AGENT
    # ==========================================

    if agente == "knowledge_agent":

        print("\n🧠 Ejecutando Knowledge Agent...")

        try:
            consolidado = cargar_json(CONSOLIDADO_JSON_PATH)

            conocimiento = extraer_conocimiento(consolidado)

            guardar_json(
                conocimiento,
                KNOWLEDGE_JSON_PATH
            )

            grafo_conocimiento = construir_grafo_conocimiento(
                conocimiento
            )

            guardar_grafo(
                grafo_conocimiento,
                GRAFO_CONOCIMIENTO_PATH
            )

            return resultado_exitoso(
                agente="knowledge_agent",
                accion=accion,
                datos=datos,
                resultado={
                    "archivo_json": KNOWLEDGE_JSON_PATH,
                    "archivo_grafo": GRAFO_CONOCIMIENTO_PATH,
                    "entidades": grafo_conocimiento.number_of_nodes(),
                    "relaciones": grafo_conocimiento.number_of_edges()
                }
            )

        except Exception as e:

            return resultado_error(
                agente="knowledge_agent",
                accion=accion,
                error=str(e),
                datos=datos
            )

    # ==========================================
    # IMAGE AGENT
    # ==========================================

    if agente == "image_agent":

        print("\n🖼️ Ejecutando Image Agent...")

        try:
            ruta_imagen = datos.get("ruta", DEFAULT_IMAGE_INPUT)

            resultado = procesar_imagen(ruta_imagen)

            guardar_json(
                resultado,
                IMAGEN_JSON_PATH
            )

            return resultado_exitoso(
                agente="image_agent",
                accion=accion,
                datos=datos,
                resultado={
                    "archivo": IMAGEN_JSON_PATH,
                    "analisis": resultado
                }
            )

        except Exception as e:

            return resultado_error(
                agente="image_agent",
                accion=accion,
                error=str(e),
                datos=datos
            )

    # ==========================================
    # AUDIO AGENT
    # ==========================================

    if agente == "audio_agent":

        print("\n🎧 Ejecutando Audio Agent...")

        try:
            ruta_audio = datos.get("ruta", DEFAULT_AUDIO_INPUT)

            resultado = procesar_audio(ruta_audio)

            guardar_json(
                resultado,
                AUDIO_JSON_PATH
            )

            return resultado_exitoso(
                agente="audio_agent",
                accion=accion,
                datos=datos,
                resultado={
                    "archivo": AUDIO_JSON_PATH,
                    "analisis": resultado
                }
            )

        except Exception as e:

            return resultado_error(
                agente="audio_agent",
                accion=accion,
                error=str(e),
                datos=datos
            )

    # ==========================================
    # DESCONOCIDO
    # ==========================================

    return resultado_error(
        agente=agente or "desconocido",
        accion=accion or "desconocida",
        error="No existe un agente asociado.",
        datos=datos
    )
