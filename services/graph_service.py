import json
import os
import networkx as nx


def cargar_json(ruta: str) -> dict:
    """
    Carga un archivo JSON.
    """

    if not os.path.exists(ruta):
        raise FileNotFoundError(
            f"No se encontró el archivo: {ruta}"
        )

    with open(
        ruta,
        "r",
        encoding="utf-8"
    ) as archivo:

        return json.load(archivo)


def construir_grafo(datos: dict) -> nx.DiGraph:
    """
    Construye un grafo dirigido a partir de los
    datos consolidados.
    """

    grafo = nx.DiGraph()

    datos_consolidados = datos.get(
        "datos_consolidados",
        {}
    )

    # ------------------------------------------
    # IDENTIFICAR ENTIDAD PRINCIPAL
    # ------------------------------------------

    nombre = datos_consolidados.get("nombre")

    if not nombre:
        nombre = "Entidad principal"

    # Nodo principal
    grafo.add_node(
        nombre,
        tipo="entidad"
    )

    # ------------------------------------------
    # CREAR RELACIONES
    # ------------------------------------------

    for atributo, valor in datos_consolidados.items():

        if atributo == "nombre":
            continue

        if valor is None:
            continue

        # Convertir listas/diccionarios a texto
        if isinstance(valor, (list, dict)):
            valor = json.dumps(
                valor,
                ensure_ascii=False
            )

        valor = str(valor)

        # Crear nodo del valor
        grafo.add_node(
            valor,
            tipo="valor"
        )

        # Crear relación
        grafo.add_edge(
            nombre,
            valor,
            relacion=atributo
        )

    return grafo


def guardar_grafo(
    grafo: nx.DiGraph,
    ruta: str
):
    """
    Guarda el grafo en formato GraphML.
    """

    carpeta = os.path.dirname(ruta)

    if carpeta:
        os.makedirs(
            carpeta,
            exist_ok=True
        )

    nx.write_graphml(
        grafo,
        ruta
    )


def construir_grafo_desde_json(
    ruta_json: str,
    ruta_salida: str
):
    """
    Carga el JSON, construye el grafo y lo guarda.
    """

    datos = cargar_json(
        ruta_json
    )

    grafo = construir_grafo(
        datos
    )

    guardar_grafo(
        grafo,
        ruta_salida
    )

    return grafo

def construir_grafo_conocimiento(
    conocimiento: dict
) -> nx.DiGraph:
    """
    Construye un grafo a partir de entidades y relaciones
    extraídas por el Knowledge Agent.
    """

    grafo = nx.DiGraph()

    entidades = conocimiento.get(
        "entidades",
        []
    )

    relaciones = conocimiento.get(
        "relaciones",
        []
    )

    # ------------------------------------------
    # ENTIDADES
    # ------------------------------------------

    for entidad in entidades:

        entidad_id = entidad.get("id")

        if not entidad_id:
            continue

        grafo.add_node(
            entidad_id,
            nombre=entidad.get(
                "nombre",
                entidad_id
            ),
            tipo=entidad.get(
                "tipo",
                "desconocido"
            )
        )

    # ------------------------------------------
    # RELACIONES
    # ------------------------------------------

    for relacion in relaciones:

        origen = relacion.get(
            "origen"
        )

        destino = relacion.get(
            "destino"
        )

        tipo_relacion = relacion.get(
            "relacion",
            "relacionado_con"
        )

        if not origen or not destino:
            continue

        # Evitar relaciones hacia entidades
        # que no existen
        if origen not in grafo:
            continue

        if destino not in grafo:
            continue

        grafo.add_edge(
            origen,
            destino,
            relacion=tipo_relacion
        )

    return grafo