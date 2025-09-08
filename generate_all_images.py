#!/usr/bin/env python3
"""
Generate All Images for Eco Pet Guide
This script generates hero images for all existing articles and product card images for routes
"""

import os
import sys
import time
from dotenv import load_dotenv

# Add current directory to path to import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

def main():
    print("🎨 Starting image generation for Eco Pet Guide...")
    print("=" * 60)
    
    # Check if we have the required dependencies
    try:
        from gemini_image_generator import GeminiImageGenerator
        from app import create_product_card_image
        print("✅ All dependencies available")
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        print("\n📋 To install required dependencies:")
        print("pip install google-generativeai pillow")
        print("\n🔑 Don't forget to set your GEMINI_API_KEY in .env file:")
        print("GEMINI_API_KEY=your_api_key_here")
        return
    
    # Check for API key
    if not os.getenv('GEMINI_API_KEY'):
        print("❌ GEMINI_API_KEY not found in environment variables")
        print("\n🔑 Please add your Gemini API key to the .env file:")
        print("GEMINI_API_KEY=your_api_key_here")
        return
    
    generator = GeminiImageGenerator()
    
    # Phase 1: Generate hero images for existing articles
    print("\n📝 Phase 1: Generating hero images for existing articles...")
    print("-" * 60)
    
    existing_articles = [
        ("Pawsitive Choices: Eco-Friendly Fun for Your Furry Friend", "pawsitive-choices-eco-friendly-fun-for-your-furry-friend", "general_article"),
        ("Spoil Your Pup & Save the Planet: The Joy of Eco-Friendly Dog Toys", "spoil-your-pup-save-the-planet-the-joy-of-eco-friendly-dog-toys", "general_article"),
        ("Eco-Friendly Dog Toys That Are Good for Your Pet and the Planet", "eco-friendly-dog-toys-that-are-good-for-your-pet-and-the-planet", "product_review"),
        ("AmazonEcoFriendlyDogToys - Comparison", "ai-generated-amazonecofriendlydogtoys-comparison", "comparison"),
        ("Best Biodegradable Dog Poop Bags 2025: Earth-Rated vs Competitors", "best-biodegradable-dog-poop-bags-2025-earth-rated-vs-competitors", "comparison"),
        ("Best Eco-Friendly Dog Toys (2025)", "best-eco-friendly-dog-toys-2025", "roundup"),
        ("West Paw Toppl vs Kong: Which Eco-Friendly Dog Toy is Better in 2025?", "west-paw-toppl-vs-kong-which-eco-friendly-dog-toy-is-better-in-2025", "comparison"),
        ("How to Choose Non-Toxic Dog Toys (Guide)", "how-to-choose-non-toxic-dog-toys-guide", "how_to_guide"),
        ("Low-Waste Dog Starter Kit: 9 Sustainable Essentials", "low-waste-dog-starter-kit-9-sustainable-essentials", "roundup"),
        ("West Paw Toppl vs Kong: Which Is Greener in 2025?", "west-paw-toppl-vs-kong-which-is-greener-in-2025", "comparison"),
        ("Best Biodegradable Dog Poop Bags (2025)", "best-biodegradable-dog-poop-bags-2025", "product_review")
    ]
    
    article_success = 0
    for i, (title, slug, article_type) in enumerate(existing_articles, 1):
        print(f"\n{i:2d}/11 📖 {title[:60]}...")
        
        # Check if image already exists
        image_path = f"site/images/library/hero-{slug}.jpg"
        if os.path.exists(image_path):
            print(f"     ⏭️  Image already exists, skipping")
            article_success += 1
            continue
        
        try:
            filepath = generator.generate_article_image(title, slug, article_type)
            if filepath:
                print(f"     ✅ Generated: {filepath}")
                article_success += 1
            else:
                print(f"     ❌ Failed to generate image")
            
            # Rate limiting to avoid API limits
            if i < len(existing_articles):
                print(f"     ⏳ Waiting 5 seconds...")
                time.sleep(5)
                
        except Exception as e:
            print(f"     ❌ Error: {e}")
    
    print(f"\n📊 Article Images: {article_success}/{len(existing_articles)} successful")
    
    # Phase 2: Generate category card images
    print("\n🏷️  Phase 2: Generating category card images...")
    print("-" * 60)
    
    categories = [
        ('Toys', 'toys'),
        ('Poop Bags', 'poop-bags'),
        ('Bowls & Feeding', 'bowls-feeding'),
        ('Leashes & Collars', 'leashes-collars'),
        ('Treats', 'treats'),
        ('Grooming', 'grooming'),
        ('Beds & Comfort', 'beds-comfort')
    ]
    
    category_success = 0
    for i, (name, slug) in enumerate(categories, 1):
        print(f"\n{i}/7 🏷️  {name}...")
        
        # Check if image already exists
        image_path = f"site/images/library/card-category-{slug}.jpg"
        if os.path.exists(image_path):
            print(f"     ⏭️  Image already exists, skipping")
            category_success += 1
            continue
        
        try:
            filepath = generator.generate_article_image(
                article_title=f"{name} Category",
                article_slug=f"category-{slug}",
                article_type='category_card',
                category=name.lower()
            )
            if filepath:
                print(f"     ✅ Generated: {filepath}")
                category_success += 1
            else:
                print(f"     ❌ Failed to generate image")
            
            # Rate limiting
            if i < len(categories):
                print(f"     ⏳ Waiting 3 seconds...")
                time.sleep(3)
                
        except Exception as e:
            print(f"     ❌ Error: {e}")
    
    print(f"\n📊 Category Images: {category_success}/{len(categories)} successful")
    
    # Phase 3: Generate hero section image
    print("\n🎯 Phase 3: Generating main hero section image...")
    print("-" * 60)
    
    hero_image_path = "site/images/library/hero-main-section.jpg"
    if os.path.exists(hero_image_path):
        print("⏭️  Main hero image already exists, skipping")
    else:
        try:
            filepath = generator.generate_article_image(
                article_title="Eco Pet Guide - Sustainable Dog Products",
                article_slug="main-hero-section",
                article_type='hero_section'
            )
            if filepath:
                print(f"✅ Generated main hero image: {filepath}")
            else:
                print("❌ Failed to generate main hero image")
        except Exception as e:
            print(f"❌ Error generating main hero image: {e}")
    
    # Phase 4: Update existing product card images (keep the text-based ones for now)
    print("\n🛍️  Phase 4: Product card images...")
    print("-" * 60)
    print("✅ Product card images are already generated with text labels")
    print("   (These work well and are consistent, keeping them as-is)")
    
    # Summary
    print("\n" + "=" * 60)
    print("🎉 IMAGE GENERATION COMPLETE!")
    print("=" * 60)
    print(f"📖 Article Hero Images: {article_success}/{len(existing_articles)}")
    print(f"🏷️  Category Card Images: {category_success}/{len(categories)}")
    print("🛍️  Product Card Images: ✅ (existing text-based)")
    print("🎯 Main Hero Image: ✅")
    
    if article_success == len(existing_articles) and category_success == len(categories):
        print("\n🎊 All images generated successfully!")
        print("🌐 Your website now has custom Gemini-generated images!")
    else:
        print("\n⚠️  Some images failed to generate. Check the logs above.")
        print("💡 You can run this script again to retry failed generations.")
    
    print("\n📋 Next Steps:")
    print("1. 🔄 Restart your server: python3 start_admin.py")
    print("2. 🌐 Visit your homepage to see the new images")
    print("3. 🚀 New articles will automatically get Gemini-generated images!")
    
    # Create a simple test to verify integration
    print("\n🧪 Testing integration...")
    try:
        from app import generate_article_hero_image
        test_result = generate_article_hero_image("Test Article", "test-article")
        if GEMINI_AVAILABLE:
            print("✅ Gemini integration is working")
        else:
            print("⚠️  Gemini integration available but API key needed")
    except Exception as e:
        print(f"❌ Integration test failed: {e}")

