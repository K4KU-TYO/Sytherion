"""
Application / Agentes Auxiliares
------------------------------------
Os 4 agentes que assistem o Agente Central, em pipeline:

  1. AgenteAnalisadorIntencao — decide qual especialista deve atuar
  2. AgenteContextualizador   — avalia continuidade com a conversa
  3. AgenteRefinador          — poli o rascunho de resposta
  4. AgenteValidador          — garante que a resposta final é segura

Cada um faz uma única coisa e implementa o mesmo contrato
(`IAgenteAuxiliar.processar`), então são intercambiáveis e novas
etapas podem entrar na lista sem alterar as existentes.
"""
from __future__ import annotations

from sytherion.core.interfaces import IAgenteAuxiliar, IOrquestrador, PacotePipeline
from sytherion.core.texto_utils import contem_palavra_chave, normalizar_texto


class AgenteAnalisadorIntencao(IAgenteAuxiliar):
    """Depende só de IOrquestrador (DIP) para descobrir qual especialista chamar."""

    def __init__(self, orquestrador: IOrquestrador) -> None:
        self._orquestrador = orquestrador

    def get_nome(self) -> str:
        return "Analisador de Intenção"

    def processar(self, pacote: PacotePipeline) -> PacotePipeline:
        pacote.especialista = self._orquestrador.selecionar_especialista(pacote.pergunta)
        if pacote.especialista is not None:
            pergunta_norm = normalizar_texto(pacote.pergunta)
            confianca = sum(
                1 for palavra in pacote.especialista.get_palavras_chave()
                if contem_palavra_chave(pergunta_norm, normalizar_texto(palavra))
            )
            if hasattr(pacote.especialista, "contar_correspondencias"):
                confianca += pacote.especialista.contar_correspondencias(pacote.pergunta) * 3
            pacote.confianca = confianca
        pacote.etapas_executadas.append(self.get_nome())
        return pacote


class AgenteContextualizador(IAgenteAuxiliar):
    def get_nome(self) -> str:
        return "Contextualizador"

    def processar(self, pacote: PacotePipeline) -> PacotePipeline:
        mensagens_usuario = [m for m in pacote.historico if m.get("autor") == "usuario"]
        pacote.continuidade = len(mensagens_usuario) > 1
        pacote.etapas_executadas.append(self.get_nome())
        return pacote


class AgenteRefinador(IAgenteAuxiliar):
    def get_nome(self) -> str:
        return "Refinador"

    def processar(self, pacote: PacotePipeline) -> PacotePipeline:
        texto = (pacote.rascunho or "").strip()
        # Só aplica o tom de continuidade quando um especialista respondeu de
        # verdade — na mensagem de "não encontrei ninguém" isso soaria estranho.
        if pacote.continuidade and texto and pacote.especialista is not None:
            texto = f"Continuando nosso fio de raciocínio: {texto}"
        pacote.refinado = texto
        pacote.etapas_executadas.append(self.get_nome())
        return pacote


class AgenteValidador(IAgenteAuxiliar):
    def get_nome(self) -> str:
        return "Validador"

    def processar(self, pacote: PacotePipeline) -> PacotePipeline:
        final = pacote.refinado
        if not final or len(final) < 3:
            final = "Não tenho informação suficiente para responder com segurança agora — pode reformular?"
        pacote.resposta_final = final
        pacote.etapas_executadas.append(self.get_nome())
        return pacote
