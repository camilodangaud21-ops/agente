import os
import queue

import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write
from config.settings import (
    VOICE_SAMPLE_RATE,
    VOICE_CHANNELS,
    VOICE_BLOCK_SIZE,
    VOICE_SILENCE_THRESHOLD,
    VOICE_SILENCE_DURATION,
    VOICE_MAX_DURATION,
    VOICE_PREFERRED_INPUT_TOKENS,
    VOICE_EXCLUDED_INPUT_TOKENS
)


def _seleccionar_dispositivo_entrada():
    """
    Elige el dispositivo de entrada de audio a utilizar.

    1. Si `VOICE_PREFERRED_INPUT_TOKENS` tiene algún valor en
       config/settings.py, se prioriza el primer dispositivo de
       entrada cuyo nombre contenga alguno de esos fragmentos
       (por ejemplo, unos auriculares específicos).
    2. Si no hay preferencia configurada (o no se encuentra),
       se elige el primer dispositivo de entrada real, evitando
       los que suelen ser virtuales o de solo salida.
    3. Como último recurso, cualquier dispositivo con canales
       de entrada disponibles.
    """
    try:
        dispositivos = sd.query_devices()
    except Exception:
        return None

    if dispositivos is None:
        return None

    if VOICE_PREFERRED_INPUT_TOKENS:

        for indice, dispositivo in enumerate(dispositivos):
            if not isinstance(dispositivo, dict):
                continue

            nombre = str(dispositivo.get("name", "")).lower()
            canales = int(dispositivo.get("max_input_channels", 0) or 0)

            if canales <= 0:
                continue

            if any(token in nombre for token in VOICE_PREFERRED_INPUT_TOKENS):
                return indice

    for indice, dispositivo in enumerate(dispositivos):
        if not isinstance(dispositivo, dict):
            continue

        nombre = str(dispositivo.get("name", "")).lower()
        canales = int(dispositivo.get("max_input_channels", 0) or 0)

        if canales <= 0:
            continue

        if any(token in nombre for token in VOICE_EXCLUDED_INPUT_TOKENS):
            continue

        return indice

    for indice, dispositivo in enumerate(dispositivos):
        if not isinstance(dispositivo, dict):
            continue

        canales = int(dispositivo.get("max_input_channels", 0) or 0)
        if canales > 0:
            return indice

    return None


def grabar_audio_hasta_silencio(
    ruta_salida: str,
    samplerate: int = VOICE_SAMPLE_RATE,
    canales: int = VOICE_CHANNELS,
    bloque: int = VOICE_BLOCK_SIZE,
    umbral_silencio: float = VOICE_SILENCE_THRESHOLD,
    silencio_maximo: float = VOICE_SILENCE_DURATION,
    tiempo_maximo: float = VOICE_MAX_DURATION
):
    """
    Graba audio hasta detectar silencio después
    de que el usuario haya comenzado a hablar.

    Parámetros:
    - umbral_silencio: sensibilidad para detectar sonido.
    - silencio_maximo: segundos de silencio antes de detener.
    - tiempo_maximo: límite de seguridad de grabación.
    """

    print("\n🎙️ Preparando micrófono...")
    print("🎤 Habla cuando estés listo...")

    os.makedirs(
        os.path.dirname(ruta_salida),
        exist_ok=True
    )

    cola_audio = queue.Queue()
    fragmentos = []

    usuario_hablo = False
    bloques_silencio = 0

    bloques_necesarios_silencio = int(
        (silencio_maximo * samplerate) / bloque
    )

    bloques_maximos = int(
        (tiempo_maximo * samplerate) / bloque
    )

    def callback(
        indata,
        frames,
        time,
        status
    ):
        if status:
            print(f"⚠️ Audio: {status}")

        cola_audio.put(
            indata.copy()
        )

    print("\n🎙️ Escuchando...")

    dispositivo_entrada = _seleccionar_dispositivo_entrada()
    if dispositivo_entrada is not None:
        print(f"📻 Micrófono seleccionado: índice {dispositivo_entrada}")

    with sd.InputStream(
        samplerate=samplerate,
        channels=canales,
        blocksize=bloque,
        device=dispositivo_entrada,
        callback=callback
    ):

        for _ in range(bloques_maximos):

            datos = cola_audio.get()

            volumen = np.linalg.norm(
                datos
            )

            fragmentos.append(
                datos
            )

            if volumen > umbral_silencio:

                if not usuario_hablo:

                    print(
                        "🗣️ Voz detectada..."
                    )

                    usuario_hablo = True

                bloques_silencio = 0

            elif usuario_hablo:

                bloques_silencio += 1

                if (
                    bloques_silencio
                    >= bloques_necesarios_silencio
                ):

                    print(
                        "🔇 Silencio detectado."
                    )

                    break

    if not usuario_hablo:

        raise ValueError(
            "No se detectó ninguna voz."
        )

    audio_final = np.concatenate(
        fragmentos,
        axis=0
    )

    write(
        ruta_salida,
        samplerate,
        audio_final
    )

    print(
        "✅ Grabación finalizada."
    )

    print(
        f"📁 Archivo: {ruta_salida}"
    )

    return ruta_salida