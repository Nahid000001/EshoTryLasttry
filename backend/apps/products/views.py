"""
Views for product management and catalog.
"""
from rest_framework import generics, status, permissions, filters, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db import models
from django.db.models import Q, Avg, Count, F
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from .models import (
    Category, Brand, Product, ProductReview, 
    ProductAttribute, Wishlist, ProductVariant
)
from .serializers import (
    CategorySerializer, BrandSerializer, ProductListSerializer,
    ProductDetailSerializer, ProductReviewSerializer, 
    ProductAttributeSerializer, WishlistSerializer,
    ProductSearchSerializer, ProductVariantSerializer
)
from .filters import ProductFilter


class CategoryListView(generics.ListAPIView):
    """List all active categories."""
    
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        return Category.objects.filter(
            is_active=True, 
            parent=None
        ).prefetch_related('children')


class CategoryDetailView(generics.RetrieveAPIView):
    """Get category details with products."""
    
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'
    
    def get_queryset(self):
        return Category.objects.filter(is_active=True)


class BrandListView(generics.ListAPIView):
    """List all active brands."""
    
    serializer_class = BrandSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    
    def get_queryset(self):
        return Brand.objects.filter(is_active=True)


class BrandDetailView(generics.RetrieveAPIView):
    """Get brand details."""
    
    serializer_class = BrandSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'
    
    def get_queryset(self):
        return Brand.objects.filter(is_active=True)


class ProductListView(generics.ListAPIView):
    """List products with filtering and search."""
    
    serializer_class = ProductListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'description', 'short_description', 'brand__name']
    ordering_fields = ['name', 'base_price', 'created_at', 'view_count', 'purchase_count']
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = Product.objects.filter(status='active').select_related(
            'category', 'brand'
        ).prefetch_related('images', 'reviews')
        
        # Handle special sorting options
        sort_by = self.request.query_params.get('sort_by', '-created_at')
        
        if sort_by == 'rating':
            queryset = queryset.annotate(
                avg_rating=Avg('reviews__rating')
            ).order_by('avg_rating')
        elif sort_by == '-rating':
            queryset = queryset.annotate(
                avg_rating=Avg('reviews__rating')
            ).order_by('-avg_rating')
        elif sort_by == 'popularity':
            queryset = queryset.order_by('view_count')
        elif sort_by == '-popularity':
            queryset = queryset.order_by('-view_count')
        elif sort_by == 'price':
            queryset = queryset.order_by('base_price')
        elif sort_by == '-price':
            queryset = queryset.order_by('-base_price')
        else:
            queryset = queryset.order_by(sort_by)
        
        return queryset


class ProductDetailView(generics.RetrieveAPIView):
    """Get product details."""
    
    serializer_class = ProductDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'
    
    def get_queryset(self):
        return Product.objects.filter(status='active').select_related(
            'category', 'brand'
        ).prefetch_related(
            'images', 'variants', 'attribute_values', 'reviews'
        )
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Increment view count
        Product.objects.filter(id=instance.id).update(view_count=F('view_count') + 1)
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ProductReviewListCreateView(generics.ListCreateAPIView):
    """List and create product reviews."""
    
    serializer_class = ProductReviewSerializer
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]
    
    def get_queryset(self):
        product_slug = self.kwargs['product_slug']
        product = get_object_or_404(Product, slug=product_slug, status='active')
        return product.reviews.filter(is_approved=True).order_by('-created_at')
    
    def perform_create(self, serializer):
        product_slug = self.kwargs['product_slug']
        product = get_object_or_404(Product, slug=product_slug, status='active')
        
        # Check if user has already reviewed this product
        if ProductReview.objects.filter(product=product, user=self.request.user).exists():
            raise serializers.ValidationError("You have already reviewed this product.")
        
        serializer.save(product=product)


class WishlistListCreateView(generics.ListCreateAPIView):
    """List and add items to wishlist."""
    
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user).select_related('product')


