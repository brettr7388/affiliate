#!/usr/bin/env python3
"""
Update hero section to use rotating images from 'all' category
"""

def update_hero_section():
    with open('site/index.html', 'r') as f:
        content = f.read()
    
    # Find the hero image section and update it
    old_hero_img = '<img id="hero-image" src="/images/library/dog.jpg" alt="Happy dog with eco-friendly pet products" class="w-full h-auto rounded-2xl shadow-2xl" loading="lazy" decoding="async" width="600" height="400">'
    
    new_hero_img = '''<div id="hero-image-container" data-hero-category="all">
                        <img id="hero-image" src="/images/rotating/all/all1.png" alt="Eco-friendly pet products" class="w-full h-auto rounded-2xl shadow-2xl" loading="lazy" decoding="async" width="600" height="400">
                    </div>'''
    
    updated_content = content.replace(old_hero_img, new_hero_img)
    
    # Add the image rotation script to the homepage
    script_tag = '<script src="js/image-rotation.js"></script>'
    
    # Insert before closing body tag
    if '</body>' in updated_content:
        updated_content = updated_content.replace('</body>', f'{script_tag}\n</body>')
    else:
        updated_content += f'\n{script_tag}'
    
    with open('site/index.html', 'w') as f:
        f.write(updated_content)
    
    print("✅ Updated hero section to use rotating images!")

if __name__ == "__main__":
    update_hero_section()
