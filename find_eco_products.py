#!/usr/bin/env python3
"""
Eco-Friendly Pet Product Research Script
========================================

This script generates a comprehensive list of eco-friendly pet products
that match the sustainability theme of the Eco Pet Guide website.

The script creates formatted product suggestions that can be given to
a ChatGPT agent to search for specific Amazon products and ASINs.
"""

import json
from datetime import datetime

def generate_product_suggestions():
    """Generate eco-friendly pet product suggestions with proper formatting"""
    
    # Current products for reference
    current_products = [
        "Eco-Friendly Dog Toys (B004A7X27M)",
        "Biodegradable Poop Bags (B07MYPFMZP)", 
        "Eco-Friendly Dog Beds (B00TQ47CPW)",
        "Organic Dog Treats (B093CLBJDW)",
        "Hemp Dog Leash (B00C9L67XW)",
        "Bamboo Dog Bowl (B08C342VQ6)"
    ]
    
    # Eco-friendly product categories to research
    product_categories = {
        "Grooming & Hygiene": {
            "description": "Sustainable grooming products for dogs",
            "keywords": ["eco-friendly", "natural", "organic", "biodegradable", "sustainable"],
            "products": [
                "Natural Dog Shampoo Bars (plastic-free)",
                "Bamboo Dog Brush (sustainable materials)",
                "Organic Dog Toothpaste (natural ingredients)",
                "Hemp Dog Towels (sustainable fabric)",
                "Biodegradable Dog Wipes (compostable)",
                "Natural Flea & Tick Spray (chemical-free)",
                "Organic Paw Balm (natural healing)",
                "Sustainable Dog Nail Clippers (eco-friendly materials)"
            ]
        },
        
        "Training & Behavior": {
            "description": "Eco-friendly training tools and accessories",
            "keywords": ["sustainable", "natural", "eco-friendly", "biodegradable"],
            "products": [
                "Bamboo Training Clicker (sustainable materials)",
                "Organic Training Treats (natural ingredients)",
                "Hemp Training Pouch (sustainable fabric)",
                "Natural Calming Spray (organic ingredients)",
                "Eco-Friendly Puzzle Toys (sustainable materials)",
                "Bamboo Treat Dispenser (renewable materials)",
                "Organic Chew Toys (natural materials)",
                "Sustainable Training Mat (eco-friendly materials)"
            ]
        },
        
        "Travel & Outdoor": {
            "description": "Sustainable travel and outdoor gear for dogs",
            "keywords": ["eco-friendly", "sustainable", "recycled", "natural"],
            "products": [
                "Recycled Dog Travel Bag (sustainable materials)",
                "Bamboo Dog Water Bottle (eco-friendly)",
                "Hemp Dog Harness (sustainable fabric)",
                "Organic Dog Sunscreen (natural protection)",
                "Biodegradable Dog Booties (compostable)",
                "Eco-Friendly Dog Carrier (sustainable materials)",
                "Natural Dog Cooling Mat (non-toxic materials)",
                "Sustainable Dog Life Jacket (recycled materials)"
            ]
        },
        
        "Health & Wellness": {
            "description": "Natural health and wellness products for dogs",
            "keywords": ["natural", "organic", "chemical-free", "sustainable"],
            "products": [
                "Organic Dog Supplements (natural ingredients)",
                "Natural Dog Probiotics (organic)",
                "Eco-Friendly Dog Vitamins (sustainable packaging)",
                "Organic Dog CBD Oil (natural wellness)",
                "Natural Dog Pain Relief (herbal ingredients)",
                "Sustainable Dog Massage Tools (eco-friendly materials)",
                "Organic Dog Ear Cleaner (natural ingredients)",
                "Natural Dog Anxiety Relief (herbal supplements)"
            ]
        },
        
        "Home & Living": {
            "description": "Sustainable home products for dogs",
            "keywords": ["eco-friendly", "sustainable", "natural", "recycled"],
            "products": [
                "Bamboo Dog Gate (sustainable materials)",
                "Organic Dog Blanket (natural fibers)",
                "Recycled Dog Crate (sustainable materials)",
                "Natural Dog Air Freshener (organic ingredients)",
                "Eco-Friendly Dog Door (sustainable materials)",
                "Organic Dog Pillow (natural materials)",
                "Sustainable Dog Food Storage (eco-friendly containers)",
                "Natural Dog Repellent (organic ingredients)"
            ]
        },
        
        "Cat Products": {
            "description": "Eco-friendly products for cats",
            "keywords": ["eco-friendly", "natural", "sustainable", "organic"],
            "products": [
                "Bamboo Cat Litter Box (sustainable materials)",
                "Natural Cat Litter (biodegradable)",
                "Organic Cat Treats (natural ingredients)",
                "Hemp Cat Collar (sustainable fabric)",
                "Eco-Friendly Cat Toys (sustainable materials)",
                "Natural Cat Scratching Post (sustainable materials)",
                "Organic Cat Food Bowls (natural materials)",
                "Sustainable Cat Carrier (eco-friendly materials)"
            ]
        },
        
        "Small Pet Products": {
            "description": "Sustainable products for small pets (rabbits, guinea pigs, etc.)",
            "keywords": ["eco-friendly", "natural", "sustainable", "organic"],
            "products": [
                "Natural Small Pet Bedding (biodegradable)",
                "Organic Small Pet Food (natural ingredients)",
                "Bamboo Small Pet Cage (sustainable materials)",
                "Eco-Friendly Small Pet Toys (sustainable materials)",
                "Natural Small Pet Treats (organic ingredients)",
                "Sustainable Small Pet Water Bottle (eco-friendly materials)",
                "Organic Small Pet Hay (natural feeding)",
                "Eco-Friendly Small Pet Litter (biodegradable)"
            ]
        }
    }
    
    return product_categories

