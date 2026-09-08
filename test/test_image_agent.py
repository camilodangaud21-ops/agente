import json

from agents.image_agent import procesar_imagen
from services.file_service import guardar_json


resultado = procesar_imagen(
    "data/input/prueba.jpg"
)

guardar_json(
    resultado,
    "data/output/imagen.json"
)

print(
    json.dumps(
        resultado,
        indent=4,
        ensure_ascii=False
    )
)

print("\nJSON guardado correctamente.")