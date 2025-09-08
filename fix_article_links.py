#!/usr/bin/env python3
"""
Fix article affiliate links to point to correct products
This script analyzes each article's content and updates the affiliate links to match the correct products
"""

import os
import re
import glob
from typing import Dict, List, Tuple

# Product URL mappings based on your current affiliate products
PRODUCT_MAPPINGS = {
    # Poop bag articles should link to PLANET POOP
    'poop': 'https://amazon.com/dp/B07MYPFMZP?tag=test0b252-20',
    'biodegradable': 'https://amazon.com/dp/B07MYPFMZP?tag=test0b252-20',
    
    # Dog toy articles should link to West Paw Hurley
    'toy': 'https://amazon.com/dp/B004A7X27M?tag=test0b252-20',
    'west paw': 'https://amazon.com/dp/B004A7X27M?tag=test0b252-20',
    'kong': 'https://amazon.com/dp/B004A7X27M?tag=test0b252-20',
    
    # Hemp leash articles should link to Good Dog Company
    'leash': 'https://amazon.com/dp/B00C9L67XW?tag=test0b252-20',
    'hemp': 'https://amazon.com/dp/B00C9L67XW?tag=test0b252-20',
    
    # Dog treat articles should link to WAG Expedition
    'treat': 'https://amazon.com/dp/B093CLBJDW?tag=test0b252-20',
    'organic': 'https://amazon.com/dp/B093CLBJDW?tag=test0b252-20',
    
    # Dog bed articles should link to PetFusion
    'bed': 'https://amazon.com/dp/B00TQ47CPW?tag=test0b252-20',
    'recycled': 'https://amazon.com/dp/B00TQ47CPW?tag=test0b252-20',
    
    # Dog bowl articles should link to Beco Bamboo
    'bowl': 'https://amazon.com/dp/B08C342VQ6?tag=test0b252-20',
    'bamboo': 'https://amazon.com/dp/B08C342VQ6?tag=test0b252-20',
    'sustainable': 'https://amazon.com/dp/B08C342VQ6?tag=test0b252-20'
}

def detect_article_type(title: str, content: str) -> str:
    """Detect what type of product this article is about"""
    title_lower = title.lower()
    content_lower = content.lower()
    
    # Check for poop bags first (most specific)
    if any(keyword in title_lower for keyword in ['poop', 'biodegradable', 'compostable']):
        return 'poop'
    
    # Check for leashes
    if any(keyword in title_lower for keyword in ['leash', 'hemp', 'collar']):
        return 'leash'
    
    # Check for beds
    if any(keyword in title_lower for keyword in ['bed', 'recycled', 'comfort']):
        return 'bed'
    
    # Check for bowls
    if any(keyword in title_lower for keyword in ['bowl', 'bamboo', 'feeding']):
        return 'bowl'
    
    # Check for treats
    if any(keyword in title_lower for keyword in ['treat', 'organic', 'snack']):
        return 'treat'
    
    # Check for toys (do this last as it's most common)
    if any(keyword in title_lower for keyword in ['toy', 'west paw', 'kong', 'chew', 'play']):
        return 'toy'
    
    # Default to toys if we can't determine
    return 'toy'

def get_correct_product_url(article_type: str) -> str:
    """Get the correct product URL for an article type"""
    return PRODUCT_MAPPINGS.get(article_type, PRODUCT_MAPPINGS['toy'])

def update_html_file(filepath: str) -> bool:
    """Update affiliate links in an HTML file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Extract title from HTML
        title_match = re.search(r'<title>(.*?) - Eco Pet Guide</title>', content)
        title = title_match.group(1) if title_match else os.path.basename(filepath)
        
        # Detect article type
        article_type = detect_article_type(title, content)
        correct_url = get_correct_product_url(article_type)
        
        # Replace all Amazon affiliate links with the correct one
        # Pattern matches various Amazon URL formats
        amazon_pattern = r'https?://(?:www\.)?amazon\.com/dp/[A-Z0-9]+(?:\?[^"\']*)?'
        content = re.sub(amazon_pattern, correct_url, content)
        
        # Also replace any /r/ internal redirect links if they exist
        internal_redirect_pattern = r'href="/r/[^"]*"'
        
        # Map to appropriate internal redirect based on article type
        redirect_mapping = {
            'poop': 'href="/r/biodegradable-poop-bags"',
            'toy': 'href="/r/eco-dog-toys-2025"',
            'leash': 'href="/r/hemp-dog-leash"',
            'treat': 'href="/r/organic-dog-treats"',
            'bed': 'href="/r/recycled-dog-bed"',
            'bowl': 'href="/r/sustainable-dog-bowls"'
        }
        
        if article_type in redirect_mapping:
            content = re.sub(internal_redirect_pattern, redirect_mapping[article_type], content)
        
        # Write back if changed
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
        
    except Exception as e:
        print(f"Error updating {filepath}: {e}")
        return False

def update_markdown_file(filepath: str) -> bool:
    """Update affiliate links in a Markdown file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Extract title from markdown
        title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else os.path.basename(filepath)
        
        # Detect article type
        article_type = detect_article_type(title, content)
        correct_url = get_correct_product_url(article_type)
        
        # Replace all Amazon affiliate links with the correct one
        amazon_pattern = r'https?://(?:www\.)?amazon\.com/dp/[A-Z0-9]+(?:\?[^)]*)?'
        content = re.sub(amazon_pattern, correct_url, content)
        
        # Write back if changed
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
        
    except Exception as e:
        print(f"Error updating {filepath}: {e}")
        return False

def main():
    print("🔗 Fixing Article Affiliate Links...")
    print("=" * 50)
    
    updated_files = []
    
    # Update HTML files
    html_files = glob.glob("site/content/*.html")
    for filepath in html_files:
        if update_html_file(filepath):
            filename = os.path.basename(filepath)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            title_match = re.search(r'<title>(.*?) - Eco Pet Guide</title>', content)
            title = title_match.group(1) if title_match else filename
            article_type = detect_article_type(title, content)
            correct_url = get_correct_product_url(article_type)
            
            print(f"✅ Updated HTML: {filename}")
            print(f"   Title: {title}")
            print(f"   Type: {article_type}")
            print(f"   URL: {correct_url}")
            print()
            updated_files.append(filepath)
    
    # Update Markdown files
    md_files = glob.glob("site/content/*.md")
    for filepath in md_files:
        if update_markdown_file(filepath):
            filename = os.path.basename(filepath)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
            title = title_match.group(1) if title_match else filename
            article_type = detect_article_type(title, content)
            correct_url = get_correct_product_url(article_type)
            
            print(f"✅ Updated MD: {filename}")
            print(f"   Title: {title}")
            print(f"   Type: {article_type}")
            print(f"   URL: {correct_url}")
            print()
            updated_files.append(filepath)
    
    print("🎉 Article Link Fix Complete!")
    print(f"📊 Updated {len(updated_files)} files")
    
    if updated_files:
        print("\n📝 Summary of Changes:")
        print("• Poop bag articles → PLANET POOP (B07MYPFMZP)")
        print("• Dog toy articles → West Paw Hurley (B004A7X27M)")
        print("• Leash articles → Good Dog Company (B00C9L67XW)")
        print("• Treat articles → WAG Expedition (B093CLBJDW)")
        print("• Bed articles → PetFusion (B00TQ47CPW)")
        print("• Bowl articles → Beco Bamboo (B08C342VQ6)")
    else:
        print("\n✅ All articles already have correct links!")
    
    print("\n🔗 All articles now link to the correct products!")

if __name__ == "__main__":
    main() 