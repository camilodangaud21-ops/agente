import json

from agents.orchestrator_agent import (
    ejecutar_intencion
)


print("\n================================")
print("      ORCHESTRATOR AGENT")
print("================================")


pruebas = [

    {
        "intencion": "generar_reporte",
        "datos": {
            "paciente": "Juan Pérez"
        }
    },

    {
        "intencion": "consultar_grafo",
        "datos": {
            "entidad": "Juan Pérez"
        }
    },

    {
        "intencion": "analizar_informacion",
        "datos": {}
    },

    {
        "intencion": "procesar_imagen",
        "datos": {}
    },

    {
        "intencion": "desconocido",
        "datos": {}
    }
]


for numero, prueba in enumerate(
    pruebas,
    start=1
):

    print(
        f"\n[PRUEBA {numero}]"
    )

    resultado = ejecutar_intencion(
        prueba
    )

    print(
        json.dumps(
            resultado,
            ensure_ascii=False,
            indent=4
        )
    )