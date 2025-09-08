# 🎨 Gemini Image Generation System

## Overview
Your Eco Pet Guide now has an automated image generation system powered by Google Gemini! This system creates custom, professional images for:

- 📖 **Article hero images** - Custom images for each blog post
- 🏷️ **Category cards** - Images for product categories  
- 🛍️ **Product cards** - Already working with text labels
- 🎯 **Hero sections** - Main homepage images

## 🚀 Quick Start

### Option 1: Automated Generation (Recommended)
1. **Get a Gemini API Key**:
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Add it to your `.env` file: `GEMINI_API_KEY=your_api_key_here`

2. **Install Dependencies** (if not already installed):
   ```bash
   pip install google-generativeai pillow
   ```

3. **Generate All Images**:
   ```bash
   python3 generate_all_images.py
   ```

### Option 2: Manual Generation (No API Key Needed)
1. **Generate Prompts File**:
   ```bash
   python3 generate_all_images.py --manual-prompts
   ```

2. **Use the Prompts**:
   - Open `manual_gemini_prompts.txt`
   - Copy each prompt into [Gemini](https://gemini.google.com)
   - Save images with the specified filenames in `site/images/library/`

## 📁 Generated Files

### Article Images
- **Location**: `site/images/library/hero-{article-slug}.jpg`
- **Size**: 600x400px (3:2 aspect ratio)
- **Style**: Professional, eco-friendly, article-specific

### Category Images  
- **Location**: `site/images/library/card-category-{category}.jpg`
- **Size**: 400x300px (4:3 aspect ratio)
- **Style**: Clean product photography

### Product Cards
- **Location**: `site/images/library/card-{product-slug}.jpg`
- **Current**: Text-based labels (TOYS, BAGS, etc.)
- **Status**: ✅ Working well, keeping as-is

## 🔄 Automatic Integration

### For New Articles
When you create new content, images are automatically generated based on:
- **Article Type Detection**: Comparison, How-to Guide, Product Review, etc.
- **Smart Prompts**: Custom prompts based on article title and content
- **Consistent Style**: All images match your eco-friendly brand

### Article Type Detection
- **Product Review**: "Best [Product]", "Review", "[Product Name]"
- **Comparison**: "vs", "comparison", "A vs B"  
- **How-To Guide**: "How to", "Guide", instructional content
- **Roundup**: "Best 10", "Top 5", numbered lists
- **General**: Everything else

## 🎨 Image Styles

### Professional Photography Style
- Clean, modern aesthetic
- Eco-friendly color palette (soft greens, natural tones)
- High-quality, web-optimized
- Consistent lighting and composition

### Content-Specific Elements
- **Dog Toys**: Natural materials, hemp, cotton, bamboo
- **Poop Bags**: Clean, biodegradable, eco-symbols
- **Comparisons**: Side-by-side layouts
- **How-To**: Instructional, people demonstrating
- **Roundups**: Flat lay arrangements

## 📊 Current Status

### ✅ What's Working
- **Product Cards**: Text-based images (TOYS, BAGS, etc.)
- **System Integration**: Ready for Gemini API
- **Manual Prompts**: Available for immediate use
- **Automatic Detection**: Article type recognition

### 🔄 What's Next
- Generate Gemini images for all 11 existing articles
- Create category card images
- Set up automatic generation for new content

## 🛠️ Technical Details

### Files Created
- `gemini_image_generator.py` - Main image generation class
- `generate_all_images.py` - Batch generation script  
- `gemini_image_prompts.md` - Detailed prompt documentation
- `manual_gemini_prompts.txt` - Copy-paste prompts for manual use
- `IMAGE_GENERATION_README.md` - This file

### Integration Points
- **app.py**: `generate_article_hero_image()` function
- **Content Pipeline**: Automatic image generation for new articles
- **Fallback System**: Text-based images if Gemini fails

## 💡 Usage Examples

### Generate Single Image
```python
from gemini_image_generator import GeminiImageGenerator

generator = GeminiImageGenerator()
image_path = generator.generate_article_image(
    "Best Eco-Friendly Dog Toys 2025",
    "eco-dog-toys-2025", 
    "product_review"
)
```

### Manual Prompt Example
```
Professional product photography of Eco-Friendly Dog Toys on a clean white background with natural lighting. Include hemp rope toys, organic cotton plush animals, and bamboo chew toys prominently displayed with eco-friendly elements like green leaves. Made from sustainable hemp rope and organic cotton. Professional commercial photography style, eco-friendly aesthetic. High resolution, professional quality, optimized for web display.

Save as: hero-eco-dog-toys-2025.jpg
```

## 🚨 Troubleshooting

### Common Issues
1. **Missing API Key**: Add `GEMINI_API_KEY` to `.env` file
2. **Import Errors**: Run `pip install google-generativeai pillow`
3. **Rate Limits**: Script includes automatic delays between generations
4. **Failed Generations**: Re-run the script, it skips existing images

### Fallback Options
- Manual generation using prompts file
- Keep existing text-based product cards
- Use placeholder images if generation fails

## 🎯 Next Steps

1. **Get your API key** and run the automated generation
2. **OR** use the manual prompts file to create images yourself
3. **Restart your server** to see the new images
4. **Create new articles** and watch them get automatic images!

---

**🌟 Your website will now have beautiful, custom images for every piece of content!** 