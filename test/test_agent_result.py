from services.agent_result import (
    resultado_exitoso,
    resultado_error,
    resultado_pendiente
)


print("\n================================")
print("      TEST AGENT RESULT")
print("================================")


print("\n[1] ÉXITO")

print(
    resultado_exitoso(
        "report_agent",
        "generar_reporte",
        {
            "paciente": "Juan Pérez"
        },
        {
            "archivo": "informe.pdf"
        }
    )
)


print("\n[2] ERROR")

print(
    resultado_error(
        "report_agent",
        "generar_reporte",
        "No se encontró el archivo."
    )
)


print("\n[3] PENDIENTE")

print(
    resultado_pendiente(
        "report_agent",
        "generar_reporte"
    )
)