def create_chatgpt_prompt():
    """Create a formatted prompt for ChatGPT agent"""
    
    categories = generate_product_suggestions()
    
    prompt = f"""
# Eco-Friendly Pet Product Research Request
## Date: {datetime.now().strftime('%Y-%m-%d')}

## Website Theme: Eco Pet Guide
**Focus**: Sustainable, eco-friendly, natural, and organic pet products
**Target Audience**: Environmentally conscious pet parents
**Current Products**: Dog toys, poop bags, beds, treats, leashes, bowls

## Research Instructions for ChatGPT Agent:

Please search for Amazon products for each category below. For each product, provide:
1. **Product Name** (exact Amazon title)
2. **Amazon ASIN** (BXXXXXXXXXX format)
3. **Price Range** (e.g., $15-25)
4. **Key Eco Features** (materials, certifications, sustainability aspects)
5. **Amazon URL** (with placeholder for affiliate tag)

## Product Categories to Research:

"""
    
    for category, details in categories.items():
        prompt += f"\n### {category}\n"
        prompt += f"**Description**: {details['description']}\n"
        prompt += f"**Keywords**: {', '.join(details['keywords'])}\n\n"
        prompt += "**Products to find**:\n"
        
        for i, product in enumerate(details['products'], 1):
            prompt += f"{i}. {product}\n"
        
        prompt += "\n---\n"
    
    prompt += """
## Format for Each Product Found:

```
Product Name: [Exact Amazon Title]
ASIN: BXXXXXXXXXX
Price: $XX-XX
Eco Features: [List key sustainable features]
Amazon URL: https://www.amazon.com/dp/BXXXXXXXXXX?tag=YOUR-AFFILIATE-TAG
Category: [Category from above]
Keywords: [Relevant eco keywords]
```

## Search Guidelines:
- Focus on products with clear eco-friendly, sustainable, natural, or organic claims
- Look for certifications like USDA Organic, FSC Certified, ASTM D6400, etc.
- Prioritize products made from bamboo, hemp, recycled materials, natural fibers
- Avoid products with excessive plastic packaging
- Target products with 4+ star ratings
- Include both budget-friendly and premium options
- Ensure products are currently available on Amazon US

## Priority Categories:
1. Grooming & Hygiene (high demand)
2. Training & Behavior (growing market)
3. Travel & Outdoor (seasonal relevance)
4. Health & Wellness (premium market)
5. Home & Living (practical needs)
6. Cat Products (expanding audience)
7. Small Pet Products (niche but loyal)

Please research 3-5 products per category, focusing on the most popular and well-reviewed eco-friendly options.
"""
    
    return prompt

def save_prompt_to_file():
    """Save the prompt to a file for easy copying"""
    
    prompt = create_chatgpt_prompt()
    
    with open('eco_product_research_prompt.txt', 'w') as f:
        f.write(prompt)
    
    print("✅ Eco product research prompt saved to: eco_product_research_prompt.txt")
    print("📋 Copy the contents and paste into ChatGPT for product research")
    
    return prompt

def create_product_template():
    """Create a template for adding new products to config.yaml"""
    
    template = """
# Template for adding new products to config.yaml
# Add this to the 'offers' section:

- affiliate_id: test0b252-20
  affiliate_param: tag
  base_url: https://www.amazon.com/dp/BXXXXXXXXXX
  name: Amazon[ProductName]
  utm_campaign: launch
  utm_source: site

# Example:
- affiliate_id: test0b252-20
  affiliate_param: tag
  base_url: https://www.amazon.com/dp/B08C342VQ6
  name: AmazonBambooEcoDogBowl
  utm_campaign: launch
  utm_source: site
"""
    
    with open('product_config_template.txt', 'w') as f:
        f.write(template)
    
    print("✅ Product config template saved to: product_config_template.txt")

def main():
    """Main function to run the script"""
    
    print("🌱 Eco Pet Guide - Product Research Script")
    print("=" * 50)
    
    # Generate and save the ChatGPT prompt
    prompt = save_prompt_to_file()
    
    # Create config template
    create_product_template()
    
    # Display summary
    categories = generate_product_suggestions()
    total_products = sum(len(details['products']) for details in categories.values())
    
    print(f"\n📊 Research Summary:")
    print(f"   Categories: {len(categories)}")
    print(f"   Total Products: {total_products}")
    print(f"   Target: 3-5 products per category")
    print(f"   Expected Results: {len(categories) * 4} products")
    
    print(f"\n🎯 Next Steps:")
    print(f"   1. Copy contents of 'eco_product_research_prompt.txt'")
    print(f"   2. Paste into ChatGPT for product research")
    print(f"   3. Use results to update config.yaml")
    print(f"   4. Test new products with content pipeline")
    
    print(f"\n💡 Pro Tips:")
    print(f"   - Focus on products with clear eco certifications")
    print(f"   - Prioritize bamboo, hemp, and recycled materials")
    print(f"   - Look for products with 4+ star ratings")
    print(f"   - Consider seasonal relevance (travel gear for summer, etc.)")

if __name__ == "__main__":
    main()
