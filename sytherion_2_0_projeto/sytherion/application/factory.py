"""
Application / Factory
-----------------------
Cria e registra as IAs especialistas. Adicionar uma nova = 1 classe em
domain/ias_especializadas.py + 1 linha no mapeamento abaixo.
"""
from __future__ import annotations

from typing import Callable, Dict, List

from sytherion.core.interfaces import IIA


class IAFactory:
    _registro: Dict[str, Callable[[], IIA]] = {}

    @classmethod
    def registrar(cls, tipo: str, construtor: Callable[[], IIA]) -> None:
        cls._registro[tipo] = construtor

    @classmethod
    def criar(cls, tipo: str) -> IIA:
        if tipo not in cls._registro:
            raise ValueError(
                f"Tipo de IA desconhecido: '{tipo}'. Disponíveis: {', '.join(sorted(cls._registro))}"
            )
        return cls._registro[tipo]()

    @classmethod
    def criar_todas(cls) -> List[IIA]:
        return [construtor() for construtor in cls._registro.values()]

    @classmethod
    def tipos_disponiveis(cls) -> List[str]:
        return sorted(cls._registro.keys())


def _registrar_ias_padrao() -> None:
    """Registra as 40 IAs especialistas em cibersegurança."""
    from sytherion.domain import ias_especializadas as ia

    mapeamento = {
        "redes_seguranca": ia.IARedesSeguranca,
        "criptografia": ia.IACriptografia,
        "pentest": ia.IAPenTest,
        "forense_digital": ia.IAForenseDigital,
        "engenharia_social": ia.IAEngenhariaSocial,
        "analise_malware": ia.IAAnaliseMalware,
        "engenharia_reversa": ia.IAEngenhariaReversa,
        "osint": ia.IAOSINT,
        "soc": ia.IASOC,
        "resposta_incidentes": ia.IARespostaIncidentes,
        "seguranca_web": ia.IASegurancaWeb,
        "seguranca_nuvem": ia.IASegurancaNuvem,
        "seguranca_iot": ia.IASegurancaIoT,
        "seguranca_mobile": ia.IASegurancaMobile,
        "grc": ia.IAGRC,
        "threat_intelligence": ia.IAThreatIntelligence,
        "red_team": ia.IARedTeam,
        "blue_team": ia.IABlueTeam,
        "seguranca_blockchain": ia.IASegurancaBlockchain,
        "seguranca_api": ia.IASegurancaAPI,
        "devsecops": ia.IADevSecOps,
        "hardening": ia.IAHardening,
        "seguranca_linux": ia.IASegurancaLinux,
        "seguranca_windows": ia.IASegurancaWindows,
        "redes_wireless": ia.IARedesWireless,
        "gestao_vulnerabilidades": ia.IAGestaoVulnerabilidades,
        "iam": ia.IAIAM,
        "criptoanalise": ia.IACriptoanalise,
        "esteganografia": ia.IAEsteganografia,
        "seguranca_banco_dados": ia.IASegurancaBancoDados,
        "anti_phishing": ia.IAAntiPhishing,
        "seguranca_industrial": ia.IASegurancaIndustrial,
        "seguranca_containers": ia.IASegurancaContainers,
        "zero_trust": ia.IAZeroTrust,
        "direito_digital": ia.IADireitoDigital,
        "seguranca_pagamentos": ia.IASegurancaPagamentos,
        "auditoria_seguranca": ia.IAAuditoriaSeguranca,
        "bug_bounty_ctf": ia.IABugBountyCTF,
        "threat_hunting": ia.IAThreatHunting,
        "ransomware": ia.IARansomware,
    }
    for tipo, classe in mapeamento.items():
        IAFactory.registrar(tipo, classe)


_registrar_ias_padrao()
