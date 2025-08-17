"""
Admin configuration for user models.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UserAddress, UserAvatar, UserStyleQuiz


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin configuration for User model."""
    
    list_display = [
        'email', 'username', 'first_name', 'last_name', 
        'is_staff', 'is_active', 'created_at'
    ]
    list_filter = [
        'is_staff', 'is_active', 'gender', 'body_type', 
        'created_at', 'last_active'
    ]
    search_fields = ['email', 'username', 'first_name', 'last_name']
    ordering = ['-created_at']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Personal Information', {
            'fields': (
                'phone_number', 'date_of_birth', 'gender',
                'height', 'weight', 'body_type'
            )
        }),
        ('Preferences', {
            'fields': (
                'preferred_colors', 'preferred_styles', 'size_preferences'
            )
        }),
        ('Privacy Settings', {
            'fields': (
                'email_notifications', 'marketing_notifications', 
                'data_sharing_consent'
            )
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'last_active'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at', 'last_active']


@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    """Admin configuration for UserAddress model."""
    
    list_display = [
        'user', 'type', 'full_name', 'city', 'state', 
        'country', 'is_default', 'created_at'
    ]
    list_filter = ['type', 'is_default', 'country', 'created_at']
    search_fields = [
        'user__email', 'full_name', 'city', 'state', 'postal_code'
    ]
    ordering = ['-created_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'type', 'is_default')
        }),
        ('Contact Information', {
            'fields': ('full_name', 'company', 'phone_number')
        }),
        ('Address Information', {
            'fields': (
                'address_line_1', 'address_line_2', 'city', 
                'state', 'postal_code', 'country'
            )
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']


@admin.register(UserAvatar)
class UserAvatarAdmin(admin.ModelAdmin):
    """Admin configuration for UserAvatar model."""
    
    list_display = [
        'user', 'name', 'is_default', 'created_at'
    ]
    list_filter = ['is_default', 'created_at']
    search_fields = ['user__email', 'name']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'name', 'is_default')
        }),
        ('Avatar Data', {
            'fields': ('avatar_data', 'measurements')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']


@admin.register(UserStyleQuiz)
class UserStyleQuizAdmin(admin.ModelAdmin):
    """Admin configuration for UserStyleQuiz model."""
    
    list_display = [
        'user', 'lifestyle', 'shopping_frequency', 'completed_at'
    ]
    list_filter = ['lifestyle', 'shopping_frequency', 'completed_at']
    search_fields = ['user__email']
    ordering = ['-completed_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Style Preferences', {
            'fields': (
                'preferred_styles', 'color_preferences', 'fit_preferences',
                'occasion_preferences', 'brand_preferences', 'price_range'
            )
        }),
        ('Lifestyle Information', {
            'fields': (
                'lifestyle', 'shopping_frequency', 'inspiration_sources'
            )
        }),
        ('Timestamps', {
            'fields': ('completed_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['completed_at', 'updated_at']
