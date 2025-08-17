import React from 'react';
import { Link } from 'react-router-dom';
import { useAuthStore } from '@/stores/authStore';

interface UserDropdownProps {
  isOpen: boolean;
  onClose: () => void;
}

export const UserDropdown: React.FC<UserDropdownProps> = ({ isOpen, onClose }) => {
  const { user, logout } = useAuthStore();

  if (!isOpen) return null;

  const handleLogout = () => {
    logout();
    onClose();
  };

  return (
    <div className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg ring-1 ring-black ring-opacity-5 z-50">
      <div className="py-1">
        {user ? (
          <>
            <div className="px-4 py-2 border-b">
              <p className="text-sm font-medium text-gray-900">{user.email}</p>
              <p className="text-sm text-gray-500">
                {user.first_name} {user.last_name}
              </p>
            </div>
            
            <Link
              to="/profile"
              className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
              onClick={onClose}
            >
              Profile
            </Link>
            
            <Link
              to="/profile/orders"
              className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
              onClick={onClose}
            >
              Orders
            </Link>
            
            <Link
              to="/wishlist"
              className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
              onClick={onClose}
            >
              Wishlist
            </Link>
            
            <div className="border-t">
              <button
                onClick={handleLogout}
                className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
              >
                Sign out
              </button>
            </div>
          </>
        ) : (
          <>
            <Link
              to="/login"
              className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
              onClick={onClose}
            >
              Sign in
            </Link>
            
            <Link
              to="/register"
              className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
              onClick={onClose}
            >
              Sign up
            </Link>
          </>
        )}
      </div>
    </div>
  );
};

export default UserDropdown;
