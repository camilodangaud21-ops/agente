# Sistema multimodal basado en agentes

Sistema Python capaz de analizar una imagen y un audio, convertir la información extraída en estructuras JSON, consolidar ambas fuentes con un modelo Gemma ejecutado localmente, generar un informe en JSON y PDF, y construir grafos GraphML con la información consolidada o con las entidades y relaciones detectadas.

El proyecto está pensado como una demostración modular de procesamiento multimodal local. La imagen y el audio se procesan por separado y después pasan por etapas de integración, generación de informe y extracción de conocimiento.

## Funcionalidades

- Análisis de imágenes con Gemma 3 mediante la API HTTP de Ollama.
- Transcripción de audio en español con OpenAI Whisper.
- Análisis semántico de la transcripción con Gemma y salida JSON.
- Integración de los resultados de imagen y audio, incluyendo coincidencias, información exclusiva y contradicciones.
- Generación de un informe estructurado y de un archivo PDF.
- Construcción de un grafo dirigido simple desde los datos consolidados.
- Extracción de entidades y relaciones para construir un grafo de conocimiento.
- Comunicación con Ollama por HTTP y respaldo por CLI para consultas de texto.

## Arquitectura y flujo

El flujo principal se divide en etapas independientes:

1. `image_agent.py` lee la imagen, la codifica en Base64 y la envía a Gemma con un prompt multimodal.
2. `audio_agent.py` carga Whisper `base`, transcribe el audio en español y envía la transcripción a Gemma.
3. `integration_agent.py` lee los JSON de imagen y audio y solicita a Gemma un JSON consolidado.
4. `report_agent.py` convierte el consolidado en un informe estructurado.
5. `pdf_service.py` transforma el informe en un PDF usando ReportLab.
6. `graph_agent.py` crea un grafo simple a partir de `datos_consolidados`.
7. `knowledge_agent.py` identifica entidades y relaciones; `graph_service.py` las guarda como grafo de conocimiento.

La integración de los agentes se apoya en servicios comunes:

- `services/gemma_service.py`: consultas a Ollama, limpieza y validación de JSON.
- `services/file_service.py`: escritura de diccionarios como JSON.
- `services/pdf_service.py`: creación del PDF.
- `services/graph_service.py`: construcción y persistencia de grafos.

## Requisitos

- Windows, macOS o Linux.
- Python 3.10 o superior recomendado.
- Git, opcional, para clonar el proyecto.
- Ollama instalado y ejecutándose localmente.
- Modelo `gemma3:4b` descargado en Ollama.
- FFmpeg instalado y disponible en el `PATH`, recomendado para que Whisper pueda leer archivos MP3.
- Memoria suficiente para ejecutar Whisper y Gemma localmente. El rendimiento depende de la CPU/GPU disponible.

## Tecnologías utilizadas

- **Python**: lenguaje principal y coordinación de los agentes.
- **Ollama**: ejecución local del modelo y exposición de la API en `http://127.0.0.1:11434`.
- **Gemma 3 4B**: análisis de imagen, interpretación de texto, integración y extracción de conocimiento.
- **OpenAI Whisper**: transcripción automática de audio.
- **Requests**: llamadas HTTP a la API de Ollama, especialmente para enviar imágenes.
- **Ollama Python**: prueba directa de conexión en `prueba_gemma.py`.
- **NetworkX**: creación de grafos dirigidos.
- **GraphML**: formato portable de salida para los grafos.
- **ReportLab**: generación del informe PDF.
- **PyTorch**: dependencia utilizada internamente por Whisper.
- **SymPy**: importada por la prueba de audio para el valor booleano `true`.

## Instalación

### 1. Crear y activar el entorno virtual

Desde la carpeta raíz del proyecto:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la activación, puede ejecutarse directamente el intérprete del entorno con `\.venv\Scripts\python.exe`.

### 2. Instalar las dependencias

El archivo existente se llama `requiriments.txt` y contiene también comandos de ejemplo. Las dependencias Python que utiliza el código son:

```powershell
python -m pip install --upgrade pip
python -m pip install requests ollama openai-whisper networkx reportlab sympy
```

Whisper puede instalar PyTorch como dependencia. Si la instalación automática no funciona, consulte la instrucción de instalación de PyTorch adecuada para su CPU o GPU y vuelva a instalar `openai-whisper`.

### 3. Instalar FFmpeg

