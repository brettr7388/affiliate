#!/usr/bin/env python3
"""
Fix dog toy articles to link to the correct West Paw dog toy product
"""

import yaml
import os
import re

def fix_config_yaml():
    """Update config.yaml to use correct dog toy product for toy articles"""
    
    # Read current config
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    # Update the AmazonEcoFriendlyDogToys to use the correct dog toy product
    for offer in config['offers']:
        if offer['name'] == 'AmazonEcoFriendlyDogToys':
            # Change from B093CLBJDW (treats) to B004A7X27M (West Paw dog toy)
            offer['base_url'] = 'https://www.amazon.com/dp/B004A7X27M'
            print(f"✅ Updated {offer['name']} to use B004A7X27M (West Paw dog toy)")
    
    # Write back to config
    with open('config.yaml', 'w') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)
    
    print("✅ Updated config.yaml with correct dog toy product")

def fix_existing_toy_articles():
    """Fix affiliate links in existing dog toy articles"""
    
    # Find all HTML and MD files in site/content
    content_dir = 'site/content'
    fixed_count = 0
    
    # Keywords that indicate dog toy articles
    toy_keywords = ['toy', 'play', 'fetch', 'chew', 'bone', 'ball', 'interactive']
    
    for filename in os.listdir(content_dir):
        if filename.endswith(('.html', '.md')):
            filepath = os.path.join(content_dir, filename)
            
            # Read file
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if this is a dog toy article
            is_toy_article = any(keyword in content.lower() for keyword in toy_keywords)
            
            # Also check filename for toy indicators
            filename_lower = filename.lower()
            is_toy_filename = any(keyword in filename_lower for keyword in ['toy', 'play', 'fetch'])
            
            # Skip bowl and treat articles
            if 'bowl' in filename_lower or 'treat' in filename_lower or 'poop' in filename_lower:
                continue
            
            if is_toy_article or is_toy_filename:
                old_content = content
                
                # Replace treat links with dog toy links
                content = re.sub(
                    r'https://www\.amazon\.com/dp/B093CLBJDW\?tag=test0b252-20',
                    'https://www.amazon.com/dp/B004A7X27M?tag=test0b252-20',
                    content
                )
                
                # Fix amazon.com links (without www)
                content = re.sub(
                    r'https://amazon\.com/dp/B093CLBJDW\?tag=test0b252-20',
                    'https://www.amazon.com/dp/B004A7X27M?tag=test0b252-20',
                    content
                )
                
                # If content changed, write it back
                if content != old_content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"✅ Fixed dog toy links in {filename}")
                    fixed_count += 1
    
    print(f"✅ Fixed dog toy links in {fixed_count} articles")

def fix_new_article():
    """Fix the specific new article that was just generated"""
    
    article_file = 'site/content/pawsitive-play-the-best-eco-friendly-dog-toys-of-2025-for-first-time-owners.html'
    
    if os.path.exists(article_file):
        with open(article_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace treat links with dog toy links
        content = re.sub(
            r'https://www\.amazon\.com/dp/B093CLBJDW\?tag=test0b252-20',
            'https://www.amazon.com/dp/B004A7X27M?tag=test0b252-20',
            content
        )
        
        with open(article_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Fixed the new dog toy article to use correct toy links")
    else:
        print("⚠️  New dog toy article not found yet")

if __name__ == "__main__":
    print("🔧 Fixing dog toy articles to use correct West Paw product...")
    fix_config_yaml()
    fix_existing_toy_articles()
    fix_new_article()
    print("🎉 All dog toy articles now link to correct West Paw product!")
    print("\nNext steps:")
    print("1. git add .")
    print("2. git commit -m 'Fix dog toy articles to use correct West Paw product'")
    print("3. git push origin master")
    print("4. Wait for Render to redeploy")
