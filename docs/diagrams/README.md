# Diagramas adicionais

Os arquivos nesta pasta fornecem representações em PlantUML dos diagramas solicitados:

- `idef0-level0.puml` — IDEF0 Nível 0 (contexto geral)
- `idef0-level1.puml` — IDEF0 Nível 1 (decomposição de funções)
- `use-case.puml` — Diagrama de Casos de Uso
- `dfd.puml` — Diagrama de Fluxo de Dados (nível alto)

Como visualizar

1. Recomendo usar a extensão PlantUML no VS Code (já instalada segundo você). Abra qualquer arquivo `.puml` e use:
   - Command Palette → `PlantUML: Preview Current Diagram` ou
   - Clique com o botão direito no editor → `Preview Current Diagram` / `Open Preview to the Side`.

2. Se preferir abrir no navegador, use a extensão "Markdown Preview Enhanced" ou exporte o diagrama como PNG/SVG pela pré-visualização da extensão PlantUML.

3. Se precisar de saída em batch (várias imagens), instale o plantuml.jar e gere imagens via script:

```bash
# Exemplo rápido (requires plantuml.jar e java)
java -jar plantuml.jar docs/diagrams/*.puml
```

Notas

- Todos os arquivos usam `skinparam defaultFontColor #000000` para garantir contraste.
- Se quiser que eu ajuste elementos, rótulos ou inclua diagramas em outro formato (draw.io, mermaid), me diga qual formato prefere.
