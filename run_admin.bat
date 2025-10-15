@echo off
REM ============================================================================
REM Script de Ejecución - Autocorrector de Tildes
REM Ejecuta automáticamente como administrador
REM ============================================================================

REM Verificar si ya se está ejecutando como administrador
net session >nul 2>&1
if %errorlevel% == 0 (
    REM Ya es administrador, ejecutar directamente
    goto :run_app
) else (
    REM No es administrador, solicitar elevación
    echo Solicitando permisos de administrador...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

:run_app
cd /d "%~dp0"

echo.
echo ========================================
echo  AUTOCORRECTOR DE TILDES
echo ========================================
echo.

REM Verificar si existe el entorno virtual
if not exist venv (
    echo [ERROR] Entorno virtual no encontrado
    echo Por favor ejecuta install.bat primero
    echo.
    pause
    exit /b 1
)

REM Activar entorno virtual y ejecutar
echo Iniciando aplicacion...
call venv\Scripts\activate.bat
python main.py

REM Si el programa cierra, mantener ventana abierta
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] La aplicacion se cerro con errores
    pause
)