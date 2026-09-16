"""
servidor_mcp.py

Servidor MCP (Model Context Protocol) que expone el grafo de
conocimiento de este proyecto (data/output/knowledge.json) como
herramientas que un agente de IA (Claude, u otro cliente MCP)
puede usar para consultar entidades y relaciones.

Requiere:
    python -m pip install "mcp<2"

Uso:
    python servidor_mcp.py

(normalmente no se corre a mano: el cliente MCP, ej. Claude
Desktop, lo levanta automáticamente según su configuración)
"""

from mcp.server.fastmcp import FastMCP

from services.graph_service import (
    cargar_json,
    construir_grafo_conocimiento
)

from config.settings import KNOWLEDGE_JSON_PATH


mcp = FastMCP("grafo-de-conocimiento")


def _cargar_grafo():
    """
    Carga el knowledge.json más reciente y construye el grafo
    en memoria. Se vuelve a leer en cada llamada para reflejar
    siempre el último estado generado por el Knowledge Agent.
    """
    datos = cargar_json(KNOWLEDGE_JSON_PATH)
    return construir_grafo_conocimiento(datos)


@mcp.tool()
def buscar_entidad(nombre: str) -> str:
    """
    Busca entidades del grafo de conocimiento cuyo nombre
    coincida (parcial o totalmente) con el texto dado.
    Devuelve el id, nombre y tipo de cada coincidencia.
    """
    grafo = _cargar_grafo()
    nombre_normalizado = nombre.lower()

    coincidencias = []
    for nodo_id, atributos in grafo.nodes(data=True):
        nombre_nodo = atributos.get("nombre", str(nodo_id))
        if nombre_normalizado in nombre_nodo.lower():
            tipo = atributos.get("tipo", "desconocido")
            coincidencias.append(f"[{nodo_id}] {nombre_nodo} ({tipo})")

    if not coincidencias:
        return f"No se encontraron entidades que coincidan con '{nombre}'."

    return "\n".join(coincidencias)


@mcp.tool()
def relaciones_de(nombre_entidad: str) -> str:
    """
    Devuelve todas las relaciones (entrantes y salientes) de
    una entidad del grafo, dado su nombre exacto o su id.
    """
    grafo = _cargar_grafo()

    nodo_id = None
    if nombre_entidad in grafo.nodes:
        nodo_id = nombre_entidad
    else:
        for nid, atributos in grafo.nodes(data=True):
            if atributos.get("nombre", "").lower() == nombre_entidad.lower():
                nodo_id = nid
                break

    if nodo_id is None:
        return f"No existe ninguna entidad llamada '{nombre_entidad}'."

    lineas = []

    for _, destino_id, datos_arista in grafo.out_edges(nodo_id, data=True):
        relacion = datos_arista.get("relacion", "relacionado con")
        nombre_destino = grafo.nodes[destino_id].get("nombre", str(destino_id))
        lineas.append(f"{nombre_entidad} --{relacion}--> {nombre_destino}")

    for origen_id, _, datos_arista in grafo.in_edges(nodo_id, data=True):
        relacion = datos_arista.get("relacion", "relacionado con")
        nombre_origen = grafo.nodes[origen_id].get("nombre", str(origen_id))
        lineas.append(f"{nombre_origen} --{relacion}--> {nombre_entidad}")

    if not lineas:
        return f"'{nombre_entidad}' no tiene relaciones registradas."

    return "\n".join(lineas)


@mcp.tool()
def listar_entidades() -> str:
    """
    Lista todas las entidades del grafo de conocimiento,
    agrupadas por tipo.
    """
    grafo = _cargar_grafo()

    if grafo.number_of_nodes() == 0:
        return "El grafo de conocimiento está vacío."

    por_tipo = {}
    for _, atributos in grafo.nodes(data=True):
        tipo = atributos.get("tipo", "desconocido")
        nombre = atributos.get("nombre", "")
        por_tipo.setdefault(tipo, []).append(nombre)

    lineas = []
    for tipo, nombres in sorted(por_tipo.items()):
        lineas.append(f"{tipo}:")
        for nombre in nombres:
            lineas.append(f"  - {nombre}")

    return "\n".join(lineas)


@mcp.tool()
def resumen_grafo() -> str:
    """
    Devuelve un resumen general del grafo de conocimiento:
    cantidad de entidades, relaciones, y tipos presentes.
    """
    grafo = _cargar_grafo()

    tipos = set()
    for _, atributos in grafo.nodes(data=True):
        tipos.add(atributos.get("tipo", "desconocido"))

    return (
        f"Entidades: {grafo.number_of_nodes()}\n"
        f"Relaciones: {grafo.number_of_edges()}\n"
        f"Tipos de entidad presentes: {', '.join(sorted(tipos))}"
    )


if __name__ == "__main__":
    mcp.run()