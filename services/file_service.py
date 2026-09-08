import json
import os


def guardar_json(datos: dict, ruta: str):
    """
    Guarda un diccionario en formato JSON.
    """

    carpeta = os.path.dirname(ruta)

    if carpeta:
        os.makedirs(
            carpeta,
            exist_ok=True
        )

    with open(
        ruta,
        "w",
        encoding="utf-8"
    ) as archivo:

        json.dump(
            datos,
            archivo,
            indent=4,
            ensure_ascii=False
        )