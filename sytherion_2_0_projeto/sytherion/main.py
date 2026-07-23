"""
Composition Root
--------------------
Único lugar onde tudo é instanciado e conectado. Terminal e API chamam
`construir_ecossistema()` para obter as mesmas instâncias.
"""
from __future__ import annotations

from dataclasses import dataclass

from sytherion.application.agente_central import AgenteCentral
from sytherion.application.agentes_auxiliares import (
    AgenteAnalisadorIntencao,
    AgenteContextualizador,
    AgenteRefinador,
    AgenteValidador,
)
from sytherion.application.factory import IAFactory
from sytherion.application.orquestrador import Orquestrador
from sytherion.application.orquestrador_persistente import OrquestradorComPersistencia
from sytherion.core.interfaces import IAgenteCentral, ILogger, IOrquestrador
from sytherion.infrastructure.config_manager import ConfigManager
from sytherion.infrastructure.logger import LoggerSytherion
from sytherion.infrastructure.repositorio_conhecimento import RepositorioConhecimentoJSON
from sytherion.infrastructure.repositorio_preferencias import RepositorioPreferenciasJSON


@dataclass
class Ecossistema:
    logger: ILogger
    orquestrador: IOrquestrador
    agente_central: IAgenteCentral
    total_especialistas: int
    repositorio_preferencias: RepositorioPreferenciasJSON


def construir_ecossistema(log_no_console: bool = True) -> Ecossistema:
    config = ConfigManager()
    logger = LoggerSytherion(caminho_arquivo=config.obter("log_arquivo"))

    orquestrador_base = Orquestrador(logger=logger)
    repositorio = RepositorioConhecimentoJSON(
        diretorio=config.obter("diretorio_conhecimento", "sytherion_data/conhecimento")
    )
    orquestrador: IOrquestrador = OrquestradorComPersistencia(orquestrador_base, repositorio)

    for ia in IAFactory.criar_todas():
        orquestrador.registrar_ia(ia)  # já restaura conhecimento salvo, via decorator

    pipeline = [
        AgenteAnalisadorIntencao(orquestrador),
        AgenteContextualizador(),
        AgenteRefinador(),
        AgenteValidador(),
    ]
    agente_central = AgenteCentral(pipeline)

    total = len(orquestrador.listar_ias())
    logger.sucesso(f"Sytherion 2.0 inicializado: {total} especialistas + 1 Agente Central + 4 agentes auxiliares.")

    repositorio_preferencias = RepositorioPreferenciasJSON(
        caminho=config.obter("arquivo_preferencias", "sytherion_data/preferencias.json")
    )

    return Ecossistema(
        logger=logger,
        orquestrador=orquestrador,
        agente_central=agente_central,
        total_especialistas=total,
        repositorio_preferencias=repositorio_preferencias,
    )


def main() -> None:
    from sytherion.interface.terminal import TerminalSytherion

    eco = construir_ecossistema()
    terminal = TerminalSytherion(
        orquestrador=eco.orquestrador,
        agente_central=eco.agente_central,
        animado=True,
    )
    terminal.iniciar()


if __name__ == "__main__":
    main()
