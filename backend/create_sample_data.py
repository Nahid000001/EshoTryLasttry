#!/usr/bin/env python
"""
Script to create sample data for EshoTry platform
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eshotry.settings')
django.setup()

from apps.users.models import User
from apps.products.models import Category, Brand, Product

def create_sample_data():
    print("Creating sample data...")
    
    # Create categories
    categories_data = [
        {'name': 'Women', 'slug': 'women', 'description': 'Women\'s fashion and accessories'},
        {'name': 'Men', 'slug': 'men', 'description': 'Men\'s fashion and accessories'},
        {'name': 'Dresses', 'slug': 'dresses', 'description': 'Beautiful dresses for all occasions'},
        {'name': 'Tops', 'slug': 'tops', 'description': 'Stylish tops and shirts'},
        {'name': 'Jeans', 'slug': 'jeans', 'description': 'Comfortable and trendy jeans'},
    ]
    
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            slug=cat_data['slug'],
            defaults=cat_data
        )
        if created:
            print(f"Created category: {category.name}")
    
    # Create brands
    brands_data = [
        {'name': 'Nike', 'slug': 'nike', 'description': 'Just Do It'},
        {'name': 'Adidas', 'slug': 'adidas', 'description': 'Impossible is Nothing'},
        {'name': 'Zara', 'slug': 'zara', 'description': 'Fast fashion retailer'},
        {'name': 'H&M', 'slug': 'hm', 'description': 'Fashion and quality at the best price'},
        {'name': 'Uniqlo', 'slug': 'uniqlo', 'description': 'Simple, quality clothing'},
    ]
    
    for brand_data in brands_data:
        brand, created = Brand.objects.get_or_create(
            slug=brand_data['slug'],
            defaults=brand_data
        )
        if created:
            print(f"Created brand: {brand.name}")
    
    # Create sample products
    women_category = Category.objects.get(slug='women')
    dresses_category = Category.objects.get(slug='dresses')
    tops_category = Category.objects.get(slug='tops')
    
    nike_brand = Brand.objects.get(slug='nike')
    zara_brand = Brand.objects.get(slug='zara')
    hm_brand = Brand.objects.get(slug='hm')
    
    products_data = [
        {
            'name': 'Summer Floral Dress',
            'slug': 'summer-floral-dress',
            'description': 'Beautiful floral dress perfect for summer occasions',
            'short_description': 'Elegant floral summer dress',
            'category': dresses_category,
            'brand': zara_brand,
            'gender': 'F',
            'sku': 'ZAR-SFD-001',
            'base_price': 89.99,
            'stock_quantity': 50,
            'is_featured': True,
        },
        {
            'name': 'Classic White T-Shirt',
            'slug': 'classic-white-tshirt',
            'description': 'Essential white t-shirt made from 100% cotton',
            'short_description': 'Basic white cotton t-shirt',
            'category': tops_category,
            'brand': hm_brand,
            'gender': 'U',
            'sku': 'HM-CWT-001',
            'base_price': 19.99,
            'stock_quantity': 100,
            'is_featured': False,
        },
        {
            'name': 'Athletic Sports Bra',
            'slug': 'athletic-sports-bra',
            'description': 'High-performance sports bra for active women',
            'short_description': 'Supportive athletic sports bra',
            'category': tops_category,
            'brand': nike_brand,
            'gender': 'F',
            'sku': 'NIKE-ASB-001',
            'base_price': 45.99,
            'sale_price': 35.99,
            'stock_quantity': 30,
            'is_featured': True,
        },
        {
            'name': 'Evening Cocktail Dress',
            'slug': 'evening-cocktail-dress',
            'description': 'Elegant black cocktail dress for special events',
            'short_description': 'Sophisticated evening dress',
            'category': dresses_category,
            'brand': zara_brand,
            'gender': 'F',
            'sku': 'ZAR-ECD-001',
            'base_price': 129.99,
            'stock_quantity': 25,
            'is_featured': True,
        },
        {
            'name': 'Casual Striped Top',
            'slug': 'casual-striped-top',
            'description': 'Comfortable striped top for everyday wear',
            'short_description': 'Relaxed fit striped top',
            'category': tops_category,
            'brand': hm_brand,
            'gender': 'F',
            'sku': 'HM-CST-001',
            'base_price': 24.99,
            'stock_quantity': 75,
            'is_featured': False,
        },
    ]
    
    for product_data in products_data:
        product, created = Product.objects.get_or_create(
            sku=product_data['sku'],
            defaults=product_data
        )
        if created:
            print(f"Created product: {product.name}")
    
    print("Sample data creation completed!")
    print(f"Created {Category.objects.count()} categories")
    print(f"Created {Brand.objects.count()} brands") 
    print(f"Created {Product.objects.count()} products")

if __name__ == '__main__':
    create_sample_data()
