"""
Backend / API
-----------------
Expõe o Ecossistema (Orquestrador + Agente Central + especialistas) via
HTTP para o frontend. Sem regra de negócio aqui — só tradução HTTP.

Executar:
    uvicorn sytherion.backend.api:app --reload
Depois abrir http://localhost:8000 (a própria API serve o frontend).
"""
from __future__ import annotations

import shutil
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from sytherion.main import construir_ecossistema

# ---------------------------------------------------------------- modelos --

class MensagemHistorico(BaseModel):
    autor: str
    texto: str


class ChatRequest(BaseModel):
    pergunta: str
    historico: List[MensagemHistorico] = []


class ChatResponse(BaseModel):
    resposta: str
    especialista: str
    dominio: str
    confianca: int
    trilha: List[str]


class EspecialistaInfo(BaseModel):
    nome: str
    dominio: str


class AlimentarResponse(BaseModel):
    sucesso: bool
    mensagem: str
    itens_aprendidos: Optional[int] = None


class TemaCustomizado(BaseModel):
    nome: str
    cores: Dict[str, str]


class TemaAtivoRequest(BaseModel):
    nome: str


class PreferenciasResponse(BaseModel):
    tema_ativo: str
    temas_customizados: Dict[str, Dict[str, str]]


# ---------------------------------------------------------------- app --

app = FastAPI(title="Sytherion 2.0 API", version="2.0.0")

VERSAO_BUILD = "2.3.0-fix-continuidade-em-fallback-sem-especialista"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

_eco = construir_ecossistema()


@app.get("/api/agentes", response_model=List[EspecialistaInfo])
def listar_agentes() -> List[EspecialistaInfo]:
    """Lista os especialistas registrados — usado pelo frontend para exibir o total real."""
    infos = []
    for nome in _eco.orquestrador.listar_ias():
        ia = _eco.orquestrador.get_ia(nome)
        if ia:
            infos.append(EspecialistaInfo(nome=ia.get_nome(), dominio=ia.get_dominio()))
    return infos


@app.post("/api/chat", response_model=ChatResponse)
def conversar(req: ChatRequest) -> ChatResponse:
    """
    Único endpoint de conversa. Delega tudo ao Agente Central real:
    ele escolhe o especialista e roda o pipeline dos 4 agentes auxiliares.
    """
    if not req.pergunta.strip():
        raise HTTPException(status_code=400, detail="Pergunta vazia.")

    historico = [{"autor": m.autor, "texto": m.texto} for m in req.historico]
    pacote = _eco.agente_central.responder(req.pergunta, historico)

    if pacote.especialista is None:
        # Nenhum especialista teve sinal para essa pergunta — resposta honesta
        # do próprio pipeline, não um erro de infraestrutura (não é 503).
        return ChatResponse(
            resposta=pacote.resposta_final or "Não encontrei um especialista para essa pergunta.",
            especialista="IA-Central",
            dominio="Roteamento",
            confianca=0,
            trilha=["IA-Central", *[e for e in pacote.etapas_executadas if e != "Analisador de Intenção"]],
        )

    trilha = ["IA-Central", pacote.especialista.get_nome(), *[
        e for e in pacote.etapas_executadas if e != "Analisador de Intenção"
    ]]

    return ChatResponse(
        resposta=pacote.resposta_final or "",
        especialista=pacote.especialista.get_nome(),
        dominio=pacote.especialista.get_dominio(),
        confianca=pacote.confianca,
        trilha=trilha,
    )


@app.post("/api/alimentar", response_model=AlimentarResponse)
async def alimentar(nome_ia: str = Form(...), arquivo: UploadFile = File(...)) -> AlimentarResponse:
    """Recebe um upload (txt/md/json/csv/pdf/docx) e alimenta a IA indicada."""
    sufixo = Path(arquivo.filename or "").suffix
    with tempfile.NamedTemporaryFile(delete=False, suffix=sufixo) as tmp:
        shutil.copyfileobj(arquivo.file, tmp)
        caminho_tmp = tmp.name

    try:
        msg = _eco.orquestrador.alimentar_ia(nome_ia, caminho_tmp)
    finally:
        Path(caminho_tmp).unlink(missing_ok=True)

    if msg.tipo.value == "erro":
        return AlimentarResponse(sucesso=False, mensagem=msg.conteudo)
    return AlimentarResponse(
        sucesso=True, mensagem=msg.conteudo, itens_aprendidos=msg.metadados.get("itens_aprendidos")
    )


@app.get("/api/status")
def status() -> dict:
    return {
        "status": "online",
        "versao": VERSAO_BUILD,
        "especialistas": _eco.total_especialistas,
        "agente_central": 1,
        "agentes_auxiliares": 4,
    }


@app.get("/api/preferencias", response_model=PreferenciasResponse)
def obter_preferencias() -> PreferenciasResponse:
    dados = _eco.repositorio_preferencias.carregar()
    return PreferenciasResponse(
        tema_ativo=dados.get("tema_ativo", "matrix"),
        temas_customizados=dados.get("temas_customizados", {}),
    )


@app.post("/api/preferencias/tema-ativo", response_model=PreferenciasResponse)
def definir_tema_ativo(req: TemaAtivoRequest) -> PreferenciasResponse:
    dados = _eco.repositorio_preferencias.carregar()
    dados["tema_ativo"] = req.nome
    _eco.repositorio_preferencias.salvar(dados)
    return PreferenciasResponse(
        tema_ativo=dados["tema_ativo"], temas_customizados=dados.get("temas_customizados", {})
    )


@app.post("/api/preferencias/tema-customizado", response_model=PreferenciasResponse)
def salvar_tema_customizado(tema: TemaCustomizado) -> PreferenciasResponse:
    if not tema.nome.strip():
        raise HTTPException(status_code=400, detail="Nome do tema não pode ser vazio.")
    dados = _eco.repositorio_preferencias.carregar()
    dados.setdefault("temas_customizados", {})[tema.nome] = tema.cores
    dados["tema_ativo"] = tema.nome
    _eco.repositorio_preferencias.salvar(dados)
    return PreferenciasResponse(
        tema_ativo=dados["tema_ativo"], temas_customizados=dados["temas_customizados"]
    )


@app.delete("/api/preferencias/tema-customizado/{nome}", response_model=PreferenciasResponse)
def excluir_tema_customizado(nome: str) -> PreferenciasResponse:
    dados = _eco.repositorio_preferencias.carregar()
    dados.setdefault("temas_customizados", {}).pop(nome, None)
    if dados.get("tema_ativo") == nome:
        dados["tema_ativo"] = "matrix"
    _eco.repositorio_preferencias.salvar(dados)
    return PreferenciasResponse(
        tema_ativo=dados["tema_ativo"], temas_customizados=dados["temas_customizados"]
    )


# ------------------------------------------------ servir o frontend estático --
_FRONTEND_DIR = Path(__file__).resolve().parent.parent.parent / "frontend"
if _FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=str(_FRONTEND_DIR), html=True), name="frontend")
