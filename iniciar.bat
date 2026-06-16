@echo off
setlocal enabledelayedexpansion

echo ========================================
echo    Kofu v0.7 (Beta) - Plataforma de IA para Office
echo ========================================
echo.
echo Directorio actual: %~dp0
echo.

echo Comprobando Ollama...
where ollama >nul 2>&1
if %errorlevel% == 0 (
    echo ✅ Ollama encontrado!
    echo Iniciando Ollama en segundo plano...
    start /b "" ollama serve
    timeout /t 2 /nobreak >nul
    echo ✅ Ollama listo!
) else (
    echo ⚠️ Ollama no encontrado. Usando razonamiento básico.
)
echo.

cd /d "%~dp0backend"

if not exist "server.py" (
    echo ERROR: No se encuentra server.py en: %CD%
    echo.
    echo Contenido del directorio:
    dir
    echo.
    pause
    exit /b 1
)

echo Iniciando servidor Kofu...
echo.
echo Servidor en http://localhost:5000
echo.

echo Abriendo web/index.html...
start "" "%~dp0web\index.html"

start /b "" py server.py
timeout /t 3 /nobreak >nul

echo.
echo El servidor se esta ejecutando en segundo plano
echo Presiona cualquier tecla para detenerlo
pause >nul

taskkill /F /IM python.exe 2>nul
taskkill /F /IM ollama.exe 2>nul

echo.
echo Servidor detenido.
echo.

endlocal
