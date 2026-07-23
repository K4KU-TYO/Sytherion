"""
Infrastructure / Repositório de Preferências
-------------------------------------------------
Salva o tema ativo e os temas customizados criados pelo usuário em
sytherion_data/preferencias.json.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from sytherion.core.interfaces import IRepositorioPreferencias

_PADRAO: Dict[str, Any] = {
    "tema_ativo": "matrix",
    "temas_customizados": {},
}


class RepositorioPreferenciasJSON(IRepositorioPreferencias):
    def __init__(self, caminho: str = "sytherion_data/preferencias.json") -> None:
        self._caminho = Path(caminho)
        self._caminho.parent.mkdir(parents=True, exist_ok=True)

    def carregar(self) -> Dict[str, Any]:
        if not self._caminho.exists():
            return dict(_PADRAO)
        try:
            with open(self._caminho, "r", encoding="utf-8") as f:
                dados = json.load(f)
            if not isinstance(dados, dict):
                return dict(_PADRAO)
            resultado = dict(_PADRAO)
            resultado.update(dados)
            return resultado
        except (json.JSONDecodeError, OSError):
            return dict(_PADRAO)

    def salvar(self, dados: Dict[str, Any]) -> None:
        with open(self._caminho, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=2, ensure_ascii=False)
