@echo off
echo 🚀 Starting EshoTry Platform Setup...

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not running. Please start Docker and try again.
    pause
    exit /b 1
)

echo ✅ Docker is running

REM Stop any existing containers
echo 🛑 Stopping existing containers...
docker-compose down

REM Start the services
echo 🔧 Starting services...
docker-compose up -d postgres mongodb redis

REM Wait for databases to be ready
echo ⏳ Waiting for databases to be ready...
timeout /t 10 /nobreak

REM Start the main services
echo 🚀 Starting main services...
docker-compose up -d

REM Wait for services to start
echo ⏳ Waiting for services to start...
timeout /t 20 /nobreak

REM Check service status
echo 📊 Checking service status...
docker-compose ps

echo.
echo ✅ Setup complete!
echo.
echo 🌐 Access URLs:
echo    Frontend: http://localhost:3000
echo    Backend API: http://localhost:8000/api
echo    Admin Panel: http://localhost:8000/admin
echo.
echo 📝 Next steps:
echo    1. Wait a few more seconds for all services to fully start
echo    2. Run migrations: docker-compose exec backend python manage.py migrate
echo    3. Create superuser: docker-compose exec backend python manage.py createsuperuser
echo.
pause
