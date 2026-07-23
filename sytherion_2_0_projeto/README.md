<div align="center">

# 🛡️ Sytherion

### Ecossistema multiagente de IA especializado em Cibersegurança

*40 agentes especialistas, 1 orquestrador central, 4 agentes de suporte, aprendizado persistente e uma interface de chat estilo ChatGPT — tudo rodando localmente, sem depender de nenhuma API externa de LLM.*

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](./LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/backend-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![Arquitetura](https://img.shields.io/badge/arquitetura-Hexagonal%20%2B%20SOLID-6f42c1.svg)](#-arquitetura)

[Como rodar](#-como-rodar) ·
[Arquitetura](#-arquitetura) ·
[Os 40 especialistas](#-os-40-especialistas) ·
[Como contribuir](#-como-contribuir)

</div>

---

## 📖 Sobre o projeto

Sytherion é um ecossistema de agentes de IA construído do zero em Python,
sem depender de nenhum modelo de linguagem externo (não usa OpenAI,
Anthropic, nem qualquer API paga). Em vez disso, cada especialista tem
sua própria base de conhecimento, que **cresce com o uso**: você ensina
um assunto a um agente enviando um arquivo de texto, e a partir daí ele
passa a responder sobre aquele tema com o que aprendeu — em prosa,
combinando frases, não citando trechos crus.

O projeto nasceu como um exercício de arquitetura de software (SOLID,
Clean/Hexagonal Architecture, Design Patterns) aplicado a um domínio
divertido — um "exército" de 40 IAs especialistas em subáreas de
cibersegurança, coordenadas por um pipeline de agentes que decide quem
responde cada pergunta.

**Por que cibersegurança?** Porque é um domínio onde precisão importa
mais que criatividade — encaixa bem com a proposta do projeto: respostas
baseadas estritamente no que foi ensinado, nunca inventadas.

---

## ✨ Principais recursos

- 🧠 **40 especialistas** cobrindo Pentest, Forense Digital, Criptografia,
  Red Team, Blue Team, Threat Hunting, Ransomware, Zero Trust, GRC e mais
- 🎯 **Roteamento automático** — você não escolhe quem responde, o
  próprio sistema identifica o assunto e chama o especialista certo
- 📚 **Aprendizado persistente** — ensine qualquer agente enviando um
  arquivo (`.txt` `.md` `.json` `.csv` `.pdf` `.docx`), e o conhecimento
  sobrevive a reinícios do servidor
- 🗣️ **Respostas em prosa** — o agente combina o que aprendeu em texto
  corrido, não em bullets crus
- 💬 **Interface web estilo ChatGPT** — múltiplas conversas, exclusão de
  chats, `Enter` para enviar, scroll por teclado/mouse/touchpad
- 🎨 **Temas customizáveis** — 4 temas prontos + crie os seus próprios
  ("mods"), com persistência entre sessões
- 🖥️ **CLI hacker** — terminal alternativo pra quem prefere linha de
  comando ao navegador
- 🏗️ **Arquitetura limpa** — SOLID, Hexagonal Architecture e Design
  Patterns aplicados de verdade, não só citados em comentário

---

## 🚀 Como rodar

### Pré-requisito

- Python 3.9 ou superior instalado ([python.org](https://www.python.org/downloads/))

### Instalação (Linux / macOS)

```bash
git clone https://github.com/seu-usuario/sytherion.git
cd sytherion
chmod +x instalar.sh
./instalar.sh
```

### Instalação (Windows)

```cmd
git clone https://github.com/seu-usuario/sytherion.git
cd sytherion
instalar.bat
```

O instalador cria um ambiente virtual (`.venv`), instala as
dependências, gera um script `iniciar.sh` / `iniciar.bat` para uso
futuro, e já sobe o servidor abrindo `http://localhost:8000` no
navegador automaticamente.

**Da segunda vez em diante**, basta:

```bash
./iniciar.sh       # Linux/macOS
iniciar.bat        # Windows
```

### Instalação manual (qualquer sistema)

```bash
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn sytherion.backend.api:app --reload
```

Depois abra `http://localhost:8000`.

### Usando o terminal em vez do navegador

```bash
python3 -m sytherion.main
```

---

## 🏗️ Arquitetura

```
sytherion/
├── core/                 # Só abstrações — nenhuma implementação concreta
│   ├── interfaces.py     # Contratos: IIA, IOrquestrador, IAgenteAuxiliar...
│   ├── base.py           # IASytherion — classe base de todo especialista
│   └── texto_utils.py    # Normalização e matching de texto
│
├── domain/
│   └── ias_especializadas.py   # As 40 classes de especialistas
│
├── application/
│   ├── factory.py                  # Registro e criação dos especialistas
│   ├── orquestrador.py             # Decide qual especialista responde
│   ├── orquestrador_persistente.py # Decorator: adiciona persistência
│   ├── agentes_auxiliares.py       # Os 4 agentes de suporte
│   └── agente_central.py           # Coordena tudo
│
├── infrastructure/
│   ├── alimentadores.py            # Leitura de txt/md/json/csv/pdf/docx
│   ├── repositorio_conhecimento.py # Persistência do que foi aprendido
│   ├── repositorio_preferencias.py # Persistência de temas/preferências
│   ├── logger.py
│   └── config_manager.py
│
├── interface/
│   └── terminal.py       # CLI alternativa ao navegador
│
├── backend/
│   └── api.py             # FastAPI — expõe tudo via HTTP
│
└── main.py                # Composition Root

frontend/
└── index.html              # Chat completo em HTML/CSS/JS puro

instalar.sh / instalar.bat  # Setup com um comando
```

### Como uma pergunta é respondida

```
Você pergunta
     │
     ▼
Agente Central
     │
     ├─► Analisador de Intenção  → escolhe o especialista certo
     ├─► [Especialista responde, usando o que aprendeu]
     ├─► Contextualizador        → avalia continuidade da conversa
     ├─► Refinador               → poli o texto da resposta
     └─► Validador               → garante que a resposta é segura
     │
     ▼
Resposta final
```

Cada uma dessas 4 etapas é uma classe independente que implementa o
mesmo contrato (`IAgenteAuxiliar`) — dá pra adicionar uma 5ª etapa sem
tocar nas outras quatro.

### Princípios aplicados

| Princípio | Como aparece no código |
|---|---|
| **S**RP | Cada classe faz uma coisa: o repositório só persiste, o orquestrador só roteia, cada agente auxiliar só faz sua etapa |
| **O**CP | Novo especialista = 1 classe + 1 linha de registro. Persistência foi adicionada via Decorator, sem alterar o Orquestrador original |
| **L**SP | Qualquer especialista, ou o `OrquestradorComPersistencia`, substitui sua contraparte "pura" sem quebrar nada |
| **I**SP | Interfaces pequenas e específicas (`IIAComAprendizado`, `IIAPersistivel`, `IIAComBuscaConhecimento`...) em vez de uma interface gigante |
| **D**IP | Camadas de aplicação dependem só de abstrações (`core/interfaces.py`), nunca de classes concretas de outras camadas |

---

## 🤖 Os 40 especialistas

<details>
<summary>Ver lista completa</summary>

Redes e Firewalls · Criptografia · Pentest · Forense Digital ·
Engenharia Social · Análise de Malware · Engenharia Reversa · OSINT ·
SOC · Resposta a Incidentes · Segurança Web (OWASP) · Segurança em
Nuvem · IoT · Mobile · Governança, Risco e Compliance (LGPD/ISO 27001) ·
Threat Intelligence · Red Team · Blue Team · Blockchain · Segurança de
APIs · DevSecOps · Hardening · Segurança Linux · Segurança Windows ·
Redes Wireless · Gestão de Vulnerabilidades · Gestão de Identidade e
Acesso · Criptoanálise · Esteganografia · Segurança de Bancos de Dados ·
Anti-Phishing · ICS/SCADA · Containers · Zero Trust · Direito Digital ·
Pagamentos (PCI-DSS) · Auditoria · Bug Bounty/CTF · Threat Hunting ·
Ransomware.

</details>

Cada especialista é uma classe pequena em `domain/ias_especializadas.py`:

```python
class IARansomware(_IACyberBase):
    _saudacoes = [
        "Backup imutável e testado é a defesa mais eficaz contra ransomware.",
        "Pagar o resgate não garante recuperação nem impede vazamento dos dados.",
    ]
    def __init__(self):
        super().__init__(
            "IA-Ransomware", "Ransomware e Extorsão Digital",
            ["ransomware", "resgate digital", "criptografia maliciosa", "backup imutavel"],
        )
```

---

## 🌐 API

O backend expõe uma API REST simples, usada tanto pelo frontend quanto
por qualquer cliente próprio que você queira construir:

| Rota | Método | Descrição |
|---|---|---|
| `/api/status` | `GET` | Status do servidor e contagem de agentes |
| `/api/agentes` | `GET` | Lista os 40 especialistas (nome + domínio) |
| `/api/chat` | `POST` | `{pergunta, historico}` → resposta do pipeline completo |
| `/api/alimentar` | `POST` | Upload de arquivo para ensinar um especialista |
| `/api/preferencias` | `GET`/`POST` | Tema ativo e temas customizados |

Documentação interativa (Swagger) disponível em `/docs` com o servidor
rodando.

---

## 🧩 Stack

- **Backend:** Python 3.9+, FastAPI, Uvicorn
- **Frontend:** HTML + CSS + JavaScript puro (sem frameworks, sem build step)
- **Persistência:** arquivos JSON em disco (sem banco de dados externo)
- **Leitura de arquivos:** `pypdf`, `python-docx`

---

## 🤝 Como contribuir

Este projeto é aberto — pull requests, forks e sugestões são bem-vindos.

**Ideias de contribuição:**
- Adicionar um novo especialista (veja o padrão em `domain/ias_especializadas.py`)
- Melhorar o roteamento por palavra-chave
- Adicionar testes automatizados formais (o projeto foi validado manualmente durante o desenvolvimento)
- Melhorar a interface web ou adicionar novos temas prontos
- Traduzir a interface para outros idiomas

**Para contribuir:**

```bash
# 1. Fork este repositório
# 2. Crie uma branch
git checkout -b minha-feature

# 3. Faça suas alterações e teste localmente
./instalar.sh

# 4. Commit e push
git commit -m "Adiciona especialista em X"
git push origin minha-feature

# 5. Abra um Pull Request
```

Ao adicionar um especialista novo, o padrão é:

```python
# domain/ias_especializadas.py
class IAExemplo(_IACyberBase):
    _saudacoes = ["Uma frase de assinatura do domínio."]
    def __init__(self):
        super().__init__("IA-Exemplo", "Nome do Domínio",
            ["palavra-chave-1", "palavra-chave-2"])

# application/factory.py — dentro de _registrar_ias_padrao()
"exemplo": ia.IAExemplo,
```

Nenhuma outra linha do sistema precisa mudar.

---

## ⚠️ Limitações conhecidas

- Não há um LLM real por trás — as respostas são sínteses baseadas em
  template do conhecimento ensinado, não geração de linguagem livre
- O roteamento é por palavra-chave, não por embeddings/similaridade
  semântica — perguntas parafraseadas de forma muito diferente do que
  foi ensinado podem não encontrar o especialista certo
- Sem autenticação — não é recomendado expor a API publicamente sem
  adicionar uma camada de auth própria

---

## 📄 Licença

Distribuído sob a licença **Apache 2.0**. Veja [`LICENSE`](./LICENSE)
para o texto completo.

Na prática: qualquer um pode usar, copiar, modificar e redistribuir
este projeto — inclusive comercialmente — desde que mantenha o aviso
de copyright e a licença original. A diferença para uma licença mais
simples como a MIT é que a Apache 2.0 inclui uma **concessão explícita
de patentes**: se alguém contribuir código para este projeto e depois
tentar processar outro usuário por infração de patente relacionada a
essa contribuição, essa pessoa perde automaticamente os direitos de uso
concedidos pela licença.

---

<div align="center">

Feito com Python, FastAPI e uma quantidade generosa de xícaras de café ☕

</div>
