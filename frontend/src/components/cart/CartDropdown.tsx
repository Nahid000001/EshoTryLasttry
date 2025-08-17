import React from 'react';
import { Link } from 'react-router-dom';
import { useCartStore } from '@/stores/cartStore';

interface CartDropdownProps {
  isOpen: boolean;
  onClose: () => void;
}

export const CartDropdown: React.FC<CartDropdownProps> = ({ isOpen, onClose }) => {
  const { items, total, removeItem } = useCartStore();

  if (!isOpen) return null;

  return (
    <div className="absolute right-0 mt-2 w-80 bg-white rounded-md shadow-lg ring-1 ring-black ring-opacity-5 z-50">
      <div className="p-4">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Shopping Cart</h3>
        
        {items.length === 0 ? (
          <p className="text-gray-500 text-center py-4">Your cart is empty</p>
        ) : (
          <>
            <div className="max-h-60 overflow-y-auto">
              {items.map((item) => (
                <div key={item.id} className="flex items-center py-2 border-b">
                  <div className="w-12 h-12 bg-gray-200 rounded flex-shrink-0">
                    <div className="w-full h-full bg-gradient-to-br from-indigo-400 to-purple-500 rounded flex items-center justify-center">
                      <span className="text-white text-sm font-bold">
                        {item.name.charAt(0)}
                      </span>
                    </div>
                  </div>
                  <div className="ml-3 flex-1">
                    <p className="text-sm font-medium text-gray-900">{item.name}</p>
                    <p className="text-sm text-gray-500">Qty: {item.quantity}</p>
                  </div>
                  <div className="ml-3">
                    <p className="text-sm font-medium text-gray-900">
                      ${(item.price * item.quantity).toFixed(2)}
                    </p>
                    <button
                      onClick={() => removeItem(item.id)}
                      className="text-xs text-red-600 hover:text-red-800"
                    >
                      Remove
                    </button>
                  </div>
                </div>
              ))}
            </div>
            
            <div className="mt-4 pt-4 border-t">
              <div className="flex justify-between items-center mb-4">
                <span className="text-lg font-medium text-gray-900">Total:</span>
                <span className="text-lg font-bold text-gray-900">${total.toFixed(2)}</span>
              </div>
              
              <div className="space-y-2">
                <Link
                  to="/cart"
                  className="block w-full bg-gray-100 text-gray-900 text-center py-2 px-4 rounded-md hover:bg-gray-200 transition-colors"
                  onClick={onClose}
                >
                  View Cart
                </Link>
                <Link
                  to="/checkout"
                  className="block w-full bg-indigo-600 text-white text-center py-2 px-4 rounded-md hover:bg-indigo-700 transition-colors"
                  onClick={onClose}
                >
                  Checkout
                </Link>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default CartDropdown;
