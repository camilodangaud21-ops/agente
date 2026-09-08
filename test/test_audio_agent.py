import json

from agents.audio_agent import procesar_audio
from services.file_service import guardar_json


ruta_audio = "data/input/prueba.mp3"
ruta_salida = "data/output/audio.json"


resultado = procesar_audio(ruta_audio)


guardar_json(
    resultado,
    ruta_salida
)


print("\nRESULTADO DEL ANÁLISIS:\n")

print(
    json.dumps(
        resultado,
        indent=4,
        ensure_ascii=False
    )
)

print(
    f"\nJSON guardado correctamente en: {ruta_salida}"
)