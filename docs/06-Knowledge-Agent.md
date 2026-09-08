
---

# 7. `06-Knowledge-Agent.md`

```markdown
# Knowledge Agent

## Responsabilidad

Extraer conocimiento semántico de la información consolidada.

## Entrada

```text
consolidado.json

Proceso
consolidado.json
      ↓
Knowledge Agent
      ↓
Gemma
      ↓
Entidades + Relaciones
Entidades

Ejemplo:

Juan Pérez → persona
Migraña → diagnóstico
Acetaminofén → medicamento
Relaciones

Ejemplo:

Juan Pérez
    │
    ├── presenta → Migraña
    │
    └── recibe → Acetaminofén
Salida
data/output/knowledge.json