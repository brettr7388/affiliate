#!/usr/bin/env python3
"""
Fix affiliate links in the database by replacing placeholder tags with real ones.
"""

import sqlite3
import sys

def update_affiliate_links(real_affiliate_tag):
    """Update all routes in the database with the real affiliate tag"""
    
    if not real_affiliate_tag or real_affiliate_tag == "YOUR-AMAZON-ASSOCIATES-TAG":
        print("❌ Please provide your real Amazon Associates tag!")
        print("Usage: python fix_affiliate_links.py your-real-tag-20")
        return False
    
    try:
        conn = sqlite3.connect('affiliate.db')
        cursor = conn.cursor()
        
        # Update all routes
        cursor.execute('''
            UPDATE routes 
            SET dest_url = REPLACE(dest_url, 'YOUR-AMAZON-ASSOCIATES-TAG', ?)
        ''', (real_affiliate_tag,))
        
        affected_rows = cursor.rowcount
        conn.commit()
        
        print(f"✅ Updated {affected_rows} routes with affiliate tag: {real_affiliate_tag}")
        
        # Show updated routes
        cursor.execute('SELECT slug, offer, dest_url FROM routes')
        routes = cursor.fetchall()
        
        print("\n📋 Updated routes:")
        for slug, offer, dest_url in routes:
            print(f"  • {slug}: {offer}")
            print(f"    → {dest_url}")
            print()
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error updating routes: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("🔧 Fix Affiliate Links")
        print("=" * 50)
        print("This script updates your database routes with your real Amazon Associates tag.")
        print()
        print("Usage:")
        print("  python fix_affiliate_links.py your-real-tag-20")
        print()
        print("Example:")
        print("  python fix_affiliate_links.py ecopetguide-20")
        print()
        
        # Show current routes
        try:
            conn = sqlite3.connect('affiliate.db')
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM routes')
            count = cursor.fetchone()[0]
            print(f"📊 You currently have {count} routes that need updating.")
            conn.close()
        except:
            print("📊 Database not found or empty.")
        
        sys.exit(1)
    
    real_tag = sys.argv[1]
    success = update_affiliate_links(real_tag)
    
    if success:
        print("🎉 All done! Your product links should now work properly.")
        print("💡 Test by visiting: http://127.0.0.1:8088 and clicking on a product card.")
    else:
        print("❌ Something went wrong. Please check the error above.")
        sys.exit(1) 