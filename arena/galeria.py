#!/usr/bin/env python3
"""Passo 5: gera a página pública de resultados (resultados/index.html + en/ + es/).

Uso: python3 arena/galeria.py
"""
import html
import json

from comum import ARENA, RES

TXT = {
    "pt": {
        "lang": "pt-BR", "title": "Arena da Capivara — resultados",
        "h1": "Quem desenha melhor uma <span class='amb'>capivara de bicicleta</span>?",
        "lead": "{n} modelos de IA receberam o mesmo pedido. Nenhum deles é gerador de imagem: todos escrevem código SVG. Um juiz comparou os desenhos dois a dois, sem saber quem fez cada um.",
        "prompt": "O pedido, igual para todos",
        "como": "Como foi medido",
        "como_itens": [
            "{n} modelos: {loc} rodando no próprio computador (Ollama) e {nuv} pela assinatura (Claude Code e Codex). Nenhuma API paga.",
            "Uma tentativa por modelo, no dia {data}. Rode de novo e o desenho muda: é uma foto, não uma sentença.",
            "Juiz principal: <b>{juiz}</b>. Viu {j} confrontos, cada par nas duas ordens (esquerda/direita), sem os nomes.",
            "Lado esquerdo venceu {viesA} das vezes (50% = sem viés de posição).",
            "{conc}",
            "Ranking pela taxa de vitória. O ELO (média de 200 ordens sorteadas) vem ao lado só para comparar.",
        ],
        "conc": "Segundo juiz (<b>{j2}</b>) refez {p} confrontos sorteados e concordou em {t}.",
        "conc_nao": "Sem segundo juiz nesta rodada.",
        "podio": "Pódio", "ranking": "Ranking completo",
        "cols": ["#", "Desenho", "Modelo", "Onde roda", "Vitórias", "Taxa", "ELO", "Tempo"],
        "fam": {"Local": "no seu PC", "Anthropic": "assinatura Claude", "OpenAI": "assinatura ChatGPT/Codex"},
        "sem": "não entregou SVG válido", "naorodou": "não rodou",
        "duelo": "O confronto mais desigual", "duelo_txt": "Primeiro contra último colocado. O que o juiz escreveu:",
        "local": "E os modelos locais?",
        "local_txt": "O melhor modelo que roda no próprio computador foi <b>{m}</b>, em {p}º lugar de {n}. O pior da nuvem ficou em {pn}º.",
        "galeria": "Todos os desenhos", "resposta": "resposta crua", "svg": "SVG",
        "motivo_nota": "",
        "rodape": "Inspirado no benchmark do pelicano de bicicleta de Simon Willison. Kit aberto para você rodar com os seus modelos:",
        "guia": "Como montar o seu", "seg": "s",
    },
    "en": {
        "lang": "en", "title": "Capybara Arena — results",
        "h1": "Which AI draws the best <span class='amb'>capybara riding a bicycle</span>?",
        "lead": "{n} AI models got the same request. None of them is an image generator: they all write SVG code. A judge compared the drawings in pairs, without knowing who made each one.",
        "prompt": "The request, identical for everyone (in Portuguese)",
        "como": "How it was measured",
        "como_itens": [
            "{n} models: {loc} running on the computer itself (Ollama) and {nuv} through the subscription (Claude Code and Codex). No paid API.",
            "One attempt per model, on {data}. Run it again and the drawing changes: it is a snapshot, not a verdict.",
            "Main judge: <b>{juiz}</b>. It saw {j} matchups, each pair in both orders (left/right), without names.",
            "The left side won {viesA} of the time (50% = no position bias).",
            "{conc}",
            "Ranked by win rate. ELO (average over 200 shuffled orders) is shown alongside for comparison.",
        ],
        "conc": "A second judge (<b>{j2}</b>) redid {p} random matchups and agreed on {t}.",
        "conc_nao": "No second judge in this round.",
        "podio": "Podium", "ranking": "Full ranking",
        "cols": ["#", "Drawing", "Model", "Runs on", "Wins", "Rate", "ELO", "Time"],
        "fam": {"Local": "your own PC", "Anthropic": "Claude subscription", "OpenAI": "ChatGPT/Codex subscription"},
        "sem": "no valid SVG", "naorodou": "did not run",
        "duelo": "The most lopsided matchup", "duelo_txt": "First place against last place. What the judge wrote (in Portuguese):",
        "local": "What about local models?",
        "local_txt": "The best model running on the computer itself was <b>{m}</b>, ranked {p} of {n}. The weakest cloud model ranked {pn}.",
        "galeria": "Every drawing", "resposta": "raw answer", "svg": "SVG",
        "motivo_nota": " (judge wrote in Portuguese)",
        "rodape": "Inspired by Simon Willison's pelican-riding-a-bicycle benchmark. Open kit so you can run it with your own models:",
        "guia": "Build your own", "seg": "s",
    },
    "es": {
        "lang": "es", "title": "Arena del Capibara — resultados",
        "h1": "¿Qué IA dibuja mejor un <span class='amb'>capibara en bicicleta</span>?",
        "lead": "{n} modelos de IA recibieron el mismo pedido. Ninguno genera imágenes: todos escriben código SVG. Un juez comparó los dibujos de dos en dos, sin saber quién hizo cada uno.",
        "prompt": "El pedido, igual para todos (en portugués)",
        "como": "Cómo se midió",
        "como_itens": [
            "{n} modelos: {loc} corriendo en la propia computadora (Ollama) y {nuv} por la suscripción (Claude Code y Codex). Ninguna API paga.",
            "Un intento por modelo, el {data}. Si lo corres de nuevo el dibujo cambia: es una foto, no una sentencia.",
            "Juez principal: <b>{juiz}</b>. Vio {j} enfrentamientos, cada par en los dos órdenes (izquierda/derecha), sin nombres.",
            "El lado izquierdo ganó {viesA} de las veces (50% = sin sesgo de posición).",
            "{conc}",
            "Ranking por tasa de victorias. El ELO (promedio de 200 órdenes sorteados) aparece al lado solo para comparar.",
        ],
        "conc": "Un segundo juez (<b>{j2}</b>) rehízo {p} enfrentamientos sorteados y coincidió en {t}.",
        "conc_nao": "Sin segundo juez en esta ronda.",
        "podio": "Podio", "ranking": "Ranking completo",
        "cols": ["#", "Dibujo", "Modelo", "Dónde corre", "Victorias", "Tasa", "ELO", "Tiempo"],
        "fam": {"Local": "en tu PC", "Anthropic": "suscripción Claude", "OpenAI": "suscripción ChatGPT/Codex"},
        "sem": "no entregó SVG válido", "naorodou": "no se ejecutó",
        "duelo": "El enfrentamiento más desigual", "duelo_txt": "Primero contra último. Lo que escribió el juez (en portugués):",
        "local": "¿Y los modelos locales?",
        "local_txt": "El mejor modelo que corre en la propia computadora fue <b>{m}</b>, en el puesto {p} de {n}. El más débil de la nube quedó en el puesto {pn}.",
        "galeria": "Todos los dibujos", "resposta": "respuesta cruda", "svg": "SVG",
        "motivo_nota": " (el juez escribió en portugués)",
        "rodape": "Inspirado en el benchmark del pelícano en bicicleta de Simon Willison. Kit abierto para que lo corras con tus modelos:",
        "guia": "Arma el tuyo", "seg": "s",
    },
}

