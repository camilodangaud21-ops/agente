
---

# 3. `02-Image-Agent.md`

```markdown
# Image Agent

## Responsabilidad

Procesar una imagen y transformarla en información estructurada.

## Entrada

Una imagen.

## Proceso

```text
Imagen
  ↓
Gemma
  ↓
Análisis visual
  ↓
JSON

Salida

El agente genera información como:

descripción
texto detectado
objetos
datos relevantes
nivel de confianza
Archivo
agents/image_agent.py
Salida
data/output/imagen.json