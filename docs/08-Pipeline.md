
---

# 9. `08-Pipeline.md`

Este es importante para entender **todo el proyecto de un vistazo**.

```markdown
# Pipeline completo

## V1.0

```text
                 ┌──────────────┐
                 │    IMAGEN    │
                 └──────┬───────┘
                        ↓
                  Image Agent
                        ↓
                  imagen.json
                        │
                        │
                        │
                 ┌──────┴───────┐
                 │ Integration  │
                 │    Agent     │
                 └──────┬───────┘
                        ↑
                        │
                   audio.json
                        ↑
                        │
                 Audio Agent
                        ↑
                        │
                 ┌──────┴───────┐
                 │    AUDIO     │
                 └──────────────┘

                        ↓

                 consolidado.json
                        │
              ┌─────────┴─────────┐
              ↓                   ↓
        Report Agent       Knowledge Agent
              ↓                   ↓
        informe.json        knowledge.json
              ↓                   ↓
             PDF           Graph Service
                                  ↓
                             grafo.graphml