# Goal — Arena da Capivara + Tríade Letal (05/10/2026)

Pedido do Nei: "faz os 3 e publica no portal" a partir da palestra do Simon Willison (pelicano de bicicleta).
Modelos: só locais (Ollama) + Claude (claude -p) + Codex (codex exec), pela assinatura. Nenhuma API externa.

Entregas:
1. Kit `inematds/arena-capivara`: gerar SVG "capivara andando de bicicleta" em ~19 modelos, renderizar, julgar em pares (2 ordens), ranking.
2. Guia PT/EN/ES em `guia/` com o método "monte seu benchmark" embutido + página de resultados em `resultados/`.
3. Kit `inematds/triade-letal`: checklist + script de inventário de MCP/tools + guia PT/EN/ES.
4. Os dois no portal (atualiza-portal).
Short: NÃO publicar; protótipo só se sobrar, pendência dita ao Nei.

## Critério de pronto (nível 3)
- `ls ~/projetos/arena-capivara/resultados/svgs/*.svg | wc -l` → ≥ 15
- `python3 arena/ranking.py --tabela` → imprime tabela com ≥ 15 modelos e taxa de vitória
- `jq length resultados/julgamentos.jsonl` equivalente: `wc -l resultados/julgamentos.jsonl` → ≥ 2× pares válidos × 0,9
- concordância juiz Claude × Codex publicada na página de resultados
- `curl -s -o /dev/null -w '%{http_code}' https://inematds.github.io/arena-capivara/guia/` → 200 (idem /guia/en/, /guia/es/, /resultados/)
- `curl -s ... https://inematds.github.io/triade-letal/guia/` → 200 (idem en/es)
- `python3 ~/projetos/triade-letal/inventario.py --demo` → sai 0 e imprime tabela
- portal: `git -C ~/projetos/portal log origin/main --oneline -5` contém commit de arena-capivara e triade-letal
