# EshoTry Code Manifest

## 📁 Project Structure Overview

```
EshoTry/
├── backend/                    # Django Backend Application
├── frontend/                   # React Frontend Application
├── docs/                      # Documentation
├── docker-compose.yml         # Container orchestration
└── README.md                  # Project overview
```

## 🎯 Backend Code Manifest

### Core Django Configuration

| File Path | Purpose | Key Components |
|-----------|---------|----------------|
| `backend/eshotry/settings.py` | Django configuration | Database settings, middleware, apps, JWT config |
| `backend/eshotry/urls.py` | URL routing | API endpoints, admin, documentation |
| `backend/eshotry/wsgi.py` | WSGI configuration | Production deployment interface |
| `backend/eshotry/asgi.py` | ASGI configuration | Async deployment interface |
| `backend/eshotry/celery.py` | Celery configuration | Background task processing |
| `backend/manage.py` | Django management | Command-line utility |
| `backend/requirements.txt` | Python dependencies | All required packages |

### User Management App

| File Path | Purpose | Key Components |
|-----------|---------|----------------|
| `backend/apps/users/models.py` | User data models | User, UserAddress, UserAvatar, UserStyleQuiz |
| `backend/apps/users/serializers.py` | API serialization | User registration, login, profile serializers |
| `backend/apps/users/views.py` | API endpoints | Authentication, profile management views |
| `backend/apps/users/urls.py` | URL routing | User-related endpoints |
| `backend/apps/users/admin.py` | Django admin | User management interface |

### Product Management App

| File Path | Purpose | Key Components |
|-----------|---------|----------------|
| `backend/apps/products/models.py` | Product data models | Product, Category, Brand, ProductVariant, ProductReview |
| `backend/apps/products/serializers.py` | API serialization | Product catalog serializers |
| `backend/apps/products/views.py` | API endpoints | Product CRUD, search, filtering |
| `backend/apps/products/filters.py` | Django filters | Advanced product filtering |
| `backend/apps/products/urls.py` | URL routing | Product-related endpoints |
| `backend/apps/products/admin.py` | Django admin | Product management interface |

### Order Management App

| File Path | Purpose | Key Components |
|-----------|---------|----------------|
| `backend/apps/orders/models.py` | Order data models | Cart, CartItem, Order, OrderItem, Coupon |
| `backend/apps/orders/serializers.py` | API serialization | Cart and order processing |
| `backend/apps/orders/views.py` | API endpoints | Shopping cart, checkout, order management |
| `backend/apps/orders/urls.py` | URL routing | Order-related endpoints |
| `backend/apps/orders/admin.py` | Django admin | Order management interface |

### Virtual Try-On App

| File Path | Purpose | Key Components |
|-----------|---------|----------------|
| `backend/apps/virtual_tryon/models.py` | Try-on data models | TryOnSession, AvatarModel, TryOnResult |
| `backend/apps/virtual_tryon/serializers.py` | API serialization | Virtual try-on data handling |
| `backend/apps/virtual_tryon/views.py` | API endpoints | Try-on session management |
| `backend/apps/virtual_tryon/ai_models.py` | AI processing | MediaPipe integration, pose estimation |
| `backend/apps/virtual_tryon/tasks.py` | Background tasks | Async image processing |

### AI Recommendations App

| File Path | Purpose | Key Components |
|-----------|---------|----------------|
| `backend/apps/recommendations/models.py` | Recommendation models | UserPreference, RecommendationScore |
| `backend/apps/recommendations/engine.py` | ML algorithms | Collaborative filtering, content-based |
| `backend/apps/recommendations/views.py` | API endpoints | Personalized recommendations |
| `backend/apps/recommendations/tasks.py` | Background tasks | Model training, batch processing |

### Analytics App

| File Path | Purpose | Key Components |
|-----------|---------|----------------|
| `backend/apps/analytics/models.py` | Analytics models | UserEvent, ProductAnalytics, SalesMetrics |
| `backend/apps/analytics/views.py` | API endpoints | Dashboard data, reporting |
| `backend/apps/analytics/aggregators.py` | Data processing | Metrics calculation, insights |

