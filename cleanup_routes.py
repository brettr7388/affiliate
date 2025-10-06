#!/usr/bin/env python3
"""
Clean up demo routes - remove duplicates and test routes
"""

import sqlite3

def cleanup_routes():
    """Clean up the routes table"""
    print("🧹 Cleaning up routes...")
    
    conn = sqlite3.connect('affiliate.db')
    cursor = conn.cursor()
    
    # Remove problematic routes
    routes_to_remove = [
        'demo-test-route',
        'ditch-the-plastic-why-the-good-dog-company-hemp-canvas-leash-is-your-new-best-friend-and-your-dog-s',
        'spoil-your-furry-friend-sustainably-a-how-to-guide-to-wag-expedition-organic-banana-coconut-treats',
        'the-sleepless-nights-are-over-finding-the-perfect-eco-friendly-bed-for-your-furry-friend'
    ]
    
    for slug in routes_to_remove:
        cursor.execute('DELETE FROM routes WHERE slug = ?', (slug,))
        print(f"   Removed: {slug}")
    
    # Update existing routes with better names
    route_updates = [
        ('hemp-dog-leash', 'Eco-Friendly Hemp Dog Leash'),
        ('organic-dog-treats', 'Premium Organic Dog Treats'),
        ('recycled-dog-bed', 'Sustainable Recycled Dog Bed'),
        ('biodegradable-poop-bags', 'Biodegradable Dog Waste Bags'),
        ('sustainable-dog-bowls', 'Bamboo & Stainless Dog Bowls'),
        ('eco-dog-toys-2025', 'Best Eco-Friendly Dog Toys 2025')
    ]
    
    for slug, new_offer in route_updates:
        cursor.execute('UPDATE routes SET offer = ? WHERE slug = ?', (new_offer, slug))
        print(f"   Updated: {slug} -> {new_offer}")
    
    # Add missing routes if they don't exist
    missing_routes = [
        {
            'slug': 'eco-dog-beds',
            'offer': 'Eco-Friendly Dog Beds',
            'dest_url': 'https://amazon.com/dp/B00TQ47CPW?tag=YOUR-AMAZON-ASSOCIATES-TAG'
        },
        {
            'slug': 'natural-dog-treats',
            'offer': 'All-Natural Dog Treats',
            'dest_url': 'https://amazon.com/dp/B093CLBJDW?tag=YOUR-AMAZON-ASSOCIATES-TAG'
        }
    ]
    
    for route in missing_routes:
        cursor.execute('SELECT COUNT(*) FROM routes WHERE slug = ?', (route['slug'],))
        if cursor.fetchone()[0] == 0:
            cursor.execute('''
                INSERT INTO routes (slug, offer, variant, dest_url)
                VALUES (?, ?, 'A', ?)
            ''', (route['slug'], route['offer'], route['dest_url']))
            print(f"   Added: {route['slug']}")
    
    conn.commit()
    conn.close()
    print("✅ Routes cleaned up successfully!")

if __name__ == "__main__":
    cleanup_routes()
