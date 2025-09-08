#!/usr/bin/env python3
"""
Update affiliate routes with ChatGPT-researched eco-friendly products
"""

import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./affiliate.db")
engine = create_engine(DATABASE_URL, future=True)

# New products from ChatGPT research
# Note: You'll need to add your Amazon Associates tag to these URLs
new_products = [
    {
        "slug": "biodegradable-poop-bags",
        "offer": "PLANET POOP Home Compostable Dog Poop Bags",
        "dest_url": "https://amazon.com/dp/B07MYPFMZP?tag=YOUR_AMAZON_TAG_HERE"
    },
    {
        "slug": "hemp-dog-leash", 
        "offer": "The Good Dog Company Hemp Canvas Basic Leash",
        "dest_url": "https://amazon.com/dp/B00C9L67XW?tag=YOUR_AMAZON_TAG_HERE"
    },
    {
        "slug": "organic-dog-treats",
        "offer": "WAG Expedition Organic Banana & Coconut Treats",
        "dest_url": "https://amazon.com/dp/B093CLBJDW?tag=YOUR_AMAZON_TAG_HERE"
    },
    {
        "slug": "recycled-dog-bed",
        "offer": "PetFusion Ultimate Dog Bed & Lounge",
        "dest_url": "https://amazon.com/dp/B00TQ47CPW?tag=YOUR_AMAZON_TAG_HERE"
    },
    {
        "slug": "sustainable-dog-bowls",
        "offer": "Beco Pets Bamboo Dog Bowl",
        "dest_url": "https://amazon.com/dp/B08C342VQ6?tag=YOUR_AMAZON_TAG_HERE"
    }
]

def update_products():
    print("🛒 Updating affiliate products with ChatGPT research...")
    print("=" * 60)
    
    # Check current Amazon tag
    amazon_tag = "test0b252-20"  # Default from your system
    print(f"💡 Using Amazon Associates tag: {amazon_tag}")
    print("   (Update this with your real tag later!)")
    print()
    
    with engine.begin() as conn:
        for product in new_products:
            # Replace placeholder with actual tag
            dest_url = product["dest_url"].replace("YOUR_AMAZON_TAG_HERE", amazon_tag)
            
            # Update the route
            conn.execute(
                text("""
                    UPDATE routes 
                    SET offer = :offer, dest_url = :dest_url, variant = 'A'
                    WHERE slug = :slug
                """),
                {
                    "slug": product["slug"],
                    "offer": product["offer"], 
                    "dest_url": dest_url
                }
            )
            
            print(f"✅ Updated: {product['slug']}")
            print(f"   Product: {product['offer']}")
            print(f"   URL: {dest_url}")
            print()
    
    print("🎉 All products updated successfully!")
    print()
    print("📋 Article ideas from your research:")
    articles = [
        "Best Biodegradable Dog Poop Bags 2025: Planet Poop Review",
        "The Good Dog Company Hemp Leash Review: Eco-Friendly Walking 2025", 
        "Best Organic Dog Treats 2025: WAG Expedition Review",
        "PetFusion Recycled Dog Bed Review: Sustainable Comfort 2025",
        "Best Sustainable Dog Bowls 2025: Beco Bamboo Review"
    ]
    
    for i, article in enumerate(articles, 1):
        print(f"{i}. {article}")
    
    print()
    print("🔗 Test your updated routes:")
    for product in new_products:
        print(f"   http://127.0.0.1:8088/r/{product['slug']}")

def check_current_routes():
    """Show current routes in database"""
    print("📊 Current Routes in Database:")
    print("=" * 50)
    
    with engine.begin() as conn:
        routes = conn.execute(
            text("SELECT slug, offer, dest_url FROM routes ORDER BY slug")
        ).fetchall()
        
        if not routes:
            print("❌ No routes found")
            return
            
        for route in routes:
            slug, offer, dest_url = route
            print(f"🔗 {slug}")
            print(f"   {offer}")
            print(f"   {dest_url[:60]}...")
            print()

if __name__ == "__main__":
    print("🛒 PRODUCT UPDATE SCRIPT")
    print("=" * 60)
    print("Adding ChatGPT-researched eco-friendly products")
    print()
    
    # Show before
    check_current_routes()
    
    # Update products
    update_products()
    
    print()
    print("🚀 Next Steps:")
    print("1. Get your Amazon Associates tag: https://affiliate-program.amazon.com/")
    print("2. Replace 'test0b252-20' with your real tag")
    print("3. Test all your affiliate links!")
    print("4. Write articles using the suggested titles above")
    print("5. Your homepage should now show the new products!")
