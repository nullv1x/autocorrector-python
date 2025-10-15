@echo off
REM ============================================================================
REM Script de Compilación - Autocorrector de Tildes
REM Genera un archivo .exe independiente
REM ============================================================================

echo.
echo ========================================
echo  COMPILADOR A EXE
echo  Autocorrector de Tildes
echo ========================================
echo.

REM Activar entorno virtual
if not exist venv (
    echo [ERROR] Entorno virtual no encontrado
    echo Ejecuta install.bat primero
    pause
    exit /b 1
)

call venv\Scripts\activate.bat

REM Instalar PyInstaller si no está instalado
echo Verificando PyInstaller...
pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo Instalando PyInstaller...
    pip install pyinstaller
    echo [OK] PyInstaller instalado
)
echo.

REM Limpiar compilaciones anteriores
echo Limpiando archivos anteriores...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist AutocorrectorTildes.spec del /q AutocorrectorTildes.spec
echo [OK] Limpieza completada
echo.

REM Compilar aplicación
echo ========================================
echo  COMPILANDO...
echo  Esto puede tomar varios minutos
echo ========================================
echo.

pyinstaller --onefile ^
    --windowed ^
    --name="AutocorrectorTildes" ^
    --add-data="data;data" ^
    --add-data="config;config" ^
    --hidden-import=PyQt6.QtCore ^
    --hidden-import=PyQt6.QtGui ^
    --hidden-import=PyQt6.QtWidgets ^
    --hidden-import=keyboard ^
    --hidden-import=pyautogui ^
    --hidden-import=pystray ^
    --hidden-import=PIL ^
    --collect-all=PyQt6 ^
    main.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] La compilacion fallo
    pause
    exit /b 1
)

echo.
echo ========================================
echo  COMPILACION EXITOSA
echo ========================================
echo.
echo El ejecutable se encuentra en:
echo   dist\AutocorrectorTildes.exe
echo.
echo IMPORTANTE:
echo   - Ejecuta el .exe como ADMINISTRADOR
echo   - Copia las carpetas 'data' y 'config' junto al .exe
echo     (PyInstaller ya las incluyo, pero por seguridad)
echo.

REM Crear un archivo de instrucciones
echo Creando instrucciones de uso...
(
echo ========================================
echo  INSTRUCCIONES - AutocorrectorTildes
echo ========================================
echo.
echo 1. Ejecuta AutocorrectorTildes.exe como ADMINISTRADOR
echo    ^(Clic derecho -^> Ejecutar como administrador^)
echo.
echo 2. En el primer inicio:
echo    - Lee el mensaje de bienvenida
echo    - Elige si deseas ejecutar en segundo plano
echo.
echo 3. Uso basico:
echo    - Activa el corrector desde la ventana principal
echo    - O usa el atajo: Ctrl+Shift+A
echo.
echo 4. El programa se ejecutara en la bandeja del sistema
echo    ^(icono junto al reloj^)
echo.
echo Para mas informacion, consulta README.md
echo.
) > dist\INSTRUCCIONES.txt

echo [OK] Instrucciones creadas en dist\INSTRUCCIONES.txt
echo.
pause