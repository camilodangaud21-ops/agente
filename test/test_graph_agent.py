from agents.graph_agent import (
    ejecutar_graph_agent
)


ruta_json = "data/output/consolidado.json"

ruta_grafo = "data/output/grafo.graphml"


grafo = ejecutar_graph_agent(
    ruta_json,
    ruta_grafo
)


print("\nNODOS DEL GRAFO:\n")

for nodo, datos in grafo.nodes(data=True):

    print(
        f"- {nodo} | {datos}"
    )


print("\nRELACIONES:\n")

for origen, destino, datos in grafo.edges(data=True):

    print(
        f"- {origen} "
        f"--[{datos.get('relacion')}]--> "
        f"{destino}"
    )


print(
    f"\nGrafo guardado en: {ruta_grafo}"
)