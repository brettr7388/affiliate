#!/usr/bin/env python3
"""
Update home.js to use image rotation system for article cards
"""

def update_home_js():
    with open('site/js/home.js', 'r') as f:
        content = f.read()
    
    # Find the article image rendering section and update it
    old_article_img = '<img src="${article.heroImage}" alt="${article.title}" class="w-full h-56 object-contain bg-gray-50 p-2" loading="lazy" decoding="async" onerror="this.src=\'/images/library/placeholder-article.jpg\'">'
    
    new_article_img = '''<div data-product-category="${article.category || 'all'}">
                            <img src="${article.heroImage}" alt="${article.title}" class="w-full h-56 object-contain bg-gray-50 p-2" loading="lazy" decoding="async" onerror="this.src='/images/library/placeholder-article.jpg'">
                        </div>'''
    
    updated_content = content.replace(old_article_img, new_article_img)
    
    # Also need to add category detection to the article mapping
    # Find the articles.map section and add category detection
    old_articles_map = 'const articlesHTML = articles.map(article => `'
    
    new_articles_map = '''// Add category detection for each article
    const articlesHTML = articles.map(article => {
        // Detect category from title and slug
        const title_lower = article.title.toLowerCase();
        const slug_lower = article.slug.toLowerCase();
        let category = 'all';
        
        if (any(keyword in title_lower for keyword in ['toy', 'play', 'kong', 'west paw']) || 'toy' in slug_lower) {
            category = 'toy';
        } else if (any(keyword in title_lower for keyword in ['poop bag', 'biodegradable', 'waste', 'bag']) || 'bag' in slug_lower) {
            category = 'bag';
        } else if (any(keyword in title_lower for keyword in ['bowl', 'feeding', 'dish']) || 'bowl' in slug_lower) {
            category = 'bowl';
        } else if (any(keyword in title_lower for keyword in ['leash', 'walking', 'lead']) || 'leash' in slug_lower) {
            category = 'leash';
        } else if (any(keyword in title_lower for keyword in ['bed', 'sleep', 'comfort', 'orthopedic']) || 'bed' in slug_lower) {
            category = 'bed';
        } else if (any(keyword in title_lower for keyword in ['treat', 'snack', 'food']) || 'treat' in slug_lower) {
            category = 'treat';
        }
        
        return `'''
    
    updated_content = updated_content.replace(old_articles_map, new_articles_map)
    
    # Close the map function properly
    old_map_end = '    `).join(\'\');'
    new_map_end = '    `;
    }).join(\'\');'
    
    updated_content = updated_content.replace(old_map_end, new_map_end)
    
    with open('site/js/home.js', 'w') as f:
        f.write(updated_content)
    
    print("✅ Updated home.js to use image rotation system!")

if __name__ == "__main__":
    update_home_js()
