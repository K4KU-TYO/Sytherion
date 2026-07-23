"""
Infrastructure / Alimentadores
----------------------------------
Cada formato de arquivo (txt, md, json, csv, pdf, docx) é uma estratégia
de leitura. AlimentadorFactory escolhe qual usar pela extensão do arquivo.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import List

from sytherion.core.interfaces import IAlimentador


class AlimentadorBase(IAlimentador):
    _extensoes: tuple = ()

    def suporta(self, extensao: str) -> bool:
        return extensao.lower().lstrip(".") in self._extensoes

    def processar(self, caminho: str) -> List[str]:
        path = Path(caminho)
        if not path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")
        return self._extrair(path)

    def _extrair(self, path: Path) -> List[str]:
        raise NotImplementedError


class AlimentadorTXT(AlimentadorBase):
    _extensoes = ("txt",)
    def _extrair(self, path: Path) -> List[str]:
        return [path.read_text(encoding="utf-8", errors="ignore")]


class AlimentadorMarkdown(AlimentadorBase):
    _extensoes = ("md", "markdown")
    def _extrair(self, path: Path) -> List[str]:
        texto = path.read_text(encoding="utf-8", errors="ignore")
        linhas = [l.lstrip("#>*- ").strip() for l in texto.split("\n")]
        return ["\n".join(l for l in linhas if l)]


class AlimentadorJSON(AlimentadorBase):
    _extensoes = ("json",)
    def _extrair(self, path: Path) -> List[str]:
        dados = json.loads(path.read_text(encoding="utf-8"))
        return [self._achatar(dados)]

    def _achatar(self, dados, prefixo: str = "") -> str:
        partes = []
        if isinstance(dados, dict):
            for chave, valor in dados.items():
                partes.append(self._achatar(valor, f"{prefixo}{chave}: "))
        elif isinstance(dados, list):
            for item in dados:
                partes.append(self._achatar(item, prefixo))
        else:
            partes.append(f"{prefixo}{dados}")
        return "\n".join(partes)


class AlimentadorCSV(AlimentadorBase):
    _extensoes = ("csv",)
    def _extrair(self, path: Path) -> List[str]:
        linhas = []
        with open(path, newline="", encoding="utf-8", errors="ignore") as f:
            leitor = csv.reader(f)
            cabecalho = next(leitor, [])
            for linha in leitor:
                linhas.append(", ".join(f"{c}={v}" for c, v in zip(cabecalho, linha)))
        return ["\n".join(linhas)]


class AlimentadorPDF(AlimentadorBase):
    _extensoes = ("pdf",)
    def _extrair(self, path: Path) -> List[str]:
        try:
            from pypdf import PdfReader
        except ImportError as exc:
            raise ImportError("Suporte a PDF requer: pip install pypdf") from exc
        leitor = PdfReader(str(path))
        return ["\n".join(p.extract_text() or "" for p in leitor.pages)]


class AlimentadorDOCX(AlimentadorBase):
    _extensoes = ("docx",)
    def _extrair(self, path: Path) -> List[str]:
        try:
            import docx
        except ImportError as exc:
            raise ImportError("Suporte a DOCX requer: pip install python-docx") from exc
        documento = docx.Document(str(path))
        return ["\n".join(p.text for p in documento.paragraphs if p.text.strip())]


class AlimentadorFactory:
    _estrategias: List[AlimentadorBase] = [
        AlimentadorTXT(), AlimentadorMarkdown(), AlimentadorJSON(),
        AlimentadorCSV(), AlimentadorPDF(), AlimentadorDOCX(),
    ]

    @classmethod
    def obter_para(cls, caminho: str) -> AlimentadorBase:
        extensao = Path(caminho).suffix.lstrip(".")
        for estrategia in cls._estrategias:
            if estrategia.suporta(extensao):
                return estrategia
        raise ValueError(f"Nenhum alimentador suporta o formato '.{extensao}'")

    @classmethod
    def registrar(cls, alimentador: AlimentadorBase) -> None:
        cls._estrategias.append(alimentador)

    @classmethod
    def formatos_suportados(cls) -> List[str]:
        formatos = []
        for e in cls._estrategias:
            formatos.extend(e._extensoes)
        return sorted(set(formatos))
