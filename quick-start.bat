@echo off
echo 🚀 EshoTry Quick Start...

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not running. Please start Docker Desktop first!
    pause
    exit /b 1
)

REM Check if containers are already running
docker-compose ps --filter "status=running" | findstr "eshotry" >nul
if not errorlevel 1 (
    echo ✅ EshoTry is already running!
    echo.
    goto :show_urls
)

echo 🔧 Starting EshoTry services...
docker-compose up -d

echo ⏳ Waiting for services to start...
timeout /t 15 /nobreak

:show_urls
echo.
echo 🌐 EshoTry is ready! Access at:
echo    🏠 Website: http://localhost:3000
echo    🔧 Admin: http://localhost:8000/admin  
echo    📚 API Docs: http://localhost:8000/api/docs/
echo.

REM Check status
docker-compose ps

pause
