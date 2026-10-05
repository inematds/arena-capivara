#!/usr/bin/env python3
"""Passo 2: SVG -> PNG (512px) e monta as imagens de confronto A|B para o juiz.

Uso: python3 arena/renderizar.py
"""
import itertools
import json
import re

import cairosvg
from PIL import Image, ImageDraw, ImageFont

from comum import RES, competidores

LADO = 512


def sem_rede(svg_texto):
    """SVG pode apontar para imagem/fonte externa: a Arena não busca nada fora (só data:)."""
    return re.sub(r'(href\s*=\s*["\'])(?!data:|#)[^"\']*', r"\1#", svg_texto)


def renderizar(cid):
    svg = RES / "svgs" / f"{cid}.svg"
    png = RES / "png" / f"{cid}.png"
    try:
        tmp = RES / "png" / f"{cid}.tmp.png"
        cairosvg.svg2png(bytestring=sem_rede(svg.read_text()).encode(), write_to=str(tmp),
                         output_width=LADO, unsafe=False)
        fundo = Image.new("RGB", (LADO, LADO), "white")
        img = Image.open(tmp).convert("RGBA")
        img.thumbnail((LADO, LADO))
        fundo.paste(img, ((LADO - img.width) // 2, (LADO - img.height) // 2), img)
        fundo.save(png)
        tmp.unlink()
        return True
    except Exception as e:
        print(f"[falha render] {cid}: {e}")
        return False


def fonte(tam):
    for f in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]:
        try:
            return ImageFont.truetype(f, tam)
        except OSError:
            pass
    return ImageFont.load_default()


def confronto(a, b):
    """Imagem lado a lado com rótulos neutros A e B (o juiz não vê o nome do modelo)."""
    img = Image.new("RGB", (LADO * 2 + 30, LADO + 60), "#dddddd")
    d = ImageDraw.Draw(img)
    for i, cid in enumerate((a, b)):
        x = i * (LADO + 30)
        img.paste(Image.open(RES / "png" / f"{cid}.png"), (x, 60))
        d.text((x + LADO // 2 - 10, 10), "AB"[i], fill="black", font=fonte(36))
    nome = RES / "pares" / f"{a}__{b}.png"
    img.save(nome)
    return nome


def main():
    validos = []
    for c in competidores():
        meta = RES / "respostas" / f"{c['id']}.json"
        if not meta.exists():
            continue
        m = json.loads(meta.read_text())
        ok = m["tem_svg"] and renderizar(c["id"])
        m["renderizou"] = bool(ok)
        meta.write_text(json.dumps(m, ensure_ascii=False, indent=2))
        if ok:
            validos.append(c["id"])
    n = 0
    for a, b in itertools.combinations(validos, 2):
        confronto(a, b)
        confronto(b, a)  # as duas ordens, contra viés de posição
        n += 2
    print(f"{len(validos)} imagens válidas, {n} confrontos montados")


if __name__ == "__main__":
    main()
