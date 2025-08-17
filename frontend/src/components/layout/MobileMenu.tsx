import React from 'react';
import { Link } from 'react-router-dom';
import { XMarkIcon } from '@heroicons/react/24/outline';

interface MobileMenuProps {
  isOpen: boolean;
  onClose: () => void;
}

export const MobileMenu: React.FC<MobileMenuProps> = ({ isOpen, onClose }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 lg:hidden">
      {/* Backdrop */}
      <div className="fixed inset-0 bg-black bg-opacity-50" onClick={onClose} />
      
      {/* Menu */}
      <div className="fixed top-0 right-0 w-64 h-full bg-white shadow-lg transform transition-transform">
        <div className="flex items-center justify-between p-4 border-b">
          <h2 className="text-lg font-semibold">Menu</h2>
          <button
            onClick={onClose}
            className="p-2 text-gray-400 hover:text-gray-600"
          >
            <XMarkIcon className="w-6 h-6" />
          </button>
        </div>
        
        <nav className="p-4">
          <ul className="space-y-4">
            <li>
              <Link 
                to="/" 
                className="block py-2 text-gray-700 hover:text-indigo-600"
                onClick={onClose}
              >
                Home
              </Link>
            </li>
            <li>
              <Link 
                to="/products" 
                className="block py-2 text-gray-700 hover:text-indigo-600"
                onClick={onClose}
              >
                Products
              </Link>
            </li>
            <li>
              <Link 
                to="/categories" 
                className="block py-2 text-gray-700 hover:text-indigo-600"
                onClick={onClose}
              >
                Categories
              </Link>
            </li>
            <li>
              <Link 
                to="/try-on" 
                className="block py-2 text-gray-700 hover:text-indigo-600"
                onClick={onClose}
              >
                Virtual Try-On
              </Link>
            </li>
          </ul>
        </nav>
      </div>
    </div>
  );
};

export default MobileMenu;
