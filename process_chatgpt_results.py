#!/usr/bin/env python3
"""
Process ChatGPT Product Research Results
=======================================

This script processes the results from ChatGPT product research
and automatically updates the config.yaml file with new products.
"""

import yaml
import re
import sys
from datetime import datetime

def parse_chatgpt_results(results_text):
    """Parse ChatGPT results and extract product information"""
    
    products = []
    
    # Split by product blocks (look for ASIN pattern)
    product_blocks = re.split(r'ASIN:\s*B[A-Z0-9]{9}', results_text)
    
    for i, block in enumerate(product_blocks[1:], 1):  # Skip first empty block
        try:
            # Extract ASIN from the split
            asin_match = re.search(r'B[A-Z0-9]{9}', results_text)
            if asin_match:
                asin = asin_match.group()
            else:
                continue
                
            # Extract product name
            name_match = re.search(r'Product Name:\s*(.+)', block)
            product_name = name_match.group(1).strip() if name_match else f"Product {i}"
            
            # Extract price
            price_match = re.search(r'Price:\s*\$([0-9-]+)', block)
            price = price_match.group(1) if price_match else "N/A"
            
            # Extract eco features
            eco_match = re.search(r'Eco Features:\s*(.+)', block)
            eco_features = eco_match.group(1).strip() if eco_match else "Eco-friendly"
            
            # Extract category
            category_match = re.search(r'Category:\s*(.+)', block)
            category = category_match.group(1).strip() if category_match else "General"
            
            # Create product entry
            product = {
                'asin': asin,
                'name': product_name,
                'price': price,
                'eco_features': eco_features,
                'category': category,
                'amazon_url': f"https://www.amazon.com/dp/{asin}?tag=YOUR-AFFILIATE-TAG"
            }
            
            products.append(product)
            
        except Exception as e:
            print(f"Error parsing product {i}: {e}")
            continue
    
    return products

def create_offer_entry(product):
    """Create a config.yaml offer entry for a product"""
    
    # Create a clean name for the offer
    clean_name = re.sub(r'[^a-zA-Z0-9\s]', '', product['name'])
    clean_name = re.sub(r'\s+', '', clean_name)
    offer_name = f"Amazon{clean_name[:20]}"  # Limit length
    
    offer = {
        'affiliate_id': 'test0b252-20',
        'affiliate_param': 'tag',
        'base_url': f"https://www.amazon.com/dp/{product['asin']}",
        'name': offer_name,
        'utm_campaign': 'launch',
        'utm_source': 'site'
    }
    
    return offer

def update_config_yaml(products, config_file='config.yaml'):
    """Update config.yaml with new products"""
    
    # Load existing config
    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
    
    # Add new offers
    new_offers = []
    for product in products:
        offer = create_offer_entry(product)
        new_offers.append(offer)
    
    # Add to existing offers
    config['offers'].extend(new_offers)
    
    # Save updated config
    with open(config_file, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)
    
    return len(new_offers)

def create_product_summary(products):
    """Create a summary of found products"""
    
    summary = f"""
# Product Research Results Summary
## Date: {datetime.now().strftime('%Y-%m-%d')}
## Total Products Found: {len(products)}

"""
    
    # Group by category
    categories = {}
    for product in products:
        category = product['category']
        if category not in categories:
            categories[category] = []
        categories[category].append(product)
    
    for category, category_products in categories.items():
        summary += f"## {category} ({len(category_products)} products)\n\n"
        
        for product in category_products:
            summary += f"### {product['name']}\n"
            summary += f"- **ASIN**: {product['asin']}\n"
            summary += f"- **Price**: ${product['price']}\n"
            summary += f"- **Eco Features**: {product['eco_features']}\n"
            summary += f"- **Amazon URL**: {product['amazon_url']}\n\n"
    
    return summary

def main():
    """Main function"""
    
    print("🌱 Processing ChatGPT Product Research Results")
    print("=" * 50)
    
    # Check if results file exists
    results_file = 'chatgpt_results.txt'
    
    try:
        with open(results_file, 'r') as f:
            results_text = f.read()
    except FileNotFoundError:
        print(f"❌ Results file '{results_file}' not found!")
        print("📋 Please save ChatGPT results to 'chatgpt_results.txt' first")
        return
    
    # Parse results
    print("📊 Parsing ChatGPT results...")
    products = parse_chatgpt_results(results_text)
    
    if not products:
        print("❌ No products found in results!")
        print("�� Make sure the results follow the expected format")
        return
    
    print(f"✅ Found {len(products)} products")
    
    # Update config
    print("🔧 Updating config.yaml...")
    added_count = update_config_yaml(products)
    print(f"✅ Added {added_count} new offers to config.yaml")
    
    # Create summary
    summary = create_product_summary(products)
    with open('product_research_summary.md', 'w') as f:
        f.write(summary)
    
    print("📄 Product summary saved to: product_research_summary.md")
    
    print(f"\n🎯 Next Steps:")
    print(f"   1. Review the updated config.yaml")
    print(f"   2. Test new products with content pipeline")
    print(f"   3. Create articles for new product categories")
    print(f"   4. Update product comparison tables")

if __name__ == "__main__":
    main()
