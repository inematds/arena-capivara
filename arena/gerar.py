#!/usr/bin/env python3
"""Passo 1: pede a capivara de bicicleta a cada competidor e guarda o SVG.

Uso:
  python3 arena/gerar.py                 # todos de modelos.json (pula os que já têm resultado)
  python3 arena/gerar.py --so llama3-2-3b claude-haiku-4-5
  python3 arena/gerar.py --refazer       # gera de novo mesmo se já existe
  python3 arena/gerar.py --paralelo 3    # roda claude/codex em paralelo (ollama sempre um por vez)
"""
import argparse
import datetime as dt
import json
import time
from concurrent.futures import ThreadPoolExecutor

from comum import ARENA, RES, competidores, extrair_svg, rodar


def gerar_um(comp, prompt, refazer):
    meta_arq = RES / "respostas" / f"{comp['id']}.json"
    if meta_arq.exists() and not refazer:
        print(f"[pula] {comp['id']} (já existe)")
        return
    print(f"[gera] {comp['id']} ({comp['motor']}:{comp['modelo']}) ...", flush=True)
    inicio = time.time()
    erro, texto = None, ""
    try:
        texto = rodar(comp, prompt)
    except Exception as e:  # falha do motor ≠ "não soube desenhar"
        erro = str(e)
    svg = extrair_svg(texto)
    segundos = round(time.time() - inicio, 1)
    (RES / "respostas" / f"{comp['id']}.txt").write_text(texto or "")
    svg_arq = RES / "svgs" / f"{comp['id']}.svg"
    if svg:
        svg_arq.write_text(svg)
    elif svg_arq.exists():
        svg_arq.unlink()
    meta = {**comp, "segundos": segundos, "tem_svg": bool(svg), "erro": erro,
            "bytes_svg": len(svg or ""), "data": dt.datetime.now().isoformat(timespec="seconds")}
    meta_arq.write_text(json.dumps(meta, ensure_ascii=False, indent=2))
    status = "ok" if svg else ("ERRO " + erro[:120] if erro else "sem SVG na resposta")
    print(f"[fim ] {comp['id']}: {status} em {segundos}s", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--so", nargs="*")
    ap.add_argument("--refazer", action="store_true")
    ap.add_argument("--paralelo", type=int, default=3)
    a = ap.parse_args()
    prompt = (ARENA / "prompt.txt").read_text().strip()
    comps = competidores(a.so)
    locais = [c for c in comps if c["motor"] == "ollama"]
    nuvem = [c for c in comps if c["motor"] != "ollama"]
    with ThreadPoolExecutor(max_workers=max(1, a.paralelo)) as ex:
        futuros = [ex.submit(gerar_um, c, prompt, a.refazer) for c in nuvem]
        for c in locais:  # memória: um peso local por vez
            gerar_um(c, prompt, a.refazer)
        for f in futuros:
            f.result()


if __name__ == "__main__":
    main()
