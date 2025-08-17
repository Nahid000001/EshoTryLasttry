"""
Views for user authentication and profile management.
"""
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login
from django.db import transaction

from .models import User, UserAddress, UserAvatar, UserStyleQuiz
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer,
    UserAddressSerializer, UserAvatarSerializer, UserStyleQuizSerializer,
    PasswordChangeSerializer
)


class UserRegistrationView(APIView):
    """User registration endpoint."""
    
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                user = serializer.save()
                
                # Generate JWT tokens
                refresh = RefreshToken.for_user(user)
                
                return Response({
                    'user': UserProfileSerializer(user).data,
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }
                }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    """User login endpoint."""
    
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserLoginSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            
            # Update last active timestamp
            user.save(update_fields=['last_active'])
            
            return Response({
                'user': UserProfileSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """User profile endpoint."""
    
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class UserAddressListCreateView(generics.ListCreateAPIView):
    """User addresses list and create endpoint."""
    
    serializer_class = UserAddressSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)


class UserAddressDetailView(generics.RetrieveUpdateDestroyAPIView):
    """User address detail endpoint."""
    
    serializer_class = UserAddressSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)


class UserAvatarListCreateView(generics.ListCreateAPIView):
    """User avatars list and create endpoint."""
    
    serializer_class = UserAvatarSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return UserAvatar.objects.filter(user=self.request.user)


class UserAvatarDetailView(generics.RetrieveUpdateDestroyAPIView):
    """User avatar detail endpoint."""
    
    serializer_class = UserAvatarSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return UserAvatar.objects.filter(user=self.request.user)


class UserStyleQuizView(generics.RetrieveUpdateAPIView):
    """User style quiz endpoint."""
    
    serializer_class = UserStyleQuizSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        try:
            return UserStyleQuiz.objects.get(user=self.request.user)
        except UserStyleQuiz.DoesNotExist:
            return None
    
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance is None:
            return Response({'detail': 'Style quiz not completed yet.'}, 
                          status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordChangeView(APIView):
    """Password change endpoint."""
    
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = PasswordChangeSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'Password changed successfully.'}, 
                          status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    """Logout endpoint that blacklists the refresh token."""
    
    try:
        refresh_token = request.data.get('refresh_token')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        
        return Response({'detail': 'Successfully logged out.'}, 
                       status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'detail': 'Error during logout.'}, 
                       status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_dashboard_view(request):
    """User dashboard with summary information."""
    
    user = request.user
    
    # Get user statistics
    from apps.orders.models import Order
    from apps.virtual_tryon.models import TryOnSession
    
    total_orders = Order.objects.filter(user=user).count()
    total_tryon_sessions = TryOnSession.objects.filter(user=user).count()
    
    return Response({
        'user': UserProfileSerializer(user).data,
        'statistics': {
            'total_orders': total_orders,
            'total_tryon_sessions': total_tryon_sessions,
            'has_completed_style_quiz': hasattr(user, 'style_quiz'),
            'avatar_count': user.avatars.count(),
            'address_count': user.addresses.count(),
        }
    }, status=status.HTTP_200_OK)
