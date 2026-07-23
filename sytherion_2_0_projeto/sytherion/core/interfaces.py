"""
Core / Interfaces
------------------
Camada mais interna do projeto (Arquitetura Hexagonal). Só contratos
(interfaces) vivem aqui, sem nenhuma implementação. Todo o resto do
sistema depende dessas abstrações, nunca de classes concretas
diretamente (Dependency Inversion).
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class TipoMensagem(str, Enum):
    CONSULTA = "consulta"
    RESPOSTA = "resposta"
    EVENTO = "evento"
    ERRO = "erro"
    APRENDIZADO = "aprendizado"


@dataclass
class Mensagem:
    """Formato padrão de comunicação entre Terminal/API, Orquestrador e IAs."""
    origem: str
    destino: str
    conteudo: str
    tipo: TipoMensagem = TipoMensagem.CONSULTA
    timestamp: datetime = field(default_factory=datetime.now)
    metadados: Dict[str, Any] = field(default_factory=dict)


# --------------------------------------------------------------------------
# Contratos de IA
# --------------------------------------------------------------------------

class IIA(ABC):
    """Contrato mínimo que toda IA especialista implementa."""

    @abstractmethod
    def responder(self, pergunta: str) -> str: ...

    @abstractmethod
    def get_nome(self) -> str: ...

    @abstractmethod
    def get_dominio(self) -> str: ...

    @abstractmethod
    def get_palavras_chave(self) -> List[str]: ...


class IIAComAprendizado(IIA):
    @abstractmethod
    def aprender(self, conhecimento: str, fonte: str = "manual") -> int: ...


class IIAComExtras(IIA):
    @abstractmethod
    def get_estatisticas(self) -> Dict[str, Any]: ...


class IIAComExportacao(IIA):
    @abstractmethod
    def exportar_conhecimento(self) -> str: ...


class IIAPersistivel(IIA):
    """IA cujo conhecimento aprendido pode ser salvo/restaurado em disco."""

    @abstractmethod
    def exportar_estado(self) -> Dict[str, str]: ...

    @abstractmethod
    def importar_estado(self, dados: Dict[str, str]) -> None: ...


class IIAComBuscaConhecimento(IIA):
    """Permite checar o quanto uma IA sabe sobre um assunto sem chamar responder()."""

    @abstractmethod
    def contar_correspondencias(self, pergunta: str) -> int: ...


# --------------------------------------------------------------------------
# Contratos de infraestrutura
# --------------------------------------------------------------------------

class IAlimentador(ABC):
    @abstractmethod
    def suporta(self, extensao: str) -> bool: ...

    @abstractmethod
    def processar(self, caminho: str) -> List[str]: ...


class ILogger(ABC):
    @abstractmethod
    def info(self, msg: str) -> None: ...
    @abstractmethod
    def sucesso(self, msg: str) -> None: ...
    @abstractmethod
    def aviso(self, msg: str) -> None: ...
    @abstractmethod
    def erro(self, msg: str) -> None: ...
    @abstractmethod
    def evento(self, origem: str, msg: str) -> None: ...


class IConfigManager(ABC):
    @abstractmethod
    def obter(self, chave: str, padrao: Any = None) -> Any: ...
    @abstractmethod
    def definir(self, chave: str, valor: Any) -> None: ...
    @abstractmethod
    def salvar(self) -> None: ...


class IOrquestrador(ABC):
    """Único ponto de entrada para registrar e consultar as IAs."""

    @abstractmethod
    def registrar_ia(self, ia: IIA) -> None: ...

    @abstractmethod
    def get_ia(self, nome: str) -> Optional[IIA]: ...

    @abstractmethod
    def rotear(self, pergunta: str, dominio: Optional[str] = None) -> Mensagem: ...

    @abstractmethod
    def selecionar_especialista(self, pergunta: str) -> Optional[IIA]:
        """Decide qual IA deveria responder, sem chamá-la."""
        ...

    @abstractmethod
    def alimentar_ia(self, nome_ia: str, caminho_arquivo: str) -> Mensagem: ...

    @abstractmethod
    def listar_ias(self) -> List[str]: ...


class IRepositorioConhecimento(ABC):
    """Persiste o conhecimento aprendido de cada IA entre execuções."""

    @abstractmethod
    def carregar(self, nome_ia: str) -> Dict[str, str]: ...

    @abstractmethod
    def salvar(self, nome_ia: str, dados: Dict[str, str]) -> None: ...


class IRepositorioPreferencias(ABC):
    """Persiste preferências de UI (tema ativo e temas customizados)."""

    @abstractmethod
    def carregar(self) -> Dict[str, Any]: ...

    @abstractmethod
    def salvar(self, dados: Dict[str, Any]) -> None: ...


# --------------------------------------------------------------------------
# Pipeline multiagente (1 Central + N Auxiliares)
# --------------------------------------------------------------------------

@dataclass
class PacotePipeline:
    """Envelope que passa por cada etapa do pipeline do Agente Central."""
    pergunta: str
    historico: List[Dict[str, str]] = field(default_factory=list)
    especialista: Optional[IIA] = None
    confianca: int = 0
    rascunho: Optional[str] = None
    continuidade: bool = False
    refinado: Optional[str] = None
    resposta_final: Optional[str] = None
    etapas_executadas: List[str] = field(default_factory=list)


class IAgenteAuxiliar(ABC):
    """Uma etapa do pipeline: recebe o pacote, processa, devolve o pacote."""

    @abstractmethod
    def processar(self, pacote: PacotePipeline) -> PacotePipeline: ...

    @abstractmethod
    def get_nome(self) -> str: ...


class IAgenteCentral(ABC):
    """Coordena o especialista escolhido + os agentes auxiliares."""

    @abstractmethod
    def responder(self, pergunta: str, historico: Optional[List[Dict[str, str]]] = None) -> PacotePipeline: ...
