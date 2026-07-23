"""
Domain / IAs Especializadas em Cibersegurança
--------------------------------------------------
40 especialidades de cibersegurança, cada uma sua própria classe.
Adicionar uma nova = 1 classe aqui + 1 registro em application/factory.py.
"""
from __future__ import annotations

import random
from typing import List

from sytherion.core.base import IASytherion


class _IACyberBase(IASytherion):
    """Sintetiza resposta com o que aprendeu, ou usa uma frase de assinatura."""

    _saudacoes: List[str] = []

    def _processar(self, pergunta: str, contexto: List[str]) -> str:
        if contexto:
            return self._sintetizar_resposta(contexto)
        assinatura = random.choice(self._saudacoes) if self._saudacoes else (
            f"Ainda não tenho conhecimento aprendido sobre isso em {self._dominio}."
        )
        return f"[{self._nome}] {assinatura} (dica: use o clipe de anexo ou 'alimentar' para me ensinar mais)"


class IARedesSeguranca(_IACyberBase):
    _saudacoes = ["Segmentação de rede limita o raio de explosão de um ataque bem-sucedido.",
                  "Um firewall mal configurado é pior que nenhum: dá falsa sensação de segurança."]
    def __init__(self):
        super().__init__("IA-RedesSeguranca", "Segurança de Redes",
            ["firewall", "ids", "ips", "vpn", "roteador", "switch", "segmentacao", "rede seguranca", "dmz"])


class IACriptografia(_IACyberBase):
    _saudacoes = ["Criptografia simétrica é rápida mas exige troca segura de chave; assimétrica resolve isso com par público/privado.",
                  "Hash não é criptografia reversível — é uma função de mão única para verificar integridade."]
    def __init__(self):
        super().__init__("IA-Criptografia", "Criptografia",
            ["criptografia", "cifra", "chave publica", "chave privada", "hash", "aes", "rsa", "criptografico"])


class IAPenTest(_IACyberBase):
    _saudacoes = ["Um pentest sempre começa com escopo bem definido e autorização por escrito.",
                  "Reconhecimento passivo não toca o alvo; ativo já interage e pode ser detectado."]
    def __init__(self):
        super().__init__("IA-PenTest", "Testes de Invasão (Pentest)",
            ["pentest", "teste de invasao", "exploit", "metasploit", "nmap", "burp suite", "invasao"])


class IAForenseDigital(_IACyberBase):
    _saudacoes = ["Cadeia de custódia quebrada pode invalidar uma evidência digital inteira num processo.",
                  "Nunca se analisa a mídia original — sempre uma imagem forense bit a bit."]
    def __init__(self):
        super().__init__("IA-ForenseDigital", "Forense Digital",
            ["forense", "evidencia digital", "cadeia de custodia", "pericia digital", "autopsy"])


class IAEngenhariaSocial(_IACyberBase):
    _saudacoes = ["Engenharia social explora confiança e urgência, não falhas de software.",
                  "Pretexting é criar uma história falsa convincente para extrair informação ou acesso."]
    def __init__(self):
        super().__init__("IA-EngenhariaSocial", "Engenharia Social",
            ["engenharia social", "pretexting", "manipulacao psicologica", "vishing"])


class IAAnaliseMalware(_IACyberBase):
    _saudacoes = ["Ransomware criptografa arquivos e exige resgate; worm se espalha sozinho pela rede.",
                  "Sandbox isola a amostra suspeita para observar comportamento sem risco ao ambiente real."]
    def __init__(self):
        super().__init__("IA-AnaliseMalware", "Análise de Malware",
            ["malware", "virus", "trojan", "worm", "spyware", "sandbox malware"])


class IAEngenhariaReversa(_IACyberBase):
    _saudacoes = ["Engenharia reversa de binário costuma começar identificando a arquitetura e o compilador usado.",
                  "Um bom debugger permite pausar a execução e inspecionar registradores em tempo real."]
    def __init__(self):
        super().__init__("IA-EngenhariaReversa", "Engenharia Reversa",
            ["engenharia reversa", "disassembly", "ida pro", "ghidra", "debugger", "binario"])


