"""Funções compartilhadas da Arena da Capivara."""
import json
import os
import re
import subprocess
import tempfile
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ARENA = RAIZ / "arena"
RES = RAIZ / "resultados"
OLLAMA = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434")


def competidores(filtro=None):
    dados = json.loads((ARENA / "modelos.json").read_text())["competidores"]
    if filtro:
        dados = [c for c in dados if c["id"] in filtro]
    return dados


def extrair_svg(texto):
    """Tira <think>, cercas de código e devolve só o primeiro <svg>...</svg> (ou None)."""
    if not texto:
        return None
    texto = re.sub(r"<think>[\s\S]*?</think>", "", texto)
    m = re.search(r"<svg[\s\S]*?</svg>", texto, re.IGNORECASE)
    return m.group(0) if m else None


def rodar_ollama(modelo, prompt, timeout=900):
    corpo = json.dumps({
        "model": modelo, "prompt": prompt, "stream": False,
        "keep_alive": 0,  # descarrega ao terminar: um modelo grande por vez
        "options": {"num_predict": 8192, "temperature": 0.7},
    }).encode()
    req = urllib.request.Request(f"{OLLAMA}/api/generate", data=corpo,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())["response"]


def rodar_claude(modelo, prompt, timeout=600, ferramentas="", imagem=None):
    """claude -p limpo: sem hooks, plugins, MCP nem skills do usuário. Usa a assinatura logada."""
    cmd = ["claude", "-p", prompt, "--model", modelo,
           "--setting-sources", "", "--strict-mcp-config", "--disable-slash-commands",
           "--no-session-persistence", "--system-prompt", "Você é um assistente.",
           "--tools", ferramentas]
    if ferramentas:
        cmd += ["--allowedTools", ferramentas]
    with tempfile.TemporaryDirectory() as tmp:
        cwd = Path(imagem).parent if imagem else tmp
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout,
                           cwd=cwd, stdin=subprocess.DEVNULL)
    if r.returncode != 0:
        raise RuntimeError(f"claude saiu {r.returncode}: {r.stderr[-400:]}")
    return r.stdout


def rodar_codex(modelo, prompt, timeout=900, imagem=None, esforco="medium"):
    """codex exec pela assinatura, só leitura, última mensagem em arquivo."""
    with tempfile.TemporaryDirectory() as tmp:
        saida = Path(tmp) / "ultima.txt"
        cmd = ["codex", "exec", "-m", modelo, "-s", "read-only", "--skip-git-repo-check",
               "-c", f"model_reasoning_effort={esforco}", "-o", str(saida)]
        if imagem:
            cmd += ["-i", str(imagem)]
        cmd.append("-")
        r = subprocess.run(cmd, input=prompt, capture_output=True, text=True,
                           timeout=timeout, cwd=tmp)
        if r.returncode != 0 or not saida.exists():
            raise RuntimeError(f"codex saiu {r.returncode}: {r.stderr[-400:]}")
        return saida.read_text()


def rodar(comp, prompt, **kw):
    motor = comp["motor"]
    if motor == "ollama":
        return rodar_ollama(comp["modelo"], prompt)
    if motor == "claude":
        return rodar_claude(comp["modelo"], prompt, **kw)
    if motor == "codex":
        return rodar_codex(comp["modelo"], prompt, **kw)
    raise ValueError(f"motor desconhecido: {motor}")
