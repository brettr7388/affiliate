#!/usr/bin/env python3
"""
Setup rotating images for the Eco Pet Guide
Creates placeholder images and provides instructions for copying real images
"""

import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import textwrap

def create_placeholder_image(category, number, size=(400, 300)):
    """Create a placeholder image for testing"""
    # Create a new image with a gradient background
    img = Image.new('RGB', size, color='#f0f8f0')
    draw = ImageDraw.Draw(img)
    
    # Add a subtle gradient effect
    for y in range(size[1]):
        color_value = int(240 - (y / size[1]) * 40)
        draw.line([(0, y), (size[0], y)], fill=(color_value, 248, color_value))
    
    # Add border
    draw.rectangle([0, 0, size[0]-1, size[1]-1], outline='#28a745', width=3)
    
    # Add text
    try:
        # Try to use a nice font
        font_large = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 24)
        font_small = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 16)
    except:
        # Fallback to default font
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Main text
    text = f"Eco-Friendly {category.title()}"
    text_width = draw.textlength(text, font=font_large)
    text_x = (size[0] - text_width) // 2
    text_y = size[1] // 2 - 20
    draw.text((text_x, text_y), text, fill='#28a745', font=font_large)
    
    # Subtitle
    subtitle = f"Image {number} - Rotating Display"
    subtitle_width = draw.textlength(subtitle, font=font_small)
    subtitle_x = (size[0] - subtitle_width) // 2
    subtitle_y = text_y + 35
    draw.text((subtitle_x, subtitle_y), subtitle, fill='#666666', font=font_small)
    
    # Add emoji based on category
    emoji_map = {
        'toy': '🧸',
        'bag': '🛍️',
        'bowl': '🥣',
        'leash': '🦮',
        'bed': '🛏️',
        'treat': '��',
        'all': '🌱'
    }
    
    emoji = emoji_map.get(category, '🌱')
    emoji_size = 40
    emoji_x = (size[0] - emoji_size) // 2
    emoji_y = text_y - 60
    draw.text((emoji_x, emoji_y), emoji, font=ImageFont.load_default())
    
    return img

def setup_image_directories():
    """Create the image directory structure and placeholder images"""
    base_path = Path("site/images/rotating")
    
    categories = {
        'toy': 4,    # 4 images for toys
        'bag': 3,
        'bowl': 3,
        'leash': 3,
        'bed': 3,
        'treat': 3,
        'all': 3
    }
    
    print("🔄 Setting up image rotation directories...")
    
    for category, count in categories.items():
        category_path = base_path / category
        category_path.mkdir(parents=True, exist_ok=True)
        
        print(f"📁 Created directory: {category_path}")
        
        # Create placeholder images
        for i in range(1, count + 1):
            img = create_placeholder_image(category, i)
            img_path = category_path / f"{category}{i}.png"
            img.save(img_path, 'PNG')
            print(f"   ✅ Created placeholder: {img_path}")
    
    print(f"\n✅ Setup complete! Created {sum(categories.values())} placeholder images.")
    
    # Create instructions file
    instructions = """
# Image Rotation Setup Instructions

## Current Status
✅ Image rotation system implemented
✅ All articles updated with rotation code
✅ Directory structure created
✅ Placeholder images generated

## Next Steps

### 1. Replace Placeholder Images
Copy your generated images to the appropriate directories:

```
site/images/rotating/
├── toy/
│   ├── toy1.png  ← Replace with your toy image 1
│   ├── toy2.png  ← Replace with your toy image 2
│   ├── toy3.png  ← Replace with your toy image 3
│   └── toy4.png  ← Replace with your toy image 4
├── bag/
│   ├── bag1.png  ← Replace with your bag image 1
│   ├── bag2.png  ← Replace with your bag image 2
│   └── bag3.png  ← Replace with your bag image 3
├── bowl/
│   ├── bowl1.png ← Replace with your bowl image 1
│   ├── bowl2.png ← Replace with your bowl image 2
│   └── bowl3.png ← Replace with your bowl image 3
├── leash/
│   ├── leash1.png ← Replace with your leash image 1
│   ├── leash2.png ← Replace with your leash image 2
│   └── leash3.png ← Replace with your leash image 3
├── bed/
│   ├── bed1.png  ← Replace with your bed image 1
│   ├── bed2.png  ← Replace with your bed image 2
│   └── bed3.png  ← Replace with your bed image 3
├── treat/
│   ├── treat1.png ← Replace with your treat image 1
│   ├── treat2.png ← Replace with your treat image 2
│   └── treat3.png ← Replace with your treat image 3
└── all/
    ├── all1.png  ← Replace with your general image 1
    ├── all2.png  ← Replace with your general image 2
    └── all3.png  ← Replace with your general image 3
```

### 2. How It Works
- Images rotate automatically on page refresh
- Each category shows the appropriate images
- Same image displays for the entire day (consistent experience)
- Manual refresh button available on each page

### 3. Testing
1. Open any article in your browser
2. Refresh the page to see different images
3. Use the "🔄 Refresh Images" button for manual rotation
4. Check that the correct category images appear

### 4. Categories by Article Type
- **Toy articles**: Show toy1.png, toy2.png, toy3.png, toy4.png
- **Bag articles**: Show bag1.png, bag2.png, bag3.png
- **Bowl articles**: Show bowl1.png, bowl2.png, bowl3.png
- **Leash articles**: Show leash1.png, leash2.png, leash3.png
- **Bed articles**: Show bed1.png, bed2.png, bed3.png
- **Treat articles**: Show treat1.png, treat2.png, treat3.png
- **General articles**: Show all1.png, all2.png, all3.png

## File Naming Convention
Make sure your images follow this exact naming:
- `{category}{number}.png`
- Examples: `toy1.png`, `bag2.png`, `bowl3.png`, etc.
"""
    
    with open("IMAGE_ROTATION_SETUP.md", "w") as f:
        f.write(instructions)
    
    print(f"\n📝 Created setup instructions: IMAGE_ROTATION_SETUP.md")

if __name__ == "__main__":
    setup_image_directories()
