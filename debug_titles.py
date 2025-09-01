#!/usr/bin/env python3
"""
Debug script to see what titles are being extracted
"""

import re
from pathlib import Path

def extract_title_from_html(html_file):
    """Extract title from HTML file"""
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
            print(f"\n--- {html_file} ---")
            print(f"Content length: {len(content)}")
            print(f"First 200 chars: {content[:200]}")
            
            # Look for h1 tag (first one)
            h1_matches = re.findall(r'<h1[^>]*>(.*?)</h1>', content, re.IGNORECASE | re.DOTALL)
            print(f"H1 matches found: {len(h1_matches)}")
            if h1_matches:
                title = h1_matches[0].strip()
                print(f"Title: '{title}'")
                return title
            else:
                print("No H1 tags found")
            
            # Look for title tag
            title_match = re.search(r'<title[^>]*>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
            if title_match:
                title = title_match.group(1).strip()
                print(f"Title from title tag: '{title}'")
                return title
            else:
                print("No title tag found")
                
    except Exception as e:
        print(f"Error reading {html_file}: {e}")
    
    # Fallback: use filename
    filename = Path(html_file).stem
    title = filename.replace('-', ' ').replace('_', ' ').title()
    print(f"Fallback title: '{title}'")
    return title

# Test with one file
content_dir = Path("site/content")
html_files = list(content_dir.glob("*.html"))
if html_files:
    extract_title_from_html(html_files[0]) 