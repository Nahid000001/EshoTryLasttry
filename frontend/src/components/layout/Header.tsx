import { useState } from 'react'
import { Link } from 'react-router-dom'

export default function Header() {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false)

  return (
    <header className="bg-gray-900 text-white">
      {/* Top announcement bar */}
      <div className="bg-gray-800 py-2">
        <div className="max-w-7xl mx-auto px-4 flex items-center justify-between text-sm">
          <div className="flex items-center space-x-4">
            <span className="bg-teal-500 text-white px-2 py-1 rounded text-xs font-medium">AI</span>
            <span>Free delivery across London • Virtual Try-On Available</span>
          </div>
          <div className="flex items-center space-x-4">
            <button className="hover:text-teal-400">?</button>
            <button className="hover:text-teal-400">Share</button>
          </div>
        </div>
      </div>

      {/* Main header */}
      <div className="max-w-7xl mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-teal-500 rounded-full flex items-center justify-center">
              <span className="text-white font-bold text-lg">E</span>
            </div>
            <div>
              <h1 className="text-xl font-bold">EshoTry</h1>
              <p className="text-xs text-gray-400">Try Before You Buy – Anywhere in London</p>
            </div>
          </Link>

          {/* Search bar */}
          <div className="flex-1 max-w-2xl mx-8">
            <div className="relative">
              <input
                type="text"
                placeholder="Search for styles, brands, or occasions..."
                className="w-full px-4 py-3 bg-white text-gray-900 rounded-lg focus:outline-none focus:ring-2 focus:ring-teal-500"
              />
              <button className="absolute right-2 top-1/2 transform -translate-y-1/2 bg-teal-500 text-white p-2 rounded-md hover:bg-teal-600">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </button>
            </div>
          </div>

          {/* Navigation */}
          <div className="flex items-center space-x-6">
            <Link to="/style-quiz" className="text-sm hover:text-teal-400">Style Quiz</Link>
            <Link to="/try-on" className="relative">
              <button className="bg-teal-500 text-white px-4 py-2 rounded-lg hover:bg-teal-600 text-sm">
                Try-On Now
                <span className="absolute -top-2 -right-2 bg-red-500 text-white text-xs w-5 h-5 rounded-full flex items-center justify-center">3</span>
              </button>
            </Link>
            <Link to="/cart" className="relative p-2 hover:text-teal-400">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 3h2l.4 2M7 13h10l4-8H5.4m0 0L7 13m0 0l-2.5 2.5M7 13l2.5 2.5m6-2.5a2.5 2.5 0 100 5 2.5 2.5 0 000-5zm0 0V9a2.5 2.5 0 00-5 0v2.5" />
              </svg>
            </Link>
            <Link to="/login" className="p-2 hover:text-teal-400">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
            </Link>
          </div>
        </div>

        {/* Category navigation */}
        <nav className="mt-4 flex items-center justify-center space-x-8">
          <Link to="/products?category=mens" className="text-sm hover:text-teal-400">Men's</Link>
          <Link to="/products?category=womens" className="text-sm hover:text-teal-400">Women's</Link>
          <Link to="/products?category=streetwear" className="text-sm hover:text-teal-400">Streetwear</Link>
          <Link to="/products?category=occasion" className="text-sm hover:text-teal-400">Occasion</Link>
          <Link to="/products?category=accessories" className="text-sm hover:text-teal-400">Accessories</Link>
          <Link to="/products?category=sale" className="text-sm text-red-400 hover:text-red-300">Sale</Link>
        </nav>
      </div>
    </header>
  )
}