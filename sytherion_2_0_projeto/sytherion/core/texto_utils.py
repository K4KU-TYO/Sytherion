"""Funções de texto compartilhadas para o roteamento por palavra-chave."""
from __future__ import annotations

import re
import unicodedata


def normalizar_texto(texto: str) -> str:
    """Remove acentos e caixa alta. 'Existência' -> 'existencia'."""
    sem_acento = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("ascii")
    return sem_acento.lower()


def contem_palavra_chave(texto_normalizado: str, palavra_chave_normalizada: str) -> bool:
    """Verifica se a palavra-chave aparece como palavra inteira, não como substring solta."""
    padrao = r"\b" + re.escape(palavra_chave_normalizada) + r"\b"
    return re.search(padrao, texto_normalizado) is not None
