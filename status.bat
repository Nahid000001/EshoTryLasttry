@echo off
echo 📊 EshoTry Platform Status...
echo.

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not running
    pause
    exit /b 1
)

echo ✅ Docker is running
echo.

REM Show container status
echo 🐳 Container Status:
docker-compose ps

echo.
echo 🌐 If services are running, access at:
echo    🏠 Website: http://localhost:3000
echo    🔧 Admin: http://localhost:8000/admin  
echo    📚 API: http://localhost:8000/api/docs/

pause
