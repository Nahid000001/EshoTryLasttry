# 🛍️ EshoTry - AI-Powered Fashion E-Commerce Platform

A modern, professional e-commerce platform built with React, Django, and AI-powered features. Experience the future of fashion shopping with virtual try-on technology and personalized recommendations.

![EshoTry Platform](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![React](https://img.shields.io/badge/React-18.0-blue)
![Django](https://img.shields.io/badge/Django-4.2-green)
![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue)
![Docker](https://img.shields.io/badge/Docker-Compose-blue)

## 🌟 Features

### 🎯 Core E-Commerce
- **Product Catalog** with categories and brands
- **Shopping Cart** with real-time updates
- **User Authentication** and profiles
- **Order Management** and tracking
- **Secure Payment Processing**

### 🤖 AI-Powered Features
- **Virtual Try-On** technology
- **AI Recommendations** based on user preferences
- **Style Quiz** for personalized suggestions
- **Smart Search** with filters and sorting

### 🎨 Professional Design
- **Modern UI/UX** with Tailwind CSS
- **Responsive Design** for all devices
- **London-focused Branding**
- **Professional E-commerce Layout**

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/eshotry.git
   cd eshotry
   ```

2. **Start the application**
   ```bash
   # For first-time setup
   .\startup.bat
   
   # For daily use
   .\quick-start.bat
   ```

3. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/api/docs/

## 🏗️ Architecture

### Frontend (React + TypeScript)
- **React 18** with functional components
- **TypeScript** for type safety
- **Vite** for fast development
- **React Router** for navigation
- **Tailwind CSS** for styling
- **Zustand** for state management

### Backend (Django + Python)
- **Django 4.2** with REST framework
- **PostgreSQL** for main database
- **MongoDB** for product data
- **Redis** for caching
- **Elasticsearch** for search
- **JWT Authentication**

### Infrastructure
- **Docker Compose** for containerization
- **Multi-service architecture**
- **Environment-based configuration**

## 📁 Project Structure

```
eshotry/
├── frontend/                 # React frontend
│   ├── src/
│   │   ├── components/      # Reusable components
│   │   ├── pages/          # Page components
│   │   ├── stores/         # Zustand stores
│   │   └── lib/            # Utilities and API
│   └── package.json
├── backend/                 # Django backend
│   ├── apps/
│   │   ├── users/          # User management
│   │   ├── products/       # Product catalog
│   │   └── orders/         # Order management
│   └── requirements.txt
├── docker-compose.yml      # Service orchestration
├── startup.bat            # First-time setup
├── quick-start.bat        # Daily startup
└── README.md
```

## 🛠️ Development

### Available Scripts

```bash
# Start all services (first time)
.\startup.bat

# Quick start (daily use)
.\quick-start.bat

# Stop all services
.\stop.bat

# Check service status
.\status.bat
```

### API Endpoints

#### Authentication
- `POST /api/auth/login/` - User login
- `POST /api/auth/register/` - User registration
- `POST /api/auth/token/refresh/` - Refresh JWT token

#### Products
- `GET /api/products/` - Product catalog
- `GET /api/products/categories/` - Product categories
- `GET /api/products/brands/` - Product brands
- `GET /api/products/collections/featured/` - Featured products

#### Orders
- `GET /api/orders/cart/` - Shopping cart
- `POST /api/orders/cart/items/` - Add to cart
- `GET /api/orders/` - Order history

## 🎨 Design System

### Color Palette
- **Primary**: Teal (#14b8a6)
- **Secondary**: Gray (#6b7280)
- **Background**: White (#ffffff)
- **Text**: Dark Gray (#111827)

### Typography
- **Headings**: Bold, professional fonts
- **Body**: Clean, readable text
- **Branding**: London-focused messaging

## 🔧 Configuration

### Environment Variables

Create `.env` files in the respective directories:

**Frontend (.env)**
```env
VITE_API_BASE_URL=http://localhost:8000/api
```

**Backend (.env)**
```env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:password@localhost:5432/eshotry
```

## 🚀 Deployment

### Production Setup

1. **Build the application**
   ```bash
   docker-compose -f docker-compose.prod.yml build
   ```

2. **Deploy with Docker**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

3. **Configure reverse proxy** (Nginx/Apache)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Django REST Framework** for the robust API
- **React Team** for the amazing frontend framework
- **Tailwind CSS** for the utility-first styling
- **Docker** for containerization

## 📞 Support

- **Email**: support@eshotry.com
- **Documentation**: [docs.eshotry.com](https://docs.eshotry.com)
- **Issues**: [GitHub Issues](https://github.com/yourusername/eshotry/issues)

---

**Made with ❤️ in London** 🇬🇧

*EshoTry - Try Before You Buy, Anywhere in London*
