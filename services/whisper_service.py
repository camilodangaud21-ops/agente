try:
    import whisper
except Exception as exc:  # pragma: no cover - depends on the local native stack
    whisper = None
    _WHISPER_IMPORT_ERROR = exc
else:
    _WHISPER_IMPORT_ERROR = None

from config.settings import (
    WHISPER_MODEL,
    WHISPER_LANGUAGE,
    WHISPER_FP16
)


_modelo = None


def obtener_modelo():

    global _modelo

    if whisper is None:
        raise RuntimeError(
            "Whisper no está disponible en este entorno. "
            "La librería nativa de Whisper/Numba falló al cargar. "
            "Recrea el entorno con Python 3.11/3.12 o reinstala Whisper."
        ) from _WHISPER_IMPORT_ERROR

    if _modelo is None:

        print(
            f"\n🧠 Cargando Whisper ({WHISPER_MODEL})..."
        )

        _modelo = whisper.load_model(
            WHISPER_MODEL
        )

        print(
            "✅ Whisper cargado correctamente."
        )

    return _modelo


def transcribir_audio(
    ruta_audio: str,
    idioma: str = WHISPER_LANGUAGE
) -> str:

    modelo = obtener_modelo()

    print(
        "\n🎧 Transcribiendo audio..."
    )

    resultado = modelo.transcribe(
        ruta_audio,
        language=idioma,
        fp16=WHISPER_FP16
    )

    return resultado["text"].strip()