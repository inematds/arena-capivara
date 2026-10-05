#!/usr/bin/env python3
"""Passo 4: transforma os julgamentos em ranking.

Mostra três números por modelo:
- vitórias/confrontos (taxa bruta: o mais honesto)
- ELO médio de 200 ordens embaralhadas (ELO de uma passada só depende da ordem)
- concordância com o 2º juiz, se houver julgamentos-codex.jsonl

Uso: python3 arena/ranking.py --tabela     (grava resultados/ranking.json)
"""
import argparse
import json
import random
from collections import defaultdict

from comum import RES, competidores


def carregar(nome):
    arq = RES / nome
    if not arq.exists():
        return []
    regs = [json.loads(l) for l in arq.read_text().splitlines() if l.strip()]
    return [r for r in regs if r["vencedor"]]


def elo(jogos, k=24, rodadas=200):
    soma = defaultdict(float)
    rnd = random.Random(7)
    for _ in range(rodadas):
        r = defaultdict(lambda: 1000.0)
        ordem = jogos[:]
        rnd.shuffle(ordem)
        for j in ordem:
            v = j["vencedor"]
            p = j["b"] if v == j["a"] else j["a"]
            esperado = 1 / (1 + 10 ** ((r[p] - r[v]) / 400))
            r[v] += k * (1 - esperado)
            r[p] -= k * (1 - esperado)
        for m, x in r.items():
            soma[m] += x
    return {m: s / rodadas for m, s in soma.items()}


def concordancia(principal, segundo):
    idx = {(r["a"], r["b"]): r["vencedor"] for r in principal}
    comuns = [(idx[(r["a"], r["b"])], r["vencedor"]) for r in segundo if (r["a"], r["b"]) in idx]
    if not comuns:
        return None
    iguais = sum(1 for x, y in comuns if x == y)
    return {"pares": len(comuns), "iguais": iguais, "taxa": round(iguais / len(comuns), 3)}


def vies_posicao(jogos):
    if not jogos:
        return None
    return round(sum(1 for j in jogos if j["vencedor_lado"] == "A") / len(jogos), 3)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tabela", action="store_true")
    a = ap.parse_args()
    jogos = carregar("julgamentos.jsonl")
    segundo = carregar("julgamentos-codex.jsonl")
    vit, tot = defaultdict(int), defaultdict(int)
    for j in jogos:
        tot[j["a"]] += 1
        tot[j["b"]] += 1
        vit[j["vencedor"]] += 1
    notas = elo(jogos)
    info = {c["id"]: c for c in competidores()}
    linhas = []
    for c in competidores():
        meta_arq = RES / "respostas" / f"{c['id']}.json"
        meta = json.loads(meta_arq.read_text()) if meta_arq.exists() else {}
        linhas.append({
            "id": c["id"], "rotulo": c["rotulo"], "familia": c["familia"],
            "motor": c["motor"], "modelo": c["modelo"],
            "valido": bool(meta.get("renderizou")), "rodou": bool(meta),
            "segundos": meta.get("segundos"), "erro": meta.get("erro"),
            "vitorias": vit[c["id"]], "confrontos": tot[c["id"]],
            "taxa": round(vit[c["id"]] / tot[c["id"]], 3) if tot[c["id"]] else 0.0,
            "elo": round(notas.get(c["id"], 0)) if c["id"] in notas else None,
        })
    linhas.sort(key=lambda x: (x["valido"], x["taxa"], x["elo"] or 0), reverse=True)
    for i, l in enumerate(linhas, 1):
        l["posicao"] = i if l["valido"] else None
    resumo = {
        "juiz": jogos[0]["juiz"] if jogos else None,
        "julgamentos": len(jogos),
        "vies_lado_A": vies_posicao(jogos),
        "segundo_juiz": segundo[0]["juiz"] if segundo else None,
        "concordancia": concordancia(jogos, segundo),
        "ranking": linhas,
    }
    (RES / "ranking.json").write_text(json.dumps(resumo, ensure_ascii=False, indent=2))
    if a.tabela:
        print(f"juiz: {resumo['juiz']} | julgamentos: {len(jogos)} | lado A venceu {resumo['vies_lado_A']}")
        if resumo["concordancia"]:
            print(f"concordância com {resumo['segundo_juiz']}: {resumo['concordancia']}")
        print(f"{'#':>2} {'modelo':<20} {'família':<10} {'vit/conf':>9} {'taxa':>6} {'ELO':>6}")
        for l in linhas:
            pos = l["posicao"] or "-"
            vc = f"{l['vitorias']}/{l['confrontos']}"
            print(f"{pos:>2} {l['rotulo']:<20} {l['familia']:<10} {vc:>9} {l['taxa']:>6.0%} {str(l['elo'] or '-'):>6}"
                  + ("" if l["valido"] else ("  (sem SVG válido)" if l["rodou"] else "  (não rodou)")))


if __name__ == "__main__":
    main()
