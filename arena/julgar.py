#!/usr/bin/env python3
"""Passo 3: um modelo-juiz olha cada confronto A|B e escolhe o melhor desenho.

O juiz não sabe quais modelos fizeram cada imagem. Cada par é julgado nas duas ordens.

Uso:
  python3 arena/julgar.py                                   # juiz padrão: Claude Sonnet 5.5
  python3 arena/julgar.py --juiz codex --modelo gpt-6-luna --amostra 60   # 2º juiz, para medir concordância
  python3 arena/julgar.py --paralelo 4
"""
import argparse
import json
import random
import re
import threading
from concurrent.futures import ThreadPoolExecutor

from comum import RES, rodar_claude, rodar_codex

PERGUNTA = """A imagem mostra dois desenhos lado a lado, marcados A (esquerda) e B (direita).
Os dois tentam ilustrar "uma capivara andando de bicicleta".
Escolha o que ilustra melhor isso: a capivara é reconhecível? a bicicleta é reconhecível?
ela está de fato andando na bicicleta? o conjunto é bem resolvido?
Responda SOMENTE com JSON, sem mais nada: {"vencedor": "A" ou "B", "motivo": "uma frase em português"}"""

trava = threading.Lock()


def ler_veredito(texto):
    m = re.search(r"\{[^{}]*\"vencedor\"[^{}]*\}", texto or "", re.S)
    if not m:
        return None, None
    try:
        d = json.loads(m.group(0))
    except json.JSONDecodeError:
        v = re.search(r"\"vencedor\"\s*:\s*\"([AB])\"", m.group(0))
        return (v.group(1) if v else None), None
    v = str(d.get("vencedor", "")).strip().upper()[:1]
    return (v if v in "AB" else None), d.get("motivo")


def julgar(par, juiz, modelo, saida):
    a, b = par.stem.split("__")
    for tentativa in range(2):
        try:
            if juiz == "claude":
                pedido = f"Leia a imagem {par.name} (use a ferramenta Read).\n\n{PERGUNTA}"
                texto = rodar_claude(modelo, pedido, ferramentas="Read", imagem=par)
            else:
                texto = rodar_codex(modelo, PERGUNTA, imagem=par, esforco="low")
        except Exception as e:
            texto = f"ERRO {e}"
        v, motivo = ler_veredito(texto)
        if v:
            break
    reg = {"a": a, "b": b, "juiz": f"{juiz}:{modelo}", "vencedor_lado": v,
           "vencedor": {"A": a, "B": b}.get(v), "motivo": motivo,
           "bruto": None if v else (texto or "")[-300:]}
    with trava, open(saida, "a") as f:
        f.write(json.dumps(reg, ensure_ascii=False) + "\n")
    print(f"{a} x {b}: {v or 'SEM VEREDITO'}", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--juiz", default="claude", choices=["claude", "codex"])
    ap.add_argument("--modelo", default=None)
    ap.add_argument("--amostra", type=int, default=0, help="julga só N confrontos sorteados")
    ap.add_argument("--paralelo", type=int, default=4)
    a = ap.parse_args()
    modelo = a.modelo or ("claude-sonnet-5-5" if a.juiz == "claude" else "gpt-6-luna")
    saida = RES / ("julgamentos.jsonl" if a.juiz == "claude" else f"julgamentos-{a.juiz}.jsonl")
    feitos = set()
    if saida.exists():
        for linha in saida.read_text().splitlines():
            r = json.loads(linha)
            if r["vencedor"]:
                feitos.add(f"{r['a']}__{r['b']}")
    pares = sorted(p for p in (RES / "pares").glob("*.png") if p.stem not in feitos)
    if a.amostra:
        random.seed(42)
        pares = random.sample(pares, min(a.amostra, len(pares)))
    print(f"juiz {a.juiz}:{modelo} — {len(pares)} confrontos a julgar")
    with ThreadPoolExecutor(max_workers=a.paralelo) as ex:
        list(ex.map(lambda p: julgar(p, a.juiz, modelo, saida), pares))


if __name__ == "__main__":
    main()
