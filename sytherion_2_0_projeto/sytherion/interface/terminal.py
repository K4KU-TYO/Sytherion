"""
Interface / Terminal
------------------------
CLI hacker do Sytherion. Único lugar que conhece I/O de console —
depende só de IOrquestrador e IAgenteCentral.
"""
from __future__ import annotations

import os
import sys
import time

from sytherion.core.interfaces import IAgenteCentral, IOrquestrador
from sytherion.infrastructure.logger import Cores

VERDE, VERDE_ESCURO, CIANO = Cores.VERDE, Cores.VERDE_ESCURO, Cores.CIANO
AMARELO, VERMELHO, CINZA = Cores.AMARELO, Cores.VERMELHO, Cores.CINZA
NEGRITO, RESET = Cores.NEGRITO, Cores.RESET

BANNER = r"""
  ███████╗██╗   ██╗████████╗██╗  ██╗███████╗██████╗ ██╗ ██████╗ ███╗   ██╗
  ██╔════╝╚██╗ ██╔╝╚══██╔══╝██║  ██║██╔════╝██╔══██╗██║██╔═══██╗████╗  ██║
  ███████╗ ╚████╔╝    ██║   ███████║█████╗  ██████╔╝██║██║   ██║██╔██╗ ██║
  ╚════██║  ╚██╔╝     ██║   ██╔══██║██╔══╝  ██╔══██╗██║██║   ██║██║╚██╗██║
  ███████║   ██║      ██║   ██║  ██║███████╗██║  ██║██║╚██████╔╝██║ ╚████║
  ╚══════╝   ╚═╝      ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝
"""


