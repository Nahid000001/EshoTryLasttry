"""
Admin configuration for product models.
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Category, Brand, Product, ProductImage, ProductVariant,
    ProductReview, ProductAttribute, ProductAttributeValue, Wishlist
)


class ProductImageInline(admin.TabularInline):
    """Inline admin for product images."""
    model = ProductImage
    extra = 1
    fields = ['image', 'alt_text', 'is_primary', 'sort_order']
    readonly_fields = ['image_preview']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 100px; max-height: 100px;" />',
                obj.image.url
            )
        return "No image"
    image_preview.short_description = "Preview"


class ProductVariantInline(admin.TabularInline):
    """Inline admin for product variants."""
    model = ProductVariant
    extra = 1
    fields = ['size', 'color', 'color_hex', 'sku', 'stock_quantity', 'price_adjustment', 'is_active']


class ProductAttributeValueInline(admin.TabularInline):
    """Inline admin for product attribute values."""
    model = ProductAttributeValue
    extra = 1
    fields = ['attribute', 'value']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin configuration for Category model."""
    
    list_display = ['name', 'parent', 'is_active', 'sort_order', 'product_count', 'created_at']
    list_filter = ['is_active', 'parent', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['sort_order', 'name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'parent')
        }),
        ('Display', {
            'fields': ('image', 'is_active', 'sort_order')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def product_count(self, obj):
        return obj.products.filter(status='active').count()
    product_count.short_description = 'Active Products'


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    """Admin configuration for Brand model."""
    
    list_display = ['name', 'is_active', 'product_count', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'website')
        }),
        ('Display', {
            'fields': ('logo', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def product_count(self, obj):
        return obj.products.filter(status='active').count()
    product_count.short_description = 'Active Products'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin configuration for Product model."""
    
    list_display = [
        'name', 'brand', 'category', 'sku', 'status', 'current_price',
        'stock_quantity', 'is_featured', 'view_count', 'created_at'
    ]
    list_filter = [
        'status', 'is_featured', 'is_virtual_tryon_enabled', 'gender',
        'brand', 'category', 'created_at'
    ]
    search_fields = ['name', 'sku', 'description', 'brand__name']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline, ProductVariantInline, ProductAttributeValueInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'name', 'slug', 'description', 'short_description',
                'category', 'brand', 'gender', 'sku', 'status'
            )
        }),
        ('Pricing', {
            'fields': ('base_price', 'sale_price', 'cost_price')
        }),
        ('Inventory', {
            'fields': ('track_inventory', 'stock_quantity', 'low_stock_threshold')
        }),
        ('Product Details', {
            'fields': ('material', 'care_instructions', 'fit_type', 'style')
        }),
        ('SEO & Metadata', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Features', {
            'fields': (
                'is_featured', 'is_virtual_tryon_enabled', 'is_customizable'
            )
        }),
        ('Analytics', {
            'fields': ('view_count', 'purchase_count'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['view_count', 'purchase_count', 'created_at', 'updated_at']
    
    def current_price(self, obj):
        return f"${obj.current_price}"
    current_price.short_description = 'Current Price'


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    """Admin configuration for ProductImage model."""
    
    list_display = ['product', 'is_primary', 'sort_order', 'image_preview', 'created_at']
    list_filter = ['is_primary', 'created_at']
    search_fields = ['product__name', 'alt_text']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 100px; max-height: 100px;" />',
                obj.image.url
            )
        return "No image"
    image_preview.short_description = "Preview"


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    """Admin configuration for ProductVariant model."""
    
    list_display = [
        'product', 'size', 'color', 'sku', 'stock_quantity',
        'final_price', 'is_active', 'created_at'
    ]
    list_filter = ['is_active', 'size', 'color', 'created_at']
    search_fields = ['product__name', 'sku', 'color']
    
    fieldsets = (
        ('Product Information', {
            'fields': ('product',)
        }),
        ('Variant Details', {
            'fields': ('size', 'color', 'color_hex', 'sku', 'image')
        }),
        ('Inventory & Pricing', {
            'fields': ('stock_quantity', 'price_adjustment')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def final_price(self, obj):
        return f"${obj.final_price}"
    final_price.short_description = 'Final Price'


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    """Admin configuration for ProductReview model."""
    
    list_display = [
        'product', 'user', 'rating', 'title', 'is_verified_purchase',
        'is_approved', 'helpful_count', 'created_at'
    ]
    list_filter = [
        'rating', 'is_verified_purchase', 'is_approved', 'fit_feedback', 'created_at'
    ]
    search_fields = ['product__name', 'user__email', 'title', 'content']
    readonly_fields = ['helpful_count', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Review Information', {
            'fields': ('product', 'user', 'rating', 'title', 'content')
        }),
        ('Purchase Information', {
            'fields': ('is_verified_purchase', 'size_purchased', 'fit_feedback')
        }),
        ('Moderation', {
            'fields': ('is_approved', 'helpful_count')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    """Admin configuration for ProductAttribute model."""
    
    list_display = ['name', 'data_type', 'is_required', 'is_filterable', 'created_at']
    list_filter = ['data_type', 'is_required', 'is_filterable', 'created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'data_type', 'choices')
        }),
        ('Settings', {
            'fields': ('is_required', 'is_filterable')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at']


@admin.register(ProductAttributeValue)
class ProductAttributeValueAdmin(admin.ModelAdmin):
    """Admin configuration for ProductAttributeValue model."""
    
    list_display = ['product', 'attribute', 'value']
    list_filter = ['attribute']
    search_fields = ['product__name', 'attribute__name', 'value']


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    """Admin configuration for Wishlist model."""
    
    list_display = ['user', 'product', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__email', 'product__name']
    readonly_fields = ['created_at']
