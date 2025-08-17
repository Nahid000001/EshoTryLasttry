"""
URL patterns for user authentication and profile management.
"""
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

urlpatterns = [
    # Authentication
    path('register/', views.UserRegistrationView.as_view(), name='user-register'),
    path('login/', views.UserLoginView.as_view(), name='user-login'),
    path('logout/', views.logout_view, name='user-logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    
    # Profile management
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('password/change/', views.PasswordChangeView.as_view(), name='password-change'),
    path('dashboard/', views.user_dashboard_view, name='user-dashboard'),
    
    # Addresses
    path('addresses/', views.UserAddressListCreateView.as_view(), name='user-addresses'),
    path('addresses/<uuid:pk>/', views.UserAddressDetailView.as_view(), name='user-address-detail'),
    
    # Avatars
    path('avatars/', views.UserAvatarListCreateView.as_view(), name='user-avatars'),
    path('avatars/<uuid:pk>/', views.UserAvatarDetailView.as_view(), name='user-avatar-detail'),
    
    # Style quiz
    path('style-quiz/', views.UserStyleQuizView.as_view(), name='user-style-quiz'),
]
