#!/usr/bin/env python3
"""
Startup fixes for Render deployment
This runs automatically when the app starts to ensure database is properly configured
"""

import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

def run_startup_fixes():
    """Run all necessary database fixes on startup"""
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./affiliate.db")
    
    # Skip fixes for local SQLite development
    if "sqlite" in DATABASE_URL.lower():
        print("📝 Skipping startup fixes for local SQLite database")
        return
    
    print("🚀 Running startup database fixes for production...")
    
    try:
        engine = create_engine(DATABASE_URL, future=True)
        
        with engine.begin() as conn:
            # Fix organic dog treats route
            print("🔧 Checking organic-dog-treats route...")
            
            # Check if route exists and is incorrect
            route = conn.execute(text("""
                SELECT slug, offer, dest_url FROM routes 
                WHERE slug = 'organic-dog-treats'
            """)).fetchone()
            
            if route and "B004A7X27M" in route.dest_url:
                print("❌ Found incorrect organic treats link - fixing...")
                conn.execute(text("""
                    UPDATE routes 
                    SET offer = 'AmazonOrganicDogTreats',
                        dest_url = 'https://www.amazon.com/dp/B093CLBJDW?tag=test0b252-20&utm_source=site&utm_campaign=content'
                    WHERE slug = 'organic-dog-treats'
                """))
                print("✅ Fixed organic-dog-treats route!")
            
            elif not route:
                print("➕ Creating organic-dog-treats route...")
                conn.execute(text("""
                    INSERT INTO routes (slug, offer, dest_url) 
                    VALUES (
                        'organic-dog-treats', 
                        'AmazonOrganicDogTreats',
                        'https://www.amazon.com/dp/B093CLBJDW?tag=test0b252-20&utm_source=site&utm_campaign=content'
                    )
                """))
                print("✅ Created organic-dog-treats route!")
            
            else:
                print("✅ Organic treats route already correct!")
            
            # Fix sustainable dog bowls route if needed
            bowl_route = conn.execute(text("""
                SELECT slug, offer, dest_url FROM routes 
                WHERE slug = 'sustainable-dog-bowls'
            """)).fetchone()
            
            if bowl_route and "B004A7X27M" in bowl_route.dest_url:
                print("🔧 Fixing sustainable-dog-bowls route...")
                conn.execute(text("""
                    UPDATE routes 
                    SET offer = 'AmazonEcoFriendlyDogBowls',
                        dest_url = 'https://www.amazon.com/dp/B08C342VQ6?tag=test0b252-20&utm_source=site&utm_campaign=content'
                    WHERE slug = 'sustainable-dog-bowls'
                """))
                print("✅ Fixed sustainable-dog-bowls route!")
        
        print("🎉 All startup fixes completed successfully!")
        
    except Exception as e:
        print(f"⚠️  Startup fix error: {e}")
        print("App will continue starting...")

if __name__ == "__main__":
    run_startup_fixes() 