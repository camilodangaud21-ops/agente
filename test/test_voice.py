import os

import whisper

from services.voice_recorder import (
    grabar_audio_hasta_silencio
)


RUTA_AUDIO = "data/temp/voz_actual.wav"


print("\n================================")
print("       PRUEBA DE VOZ")
print("================================")


input(
    "\nPresiona ENTER para comenzar la grabación..."
)


# ==========================================
# 1. GRABAR
# ==========================================

print("\n🎙️ Grabando...")

ruta = grabar_audio_hasta_silencio(
    RUTA_AUDIO
)


# ==========================================
# 2. CARGAR WHISPER
# ==========================================

print("\n🧠 Cargando Whisper...")

modelo = whisper.load_model(
    "base"
)


# ==========================================
# 3. TRANSCRIBIR
# ==========================================

print("\n[1/2] Transcribiendo audio...")

resultado = modelo.transcribe(
    ruta,
    language="es"
)


texto = resultado["text"].strip()


# ==========================================
# 4. MOSTRAR
# ==========================================

print("\n[2/2] Transcripción obtenida:")
print("--------------------------------")
print(texto)
print("--------------------------------")


# ==========================================
# 5. INFORMACIÓN
# ==========================================

if os.path.exists(ruta):

    tamaño = os.path.getsize(ruta)

    print(
        f"\n✅ Audio almacenado correctamente."
    )

    print(
        f"📁 Ruta: {ruta}"
    )

    print(
        f"📦 Tamaño: {tamaño / 1024:.2f} KB"
    )