#!/usr/bin/env python3
"""
Create Manual Prompts for AI Image Generation
This creates prompts you can copy/paste into any AI image generator
"""

def create_category_prompts():
    """Create prompts for category images"""
    categories = [
        ('Toys', 'A collection of eco-friendly dog toys made from natural materials like hemp rope, organic cotton, and bamboo. Arranged on a clean white background with green plants. Professional product photography style, bright and clean.'),
        ('Poop Bags', 'Clean, professional image of biodegradable poop bag rolls with eco-friendly packaging, surrounded by green leaves and eco-symbols. White background, professional product photography.'),
        ('Bowls & Feeding', 'Beautiful bamboo and stainless steel eco-friendly dog bowls arranged on a clean kitchen counter with plants in background. Professional lifestyle photography, clean and modern.'),
        ('Leashes & Collars', 'High-quality hemp and recycled material dog leashes and collars displayed on natural wood surface with green plants. Professional product photography, natural aesthetic.'),
        ('Treats', 'Organic, natural dog treats in eco-friendly packaging on a rustic wooden surface with herbs and natural elements. Professional food photography style.'),
        ('Grooming', 'Natural, eco-friendly dog grooming products (shampoos, brushes, towels) made from sustainable materials in a clean, modern bathroom setting.'),
        ('Beds & Comfort', 'Comfortable eco-friendly dog beds made from recycled materials in a cozy, modern living room setting. Professional interior photography, warm and inviting.')
    ]
    
    print("🏷️ CATEGORY CARD IMAGE PROMPTS")
    print("=" * 50)
    print("Copy these prompts into any AI image generator (DALL-E, Midjourney, Gemini, etc.)")
    print("Save images as: card-category-{category}.jpg in site/images/library/\n")
    
    for i, (category, prompt) in enumerate(categories, 1):
        slug = category.lower().replace(' & ', '-').replace(' ', '-')
        print(f"{i}. {category}")
        print(f"   Filename: card-category-{slug}.jpg")
        print(f"   Prompt: {prompt}")
        print()

def create_hero_section_prompts():
    """Create prompts for hero section images"""
    print("🎯 HERO SECTION IMAGE PROMPTS")
    print("=" * 50)
    print("For the main homepage hero section\n")
    
    prompts = [
        ("Main Hero", "main-hero", "A heartwarming scene of a happy family with their dog in a beautiful, eco-friendly home environment. The dog is playing with sustainable toys while the family watches lovingly. Natural lighting, plants throughout the space, modern eco-friendly home aesthetic. Professional lifestyle photography, warm and inviting."),
        ("Trust Badge 1", "trust-planet", "A simple, clean illustration of a green earth with leaves growing from it, symbolizing environmental protection. Minimalist style, eco-green color palette."),
        ("Trust Badge 2", "trust-approved", "A happy, healthy dog showing approval with a green checkmark nearby. Clean, friendly illustration style, professional and trustworthy."),
        ("Trust Badge 3", "trust-tested", "Diverse dog owners with their pets, all looking happy and satisfied. Include a quality assurance badge. Professional, friendly illustration style.")
    ]
    
    for name, slug, prompt in prompts:
        print(f"• {name}")
        print(f"  Filename: {slug}.jpg")
        print(f"  Prompt: {prompt}")
        print()

def create_future_article_templates():
    """Create template prompts for future articles"""
    print("📝 FUTURE ARTICLE TEMPLATES")
    print("=" * 50)
    print("Use these templates for new articles by replacing [PLACEHOLDERS]\n")
    
    templates = [
        ("Product Review", "Professional product photography of [PRODUCT NAME] on a clean white background with natural lighting. Include the actual product prominently displayed with eco-friendly elements like green leaves. Made from [MATERIALS]. Professional commercial photography style, eco-friendly aesthetic."),
        ("Comparison Article", "A clean comparison layout showing [PRODUCT A] vs [PRODUCT B] side by side on a neutral background. Both products clearly visible and well-lit. Include subtle eco-friendly elements. Modern, clean aesthetic."),
        ("How-To Guide", "An educational image showing [TOPIC] with clear visual elements and a dog owner demonstrating the concept. Include relevant props. Clean, modern, instructional design aesthetic."),
        ("Roundup/List", "A beautiful flat lay of [NUMBER] [CATEGORY] items, all eco-friendly and sustainable. Clean white background, professional photography, each item clearly visible."),
        ("General Article", "A professional image representing [TOPIC] in an eco-friendly context. Include dogs, natural materials, and sustainable products. Clean, modern aesthetic with soft natural lighting.")
    ]
    
    for article_type, template in templates:
        print(f"• {article_type}:")
        print(f"  {template}")
        print()

if __name__ == "__main__":
    print("🎨 MANUAL AI IMAGE GENERATION PROMPTS")
    print("=" * 60)
    print("Use these prompts with DALL-E, Midjourney, Gemini, or any AI image generator")
    print("All images should be high-resolution, professional quality, optimized for web\n")
    
    create_category_prompts()
    create_hero_section_prompts() 
    create_future_article_templates()
    
    print("💡 TIPS:")
    print("- Add 'high resolution, professional quality, web optimized' to any prompt")
    print("- Maintain eco-friendly aesthetic: greens, natural materials, clean design")
    print("- For product photos: clean backgrounds, good lighting, clear visibility")
    print("- For lifestyle: natural lighting, plants, modern eco-friendly homes")
    print("- Save as JPG, optimize file size for web loading speed")
