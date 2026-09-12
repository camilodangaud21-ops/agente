from unittest.mock import patch

from agents.agent_executor import ejecutar_agente
from agents.orchestrator_agent import ejecutar_intencion
from agents.voice_agent import _detectar_categoria_probable
from agents.voice_controller import _archivos_requeridos

from config.settings import (
    AUDIO_JSON_PATH,
    CONSOLIDADO_JSON_PATH,
    IMAGEN_JSON_PATH
)


def test_voice_agent_detects_integration_intent():
    assert _detectar_categoria_probable(
        "integra la imagen y el audio"
    ) == "integrar_informacion"


def test_orchestrator_routes_integration_agent():
    decision = ejecutar_intencion({
        "intencion": "integrar_informacion",
        "datos": {}
    })

    assert decision == {
        "agente": "integration_agent",
        "accion": "integrar_informacion",
        "datos": {}
    }


def test_voice_controller_requires_image_and_audio_json():
    archivos = _archivos_requeridos(
        "integration_agent",
        {}
    )

    assert archivos == [
        IMAGEN_JSON_PATH,
        AUDIO_JSON_PATH
    ]


def test_integration_executor_saves_consolidated_json():
    resultado_integracion = {
        "fuentes": ["imagen", "audio"],
        "resumen_integrado": "Información integrada",
        "coincidencias": [],
        "informacion_exclusiva": {
            "imagen": [],
            "audio": []
        },
        "posibles_contradicciones": [],
        "datos_consolidados": {},
        "nivel_confianza": "alta"
    }

    with patch(
        "agents.agent_executor.integrar_informacion",
        return_value=resultado_integracion
    ) as integrar_mock, patch(
        "agents.agent_executor.guardar_json"
    ) as guardar_mock:
        resultado = ejecutar_agente(
            agente="integration_agent",
            accion="integrar_informacion",
            datos={}
        )

    integrar_mock.assert_called_once_with(
        IMAGEN_JSON_PATH,
        AUDIO_JSON_PATH
    )
    guardar_mock.assert_called_once_with(
        resultado_integracion,
        CONSOLIDADO_JSON_PATH
    )
    assert resultado["completado"] is True
    assert resultado["resultado"]["archivo"] == CONSOLIDADO_JSON_PATH
