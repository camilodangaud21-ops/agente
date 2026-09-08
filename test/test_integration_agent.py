import json

from agents.integration_agent import integrar_informacion
from services.file_service import guardar_json


ruta_imagen = "data/output/imagen.json"
ruta_audio = "data/output/audio.json"
ruta_salida = "data/output/consolidado.json"


resultado = integrar_informacion(
    ruta_imagen,
    ruta_audio
)


guardar_json(
    resultado,
    ruta_salida
)


print("\nRESULTADO DE LA INTEGRACIÓN:\n")

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