Whisper requiere FFmpeg para leer muchos formatos de audio. En Windows, instálelo con un gestor disponible, por ejemplo:

```powershell
winget install Gyan.FFmpeg.Shared
```

Cierre y vuelva a abrir la terminal después de instalarlo y compruebe:

```powershell
ffmpeg -version
```

### 4. Instalar y preparar Ollama

Instale Ollama desde https://ollama.com/download y descargue el modelo:

```powershell
ollama pull gemma3:4b
ollama list
```

Ollama debe estar activo antes de ejecutar los agentes. Puede comprobar la disponibilidad del modelo con:

```powershell
ollama run gemma3:4b
```

Para consultas de texto, el servicio intenta primero la API HTTP y después la CLI si la API no responde. El análisis de imágenes requiere la API HTTP.

## Estructura del proyecto

```text
Agente_multimodal/
|-- main.py                         Punto de entrada inicial
|-- prueba_gemma.py                 Prueba directa de Ollama
|-- requiriments.txt                Dependencias y comandos originales
|-- agents/
|   |-- image_agent.py              Análisis de imágenes
|   |-- audio_agent.py              Transcripción y análisis de audio
|   |-- integration_agent.py        Consolidación de fuentes
|   |-- report_agent.py             Generación del informe JSON
|   |-- graph_agent.py              Grafo desde consolidado
|   |-- knowledge_agent.py          Entidades y relaciones
|-- services/
|   |-- gemma_service.py            Cliente de Gemma/Ollama
|   |-- file_service.py             Persistencia JSON
|   |-- pdf_service.py              Persistencia PDF
|   |-- graph_service.py            NetworkX y GraphML
|-- data/
|   |-- input/                      Archivos de entrada
|   |-- output/                     Resultados generados
|-- test/                           Scripts ejecutables de prueba
|-- graphs/                         Paquete reservado para grafos
```

## Preparar los archivos de entrada

Coloque los archivos en `data/input/`. Los scripts de prueba esperan estos nombres:

- `data/input/prueba.jpg` para el análisis de imagen.
- `data/input/prueba.mp3` para el análisis de audio.

Puede utilizar otros formatos compatibles cambiando la ruta dentro del script correspondiente. La imagen se envía codificada en Base64 y el audio es leído por Whisper.

## Ejecución recomendada

Ejecute cada etapa desde la raíz del proyecto y mantenga activa la misma instalación de Python.

### 1. Comprobar Gemma

```powershell
.\.venv\Scripts\python.exe .\prueba_gemma.py
```

La salida esperada contiene `conexión exitosa` o la respuesta configurada en el script.

### 2. Analizar la imagen

```powershell
.\.venv\Scripts\python.exe -m test.test_image_agent
```

Genera `data/output/imagen.json`.

### 3. Analizar el audio

```powershell
.\.venv\Scripts\python.exe -m test.test_audio_agent
```

Genera `data/output/audio.json`. En CPU, Whisper puede mostrar el aviso de que FP16 no está disponible; es un comportamiento normal y utiliza FP32.

### 4. Integrar los resultados

```powershell
.\.venv\Scripts\python.exe -m test.test_integration_agent
```

Lee los dos JSON anteriores y genera `data/output/consolidado.json`.

### 5. Crear el informe

```powershell
.\.venv\Scripts\python.exe -m test.test_report_agent
```

Genera:

- `data/output/informe.json`: informe estructurado.
- `data/output/informe_final.pdf`: informe legible en PDF.

### 6. Crear el grafo simple

```powershell
.\.venv\Scripts\python.exe -m test.test_graph_agent
```

Genera `data/output/grafo.graphml`. Este grafo utiliza `datos_consolidados`; si ese objeto está vacío, puede producir solamente el nodo predeterminado `Entidad principal`.

### 7. Crear el grafo de conocimiento

```powershell
.\.venv\Scripts\python.exe -m test.test_knowledge_agent
```

Genera:

- `data/output/knowledge.json`: entidades y relaciones extraídas por Gemma.
- `data/output/grafo_conocimiento.graphml`: grafo dirigido con atributos de tipo y relación.

Los archivos `.graphml` pueden abrirse con Gephi, y también pueden inspeccionarse con NetworkX.

## Ejemplo de formatos JSON

### Resultado de imagen

```json
{
	"fuente": "imagen",
	"tipo_contenido": "",
	"descripcion_general": "",
	"texto_detectado": [],
	"objetos_detectados": [],
	"datos_relevantes": {},
	"nivel_confianza": ""
}
```

