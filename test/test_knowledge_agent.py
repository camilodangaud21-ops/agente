import json

from agents.knowledge_agent import (
    extraer_conocimiento
)

from services.graph_service import (
    construir_grafo_conocimiento,
    guardar_grafo
)


ruta_consolidado = (
    "data/output/consolidado.json"
)

ruta_conocimiento = (
    "data/output/knowledge.json"
)

ruta_grafo = (
    "data/output/grafo_conocimiento.graphml"
)


# ==========================================
# 1. CARGAR CONSOLIDADO
# ==========================================

with open(
    ruta_consolidado,
    "r",
    encoding="utf-8"
) as archivo:

    datos = json.load(archivo)


# ==========================================
# 2. EXTRAER CONOCIMIENTO
# ==========================================

print(
    "[1/3] Extrayendo entidades y relaciones..."
)

conocimiento = extraer_conocimiento(
    datos
)


# ==========================================
# 3. GUARDAR KNOWLEDGE.JSON
# ==========================================

with open(
    ruta_conocimiento,
    "w",
    encoding="utf-8"
) as archivo:

    json.dump(
        conocimiento,
        archivo,
        ensure_ascii=False,
        indent=4
    )


print(
    "[2/3] Knowledge JSON generado."
)


# ==========================================
# 4. CONSTRUIR GRAFO
# ==========================================

print(
    "[3/3] Construyendo grafo de conocimiento..."
)

grafo = construir_grafo_conocimiento(
    conocimiento
)


guardar_grafo(
    grafo,
    ruta_grafo
)


# ==========================================
# MOSTRAR RESULTADO
# ==========================================

print("\n========== ENTIDADES ==========\n")

for entidad in conocimiento.get(
    "entidades",
    []
):

    print(
        f"{entidad['id']} "
        f"→ {entidad['nombre']} "
        f"({entidad['tipo']})"
    )


print("\n========== RELACIONES ==========\n")

for relacion in conocimiento.get(
    "relaciones",
    []
):

    print(
        f"{relacion['origen']} "
        f"--[{relacion['relacion']}]--> "
        f"{relacion['destino']}"
    )


print(
    "\nGrafo generado correctamente."
)

print(
    f"Knowledge JSON: {ruta_conocimiento}"
)

print(
    f"Grafo: {ruta_grafo}"
)