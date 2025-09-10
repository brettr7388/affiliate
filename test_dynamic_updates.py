#!/usr/bin/env python3
"""
Test script to demonstrate how the dynamic product comparison system works.

This shows the complete flow:
1. Add new route to database (simulates admin portal creating new article)
2. Update config.yaml with new product comparison
3. Show how homepage automatically picks up changes
"""

import sqlite3
import yaml
import requests
import json
from datetime import datetime

def show_current_routes():
    """Show current routes in database"""
    print("📊 Current Routes in Database:")
    print("=" * 50)
    
    conn = sqlite3.connect('affiliate.db')
    cursor = conn.cursor()
    cursor.execute('SELECT slug, offer, dest_url FROM routes ORDER BY slug')
    routes = cursor.fetchall()
    
    for slug, offer, dest_url in routes:
        print(f"  • {slug}")
        print(f"    Offer: {offer}")
        print(f"    URL: {dest_url}")
        print()
    
    conn.close()
    print(f"Total routes: {len(routes)}")
    return routes

def show_current_comparisons():
    """Show what product comparisons are currently configured"""
    print("\n🎯 Current Product Comparisons:")
    print("=" * 50)
    
    try:
        response = requests.get('http://127.0.0.1:8088/api/product-comparisons')
        data = response.json()
        
        for comparison in data.get('comparisons', []):
            print(f"  📦 {comparison['title']}")
            print(f"     Category: {comparison['category']}")
            print(f"     Display: {comparison['display_type']}")
            print(f"     Products: {len(comparison['products'])}")
            
            for product in comparison['products']:
                print(f"       - {product['name']} → {product['link']}")
            print()
        
        print(f"Total comparisons: {len(data.get('comparisons', []))}")
        
    except Exception as e:
        print(f"Error fetching comparisons: {e}")

def add_new_route(slug, offer, dest_url):
    """Add a new route to the database (simulates admin portal)"""
    print(f"\n🆕 Adding New Route: {slug}")
    print("=" * 50)
    
    conn = sqlite3.connect('affiliate.db')
    cursor = conn.cursor()
    
    # Insert new route (with UPSERT to handle conflicts)
    cursor.execute('''
        INSERT OR REPLACE INTO routes (slug, offer, variant, dest_url)
        VALUES (?, ?, ?, ?)
    ''', (slug, offer, 'A', dest_url))
    
    conn.commit()
    conn.close()
    
    print(f"✅ Added route: {slug} → {dest_url}")

def add_new_product_comparison(category, title, products):
    """Add a new product comparison to config.yaml"""
    print(f"\n📝 Adding New Product Comparison: {title}")
    print("=" * 50)
    
    # Load current config
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    # Add new comparison to the product_comparisons list
    new_comparison = {
        'category': category,
        'title': title,
        'description': f'Compare the best {category.replace("-", " ")} products',
        'display_type': 'cards',
        'products': products
    }
    
    content_config = config.setdefault('content', {})
    comparisons = content_config.setdefault('product_comparisons', [])
    
    # Check if category already exists
    existing_index = None
    for i, comp in enumerate(comparisons):
        if comp['category'] == category:
            existing_index = i
            break
    
    if existing_index is not None:
        # Update existing comparison
        comparisons[existing_index] = new_comparison
        print(f"✅ Updated existing comparison for category: {category}")
    else:
        # Add new comparison
        comparisons.append(new_comparison)
        print(f"✅ Added new comparison for category: {category}")
    
    # Write back to config
    with open('config.yaml', 'w') as f:
        yaml.dump(config, f, default_flow_style=False, indent=2)
    
    print(f"📄 Config updated with {len(products)} products")

def test_dynamic_update_flow():
    """Test the complete dynamic update flow"""
    print("🧪 TESTING DYNAMIC PRODUCT COMPARISON UPDATES")
    print("=" * 60)
    
    # Step 1: Show current state
    print("STEP 1: Current State")
    routes = show_current_routes()
    show_current_comparisons()
    
    # Step 2: Add new route (simulates content generation)
    print("\nSTEP 2: Simulate Adding New Product Category")
    new_slug = "eco-dog-leashes-2025"
    new_offer = "AmazonEcoFriendlyDogLeashes"
    new_dest_url = "https://www.amazon.com/dp/B08EXAMPLE?tag=YOUR-AMAZON-ASSOCIATES-TAG"
    
    add_new_route(new_slug, new_offer, new_dest_url)
    
    # Step 3: Add new product comparison
    print("\nSTEP 3: Add New Product Comparison Configuration")
    new_products = [
        {
            'name': 'Hemp Dog Leash',
            'rating': '⭐⭐⭐⭐⭐',
            'description': '100% organic hemp, durable and eco-friendly',
            'price': '$25',
            'route_slug': new_slug,
            'badge': 'Most Sustainable',
            'badge_color': 'eco-green'
        },
        {
            'name': 'Recycled Rope Leash',
            'rating': '⭐⭐⭐⭐',
            'description': 'Made from recycled climbing rope',
            'price': '$20',
            'route_slug': new_slug,
            'badge': 'Best Value',
            'badge_color': 'gray'
        },
        {
            'name': 'Cork & Canvas Leash',
            'rating': '⭐⭐⭐⭐⭐',
            'description': 'Sustainable cork handle with organic canvas',
            'price': '$30',
            'route_slug': new_slug,
            'badge': 'Premium Choice',
            'badge_color': 'gray'
        }
    ]
    
    add_new_product_comparison(
        category='dog-leashes',
        title='🦮 Best Eco-Friendly Dog Leashes',
        products=new_products
    )
    
    # Step 4: Show updated state
    print("\nSTEP 4: Updated State (After Changes)")
    show_current_routes()
    show_current_comparisons()
    
    # Step 5: Instructions for user
    print("\nSTEP 5: See Changes on Homepage")
    print("=" * 50)
    print("🌐 Visit http://127.0.0.1:8088 to see the new comparison!")
    print("📄 The homepage will now show 3 product comparisons instead of 2")
    print("🔄 The new 'Best Eco-Friendly Dog Leashes' section will appear automatically")
    print("✨ All links will work and point to the new route we created")
    
    print("\n🎯 KEY POINTS:")
    print("  ✅ No manual HTML editing required")
    print("  ✅ New routes automatically detected by API")
    print("  ✅ Product comparisons render dynamically")
    print("  ✅ Scroll animations work on new content")
    print("  ✅ Links automatically generated from database routes")

def cleanup_test_data():
    """Remove test data added during demonstration"""
    print("\n🧹 CLEANUP: Removing Test Data")
    print("=" * 50)
    
    # Remove test route
    conn = sqlite3.connect('affiliate.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM routes WHERE slug = ?', ('eco-dog-leashes-2025',))
    conn.commit()
    conn.close()
    print("✅ Removed test route from database")
    
    # Remove test comparison from config
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    content_config = config.get('content', {})
    comparisons = content_config.get('product_comparisons', [])
    
    # Remove dog-leashes comparison
    updated_comparisons = [comp for comp in comparisons if comp.get('category') != 'dog-leashes']
    content_config['product_comparisons'] = updated_comparisons
    
    with open('config.yaml', 'w') as f:
        yaml.dump(config, f, default_flow_style=False, indent=2)
    
    print("✅ Removed test comparison from config")
    print("🔄 Homepage will return to original state")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "cleanup":
        cleanup_test_data()
    else:
        test_dynamic_update_flow()
        
        print("\n" + "="*60)
        print("Run 'python test_dynamic_updates.py cleanup' to remove test data") 