"""
Serializers for product-related models.
"""
from rest_framework import serializers
from django.db.models import Avg, Count
from .models import (
    Category, Brand, Product, ProductImage, ProductVariant,
    ProductReview, ProductAttribute, ProductAttributeValue, Wishlist
)


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for product categories."""
    
    children = serializers.SerializerMethodField()
    product_count = serializers.SerializerMethodField()
    full_path = serializers.ReadOnlyField()
    
    class Meta:
        model = Category
        fields = [
            'id', 'name', 'slug', 'description', 'parent', 'image',
            'is_active', 'sort_order', 'full_path', 'children', 
            'product_count', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_children(self, obj):
        if obj.children.exists():
            return CategorySerializer(
                obj.children.filter(is_active=True), 
                many=True, 
                context=self.context
            ).data
        return []
    
    def get_product_count(self, obj):
        return obj.products.filter(status='active').count()


class BrandSerializer(serializers.ModelSerializer):
    """Serializer for product brands."""
    
    product_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Brand
        fields = [
            'id', 'name', 'slug', 'description', 'logo', 'website',
            'is_active', 'product_count', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_product_count(self, obj):
        return obj.products.filter(status='active').count()


class ProductImageSerializer(serializers.ModelSerializer):
    """Serializer for product images."""
    
    class Meta:
        model = ProductImage
        fields = [
            'id', 'image', 'alt_text', 'is_primary', 'sort_order', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class ProductVariantSerializer(serializers.ModelSerializer):
    """Serializer for product variants."""
    
    final_price = serializers.ReadOnlyField()
    is_in_stock = serializers.ReadOnlyField()
    
    class Meta:
        model = ProductVariant
        fields = [
            'id', 'size', 'color', 'color_hex', 'sku', 'stock_quantity',
            'price_adjustment', 'final_price', 'image', 'is_active',
            'is_in_stock', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class ProductAttributeValueSerializer(serializers.ModelSerializer):
    """Serializer for product attribute values."""
    
    attribute_name = serializers.CharField(source='attribute.name', read_only=True)
    attribute_slug = serializers.CharField(source='attribute.slug', read_only=True)
    
    class Meta:
        model = ProductAttributeValue
        fields = ['attribute_name', 'attribute_slug', 'value']


class ProductReviewSerializer(serializers.ModelSerializer):
    """Serializer for product reviews."""
    
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    user_initial = serializers.SerializerMethodField()
    
    class Meta:
        model = ProductReview
        fields = [
            'id', 'rating', 'title', 'content', 'user_name', 'user_initial',
            'is_verified_purchase', 'helpful_count', 'size_purchased',
            'fit_feedback', 'created_at'
        ]
        read_only_fields = ['id', 'user_name', 'user_initial', 'created_at']
    
    def get_user_initial(self, obj):
        if obj.user.first_name:
            return obj.user.first_name[0].upper()
        return obj.user.email[0].upper()
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class ProductListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for product lists."""
    
    category_name = serializers.CharField(source='category.name', read_only=True)
    brand_name = serializers.CharField(source='brand.name', read_only=True)
    primary_image = serializers.SerializerMethodField()
    current_price = serializers.ReadOnlyField()
    is_on_sale = serializers.ReadOnlyField()
    discount_percentage = serializers.ReadOnlyField()
    is_in_stock = serializers.ReadOnlyField()
    average_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    is_wishlisted = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'short_description', 'category_name',
            'brand_name', 'gender', 'sku', 'base_price', 'sale_price',
            'current_price', 'is_on_sale', 'discount_percentage',
            'is_in_stock', 'is_featured', 'is_virtual_tryon_enabled',
            'primary_image', 'average_rating', 'review_count',
            'is_wishlisted', 'view_count'
        ]
    
    def get_primary_image(self, obj):
        primary_image = obj.images.filter(is_primary=True).first()
        if primary_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(primary_image.image.url)
            return primary_image.image.url
        return None
    
    def get_average_rating(self, obj):
        avg_rating = obj.reviews.filter(is_approved=True).aggregate(
            avg_rating=Avg('rating')
        )['avg_rating']
        return round(avg_rating, 1) if avg_rating else 0
    
    def get_review_count(self, obj):
        return obj.reviews.filter(is_approved=True).count()
    
    def get_is_wishlisted(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Wishlist.objects.filter(user=request.user, product=obj).exists()
        return False


class ProductDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for product detail view."""
    
    category = CategorySerializer(read_only=True)
    brand = BrandSerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    attribute_values = ProductAttributeValueSerializer(many=True, read_only=True)
    reviews = serializers.SerializerMethodField()
    
    current_price = serializers.ReadOnlyField()
    is_on_sale = serializers.ReadOnlyField()
    discount_percentage = serializers.ReadOnlyField()
    is_in_stock = serializers.ReadOnlyField()
    is_low_stock = serializers.ReadOnlyField()
    
    average_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    rating_distribution = serializers.SerializerMethodField()
    is_wishlisted = serializers.SerializerMethodField()
    
    # Size and color options
    available_sizes = serializers.SerializerMethodField()
    available_colors = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'short_description',
            'category', 'brand', 'gender', 'sku', 'status',
            'base_price', 'sale_price', 'current_price', 'is_on_sale',
            'discount_percentage', 'stock_quantity', 'is_in_stock',
            'is_low_stock', 'material', 'care_instructions', 'fit_type',
            'style', 'is_featured', 'is_virtual_tryon_enabled',
            'is_customizable', 'images', 'variants', 'attribute_values',
            'reviews', 'average_rating', 'review_count', 'rating_distribution',
            'is_wishlisted', 'available_sizes', 'available_colors',
            'view_count', 'purchase_count', 'created_at'
        ]
        read_only_fields = ['id', 'view_count', 'purchase_count', 'created_at']
    
    def get_reviews(self, obj):
        reviews = obj.reviews.filter(is_approved=True)[:5]  # Latest 5 reviews
        return ProductReviewSerializer(reviews, many=True, context=self.context).data
    
    def get_average_rating(self, obj):
        avg_rating = obj.reviews.filter(is_approved=True).aggregate(
            avg_rating=Avg('rating')
        )['avg_rating']
        return round(avg_rating, 1) if avg_rating else 0
    
    def get_review_count(self, obj):
        return obj.reviews.filter(is_approved=True).count()
    
    def get_rating_distribution(self, obj):
        distribution = {}
        for i in range(1, 6):
            count = obj.reviews.filter(is_approved=True, rating=i).count()
            distribution[str(i)] = count
        return distribution
    
    def get_is_wishlisted(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Wishlist.objects.filter(user=request.user, product=obj).exists()
        return False
    
    def get_available_sizes(self, obj):
        sizes = obj.variants.filter(is_active=True).values_list('size', flat=True).distinct()
        return list(sizes)
    
    def get_available_colors(self, obj):
        colors = obj.variants.filter(is_active=True).values('color', 'color_hex').distinct()
        return list(colors)


class ProductAttributeSerializer(serializers.ModelSerializer):
    """Serializer for product attributes."""
    
    class Meta:
        model = ProductAttribute
        fields = [
            'id', 'name', 'slug', 'data_type', 'choices',
            'is_required', 'is_filterable', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class WishlistSerializer(serializers.ModelSerializer):
    """Serializer for wishlist items."""
    
    product = ProductListSerializer(read_only=True)
    product_id = serializers.UUIDField(write_only=True)
    
    class Meta:
        model = Wishlist
        fields = ['id', 'product', 'product_id', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
    def validate_product_id(self, value):
        try:
            product = Product.objects.get(id=value, status='active')
            return product
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product not found or inactive.")


class ProductSearchSerializer(serializers.Serializer):
    """Serializer for product search parameters."""
    
    q = serializers.CharField(required=False, allow_blank=True)
    category = serializers.UUIDField(required=False)
    brand = serializers.UUIDField(required=False)
    gender = serializers.ChoiceField(choices=Product.GENDER_CHOICES, required=False)
    min_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    max_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    size = serializers.CharField(required=False)
    color = serializers.CharField(required=False)
    in_stock = serializers.BooleanField(required=False)
    on_sale = serializers.BooleanField(required=False)
    rating = serializers.IntegerField(min_value=1, max_value=5, required=False)
    sort_by = serializers.ChoiceField(
        choices=[
            'name', '-name', 'price', '-price', 'created_at', '-created_at',
            'rating', '-rating', 'popularity', '-popularity'
        ],
        required=False,
        default='-created_at'
    )
