#!/usr/bin/env python3
"""
Quick fix for broken affiliate routes
This adds temporary Amazon URLs so routes work while you research real products
"""

import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./affiliate.db")
engine = create_engine(DATABASE_URL, future=True)

# Temporary Amazon URLs (you'll replace these with real products)
# Using generic Amazon pet product pages as placeholders
temp_routes = [
    {
        "slug": "biodegradable-poop-bags",
        "offer": "Earth-Rated Biodegradable Poop Bags",
        "dest_url": "https://www.amazon.com/dp/B004A7X27M?tag=test0b252-20"
    },
    {
        "slug": "eco-dog-toys-2025", 
        "offer": "Best Eco-Friendly Dog Toys 2025",
        "dest_url": "https://www.amazon.com/dp/B0002DJX44?tag=test0b252-20"
    },
    {
        "slug": "hemp-dog-leash",
        "offer": "Hemp Dog Leash - Planet Friendly", 
        "dest_url": "https://www.amazon.com/dp/B001FWXM0A?tag=test0b252-20"
    },
    {
        "slug": "organic-dog-treats",
        "offer": "Organic Dog Treats - Natural & Healthy",
        "dest_url": "https://www.amazon.com/dp/B004A7X27M?tag=test0b252-20"
    },
    {
        "slug": "recycled-dog-bed",
        "offer": "Recycled Dog Bed - Eco-Friendly Comfort",
        "dest_url": "https://www.amazon.com/dp/B001FWXM0A?tag=test0b252-20"
    },
    {
        "slug": "sustainable-dog-bowls",
        "offer": "Sustainable Dog Bowls - Bamboo & Steel",
        "dest_url": "https://www.amazon.com/dp/B0002DJX44?tag=test0b252-20"
    }
]

def fix_routes():
    print("🔧 Fixing broken affiliate routes...")
    print("=" * 50)
    
    with engine.begin() as conn:
        for route in temp_routes:
            # Check if route exists
            existing = conn.execute(
                text("SELECT slug FROM routes WHERE slug = :slug"),
                {"slug": route["slug"]}
            ).fetchone()
            
            if existing:
                # Update existing route
                conn.execute(
                    text("""
                        UPDATE routes 
                        SET offer = :offer, dest_url = :dest_url, variant = 'A'
                        WHERE slug = :slug
                    """),
                    route
                )
                print(f"✅ Updated: {route['slug']}")
            else:
                # Insert new route
                conn.execute(
                    text("""
                        INSERT INTO routes (slug, offer, dest_url, variant)
                        VALUES (:slug, :offer, :dest_url, 'A')
                    """),
                    {**route, "variant": "A"}
                )
                print(f"➕ Created: {route['slug']}")
    
    print("\n🎉 All routes fixed!")
    print("\n📋 Next steps:")
    print("1. Use the ChatGPT script to find real products")
    print("2. Update routes via admin panel: http://127.0.0.1:8088/admin")
    print("3. Test your affiliate links!")
    
    print("\n🔗 Test your routes:")
    for route in temp_routes:
        print(f"   http://127.0.0.1:8088/r/{route['slug']}")

def check_routes():
    """Check current routes in database"""
    print("\n📊 Current Routes in Database:")
    print("=" * 50)
    
    with engine.begin() as conn:
        routes = conn.execute(
            text("SELECT slug, offer, dest_url FROM routes ORDER BY slug")
        ).fetchall()
        
        if not routes:
            print("❌ No routes found in database")
            return
        
        for route in routes:
            slug, offer, dest_url = route
            print(f"🔗 {slug}")
            print(f"   Offer: {offer}")
            print(f"   URL: {dest_url}")
            print()

if __name__ == "__main__":
    print("🛠️  AFFILIATE ROUTE FIXER")
    print("=" * 60)
    
    # Show current state
    check_routes()
    
    # Fix the routes
    fix_routes()
    
    # Show final state
    check_routes()
    
    print("💡 TIP: Replace 'test0b252-20' with your real Amazon Associates tag!")
    print("📖 Get your Amazon Associates tag at: https://affiliate-program.amazon.com/")
