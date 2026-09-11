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

def _nombre_valido_obsidian(nombre: str) -> str:
    """
    Limpia un nombre para que sirva como nombre de archivo
    y como wikilink válido en Windows y en Obsidian.
    """

    caracteres_prohibidos = '<>:"/\\|?*[]'

    limpio = nombre

    for caracter in caracteres_prohibidos:
        limpio = limpio.replace(caracter, "")

    return limpio.strip()


def exportar_a_obsidian(
    grafo: nx.DiGraph,
    carpeta_salida: str
):
    """
    Exporta el grafo de conocimiento como notas de Obsidian:
    una nota .md por cada entidad, con enlaces [[wikilink]]
    hacia las entidades relacionadas. Al abrir la carpeta
    como Vault en Obsidian, el grafo visual se arma solo.
    """

    os.makedirs(
        carpeta_salida,
        exist_ok=True
    )

    for nodo_id, atributos in grafo.nodes(data=True):

        nombre = atributos.get("nombre", str(nodo_id))
        tipo = atributos.get("tipo", "desconocido")

        nombre_archivo = _nombre_valido_obsidian(nombre)

        ruta = os.path.join(
            carpeta_salida,
            f"{nombre_archivo}.md"
        )

        lineas = []
        lineas.append("---")
        lineas.append(f"tipo: {tipo}")
        lineas.append("---")
        lineas.append(f"# {nombre}")
        lineas.append("")

        salientes = list(grafo.out_edges(nodo_id, data=True))

        if salientes:
            lineas.append("## Relaciones")
            for _, destino_id, datos_arista in salientes:
                relacion = datos_arista.get("relacion", "relacionado con")
                nombre_destino = grafo.nodes[destino_id].get("nombre", str(destino_id))
                nombre_destino_valido = _nombre_valido_obsidian(nombre_destino)
                lineas.append(f"- {relacion} [[{nombre_destino_valido}]]")

        entrantes = list(grafo.in_edges(nodo_id, data=True))

        if entrantes:
            lineas.append("")
            lineas.append("## Referenciado por")
            for origen_id, _, datos_arista in entrantes:
                relacion = datos_arista.get("relacion", "relacionado con")
                nombre_origen = grafo.nodes[origen_id].get("nombre", str(origen_id))
                nombre_origen_valido = _nombre_valido_obsidian(nombre_origen)
                lineas.append(f"- [[{nombre_origen_valido}]] {relacion} esta entidad")

        with open(ruta, "w", encoding="utf-8") as archivo:
            archivo.write("\n".join(lineas))

    print(f"✅ {grafo.number_of_nodes()} notas exportadas a: {carpeta_salida}")