class TerminalSytherion:
    def __init__(self, orquestrador: IOrquestrador, agente_central: IAgenteCentral, animado: bool = True) -> None:
        self._orquestrador = orquestrador
        self._central = agente_central
        self._animado = animado
        self._historico_cli: list = []  # espelha o histórico de uma "conversa" no terminal

    @staticmethod
    def _limpar_tela() -> None:
        os.system("cls" if os.name == "nt" else "clear")

    def _digitar(self, texto: str, delay: float = 0.0012) -> None:
        if not self._animado:
            print(texto)
            return
        for ch in texto:
            sys.stdout.write(ch)
            sys.stdout.flush()
            time.sleep(delay)
        print()

    def _linha(self, char: str = "─", tamanho: int = 74) -> str:
        return f"{VERDE_ESCURO}{char * tamanho}{RESET}"

    def exibir_banner(self) -> None:
        self._limpar_tela()
        print(f"{VERDE}{BANNER}{RESET}")
        print(self._linha("═"))
        self._digitar(f"{CIANO}  >> ECOSSISTEMA DE IAs ESPECIALIZADAS — SYTHERION 2.0{RESET}", delay=0.0008)
        n_ias = len(self._orquestrador.listar_ias())
        print(f"{CINZA}  >> {n_ias} especialistas + 1 Agente Central + 4 agentes auxiliares{RESET}")
        print(f"{CINZA}  >> Arquitetura: Hexagonal + SOLID + DDD + Multiagente{RESET}")
        print(self._linha("═"))
        print()

    def exibir_menu(self) -> None:
        opcoes = [
            ("1", "Conversar com o Agente Central (pipeline completo, recomendado)"),
            ("2", "Conversar diretamente com uma IA especialista"),
            ("3", "Listar todos os especialistas disponíveis"),
            ("4", "Alimentar uma IA com um arquivo (txt/md/json/csv/pdf/docx)"),
            ("5", "Ver estatísticas de uma IA"),
            ("6", "Exportar conhecimento de uma IA"),
            ("0", "Sair"),
        ]
        print(f"{VERDE}┌─ MENU PRINCIPAL {'─' * 54}┐{RESET}")
        for chave, texto in opcoes:
            print(f"{VERDE}│{RESET}  {AMARELO}[{chave}]{RESET} {texto}")
        print(f"{VERDE}└{'─' * 72}┘{RESET}")

    def _prompt(self, texto: str) -> str:
        return input(f"{CIANO}sytherion{RESET}{CINZA}@{RESET}{VERDE}root{RESET}{NEGRITO}:~${RESET} {texto}").strip()

    def _listar_ias(self) -> None:
        ias = self._orquestrador.listar_ias()
        print(f"\n{VERDE}Especialistas registrados ({len(ias)}):{RESET}")
        for i, nome in enumerate(ias, 1):
            ia = self._orquestrador.get_ia(nome)
            dominio = ia.get_dominio() if ia else "?"
            print(f"  {CINZA}{i:>2}.{RESET} {NEGRITO}{nome}{RESET} — {dominio}")
        print()

    def _conversar_com_central(self) -> None:
        print(f"{CINZA}Conversando com o Agente Central. Ele escolhe o especialista sozinho. Digite 'sair' para encerrar.{RESET}")
        self._historico_cli = []
        while True:
            pergunta = self._prompt("> ")
            if pergunta.lower() in ("sair", "exit", "voltar"):
                break
            self._historico_cli.append({"autor": "usuario", "texto": pergunta})
            pacote = self._central.responder(pergunta, self._historico_cli)
            print(f"{CIANO}  [pipeline] {' → '.join(pacote.etapas_executadas)}{RESET}")
            especialista_nome = pacote.especialista.get_nome() if pacote.especialista else "?"
            print(f"{CINZA}  [especialista escolhido: {especialista_nome} | confiança: {pacote.confianca}]{RESET}")
            print(f"{VERDE}{pacote.resposta_final}{RESET}\n")
            self._historico_cli.append({"autor": "assistente", "texto": pacote.resposta_final})

    def _conversar_direto(self) -> None:
        self._listar_ias()
        nome = self._prompt("nome exato da IA (ou 'voltar'): ")
        if nome.lower() == "voltar":
            return
        ia = self._orquestrador.get_ia(nome)
        if ia is None:
            print(f"{VERMELHO}IA não encontrada.{RESET}")
            return
        print(f"{CINZA}Conversando com {nome}. Digite 'sair' para encerrar.{RESET}")
        while True:
            pergunta = self._prompt("> ")
            if pergunta.lower() in ("sair", "exit", "voltar"):
                break
            print(f"{VERDE}{ia.responder(pergunta)}{RESET}\n")

    def _alimentar_ia(self) -> None:
        self._listar_ias()
        nome = self._prompt("nome da IA a alimentar: ")
        caminho = self._prompt("caminho do arquivo: ")
        msg = self._orquestrador.alimentar_ia(nome, caminho)
        cor = VERMELHO if msg.tipo.value == "erro" else VERDE
        print(f"{cor}{msg.conteudo}{RESET}\n")

    def _ver_estatisticas(self) -> None:
        nome = self._prompt("nome da IA: ")
        ia = self._orquestrador.get_ia(nome)
        if ia is None or not hasattr(ia, "get_estatisticas"):
            print(f"{VERMELHO}IA não encontrada ou sem estatísticas.{RESET}")
            return
        print(f"\n{VERDE}── Estatísticas: {nome} ──{RESET}")
        for chave, valor in ia.get_estatisticas().items():
            print(f"  {CINZA}{chave}:{RESET} {valor}")
        print()

    def _exportar_conhecimento(self) -> None:
        nome = self._prompt("nome da IA: ")
        ia = self._orquestrador.get_ia(nome)
        if ia is None or not hasattr(ia, "exportar_conhecimento"):
            print(f"{VERMELHO}IA não encontrada ou sem suporte a exportação.{RESET}")
            return
        destino = f"sytherion_data/exports/{nome}.md"
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        with open(destino, "w", encoding="utf-8") as f:
            f.write(ia.exportar_conhecimento())
        print(f"{VERDE}Exportado para {destino}{RESET}\n")

    def iniciar(self) -> None:
        self.exibir_banner()
        acoes = {
            "1": self._conversar_com_central,
            "2": self._conversar_direto,
            "3": self._listar_ias,
            "4": self._alimentar_ia,
            "5": self._ver_estatisticas,
            "6": self._exportar_conhecimento,
        }
        while True:
            self.exibir_menu()
            escolha = self._prompt("escolha uma opção: ")
            if escolha == "0":
                print(f"{VERDE}Encerrando Sytherion 2.0. Até a próxima.{RESET}")
                break
            acao = acoes.get(escolha)
            if acao is None:
                print(f"{VERMELHO}Opção inválida.{RESET}\n")
                continue
            try:
                acao()
            except (KeyboardInterrupt, EOFError):
                print(f"\n{VERDE}Encerrando Sytherion 2.0.{RESET}")
                break