CSS = """
:root{--bg:#0b0d10;--card:#13171c;--line:#232a33;--tx:#e8e6e1;--mut:#9aa3ad;--amb:#E2A23B;--sky:#38bdf8;--pro:#cbd5e1}
body.light{--bg:#f7f5f0;--card:#fff;--line:#e3ded3;--tx:#1d1d1b;--mut:#5d636b;--pro:#b45309}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--tx);font:16px/1.6 Inter,system-ui,sans-serif}
h1,h2,h3{font-family:Sora,Inter,sans-serif;line-height:1.2}a{color:var(--amb)}
.amb{color:var(--amb)}.wrap{max-width:1100px;margin:0 auto;padding:0 16px}
nav{position:sticky;top:0;z-index:5;background:color-mix(in srgb,var(--bg) 88%,transparent);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
nav .wrap{display:flex;gap:12px;align-items:center;height:56px;flex-wrap:nowrap;overflow:hidden}
nav .logo{font-weight:700;color:var(--amb);text-decoration:none;white-space:nowrap}
nav .inema{color:var(--sky);text-decoration:none;font-weight:600}nav .pro{color:var(--pro);text-decoration:none;font-weight:700}
nav .sp{flex:1}nav .lang a{color:var(--mut);text-decoration:none;margin-left:6px;font-size:14px}nav .lang a.on{color:var(--amb);font-weight:700}
nav button{background:none;border:1px solid var(--line);color:var(--tx);border-radius:8px;padding:4px 8px;cursor:pointer}
header{padding:48px 0 16px}header h1{font-size:clamp(28px,5vw,46px);margin:0 0 12px}.lead{color:var(--mut);font-size:18px;max-width:760px}
.prompt{background:var(--card);border:1px solid var(--line);border-left:4px solid var(--amb);border-radius:10px;padding:14px 16px;font-family:'JetBrains Mono',monospace;font-size:15px;overflow-wrap:anywhere}
section{padding:28px 0}.mut{color:var(--mut)}
ul.como{padding-left:20px}ul.como li{margin:6px 0}
.podio{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;overflow:hidden}
.card img{width:100%;display:block;background:#fff;aspect-ratio:1}
.card .info{padding:12px 14px}.card .pos{font-family:Sora;font-size:28px;color:var(--amb);font-weight:800}
.card .nm{font-weight:700}.tag{display:inline-block;font-size:12px;border:1px solid var(--line);border-radius:99px;padding:1px 8px;color:var(--mut)}
.tag.Local{color:#4ade80;border-color:#166534}.tag.Anthropic{color:#f0a868;border-color:#7c4a1e}.tag.OpenAI{color:#7dd3fc;border-color:#1e4e6c}
.tbl{width:100%;border-collapse:collapse;font-size:15px}.tbl th,.tbl td{padding:8px 6px;border-bottom:1px solid var(--line);text-align:left;vertical-align:middle}
.tbl th{color:var(--mut);font-weight:600;font-size:13px}.tbl img{width:56px;height:56px;border-radius:6px;background:#fff;display:block}
.bar{height:8px;background:var(--line);border-radius:9px;min-width:60px}.bar i{display:block;height:100%;background:var(--amb);border-radius:9px}
.tblw{overflow-x:auto}
.duelo img{width:100%;border-radius:12px;border:1px solid var(--line)}
blockquote{margin:12px 0;padding:10px 16px;border-left:3px solid var(--amb);background:var(--card);border-radius:8px}
.gal{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:14px}
.gal .card .info{font-size:14px}.gal a{font-size:13px}
footer{border-top:1px solid var(--line);padding:24px 0 48px;color:var(--mut);font-size:14px}
@media(max-width:720px){.podio{grid-template-columns:1fr}.hide-m{display:none}nav .sec{display:none}}
"""


