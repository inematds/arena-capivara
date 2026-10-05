# Canal — arena-capivara (só acrescentar; nunca reescrever)

Conhecimento do projeto que a compactação perde: fatos descobertos, aprendizados, glossário, armadilhas, onde estão as coisas.
Não é estado da tarefa (isso vai em state/plan/progress). Preencha cedo — o hook avisa na faixa 1 (~50% do contexto).

Formato: `- AAAA-MM-DD HH:MM · fato|aprendizado|glossário|armadilha · texto`


## 05/10/2026 18:20
- claude -p limpo: `--setting-sources "" --strict-mcp-config --disable-slash-commands --system-prompt ... --tools ""` (~450 tokens de entrada). `--bare` NÃO serve: pula keychain → "Not logged in".
- cairosvg instalado é antigo: sem `url_fetcher`. Sanitizo href (só data:/#) antes do render.
- Capa da tríade sem --cena saiu "trio gótico"; com --cena explícita ficou certa.
- Tradução dos guias: corpo em scratchpad (montar.py + traduz.sh via codex gpt-6-luna).