class IAOSINT(_IACyberBase):
    _saudacoes = ["OSINT usa só fontes públicas — o desafio é correlacionar, não acessar o que já é aberto.",
                  "Footprinting mapeia a superfície de ataque de um alvo antes de qualquer tentativa ativa."]
    def __init__(self):
        super().__init__("IA-OSINT", "OSINT (Inteligência de Fontes Abertas)",
            ["osint", "reconhecimento", "footprinting", "shodan", "maltego"])


class IASOC(_IACyberBase):
    _saudacoes = ["Um SOC eficiente prioriza alertas por risco real, não por volume.",
                  "SIEM correlaciona logs de múltiplas fontes para revelar padrões que um log isolado não mostra."]
    def __init__(self):
        super().__init__("IA-SOC", "SOC e Monitoramento",
            ["soc", "siem", "monitoramento seguranca", "alerta seguranca", "splunk", "correlacao de eventos"])


class IARespostaIncidentes(_IACyberBase):
    _saudacoes = ["Um playbook de resposta a incidentes bem ensaiado economiza minutos preciosos numa crise real.",
                  "Contenção vem antes de erradicação — parar o sangramento antes de limpar a ferida."]
    def __init__(self):
        super().__init__("IA-RespostaIncidentes", "Resposta a Incidentes",
            ["resposta a incidentes", "contencao", "erradicacao", "playbook", "incidente de seguranca"])


class IASegurancaWeb(_IACyberBase):
    _saudacoes = ["SQL Injection continua no top da OWASP porque input não validado nunca sai de moda como erro.",
                  "XSS explora a confiança do navegador no conteúdo de uma página que ele acha legítimo."]
    def __init__(self):
        super().__init__("IA-SegurancaWeb", "Segurança de Aplicações Web",
            ["owasp", "sql injection", "xss", "csrf", "aplicacao web seguranca", "injecao de codigo"])


class IASegurancaNuvem(_IACyberBase):
    _saudacoes = ["A maioria dos incidentes em nuvem vem de configuração errada, não de falha do provedor.",
                  "Bucket S3 público por engano ainda é uma das causas mais comuns de vazamento de dados."]
    def __init__(self):
        super().__init__("IA-SegurancaNuvem", "Segurança em Nuvem",
            ["cloud seguranca", "aws seguranca", "azure seguranca", "gcp seguranca", "bucket", "seguranca nuvem"])


class IASegurancaIoT(_IACyberBase):
    _saudacoes = ["Muito dispositivo IoT nunca recebe atualização de firmware depois de sair da fábrica.",
                  "Senha padrão de fábrica é a porta de entrada mais explorada em botnets de IoT."]
    def __init__(self):
        super().__init__("IA-SegurancaIoT", "Segurança de IoT",
            ["iot", "dispositivo conectado", "firmware", "mqtt", "botnet iot"])


class IASegurancaMobile(_IACyberBase):
    _saudacoes = ["Permissões excessivas em um app mobile são risco mesmo sem nenhuma vulnerabilidade de código.",
                  "Engenharia reversa de um APK revela muito mais do que os desenvolvedores imaginam."]
    def __init__(self):
        super().__init__("IA-SegurancaMobile", "Segurança Mobile",
            ["mobile seguranca", "android seguranca", "ios seguranca", "apk", "app movel seguranca"])


class IAGRC(_IACyberBase):
    _saudacoes = ["Compliance não é sinônimo de segurança real — é o piso mínimo exigido, não o teto desejável.",
                  "LGPD e GDPR mudaram a forma como incidentes de dados viram evento reportável obrigatório."]
    def __init__(self):
        super().__init__("IA-GRC", "Governança, Risco e Compliance",
            ["grc", "compliance", "lgpd", "iso 27001", "gdpr", "gestao de risco"])


