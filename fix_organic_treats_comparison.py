#!/usr/bin/env python3
"""
Fix the organic dog treats comparison section to use correct Amazon links
"""

import yaml
import os

def fix_organic_treats_comparison():
    """Update the organic dog treats comparison to use direct Amazon links"""
    
    # Read current config
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    # Find the organic dog treats comparison section
    if 'content' in config and 'product_comparisons' in config['content']:
        for comparison in config['content']['product_comparisons']:
            if comparison['title'] == "🍌 Best Organic Dog Treats":
                print("✅ Found organic dog treats comparison section")
                
                # Update all products to use the correct Amazon link
                for product in comparison['products']:
                    # Remove route_slug and add direct Amazon link
                    if 'route_slug' in product:
                        del product['route_slug']
                    
                    # Add the correct Amazon affiliate link
                    product['link'] = 'https://www.amazon.com/dp/B093CLBJDW?tag=test0b252-20&th=1'
                    
                    print(f"✅ Updated {product['name']} to use correct Amazon link")
    else:
        print("❌ product_comparisons section not found in config")
        return
    
    # Write back to config
    with open('config.yaml', 'w') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)
    
    print("✅ Updated organic dog treats comparison with correct Amazon links")

if __name__ == "__main__":
    print("🔧 Fixing organic dog treats comparison section...")
    fix_organic_treats_comparison()
    print("🎉 Organic dog treats comparison fixed!")
    print("\nNext steps:")
    print("1. git add .")
    print("2. git commit -m 'Fix organic dog treats comparison links'")
    print("3. git push origin master")
    print("4. Wait for Render to redeploy")
