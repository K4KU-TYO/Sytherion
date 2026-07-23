"""
Application / Orquestrador com Persistência (Decorator)
-----------------------------------------------------------
Envolve um Orquestrador comum para adicionar persistência em disco,
sem alterar a classe original: ao registrar uma IA, restaura o
conhecimento salvo; ao aprender algo novo, salva de novo.
"""
from __future__ import annotations

from typing import List, Optional

from sytherion.core.interfaces import IIA, IOrquestrador, IRepositorioConhecimento, Mensagem, TipoMensagem


class OrquestradorComPersistencia(IOrquestrador):
    def __init__(self, interno: IOrquestrador, repositorio: IRepositorioConhecimento) -> None:
        self._interno = interno
        self._repo = repositorio

    def registrar_ia(self, ia: IIA) -> None:
        self._interno.registrar_ia(ia)
        if hasattr(ia, "importar_estado"):
            estado_salvo = self._repo.carregar(ia.get_nome())
            if estado_salvo:
                ia.importar_estado(estado_salvo)

    def get_ia(self, nome: str) -> Optional[IIA]:
        return self._interno.get_ia(nome)

    def rotear(self, pergunta: str, dominio: Optional[str] = None) -> Mensagem:
        return self._interno.rotear(pergunta, dominio)

    def selecionar_especialista(self, pergunta: str) -> Optional[IIA]:
        return self._interno.selecionar_especialista(pergunta)

    def listar_ias(self) -> List[str]:
        return self._interno.listar_ias()

    def alimentar_ia(self, nome_ia: str, caminho_arquivo: str) -> Mensagem:
        msg = self._interno.alimentar_ia(nome_ia, caminho_arquivo)
        if msg.tipo == TipoMensagem.APRENDIZADO:
            ia = self._interno.get_ia(nome_ia)
            if ia is not None and hasattr(ia, "exportar_estado"):
                self._repo.salvar(nome_ia, ia.exportar_estado())
        return msg
