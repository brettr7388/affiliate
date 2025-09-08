#!/usr/bin/env python3
"""
Fix existing articles that are pointing to the wrong Amazon products.

This script analyzes article titles and updates their database routes 
to point to the correct Amazon products.
"""

import sqlite3
import yaml
import re
from urllib.parse import urlencode, urlparse, urlunparse, parse_qsl

def build_affiliate_url(base_url: str, param: str, affiliate_id: str, utm_params: dict) -> str:
    """Build affiliate URL with UTM parameters"""
    parsed = urlparse(base_url)
    query_params = parse_qsl(parsed.query)
    
    # Add affiliate parameter
    query_params.append((param, affiliate_id))
    
    # Add UTM parameters
    for key, value in utm_params.items():
        query_params.append((key, value))
    
    # Rebuild URL
    new_query = urlencode(query_params)
    return urlunparse(parsed._replace(query=new_query))

def select_best_offer_for_title(title, offers):
    """Select the most appropriate offer based on article title"""
    title_lower = title.lower()
    
    print(f"  🔍 Analyzing title: '{title}'")
    
    # Priority matching for specific products
    if any(keyword in title_lower for keyword in ['bed', 'sleep', 'comfort', 'orthopedic', 'sleepless']):
        # Look for dog bed offer
        for offer in offers:
            if 'bed' in offer.get('name', '').lower() or 'B00TQ47CPW' in offer.get('base_url', ''):
                print(f"  ✅ Matched to dog bed offer: {offer['name']}")
                return offer
    
    elif any(keyword in title_lower for keyword in ['poop bag', 'biodegradable', 'waste']):
        # Look for poop bags offer
        for offer in offers:
            if 'poop' in offer.get('name', '').lower() or 'bag' in offer.get('name', '').lower():
                print(f"  ✅ Matched to poop bags offer: {offer['name']}")
                return offer
    
    elif any(keyword in title_lower for keyword in ['toy', 'play', 'kong', 'west paw']):
        # Look for dog toys offer
        for offer in offers:
            if 'toy' in offer.get('name', '').lower() or 'B004A7X27M' in offer.get('base_url', ''):
                print(f"  ✅ Matched to dog toys offer: {offer['name']}")
                return offer
    
    # Default to first offer if no specific match
    print(f"  ⚠️  No specific match, using default: {offers[0]['name']}")
    return offers[0]

def get_article_title_from_slug(slug):
    """Convert slug back to readable title for analysis"""
    # Remove common suffixes
    title = slug.replace('-', ' ')
    title = re.sub(r'\d{4}$', '', title)  # Remove year
    title = re.sub(r'\s+', ' ', title).strip()
    return title.title()

def fix_article_offers():
    """Fix all articles to point to correct Amazon products"""
    print("🔧 FIXING ARTICLE OFFERS")
    print("=" * 50)
    
    # Load config
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    offers = config['offers']
    print(f"📦 Found {len(offers)} offers in config:")
    for offer in offers:
        print(f"  • {offer['name']}: {offer['base_url']}")
    
    # Connect to database
    conn = sqlite3.connect('affiliate.db')
    cursor = conn.cursor()
    
    # Get all routes
    cursor.execute('SELECT slug, offer, dest_url FROM routes ORDER BY slug')
    routes = cursor.fetchall()
    
    print(f"\n📊 Found {len(routes)} routes to analyze:")
    
    updates_made = 0
    
    for slug, current_offer, current_url in routes:
        print(f"\n📄 Route: {slug}")
        print(f"  Current offer: {current_offer}")
        print(f"  Current URL: {current_url}")
        
        # Get article title from slug for analysis
        title = get_article_title_from_slug(slug)
        
        # Find the best offer for this title
        best_offer = select_best_offer_for_title(title, offers)
        
        # Build the correct URL
        correct_url = build_affiliate_url(
            best_offer['base_url'],
            best_offer['affiliate_param'],
            best_offer['affiliate_id'],
            {'utm_source': 'site', 'utm_campaign': 'content'}
        )
        
        # Check if update is needed
        if current_url != correct_url or current_offer != best_offer['name']:
            print(f"  🔄 UPDATE NEEDED:")
            print(f"    New offer: {best_offer['name']}")
            print(f"    New URL: {correct_url}")
            
            # Update the route
            cursor.execute('''
                UPDATE routes 
                SET offer = ?, dest_url = ?
                WHERE slug = ?
            ''', (best_offer['name'], correct_url, slug))
            
            updates_made += 1
            print(f"  ✅ Updated!")
        else:
            print(f"  ✅ Already correct")
    
    # Commit changes
    conn.commit()
    conn.close()
    
    print(f"\n🎉 SUMMARY:")
    print(f"  📊 Total routes analyzed: {len(routes)}")
    print(f"  🔄 Routes updated: {updates_made}")
    print(f"  ✅ Routes already correct: {len(routes) - updates_made}")
    
    if updates_made > 0:
        print(f"\n🌐 All article links now point to the correct Amazon products!")
        print(f"💡 Test by visiting your articles and checking the affiliate links")
    else:
        print(f"\n✨ All articles were already pointing to the correct products!")

if __name__ == "__main__":
    fix_article_offers() 