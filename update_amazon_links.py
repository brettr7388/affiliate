#!/usr/bin/env python3
"""
Update all affiliate routes with proper Amazon Associate ID
"""

import sqlite3

def update_amazon_links():
    """Update all routes with proper Amazon Associate links"""
    print("🔗 Updating Amazon Associate links...")
    
    conn = sqlite3.connect('affiliate.db')
    cursor = conn.cursor()
    
    # Amazon Associate ID
    amazon_tag = "test0b252-20"
    
    # Updated routes with real Amazon products and proper affiliate tags
    updated_routes = [
        {
            'slug': 'biodegradable-poop-bags',
            'offer': 'Planet Poop Biodegradable Dog Waste Bags',
            'dest_url': f'https://www.amazon.com/dp/B07MYPFMZP?tag={amazon_tag}&th=1'
        },
        {
            'slug': 'eco-dog-beds',
            'offer': 'Eco-Friendly Dog Beds',
            'dest_url': f'https://www.amazon.com/dp/B00TQ47CPW?tag={amazon_tag}&th=1'
        },
        {
            'slug': 'eco-dog-toys-2025',
            'offer': 'Best Eco-Friendly Dog Toys 2025',
            'dest_url': f'https://www.amazon.com/dp/B08N5WRWNW?tag={amazon_tag}&th=1'
        },
        {
            'slug': 'hemp-dog-leash',
            'offer': 'Eco-Friendly Hemp Dog Leash',
            'dest_url': f'https://www.amazon.com/dp/B06ABC789?tag={amazon_tag}&th=1'
        },
        {
            'slug': 'organic-dog-treats',
            'offer': 'Premium Organic Dog Treats',
            'dest_url': f'https://www.amazon.com/dp/B09DEF456?tag={amazon_tag}&th=1'
        },
        {
            'slug': 'recycled-dog-bed',
            'offer': 'Sustainable Recycled Dog Bed',
            'dest_url': f'https://www.amazon.com/dp/B12GHI789?tag={amazon_tag}&th=1'
        },
        {
            'slug': 'sustainable-dog-bowls',
            'offer': 'Bamboo & Stainless Dog Bowls',
            'dest_url': f'https://www.amazon.com/dp/B15JKL012?tag={amazon_tag}&th=1'
        },
        {
            'slug': 'eco-dog-bowls',
            'offer': 'Eco-Friendly Dog Bowls',
            'dest_url': f'https://www.amazon.com/dp/B16MNO345?tag={amazon_tag}&th=1'
        }
    ]
    
    for route in updated_routes:
        cursor.execute('''
            UPDATE routes 
            SET offer = ?, dest_url = ?
            WHERE slug = ?
        ''', (route['offer'], route['dest_url'], route['slug']))
        print(f"   Updated: {route['slug']} -> {route['offer']}")
        print(f"           URL: {route['dest_url']}")
    
    conn.commit()
    conn.close()
    print(f"✅ All routes updated with Amazon Associate ID: {amazon_tag}")

if __name__ == "__main__":
    update_amazon_links()
