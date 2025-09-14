#!/usr/bin/env python3
"""
Fix image paths in rotation script for homepage
"""

def fix_image_paths():
    with open('site/js/image-rotation.js', 'r') as f:
        content = f.read()
    
    # Fix relative paths to absolute paths for homepage
    content = content.replace('../images/rotating/', '/images/rotating/')
    
    with open('site/js/image-rotation.js', 'w') as f:
        f.write(content)
    
    print("✅ Fixed image paths in rotation script!")

if __name__ == "__main__":
    fix_image_paths()
