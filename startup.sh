#!/bin/bash

echo "🚀 Starting EshoTry Platform Setup..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

echo "✅ Docker is running"

# Stop any existing containers
echo "🛑 Stopping existing containers..."
docker-compose down

# Clean up any existing volumes (optional)
read -p "Do you want to clean up existing data? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🧹 Cleaning up volumes..."
    docker-compose down -v
    docker system prune -f
fi

# Start the services
echo "🔧 Starting services..."
docker-compose up -d postgres mongodb redis

# Wait for databases to be ready
echo "⏳ Waiting for databases to be ready..."
sleep 10

# Start the main services
echo "🚀 Starting main services..."
docker-compose up -d

# Wait for services to start
echo "⏳ Waiting for services to start..."
sleep 20

# Check service status
echo "📊 Checking service status..."
docker-compose ps

# Show logs for any failed services
if ! docker-compose ps | grep -q "Up"; then
    echo "❌ Some services failed to start. Showing logs..."
    docker-compose logs
else
    echo "✅ All services are running!"
    echo ""
    echo "🌐 Access URLs:"
    echo "   Frontend: http://localhost:3000"
    echo "   Backend API: http://localhost:8000/api"
    echo "   Admin Panel: http://localhost:8000/admin"
    echo ""
    echo "📝 Next steps:"
    echo "   1. Wait a few more seconds for all services to fully start"
    echo "   2. Run migrations: docker-compose exec backend python manage.py migrate"
    echo "   3. Create superuser: docker-compose exec backend python manage.py createsuperuser"
    echo ""
fi
