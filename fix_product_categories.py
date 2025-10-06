#!/usr/bin/env python3
"""
Fix product categories - remove duplicate treats, add more bowls
"""

import sqlite3

def fix_product_categories():
    """Fix the product categories"""
    print("🔧 Fixing product categories...")
    
    conn = sqlite3.connect('affiliate.db')
    cursor = conn.cursor()
    
    # Remove the natural-dog-treats (keep organic-dog-treats)
    cursor.execute('DELETE FROM routes WHERE slug = ?', ('natural-dog-treats',))
    print("   Removed: natural-dog-treats")
    
    # Add a new dog bowl category
    new_bowl_route = {
        'slug': 'eco-dog-bowls',
        'offer': 'Eco-Friendly Dog Bowls',
        'dest_url': 'https://amazon.com/dp/B16MNO345?tag=YOUR-AMAZON-ASSOCIATES-TAG'
    }
    
    cursor.execute('''
        INSERT INTO routes (slug, offer, variant, dest_url)
        VALUES (?, ?, 'A', ?)
    ''', (new_bowl_route['slug'], new_bowl_route['offer'], new_bowl_route['dest_url']))
    print(f"   Added: {new_bowl_route['slug']}")
    
    conn.commit()
    conn.close()
    print("✅ Product categories fixed!")

if __name__ == "__main__":
    fix_product_categories()