### Resultado de audio

```json
{
	"fuente": "audio",
	"transcripcion": "",
	"resumen": "",
	"temas_detectados": [],
	"datos_relevantes": {},
	"nivel_confianza": ""
}
```

### Grafo de conocimiento

```json
{
	"entidades": [
		{"id": "E1", "nombre": "", "tipo": ""}
	],
	"relaciones": [
		{"origen": "E1", "relacion": "relacionado con", "destino": "E2"}
	]
}
```

## Ejecutar las pruebas

Los archivos de `test/` son scripts ejecutables, no una suite `pytest` tradicional. Para ejecutar todas las etapas:

```powershell
.\.venv\Scripts\python.exe -m test.test_image_agent
.\.venv\Scripts\python.exe -m test.test_audio_agent
.\.venv\Scripts\python.exe -m test.test_integration_agent
.\.venv\Scripts\python.exe -m test.test_report_agent
.\.venv\Scripts\python.exe -m test.test_graph_agent
.\.venv\Scripts\python.exe -m test.test_knowledge_agent
```

Estas pruebas realizan llamadas reales a Whisper y Ollama, por lo que necesitan los archivos de entrada, el modelo descargado y una conexión local con Ollama. No son pruebas aisladas ni mocks.

## Configuración de Ollama

La configuración actual está definida en `services/gemma_service.py`:

- Modelo: `gemma3:4b`.
- URL: `http://127.0.0.1:11434`.
- Tiempo de espera de generación: hasta 300 segundos.

También puede cambiarse la ruta del ejecutable de Ollama mediante la variable opcional `OLLAMA_PATH` cuando la CLI no está disponible en el `PATH`.

## Problemas frecuentes

**No se puede conectar con Ollama**

Compruebe que Ollama esté ejecutándose, que `ollama list` muestre `gemma3:4b` y que el puerto `11434` no esté bloqueado.

**El modelo no existe**

Ejecute `ollama pull gemma3:4b` y confirme el nombre exacto con `ollama list`.

**Whisper falla al leer el audio**

Compruebe que FFmpeg esté instalado, que `data/input/prueba.mp3` exista y que el archivo pueda reproducirse normalmente.

**Gemma devuelve JSON inválido**

El servicio solicita formato JSON y valida la respuesta. Si falla, imprime la respuesta recibida para facilitar el diagnóstico. La salida de un modelo generativo puede variar; repetir la ejecución o usar un prompt más restrictivo puede ayudar.

**La ejecución tarda mucho**

La primera carga de Whisper descarga el modelo `base`. Además, Gemma se ejecuta localmente y el tiempo depende de la CPU, GPU y memoria disponibles.

**`main.py` no ejecuta el flujo completo**

El `main.py` incluido corresponde a una versión anterior de la interfaz: llama a `integrar_datos` y entrega diccionarios a funciones que actualmente esperan rutas de archivos. Por eso, la ejecución reproducible actual es la secuencia de scripts `test.test_*` documentada arriba. Actualizar `main.py` para orquestar esas etapas sería una mejora pendiente.

## Limitaciones y consideraciones

- Las respuestas dependen del modelo Gemma y no sustituyen una validación humana.
- El sistema solicita no inventar datos, pero esa instrucción no garantiza exactitud absoluta.
- Los archivos de entrada y salida utilizan rutas relativas; ejecute los comandos desde la raíz del proyecto.
- La extracción de entidades y relaciones depende de la calidad del JSON consolidado.
- El grafo simple solo representa atributos presentes en `datos_consolidados`; el grafo de conocimiento representa entidades y relaciones explícitas.
- El procesamiento puede requerir recursos considerables y no está diseñado todavía como servicio web o aplicación multiusuario.

## Resultado esperado

Después de completar el flujo, `data/output/` puede contener:

```text
imagen.json
audio.json
consolidado.json
informe.json
informe_final.pdf
grafo.graphml
grafo_conocimiento.graphml
knowledge.json
```

En conjunto, estos archivos permiten revisar cada etapa, reutilizar los datos JSON, leer el informe final y visualizar las relaciones extraídas automáticamente.

## Licencia y datos

Este repositorio no incluye una declaración de licencia. Antes de distribuirlo, agregue la licencia correspondiente. No utilice datos personales o clínicos reales sin autorización, anonimización y controles de protección de datos adecuados.