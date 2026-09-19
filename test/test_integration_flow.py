from unittest.mock import patch

from agents.agent_executor import ejecutar_agente
from agents.orchestrator_agent import ejecutar_intencion
from agents.voice_agent import _detectar_categoria_probable
from agents.voice_controller import _archivos_requeridos

from config.settings import (
    AUDIO_JSON_PATH,
    CONSOLIDADO_JSON_PATH,
    DEFAULT_AUDIO_INPUT,
    DEFAULT_IMAGE_INPUT,
    IMAGEN_JSON_PATH
)


def test_voice_agent_detects_integration_intent():
    assert _detectar_categoria_probable(
        "integra la imagen y el audio"
    ) == "integrar_informacion"


def test_voice_agent_detects_complete_workflow_intent():
    assert _detectar_categoria_probable(
        "procesa toda la información y genera el conocimiento"
    ) == "procesar_informacion_completa"


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


def test_orchestrator_routes_complete_workflow():
    decision = ejecutar_intencion({
        "intencion": "procesar_informacion_completa",
        "datos": {}
    })

    assert decision == {
        "agente": "workflow_agent",
        "accion": "procesar_informacion_completa",
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


def test_voice_controller_requires_raw_inputs_for_complete_workflow():
    archivos = _archivos_requeridos(
        "workflow_agent",
        {}
    )

    assert archivos == [
        DEFAULT_IMAGE_INPUT,
        DEFAULT_AUDIO_INPUT
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
    assert resultado["estado"] == "completado"


def test_complete_workflow_orchestrates_all_stages():
    resultado_imagen = {"texto": "imagen procesada"}
    resultado_audio = {"texto": "audio procesado"}
    resultado_integracion = {
        "fuentes": ["imagen", "audio"],
        "datos_consolidados": {}
    }
    conocimiento = {
        "entidades": [
            {"id": "e1", "nombre": "Entidad 1", "tipo": "tema"}
        ],
        "relaciones": []
    }

    class FakeGraph:
        def number_of_nodes(self):
            return 1

        def number_of_edges(self):
            return 0

    with patch(
        "agents.agent_executor.procesar_imagen",
        return_value=resultado_imagen
    ) as imagen_mock, patch(
        "agents.agent_executor.procesar_audio",
        return_value=resultado_audio
    ) as audio_mock, patch(
        "agents.agent_executor.integrar_informacion",
        return_value=resultado_integracion
    ) as integrar_mock, patch(
        "agents.agent_executor.extraer_conocimiento",
        return_value=conocimiento
    ) as conocimiento_mock, patch(
        "agents.agent_executor.cargar_json",
        return_value=resultado_integracion
    ), patch(
        "agents.agent_executor.guardar_json"
    ) as guardar_mock, patch(
        "agents.agent_executor.construir_grafo_conocimiento",
        return_value=FakeGraph()
    ) as grafo_mock, patch(
        "agents.agent_executor.guardar_grafo"
    ) as guardar_grafo_mock, patch(
        "agents.agent_executor.exportar_a_obsidian"
    ) as obsidian_mock:
        resultado = ejecutar_agente(
            agente="workflow_agent",
            accion="procesar_informacion_completa",
            datos={}
        )

    imagen_mock.assert_called_once_with(DEFAULT_IMAGE_INPUT)
    audio_mock.assert_called_once_with(DEFAULT_AUDIO_INPUT)
    integrar_mock.assert_called_once_with(
        IMAGEN_JSON_PATH,
        AUDIO_JSON_PATH
    )
    conocimiento_mock.assert_called_once_with(resultado_integracion)
    guardar_mock.assert_any_call(resultado_integracion, CONSOLIDADO_JSON_PATH)
    grafo_mock.assert_called_once_with(conocimiento)
    guardar_grafo_mock.assert_called_once()
    obsidian_mock.assert_called_once()

    assert resultado["estado"] == "completado"
    assert resultado["resultado"]["consolidado"] == CONSOLIDADO_JSON_PATH
