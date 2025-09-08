#!/usr/bin/env python3
"""
Verify all article links are pointing to correct products
"""

import os
import re
import glob

def check_article_links():
    print("🔍 Verifying Article Affiliate Links...")
    print("=" * 60)
    
    # Check HTML files
    html_files = glob.glob("site/content/*.html")
    
    poop_articles = []
    toy_articles = []
    other_articles = []
    
    for filepath in html_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract title
            title_match = re.search(r'<title>(.*?) - Eco Pet Guide</title>', content)
            title = title_match.group(1) if title_match else os.path.basename(filepath)
            
            # Find Amazon links
            amazon_links = re.findall(r'https://amazon\.com/dp/([A-Z0-9]+)', content)
            
            if amazon_links:
                product_id = amazon_links[0]  # Take first link
                
                if 'poop' in title.lower() or 'biodegradable' in title.lower():
                    expected_id = 'B07MYPFMZP'  # PLANET POOP
                    status = "✅" if product_id == expected_id else "❌"
                    poop_articles.append((title, product_id, expected_id, status))
                
                elif 'toy' in title.lower() or 'kong' in title.lower() or 'west paw' in title.lower():
                    expected_id = 'B004A7X27M'  # West Paw Hurley
                    status = "✅" if product_id == expected_id else "❌"
                    toy_articles.append((title, product_id, expected_id, status))
                
                else:
                    other_articles.append((title, product_id))
                    
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
    
    # Display results
    print("🛒 POOP BAG ARTICLES:")
    print("-" * 40)
    for title, actual, expected, status in poop_articles:
        print(f"{status} {title}")
        print(f"   Actual: {actual} | Expected: {expected}")
        if actual == expected:
            print(f"   ✅ Links to PLANET POOP correctly!")
        else:
            print(f"   ❌ Should link to PLANET POOP (B07MYPFMZP)")
        print()
    
    print("🎾 TOY ARTICLES:")
    print("-" * 40)
    for title, actual, expected, status in toy_articles:
        print(f"{status} {title}")
        print(f"   Actual: {actual} | Expected: {expected}")
        if actual == expected:
            print(f"   ✅ Links to West Paw Hurley correctly!")
        else:
            print(f"   ❌ Should link to West Paw Hurley (B004A7X27M)")
        print()
    
    if other_articles:
        print("🔧 OTHER ARTICLES:")
        print("-" * 40)
        for title, product_id in other_articles:
            print(f"• {title}")
            print(f"   Product: {product_id}")
            print()
    
    # Summary
    total_poop = len(poop_articles)
    correct_poop = sum(1 for _, actual, expected, _ in poop_articles if actual == expected)
    
    total_toy = len(toy_articles)
    correct_toy = sum(1 for _, actual, expected, _ in toy_articles if actual == expected)
    
    print("📊 SUMMARY:")
    print("=" * 30)
    print(f"Poop Bag Articles: {correct_poop}/{total_poop} correct")
    print(f"Toy Articles: {correct_toy}/{total_toy} correct")
    print(f"Other Articles: {len(other_articles)}")
    
    total_articles = total_poop + total_toy
    total_correct = correct_poop + correct_toy
    
    if total_correct == total_articles:
        print(f"\n🎉 ALL ARTICLES HAVE CORRECT LINKS! ({total_correct}/{total_articles})")
    else:
        print(f"\n⚠️  {total_articles - total_correct} articles need fixing")
    
    print("\n🔗 Product Mapping:")
    print("• Poop Bag articles → PLANET POOP (B07MYPFMZP)")
    print("• Dog Toy articles → West Paw Hurley (B004A7X27M)")

if __name__ == "__main__":
    check_article_links() 