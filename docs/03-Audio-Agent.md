
---

# 4. `03-Audio-Agent.md`

```markdown
# Audio Agent

## Responsabilidad

Procesar audio y convertirlo en información estructurada.

## Proceso

```text
Audio
  ↓
Whisper
  ↓
Transcripción
  ↓
Gemma
  ↓
JSON


Tecnologías
Whisper
Gemma
Ollama
Archivo
agents/audio_agent.py
Salida
data/output/audio.json