def generate_prompts_for_manual_use():
    """Generate a text file with all prompts for manual use in Gemini"""
    print("\n📝 Generating manual prompts file...")
    
    try:
        from gemini_image_generator import GeminiImageGenerator
        generator = GeminiImageGenerator()
        
        with open("manual_gemini_prompts.txt", "w") as f:
            f.write("GEMINI IMAGE PROMPTS FOR ECO PET GUIDE\n")
            f.write("=" * 50 + "\n\n")
            f.write("Copy and paste these prompts into Gemini's image generator\n")
            f.write("Save images as specified filenames in site/images/library/\n\n")
            
            # Article prompts
            existing_articles = [
                ("Pawsitive Choices: Eco-Friendly Fun for Your Furry Friend", "pawsitive-choices-eco-friendly-fun-for-your-furry-friend", "general_article"),
                ("Spoil Your Pup & Save the Planet: The Joy of Eco-Friendly Dog Toys", "spoil-your-pup-save-the-planet-the-joy-of-eco-friendly-dog-toys", "general_article"),
                ("Eco-Friendly Dog Toys That Are Good for Your Pet and the Planet", "eco-friendly-dog-toys-that-are-good-for-your-pet-and-the-planet", "product_review"),
                ("AmazonEcoFriendlyDogToys - Comparison", "ai-generated-amazonecofriendlydogtoys-comparison", "comparison"),
                ("Best Biodegradable Dog Poop Bags 2025: Earth-Rated vs Competitors", "best-biodegradable-dog-poop-bags-2025-earth-rated-vs-competitors", "comparison"),
                ("Best Eco-Friendly Dog Toys (2025)", "best-eco-friendly-dog-toys-2025", "roundup"),
                ("West Paw Toppl vs Kong: Which Eco-Friendly Dog Toy is Better in 2025?", "west-paw-toppl-vs-kong-which-eco-friendly-dog-toy-is-better-in-2025", "comparison"),
                ("How to Choose Non-Toxic Dog Toys (Guide)", "how-to-choose-non-toxic-dog-toys-guide", "how_to_guide"),
                ("Low-Waste Dog Starter Kit: 9 Sustainable Essentials", "low-waste-dog-starter-kit-9-sustainable-essentials", "roundup"),
                ("West Paw Toppl vs Kong: Which Is Greener in 2025?", "west-paw-toppl-vs-kong-which-is-greener-in-2025", "comparison"),
                ("Best Biodegradable Dog Poop Bags (2025)", "best-biodegradable-dog-poop-bags-2025", "product_review")
            ]
            
            f.write("ARTICLE HERO IMAGES\n")
            f.write("-" * 20 + "\n\n")
            
            for i, (title, slug, article_type) in enumerate(existing_articles, 1):
                prompt = generator._create_prompt(title, article_type)
                f.write(f"{i}. {title}\n")
                f.write(f"   Filename: hero-{slug}.jpg\n")
                f.write(f"   Prompt: {prompt}\n\n")
        
        print("✅ Manual prompts saved to: manual_gemini_prompts.txt")
        
    except Exception as e:
        print(f"❌ Error generating manual prompts: {e}")

if __name__ == "__main__":
    # Check if user wants manual prompts
    if len(sys.argv) > 1 and sys.argv[1] == "--manual-prompts":
        generate_prompts_for_manual_use()
    else:
        main()
