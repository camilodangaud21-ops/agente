from agents.voice_controller import ejecutar_comando_voz


def mostrar_banner():

    print("==============================================")
    print("        Sistema multimodal con agentes de IA")
    print("==============================================")


def main():

    mostrar_banner()

    print("\n🎤 Modo asistente de voz")
    print("Habla para indicarle al sistema qué deseas hacer.")
    print("Di 'Salir' para finalizar.\n")

    while True:

        try:

            resultado = ejecutar_comando_voz()

            print("\n📦 Resultado:")
            print(resultado)

            # --------------------------------------
            # Verificar si debemos terminar
            # --------------------------------------

            if isinstance(resultado, dict):

                accion = str(
                    resultado.get(
                        "accion",
                        ""
                    )
                ).lower()

                if accion == "salir":

                    print(
                        "\n👋 Cerrando asistente..."
                    )

                    break

        except KeyboardInterrupt:

            print(
                "\n\n👋 Programa finalizado."
            )

            break

        except Exception as e:

            print(
                "\n❌ Ocurrió un error:"
            )

            print(e)


if __name__ == "__main__":
    main()