# Changelog | Agente Multimodal

Registro de las versiones, funcionalidades y decisiones relevantes del proyecto.

## Estado actual

| Version | Estado | Alcance |
| --- | --- | --- |
| `1.0.0` | Finalizada | Pipeline multimodal, informes y grafos |
| `2.0.0` | Finalizada | Asistente de voz y orquestacion de agentes |
| `3.0.0` | Planificada | Nueva etapa experimental |

---

## [2.0.0] - Version 2.0

**Estado:** Finalizada

La version 2.0 transforma el pipeline multimodal en un asistente interactivo. El usuario puede hablar con el sistema, el `Voice Agent` interpreta la orden, el `Orchestrator Agent` decide que componente debe actuar y el `Agent Executor` ejecuta la accion.

### Resumen del flujo

```text
Microfono
    |
    v
Audio WAV -> Whisper -> Voice Agent -> Orchestrator Agent
                                              |
                                              v
                                        Agent Executor
                                              |
                    +-------------------------+------------------+
                    v                         v                  v
              Report Agent              Graph Agent       Knowledge Agent
                    |                         |                  |
                    v                         v                  v
             informe_voz.pdf              GraphML           conocimiento
```

### Reconocimiento de voz

Se incorporo la interaccion mediante microfono:

- Captura de audio desde el dispositivo de entrada.
- Almacenamiento temporal en `data/temp/`.
- Generacion de archivos WAV.
- Transcripcion con Whisper.
- Configuracion del idioma espanol.
- Reutilizacion de servicios para centralizar el procesamiento.

Flujo de datos:

```text
Microfono -> Audio WAV -> Whisper -> Texto
```

### Grabacion inteligente

La grabacion ya no depende solamente de una duracion fija. `voice_recorder.py`:

1. Prepara el microfono.
2. Detecta cuando el usuario comienza a hablar.
3. Mantiene la captura mientras existe actividad de voz.
4. Detecta un periodo de silencio.
5. Finaliza y guarda automaticamente el archivo WAV.

Esto permite comandos de distinta duracion y evita grabaciones innecesariamente largas.

### Voice Agent

`voice_agent.py` convierte la transcripcion en una intencion estructurada mediante Gemma.

Entrada de ejemplo:

> Genera un reporte del paciente Juan Perez.

Salida esperada:

```json
{
  "intencion": "generar_reporte",
  "datos": {
    "paciente": "Juan Perez"
  }
}
```

El agente interpreta la orden, pero no ejecuta acciones. Esta separacion mantiene independiente la comprension del lenguaje y la ejecucion del sistema.

### Orchestrator Agent

`orchestrator_agent.py` transforma la intencion en una decision operativa:

```json
{
  "agente": "report_agent",
  "accion": "generar_reporte",
  "datos": {
    "paciente": "Juan Perez"
  }
}
```

Intenciones contempladas:

- `generar_reporte`
- `consultar_grafo`
- `analizar_informacion`
- `procesar_imagen`
- `procesar_audio`
- `desconocido`

La arquitectura separa explicitamente:

```text
Interpretacion -> Decision -> Ejecucion
```

### Agent Executor

`agent_executor.py` ejecuta la decision del orquestador y unifica la respuesta de los agentes.

Agentes contemplados:

- `report_agent`
- `graph_agent`
- `knowledge_agent`
- `image_agent`
- `audio_agent`

Formato estandar de resultado:

```json
{
  "estado": "completado",
  "agente": "report_agent",
  "accion": "generar_reporte",
  "datos": {},
  "resultado": {},
  "error": null
}
```

Este contrato permite informar tanto ejecuciones exitosas como errores de forma consistente.

### Informes y PDF

Se consolido el flujo del `Report Agent`:

1. Carga la informacion consolidada.
2. Envia los datos a Gemma.
3. Genera un informe estructurado.
4. Utiliza `pdf_service.py` y ReportLab para crear el PDF.

El resultado principal de la ejecucion por voz es:

```text
data/output/informe_voz.pdf
```

### Gemma y Ollama

Gemma se ejecuta localmente mediante Ollama:

- Modelo: `gemma3:4b`
- API: `http://127.0.0.1:11434/api/generate`
- Respuestas estructuradas en JSON.
- Validacion de las respuestas recibidas.
- Manejo de errores HTTP, conexion y timeout.
- Opciones de generacion para limitar respuestas cortas, como la deteccion de intenciones.
- Respaldo por CLI para consultas de texto cuando la API no esta disponible.

### Configuracion centralizada

Se incorporo `config/settings.py` para evitar valores duplicados en distintos modulos. La configuracion incluye:

- Modelo y URL de Ollama.
- Modelo e idioma de Whisper.
- Frecuencia de muestreo y canales del microfono.
- Umbral y duracion del silencio.
- Duracion maxima de grabacion.
- Rutas temporales y de salida.