class IAThreatIntelligence(_IACyberBase):
    _saudacoes = ["IOCs (indicadores de comprometimento) tem validade curta; TTPs de um grupo mudam bem mais devagar.",
                  "MITRE ATT&CK virou linguagem comum para descrever comportamento de atacante, não só uma lista."]
    def __init__(self):
        super().__init__("IA-ThreatIntelligence", "Threat Intelligence",
            ["threat intelligence", "ioc", "ttp", "mitre", "feed de ameacas", "inteligencia de ameacas"])


class IARedTeam(_IACyberBase):
    _saudacoes = ["Red Team simula um adversário real, com objetivo e furtividade, não só uma varredura de vulnerabilidades.",
                  "Adversary emulation reproduz as táticas de um grupo de ameaça específico, não um ataque genérico."]
    def __init__(self):
        super().__init__("IA-RedTeam", "Red Team",
            ["red team", "simulacao de ataque", "adversary emulation", "operacao ofensiva"])


class IABlueTeam(_IACyberBase):
    _saudacoes = ["Blue Team vive de detectar rápido o que não deu para prevenir.",
                  "Hardening defensivo reduz superfície de ataque antes mesmo de qualquer alerta disparar."]
    def __init__(self):
        super().__init__("IA-BlueTeam", "Blue Team",
            ["blue team", "defesa ativa", "deteccao de ameacas", "hardening defensivo"])


class IASegurancaBlockchain(_IACyberBase):
    _saudacoes = ["A maioria dos golpes cripto explora o usuário, não uma falha criptográfica do blockchain em si.",
                  "Smart contract com bug vira dinheiro perdido de forma irreversível assim que é publicado."]
    def __init__(self):
        super().__init__("IA-SegurancaBlockchain", "Segurança de Blockchain",
            ["blockchain seguranca", "criptomoeda seguranca", "smart contract", "carteira cripto", "exchange seguranca"])


class IASegurancaAPI(_IACyberBase):
    _saudacoes = ["Uma API sem rate limiting é um convite a abuso e ataques de força bruta.",
                  "JWT mal validado (assinatura ignorada) é uma das falhas mais comuns em APIs modernas."]
    def __init__(self):
        super().__init__("IA-SegurancaAPI", "Segurança de APIs",
            ["api seguranca", "oauth", "jwt", "rate limiting", "token de acesso"])


class IADevSecOps(_IACyberBase):
    _saudacoes = ["Shift left significa achar a vulnerabilidade no código, não em produção depois do deploy.",
                  "SAST analisa código-fonte estático; DAST testa a aplicação already rodando."]
    def __init__(self):
        super().__init__("IA-DevSecOps", "DevSecOps",
            ["devsecops", "pipeline seguro", "sast", "dast", "shift left"])


class IAHardening(_IACyberBase):
    _saudacoes = ["Hardening começa desligando tudo que o sistema não precisa para funcionar.",
                  "Um CIS Benchmark é um checklist de configuração segura reconhecido pela indústria."]
    def __init__(self):
        super().__init__("IA-Hardening", "Hardening de Sistemas",
            ["hardening", "endurecimento de sistema", "cis benchmark", "baseline de seguranca"])


class IASegurancaLinux(_IACyberBase):
    _saudacoes = ["SELinux e AppArmor impõem controle de acesso obrigatório além das permissões tradicionais do Linux.",
                  "auditd registra chamadas de sistema relevantes para investigação posterior."]
    def __init__(self):
        super().__init__("IA-SegurancaLinux", "Segurança em Linux",
            ["linux seguranca", "selinux", "apparmor", "iptables", "auditd"])


class IASegurancaWindows(_IACyberBase):
    _saudacoes = ["Active Directory mal configurado é o alvo número um em ataques internos a redes Windows.",
                  "GPOs (políticas de grupo) aplicam configuração de segurança em escala num domínio Windows."]
    def __init__(self):
        super().__init__("IA-SegurancaWindows", "Segurança em Windows",
            ["windows seguranca", "active directory", "gpo", "powershell seguranca", "dominio windows"])


