# Arena da Capivara

[![Arena da Capivara](guia/assets/banner.jpg)](https://inematds.github.io/arena-capivara/guia/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

Qual IA desenha a melhor capivara de bicicleta? Pedimos o mesmo SVG a 19 modelos: 10 rodando no próprio computador (Ollama) e 9 pela assinatura do Claude e do ChatGPT (CLIs `claude` e `codex`). Nenhuma API paga. Um juiz cego comparou os desenhos dois a dois, nas duas ordens.

Inspirado no benchmark do pelicano de bicicleta de Simon Willison.

## 📖 Guia e resultado

- Guia (o que é, como rodar, como montar o seu benchmark): **https://inematds.github.io/arena-capivara/guia/**
- Resultado da rodada 1 (ranking, galeria, código de cada SVG): **https://inematds.github.io/arena-capivara/resultados/**

## Rodada 1 (05/10/2026)

| # | Modelo | Onde roda | Vitórias |
|---|---|---|---|
| 1 | Claude Fable 5.1 | assinatura Claude | 97% |
| 2 | GPT-6.1 Sol | assinatura ChatGPT/Codex | 94% |
| 3 | GPT-6 Astra | assinatura ChatGPT/Codex | 91% |
| 4 | Claude Opus 5.5 | assinatura Claude | 82% |
| 5 | **Qwen 3.8 27B** | **no seu PC** | 74% |
| 6 | GPT-5.5 | assinatura ChatGPT/Codex | 71% |
| 7 | Claude Sonnet 5.5 | assinatura Claude | 65% |

Tabela completa (18 modelos com SVG válido; o Command R 35B não entregou) na [página de resultados](https://inematds.github.io/arena-capivara/resultados/). Juiz: Claude Sonnet 5.5, 306 confrontos. Segundo juiz (GPT-6 Luna) concordou em 92% dos 64 que refez. Lado esquerdo venceu 49,7% (sem viés de posição). Uma tentativa por modelo: é uma foto, não uma sentença.

## Rodar no seu PC

```bash
pip install cairosvg pillow
git clone https://github.com/inematds/arena-capivara && cd arena-capivara
# edite arena/modelos.json com os modelos que você tem
python3 arena/gerar.py           # pede o desenho a cada modelo
python3 arena/renderizar.py      # SVG -> PNG + confrontos A|B
python3 arena/julgar.py          # juiz cego (Claude Sonnet 5.5 pela assinatura)
python3 arena/julgar.py --juiz codex --modelo gpt-6-luna --amostra 60   # 2º juiz
python3 arena/ranking.py --tabela
python3 arena/galeria.py         # resultados/index.html (+ en/ es/)
```

Os confrontos (`resultados/pares/`) não vão para o repositório; o `renderizar.py` recria.

Projeto irmão, da mesma palestra: [Tríade Letal](https://inematds.github.io/triade-letal/guia/), quando um agente de IA pode vazar seus dados.

Licença MIT · [INEMA.CLUB](https://inema.club)