def pct(x):
    return f"{round((x or 0) * 100)}%"


def pagina(lg, dados, prompt, data):
    t = TXT[lg]
    pre = "" if lg == "pt" else "../"
    rk = dados["ranking"]
    validos = [r for r in rk if r["valido"]]
    n = len([r for r in rk if r["rodou"]])
    loc = len([r for r in rk if r["rodou"] and r["familia"] == "Local"])
    conc = dados.get("concordancia")
    conc_txt = (t["conc"].format(j2=dados["segundo_juiz"].split(":", 1)[1], p=conc["pares"], t=pct(conc["taxa"]))
                if conc else t["conc_nao"])
    itens = [s.format(n=n, loc=loc, nuv=n - loc, data=data, juiz=(dados["juiz"] or "").split(":", 1)[-1],
                      j=dados["julgamentos"], viesA=pct(dados["vies_lado_A"]), conc=conc_txt) for s in t["como_itens"]]

    def img(r):
        return f"{pre}png/{r['id']}.png"

    def fam(r):
        return f"<span class='tag {r['familia']}'>{t['fam'][r['familia']]}</span>"

    podio = "".join(
        f"<div class='card'><img src='{img(r)}' alt='{html.escape(r['rotulo'])}' loading='lazy'>"
        f"<div class='info'><div class='pos'>{r['posicao']}º</div><div class='nm'>{html.escape(r['rotulo'])}</div>"
        f"{fam(r)} <span class='mut'>{pct(r['taxa'])}</span></div></div>" for r in validos[:3])

    linhas = []
    for r in rk:
        if not r["rodou"]:
            continue
        if r["valido"]:
            linhas.append(
                f"<tr><td><b>{r['posicao']}</b></td><td><img src='{img(r)}' alt='' loading='lazy'></td>"
                f"<td><b>{html.escape(r['rotulo'])}</b><br><code class='mut'>{html.escape(r['modelo'])}</code></td>"
                f"<td>{fam(r)}</td><td>{r['vitorias']}/{r['confrontos']}</td>"
                f"<td><div class='bar'><i style='width:{pct(r['taxa'])}'></i></div>{pct(r['taxa'])}</td>"
                f"<td class='hide-m'>{r['elo']}</td><td class='hide-m'>{r['segundos']}{t['seg']}</td></tr>")
        else:
            linhas.append(
                f"<tr><td>–</td><td></td><td><b>{html.escape(r['rotulo'])}</b><br><code class='mut'>{html.escape(r['modelo'])}</code></td>"
                f"<td>{fam(r)}</td><td colspan='4' class='mut'>{t['sem']}</td></tr>")

    duelo = ""
    if len(validos) >= 2:
        a, b = validos[0]["id"], validos[-1]["id"]
        motivo = dados.get("duelo_motivo")
        duelo = (f"<section><h2>{t['duelo']}</h2><p class='mut'>{t['duelo_txt']}</p>"
                 f"<div class='duelo'><img src='{pre}pares/{a}__{b}.png' alt='' loading='lazy'></div>"
                 + (f"<blockquote>{html.escape(motivo)}{t['motivo_nota']}</blockquote>" if motivo else "") + "</section>")

    local = ""
    locs = [r for r in validos if r["familia"] == "Local"]
    nuvs = [r for r in validos if r["familia"] != "Local"]
    if locs and nuvs:
        local = (f"<section><h2>{t['local']}</h2><p>"
                 + t["local_txt"].format(m=html.escape(locs[0]["rotulo"]), p=locs[0]["posicao"], n=len(validos), pn=nuvs[-1]["posicao"])
                 + "</p></section>")

    gal = "".join(
        f"<div class='card'><img src='{img(r)}' alt='{html.escape(r['rotulo'])}' loading='lazy'><div class='info'>"
        f"<b>{r['posicao']}º</b> {html.escape(r['rotulo'])}<br>"
        f"<a href='{pre}svgs/{r['id']}.svg'>{t['svg']}</a> · <a href='{pre}respostas/{r['id']}.txt'>{t['resposta']}</a></div></div>"
        for r in validos)

    langs = "".join(f"<a href='{(pre + ('' if l == 'pt' else l + '/')) or './'}' class='{'on' if l == lg else ''}'>{l.upper()}</a>"
                    for l in ("pt", "en", "es"))
    guia = "../guia/" + ("" if lg == "pt" else f"{lg}/")
    guia = ("../" if lg != "pt" else "") + guia
    return f"""<!doctype html><html lang="{t['lang']}"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>{t['title']}</title>
<meta name="description" content="{html.escape(t['lead'].format(n=n))}">
<link rel="alternate" hreflang="pt-BR" href="https://inematds.github.io/arena-capivara/resultados/">
<link rel="alternate" hreflang="en" href="https://inematds.github.io/arena-capivara/resultados/en/">
<link rel="alternate" hreflang="es" href="https://inematds.github.io/arena-capivara/resultados/es/">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Sora:wght@700;800&family=JetBrains+Mono&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>
<nav><div class="wrap"><a class="logo" href="{guia}">🦫 Arena da Capivara</a><span class="mut">|</span>
<a class="inema" href="https://inema.club" target="_blank">INEMA.CLUB</a><span class="mut">-</span><a class="pro" href="https://inema.pro" target="_blank">PRO</a>
<span class="sp"></span><a class="sec" href="{guia}">{t['guia']}</a><span class="lang">{langs}</span>
<button id="tg" aria-label="tema">🌙</button></div></nav>
<header class="wrap"><h1>{t['h1']}</h1><p class="lead">{t['lead'].format(n=n)}</p>
<h3>{t['prompt']}</h3><div class="prompt">{html.escape(prompt)}</div></header>
<main class="wrap">
<section><h2>{t['podio']}</h2><div class="podio">{podio}</div></section>
<section><h2>{t['como']}</h2><ul class="como">{''.join(f'<li>{i}</li>' for i in itens)}</ul></section>
<section><h2>{t['ranking']}</h2><div class="tblw"><table class="tbl"><thead><tr>{''.join(f"<th class='{'hide-m' if i > 5 else ''}'>{c}</th>" for i, c in enumerate(t['cols']))}</tr></thead>
<tbody>{''.join(linhas)}</tbody></table></div></section>
{local}{duelo}
<section><h2>{t['galeria']}</h2><div class="gal">{gal}</div></section>
</main>
<footer class="wrap">{t['rodape']} <a href="https://github.com/inematds/arena-capivara">github.com/inematds/arena-capivara</a> · <a href="{guia}">{t['guia']}</a> · <a href="https://inema.club" target="_blank" style="color:var(--sky)">INEMA.CLUB</a></footer>
<script>
const tgBtn=document.getElementById('tg');
function aplicaTema(l){{document.body.classList.toggle('light',l);tgBtn.textContent=l?'☀️':'🌙'}}
try{{aplicaTema(localStorage.getItem('tema')==='light')}}catch(e){{}}
tgBtn.onclick=()=>{{const l=!document.body.classList.contains('light');aplicaTema(l);try{{localStorage.setItem('tema',l?'light':'dark')}}catch(e){{}}}};
</script></body></html>"""


def main():
    dados = json.loads((RES / "ranking.json").read_text())
    validos = [r for r in dados["ranking"] if r["valido"]]
    if len(validos) >= 2:
        a, b = validos[0]["id"], validos[-1]["id"]
        for linha in (RES / "julgamentos.jsonl").read_text().splitlines():
            j = json.loads(linha)
            if j["a"] == a and j["b"] == b and j.get("motivo"):
                dados["duelo_motivo"] = j["motivo"]
    prompt = (ARENA / "prompt.txt").read_text().strip()
    datas = []
    for r in dados["ranking"]:
        arq = RES / "respostas" / f"{r['id']}.json"
        if arq.exists():
            datas.append(json.loads(arq.read_text())["data"][:10])
    data = max(datas) if datas else ""
    data_fmt = "/".join(reversed(data.split("-"))) if data else ""
    (RES / "index.html").write_text(pagina("pt", dados, prompt, data_fmt))
    for lg in ("en", "es"):
        (RES / lg).mkdir(exist_ok=True)
        (RES / lg / "index.html").write_text(pagina(lg, dados, prompt, data))
    print("resultados/index.html + en/ + es/ gerados")


if __name__ == "__main__":
    main()