## 🎨 Frontend Code Manifest

### Core Application Structure

| File Path | Purpose | Key Components |
|-----------|---------|----------------|
| `frontend/src/main.tsx` | Application entry | React rendering, providers setup |
| `frontend/src/App.tsx` | Main application | Route configuration, layout |
| `frontend/src/index.css` | Global styles | Tailwind base, component styles |
| `frontend/package.json` | Dependencies | React, TypeScript, Tailwind packages |
| `frontend/vite.config.ts` | Build configuration | Vite setup, proxy configuration |
| `frontend/tailwind.config.js` | Styling configuration | Custom theme, plugins |

### State Management

| File Path | Purpose | Key Components |
|-----------|---------|----------------|
| `frontend/src/stores/authStore.ts` | Authentication state | User login, registration, profile |
| `frontend/src/stores/cartStore.ts` | Shopping cart state | Cart items, quantities, totals |
| `frontend/src/stores/productStore.ts` | Product catalog state | Products, categories, filters |
| `frontend/src/stores/wishlistStore.ts` | Wishlist state | Saved products |

### API Integration

| File Path | Purpose | Key Components |
|-----------|---------|----------------|
| `frontend/src/lib/api.ts` | API client | Axios configuration, endpoints |
| `frontend/src/lib/utils.ts` | Utility functions | Formatting, validation, helpers |
| `frontend/src/types/index.ts` | TypeScript types | Interface definitions |

### Layout Components

| File Path | Purpose | Key Components |
|-----------|---------|----------------|
| `frontend/src/components/layout/Layout.tsx` | Main layout | Header, footer, outlet |
| `frontend/src/components/layout/Header.tsx` | Navigation header | Menu, search, cart, user menu |
| `frontend/src/components/layout/Footer.tsx` | Site footer | Links, newsletter, social media |
| `frontend/src/components/layout/MobileMenu.tsx` | Mobile navigation | Responsive menu |

### Authentication Components

| File Path | Purpose | Key Components |
|-----------|---------|----------------|
| `frontend/src/components/auth/LoginForm.tsx` | User login | Form validation, authentication |
| `frontend/src/components/auth/RegisterForm.tsx` | User registration | Account creation |
| `frontend/src/components/auth/ProtectedRoute.tsx` | Route protection | Authentication guard |
| `frontend/src/components/auth/UserDropdown.tsx` | User menu | Profile, logout options |

### Product Components

| File Path | Purpose | Key Components |
|-----------|---------|----------------|
| `frontend/src/components/products/ProductCard.tsx` | Product display | Image, price, actions |
| `frontend/src/components/products/ProductGrid.tsx` | Product listing | Grid layout, pagination |
| `frontend/src/components/products/ProductDetail.tsx` | Product details | Full product information |
| `frontend/src/components/products/ProductFilters.tsx` | Search filters | Category, price, brand filters |
| `frontend/src/components/products/ProductSearch.tsx` | Search interface | Query input, suggestions |

### Shopping Cart Components

| File Path | Purpose | Key Components |
|-----------|---------|----------------|
| `frontend/src/components/cart/CartDropdown.tsx` | Cart preview | Mini cart display |
| `frontend/src/components/cart/CartItem.tsx` | Cart item | Product details, quantity controls |
| `frontend/src/components/cart/CartSummary.tsx` | Order summary | Totals, taxes, shipping |

### Virtual Try-On Components

| File Path | Purpose | Key Components |
|-----------|---------|----------------|
| `frontend/src/components/tryon/VirtualTryOn.tsx` | Try-on interface | Main try-on component |
| `frontend/src/components/tryon/AvatarCreator.tsx` | Avatar generation | Body measurements, 3D model |
| `frontend/src/components/tryon/PhotoUpload.tsx` | Photo capture | Camera integration, upload |
| `frontend/src/components/tryon/TryOnResults.tsx` | Results display | Before/after comparison |

