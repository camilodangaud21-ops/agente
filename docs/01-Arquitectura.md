# Arquitectura

## Arquitectura general

El sistema utiliza diferentes agentes especializados.

```text
Imagen
  ↓
Image Agent
  ↓
imagen.json

Audio
  ↓
Audio Agent
  ↓
audio.json

imagen.json + audio.json
  ↓
Integration Agent
  ↓
consolidado.json

consolidado.json
  ├──→ Report Agent
  │       ↓
  │     informe.json
  │       ↓
  │     PDF
  │
  └──→ Knowledge Agent
          ↓
      knowledge.json
          ↓
      Graph Service
          ↓
      grafo.graphml


      Componentes
Image Agent

Procesa imágenes y obtiene información estructurada.

Audio Agent

Transcribe audio mediante Whisper y posteriormente utiliza Gemma para estructurar la información.

Integration Agent

Combina la información obtenida de las diferentes fuentes.

Report Agent

Genera un informe estructurado.

Knowledge Agent

Extrae entidades y relaciones.

Graph Service

Representa las entidades y relaciones mediante un grafo.