### Punto de entrada

`main.py` funciona como entrada principal de la V2.0:

```powershell
.\.venv\Scripts\python.exe main.py
```

El programa muestra el banner, solicita una grabacion, ejecuta el flujo de voz y permite introducir nuevos comandos hasta que el usuario lo finaliza.

### Pruebas realizadas

Durante el desarrollo se validaron los siguientes componentes:

| Componente | Validaciones |
| --- | --- |
| Voice Recorder | Microfono detectado, grabacion realizada y WAV generado |
| Whisper | Audio procesado y transcripcion obtenida |
| Voice Agent | Intencion, datos extraidos y JSON generado |
| Orchestrator Agent | Reporte, grafo, analisis, imagen, audio y desconocido |
| Agent Executor | Ejecucion de agente, informe, PDF, errores y estados |
| Integracion | Flujo completo desde voz hasta `informe_voz.pdf` |

Resultado documentado: **V2.0 funcionando correctamente**.

### Arquitectura alcanzada

```text
Usuario
   |
   v
Microfono
   |
   v
Whisper
   |
   v
Voice Agent
   |
   v
Orchestrator Agent
   |
   v
Agent Executor
   |
   +----------------+----------------+----------------+
   v                v                v                v
Image Agent    Audio Agent    Report Agent    Knowledge Agent
   |                |                |                |
   v                v                v                v
 JSON             JSON       informe.json     knowledge.json
                                     |                |
                                     v                v
                              PDF Service       Graph Service
                                     |                |
                                     v                v
                              informe PDF      grafo GraphML
```

---

## [1.0.0] - Version 1.0

**Estado:** Finalizada

La primera version establecio la arquitectura multimodal y el procesamiento independiente de imagen y audio.

### Image Agent

`image_agent.py` analiza imagenes con Gemma y genera informacion estructurada:

- Descripcion general.
- Texto detectado.
- Objetos identificados.
- Datos relevantes.
- Nivel de confianza.

El resultado se guarda en:

```text
data/output/imagen.json
```

### Audio Agent

`audio_agent.py` procesa un archivo de audio con el siguiente flujo:

```text
Audio -> Whisper -> Transcripcion -> Gemma -> JSON
```

El resultado incluye la transcripcion, un resumen, temas y datos relevantes:

```text
data/output/audio.json
```

### Integracion multimodal

`integration_agent.py` combina los resultados de imagen y audio, identifica coincidencias, separa la informacion exclusiva y registra posibles contradicciones.

```text
Imagen -> imagen.json -+
                        +-> Integration Agent -> consolidado.json
Audio  -> audio.json  -+
```

### Report Agent

`report_agent.py` analiza `consolidado.json` con Gemma y genera un informe estructurado en:

```text
data/output/informe.json
```

### PDF Service

`pdf_service.py` utiliza ReportLab para transformar el informe estructurado en un documento PDF.

### Knowledge Agent

`knowledge_agent.py` extrae entidades, tipos y relaciones a partir de la informacion consolidada. Su salida se guarda en:

```text
data/output/knowledge.json
```

### Graph Agent y Graph Service

Los componentes de grafos representan los datos como estructuras dirigidas y las guardan en GraphML.

Salidas principales:

- `data/output/grafo.graphml`
- `data/output/grafo_conocimiento.graphml`

Ejemplo conceptual:

```text
Juan Perez --tiene diagnostico--> Migrana
Juan Perez --recibe tratamiento--> Acetaminofen
```

---

## Evolucion del proyecto

```text
V1.0
  Procesamiento de imagen y audio
  JSON estructurado
  Consolidacion multimodal
  Informes y PDF
  Entidades, relaciones y grafos
        |
        v
V2.0
  Microfono
  Whisper
  Grabacion por silencio
  Voice Agent
  Orchestrator Agent
  Agent Executor
  Configuracion centralizada
  Punto de entrada main.py
        |
        v
V3.0
  Nueva etapa experimental
```

## Proximo objetivo: V3.0

La V3.0 se desarrollara preferiblemente en una rama independiente para preservar la estabilidad de la V2.0.

Lineas de investigacion posibles:

- Memoria de contexto.
- Herramientas externas.
- Agentes mas autonomos.
- Automatizacion de tareas.
- Integracion con APIs.
- Interfaces graficas.
- Interaccion multimodal avanzada.

## Nota de mantenimiento

Las nuevas funcionalidades deben documentarse en una nueva entrada siguiendo el formato:

```markdown
## [X.Y.Z] - Titulo de la version

**Estado:** En desarrollo | Finalizada

Descripcion breve del cambio.

### Nuevas funcionalidades

- Cambio realizado.

### Correcciones

- Problema solucionado.
```
