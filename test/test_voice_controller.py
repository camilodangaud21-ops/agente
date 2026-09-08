from agents.voice_controller import (
    ejecutar_comando_voz
)


print("\n================================")
print("   ASISTENTE DE VOZ V2.0")
print("================================")

print(
    "\nWhisper se cargará una sola vez."
)


while True:

    input(
        "\nPresiona ENTER para hablar..."
    )

    try:

        resultado = ejecutar_comando_voz()

        print("\n📦 Resultado:")
        print(resultado)

    except Exception as e:

        print(
            f"\n❌ Ocurrió un error: {e}"
        )

    continuar = input(
        "\n¿Deseas dar otro comando? (s/n): "
    ).strip().lower()

    if continuar != "s":

        print(
            "\n👋 Finalizando asistente..."
        )

        break