from services.graph_service import (
    construir_grafo_desde_json
)


def ejecutar_graph_agent(
    ruta_json: str,
    ruta_salida: str
):
    """
    Ejecuta el agente encargado de transformar
    información estructurada en un grafo.
    """

    print("[1/2] Construyendo grafo...")

    grafo = construir_grafo_desde_json(
        ruta_json,
        ruta_salida
    )

    print("[2/2] Grafo generado correctamente.")

    print(
        f"Nodos: {grafo.number_of_nodes()}"
    )

    print(
        f"Relaciones: {grafo.number_of_edges()}"
    )

    return grafo