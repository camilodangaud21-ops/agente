
---

# 5. `04-Integration-Agent.md`

```markdown
# Integration Agent

## Responsabilidad

Integrar la información proveniente de diferentes agentes.

## Entrada

```text
imagen.json
audio.json

Proceso
Image Agent
      ↓
imagen.json
      ┐
      ├──→ Integration Agent
      ┘
audio.json
      ↑
Audio Agent
Salida
consolidado.json
Objetivo

Obtener una única representación estructurada de toda la información recolectada.