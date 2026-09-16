"""
servidor_mcp.py

Servidor MCP (Model Context Protocol) para el grafo de conocimiento
 del proyecto.

El servidor permite que un cliente MCP consulte y actualice el
conocimiento generado por el Knowledge Agent.

Requiere:
    python -m pip install "mcp<2"

Uso:
    python servidor_mcp.py

Normalmente el servidor es iniciado automáticamente por
services/mcp_client.py mediante transporte STDIO.
"""

import json

from mcp.server.fastmcp import FastMCP

from services.graph_service import (
    cargar_json,
    construir_grafo_conocimiento,
    guardar_grafo,
)

from services.file_service import guardar_json

from config.settings import (
    KNOWLEDGE_JSON_PATH,
    GRAFO_CONOCIMIENTO_PATH,
)


mcp = FastMCP("grafo-de-conocimiento")


def _cargar_grafo():
    """Carga el conocimiento actual y construye el grafo en memoria."""
    datos = cargar_json(KNOWLEDGE_JSON_PATH)
    return construir_grafo_conocimiento(datos)


@mcp.tool()
def actualizar_conocimiento(conocimiento_json: str) -> str:
    """
    Recibe el conocimiento estructurado generado por el agente,
    lo valida de forma básica, lo guarda en knowledge.json y
    regenera el grafo GraphML.
    """
    try:
        conocimiento = json.loads(conocimiento_json)

        if not isinstance(conocimiento, dict):
            return "Error: el conocimiento debe ser un objeto JSON."

        entidades = conocimiento.get("entidades")
        relaciones = conocimiento.get("relaciones")

        if not isinstance(entidades, list) or not isinstance(relaciones, list):
            return "Error: el JSON debe contener las listas 'entidades' y 'relaciones'."

        ids = set()
        for entidad in entidades:
            if not isinstance(entidad, dict):
                return "Error: cada entidad debe ser un objeto JSON."
            entidad_id = entidad.get("id")
            nombre = entidad.get("nombre")
            tipo = entidad.get("tipo")
            if not all(isinstance(valor, str) and valor.strip() for valor in (entidad_id, nombre, tipo)):
                return "Error: cada entidad requiere id, nombre y tipo no vacíos."
            if entidad_id in ids:
                return f"Error: id de entidad duplicado: {entidad_id}."
            ids.add(entidad_id)

        for relacion in relaciones:
            if not isinstance(relacion, dict):
                return "Error: cada relación debe ser un objeto JSON."
            origen = relacion.get("origen")
            tipo_relacion = relacion.get("relacion")
            destino = relacion.get("destino")
            if not all(isinstance(valor, str) and valor.strip() for valor in (origen, tipo_relacion, destino)):
                return "Error: cada relación requiere origen, relacion y destino no vacíos."
            if origen not in ids or destino not in ids:
                return "Error: una relación referencia una entidad inexistente."

        guardar_json(conocimiento, KNOWLEDGE_JSON_PATH)
        grafo = construir_grafo_conocimiento(conocimiento)
        guardar_grafo(grafo, GRAFO_CONOCIMIENTO_PATH)

        return json.dumps(
            {
                "estado": "actualizado",
                "archivo_json": KNOWLEDGE_JSON_PATH,
                "archivo_grafo": GRAFO_CONOCIMIENTO_PATH,
                "entidades": grafo.number_of_nodes(),
                "relaciones": grafo.number_of_edges(),
            },
            ensure_ascii=False,
        )

    except json.JSONDecodeError as error:
        return f"Error: JSON inválido: {error}"
    except Exception as error:
        return f"Error al actualizar el conocimiento: {error}"


@mcp.tool()
def buscar_entidad(nombre: str) -> str:
    """Busca entidades del grafo cuyo nombre coincida parcial o totalmente."""
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
    """Devuelve las relaciones entrantes y salientes de una entidad."""
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
    """Lista todas las entidades del grafo, agrupadas por tipo."""
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
    """Devuelve cantidades de entidades, relaciones y tipos presentes."""
    grafo = _cargar_grafo()

    tipos = {
        atributos.get("tipo", "desconocido")
        for _, atributos in grafo.nodes(data=True)
    }

    return (
        f"Entidades: {grafo.number_of_nodes()}\n"
        f"Relaciones: {grafo.number_of_edges()}\n"
        f"Tipos de entidad presentes: {', '.join(sorted(tipos))}"
    )


if __name__ == "__main__":
    mcp.run()
