# 🚀 EshoTry Quick Start Guide

## Prerequisites

- Docker Desktop installed and running
- Git (for cloning the repository)

## Quick Setup (5 minutes)

### Option 1: Automated Setup (Recommended)

**For Windows:**
```bash
# Run the automated setup script
startup.bat
```

**For macOS/Linux:**
```bash
# Make the script executable
chmod +x startup.sh

# Run the automated setup script
./startup.sh
```

### Option 2: Manual Setup

1. **Start the services:**
```bash
docker-compose up -d
```

2. **Wait for services to start (about 30 seconds)**

3. **Run database migrations:**
```bash
docker-compose exec backend python manage.py migrate
```

4. **Create an admin user:**
```bash
docker-compose exec backend python manage.py createsuperuser
```

## Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/api  
- **Admin Panel**: http://localhost:8000/admin
- **API Documentation**: http://localhost:8000/api/docs

## Troubleshooting

### If Docker build fails:

1. **Clean Docker cache:**
```bash
docker system prune -f
docker-compose down -v
```

2. **Rebuild containers:**
```bash
docker-compose build --no-cache
docker-compose up -d
```

### If services don't start:

1. **Check logs:**
```bash
docker-compose logs backend
docker-compose logs frontend
```

2. **Check service status:**
```bash
docker-compose ps
```

3. **Restart specific service:**
```bash
docker-compose restart backend
```

### Common Issues:

**Port conflicts:**
- Make sure ports 3000, 8000, 5432, 27017, 6379, 9200 are not in use
- Stop any existing services on these ports

**Memory issues:**
- Increase Docker memory allocation to at least 4GB
- Close unnecessary applications

**Permission issues (Linux/macOS):**
```bash
sudo chown -R $USER:$USER .
```

## Development Workflow

### Backend Development

```bash
# Access backend container
docker-compose exec backend bash

# Run Django commands
python manage.py shell
python manage.py test
python manage.py collectstatic
```

### Frontend Development

```bash
# Access frontend container
docker-compose exec frontend sh

# Run npm commands
npm test
npm run lint
npm run build
```

### Database Management

```bash
# PostgreSQL
docker-compose exec postgres psql -U postgres eshotry

# MongoDB
docker-compose exec mongodb mongosh eshotry

# Redis CLI
docker-compose exec redis redis-cli
```

## Sample Data

### Create sample categories and products:

```bash
# Access Django shell
docker-compose exec backend python manage.py shell

# In Django shell:
from apps.products.models import Category, Brand
Category.objects.create(name='Women', slug='women')
Category.objects.create(name='Men', slug='men')
Brand.objects.create(name='Nike', slug='nike')
```

## Environment Configuration

Create `.env` files for custom configuration:

**Backend (.env):**
```
DEBUG=True
SECRET_KEY=your-secret-key
DB_NAME=eshotry
DB_USER=postgres
DB_PASSWORD=postgres
```

**Frontend (.env):**
```
VITE_API_BASE_URL=http://localhost:8000/api
```

## Next Steps

1. **Explore the Admin Panel** - Add products, categories, and users
2. **Test the Frontend** - Browse products, create accounts, test shopping cart
3. **API Testing** - Use the interactive API docs at `/api/docs`
4. **Customize** - Modify components, add features, update styling

## Getting Help

- Check the logs: `docker-compose logs`
- View running services: `docker-compose ps`
- Access container shell: `docker-compose exec <service> bash`
- Stop all services: `docker-compose down`
- Remove all data: `docker-compose down -v`

---

🎉 **You're ready to start developing with EshoTry!**
