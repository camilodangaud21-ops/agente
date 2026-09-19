"""
servidor_mcp.py

Servidor MCP local del proyecto usando la API de bajo nivel de MCP.

Esta implementación mantiene las mismas herramientas públicas del servidor
anterior, pero evita FastMCP para reducir dependencias y aislar problemas
relacionados con FastMCP/Pydantic Settings.

Uso normal:
    services/mcp_client.py inicia este archivo automáticamente por STDIO.
"""

import json
from typing import Any

import mcp.types as types
from mcp.server.lowlevel.server import Server
from mcp.server.stdio import stdio_server

from config.settings import (
    GRAFO_CONOCIMIENTO_PATH,
    KNOWLEDGE_JSON_PATH,
)
from services.file_service import guardar_json
from services.graph_service import (
    cargar_json,
    construir_grafo_conocimiento,
    guardar_grafo,
)


SERVER_NAME = "grafo-de-conocimiento"

server = Server(SERVER_NAME)


def _cargar_grafo():
    """Carga el conocimiento actual y construye el grafo en memoria."""
    datos = cargar_json(KNOWLEDGE_JSON_PATH)
    return construir_grafo_conocimiento(datos)


def _resultado(texto: str, error: bool = False) -> types.CallToolResult:
    """Construye una respuesta MCP de texto."""
    return types.CallToolResult(
        content=[
            types.TextContent(
                type="text",
                text=texto,
            )
        ],
        isError=error,
    )


def _validar_conocimiento(conocimiento: Any) -> tuple[str | None, list, list]:
    """Valida la estructura mínima esperada por el grafo."""
    if not isinstance(conocimiento, dict):
        return "El conocimiento debe ser un objeto JSON.", [], []

    entidades = conocimiento.get("entidades")
    relaciones = conocimiento.get("relaciones")

    if not isinstance(entidades, list) or not isinstance(relaciones, list):
        return (
            "El JSON debe contener las listas 'entidades' y 'relaciones'.",
            [],
            [],
        )

    ids = set()

    for entidad in entidades:
        if not isinstance(entidad, dict):
            return "Cada entidad debe ser un objeto JSON.", [], []

        entidad_id = entidad.get("id")
        nombre = entidad.get("nombre")
        tipo = entidad.get("tipo")

        if not all(
            isinstance(valor, str) and valor.strip()
            for valor in (entidad_id, nombre, tipo)
        ):
            return (
                "Cada entidad requiere id, nombre y tipo no vacíos.",
                [],
                [],
            )

        if entidad_id in ids:
            return f"Id de entidad duplicado: {entidad_id}.", [], []

        ids.add(entidad_id)

    for relacion in relaciones:
        if not isinstance(relacion, dict):
            return "Cada relación debe ser un objeto JSON.", [], []

        origen = relacion.get("origen")
        tipo_relacion = relacion.get("relacion")
        destino = relacion.get("destino")

        if not all(
            isinstance(valor, str) and valor.strip()
            for valor in (origen, tipo_relacion, destino)
        ):
            return (
                "Cada relación requiere origen, relacion y destino no vacíos.",
                [],
                [],
            )

        if origen not in ids or destino not in ids:
            return (
                "Una relación referencia una entidad inexistente.",
                [],
                [],
            )

    return None, entidades, relaciones


def _actualizar_conocimiento(conocimiento_json: str) -> str:
    """Valida y persiste el conocimiento recibido."""
    try:
        conocimiento = json.loads(conocimiento_json)
    except json.JSONDecodeError as error:
        return json.dumps(
            {
                "estado": "error",
                "error": f"JSON inválido: {error}",
            },
            ensure_ascii=False,
        )

    error, entidades, relaciones = _validar_conocimiento(conocimiento)

    if error:
        return json.dumps(
            {
                "estado": "error",
                "error": error,
            },
            ensure_ascii=False,
        )

    try:
        guardar_json(conocimiento, KNOWLEDGE_JSON_PATH)

        grafo = construir_grafo_conocimiento(conocimiento)
        guardar_grafo(grafo, GRAFO_CONOCIMIENTO_PATH)

        return json.dumps(
            {
                "estado": "actualizado",
                "archivo_json": KNOWLEDGE_JSON_PATH,
                "archivo_grafo": GRAFO_CONOCIMIENTO_PATH,
                "entidades": len(entidades),
                "relaciones": len(relaciones),
            },
            ensure_ascii=False,
        )
    except Exception as error:
        return json.dumps(
            {
                "estado": "error",
                "error": f"Error al guardar el conocimiento: {error}",
            },
            ensure_ascii=False,
        )


def _buscar_entidad(nombre: str) -> str:
    """Busca entidades por coincidencia parcial de nombre."""
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


