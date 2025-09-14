#!/usr/bin/env python3
"""
Fix the app.py file structure for article hero images
"""

def fix_app_py():
    with open('app.py', 'r') as f:
        content = f.read()
    
    # Find and replace the problematic section
    old_section = '''        return Article(
            slug=slug,
            title=title,
        excerpt=excerpt,
        # Determine article category for rotating images
        article_category = detect_article_category(title, slug)
        heroImage=f"/images/rotating/{article_category}/{article_category}1.png",  # Rotating image system
            tags=tags,
            publishedAt=published_at,
            estimatedReadMin=read_min
        )'''
    
    new_section = '''        # Determine article category for rotating images
        article_category = detect_article_category(title, slug)
        
        return Article(
            slug=slug,
            title=title,
            excerpt=excerpt,
            heroImage=f"/images/rotating/{article_category}/{article_category}1.png",  # Rotating image system
            tags=tags,
            publishedAt=published_at,
            estimatedReadMin=read_min
        )'''
    
    updated_content = content.replace(old_section, new_section)
    
    with open('app.py', 'w') as f:
        f.write(updated_content)
    
    print("✅ Fixed app.py structure!")

if __name__ == "__main__":
    fix_app_py()
