# EshoTry Deployment Guide

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose installed
- Git
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)

### 1. Clone Repository

```bash
git clone <repository-url>
cd EshoTry
```

### 2. Environment Setup

```bash
# Copy environment files
cp backend/env.example backend/.env
cp frontend/.env.example frontend/.env

# Edit environment variables as needed
# Update database credentials, API keys, etc.
```

### 3. Docker Deployment (Recommended)

```bash
# Start all services
docker-compose up -d

# Check services status
docker-compose ps

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

### 4. Initialize Database

```bash
# Run migrations
docker-compose exec backend python manage.py migrate

# Create superuser
docker-compose exec backend python manage.py createsuperuser

# Load sample data (optional)
docker-compose exec backend python manage.py loaddata fixtures/sample_data.json
```

### 5. Access Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/api
- **Admin Panel**: http://localhost:8000/admin
- **API Documentation**: http://localhost:8000/api/docs

## 📋 Manual Development Setup

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up databases (PostgreSQL, MongoDB, Redis, Elasticsearch)
# Update .env file with connection details

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### Background Services

```bash
# Start Celery worker (in separate terminal)
cd backend
celery -A eshotry worker -l info

# Start Celery beat scheduler (in separate terminal)
cd backend
celery -A eshotry beat -l info
```

## 🌐 Production Deployment

### AWS Deployment

#### 1. Infrastructure Setup

```bash
# Using AWS CDK or Terraform
# - EC2 instances or ECS cluster
# - RDS PostgreSQL
# - ElastiCache Redis
# - Elasticsearch Service
# - S3 bucket for media files
# - CloudFront CDN
# - Load Balancer
```

#### 2. Environment Variables

```bash
# Production environment variables
DEBUG=False
SECRET_KEY=your-super-secret-production-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DB_HOST=your-rds-endpoint
DB_NAME=eshotry_prod
DB_USER=your-db-user
DB_PASSWORD=your-db-password

# Redis
REDIS_HOST=your-elasticache-endpoint

# S3 Storage
USE_S3=True
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name

# Email
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@domain.com
EMAIL_HOST_PASSWORD=your-app-password

# Stripe
STRIPE_PUBLISHABLE_KEY=pk_live_your_publishable_key
STRIPE_SECRET_KEY=sk_live_your_secret_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret

# Monitoring
SENTRY_DSN=your-sentry-dsn
```

#### 3. Docker Production Build

```dockerfile
# Production Dockerfile for backend
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Start with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "eshotry.wsgi:application"]
```

```dockerfile
# Production Dockerfile for frontend
FROM node:18-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### DigitalOcean Deployment

#### 1. Droplet Setup

```bash
# Create Ubuntu 22.04 droplet
# Install Docker and Docker Compose
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

#### 2. Application Deployment

```bash
# Clone repository
git clone <repository-url>
cd EshoTry

# Set up environment
cp backend/env.example backend/.env
# Edit .env with production values

# Deploy with Docker Compose
docker-compose -f docker-compose.prod.yml up -d

# Set up SSL with Let's Encrypt
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

## 🔄 CI/CD Pipeline

### GitHub Actions Workflow

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: 3.11
    
    - name: Install dependencies
      run: |
        cd backend
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        cd backend
        python manage.py test
    
    - name: Set up Node.js
      uses: actions/setup-node@v3
      with:
        node-version: 18
    
    - name: Install frontend dependencies
      run: |
        cd frontend
        npm ci
    
    - name: Run frontend tests
      run: |
        cd frontend
        npm test

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy to production
      uses: appleboy/ssh-action@v0.1.5
      with:
        host: ${{ secrets.HOST }}
        username: ${{ secrets.USERNAME }}
        key: ${{ secrets.PRIVATE_KEY }}
        script: |
          cd /var/www/eshotry
          git pull origin main
          docker-compose down
          docker-compose build
          docker-compose up -d
          docker-compose exec -T backend python manage.py migrate
          docker-compose exec -T backend python manage.py collectstatic --noinput
```

## 📊 Monitoring & Logging

### Application Monitoring

```python
# settings.py - Sentry integration
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn=os.getenv('SENTRY_DSN'),
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True
)
```

### Health Checks

```python
# backend/health/views.py
from django.http import JsonResponse
from django.db import connection

def health_check(request):
    try:
        # Check database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        return JsonResponse({
            'status': 'healthy',
            'database': 'connected',
            'timestamp': timezone.now().isoformat()
        })
    except Exception as e:
        return JsonResponse({
            'status': 'unhealthy',
            'error': str(e)
        }, status=500)
```

### Log Configuration

```python
# settings.py - Production logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/eshotry/django.log',
            'maxBytes': 1024*1024*15,  # 15MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

## 🔧 Maintenance

### Database Backup

```bash
# PostgreSQL backup
docker-compose exec postgres pg_dump -U postgres eshotry > backup_$(date +%Y%m%d_%H%M%S).sql

# MongoDB backup
docker-compose exec mongodb mongodump --db eshotry --out /backup/mongodb_$(date +%Y%m%d_%H%M%S)
```

### Updates and Migrations

```bash
# Zero-downtime deployment
docker-compose pull
docker-compose up -d --no-deps backend
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py collectstatic --noinput
```

### SSL Certificate Renewal

```bash
# Automatic renewal with cron
0 12 * * * /usr/bin/certbot renew --quiet
```

## 🔍 Troubleshooting

### Common Issues

1. **Database Connection Issues**
   ```bash
   # Check database container
   docker-compose logs postgres
   
   # Test connection
   docker-compose exec backend python manage.py dbshell
   ```

2. **Static Files Not Loading**
   ```bash
   # Collect static files
   docker-compose exec backend python manage.py collectstatic --noinput
   
   # Check file permissions
   docker-compose exec backend ls -la /app/staticfiles/
   ```

3. **Memory Issues**
   ```bash
   # Monitor container resources
   docker stats
   
   # Increase memory limits in docker-compose.yml
   services:
     backend:
       deploy:
         resources:
           limits:
             memory: 1G
   ```

### Performance Optimization

1. **Database Optimization**
   ```sql
   -- Add database indexes
   CREATE INDEX idx_products_status_featured ON products(status, is_featured);
   CREATE INDEX idx_orders_user_status ON orders(user_id, status);
   ```

2. **Caching Strategy**
   ```python
   # settings.py
   CACHES = {
       'default': {
           'BACKEND': 'django_redis.cache.RedisCache',
           'LOCATION': 'redis://redis:6379/1',
           'OPTIONS': {
               'CLIENT_CLASS': 'django_redis.client.DefaultClient',
           }
       }
   }
   ```

3. **CDN Configuration**
   ```python
   # Static files CDN
   if USE_S3:
       STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
       DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
       AWS_S3_CUSTOM_DOMAIN = 'cdn.yourdomain.com'
   ```