### UI Components

| File Path | Purpose | Key Components |
|-----------|---------|----------------|
| `frontend/src/components/ui/Button.tsx` | Button component | Various button styles |
| `frontend/src/components/ui/Input.tsx` | Input component | Form inputs, validation |
| `frontend/src/components/ui/Modal.tsx` | Modal dialog | Overlay, dialog box |
| `frontend/src/components/ui/SearchBar.tsx` | Search input | Global search functionality |
| `frontend/src/components/ui/LoadingSpinner.tsx` | Loading indicator | Async operation feedback |

### Page Components

| File Path | Purpose | Key Components |
|-----------|---------|----------------|
| `frontend/src/pages/HomePage.tsx` | Landing page | Hero, features, products |
| `frontend/src/pages/ProductListPage.tsx` | Product catalog | Search, filter, pagination |
| `frontend/src/pages/ProductDetailPage.tsx` | Product details | Full product view |
| `frontend/src/pages/CartPage.tsx` | Shopping cart | Cart management |
| `frontend/src/pages/CheckoutPage.tsx` | Checkout process | Payment, shipping |
| `frontend/src/pages/VirtualTryOnPage.tsx` | Try-on interface | Virtual fitting room |
| `frontend/src/pages/StyleQuizPage.tsx` | Style assessment | Preference collection |

### Profile Pages

| File Path | Purpose | Key Components |
|-----------|---------|----------------|
| `frontend/src/pages/profile/ProfilePage.tsx` | User profile | Account information |
| `frontend/src/pages/profile/OrdersPage.tsx` | Order history | Past purchases |
| `frontend/src/pages/profile/AddressesPage.tsx` | Address management | Shipping addresses |
| `frontend/src/pages/profile/AvatarsPage.tsx` | Avatar management | Saved avatars |

### Home Page Components

| File Path | Purpose | Key Components |
|-----------|---------|----------------|
| `frontend/src/components/home/HeroSection.tsx` | Hero banner | Main value proposition |
| `frontend/src/components/home/FeaturedProducts.tsx` | Featured items | Curated product display |
| `frontend/src/components/home/TrendingProducts.tsx` | Popular items | Trending product carousel |
| `frontend/src/components/home/CategoryGrid.tsx` | Category navigation | Visual category links |
| `frontend/src/components/home/TestimonialsSection.tsx` | Customer reviews | Social proof |
| `frontend/src/components/home/NewsletterSignup.tsx` | Email subscription | Marketing signup |

## 🐳 DevOps & Deployment

### Container Configuration

| File Path | Purpose | Key Components |
|-----------|---------|----------------|
| `docker-compose.yml` | Development setup | Multi-container orchestration |
| `docker-compose.prod.yml` | Production setup | Optimized production config |
| `backend/Dockerfile` | Backend container | Python, Django, dependencies |
| `frontend/Dockerfile` | Frontend container | Node.js, React, build process |

### CI/CD Pipeline

| File Path | Purpose | Key Components |
|-----------|---------|----------------|
| `.github/workflows/test.yml` | Automated testing | Unit tests, integration tests |
| `.github/workflows/deploy.yml` | Deployment automation | Build, test, deploy pipeline |
| `.github/workflows/security.yml` | Security scanning | Vulnerability assessment |

## 📊 Database Schemas

### Migration Files

| File Path | Purpose | Key Components |
|-----------|---------|----------------|
| `backend/apps/users/migrations/` | User schema | Database table creation |
| `backend/apps/products/migrations/` | Product schema | Catalog structure |
| `backend/apps/orders/migrations/` | Order schema | Commerce tables |

### Fixture Data

| File Path | Purpose | Key Components |
|-----------|---------|----------------|
| `backend/fixtures/sample_categories.json` | Test categories | Sample category data |
| `backend/fixtures/sample_brands.json` | Test brands | Sample brand data |
| `backend/fixtures/sample_products.json` | Test products | Sample product catalog |