class IARedesWireless(_IACyberBase):
    _saudacoes = ["WPA3 corrige fraquezas conhecidas do WPA2 contra ataques de dicionário offline.",
                  "Wardriving é mapear redes wireless vulneráveis simplesmente dirigindo por uma área com o equipamento certo."]
    def __init__(self):
        super().__init__("IA-RedesWireless", "Segurança de Redes Wireless",
            ["wireless", "wifi seguranca", "wpa2", "wpa3", "wardriving"])


class IAGestaoVulnerabilidades(_IACyberBase):
    _saudacoes = ["CVSS pontua a severidade de uma vulnerabilidade, mas o contexto do seu ambiente decide a prioridade real.",
                  "Um scanner encontra a vulnerabilidade; gestão de vulnerabilidades é o processo de realmente corrigi-la a tempo."]
    def __init__(self):
        super().__init__("IA-GestaoVulnerabilidades", "Gestão de Vulnerabilidades",
            ["vulnerabilidade", "cve", "cvss", "scanner de vulnerabilidade", "patch de seguranca"])


class IAIAM(_IACyberBase):
    _saudacoes = ["MFA reduz drasticamente o risco de uma senha vazada virar acesso indevido.",
                  "SSO centraliza autenticação, mas também centraliza o risco se essa credencial única for comprometida."]
    def __init__(self):
        super().__init__("IA-IAM", "Gestão de Identidade e Acesso",
            ["iam", "autenticacao", "autorizacao", "mfa", "sso", "controle de acesso"])


class IACriptoanalise(_IACyberBase):
    _saudacoes = ["Um ataque de força bruta testa todas as chaves possíveis; um ataque de dicionário testa só as prováveis.",
                  "Rainbow tables trocam tempo de processamento por espaço de armazenamento para quebrar hashes mais rápido."]
    def __init__(self):
        super().__init__("IA-Criptoanalise", "Criptoanálise",
            ["criptoanalise", "quebra de cifra", "forca bruta criptografica", "rainbow table"])


class IAEsteganografia(_IACyberBase):
    _saudacoes = ["Esteganografia esconde a existência da mensagem; criptografia esconde o conteúdo dela.",
                  "Ocultar dados no bit menos significativo (LSB) de uma imagem é a técnica mais clássica de esteganografia."]
    def __init__(self):
        super().__init__("IA-Esteganografia", "Esteganografia",
            ["esteganografia", "mensagem oculta", "lsb esteganografia", "canal encoberto"])


class IASegurancaBancoDados(_IACyberBase):
    _saudacoes = ["Criptografar dados em repouso não substitui controle de acesso correto ao banco.",
                  "Backup de banco de dados sem criptografia é um vazamento esperando para acontecer."]
    def __init__(self):
        super().__init__("IA-SegurancaBancoDados", "Segurança de Bancos de Dados",
            ["seguranca de banco de dados", "criptografia de dados", "backup seguro", "vazamento de dados"])


class IAAntiPhishing(_IACyberBase):
    _saudacoes = ["SPF, DKIM e DMARC juntos dificultam muito a falsificação do remetente de um e-mail.",
                  "Spoofing de e-mail explora a confiança no campo 'De:', que não é verificado por padrão."]
    def __init__(self):
        super().__init__("IA-AntiPhishing", "Segurança de E-mail e Anti-Phishing",
            ["phishing", "spam", "spoofing", "spf", "dkim", "dmarc"])


class IASegurancaIndustrial(_IACyberBase):
    _saudacoes = ["Ambientes ICS/SCADA priorizam disponibilidade acima de tudo — parar a planta pode ser mais perigoso que o ataque.",
                  "PLCs antigos muitas vezes nunca foram projetados pensando em segurança de rede."]
    def __init__(self):
        super().__init__("IA-SegurancaIndustrial", "Segurança Industrial (ICS/SCADA)",
            ["ics", "scada", "plc", "automacao industrial", "tecnologia operacional"])


