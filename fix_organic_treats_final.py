#!/usr/bin/env python3
"""
Final fix for organic dog treats comparison section
"""

import yaml
import os

def fix_organic_treats_comparison():
    """Ensure organic dog treats comparison uses correct Amazon links"""
    
    # Read current config
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    # Find and fix the organic dog treats comparison
    if 'content' in config and 'product_comparisons' in config['content']:
        for comparison in config['content']['product_comparisons']:
            if comparison['title'] == "🍌 Best Organic Dog Treats":
                print("✅ Found organic dog treats comparison section")
                
                # Ensure all products use the correct Amazon link
                for product in comparison['products']:
                    # Force the correct Amazon link
                    product['link'] = 'https://www.amazon.com/dp/B093CLBJDW?tag=test0b252-20'
                    
                    # Remove any route_slug that might be interfering
                    if 'route_slug' in product:
                        del product['route_slug']
                    
                    print(f"✅ Updated {product['name']} to use B093CLBJDW (dog treats)")
    
    # Write back to config
    with open('config.yaml', 'w') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)
    
    print("✅ Organic dog treats comparison now uses correct Amazon links")

if __name__ == "__main__":
    print("🔧 Final fix for organic dog treats comparison...")
    fix_organic_treats_comparison()
    print("🎉 Organic dog treats comparison fixed!")
    print("\nNext steps:")
    print("1. git add .")
    print("2. git commit -m 'Final fix: organic dog treats comparison links'")
    print("3. git push origin master")
    print("4. Wait for Render to redeploy")
