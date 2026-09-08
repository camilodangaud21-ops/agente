from typing import Any, Optional


def resultado_exitoso(
    agente: str,
    accion: str,
    datos: Optional[dict] = None,
    resultado: Any = None
) -> dict:
    """
    Construye una respuesta estándar para una ejecución exitosa.
    """

    return {
        "estado": "completado",
        "agente": agente,
        "accion": accion,
        "datos": datos or {},
        "resultado": resultado,
        "error": None
    }


def resultado_error(
    agente: str,
    accion: str,
    error: str,
    datos: Optional[dict] = None
) -> dict:
    """
    Construye una respuesta estándar para una ejecución fallida.
    """

    return {
        "estado": "error",
        "agente": agente,
        "accion": accion,
        "datos": datos or {},
        "resultado": None,
        "error": error
    }


def resultado_pendiente(
    agente: str,
    accion: str,
    datos: Optional[dict] = None
) -> dict:
    """
    Construye una respuesta estándar para una acción pendiente.
    """

    return {
        "estado": "pendiente",
        "agente": agente,
        "accion": accion,
        "datos": datos or {},
        "resultado": None,
        "error": None
    }