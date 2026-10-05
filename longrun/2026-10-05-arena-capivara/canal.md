# Canal — arena-capivara (só acrescentar; nunca reescrever)

Conhecimento do projeto que a compactação perde: fatos descobertos, aprendizados, glossário, armadilhas, onde estão as coisas.
Não é estado da tarefa (isso vai em state/plan/progress). Preencha cedo — o hook avisa na faixa 1 (~50% do contexto).

Formato: `- AAAA-MM-DD HH:MM · fato|aprendizado|glossário|armadilha · texto`


## 05/10/2026 18:20
- claude -p limpo: `--setting-sources "" --strict-mcp-config --disable-slash-commands --system-prompt ... --tools ""` (~450 tokens de entrada). `--bare` NÃO serve: pula keychain → "Not logged in".
- cairosvg instalado é antigo: sem `url_fetcher`. Sanitizo href (só data:/#) antes do render.
- Capa da tríade sem --cena saiu "trio gótico"; com --cena explícita ficou certa.
- Tradução dos guias: corpo em scratchpad (montar.py + traduz.sh via codex gpt-6-luna).

## 05/10/2026 19:00 — fechamento
- Tudo publicado. Corpos dos guias e scripts de montagem/tradução ficaram no scratchpad da sessão (montar.py, traduz.sh, preencher_arena.py); o guia publicado é a fonte agora.
- duelo da página de resultados = resultados/duelo.png (copiado pelo galeria.py); resultados/pares/ fora do git.
- Portal: outra sessão publicava ao mesmo tempo; esperei o publica.sh dela terminar (kill -0 no PID) antes de editar.
