"""
Application / Orquestrador
----------------------------
Registra as IAs e decide qual delas responde cada pergunta. Não conhece
implementações concretas, só as interfaces (DIP).
"""
from __future__ import annotations

from typing import Dict, List, Optional

from sytherion.core.interfaces import IIA, ILogger, IOrquestrador, Mensagem, TipoMensagem
from sytherion.core.texto_utils import contem_palavra_chave, normalizar_texto
from sytherion.infrastructure.alimentadores import AlimentadorFactory


class Orquestrador(IOrquestrador):
    def __init__(self, logger: ILogger) -> None:
        self._logger = logger
        self._ias: Dict[str, IIA] = {}

    # ---------------------------------------------------------- registro --
    def registrar_ia(self, ia: IIA) -> None:
        nome = ia.get_nome()
        if nome in self._ias:
            self._logger.aviso(f"IA '{nome}' já registrada — sobrescrevendo.")
        self._ias[nome] = ia
        self._logger.evento("ORQUESTRADOR", f"IA registrada: {nome} ({ia.get_dominio()})")

    def listar_ias(self) -> List[str]:
        return sorted(self._ias.keys())

    def get_ia(self, nome: str) -> Optional[IIA]:
        return self._ias.get(nome)

    # ---------------------------------------------------------- seleção --
    # Conhecimento aprendido pesa mais que palavras-chave fixas do domínio.
    _PESO_CONHECIMENTO_APRENDIDO = 3

    def selecionar_especialista(self, pergunta: str) -> Optional[IIA]:
        pergunta_norm = normalizar_texto(pergunta)
        melhor_ia, melhor_pontuacao = None, 0
        for ia in self._ias.values():
            pontuacao = sum(1 for palavra in ia.get_palavras_chave() if contem_palavra_chave(pergunta_norm, normalizar_texto(palavra)))
            if hasattr(ia, "contar_correspondencias"):
                pontuacao += ia.contar_correspondencias(pergunta) * self._PESO_CONHECIMENTO_APRENDIDO
            if pontuacao > melhor_pontuacao:
                melhor_ia, melhor_pontuacao = ia, pontuacao
        # Sem nenhum sinal, retorna None — o pipeline assume isso e responde
        # honestamente, em vez de cair numa IA aleatória.
        return melhor_ia

    # ---------------------------------------------------------- roteamento --
    def rotear(self, pergunta: str, dominio: Optional[str] = None) -> Mensagem:
        ia_alvo = self._ias.get(dominio) if dominio else self.selecionar_especialista(pergunta)
        if ia_alvo is None:
            self._logger.erro("Nenhuma IA disponível para responder à consulta.")
            return Mensagem(origem="ORQUESTRADOR", destino="usuario",
                conteudo="Nenhuma IA especializada foi encontrada para essa pergunta.", tipo=TipoMensagem.ERRO)
        resposta = ia_alvo.responder(pergunta)
        self._logger.evento("ORQUESTRADOR", f"Consulta roteada para {ia_alvo.get_nome()}")
        return Mensagem(origem=ia_alvo.get_nome(), destino="usuario", conteudo=resposta,
            tipo=TipoMensagem.RESPOSTA, metadados={"dominio": ia_alvo.get_dominio()})

    # ---------------------------------------------------------- aprendizado --
    def alimentar_ia(self, nome_ia: str, caminho_arquivo: str) -> Mensagem:
        ia = self._ias.get(nome_ia)
        if ia is None:
            return Mensagem(origem="ORQUESTRADOR", destino="usuario",
                conteudo=f"IA '{nome_ia}' não encontrada.", tipo=TipoMensagem.ERRO)
        if not hasattr(ia, "aprender"):
            return Mensagem(origem="ORQUESTRADOR", destino="usuario",
                conteudo=f"IA '{nome_ia}' não suporta aprendizado.", tipo=TipoMensagem.ERRO)
        try:
            alimentador = AlimentadorFactory.obter_para(caminho_arquivo)
            trechos = alimentador.processar(caminho_arquivo)
            total = sum(ia.aprender(trecho, fonte=caminho_arquivo) for trecho in trechos)
            self._logger.sucesso(f"{nome_ia} aprendeu {total} novos itens de '{caminho_arquivo}'.")
            return Mensagem(origem="ORQUESTRADOR", destino="usuario",
                conteudo=f"{nome_ia} absorveu {total} novos itens de conhecimento.",
                tipo=TipoMensagem.APRENDIZADO, metadados={"itens_aprendidos": total})
        except Exception as exc:  # noqa: BLE001
            self._logger.erro(f"Falha ao alimentar {nome_ia}: {exc}")
            return Mensagem(origem="ORQUESTRADOR", destino="usuario",
                conteudo=f"Erro ao processar arquivo: {exc}", tipo=TipoMensagem.ERRO)
