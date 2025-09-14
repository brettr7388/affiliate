#!/usr/bin/env python3
"""
Update articles with image rotation system
Adds rotating product images to all articles based on their content
"""

import os
import re
from pathlib import Path

def detect_product_category(title, content):
    """Detect the main product category from article title and content"""
    title_lower = title.lower()
    content_lower = content.lower()
    
    # Check for specific product categories
    if any(keyword in title_lower for keyword in ['toy', 'play', 'kong', 'west paw']):
        return 'toy'
    elif any(keyword in title_lower for keyword in ['poop bag', 'biodegradable', 'waste', 'bag']):
        return 'bag'
    elif any(keyword in title_lower for keyword in ['bowl', 'feeding', 'dish']):
        return 'bowl'
    elif any(keyword in title_lower for keyword in ['leash', 'walking', 'lead']):
        return 'leash'
    elif any(keyword in title_lower for keyword in ['bed', 'sleep', 'comfort', 'orthopedic']):
        return 'bed'
    elif any(keyword in title_lower for keyword in ['treat', 'snack', 'food']):
        return 'treat'
    else:
        return 'all'  # Default for general articles

def add_image_rotation_to_html(html_content, category):
    """Add image rotation elements to HTML content"""
    
    # Add the image rotation script
    script_tag = '<script src="../js/image-rotation.js"></script>'
    
    # Add a hero image section with rotation
    hero_section = f'''
    <div class="hero-image-section" data-hero-category="{category}" style="text-align: center; margin: 2rem 0;">
        <img src="../images/rotating/{category}/{category}1.png" 
             alt="Eco-friendly {category} product" 
             style="max-width: 100%; height: auto; border-radius: 12px; box-shadow: 0 8px 25px rgba(0,0,0,0.1);">
    </div>
    '''
    
    # Add product showcase section
    product_section = f'''
    <div class="product-showcase" data-product-category="{category}" style="text-align: center; margin: 2rem 0; padding: 2rem; background: linear-gradient(135deg, #f8f9fa, #e9ecef); border-radius: 12px;">
        <h3 style="color: #28a745; margin-bottom: 1rem;">🌟 Featured Eco-Friendly {category.title()} Product</h3>
        <img src="../images/rotating/{category}/{category}1.png" 
             alt="Eco-friendly {category} product showcase" 
             style="max-width: 300px; height: auto; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
    </div>
    '''
    
    # Insert the script before closing body tag
    if '</body>' in html_content:
        html_content = html_content.replace('</body>', f'{script_tag}\n</body>')
    else:
        html_content += f'\n{script_tag}'
    
    # Insert hero section after the main article tag starts
    if '<article class="article-content">' in html_content:
        html_content = html_content.replace(
            '<article class="article-content">',
            f'<article class="article-content">\n{hero_section}'
        )
    elif '<main>' in html_content:
        html_content = html_content.replace(
            '<main>',
            f'<main>\n{hero_section}'
        )
    
    # Insert product showcase before CTA section
    if '<div class="cta-section">' in html_content:
        html_content = html_content.replace(
            '<div class="cta-section">',
            f'{product_section}\n<div class="cta-section">'
        )
    
    return html_content

def update_article_file(file_path):
    """Update a single article file with image rotation"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract title from HTML
        title_match = re.search(r'<title>(.*?)</title>', content)
        title = title_match.group(1) if title_match else ""
        
        # Detect product category
        category = detect_product_category(title, content)
        
        # Add image rotation elements
        updated_content = add_image_rotation_to_html(content, category)
        
        # Write back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print(f"✅ Updated {file_path.name} with {category} category")
        return True
        
    except Exception as e:
        print(f"❌ Error updating {file_path.name}: {e}")
        return False

def main():
    """Update all article HTML files with image rotation"""
    content_dir = Path("site/content")
    
    if not content_dir.exists():
        print("❌ Content directory not found!")
        return
    
    html_files = list(content_dir.glob("*.html"))
    
    if not html_files:
        print("❌ No HTML files found in content directory!")
        return
    
    print(f"🔄 Found {len(html_files)} HTML files to update...")
    
    updated_count = 0
    for html_file in html_files:
        if update_article_file(html_file):
            updated_count += 1
    
    print(f"\n✅ Successfully updated {updated_count}/{len(html_files)} articles!")
    print("\n📁 Image structure created:")
    print("   site/images/rotating/")
    print("   ├── toy/ (4 images)")
    print("   ├── bag/ (3 images)")
    print("   ├── bowl/ (3 images)")
    print("   ├── leash/ (3 images)")
    print("   ├── bed/ (3 images)")
    print("   ├── treat/ (3 images)")
    print("   └── all/ (3 images)")
    print("\n🎯 Next steps:")
    print("   1. Copy your generated images to the appropriate category folders")
    print("   2. Name them: category1.png, category2.png, etc.")
    print("   3. Images will rotate automatically on page refresh!")

if __name__ == "__main__":
    main()
