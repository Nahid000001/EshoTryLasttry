"""
Django filters for product filtering.
"""
import django_filters
from django.db.models import Q
from .models import Product, Category, Brand, ProductVariant


class ProductFilter(django_filters.FilterSet):
    """Filter set for products."""
    
    # Basic filters
    category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.filter(is_active=True),
        field_name='category'
    )
    brand = django_filters.ModelChoiceFilter(
        queryset=Brand.objects.filter(is_active=True),
        field_name='brand'
    )
    gender = django_filters.ChoiceFilter(choices=Product.GENDER_CHOICES)
    
    # Price filters
    min_price = django_filters.NumberFilter(field_name='base_price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='base_price', lookup_expr='lte')
    
    # Stock filters
    in_stock = django_filters.BooleanFilter(method='filter_in_stock')
    on_sale = django_filters.BooleanFilter(method='filter_on_sale')
    
    # Variant filters
    size = django_filters.CharFilter(method='filter_size')
    color = django_filters.CharFilter(method='filter_color')
    
    # Feature filters
    featured = django_filters.BooleanFilter(field_name='is_featured')
    virtual_tryon = django_filters.BooleanFilter(field_name='is_virtual_tryon_enabled')
    
    # Text search
    search = django_filters.CharFilter(method='filter_search')
    
    class Meta:
        model = Product
        fields = [
            'category', 'brand', 'gender', 'min_price', 'max_price',
            'in_stock', 'on_sale', 'size', 'color', 'featured',
            'virtual_tryon', 'search'
        ]
    
    def filter_in_stock(self, queryset, name, value):
        """Filter products that are in stock."""
        if value:
            return queryset.filter(
                Q(track_inventory=False) | Q(stock_quantity__gt=0)
            )
        return queryset
    
    def filter_on_sale(self, queryset, name, value):
        """Filter products that are on sale."""
        if value:
            return queryset.filter(
                sale_price__isnull=False,
                sale_price__lt=models.F('base_price')
            )
        return queryset
    
    def filter_size(self, queryset, name, value):
        """Filter products by available size."""
        if value:
            return queryset.filter(
                variants__size__iexact=value,
                variants__is_active=True
            ).distinct()
        return queryset
    
    def filter_color(self, queryset, name, value):
        """Filter products by available color."""
        if value:
            return queryset.filter(
                variants__color__icontains=value,
                variants__is_active=True
            ).distinct()
        return queryset
    
    def filter_search(self, queryset, name, value):
        """Full-text search across multiple fields."""
        if value:
            return queryset.filter(
                Q(name__icontains=value) |
                Q(description__icontains=value) |
                Q(short_description__icontains=value) |
                Q(brand__name__icontains=value) |
                Q(category__name__icontains=value) |
                Q(sku__icontains=value)
            ).distinct()
        return queryset
