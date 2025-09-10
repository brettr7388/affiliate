# Eco Pet Guide - Product Research Workflow

## Overview
This workflow helps you find and add new eco-friendly pet products to your affiliate website using ChatGPT for product research.

## Files Created
- `find_eco_products.py` - Generates research prompts for ChatGPT
- `process_chatgpt_results.py` - Processes ChatGPT results and updates config
- `eco_product_research_prompt.txt` - Ready-to-use prompt for ChatGPT
- `product_config_template.txt` - Template for adding products to config.yaml

## Step-by-Step Workflow

### 1. Generate Research Prompt
```bash
python3 find_eco_products.py
```
This creates `eco_product_research_prompt.txt` with 56 product suggestions across 7 categories.

### 2. Use ChatGPT for Research
1. Copy the contents of `eco_product_research_prompt.txt`
2. Paste into ChatGPT
3. Ask ChatGPT to research the products and provide ASINs
4. Save the results to `chatgpt_results.txt`

### 3. Process Results
```bash
python3 process_chatgpt_results.py
```
This will:
- Parse the ChatGPT results
- Extract product information (ASIN, name, price, eco features)
- Update `config.yaml` with new offers
- Create a summary in `product_research_summary.md`

### 4. Test New Products
```bash
# Test the content pipeline with a new product
python3 -c "
from content_pipeline import generate_post
slug = generate_post(title='Test New Eco Product', body_md='Test content')
print(f'Generated: {slug}')
"
```

## Product Categories Included

1. **Grooming & Hygiene** (8 products)
   - Natural shampoo bars, bamboo brushes, organic toothpaste, etc.

2. **Training & Behavior** (8 products)
   - Bamboo clickers, organic treats, hemp training pouches, etc.

3. **Travel & Outdoor** (8 products)
   - Recycled travel bags, bamboo water bottles, hemp harnesses, etc.

4. **Health & Wellness** (8 products)
   - Organic supplements, natural probiotics, eco-friendly vitamins, etc.

5. **Home & Living** (8 products)
   - Bamboo gates, organic blankets, recycled crates, etc.

6. **Cat Products** (8 products)
   - Bamboo litter boxes, natural litter, organic treats, etc.

7. **Small Pet Products** (8 products)
   - Natural bedding, organic food, bamboo cages, etc.

## Expected Results
- **Target**: 3-5 products per category
- **Total Expected**: 28 new products
- **Focus**: Eco-friendly, sustainable, natural, organic materials

## Eco-Friendly Criteria
Products should have:
- Clear eco-friendly, sustainable, or natural claims
- Certifications (USDA Organic, FSC Certified, ASTM D6400, etc.)
- Materials: bamboo, hemp, recycled materials, natural fibers
- Minimal plastic packaging
- 4+ star ratings on Amazon

## Example ChatGPT Results Format
```
Product Name: Natural Bamboo Dog Brush
ASIN: B123456789
Price: $15-20
Eco Features: Made from sustainable bamboo, biodegradable bristles
Amazon URL: https://www.amazon.com/dp/B123456789?tag=YOUR-AFFILIATE-TAG
Category: Grooming & Hygiene
Keywords: bamboo, sustainable, natural, eco-friendly
```

## Tips for Success
1. **Be Specific**: Ask ChatGPT to focus on products with clear eco certifications
2. **Verify ASINs**: Double-check that ASINs are valid and products are available
3. **Test Pipeline**: Always test new products with your content pipeline
4. **Update Categories**: Add new product categories to your config as needed
5. **Monitor Performance**: Track which new products perform best

## Troubleshooting
- If `process_chatgpt_results.py` fails, check the format of your ChatGPT results
- Make sure ASINs are in the correct BXXXXXXXXXX format
- Verify that products are currently available on Amazon US
- Test each new product category with the content pipeline

## Next Steps After Adding Products
1. Create articles for new product categories
2. Update product comparison tables in config.yaml
3. Add new product categories to the content pipeline
4. Create category-specific CTA messaging
5. Test affiliate links and tracking
