import json

import servidor_mcp


def test_mcp_expone_herramienta_de_actualizacion():
    herramientas = servidor_mcp.mcp._tool_manager._tools
    assert "actualizar_conocimiento" in herramientas
    assert "buscar_entidad" in herramientas
    assert "relaciones_de" in herramientas


def test_actualizar_conocimiento_rechaza_relacion_sin_entidad():
    conocimiento = {
        "entidades": [
            {"id": "a", "nombre": "A", "tipo": "persona"}
        ],
        "relaciones": [
            {"origen": "a", "relacion": "conoce", "destino": "b"}
        ]
    }

    resultado = servidor_mcp.actualizar_conocimiento(
        json.dumps(conocimiento, ensure_ascii=False)
    )

    assert resultado.startswith("Error:")
    assert "entidad inexistente" in resultado


def test_mcp_herramientas_tienen_docstrings():
    herramientas = servidor_mcp.mcp._tool_manager._tools
    assert herramientas["actualizar_conocimiento"].fn.__doc__
    assert herramientas["buscar_entidad"].fn.__doc__
    assert herramientas["relaciones_de"].fn.__doc__
