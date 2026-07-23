#!/bin/bash
# ============================================================================
# SYTHERION 2.0 - Instalador (Linux / macOS)
# ============================================================================
# 1. Cria um ambiente virtual Python isolado (.venv)
# 2. Instala as dependências dentro dele
# 3. Gera o "iniciar.sh" - o script que você vai usar dali pra frente
# 4. Roda o programa agora mesmo (primeira execução)
# ============================================================================
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

echo "════════════════════════════════════════════════════════════"
echo "  SYTHERION 2.0 — Instalador"
echo "════════════════════════════════════════════════════════════"

if ! command -v python3 &> /dev/null; then
    echo "[ERRO] python3 não encontrado. Instale o Python 3.9+ antes de continuar."
    exit 1
fi

if [ ! -d ".venv" ]; then
    echo "[*] Criando ambiente virtual em .venv ..."
    python3 -m venv .venv
else
    echo "[*] Ambiente virtual .venv já existe, reaproveitando."
fi

echo "[*] Ativando ambiente virtual..."
# shellcheck disable=SC1091
source .venv/bin/activate

echo "[*] Instalando dependências (requirements.txt)..."
pip install --upgrade pip -q
pip install -r requirements.txt -q

echo "[*] Gerando o iniciador (iniciar.sh)..."
cat > iniciar.sh << 'INICIADOR_EOF'
#!/bin/bash
# Gerado automaticamente por instalar.sh — não precisa editar isso.
# Sobe o servidor Sytherion e abre a página da IA no navegador.
set -e
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"
# shellcheck disable=SC1091
source .venv/bin/activate

HOST="127.0.0.1"
PORT="8000"
URL="http://${HOST}:${PORT}"

echo "════════════════════════════════════════════════════════════"
echo "  SYTHERION 2.0 — iniciando"
echo "════════════════════════════════════════════════════════════"

python3 -m uvicorn sytherion.backend.api:app --host "$HOST" --port "$PORT" &
SERVER_PID=$!

trap 'echo; echo "Encerrando Sytherion 2.0..."; kill $SERVER_PID 2>/dev/null; exit 0' INT TERM

echo "[*] Aguardando o servidor subir..."
for i in $(seq 1 40); do
    if curl -s "${URL}/api/status" > /dev/null 2>&1; then
        echo "[OK] Servidor no ar."
        break
    fi
    sleep 0.5
done

echo "[*] Abrindo ${URL} no navegador..."
if command -v xdg-open > /dev/null 2>&1; then
    xdg-open "$URL" > /dev/null 2>&1 &
elif command -v open > /dev/null 2>&1; then
    open "$URL"
else
    echo "Não consegui abrir o navegador automaticamente."
    echo "Abra manualmente: $URL"
fi

echo
echo "Sytherion 2.0 rodando em ${URL}"
echo "Pressione Ctrl+C aqui para encerrar o servidor."
wait $SERVER_PID
INICIADOR_EOF

chmod +x iniciar.sh

echo
echo "════════════════════════════════════════════════════════════"
echo "  Instalação concluída!"
echo "════════════════════════════════════════════════════════════"
echo "  A partir de agora, para rodar o Sytherion, use apenas:"
echo
echo "      ./iniciar.sh"
echo
echo "  Iniciando agora, pela primeira vez..."
echo "════════════════════════════════════════════════════════════"
echo

./iniciar.sh
