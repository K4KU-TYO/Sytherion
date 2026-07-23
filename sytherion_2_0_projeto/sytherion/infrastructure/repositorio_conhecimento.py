"""
Infrastructure / Repositório de Conhecimento
-------------------------------------------------
Salva e carrega o conhecimento aprendido de cada IA como JSON, um
arquivo por especialista, em sytherion_data/conhecimento/.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Dict

from sytherion.core.interfaces import IRepositorioConhecimento

_NOME_SEGURO_RE = re.compile(r"[^a-zA-Z0-9_-]+")


class RepositorioConhecimentoJSON(IRepositorioConhecimento):
    def __init__(self, diretorio: str = "sytherion_data/conhecimento") -> None:
        self._diretorio = Path(diretorio)
        self._diretorio.mkdir(parents=True, exist_ok=True)

    def _caminho(self, nome_ia: str) -> Path:
        nome_seguro = _NOME_SEGURO_RE.sub("_", nome_ia)
        return self._diretorio / f"{nome_seguro}.json"

    def carregar(self, nome_ia: str) -> Dict[str, str]:
        caminho = self._caminho(nome_ia)
        if not caminho.exists():
            return {}
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                dados = json.load(f)
            return dados if isinstance(dados, dict) else {}
        except (json.JSONDecodeError, OSError):
            return {}

    def salvar(self, nome_ia: str, dados: Dict[str, str]) -> None:
        caminho = self._caminho(nome_ia)
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=2, ensure_ascii=False)
