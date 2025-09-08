#!/usr/bin/env python3
"""
Image generator integration for affiliate marketing
Creates slideshow-style images for social media posts
"""

import sys
import os
from pathlib import Path
from image_library import image_library
from datetime import datetime
import uuid

# Add the text-to-image directory to Python path
text_to_image_path = Path(__file__).parent.parent / "text-to-image"
sys.path.insert(0, str(text_to_image_path))

try:
    from generate_image import check_device, load_model, generate_image as stable_diffusion_generate
except ImportError as e:
    print(f"❌ Cannot import text-to-image module: {e}")
    stable_diffusion_generate = None

class SlideshowImageGenerator:
    def __init__(self):
        self.model_loaded = False
        self.pipe = None
        self.device = None
        
    def load_model_if_needed(self):
        """Load the Stable Diffusion model if not already loaded"""
        if not self.model_loaded and stable_diffusion_generate:
            try:
                print("📥 Loading image generation model...")
                self.device = check_device()
                self.pipe = load_model(self.device)
                self.model_loaded = True
                print("✅ Image model loaded successfully!")
                return True
            except Exception as e:
                print(f"❌ Failed to load model: {e}")
                return False
        return self.model_loaded
    
    def generate_product_slideshow_images(self, 
                                        product_name: str,
                                        article_title: str,
                                        style: str = "simple",
                                        count: int = 3,
                                        progress_callback=None) -> list:
        """
        Generate slideshow images for a product article
        """
        if not self.load_model_if_needed():
            raise Exception("Image generation model not available")
        
        images = []
        
        # Create output directory
        output_dir = Path("site/images/slideshows")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate different types of images
        prompts = self._create_slideshow_prompts(product_name, article_title, style, count)
        
        if progress_callback:
            progress_callback(10, f"Model loaded, generating {count} images...")
        
        for i, prompt_data in enumerate(prompts):
            try:
                current_progress = 10 + (i * 70 // len(prompts))
                if progress_callback:
                    progress_callback(current_progress, f"Generating image {i+1}/{len(prompts)}: {prompt_data['title']}")
                
                print(f"🎨 Generating image {i+1}/{len(prompts)}: {prompt_data['title']}")
                
                # Generate image using your existing model
                image = stable_diffusion_generate(
                    self.pipe, 
                    prompt_data['prompt'], 
                    prompt_data.get('negative_prompt', '')
                )
                
                if image:
                    # Save with meaningful filename
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    clean_name = product_name.lower().replace(' ', '_').replace('-', '_')
                    filename = f"{timestamp}_{clean_name}_slide_{i+1}.png"
                    filepath = output_dir / filename
                    
                    image.save(filepath)
                    
                    images.append({
                        'filename': filename,
                        'path': str(filepath),
                        'title': prompt_data['title'],
                        'prompt': prompt_data['prompt'],
                        'url': f"/images/slideshows/{filename}"
                    })
                    
                    save_progress = 80 + (i * 15 // len(prompts))
                    if progress_callback:
                        progress_callback(save_progress, f"Saved image {i+1}: {prompt_data['title']}")
                    
                    print(f"✅ Saved: {filename}")
                else:
                    print(f"❌ Failed to generate image {i+1}")
                    
            except Exception as e:
                print(f"❌ Error generating image {i+1}: {e}")
                continue
        
        if progress_callback:
            progress_callback(100, f"Completed! Generated {len(images)} images")
        
        # Add to image library
        try:
            if images:  # Only if we have images
                library_entry = image_library.add_images(images, product_name, style, timestamp)
                print(f"📚 Added {len(images)} images to library: {library_entry['id']}")
        except Exception as e:
            print(f"⚠️  Library storage failed: {e}")
        
        return images
    
    def _create_slideshow_prompts(self, product_name: str, article_title: str, style: str, count: int) -> list:
        """Create prompts for slideshow images"""
        
        # Determine product type for better prompts
        product_lower = product_name.lower()
        
        if "poop" in product_lower or "bag" in product_lower:
            # Poop bag specific prompts - NO HUMANS, focus on product and dogs
            base_prompts = [
                {
                    'title': 'Product Hero Shot',
                    'prompt': f"biodegradable dog poop bags, eco-friendly packaging, green and earth tones, professional product photography, premium quality",
                    'negative_prompt': 'humans, people, hands, person, plastic bags, non-biodegradable, artificial colors, cluttered background'
                },
                {
                    'title': 'Environmental Comparison',
                    'prompt': f"biodegradable poop bag decomposing in soil next to plastic bag, environmental comparison, nature background, sustainability concept",
                    'negative_prompt': 'humans, people, person, hands, complex scene, multiple objects, text overlay'
                },
                {
                    'title': 'Happy Dog Outside',
                    'prompt': f"happy dog in clean park environment, responsible pet ownership concept, well-maintained outdoor space, eco-friendly lifestyle",
                    'negative_prompt': 'humans, people, person, hands, messy environment, inappropriate content, complex background'
                },
                {
                    'title': 'Premium Packaging',
                    'prompt': f"eco-friendly poop bag packaging with green certification symbols, premium biodegradable product, clean professional design",
                    'negative_prompt': 'humans, people, hands, person, plastic packaging, non-eco design, cluttered'
                },
                {
                    'title': 'Nature Friendly',
                    'prompt': f"biodegradable poop bags with green leaves and earth elements, zero waste concept, environmental responsibility, natural setting",
                    'negative_prompt': 'humans, people, person, hands, artificial elements, plastic, non-sustainable imagery'
                }
            ]
        elif "toy" in product_lower:
            # Dog toy specific prompts - NO HUMANS, dogs and products only
            base_prompts = [
                {
                    'title': 'Product Hero Shot',
                    'prompt': f"eco-friendly dog toy, natural materials, clean white background, professional product photography, premium pet product",
                    'negative_prompt': 'humans, people, hands, person, cheap plastic, cluttered background, stuffed animal, plush toy'
                },
                {
                    'title': 'Happy Dog Playing',
                    'prompt': f"golden retriever or labrador happily playing with eco-friendly dog toy, outdoor grass setting, natural lighting, joyful dog expression",
                    'negative_prompt': 'humans, people, person, hands, indoor setting, multiple dogs, aggressive behavior, artificial lighting'
                },
                {
                    'title': 'Product Close-Up',
                    'prompt': f"detailed close-up of eco-friendly dog toy showing natural texture and quality materials, macro photography, premium construction",
                    'negative_prompt': 'humans, people, hands, person, cheap materials, plastic, artificial, low quality'
                },
                {
                    'title': 'Size Comparison',
                    'prompt': f"eco-friendly dog toy next to dog paw for size reference, clean background, product sizing guide, helpful comparison",
                    'negative_prompt': 'humans, people, person, hands, human body parts, complex scene, multiple objects'
                },
                {
                    'title': 'Dog with Toy',
                    'prompt': f"cute dog sitting next to eco-friendly toy, proud pet owner moment, natural outdoor setting, healthy happy dog",
                    'negative_prompt': 'humans, people, person, hands, indoor setting, multiple pets, artificial background'
                }
            ]
        else:
            # General eco pet product prompts - dogs and products only, NO HUMANS
            base_prompts = [
                {
                    'title': 'Product Hero Shot',
                    'prompt': f"premium eco-friendly pet product, clean white background, professional studio lighting, high-end commercial photography",
                    'negative_prompt': 'humans, people, hands, person, cheap, low quality, cluttered background, multiple objects, text, logos'
                },
                {
                    'title': 'Dog Product Combo',
                    'prompt': f"happy dog next to eco-friendly pet product, clean background, natural lighting, product showcase with satisfied pet",
                    'negative_prompt': 'humans, people, hands, person, expensive looking, luxury only, complex scene, text overlay'
                },
                {
                    'title': 'Product Benefits',
                    'prompt': f"eco-friendly pet product with green nature elements, sustainability benefits, clean minimal design, environmental appeal",
                    'negative_prompt': 'humans, people, hands, person, complex scene, multiple problems, cluttered, abstract'
                },
                {
                    'title': 'Quality Focus',
                    'prompt': f"eco-friendly pet product showing premium materials and construction, natural textures, high-quality manufacturing",
                    'negative_prompt': 'humans, people, hands, person, artificial, chemical, unsafe, low quality'
                },
                {
                    'title': 'Happy Pet Life',
                    'prompt': f"content dog in natural setting with eco-friendly pet products, healthy pet lifestyle, outdoor environment, well-cared-for pet",
                    'negative_prompt': 'humans, people, hands, person, outdated, unpopular, low engagement, boring, indoor setting'
                }
            ]
        
        # Adjust prompts based on style
        if style == "minimal":
            for prompt in base_prompts:
                prompt['prompt'] += ", ultra minimal, clean, simple"
                prompt['negative_prompt'] += ", detailed, complex, ornate"
        elif style == "vibrant":
            for prompt in base_prompts:
                prompt['prompt'] += ", bright colors, vibrant, eye-catching"
        elif style == "professional":
            for prompt in base_prompts:
                prompt['prompt'] += ", professional photography, high quality, studio lighting"
        
        # Return requested number of prompts
        return base_prompts[:count]
    
    def test_connection(self) -> bool:
        """Test if the image generation system is available"""
        try:
            return stable_diffusion_generate is not None
        except:
            return False

# Test function
if __name__ == "__main__":
    generator = SlideshowImageGenerator()
    if generator.test_connection():
        print("✅ Image generator available!")
        
        # Test with a simple prompt
        try:
            images = generator.generate_product_slideshow_images(
                "eco-friendly dog toy", 
                "Test Article", 
                "simple", 
                1
            )
            print(f"✅ Generated {len(images)} test images")
        except Exception as e:
            print(f"❌ Test generation failed: {e}")
    else:
        print("❌ Image generator not available")
