#!/usr/bin/env python3
"""
Fix organic dog treats route in Render PostgreSQL database
Run this script on Render or with the Render DATABASE_URL
"""

import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

# Use DATABASE_URL from environment (Render will have this set)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./affiliate.db")
engine = create_engine(DATABASE_URL, future=True)

def fix_organic_treats_route():
    """Fix the organic-dog-treats route to point to the correct product"""
    print("🔧 Fixing organic dog treats route...")
    
    with engine.begin() as conn:
        # Check current route
        current = conn.execute(text("""
            SELECT slug, offer, dest_url FROM routes 
            WHERE slug = 'organic-dog-treats'
        """)).fetchone()
        
        if current:
            print(f"Current route: {current.slug}")
            print(f"Current offer: {current.offer}")
            print(f"Current URL: {current.dest_url}")
            
            if "B004A7X27M" in current.dest_url:
                print("❌ Found incorrect link - fixing now...")
                
                # Update to correct organic treats link
                conn.execute(text("""
                    UPDATE routes 
                    SET offer = 'AmazonOrganicDogTreats',
                        dest_url = 'https://www.amazon.com/dp/B093CLBJDW?tag=test0b252-20&utm_source=site&utm_campaign=content'
                    WHERE slug = 'organic-dog-treats'
                """))
                
                print("✅ Updated organic-dog-treats route!")
                
                # Verify the fix
                updated = conn.execute(text("""
                    SELECT slug, offer, dest_url FROM routes 
                    WHERE slug = 'organic-dog-treats'
                """)).fetchone()
                
                print(f"✅ Verified - New URL: {updated.dest_url}")
                
            else:
                print("✅ Route already has correct link!")
        else:
            print("❌ organic-dog-treats route not found - creating it...")
            
            # Insert the correct route
            conn.execute(text("""
                INSERT INTO routes (slug, offer, dest_url) 
                VALUES (
                    'organic-dog-treats', 
                    'AmazonOrganicDogTreats',
                    'https://www.amazon.com/dp/B093CLBJDW?tag=test0b252-20&utm_source=site&utm_campaign=content'
                )
            """))
            
            print("✅ Created organic-dog-treats route!")

if __name__ == "__main__":
    print("🐕 Organic Dog Treats Route Fixer")
    print("=" * 50)
    print(f"Database: {DATABASE_URL}")
    
    try:
        fix_organic_treats_route()
        print("\n🎉 Fix completed successfully!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Make sure you have the correct DATABASE_URL set.") 