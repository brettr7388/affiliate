#!/usr/bin/env python3
"""
Fix Amazon affiliate links in config.yaml and regenerate articles
"""

import yaml
import os
import re

def fix_config_yaml():
    """Update config.yaml with correct Amazon product IDs"""
    
    # Read current config
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    # Update the offers section with correct product IDs
    for offer in config['offers']:
        if offer['name'] == 'AmazonEcoFriendlyDogToys':
            # Change from B004A7X27M to B093CLBJDW (correct eco-friendly dog toys)
            offer['base_url'] = 'https://www.amazon.com/dp/B093CLBJDW'
            print(f"✅ Updated {offer['name']} to use B093CLBJDW")
    
    # Write back to config
    with open('config.yaml', 'w') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)
    
    print("✅ Updated config.yaml with correct affiliate links")

def fix_existing_articles():
    """Fix affiliate links in existing articles"""
    
    # Find all HTML and MD files in site/content
    content_dir = 'site/content'
    fixed_count = 0
    
    for filename in os.listdir(content_dir):
        if filename.endswith(('.html', '.md')):
            filepath = os.path.join(content_dir, filename)
            
            # Read file
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replace incorrect Amazon links
            old_content = content
            
            # Fix the main product link
            content = re.sub(
                r'https://www\.amazon\.com/dp/B004A7X27M\?tag=test0b252-20',
                'https://www.amazon.com/dp/B093CLBJDW?tag=test0b252-20',
                content
            )
            
            # Fix amazon.com links (without www)
            content = re.sub(
                r'https://amazon\.com/dp/B004A7X27M\?tag=test0b252-20',
                'https://www.amazon.com/dp/B093CLBJDW?tag=test0b252-20',
                content
            )
            
            # If content changed, write it back
            if content != old_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ Fixed affiliate links in {filename}")
                fixed_count += 1
    
    print(f"✅ Fixed affiliate links in {fixed_count} articles")

if __name__ == "__main__":
    print("🔧 Fixing Amazon affiliate links...")
    fix_config_yaml()
    fix_existing_articles()
    print("🎉 All affiliate links have been fixed!")
    print("\nNext steps:")
    print("1. git add .")
    print("2. git commit -m 'Fix Amazon affiliate links'")
    print("3. git push origin main")
    print("4. Wait for Render to redeploy")
