import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import { api } from '@/lib/api'

// Simple toast replacement for now
const toast = {
  success: (message: string) => console.log('✅', message),
  error: (message: string) => console.error('❌', message),
}

export interface CartItem {
  id: string
  product: {
    id: string
    name: string
    slug: string
    brand_name: string
    current_price: number
    primary_image?: string
    is_in_stock: boolean
  }
  variant?: {
    id: string
    size: string
    color: string
    color_hex?: string
    final_price: number
    is_in_stock: boolean
  }
  quantity: number
  unit_price: number
  total_price: number
  created_at: string
  updated_at: string
}

export interface Cart {
  id: string
  items: CartItem[]
  total_items: number
  subtotal: number
  is_empty: boolean
  created_at: string
  updated_at: string
}

interface CartStore {
  cart: Cart | null
  isLoading: boolean
  
  // Actions
  fetchCart: () => Promise<void>
  addToCart: (productId: string, variantId?: string, quantity?: number) => Promise<void>
  updateQuantity: (itemId: string, quantity: number) => Promise<void>
  removeFromCart: (itemId: string) => Promise<void>
  clearCart: () => Promise<void>
  
  // Local cart for guest users
  localCart: CartItem[]
  addToLocalCart: (item: Omit<CartItem, 'id' | 'created_at' | 'updated_at'>) => void
  updateLocalQuantity: (productId: string, variantId: string | undefined, quantity: number) => void
  removeFromLocalCart: (productId: string, variantId?: string) => void
  clearLocalCart: () => void
  getLocalCartTotal: () => number
  getLocalCartItemCount: () => number
}

export const useCartStore = create<CartStore>()(
  persist(
    (set, get) => ({
      cart: null,
      isLoading: false,
      localCart: [],

      fetchCart: async () => {
        try {
          set({ isLoading: true })
          
          const response = await api.get('/orders/cart/')
          
          set({
            cart: response.data,
            isLoading: false,
          })
        } catch (error: any) {
          set({ isLoading: false })
          
          if (error.response?.status !== 401) {
            toast.error('Failed to fetch cart')
          }
        }
      },

      addToCart: async (productId: string, variantId?: string, quantity = 1) => {
        try {
          const payload = {
            product_id: productId,
            variant_id: variantId,
            quantity,
          }

          const response = await api.post('/orders/cart/items/', payload)
          
          // Refresh cart after adding item
          await get().fetchCart()
          
          toast.success('Item added to cart')
        } catch (error: any) {
          const message = error.response?.data?.detail || 'Failed to add to cart'
          toast.error(message)
          throw error
        }
      },

      updateQuantity: async (itemId: string, quantity: number) => {
        try {
          if (quantity <= 0) {
            await get().removeFromCart(itemId)
            return
          }

          await api.patch(`/orders/cart/items/${itemId}/`, { quantity })
          
          // Update cart locally
          set(state => ({
            cart: state.cart ? {
              ...state.cart,
              items: state.cart.items.map(item =>
                item.id === itemId
                  ? { ...item, quantity, total_price: item.unit_price * quantity }
                  : item
              ),
            } : null,
          }))
          
          // Recalculate totals
          await get().fetchCart()
        } catch (error: any) {
          toast.error('Failed to update quantity')
          throw error
        }
      },

      removeFromCart: async (itemId: string) => {
        try {
          await api.delete(`/orders/cart/items/${itemId}/`)
          
          // Remove item from cart locally
          set(state => ({
            cart: state.cart ? {
              ...state.cart,
              items: state.cart.items.filter(item => item.id !== itemId),
            } : null,
          }))
          
          // Refresh cart to get updated totals
          await get().fetchCart()
          
          toast.success('Item removed from cart')
        } catch (error: any) {
          toast.error('Failed to remove item')
          throw error
        }
      },

      clearCart: async () => {
        try {
          await api.delete('/orders/cart/')
          
          set({ cart: null })
          
          toast.success('Cart cleared')
        } catch (error: any) {
          toast.error('Failed to clear cart')
          throw error
        }
      },

      // Local cart methods for guest users
      addToLocalCart: (item) => {
        set(state => {
          const existingItemIndex = state.localCart.findIndex(
            cartItem => 
              cartItem.product.id === item.product.id &&
              cartItem.variant?.id === item.variant?.id
          )

          if (existingItemIndex >= 0) {
            // Update existing item quantity
            const updatedCart = [...state.localCart]
            updatedCart[existingItemIndex] = {
              ...updatedCart[existingItemIndex],
              quantity: updatedCart[existingItemIndex].quantity + item.quantity,
              total_price: updatedCart[existingItemIndex].unit_price * 
                (updatedCart[existingItemIndex].quantity + item.quantity),
            }
            return { localCart: updatedCart }
          } else {
            // Add new item
            const newItem: CartItem = {
              ...item,
              id: `local-${Date.now()}-${Math.random()}`,
              created_at: new Date().toISOString(),
              updated_at: new Date().toISOString(),
            }
            return { localCart: [...state.localCart, newItem] }
          }
        })
        
        toast.success('Item added to cart')
      },

      updateLocalQuantity: (productId, variantId, quantity) => {
        if (quantity <= 0) {
          get().removeFromLocalCart(productId, variantId)
          return
        }

        set(state => ({
          localCart: state.localCart.map(item =>
            item.product.id === productId && item.variant?.id === variantId
              ? { ...item, quantity, total_price: item.unit_price * quantity }
              : item
          ),
        }))
      },

      removeFromLocalCart: (productId, variantId) => {
        set(state => ({
          localCart: state.localCart.filter(
            item => !(item.product.id === productId && item.variant?.id === variantId)
          ),
        }))
        
        toast.success('Item removed from cart')
      },

      clearLocalCart: () => {
        set({ localCart: [] })
        toast.success('Cart cleared')
      },

      getLocalCartTotal: () => {
        const { localCart } = get()
        return localCart.reduce((total, item) => total + item.total_price, 0)
      },

      getLocalCartItemCount: () => {
        const { localCart } = get()
        return localCart.reduce((count, item) => count + item.quantity, 0)
      },
    }),
    {
      name: 'cart-storage',
      partialize: (state) => ({
        localCart: state.localCart,
      }),
    }
  )
)