def _relaciones_de(nombre_entidad: str) -> str:
    """Devuelve relaciones entrantes y salientes de una entidad."""
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

    for _, destino_id, datos_arista in grafo.out_edges(
        nodo_id,
        data=True,
    ):
        relacion = datos_arista.get("relacion", "relacionado con")
        nombre_destino = grafo.nodes[destino_id].get(
            "nombre",
            str(destino_id),
        )
        lineas.append(
            f"{nombre_entidad} --{relacion}--> {nombre_destino}"
        )

    for origen_id, _, datos_arista in grafo.in_edges(
        nodo_id,
        data=True,
    ):
        relacion = datos_arista.get("relacion", "relacionado con")
        nombre_origen = grafo.nodes[origen_id].get(
            "nombre",
            str(origen_id),
        )
        lineas.append(
            f"{nombre_origen} --{relacion}--> {nombre_entidad}"
        )

    if not lineas:
        return f"'{nombre_entidad}' no tiene relaciones registradas."

    return "\n".join(lineas)


def _listar_entidades() -> str:
    """Lista las entidades del grafo agrupadas por tipo."""
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


def _resumen_grafo() -> str:
    """Devuelve cantidades de entidades, relaciones y tipos."""
    grafo = _cargar_grafo()

    tipos = {
        atributos.get("tipo", "desconocido")
        for _, atributos in grafo.nodes(data=True)
    }

    tipos_texto = ", ".join(sorted(tipos)) if tipos else "ninguno"

    return (
        f"Entidades: {grafo.number_of_nodes()}\n"
        f"Relaciones: {grafo.number_of_edges()}\n"
        f"Tipos de entidad presentes: {tipos_texto}"
    )


TOOLS = [
    types.Tool(
        name="actualizar_conocimiento",
        description=(
            "Recibe conocimiento estructurado, lo valida, guarda "
            "knowledge.json y regenera el grafo GraphML."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "conocimiento_json": {
                    "type": "string",
                    "description": "Conocimiento estructurado serializado como JSON.",
                }
            },
            "required": ["conocimiento_json"],
        },
    ),
    types.Tool(
        name="buscar_entidad",
        description="Busca entidades del grafo por nombre parcial o completo.",
        inputSchema={
            "type": "object",
            "properties": {
                "nombre": {
                    "type": "string",
                    "description": "Nombre o parte del nombre de la entidad.",
                }
            },
            "required": ["nombre"],
        },
    ),
    types.Tool(
        name="relaciones_de",
        description="Devuelve las relaciones entrantes y salientes de una entidad.",
        inputSchema={
            "type": "object",
            "properties": {
                "nombre_entidad": {
                    "type": "string",
                    "description": "Id o nombre exacto de la entidad.",
                }
            },
            "required": ["nombre_entidad"],
        },
    ),
    types.Tool(
        name="listar_entidades",
        description="Lista todas las entidades del grafo agrupadas por tipo.",
        inputSchema={
            "type": "object",
            "properties": {},
        },
    ),
    types.Tool(
        name="resumen_grafo",
        description="Devuelve cantidades de entidades, relaciones y tipos presentes.",
        inputSchema={
            "type": "object",
            "properties": {},
        },
    ),
]


async def _listar_herramientas(
    ctx,
    params,
) -> types.ListToolsResult:
    """Devuelve las herramientas disponibles en el servidor."""
    return types.ListToolsResult(tools=TOOLS)


async def _llamar_herramienta(
    ctx,
    params: types.CallToolRequestParams,
) -> types.CallToolResult:
    """Ejecuta una herramienta MCP por nombre."""
    nombre = params.name
    argumentos = params.arguments or {}

    try:
        if nombre == "actualizar_conocimiento":
            conocimiento_json = argumentos.get("conocimiento_json")

            if not isinstance(conocimiento_json, str):
                return _resultado(
                    "El argumento 'conocimiento_json' es obligatorio y debe ser texto.",
                    error=True,
                )

            return _resultado(_actualizar_conocimiento(conocimiento_json))

        if nombre == "buscar_entidad":
            nombre_entidad = argumentos.get("nombre")

            if not isinstance(nombre_entidad, str):
                return _resultado(
                    "El argumento 'nombre' es obligatorio y debe ser texto.",
                    error=True,
                )

            return _resultado(_buscar_entidad(nombre_entidad))

        if nombre == "relaciones_de":
            nombre_entidad = argumentos.get("nombre_entidad")

            if not isinstance(nombre_entidad, str):
                return _resultado(
                    "El argumento 'nombre_entidad' es obligatorio y debe ser texto.",
                    error=True,
                )

            return _resultado(_relaciones_de(nombre_entidad))

        if nombre == "listar_entidades":
            return _resultado(_listar_entidades())

        if nombre == "resumen_grafo":
            return _resultado(_resumen_grafo())

        return _resultado(
            f"Herramienta MCP desconocida: {nombre}",
            error=True,
        )

    except Exception as error:
        return _resultado(
            f"Error al ejecutar '{nombre}': {error}",
            error=True,
        )


server = Server(
    SERVER_NAME,
    on_list_tools=_listar_herramientas,
    on_call_tool=_llamar_herramienta,
)


async def main():
    """Ejecuta el servidor MCP usando STDIO."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
