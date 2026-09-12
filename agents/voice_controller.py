import os

from services.voice_recorder import (
    grabar_audio_mientras_enter
)

from services.whisper_service import (
    transcribir_audio
)

from agents.voice_agent import (
    interpretar_comando
)

from agents.orchestrator_agent import (
    ejecutar_intencion
)

from agents.agent_executor import (
    ejecutar_agente
)

from services.agent_result import (
    resultado_exitoso,
    resultado_error
)

from config.settings import (
    VOICE_TEMP_PATH,
    VOICE_EXIT_KEYWORDS,
    CONSOLIDADO_JSON_PATH,
    IMAGEN_JSON_PATH,
    AUDIO_JSON_PATH,
    DEFAULT_IMAGE_INPUT,
    DEFAULT_AUDIO_INPUT
)


# ==========================================
# VALIDACIÓN PREVIA A LA EJECUCIÓN
# ==========================================

def _archivos_requeridos(agente: str, datos: dict):
    """
    Indica qué archivos necesita el agente para poder ejecutar
    la acción, según lo que realmente usa agent_executor.py.

    Devuelve una lista de rutas. Una acción puede depender de
    uno o varios archivos.
    """

    if agente == "integration_agent":
        return [
            IMAGEN_JSON_PATH,
            AUDIO_JSON_PATH
        ]

    if agente in ("report_agent", "graph_agent", "knowledge_agent"):
        return [CONSOLIDADO_JSON_PATH]

    if agente == "image_agent":
        return [datos.get("ruta", DEFAULT_IMAGE_INPUT)]

    if agente == "audio_agent":
        return [datos.get("ruta", DEFAULT_AUDIO_INPUT)]

    return []


def _confirmar_ejecucion(agente: str, accion: str, archivos_requeridos) -> bool:
    """
    Muestra un resumen de la acción que está por ejecutarse
    y pide confirmación explícita antes de continuar.

    Devuelve True solo si el usuario confirma explícitamente
    con "s" o "si". Cualquier otra respuesta (incluida una
    respuesta vacía o ambigua) se trata como "no", por
    seguridad.
    """

    print("\n================================")
    print("     CONFIRMACIÓN REQUERIDA")
    print("================================")
    print(f"Agente a ejecutar : {agente}")
    print(f"Acción            : {accion}")

    if archivos_requeridos:
        print("Archivos necesarios:")
        for archivo in archivos_requeridos:
            print(f"  - {archivo} (encontrado ✅)")

    respuesta = input(
        "\n¿Deseás continuar? [s = sí / n = no]: "
    ).strip().lower()

    return respuesta in ("s", "si", "sí")


def ejecutar_comando_voz():
    """
    Ejecuta el flujo completo de voz:

    Micrófono (push-to-talk: mantener ENTER)
        ↓
    Whisper
        ↓
    Voice Agent
        ↓
    Orchestrator
        ↓
    Agent Executor
    """

    print("\n================================")
    print("       VOICE CONTROLLER")
    print("================================")

    # ==========================================
    # 1. GRABAR
    # ==========================================

    print("\n🎙️ Paso 1/5 - Escuchando comando...")

    grabar_audio_mientras_enter(
        ruta_salida=VOICE_TEMP_PATH
    )

    # ==========================================
    # 2. TRANSCRIBIR
    # ==========================================

    print("\n🧠 Paso 2/5 - Procesando voz...")

    texto = transcribir_audio(
        ruta_audio=VOICE_TEMP_PATH,
        idioma="es"
    )

    print("\n📝 Transcripción:")
    print("--------------------------------")
    print(texto)
    print("--------------------------------")

    if not texto:
        raise ValueError(
            "Whisper no detectó ningún texto."
        )

    # ==========================================
    # 2.5 DETECCIÓN TEMPRANA DE SALIDA
    # ==========================================
    #
    # Si el usuario pidió salir, se corta el flujo aquí mismo:
    # no tiene sentido gastar una consulta a Gemma solo para
    # interpretar una intención de cierre.

    if texto.strip().lower() in VOICE_EXIT_KEYWORDS:

        print("\n👋 Comando de salida detectado.")

        return resultado_exitoso(
            agente=None,
            accion="salir",
            datos={},
            resultado="El usuario solicitó finalizar el programa."
        )

    # ==========================================
    # 3. VOICE AGENT
    # ==========================================

    print("\n🤖 Paso 3/5 - Analizando intención...")

    intencion = interpretar_comando(
        texto
    )

    print("\n🎯 Intención detectada:")
    print(intencion)

    # ==========================================
    # 4. ORCHESTRATOR
    # ==========================================

    print("\n🧠 Paso 4/5 - Orquestando...")

    decision = ejecutar_intencion(
        intencion
    )

    print("\n🚦 Decisión:")
    print(decision)

    # ==========================================
    # 4.5 VALIDACIÓN: ¿EXISTEN LOS ARCHIVOS NECESARIOS?
    # ==========================================

    archivos_requeridos = _archivos_requeridos(
        decision["agente"],
        decision["datos"]
    )

    archivos_faltantes = [
        archivo
        for archivo in archivos_requeridos
        if not os.path.exists(archivo)
    ]

    if archivos_faltantes:

        print("\n❌ No se puede continuar: faltan archivos requeridos:")
        for archivo in archivos_faltantes:
            print(f"  - {archivo}")

        return resultado_error(
            agente=decision["agente"],
            accion=decision["accion"],
            error=(
                "No se encontraron los archivos requeridos: "
                + ", ".join(archivos_faltantes)
            ),
            datos=decision["datos"]
        )

    # ==========================================
    # 4.6 CONFIRMACIÓN EXPLÍCITA DEL USUARIO
    # ==========================================

    if not _confirmar_ejecucion(
        decision["agente"],
        decision["accion"],
        archivos_requeridos
    ):

        print("\n🚫 Operación cancelada por el usuario.")

        return resultado_error(
            agente=decision["agente"],
            accion=decision["accion"],
            error="El usuario canceló la operación.",
            datos=decision["datos"]
        )

    # ==========================================
    # 5. EXECUTOR
    # ==========================================

    print("\n⚙️ Paso 5/5 - Ejecutando agente...")

    resultado_final = ejecutar_agente(
        agente=decision["agente"],
        accion=decision["accion"],
        datos=decision["datos"]
    )

    print("\n================================")
    print("       RESULTADO FINAL")
    print("================================")

    print(resultado_final)

    return resultado_final
