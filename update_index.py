#!/usr/bin/env python3
"""
Automatically update the index.html file to include all articles
"""

import os
import glob
import re
from pathlib import Path

def extract_title_from_html(html_file):
    """Extract title from HTML file"""
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # Look for h1 tag (first one)
            h1_matches = re.findall(r'<h1[^>]*>(.*?)</h1>', content, re.IGNORECASE | re.DOTALL)
            if h1_matches:
                return h1_matches[0].strip()
            # Look for title tag
            title_match = re.search(r'<title[^>]*>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
            if title_match:
                return title_match.group(1).strip()
    except Exception as e:
        print(f"Error reading {html_file}: {e}")
    
    # Fallback: use filename
    filename = Path(html_file).stem
    return filename.replace('-', ' ').replace('_', ' ').title()

def update_index():
    """Update index.html with all articles"""
    
    # Get all HTML files in content directory
    content_dir = Path("site/content")
    html_files = list(content_dir.glob("*.html"))
    
    # Sort by modification time (newest first)
    html_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    
    # Generate article list
    article_links = []
    for html_file in html_files:
        filename = html_file.name
        title = extract_title_from_html(html_file)
        article_links.append(f'        <li><a href="content/{filename}">{title}</a></li>')
    
    # Read current index.html
    index_file = Path("site/index.html")
    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace the article list
    start_marker = '    <h2>Latest posts</h2>\n    <ul>'
    end_marker = '      </ul>\n      '
    
    start_pos = content.find(start_marker)
    end_pos = content.find(end_marker)
    
    if start_pos != -1 and end_pos != -1:
        new_content = content[:start_pos + len(start_marker)] + '\n' + '\n'.join(article_links) + '\n' + content[end_pos:]
        
        # Write updated content
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ Updated index.html with {len(article_links)} articles")
        print("📝 Articles included:")
        for link in article_links:
            print(f"   - {link.split('>')[1].split('<')[0]}")
    else:
        print("❌ Could not find article list markers in index.html")

if __name__ == "__main__":
    update_index() 