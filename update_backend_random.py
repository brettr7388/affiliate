#!/usr/bin/env python3
"""
Update backend to use random image selection
"""

def update_backend_random():
    with open('app.py', 'r') as f:
        content = f.read()
    
    # Add random image selection function
    random_function = '''
def get_random_image_for_category(category):
    """Get a random image for the given category"""
    import random
    
    category_images = {
        'toy': ['toy1.png', 'toy2.png', 'toy3.png', 'toy4.png'],
        'bag': ['bag1.png', 'bag2.png', 'bag3.png'],
        'bowl': ['bowl1.png', 'bowl2.png', 'bowl3.png'],
        'leash': ['leash1.png', 'leash2.png', 'leash3.png'],
        'bed': ['bed1.png', 'bed2.png', 'bed3.png'],
        'treat': ['treat1.png', 'treat2.png', 'treat3.png'],
        'all': ['all1.png', 'all2.png', 'all3.png']
    }
    
    images = category_images.get(category, ['all1.png'])
    return random.choice(images)

'''
    
    # Insert the function before detect_article_category
    insert_point = content.find('def detect_article_category(title, slug):')
    content = content[:insert_point] + random_function + content[insert_point:]
    
    # Update the heroImage line to use random selection
    old_hero_line = 'heroImage=f"/images/rotating/{article_category}/{article_category}1.png",  # Rotating image system'
    new_hero_line = 'heroImage=f"/images/rotating/{article_category}/{get_random_image_for_category(article_category)}",  # Random image system'
    
    content = content.replace(old_hero_line, new_hero_line)
    
    with open('app.py', 'w') as f:
        f.write(content)
    
    print("✅ Updated backend to use random image selection!")

if __name__ == "__main__":
    update_backend_random()
