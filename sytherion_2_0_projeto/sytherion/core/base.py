"""
Core / Base
------------
Classe base de todas as IAs especialistas (Template Method):
`responder()` é fixo, `_processar()` é o hook que cada IA implementa.
Adicionar uma IA nova nunca exige alterar esta classe.
"""
from __future__ import annotations

import re
from abc import abstractmethod
from typing import Any, Dict, List, Optional

from sytherion.core.interfaces import IIAComAprendizado, IIAComBuscaConhecimento, IIAComExtras, IIAComExportacao, IIAPersistivel
from sytherion.core.texto_utils import contem_palavra_chave, normalizar_texto

_TOKEN_RE = re.compile(r"[a-zA-ZÀ-ÿ]{3,}")


class IASytherion(IIAComAprendizado, IIAComExtras, IIAComExportacao, IIAPersistivel, IIAComBuscaConhecimento):
    """Base abstrata de todas as IAs especialistas do ecossistema."""

    def __init__(
        self,
        nome: str,
        dominio: str,
        palavras_chave: Optional[List[str]] = None,
        conhecimento_inicial: Optional[Dict[str, str]] = None,
    ) -> None:
        self._nome = nome
        self._dominio = dominio
        self._palavras_chave = palavras_chave or []
        self._base_conhecimento: Dict[str, str] = dict(conhecimento_inicial or {})
        self._historico: List[Dict[str, str]] = []
        self._total_consultas = 0
        self._total_aprendizados = 0

    # ---------------------------------------------------------------- IIA --
    def get_nome(self) -> str:
        return self._nome

    def get_dominio(self) -> str:
        return self._dominio

    def get_palavras_chave(self) -> List[str]:
        return list(self._palavras_chave)

    def responder(self, pergunta: str) -> str:
        """Template Method: fluxo fixo, não sobrescrever."""
        self._total_consultas += 1
        contexto = self._buscar_conhecimento(pergunta)
        resposta = self._processar(pergunta, contexto)
        self._historico.append({"pergunta": pergunta, "resposta": resposta})
        return resposta

    @abstractmethod
    def _processar(self, pergunta: str, contexto: List[str]) -> str:
        """Hook method: cada IA especialista define sua lógica de domínio aqui."""
        raise NotImplementedError

    # ------------------------------------------------- IIAComAprendizado --
    def aprender(self, conhecimento: str, fonte: str = "manual") -> int:
        adicionados = 0
        for linha in (l.strip() for l in conhecimento.split("\n")):
            if not linha or len(linha) < 5:
                continue
            chave = self._extrair_chave(linha)
            if chave and chave not in self._base_conhecimento:
                self._base_conhecimento[chave] = linha
                adicionados += 1
        self._total_aprendizados += adicionados
        return adicionados

    @staticmethod
    def _extrair_chave(linha: str) -> str:
        palavras = _TOKEN_RE.findall(linha.lower())
        return palavras[0] if palavras else ""

    def _buscar_conhecimento(self, pergunta: str, limite: int = 5) -> List[str]:
        termos = set(_TOKEN_RE.findall(normalizar_texto(pergunta)))
        if not termos:
            return []
        achados = [
            valor
            for chave, valor in self._base_conhecimento.items()
            if normalizar_texto(chave) in termos
            or any(contem_palavra_chave(normalizar_texto(valor), t) for t in termos)
        ]
        return achados[:limite]

    _CONECTORES = ["", "Além disso, ", "Complementando, ", "Também vale destacar que ", "Reforçando, "]

    def _sintetizar_resposta(self, contexto: List[str]) -> str:
        """Combina o conhecimento aprendido em um parágrafo corrido, não em bullets crus."""
        partes = []
        for i, frase in enumerate(contexto):
            frase = frase.strip()
            if not frase:
                continue
            if frase[-1] not in ".!?":
                frase += "."
            conector = self._CONECTORES[i % len(self._CONECTORES)]
            partes.append(f"{conector}{frase}")
        corpo = " ".join(partes)
        return f"[{self._nome}] Baseado no que aprendi sobre {self._dominio.lower()}, posso te dizer o seguinte: {corpo}"

    # ------------------------------------------------------ IIAComExtras --
    def get_estatisticas(self) -> Dict[str, Any]:
        return {
            "nome": self._nome,
            "dominio": self._dominio,
            "consultas_realizadas": self._total_consultas,
            "itens_conhecimento": len(self._base_conhecimento),
            "aprendizados_totais": self._total_aprendizados,
            "palavras_chave": self._palavras_chave,
        }

    # -------------------------------------------------- IIAComExportacao --
    def exportar_conhecimento(self) -> str:
        linhas = [f"# Base de Conhecimento — {self._nome} ({self._dominio})", ""]
        if not self._base_conhecimento:
            linhas.append("_(nenhum conhecimento adicional aprendido ainda)_")
        for chave, valor in sorted(self._base_conhecimento.items()):
            linhas.append(f"- **{chave}**: {valor}")
        return "\n".join(linhas)

    # --------------------------------------------------- IIAPersistivel --
    def exportar_estado(self) -> Dict[str, str]:
        """Dados brutos (chave -> conhecimento) prontos para serialização em JSON."""
        return dict(self._base_conhecimento)

    def importar_estado(self, dados: Dict[str, str]) -> None:
        """Restaura conhecimento salvo anteriormente, sem contar como 'aprendizado novo'."""
        for chave, valor in dados.items():
            self._base_conhecimento.setdefault(chave, valor)

    # ----------------------------------------- IIAComBuscaConhecimento --
    def contar_correspondencias(self, pergunta: str) -> int:
        """Quantos itens aprendidos combinam com a pergunta — usado no roteamento."""
        return len(self._buscar_conhecimento(pergunta, limite=1000))
