import json

from agents.report_agent import generar_informe
from services.file_service import guardar_json
from services.pdf_service import generar_pdf


ruta_consolidado = "data/output/consolidado.json"
ruta_informe_json = "data/output/informe.json"
ruta_informe_pdf = "data/output/informe_final.pdf"


# ==========================================
# GENERAR INFORME
# ==========================================

resultado = generar_informe(
    ruta_consolidado
)


# ==========================================
# GUARDAR JSON
# ==========================================

guardar_json(
    resultado,
    ruta_informe_json
)


# ==========================================
# GENERAR PDF
# ==========================================

generar_pdf(
    resultado,
    ruta_informe_pdf
)


# ==========================================
# MOSTRAR RESULTADO
# ==========================================

print("\nINFORME GENERADO CORRECTAMENTE")

print(
    f"\nJSON: {ruta_informe_json}"
)

print(
    f"PDF: {ruta_informe_pdf}"
)