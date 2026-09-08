from agents.voice_agent import interpretar_comando


print("\n================================")
print("        VOICE AGENT")
print("================================")


texto = input(
    "\nEscribe un comando para simular la transcripción:\n> "
)


print("\n🧠 Analizando comando con Gemma...")


resultado = interpretar_comando(texto)


print("\n========== RESULTADO ==========\n")


print(
    "Intención:",
    resultado.get("intencion")
)


print(
    "\nDatos:"
)


for clave, valor in resultado.get(
    "datos",
    {}
).items():

    print(
        f"  {clave}: {valor}"
    )


print(
    "\nJSON completo:"
)


import json

print(
    json.dumps(
        resultado,
        ensure_ascii=False,
        indent=4
    )
)