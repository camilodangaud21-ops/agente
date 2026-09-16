"""Cliente MCP local para conectar el agente con servidor MCP por STDIO."""

import asyncio
import json
import sys
from pathlib import Path
from typing import Any, Dict

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


PROJECT_ROOT = Path(__file__).resolve().parent.parent
MCP_SERVER_PATH = PROJECT_ROOT / "servidor_mcp.py"


async def _llamar_herramienta(nombre: str, argumentos: Dict[str, Any]) -> str:
    """Inicia el servidor MCP local, ejecuta una herramienta y devuelve su texto."""
    server_params = StdioServerParameters(
        command=sys.executable,
        args=[str(MCP_SERVER_PATH)],
        env=None,
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            resultado = await session.call_tool(nombre, argumentos)

            textos = []
            for contenido in resultado.content:
                if hasattr(contenido, "text"):
                    textos.append(contenido.text)

            if resultado.isError:
                raise RuntimeError("; ".join(textos) or "El servidor MCP devolvió un error.")

            return "\n".join(textos)


def actualizar_conocimiento(conocimiento: Dict[str, Any]) -> Dict[str, Any]:
    """
    Envía el conocimiento generado por Knowledge Agent al servidor MCP.

    El servidor MCP es responsable de persistir knowledge.json y regenerar
    el grafo GraphML. Esto hace explícita la conexión Agente -> MCP -> Grafo.
    """
    respuesta = asyncio.run(
        _llamar_herramienta(
            "actualizar_conocimiento",
            {
                "conocimiento_json": json.dumps(
                    conocimiento,
                    ensure_ascii=False,
                )
            },
        )
    )

    try:
        return json.loads(respuesta)
    except json.JSONDecodeError as error:
        raise RuntimeError(f"Respuesta inválida del servidor MCP: {respuesta}") from error


def consultar_mcp(nombre_herramienta: str, argumentos: Dict[str, Any] | None = None) -> str:
    """Permite consultar una herramienta MCP desde código Python síncrono."""
    return asyncio.run(
        _llamar_herramienta(nombre_herramienta, argumentos or {})
    )
