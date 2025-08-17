"""
URL patterns for product management.
"""
from django.urls import path

from . import views

urlpatterns = [
    # Categories
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('categories/<slug:slug>/', views.CategoryDetailView.as_view(), name='category-detail'),
    
    # Brands
    path('brands/', views.BrandListView.as_view(), name='brand-list'),
    path('brands/<slug:slug>/', views.BrandDetailView.as_view(), name='brand-detail'),
    
    # Products
    path('', views.ProductListView.as_view(), name='product-list'),
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('<slug:product_slug>/variants/', views.ProductVariantListView.as_view(), name='product-variants'),
    
    # Product collections
    path('collections/featured/', views.FeaturedProductsView.as_view(), name='featured-products'),
    path('collections/trending/', views.TrendingProductsView.as_view(), name='trending-products'),
    path('collections/new-arrivals/', views.NewArrivalsView.as_view(), name='new-arrivals'),
    
    # Reviews
    path('<slug:product_slug>/reviews/', views.ProductReviewListCreateView.as_view(), name='product-reviews'),
    path('reviews/<uuid:review_id>/helpful/', views.mark_review_helpful, name='mark-review-helpful'),
    
    # Wishlist
    path('wishlist/', views.WishlistListCreateView.as_view(), name='wishlist'),
    path('wishlist/<uuid:pk>/', views.WishlistDetailView.as_view(), name='wishlist-detail'),
    path('<slug:product_slug>/wishlist/toggle/', views.toggle_wishlist, name='toggle-wishlist'),
    
    # Search and filters
    path('search/suggestions/', views.product_search_suggestions, name='search-suggestions'),
    path('filters/', views.product_filters, name='product-filters'),
    path('attributes/', views.ProductAttributeListView.as_view(), name='product-attributes'),
]
