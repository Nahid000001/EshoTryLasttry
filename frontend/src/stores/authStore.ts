import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import { api } from '@/lib/api'

// Simple toast replacement for now
const toast = {
  success: (message: string) => console.log('✅', message),
  error: (message: string) => console.error('❌', message),
  loading: (message: string) => console.log('⏳', message),
}

export interface User {
  id: string
  username: string
  email: string
  first_name: string
  last_name: string
  full_name: string
  phone_number?: string
  date_of_birth?: string
  gender?: 'M' | 'F' | 'O' | 'P'
  height?: number
  weight?: number
  body_type?: 'slim' | 'athletic' | 'regular' | 'plus'
  preferred_colors: string[]
  preferred_styles: string[]
  size_preferences: Record<string, any>
  email_notifications: boolean
  marketing_notifications: boolean
  data_sharing_consent: boolean
  has_avatar_data: boolean
  created_at: string
  last_active: string
}

export interface AuthTokens {
  access: string
  refresh: string
}

interface AuthStore {
  user: User | null
  tokens: AuthTokens | null
  isAuthenticated: boolean
  isLoading: boolean
  
  // Actions
  login: (email: string, password: string) => Promise<void>
  register: (userData: RegisterData) => Promise<void>
  logout: () => void
  refreshToken: () => Promise<void>
  updateProfile: (userData: Partial<User>) => Promise<void>
  initializeAuth: () => void
}

export interface RegisterData {
  username: string
  email: string
  password: string
  password_confirm: string
  first_name: string
  last_name: string
  phone_number?: string
  date_of_birth?: string
  gender?: string
  marketing_notifications?: boolean
  data_sharing_consent?: boolean
}

export const useAuthStore = create<AuthStore>()(
  persist(
    (set, get) => ({
      user: null,
      tokens: null,
      isAuthenticated: false,
      isLoading: false,

      login: async (email: string, password: string) => {
        try {
          set({ isLoading: true })
          
          const response = await api.post('/auth/login/', {
            email,
            password,
          })

          const { user, tokens } = response.data
          
          // Set auth header for future requests
          api.defaults.headers.common['Authorization'] = `Bearer ${tokens.access}`
          
          set({
            user,
            tokens,
            isAuthenticated: true,
            isLoading: false,
          })

          toast.success(`Welcome back, ${user.first_name}!`)
        } catch (error: any) {
          set({ isLoading: false })
          const message = error.response?.data?.detail || 'Login failed'
          toast.error(message)
          throw error
        }
      },

      register: async (userData: RegisterData) => {
        try {
          set({ isLoading: true })
          
          const response = await api.post('/auth/register/', userData)
          const { user, tokens } = response.data
          
          // Set auth header for future requests
          api.defaults.headers.common['Authorization'] = `Bearer ${tokens.access}`
          
          set({
            user,
            tokens,
            isAuthenticated: true,
            isLoading: false,
          })

          toast.success(`Welcome to EshoTry, ${user.first_name}!`)
        } catch (error: any) {
          set({ isLoading: false })
          const message = error.response?.data?.detail || 'Registration failed'
          toast.error(message)
          throw error
        }
      },

      logout: () => {
        const { tokens } = get()
        
        // Send logout request to blacklist tokens
        if (tokens?.refresh) {
          api.post('/auth/logout/', { refresh_token: tokens.refresh })
            .catch(() => {
              // Ignore errors on logout
            })
        }
        
        // Clear auth header
        delete api.defaults.headers.common['Authorization']
        
        set({
          user: null,
          tokens: null,
          isAuthenticated: false,
        })

        toast.success('Logged out successfully')
      },

      refreshToken: async () => {
        try {
          const { tokens } = get()
          
          if (!tokens?.refresh) {
            throw new Error('No refresh token')
          }

          const response = await api.post('/auth/token/refresh/', {
            refresh: tokens.refresh,
          })

          const newTokens = {
            access: response.data.access,
            refresh: tokens.refresh,
          }

          // Update auth header
          api.defaults.headers.common['Authorization'] = `Bearer ${newTokens.access}`

          set({ tokens: newTokens })
        } catch (error) {
          // If refresh fails, logout user
          get().logout()
          throw error
        }
      },

      updateProfile: async (userData: Partial<User>) => {
        try {
          const response = await api.patch('/auth/profile/', userData)
          const updatedUser = response.data

          set(state => ({
            user: state.user ? { ...state.user, ...updatedUser } : null
          }))

          toast.success('Profile updated successfully')
        } catch (error: any) {
          const message = error.response?.data?.detail || 'Profile update failed'
          toast.error(message)
          throw error
        }
      },

      initializeAuth: () => {
        const { tokens } = get()
        
        if (tokens?.access) {
          // Set auth header if we have tokens
          api.defaults.headers.common['Authorization'] = `Bearer ${tokens.access}`
          
          // Verify token is still valid
          api.get('/auth/profile/')
            .then(response => {
              set({
                user: response.data,
                isAuthenticated: true,
              })
            })
            .catch(() => {
              // Token is invalid, try to refresh
              get().refreshToken().catch(() => {
                // Refresh failed, logout
                get().logout()
              })
            })
        }
      },
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({
        user: state.user,
        tokens: state.tokens,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
)
