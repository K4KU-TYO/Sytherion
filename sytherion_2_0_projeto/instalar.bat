@echo off
REM ============================================================================
REM SYTHERION 2.0 - Instalador (Windows)
REM ============================================================================
REM 1. Cria um ambiente virtual Python isolado (.venv)
REM 2. Instala as dependencias dentro dele
REM 3. Gera o "iniciar.bat" - o script que voce vai usar dali pra frente
REM 4. Roda o programa agora mesmo (primeira execucao)
REM ============================================================================

cd /d "%~dp0"

echo ================================================================
echo   SYTHERION 2.0 - Instalador
echo ================================================================

where python >nul 2>nul
if errorlevel 1 (
    echo [ERRO] python nao encontrado no PATH. Instale o Python 3.9+ antes de continuar.
    pause
    exit /b 1
)

if not exist ".venv" (
    echo [*] Criando ambiente virtual em .venv ...
    python -m venv .venv
) else (
    echo [*] Ambiente virtual .venv ja existe, reaproveitando.
)

echo [*] Ativando ambiente virtual...
call .venv\Scripts\activate.bat

echo [*] Instalando dependencias (requirements.txt)...
python -m pip install --upgrade pip -q
python -m pip install -r requirements.txt -q

echo [*] Gerando o iniciador (iniciar.bat)...

echo @echo off > iniciar.bat
echo REM Gerado automaticamente por instalar.bat - nao precisa editar isso. >> iniciar.bat
echo cd /d "%%~dp0" >> iniciar.bat
echo call .venv\Scripts\activate.bat >> iniciar.bat
echo echo ================================================================ >> iniciar.bat
echo echo   SYTHERION 2.0 - iniciando >> iniciar.bat
echo echo ================================================================ >> iniciar.bat
echo start "Sytherion 2.0 - servidor" /min cmd /c "python -m uvicorn sytherion.backend.api:app --host 127.0.0.1 --port 8000" >> iniciar.bat
echo echo [*] Aguardando o servidor subir... >> iniciar.bat
echo timeout /t 5 /nobreak ^>nul >> iniciar.bat
echo start http://127.0.0.1:8000 >> iniciar.bat
echo echo. >> iniciar.bat
echo echo Sytherion 2.0 rodando em http://127.0.0.1:8000 >> iniciar.bat
echo echo Feche a janela minimizada "Sytherion 2.0 - servidor" para encerrar. >> iniciar.bat
echo pause >> iniciar.bat

echo.
echo ================================================================
echo   Instalacao concluida!
echo ================================================================
echo   A partir de agora, para rodar o Sytherion, use apenas:
echo.
echo       iniciar.bat
echo.
echo   Iniciando agora, pela primeira vez...
echo ================================================================
echo.

call iniciar.bat
