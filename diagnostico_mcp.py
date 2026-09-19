"""
diagnostico_timeout.py

Igual que diagnostico_mcp.py, pero con un límite de tiempo (timeout)
para que actualizar_conocimiento falle rápido en vez de colgarse
indefinidamente, y así ver el error real.

Uso:
    python diagnostico_timeout.py
"""
import asyncio
import json
import sys
import time
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

PROJECT_ROOT = Path(__file__).resolve().parent
MCP_SERVER_PATH = PROJECT_ROOT / "servidor_mcp.py"
LOG_STDERR_PATH = PROJECT_ROOT / "servidor_mcp_stderr.log"


async def probar_con_timeout(nombre_herramienta, argumentos, segundos=15):
    server_params = StdioServerParameters(
        command=sys.executable,
        args=[str(MCP_SERVER_PATH)],
        env=None,
    )

    inicio = time.time()

    with open(LOG_STDERR_PATH, "w", encoding="utf-8") as log_stderr:
        async with stdio_client(server_params, errlog=log_stderr) as (read, write):
            async with ClientSession(read, write) as session:
                print("  Inicializando sesión...")
                await asyncio.wait_for(session.initialize(), timeout=segundos)
                print(f"  Sesión inicializada ({time.time() - inicio:.2f}s). Llamando herramienta...")

                resultado = await asyncio.wait_for(
                    session.call_tool(nombre_herramienta, argumentos),
                    timeout=segundos
                )

                duracion = time.time() - inicio
                print(f"  Herramienta respondió en {duracion:.2f}s")

                textos = [c.text for c in resultado.content if hasattr(c, "text")]
                return "\n".join(textos)


async def main():
    print("=== Prueba: actualizar_conocimiento (con timeout de 15s) ===")

    conocimiento_prueba = {
        "entidades": [
            {"id": "T1", "nombre": "Prueba Diagnostico", "tipo": "test"}
        ],
        "relaciones": []
    }

    try:
        resultado = await probar_con_timeout(
            "actualizar_conocimiento",
            {"conocimiento_json": json.dumps(conocimiento_prueba, ensure_ascii=False)},
            segundos=15
        )
        print(f"\n[OK]\n{resultado}")
    except asyncio.TimeoutError:
        print("\n[TIMEOUT] La llamada no respondió dentro de 15 segundos.")
        print("El problema está confirmado en el transporte MCP para esta herramienta específica.")
    except Exception as e:
        print(f"\n[ERROR] {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

    print("\n=== STDERR DEL SERVIDOR (servidor_mcp_stderr.log) ===")
    try:
        with open(LOG_STDERR_PATH, "r", encoding="utf-8") as f:
            contenido = f.read()
            print(contenido if contenido.strip() else "(vacío)")
    except FileNotFoundError:
        print("(no se generó el archivo de log)")


if __name__ == "__main__":
    asyncio.run(main())