import json
import os

from agents.knowledge_agent import extraer_conocimiento
from services.graph_service import (
    construir_grafo_conocimiento,
    guardar_grafo,
    exportar_a_obsidian
)

RUTA_ENTRADA = "data/output/imagen.json"
RUTA_KNOWLEDGE = "data/output/knowledge.json"
RUTA_GRAFO = "data/output/grafo_conocimiento.graphml"
RUTA_VAULT = "data/output/obsidian_vault"


def main():

    if not os.path.exists(RUTA_ENTRADA):
        print(f"❌ No existe {RUTA_ENTRADA}. Corré primero 'procesa la imagen' con main.py.")
        return

    with open(RUTA_ENTRADA, "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)

    print("[1/4] Extrayendo entidades y relaciones con Gemma (puede tardar)...")
    conocimiento = extraer_conocimiento(datos)

    with open(RUTA_KNOWLEDGE, "w", encoding="utf-8") as archivo:
        json.dump(conocimiento, archivo, ensure_ascii=False, indent=2)

    print(f"[2/4] Knowledge JSON guardado en: {RUTA_KNOWLEDGE}")

    grafo = construir_grafo_conocimiento(conocimiento)
    guardar_grafo(grafo, RUTA_GRAFO)

    print(f"[3/4] Grafo guardado en: {RUTA_GRAFO}")
    print(f"       Nodos: {grafo.number_of_nodes()} | Relaciones: {grafo.number_of_edges()}")

    exportar_a_obsidian(grafo, RUTA_VAULT)

    print(f"[4/4] Listo. Abrí '{RUTA_VAULT}' como Vault en Obsidian.")


if __name__ == "__main__":
    main()