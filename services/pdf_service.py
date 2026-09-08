import os

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    ListFlowable,
    ListItem
)
from reportlab.lib.units import cm


def generar_pdf(
    informe: dict,
    ruta_salida: str
):
    """
    Genera un archivo PDF a partir del informe
    estructurado generado por el Report Agent.
    """

    # Crear carpeta si no existe
    carpeta = os.path.dirname(ruta_salida)

    if carpeta:
        os.makedirs(
            carpeta,
            exist_ok=True
        )

    # ------------------------------------------
    # Configuración del documento
    # ------------------------------------------

    documento = SimpleDocTemplate(
        ruta_salida,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm
    )

    estilos = getSampleStyleSheet()

    titulo = estilos["Title"]
    titulo.alignment = TA_CENTER

    subtitulo = estilos["Heading2"]

    texto = estilos["BodyText"]

    contenido = []

    # ------------------------------------------
    # TÍTULO
    # ------------------------------------------

    contenido.append(
        Paragraph(
            str(
                informe.get(
                    "titulo",
                    "Informe de análisis multimodal"
                )
            ),
            titulo
        )
    )

    contenido.append(
        Spacer(1, 20)
    )

    # ------------------------------------------
    # RESUMEN EJECUTIVO
    # ------------------------------------------

    contenido.append(
        Paragraph(
            "Resumen ejecutivo",
            subtitulo
        )
    )

    contenido.append(
        Paragraph(
            str(
                informe.get(
                    "resumen_ejecutivo",
                    "Sin información disponible."
                )
            ),
            texto
        )
    )

    contenido.append(
        Spacer(1, 15)
    )

    # ------------------------------------------
    # HALLAZGOS
    # ------------------------------------------

    contenido.append(
        Paragraph(
            "Hallazgos principales",
            subtitulo
        )
    )

    hallazgos = informe.get(
        "hallazgos_principales",
        []
    )

    _agregar_lista(
        contenido,
        hallazgos,
        texto,
        "No se encontraron hallazgos."
    )

    contenido.append(
        Spacer(1, 15)
    )

    # ------------------------------------------
    # COINCIDENCIAS
    # ------------------------------------------

    contenido.append(
        Paragraph(
            "Coincidencias relevantes",
            subtitulo
        )
    )

    coincidencias = informe.get(
        "coincidencias_relevantes",
        []
    )

    _agregar_lista(
        contenido,
        coincidencias,
        texto,
        "No se encontraron coincidencias relevantes."
    )

    contenido.append(
        Spacer(1, 15)
    )

    # ------------------------------------------
    # CONTRADICCIONES
    # ------------------------------------------

    contenido.append(
        Paragraph(
            "Contradicciones detectadas",
            subtitulo
        )
    )

    contradicciones = informe.get(
        "contradicciones_detectadas",
        []
    )

    _agregar_lista(
        contenido,
        contradicciones,
        texto,
        "No se detectaron contradicciones."
    )

    contenido.append(
        Spacer(1, 15)
    )

    # ------------------------------------------
    # CONCLUSIÓN
    # ------------------------------------------

    contenido.append(
        Paragraph(
            "Conclusión",
            subtitulo
        )
    )

    contenido.append(
        Paragraph(
            str(
                informe.get(
                    "conclusion",
                    "No se generó una conclusión."
                )
            ),
            texto
        )
    )

    contenido.append(
        Spacer(1, 15)
    )

    # ------------------------------------------
    # NIVEL DE CONFIANZA
    # ------------------------------------------

    contenido.append(
        Paragraph(
            "Nivel de confianza",
            subtitulo
        )
    )

    contenido.append(
        Paragraph(
            str(
                informe.get(
                    "nivel_confianza_general",
                    "No especificado"
                )
            ),
            texto
        )
    )

    # ------------------------------------------
    # GENERAR PDF
    # ------------------------------------------

    documento.build(contenido)


def _agregar_lista(
    contenido,
    elementos,
    estilo,
    mensaje_vacio
):
    """
    Agrega una lista de elementos al documento PDF.
    """

    if elementos:

        lista = ListFlowable(
            [
                ListItem(
                    Paragraph(
                        str(elemento),
                        estilo
                    )
                )
                for elemento in elementos
            ],
            bulletType="bullet"
        )

        contenido.append(lista)

    else:

        contenido.append(
            Paragraph(
                mensaje_vacio,
                estilo
            )
        )