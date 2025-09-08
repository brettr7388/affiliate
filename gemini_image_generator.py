"""
Gemini Image Generator for Eco Pet Guide
Automatically generates high-quality images for articles using Google Gemini
"""

import os
import re
import json
import time
import requests
from typing import Optional, Dict, List
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class GeminiImageGenerator:
    def __init__(self):
        """Initialize the Gemini Image Generator"""
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Load prompt templates
        self.prompt_templates = self._load_prompt_templates()
        
    def _load_prompt_templates(self) -> Dict[str, str]:
        """Load prompt templates for different article types"""
        return {
            'product_review': "Professional product photography of {product_name} on a clean white background with natural lighting. Include the actual product prominently displayed with eco-friendly elements like green leaves or natural materials around it. {product_details}. Professional commercial photography style, eco-friendly aesthetic.",
            
            'comparison': "A clean comparison layout showing {product_a} vs {product_b} side by side on a neutral background. Both products should be clearly visible and well-lit. Include subtle eco-friendly elements and maintain professional product photography standards. Modern, clean aesthetic.",
            
            'how_to_guide': "An educational, infographic-style image showing {topic} with clear visual elements and a dog owner demonstrating the concept. Include relevant props and maintain a clean, modern, instructional design aesthetic. Professional lifestyle photography.",
            
            'roundup': "A beautiful flat lay or arranged display of {number} {category} items, all eco-friendly and sustainable. Clean white background, professional photography, each item clearly visible and well-lit. Eco-friendly aesthetic with natural elements.",
            
            'general_article': "A professional, high-quality image representing {topic} in an eco-friendly context. Include dogs, natural materials, and sustainable products. Clean, modern aesthetic with soft natural lighting. Professional lifestyle photography style.",
            
            'category_card': "A {category} themed image showing eco-friendly dog {category} in a natural, sustainable setting. Professional product photography, clean and modern aesthetic, eco-friendly color palette.",
            
            'hero_section': "A heartwarming scene of a happy family with their dog in a beautiful, eco-friendly home environment. The dog is playing with sustainable toys while the family watches lovingly. Natural lighting, plants throughout the space, modern eco-friendly home aesthetic. Professional lifestyle photography, warm and inviting."
        }
    
    def generate_article_image(self, article_title: str, article_slug: str, article_type: str = 'general_article', **kwargs) -> Optional[str]:
        """
        Generate an image for an article
        
        Args:
            article_title: The title of the article
            article_slug: The slug for the article (used for filename)
            article_type: Type of article (product_review, comparison, how_to_guide, etc.)
            **kwargs: Additional parameters for prompt customization
            
        Returns:
            Path to the generated image file, or None if generation failed
        """
        try:
            # Generate the prompt
            prompt = self._create_prompt(article_title, article_type, **kwargs)
            
            # Generate the image using Gemini
            image_data = self._generate_image_with_gemini(prompt)
            
            if image_data:
                # Save the image
                filename = f"hero-{article_slug}.jpg"
                filepath = f"site/images/library/{filename}"
                
                # Ensure directory exists
                os.makedirs("site/images/library", exist_ok=True)
                
                # Save the image
                with open(filepath, 'wb') as f:
                    f.write(image_data)
                
                # Optimize the image
                self._optimize_image(filepath)
                
                print(f"✅ Generated image: {filepath}")
                return filepath
            
            return None
            
        except Exception as e:
            print(f"❌ Error generating image for {article_slug}: {e}")
            return None
    
    def _create_prompt(self, article_title: str, article_type: str, **kwargs) -> str:
        """Create a detailed prompt for image generation"""
        
        # Get base template
        template = self.prompt_templates.get(article_type, self.prompt_templates['general_article'])
        
        # Extract key information from article title
        topic = article_title.lower()
        
        # Customize based on article type
        if article_type == 'product_review':
            product_name = kwargs.get('product_name', self._extract_product_name(article_title))
            product_details = kwargs.get('product_details', self._generate_product_details(topic))
            prompt = template.format(product_name=product_name, product_details=product_details)
            
        elif article_type == 'comparison':
            products = self._extract_comparison_products(article_title)
            prompt = template.format(
                product_a=products.get('product_a', 'Product A'),
                product_b=products.get('product_b', 'Product B')
            )
            
        elif article_type == 'how_to_guide':
            topic_clean = article_title.replace('How to ', '').replace('Guide', '').strip()
            prompt = template.format(topic=topic_clean)
            
        elif article_type == 'roundup':
            number, category = self._extract_roundup_info(article_title)
            prompt = template.format(number=number, category=category)
            
        elif article_type == 'category_card':
            category = kwargs.get('category', 'products')
            prompt = template.format(category=category)
            
        else:
            # General article
            prompt = template.format(topic=article_title)
        
        # Add consistent style elements
        prompt += " High resolution, professional quality, optimized for web display."
        
        return prompt
    
    def _generate_image_with_gemini(self, prompt: str) -> Optional[bytes]:
        """Generate image using Gemini API"""
        try:
            # Note: This is a placeholder for actual Gemini image generation
            # The actual implementation would depend on Google's image generation API
            # For now, we'll use a text-to-image service or create placeholder logic
            
            print(f"🎨 Generating image with prompt: {prompt[:100]}...")
            
            # Placeholder: In actual implementation, you would call:
            # response = genai.generate_image(prompt=prompt, size="600x400")
            # return response.image_data
            
            # For now, return None to indicate we need to implement the actual API call
            return None
            
        except Exception as e:
            print(f"Error calling Gemini image API: {e}")
            return None
    
    def _extract_product_name(self, title: str) -> str:
        """Extract product name from article title"""
        # Look for common product patterns
        if 'west paw' in title.lower():
            return 'West Paw Toppl'
        elif 'kong' in title.lower():
            return 'Kong Classic'
        elif 'earth-rated' in title.lower():
            return 'Earth-Rated Poop Bags'
        elif 'poop bag' in title.lower():
            return 'Biodegradable Poop Bags'
        elif 'dog toy' in title.lower():
            return 'Eco-Friendly Dog Toys'
        else:
            # Extract first few words as product name
            words = title.split()[:3]
            return ' '.join(words)
    
    def _generate_product_details(self, topic: str) -> str:
        """Generate product details based on topic"""
        details = []
        
        if 'toy' in topic:
            details.append("Made from sustainable hemp rope and organic cotton")
        if 'poop' in topic or 'bag' in topic:
            details.append("Biodegradable materials that break down naturally")
        if 'bowl' in topic:
            details.append("Crafted from sustainable bamboo and stainless steel")
        if 'leash' in topic:
            details.append("Durable hemp fibers with recycled metal hardware")
        if 'treat' in topic:
            details.append("Organic ingredients in compostable packaging")
        if 'bed' in topic:
            details.append("Recycled fill materials with organic cotton cover")
        
        if not details:
            details.append("Eco-friendly materials and sustainable manufacturing")
        
        return ', '.join(details)
    
    def _extract_comparison_products(self, title: str) -> Dict[str, str]:
        """Extract product names from comparison titles"""
        title_lower = title.lower()
        
        if 'vs' in title_lower:
            parts = title_lower.split('vs')
            if len(parts) >= 2:
                product_a = parts[0].strip().title()
                product_b = parts[1].split(':')[0].strip().title()
                return {'product_a': product_a, 'product_b': product_b}
        
        # Default fallback
        return {'product_a': 'Product A', 'product_b': 'Product B'}
    
    def _extract_roundup_info(self, title: str) -> tuple:
        """Extract number and category from roundup titles"""
        import re
        
        # Look for numbers
        numbers = re.findall(r'\b(\d+)\b', title)
        number = numbers[0] if numbers else '5'
        
        # Determine category
        title_lower = title.lower()
        if 'toy' in title_lower:
            category = 'eco-friendly dog toys'
        elif 'bag' in title_lower:
            category = 'biodegradable poop bags'
        elif 'essential' in title_lower:
            category = 'sustainable dog essentials'
        elif 'bowl' in title_lower:
            category = 'eco-friendly dog bowls'
        else:
            category = 'eco-friendly dog products'
        
        return number, category
    
    def _optimize_image(self, filepath: str):
        """Optimize image for web display"""
        try:
            with Image.open(filepath) as img:
                # Convert to RGB if necessary
                if img.mode in ('RGBA', 'P'):
                    img = img.convert('RGB')
                
                # Optimize and save
                img.save(filepath, 'JPEG', quality=85, optimize=True)
                
        except Exception as e:
            print(f"Warning: Could not optimize image {filepath}: {e}")
    
    def generate_category_images(self) -> Dict[str, str]:
        """Generate images for all product categories"""
        categories = [
            'toys', 'poop-bags', 'bowls-feeding', 'leashes-collars', 
            'treats', 'grooming', 'beds-comfort'
        ]
        
        generated_images = {}
        
        for category in categories:
            try:
                filepath = self.generate_article_image(
                    article_title=f"{category.replace('-', ' ').title()} Category",
                    article_slug=f"category-{category}",
                    article_type='category_card',
                    category=category.replace('-', ' ')
                )
                
                if filepath:
                    generated_images[category] = filepath
                    time.sleep(2)  # Rate limiting
                    
            except Exception as e:
                print(f"Error generating category image for {category}: {e}")
        
        return generated_images
    
    def generate_hero_section_images(self) -> Dict[str, str]:
        """Generate images for hero section elements"""
        hero_images = {}
        
        # Main hero image
        try:
            filepath = self.generate_article_image(
                article_title="Eco Pet Guide Hero Section",
                article_slug="main-hero",
                article_type='hero_section'
            )
            if filepath:
                hero_images['main_hero'] = filepath
        except Exception as e:
            print(f"Error generating main hero image: {e}")
        
        return hero_images
    
    def regenerate_all_existing_images(self) -> Dict[str, str]:
        """Regenerate images for all existing articles"""
        
        # Article mapping with their types
        articles = [
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
        
        generated_images = {}
        
        for title, slug, article_type in articles:
            try:
                print(f"Generating image for: {title}")
                filepath = self.generate_article_image(title, slug, article_type)
                
                if filepath:
                    generated_images[slug] = filepath
                    
                # Rate limiting to avoid API limits
                time.sleep(3)
                
            except Exception as e:
                print(f"Error generating image for {slug}: {e}")
        
        return generated_images

# Integration function for the main app
def integrate_with_content_pipeline():
    """Integration function to add image generation to content pipeline"""
    
    def generate_image_for_new_article(title: str, slug: str, content: str) -> Optional[str]:
        """Generate image when new article is created"""
        try:
            generator = GeminiImageGenerator()
            
            # Determine article type from content
            article_type = 'general_article'
            content_lower = content.lower()
            
            if 'vs' in title.lower() or 'comparison' in content_lower:
                article_type = 'comparison'
            elif 'how to' in title.lower() or 'guide' in title.lower():
                article_type = 'how_to_guide'
            elif any(num in title for num in ['5', '10', '15', '20']) and ('best' in title.lower() or 'top' in title.lower()):
                article_type = 'roundup'
            elif 'review' in content_lower or 'product' in title.lower():
                article_type = 'product_review'
            
            return generator.generate_article_image(title, slug, article_type)
            
        except Exception as e:
            print(f"Error in image generation integration: {e}")
            return None
    
    return generate_image_for_new_article

if __name__ == "__main__":
    # Test the image generator
    generator = GeminiImageGenerator()
    
    # Test generating a single image
    test_image = generator.generate_article_image(
        "Best Eco-Friendly Dog Toys 2025",
        "test-eco-dog-toys",
        "product_review"
    )
    
    if test_image:
        print(f"✅ Test image generated: {test_image}")
    else:
        print("❌ Test image generation failed")
