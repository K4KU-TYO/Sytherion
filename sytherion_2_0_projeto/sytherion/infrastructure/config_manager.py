"""Configuração persistente em JSON."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from sytherion.core.interfaces import IConfigManager

_PADRAO: Dict[str, Any] = {
    "log_arquivo": "sytherion_data/logs/sytherion.log",
    "diretorio_exportacao": "sytherion_data/exports",
    "diretorio_uploads": "sytherion_data/uploads",
    "banner_animado": True,
}


class ConfigManager(IConfigManager):
    def __init__(self, caminho: str = "sytherion_data/config.json") -> None:
        self._caminho = Path(caminho)
        self._dados: Dict[str, Any] = dict(_PADRAO)
        self._carregar()

    def _carregar(self) -> None:
        if self._caminho.exists():
            try:
                with open(self._caminho, "r", encoding="utf-8") as f:
                    self._dados.update(json.load(f))
            except (json.JSONDecodeError, OSError):
                pass
        else:
            self.salvar()

    def obter(self, chave: str, padrao: Any = None) -> Any:
        return self._dados.get(chave, padrao)

    def definir(self, chave: str, valor: Any) -> None:
        self._dados[chave] = valor

    def salvar(self) -> None:
        self._caminho.parent.mkdir(parents=True, exist_ok=True)
        with open(self._caminho, "w", encoding="utf-8") as f:
            json.dump(self._dados, f, indent=2, ensure_ascii=False)
