"""
Serializers for user-related models.
"""
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import User, UserAddress, UserAvatar, UserStyleQuiz


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'phone_number', 'date_of_birth',
            'gender', 'marketing_notifications', 'data_sharing_consent'
        ]
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match.")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login."""
    
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(
                request=self.context.get('request'),
                username=email,
                password=password
            )
            
            if not user:
                raise serializers.ValidationError('Invalid credentials.')
            
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled.')
            
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('Must include email and password.')


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile information."""
    
    full_name = serializers.ReadOnlyField()
    has_avatar_data = serializers.ReadOnlyField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'full_name',
            'phone_number', 'date_of_birth', 'gender', 'height', 'weight',
            'body_type', 'preferred_colors', 'preferred_styles', 'size_preferences',
            'email_notifications', 'marketing_notifications', 'data_sharing_consent',
            'has_avatar_data', 'created_at', 'last_active'
        ]
        read_only_fields = ['id', 'username', 'email', 'created_at', 'last_active']


class UserAddressSerializer(serializers.ModelSerializer):
    """Serializer for user addresses."""
    
    class Meta:
        model = UserAddress
        fields = [
            'id', 'type', 'is_default', 'full_name', 'company',
            'address_line_1', 'address_line_2', 'city', 'state',
            'postal_code', 'country', 'phone_number', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        user = self.context['request'].user
        
        # If this is set as default, remove default from other addresses
        if validated_data.get('is_default', False):
            UserAddress.objects.filter(user=user, is_default=True).update(is_default=False)
        
        return UserAddress.objects.create(user=user, **validated_data)
    
    def update(self, instance, validated_data):
        # If this is set as default, remove default from other addresses
        if validated_data.get('is_default', False) and not instance.is_default:
            UserAddress.objects.filter(
                user=instance.user, is_default=True
            ).exclude(id=instance.id).update(is_default=False)
        
        return super().update(instance, validated_data)


class UserAvatarSerializer(serializers.ModelSerializer):
    """Serializer for user avatars."""
    
    class Meta:
        model = UserAvatar
        fields = [
            'id', 'name', 'avatar_data', 'measurements', 'is_default',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        user = self.context['request'].user
        
        # If this is set as default, remove default from other avatars
        if validated_data.get('is_default', False):
            UserAvatar.objects.filter(user=user, is_default=True).update(is_default=False)
        
        return UserAvatar.objects.create(user=user, **validated_data)
    
    def update(self, instance, validated_data):
        # If this is set as default, remove default from other avatars
        if validated_data.get('is_default', False) and not instance.is_default:
            UserAvatar.objects.filter(
                user=instance.user, is_default=True
            ).exclude(id=instance.id).update(is_default=False)
        
        return super().update(instance, validated_data)


class UserStyleQuizSerializer(serializers.ModelSerializer):
    """Serializer for user style quiz."""
    
    class Meta:
        model = UserStyleQuiz
        fields = [
            'id', 'preferred_styles', 'color_preferences', 'fit_preferences',
            'occasion_preferences', 'brand_preferences', 'price_range',
            'lifestyle', 'shopping_frequency', 'inspiration_sources',
            'completed_at', 'updated_at'
        ]
        read_only_fields = ['id', 'completed_at', 'updated_at']
    
    def create(self, validated_data):
        user = self.context['request'].user
        
        # Update or create style quiz
        quiz, created = UserStyleQuiz.objects.update_or_create(
            user=user,
            defaults=validated_data
        )
        return quiz


class PasswordChangeSerializer(serializers.Serializer):
    """Serializer for password change."""
    
    old_password = serializers.CharField(style={'input_type': 'password'})
    new_password = serializers.CharField(
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    new_password_confirm = serializers.CharField(style={'input_type': 'password'})
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Old password is incorrect.')
        return value
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("New passwords don't match.")
        return attrs
    
    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
