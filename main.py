from agents.voice_controller import ejecutar_comando_voz


def mostrar_banner():

    print("+------------------------------------------------+")
    print("|        SISTEMA MULTIMODAL DE AGENTES de ia     |")
    print("+------------------------------------------------+")


def main():

    mostrar_banner()

    print("\n[ASISTENTE DE VOZ]")
    print("Indica por voz la acción que deseas ejecutar.")
    print("Di 'Salir' para finalizar.\n")

    while True:

        try:

            resultado = ejecutar_comando_voz()

            print("\n[RESULTADO]")
            print("----------------------------------------------")
            print(resultado)
            print("----------------------------------------------")

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
                        "\n[INFO] Cerrando asistente..."
                    )

                    break

        except KeyboardInterrupt:

            print(
                "\n\n[INFO] Programa finalizado."
            )

            break

        except Exception as e:

            print(
                "\n[ERROR] Ocurrió un error:"
            )

            print(e)


if __name__ == "__main__":
    main()