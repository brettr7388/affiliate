#!/usr/bin/env python3
"""
Update article hero images to use rotating image system
"""

import re
import os

def detect_article_category(title, slug):
    """Detect the main product category from article title and slug"""
    title_lower = title.lower()
    slug_lower = slug.lower()
    
    # Check for specific product categories
    if any(keyword in title_lower for keyword in ['toy', 'play', 'kong', 'west paw']) or 'toy' in slug_lower:
        return 'toy'
    elif any(keyword in title_lower for keyword in ['poop bag', 'biodegradable', 'waste', 'bag']) or 'bag' in slug_lower:
        return 'bag'
    elif any(keyword in title_lower for keyword in ['bowl', 'feeding', 'dish']) or 'bowl' in slug_lower:
        return 'bowl'
    elif any(keyword in title_lower for keyword in ['leash', 'walking', 'lead']) or 'leash' in slug_lower:
        return 'leash'
    elif any(keyword in title_lower for keyword in ['bed', 'sleep', 'comfort', 'orthopedic']) or 'bed' in slug_lower:
        return 'bed'
    elif any(keyword in title_lower for keyword in ['treat', 'snack', 'food']) or 'treat' in slug_lower:
        return 'treat'
    else:
        return 'all'  # Default for general articles

def update_app_py():
    """Update app.py to use rotating images for articles"""
    
    # Read the current app.py
    with open('app.py', 'r') as f:
        content = f.read()
    
    # Find the parse_markdown_file function and update the heroImage line
    old_hero_line = 'heroImage=f"/images/library/hero-{slug}.jpg",  # Default hero image path'
    
    new_hero_logic = '''        # Determine article category for rotating images
        article_category = detect_article_category(title, slug)
        heroImage=f"/images/rotating/{article_category}/{article_category}1.png",  # Rotating image system'''
    
    # Replace the heroImage line
    updated_content = content.replace(old_hero_line, new_hero_logic)
    
    # Add the detect_article_category function before parse_markdown_file
    function_to_add = '''
def detect_article_category(title, slug):
    """Detect the main product category from article title and slug"""
    title_lower = title.lower()
    slug_lower = slug.lower()
    
    # Check for specific product categories
    if any(keyword in title_lower for keyword in ['toy', 'play', 'kong', 'west paw']) or 'toy' in slug_lower:
        return 'toy'
    elif any(keyword in title_lower for keyword in ['poop bag', 'biodegradable', 'waste', 'bag']) or 'bag' in slug_lower:
        return 'bag'
    elif any(keyword in title_lower for keyword in ['bowl', 'feeding', 'dish']) or 'bowl' in slug_lower:
        return 'bowl'
    elif any(keyword in title_lower for keyword in ['leash', 'walking', 'lead']) or 'leash' in slug_lower:
        return 'leash'
    elif any(keyword in title_lower for keyword in ['bed', 'sleep', 'comfort', 'orthopedic']) or 'bed' in slug_lower:
        return 'bed'
    elif any(keyword in title_lower for keyword in ['treat', 'snack', 'food']) or 'treat' in slug_lower:
        return 'treat'
    else:
        return 'all'  # Default for general articles

'''
    
    # Insert the function before parse_markdown_file
    insert_point = content.find('def parse_markdown_file(filepath: str) -> Optional[Article]:')
    updated_content = updated_content[:insert_point] + function_to_add + updated_content[insert_point:]
    
    # Write the updated content back
    with open('app.py', 'w') as f:
        f.write(updated_content)
    
    print("✅ Updated app.py to use rotating images for articles!")

if __name__ == "__main__":
    update_app_py()
