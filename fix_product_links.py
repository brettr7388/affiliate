#!/usr/bin/env python3
"""
Fix product-specific affiliate links in config.yaml
"""

import yaml
import os
import re

def fix_config_yaml():
    """Update config.yaml with correct product-specific Amazon IDs"""
    
    # Read current config
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    # Define correct product mappings
    correct_products = {
        'AmazonEcoFriendlyDogToys': 'B093CLBJDW',  # Dog treats (for toy articles)
        'AmazonBiodegradablePoopBags': 'B07MYPFMZP',  # Poop bags
        'AmazonEcoFriendlyDogBeds': 'B00TQ47CPW',  # Dog beds
        'AmazonEcoFriendlyDogBowls': 'B08C342VQ6',  # Dog bowls (NEW)
        'AmazonOrganicDogTreats': 'B093CLBJDW'  # Organic treats (NEW)
    }
    
    # Update offers section
    for offer in config['offers']:
        if offer['name'] in correct_products:
            new_product_id = correct_products[offer['name']]
            old_url = offer['base_url']
            new_url = f'https://www.amazon.com/dp/{new_product_id}'
            offer['base_url'] = new_url
            print(f"✅ Updated {offer['name']}: {old_url} → {new_url}")
    
    # Add missing product categories
    existing_names = [offer['name'] for offer in config['offers']]
    
    if 'AmazonEcoFriendlyDogBowls' not in existing_names:
        config['offers'].append({
            'affiliate_id': 'test0b252-20',
            'affiliate_param': 'tag',
            'base_url': 'https://www.amazon.com/dp/B08C342VQ6',
            'name': 'AmazonEcoFriendlyDogBowls',
            'utm_campaign': 'launch',
            'utm_source': 'site'
        })
        print("✅ Added AmazonEcoFriendlyDogBowls (B08C342VQ6)")
    
    if 'AmazonOrganicDogTreats' not in existing_names:
        config['offers'].append({
            'affiliate_id': 'test0b252-20',
            'affiliate_param': 'tag',
            'base_url': 'https://www.amazon.com/dp/B093CLBJDW',
            'name': 'AmazonOrganicDogTreats',
            'utm_campaign': 'launch',
            'utm_source': 'site'
        })
        print("✅ Added AmazonOrganicDogTreats (B093CLBJDW)")
    
    # Write back to config
    with open('config.yaml', 'w') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)
    
    print("✅ Updated config.yaml with correct product-specific links")

def fix_bowl_article():
    """Fix the specific dog bowl article"""
    
    article_file = 'site/content/pawsitive-change-eco-friendly-dog-bowls-for-a-sustainable-pet-life.html'
    
    if os.path.exists(article_file):
        with open(article_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace dog treat links with dog bowl links in the bowl article
        content = re.sub(
            r'https://www\.amazon\.com/dp/B093CLBJDW\?tag=test0b252-20',
            'https://www.amazon.com/dp/B08C342VQ6?tag=test0b252-20',
            content
        )
        
        with open(article_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Fixed dog bowl article to use correct bowl links")
    else:
        print("⚠️  Dog bowl article not found")

def fix_treat_articles():
    """Ensure treat articles use the correct treat links"""
    
    treat_keywords = ['treat', 'organic', 'biscuit', 'snack']
    content_dir = 'site/content'
    
    for filename in os.listdir(content_dir):
        if filename.endswith('.html'):
            filepath = os.path.join(content_dir, filename)
            
            # Check if this is a treat-related article
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Skip bowl articles
            if 'bowl' in filename.lower():
                continue
                
            # Check if article mentions treats
            is_treat_article = any(keyword in content.lower() for keyword in treat_keywords)
            
            if is_treat_article:
                # Ensure it uses the correct treat link
                content = re.sub(
                    r'https://www\.amazon\.com/dp/B08C342VQ6\?tag=test0b252-20',
                    'https://www.amazon.com/dp/B093CLBJDW?tag=test0b252-20',
                    content
                )
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"✅ Ensured treat links in {filename}")

if __name__ == "__main__":
    print("🔧 Fixing product-specific affiliate links...")
    fix_config_yaml()
    fix_bowl_article()
    fix_treat_articles()
    print("🎉 Product-specific links have been fixed!")
    print("\nNext steps:")
    print("1. git add .")
    print("2. git commit -m 'Fix product-specific affiliate links'")
    print("3. git push origin master")
    print("4. Wait for Render to redeploy")
