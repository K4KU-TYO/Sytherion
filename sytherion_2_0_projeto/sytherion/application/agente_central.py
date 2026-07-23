"""
Application / Agente Central
--------------------------------
Único ponto que Terminal e API conversam diretamente. Escolhe o
especialista (via Analisador de Intenção), deixa ele responder, e
passa o resultado pelos outros 3 agentes auxiliares.
"""
from __future__ import annotations

import random
from typing import Dict, List, Optional

from sytherion.core.interfaces import IAgenteAuxiliar, IAgenteCentral, PacotePipeline

_SEM_ESPECIALISTA_VARIACOES = [
    "Nenhum dos 40 especialistas tem conhecimento relacionado a essa pergunta ainda. "
    "Tente palavras mais específicas, ou ensine um especialista sobre o assunto "
    "(clipe de anexo no chat, ou opção 4 no terminal).",
    "Não encontrei, entre os 40 especialistas, nenhum com conhecimento sobre isso. "
    "Pode reformular com termos mais específicos, ou ensinar um deles sobre o tema primeiro.",
    "Essa pergunta não bateu com nenhum dos 40 especialistas ainda. "
    "Uma reformulação mais específica pode ajudar, ou você pode ensinar um deles sobre o assunto.",
]


class AgenteCentral(IAgenteCentral):
    def __init__(self, pipeline: List[IAgenteAuxiliar]) -> None:
        if not pipeline:
            raise ValueError("AgenteCentral precisa de ao menos 1 agente auxiliar (o Analisador de Intenção).")
        self._pipeline = pipeline

    def responder(self, pergunta: str, historico: Optional[List[Dict[str, str]]] = None) -> PacotePipeline:
        pacote = PacotePipeline(pergunta=pergunta, historico=historico or [])

        analisador, *auxiliares_restantes = self._pipeline
        pacote = analisador.processar(pacote)  # decide o especialista

        if pacote.especialista is not None:
            pacote.rascunho = pacote.especialista.responder(pergunta)  # especialista atua sozinho
        else:
            pacote.rascunho = random.choice(_SEM_ESPECIALISTA_VARIACOES)

        for auxiliar in auxiliares_restantes:
            pacote = auxiliar.processar(pacote)

        return pacote
