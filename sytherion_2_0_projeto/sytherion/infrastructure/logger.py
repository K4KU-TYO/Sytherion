"""Logger com saída colorida no terminal."""
from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Optional

from sytherion.core.interfaces import ILogger


class Cores:
    VERDE = "\033[92m"
    VERDE_ESCURO = "\033[32m"
    CIANO = "\033[96m"
    AMARELO = "\033[93m"
    VERMELHO = "\033[91m"
    CINZA = "\033[90m"
    NEGRITO = "\033[1m"
    RESET = "\033[0m"


class LoggerSytherion(ILogger):
    def __init__(self, caminho_arquivo: Optional[str] = None) -> None:
        self._caminho_arquivo = Path(caminho_arquivo) if caminho_arquivo else None
        if self._caminho_arquivo:
            self._caminho_arquivo.parent.mkdir(parents=True, exist_ok=True)

    def _timestamp(self) -> str:
        return datetime.now().strftime("%H:%M:%S")

    def _escrever(self, linha_tela: str, linha_arquivo: str) -> None:
        print(linha_tela)
        if self._caminho_arquivo:
            with open(self._caminho_arquivo, "a", encoding="utf-8") as f:
                f.write(linha_arquivo + "\n")

    def info(self, msg: str) -> None:
        self._escrever(f"{Cores.CINZA}[{self._timestamp()}] [INFO]{Cores.RESET} {msg}", f"[{self._timestamp()}] [INFO] {msg}")

    def sucesso(self, msg: str) -> None:
        self._escrever(f"{Cores.VERDE}[{self._timestamp()}] [OK]{Cores.RESET} {msg}", f"[{self._timestamp()}] [OK] {msg}")

    def aviso(self, msg: str) -> None:
        self._escrever(f"{Cores.AMARELO}[{self._timestamp()}] [AVISO]{Cores.RESET} {msg}", f"[{self._timestamp()}] [AVISO] {msg}")

    def erro(self, msg: str) -> None:
        self._escrever(f"{Cores.VERMELHO}[{self._timestamp()}] [ERRO]{Cores.RESET} {msg}", f"[{self._timestamp()}] [ERRO] {msg}")

    def evento(self, origem: str, msg: str) -> None:
        self._escrever(f"{Cores.CIANO}[{self._timestamp()}] [{origem}]{Cores.RESET} {msg}", f"[{self._timestamp()}] [{origem}] {msg}")