class IASegurancaContainers(_IACyberBase):
    _saudacoes = ["Uma imagem de container desatualizada carrega vulnerabilidades conhecidas para dentro do seu cluster.",
                  "Kubernetes mal configurado (RBAC solto) pode dar a um pod comprometido acesso ao cluster inteiro."]
    def __init__(self):
        super().__init__("IA-SegurancaContainers", "Segurança de Containers",
            ["container seguranca", "docker seguranca", "kubernetes seguranca", "imagem vulneravel"])


class IAZeroTrust(_IACyberBase):
    _saudacoes = ["Zero Trust parte do princípio de que a rede interna já pode estar comprometida.",
                  "Least privilege significa dar exatamente o acesso necessário, nada além disso, por padrão."]
    def __init__(self):
        super().__init__("IA-ZeroTrust", "Arquitetura Zero Trust",
            ["zero trust", "microsegmentacao", "least privilege", "verificacao continua"])


class IADireitoDigital(_IACyberBase):
    _saudacoes = ["Este ecossistema não substitui aconselhamento jurídico profissional em crimes cibernéticos.",
                  "A tipificação de um crime cibernético varia bastante conforme a jurisdição envolvida."]
    def __init__(self):
        super().__init__("IA-DireitoDigital", "Direito Digital e Crimes Cibernéticos",
            ["crime cibernetico", "direito digital", "marco civil da internet", "lei de crimes ciberneticos"])


class IASegurancaPagamentos(_IACyberBase):
    _saudacoes = ["PCI-DSS existe porque dado de cartão é um dos alvos mais valiosos para um atacante.",
                  "Tokenização substitui o número real do cartão por um token inútil fora do contexto da transação."]
    def __init__(self):
        super().__init__("IA-SegurancaPagamentos", "Segurança de Pagamentos",
            ["pci dss", "cartao de credito seguranca", "fraude de pagamento", "tokenizacao"])


class IAAuditoriaSeguranca(_IACyberBase):
    _saudacoes = ["Uma auditoria de segurança encontra o que o dia a dia operacional deixou passar despercebido.",
                  "Controle interno fraco é, na prática, um convite documentado a falhas de segurança."]
    def __init__(self):
        super().__init__("IA-AuditoriaSeguranca", "Auditoria de Segurança da Informação",
            ["auditoria de seguranca", "conformidade de seguranca", "controle interno", "auditoria iso"])


class IABugBountyCTF(_IACyberBase):
    _saudacoes = ["Um bom relatório de bug bounty é tão importante quanto encontrar a falha em si.",
                  "CTFs ensinam técnica em ambiente controlado, sem o risco legal de um alvo real."]
    def __init__(self):
        super().__init__("IA-BugBountyCTF", "Bug Bounty e CTF",
            ["bug bounty", "ctf", "capture the flag", "hackerone", "writeup de ctf"])


class IAThreatHunting(_IACyberBase):
    _saudacoes = ["Threat hunting parte da hipótese de que já fomos comprometidos e ainda não percebemos.",
                  "Caçar ameaça é procurar TTPs sutis que não disparam alerta automático nenhum."]
    def __init__(self):
        super().__init__("IA-ThreatHunting", "Threat Hunting",
            ["threat hunting", "caca a ameacas", "hipotese de ataque", "deteccao proativa"])


class IARansomware(_IACyberBase):
    _saudacoes = ["Backup imutável e testado é a defesa mais eficaz contra ransomware, mais até que qualquer antivírus.",
                  "Pagar o resgate não garante recuperação nem impede vazamento dos dados roubados antes da criptografia."]
    def __init__(self):
        super().__init__("IA-Ransomware", "Ransomware e Extorsão Digital",
            ["ransomware", "resgate digital", "criptografia maliciosa", "backup imutavel"])
