#!/usr/bin/env python3
"""
Fix all articles that have generic/wrong affiliate links by regenerating them
with the correct smart offer selection.
"""

import os
import re
from content_pipeline import generate_post

def extract_article_content(filepath):
    """Extract title and body from markdown file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        
        # Find title
        title_line = None
        for line in lines:
            if line.startswith('# '):
                title_line = line.replace('# ', '').strip()
                break
        
        if not title_line:
            return None, None
        
        # Find body content (skip title, disclosure, and footer)
        body_lines = []
        in_body = False
        
        for line in lines:
            # Skip title, disclosure, and metadata
            if line.startswith('# ') or line.startswith('> ') or line.startswith('**Try this:**') or line.startswith('*We might'):
                continue
            if line.startswith('---'):
                if in_body:
                    break  # End of body
                else:
                    in_body = True  # Start of body
                    continue
            
            if in_body and line.strip():
                body_lines.append(line)
        
        if not body_lines:
            # Try alternative approach - get everything between title and footer
            body_lines = []
            found_title = False
            for line in lines:
                if line.startswith('# '):
                    found_title = True
                    continue
                if found_title and line.startswith('---'):
                    break
                if found_title and not line.startswith('> '):
                    body_lines.append(line)
        
        body_md = '\n'.join(body_lines).strip()
        return title_line, body_md
    
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None, None

def fix_article(md_filepath):
    """Fix a single article by regenerating it"""
    print(f"\n📄 Processing: {os.path.basename(md_filepath)}")
    
    title, body_md = extract_article_content(md_filepath)
    
    if not title or not body_md:
        print(f"  ❌ Could not extract content")
        return False
    
    print(f"  📝 Title: {title}")
    print(f"  📄 Body length: {len(body_md)} chars")
    
    # Regenerate with smart offer selection
    try:
        slug = generate_post(title=title, body_md=body_md)
        print(f"  ✅ Regenerated with slug: {slug}")
        return True
    except Exception as e:
        print(f"  ❌ Error regenerating: {e}")
        return False

def main():
    """Fix all articles with wrong affiliate links"""
    print("🔧 FIXING ALL ARTICLES WITH WRONG LINKS")
    print("=" * 60)
    
    # Articles that need fixing based on the grep results
    problem_articles = [
        'pawsitive-poop-your-guide-to-eco-friendly-dog-waste-disposal-with-planet-poop-home-compostable-bags',
        'snuggle-up-sustainably-introducing-the-petfusion-ultimate-dog-bed-lounge-a-first-timer-s-guide-to-eco-friendly-comfort', 
        'nourish-your-pup-nurture-the-planet-a-guide-to-using-the-beco-pets-bamboo-dog-bowl',
        'low-waste-dog-starter-kit-9-sustainable-essentials'
    ]
    
    fixed_count = 0
    total_count = len(problem_articles)
    
    for article_slug in problem_articles:
        md_path = f'site/content/{article_slug}.md'
        
        if os.path.exists(md_path):
            if fix_article(md_path):
                fixed_count += 1
        else:
            print(f"\n❌ Markdown file not found: {md_path}")
    
    print(f"\n🎉 SUMMARY:")
    print(f"  📊 Total articles processed: {total_count}")
    print(f"  ✅ Articles fixed: {fixed_count}")
    print(f"  ❌ Articles failed: {total_count - fixed_count}")
    
    if fixed_count > 0:
        print(f"\n🌐 All fixed articles now have the correct product links!")
        print(f"💡 Check your articles - they should now link to the right Amazon products")

if __name__ == "__main__":
    main() 