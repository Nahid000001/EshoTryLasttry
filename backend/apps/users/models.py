"""
User models for EshoTry platform.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid


class User(AbstractUser):
    """Extended user model with additional fields for EshoTry platform."""
    
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('P', 'Prefer not to say'),
    ]
    
    BODY_TYPE_CHOICES = [
        ('slim', 'Slim'),
        ('athletic', 'Athletic'),
        ('regular', 'Regular'),
        ('plus', 'Plus Size'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    
    # Avatar and measurements
    height = models.IntegerField(
        validators=[MinValueValidator(100), MaxValueValidator(250)],
        blank=True, null=True,
        help_text="Height in centimeters"
    )
    weight = models.IntegerField(
        validators=[MinValueValidator(30), MaxValueValidator(300)],
        blank=True, null=True,
        help_text="Weight in kilograms"
    )
    body_type = models.CharField(max_length=20, choices=BODY_TYPE_CHOICES, blank=True, null=True)
    
    # Preferences
    preferred_brands = models.ManyToManyField('products.Brand', blank=True)
    preferred_colors = models.JSONField(default=list, blank=True)
    preferred_styles = models.JSONField(default=list, blank=True)
    size_preferences = models.JSONField(default=dict, blank=True)
    
    # Privacy settings
    email_notifications = models.BooleanField(default=True)
    marketing_notifications = models.BooleanField(default=False)
    data_sharing_consent = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_active = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['created_at']),
            models.Index(fields=['last_active']),
        ]
    
    def __str__(self):
        return f"{self.email} ({self.username})"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    
    @property
    def has_avatar_data(self):
        return bool(self.height and self.weight and self.body_type)


class UserAddress(models.Model):
    """User shipping addresses."""
    
    ADDRESS_TYPE_CHOICES = [
        ('home', 'Home'),
        ('work', 'Work'),
        ('other', 'Other'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    type = models.CharField(max_length=10, choices=ADDRESS_TYPE_CHOICES, default='home')
    is_default = models.BooleanField(default=False)
    
    # Address fields
    full_name = models.CharField(max_length=255)
    company = models.CharField(max_length=255, blank=True)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_addresses'
        verbose_name = 'User Address'
        verbose_name_plural = 'User Addresses'
        indexes = [
            models.Index(fields=['user', 'is_default']),
            models.Index(fields=['user', 'type']),
        ]
    
    def __str__(self):
        return f"{self.full_name} - {self.city}, {self.state}"


class UserAvatar(models.Model):
    """Stored user avatars for virtual try-on."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='avatars')
    name = models.CharField(max_length=100)
    avatar_data = models.JSONField()  # 3D avatar parameters
    measurements = models.JSONField()  # Detailed body measurements
    is_default = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_avatars'
        verbose_name = 'User Avatar'
        verbose_name_plural = 'User Avatars'
        indexes = [
            models.Index(fields=['user', 'is_default']),
        ]
    
    def __str__(self):
        return f"{self.user.email} - {self.name}"


class UserStyleQuiz(models.Model):
    """User style preferences from style quiz."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='style_quiz')
    
    # Style preferences
    preferred_styles = models.JSONField(default=list)
    color_preferences = models.JSONField(default=list)
    fit_preferences = models.JSONField(default=list)
    occasion_preferences = models.JSONField(default=list)
    brand_preferences = models.JSONField(default=list)
    price_range = models.JSONField(default=dict)
    
    # Lifestyle questions
    lifestyle = models.CharField(max_length=50, blank=True)
    shopping_frequency = models.CharField(max_length=50, blank=True)
    inspiration_sources = models.JSONField(default=list)
    
    completed_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_style_quiz'
        verbose_name = 'User Style Quiz'
        verbose_name_plural = 'User Style Quizzes'
    
    def __str__(self):
        return f"{self.user.email} - Style Quiz"
