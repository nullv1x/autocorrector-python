@echo off
REM ============================================================================
REM Script de Instalación - Autocorrector de Tildes
REM ============================================================================

echo.
echo ========================================
echo  AUTOCORRECTOR DE TILDES - INSTALADOR
echo ========================================
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python no está instalado o no está en el PATH
    echo.
    echo Por favor instala Python 3.11 o superior desde:
    echo https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo [OK] Python detectado
python --version
echo.

REM Verificar versión de Python
python -c "import sys; exit(0 if sys.version_info >= (3, 11) else 1)"
if %errorlevel% neq 0 (
    echo [ERROR] Se requiere Python 3.11 o superior
    pause
    exit /b 1
)

echo [OK] Versión de Python compatible
echo.

REM Crear entorno virtual
echo [1/4] Creando entorno virtual...
if exist venv (
    echo El entorno virtual ya existe
) else (
    python -m venv venv
    echo [OK] Entorno virtual creado
)
echo.

REM Activar entorno virtual
echo [2/4] Activando entorno virtual...
call venv\Scripts\activate.bat
echo [OK] Entorno virtual activado
echo.

REM Actualizar pip
echo [3/4] Actualizando pip...
python -m pip install --upgrade pip --quiet
echo [OK] pip actualizado
echo.

REM Instalar dependencias
echo [4/4] Instalando dependencias...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Falló la instalación de dependencias
    pause
    exit /b 1
)
echo [OK] Dependencias instaladas correctamente
echo.

REM Crear estructura de carpetas
echo Creando estructura de carpetas...
if not exist core mkdir core
if not exist ui mkdir ui
if not exist config mkdir config
if not exist data mkdir data
echo [OK] Estructura de carpetas creada
echo.

echo ========================================
echo  INSTALACION COMPLETADA EXITOSAMENTE
echo ========================================
echo.
echo Para ejecutar la aplicacion:
echo   1. Abre una terminal como ADMINISTRADOR
echo   2. Navega a esta carpeta
echo   3. Ejecuta: venv\Scripts\activate
echo   4. Ejecuta: python main.py
echo.
echo O simplemente ejecuta: run_admin.bat
echo.
pause