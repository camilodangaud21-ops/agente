import json

from agents.orchestrator_agent import ejecutar_intencion
from agents.agent_executor import ejecutar_agente


print("\n================================")
print("       AGENT EXECUTOR")
print("================================")


intencion = {
    "intencion": "generar_reporte",
    "datos": {
        "paciente": "Juan Pérez"
    }
}


# ==========================================
# ORCHESTRATOR
# ==========================================

decision = ejecutar_intencion(
    intencion
)


print("\n🧠 Decisión del Orchestrator:")

print(
    json.dumps(
        decision,
        ensure_ascii=False,
        indent=4
    )
)


# ==========================================
# EXECUTOR
# ==========================================

resultado = ejecutar_agente(
    agente=decision["agente"],
    accion=decision["accion"],
    datos=decision["datos"]
)


print("\n🚀 Resultado del Executor:")

print(
    json.dumps(
        resultado,
        ensure_ascii=False,
        indent=4
    )
)