## 🧪 Testing Suite

### Backend Tests

| File Path | Purpose | Key Components |
|-----------|---------|----------------|
| `backend/apps/users/tests.py` | User functionality | Authentication, profile tests |
| `backend/apps/products/tests.py` | Product features | Catalog, search tests |
| `backend/apps/orders/tests.py` | Commerce logic | Cart, checkout tests |
| `backend/tests/test_api.py` | API integration | Endpoint testing |

### Frontend Tests

| File Path | Purpose | Key Components |
|-----------|---------|----------------|
| `frontend/src/components/__tests__/` | Component tests | Unit testing components |
| `frontend/src/pages/__tests__/` | Page tests | Integration testing |
| `frontend/src/utils/__tests__/` | Utility tests | Function testing |

## 📚 Documentation

| File Path | Purpose | Key Components |
|-----------|---------|----------------|
| `docs/ARCHITECTURE.md` | System design | High-level architecture |
| `docs/DEPLOYMENT.md` | Deployment guide | Setup instructions |
| `docs/API.md` | API documentation | Endpoint specifications |
| `docs/TESTING.md` | Testing strategy | Test coverage, methodology |
| `docs/CODE_MANIFEST.md` | Code organization | This document |

## 🔧 Configuration Files

### Environment Configuration

| File Path | Purpose | Key Components |
|-----------|---------|----------------|
| `backend/env.example` | Environment template | Required variables |
| `frontend/.env.example` | Frontend environment | API URLs, feature flags |

### Code Quality

| File Path | Purpose | Key Components |
|-----------|---------|----------------|
| `backend/.pylintrc` | Python linting | Code quality rules |
| `frontend/.eslintrc.js` | JavaScript linting | React, TypeScript rules |
| `frontend/.prettierrc` | Code formatting | Style consistency |

### Build Configuration

| File Path | Purpose | Key Components |
|-----------|---------|----------------|
| `frontend/tsconfig.json` | TypeScript config | Compilation settings |
| `frontend/tsconfig.node.json` | Node TypeScript | Build tool configuration |
| `backend/pyproject.toml` | Python project | Package configuration |

## 📈 Contribution Summary

### Backend Development
- **Django application structure** with modular apps
- **RESTful API design** with comprehensive serializers
- **Database modeling** for e-commerce domain
- **Authentication system** with JWT tokens
- **Background task processing** with Celery
- **AI integration** for recommendations and virtual try-on

### Frontend Development
- **Modern React application** with TypeScript
- **Responsive design** with Tailwind CSS
- **State management** with Zustand
- **API integration** with React Query
- **Component-based architecture** with reusable UI
- **Progressive enhancement** for virtual try-on features

### DevOps & Infrastructure
- **Containerization** with Docker and Docker Compose
- **CI/CD pipeline** with GitHub Actions
- **Multi-database architecture** (PostgreSQL, MongoDB, Redis, Elasticsearch)
- **Production deployment** configuration
- **Monitoring and logging** setup

### Documentation & Testing
- **Comprehensive documentation** for architecture and deployment
- **Testing strategy** for both frontend and backend
- **Code organization** with clear separation of concerns
- **Development workflow** with proper tooling

## 🎯 Key Features Implemented

1. **User Management**: Registration, authentication, profile management
2. **Product Catalog**: Products, categories, brands, reviews, wishlist
3. **Shopping Experience**: Cart, checkout, order management
4. **Virtual Try-On**: Avatar creation, photo upload, size comparison
5. **AI Recommendations**: Personalized product suggestions
6. **Search & Filtering**: Advanced product discovery
7. **Responsive Design**: Mobile-first, accessible interface
8. **Admin Dashboard**: Product and user management
9. **Analytics**: User behavior and sales metrics
10. **Payment Integration**: Stripe payment processing

This code manifest provides a comprehensive overview of the EshoTry platform's structure, highlighting the key components and their purposes in building a modern, scalable e-commerce platform with advanced AI features.
