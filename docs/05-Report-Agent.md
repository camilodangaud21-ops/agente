
---

# 6. `05-Report-Agent.md`

```markdown
# Report Agent

## Responsabilidad

Generar un informe a partir de la información consolidada.

## Entrada

```text
consolidado.json


Proceso
consolidado.json
      ↓
Report Agent
      ↓
Gemma
      ↓
informe.json

Posteriormente el informe es convertido a PDF mediante pdf_service.py.

Salidas
data/output/informe.json
data/output/informe_final.pdf