import { Link } from 'react-router-dom'
import { useState, useEffect } from 'react'

interface Product {
  id: string;
  name: string;
  short_description: string;
  base_price: string;
  current_price: number;
  category_name: string;
  brand_name: string;
  gender: string;
  sku: string;
}

interface Category {
  id: string;
  name: string;
  slug: string;
  description: string;
}

export default function HomePage() {
  const [products, setProducts] = useState<Product[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // Fetch products and categories from the API
        const [productsRes, categoriesRes] = await Promise.all([
          fetch('http://localhost:8000/api/products/collections/featured/'),
          fetch('http://localhost:8000/api/products/categories/')
        ]);
        
        if (productsRes.ok && categoriesRes.ok) {
          const productsData = await productsRes.json();
          const categoriesData = await categoriesRes.json();
          
          setProducts(productsData.results || []);
          setCategories(categoriesData.results || []);
        }
      } catch (error) {
        console.error('Error fetching data:', error);
        // Set empty arrays even on error so page still loads
        setProducts([]);
        setCategories([]);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  return (
    <div className="min-h-screen bg-white">
      {/* Simple Header */}
      <header className="bg-gray-900 text-white py-4">
        <div className="max-w-7xl mx-auto px-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-teal-500 rounded-full flex items-center justify-center">
                <span className="text-white font-bold text-lg">E</span>
              </div>
              <div>
                <h1 className="text-xl font-bold">EshoTry</h1>
                <p className="text-xs text-gray-400">Try Before You Buy – Anywhere in London</p>
              </div>
            </div>
            <nav className="flex space-x-6">
              <Link to="/products" className="text-sm hover:text-teal-400">Products</Link>
              <Link to="/cart" className="text-sm hover:text-teal-400">Cart</Link>
              <Link to="/login" className="text-sm hover:text-teal-400">Login</Link>
            </nav>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="bg-gradient-to-br from-gray-50 to-gray-100 py-20">
        <div className="max-w-7xl mx-auto px-4 text-center">
          <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
            London's Premier Fashion Destination
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            Experience AI-powered virtual try-on technology and curated collections from the city's finest brands. 
            Try before you buy, anywhere in London.
          </p>
          <div className="space-x-4">
            <Link
              to="/products"
              className="bg-teal-500 text-white px-8 py-3 rounded-lg font-semibold hover:bg-teal-600 transition-colors inline-block"
            >
              Shop Now
            </Link>
            <Link
              to="/try-on"
              className="border border-teal-500 text-teal-500 px-8 py-3 rounded-lg font-semibold hover:bg-teal-500 hover:text-white transition-colors inline-block"
            >
              Try Virtual Fitting
            </Link>
          </div>
        </div>
      </section>

      {/* Categories Section */}
      {categories.length > 0 && (
        <section className="py-16">
          <div className="max-w-7xl mx-auto px-4">
            <div className="text-center mb-12">
              <h2 className="text-3xl font-bold text-gray-900 mb-4">Shop by Category</h2>
              <p className="text-lg text-gray-600">Discover our curated collections</p>
            </div>
            
            <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-6">
              {categories.slice(0, 6).map((category) => (
                <Link
                  key={category.id}
                  to={`/products?category=${category.slug}`}
                  className="group text-center"
                >
                  <div className="w-full aspect-square bg-gradient-to-br from-teal-400 to-teal-600 rounded-lg mb-4 flex items-center justify-center group-hover:scale-105 transition-transform">
                    <span className="text-white text-2xl font-bold">
                      {category.name.charAt(0)}
                    </span>
                  </div>
                  <h3 className="font-semibold text-gray-900 text-sm">{category.name}</h3>
                </Link>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* Featured Products */}
      {products.length > 0 && (
        <section className="py-16 bg-gray-50">
          <div className="max-w-7xl mx-auto px-4">
            <div className="text-center mb-12">
              <h2 className="text-3xl font-bold text-gray-900 mb-4">Featured Products</h2>
              <p className="text-lg text-gray-600">Check out our latest and most popular items</p>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {products.slice(0, 4).map((product) => (
                <div key={product.id} className="bg-white rounded-lg shadow-sm hover:shadow-lg transition-shadow overflow-hidden">
                  <div className="w-full h-64 bg-gradient-to-br from-gray-200 to-gray-300 relative">
                    <div className="w-full h-full flex items-center justify-center">
                      <span className="text-gray-600 text-2xl font-bold">
                        {product.name.charAt(0)}
                      </span>
                    </div>
                    <button className="absolute bottom-3 left-3 right-3 bg-teal-500 text-white py-2 px-4 rounded-md hover:bg-teal-600 transition-colors text-sm font-medium">
                      Add to Cart
                    </button>
                  </div>
                  <div className="p-4">
                    <p className="text-sm text-gray-500 mb-1">{product.brand_name}</p>
                    <h3 className="font-medium text-gray-900 mb-2">{product.name}</h3>
                    <div className="flex items-center justify-between">
                      <span className="text-lg font-semibold text-gray-900">£{product.current_price}</span>
                      <div className="flex items-center text-sm text-gray-500">
                        <span className="text-yellow-400">★</span>
                        <span className="ml-1">4.5 (124)</span>
                      </div>
                    </div>
                    <p className="text-xs text-gray-400 mt-2">89 try-ons</p>
                  </div>
                </div>
              ))}
            </div>
            
            <div className="text-center mt-12">
              <Link
                to="/products"
                className="bg-teal-500 text-white px-8 py-3 rounded-lg font-semibold hover:bg-teal-600 transition-colors"
              >
                View All Products
              </Link>
            </div>
          </div>
        </section>
      )}

      {/* Features Section */}
      <section className="py-16">
        <div className="max-w-7xl mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">Why Choose EshoTry?</h2>
            <p className="text-lg text-gray-600">Experience the future of fashion shopping</p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="w-16 h-16 bg-teal-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-teal-600 text-2xl">🤖</span>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">AI Recommendations</h3>
              <p className="text-gray-600">Get personalized product suggestions powered by advanced AI</p>
            </div>
            
            <div className="text-center">
              <div className="w-16 h-16 bg-teal-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-teal-600 text-2xl">📷</span>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Virtual Try-On</h3>
              <p className="text-gray-600">See how clothes look on you before you buy</p>
            </div>
            
            <div className="text-center">
              <div className="w-16 h-16 bg-teal-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-teal-600 text-2xl">🛡️</span>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Secure Shopping</h3>
              <p className="text-gray-600">Shop with confidence with our secure payment system</p>
            </div>
          </div>
        </div>
      </section>

      {/* Simple Footer */}
      <footer className="bg-gray-900 text-white py-8">
        <div className="max-w-7xl mx-auto px-4 text-center">
          <p className="text-gray-400 text-sm">
            © 2024 EshoTry. All rights reserved. Made with ❤️ in London.
          </p>
        </div>
      </footer>
    </div>
  )
}