class WishlistDetailView(generics.DestroyAPIView):
    """Remove item from wishlist."""
    
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def toggle_wishlist(request, product_slug):
    """Toggle product in/out of wishlist."""
    
    product = get_object_or_404(Product, slug=product_slug, status='active')
    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )
    
    if not created:
        wishlist_item.delete()
        return Response({'wishlisted': False}, status=status.HTTP_200_OK)
    
    return Response({'wishlisted': True}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_review_helpful(request, review_id):
    """Mark a review as helpful."""
    
    review = get_object_or_404(ProductReview, id=review_id, is_approved=True)
    
    # Increment helpful count
    ProductReview.objects.filter(id=review_id).update(
        helpful_count=F('helpful_count') + 1
    )
    
    return Response({'helpful_count': review.helpful_count + 1}, status=status.HTTP_200_OK)


class FeaturedProductsView(generics.ListAPIView):
    """Get featured products."""
    
    serializer_class = ProductListSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        return Product.objects.filter(
            status='active', 
            is_featured=True
        ).select_related('category', 'brand').prefetch_related('images')[:12]


class TrendingProductsView(generics.ListAPIView):
    """Get trending products based on views and purchases."""
    
    serializer_class = ProductListSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        return Product.objects.filter(
            status='active'
        ).select_related('category', 'brand').prefetch_related('images').annotate(
            popularity_score=F('view_count') + (F('purchase_count') * 5)
        ).order_by('-popularity_score')[:12]


class NewArrivalsView(generics.ListAPIView):
    """Get new arrival products."""
    
    serializer_class = ProductListSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        return Product.objects.filter(
            status='active'
        ).select_related('category', 'brand').prefetch_related('images').order_by('-created_at')[:12]


class ProductAttributeListView(generics.ListAPIView):
    """List product attributes for filtering."""
    
    serializer_class = ProductAttributeSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        return ProductAttribute.objects.filter(is_filterable=True)


class ProductVariantListView(generics.ListAPIView):
    """Get variants for a specific product."""
    
    serializer_class = ProductVariantSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        product_slug = self.kwargs['product_slug']
        product = get_object_or_404(Product, slug=product_slug, status='active')
        return product.variants.filter(is_active=True)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def product_search_suggestions(request):
    """Get search suggestions for products."""
    
    query = request.query_params.get('q', '').strip()
    if not query or len(query) < 2:
        return Response({'suggestions': []})
    
    # Product name suggestions
    product_names = Product.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query),
        status='active'
    ).values_list('name', flat=True)[:5]
    
    # Brand suggestions
    brand_names = Brand.objects.filter(
        name__icontains=query,
        is_active=True
    ).values_list('name', flat=True)[:3]
    
    # Category suggestions
    category_names = Category.objects.filter(
        name__icontains=query,
        is_active=True
    ).values_list('name', flat=True)[:3]
    
    suggestions = {
        'products': list(product_names),
        'brands': list(brand_names),
        'categories': list(category_names),
    }
    
    return Response({'suggestions': suggestions})


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def product_filters(request):
    """Get available filters for products."""
    
    # Get available categories
    categories = Category.objects.filter(
        is_active=True,
        products__status='active'
    ).distinct().values('id', 'name', 'slug')
    
    # Get available brands
    brands = Brand.objects.filter(
        is_active=True,
        products__status='active'
    ).distinct().values('id', 'name', 'slug')
    
    # Get available sizes
    sizes = ProductVariant.objects.filter(
        product__status='active',
        is_active=True
    ).values_list('size', flat=True).distinct()
    
    # Get available colors
    colors = ProductVariant.objects.filter(
        product__status='active',
        is_active=True
    ).values('color', 'color_hex').distinct()
    
    # Get price range
    price_range = Product.objects.filter(status='active').aggregate(
        min_price=models.Min('base_price'),
        max_price=models.Max('base_price')
    )
    
    filters = {
        'categories': list(categories),
        'brands': list(brands),
        'sizes': list(set(sizes)),
        'colors': list(colors),
        'price_range': price_range,
        'genders': [{'value': choice[0], 'label': choice[1]} for choice in Product.GENDER_CHOICES],
    }
    
    return Response({'filters': filters})
