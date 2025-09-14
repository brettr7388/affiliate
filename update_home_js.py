#!/usr/bin/env python3
"""
Update home.js to add rotation containers to article cards
"""

def update_home_js():
    with open('site/js/home.js', 'r') as f:
        content = f.read()
    
    # Find and replace the article image section
    old_img = '<img src="${article.heroImage}" alt="${article.title}" class="w-full h-56 object-contain bg-gray-50 p-2" loading="lazy" decoding="async" onerror="this.src=\'/images/library/placeholder-article.jpg\'">'
    
    new_img = '<div data-product-category="${article.category || \'all\'}"><img src="${article.heroImage}" alt="${article.title}" class="w-full h-56 object-contain bg-gray-50 p-2" loading="lazy" decoding="async" onerror="this.src=\'/images/library/placeholder-article.jpg\'"></div>'
    
    updated_content = content.replace(old_img, new_img)
    
    # Also need to add category detection logic
    # Find the articles.map section and add category detection
    old_map_start = 'const articlesHTML = articles.map(article => `'
    
    new_map_start = '''// Add category detection for each article
    const articlesHTML = articles.map(article => {
        // Detect category from title and slug
        const title_lower = article.title.toLowerCase();
        const slug_lower = article.slug.toLowerCase();
        let category = 'all';
        
        if (title_lower.includes('toy') || title_lower.includes('play') || title_lower.includes('kong') || title_lower.includes('west paw') || slug_lower.includes('toy')) {
            category = 'toy';
        } else if (title_lower.includes('poop bag') || title_lower.includes('biodegradable') || title_lower.includes('waste') || title_lower.includes('bag') || slug_lower.includes('bag')) {
            category = 'bag';
        } else if (title_lower.includes('bowl') || title_lower.includes('feeding') || title_lower.includes('dish') || slug_lower.includes('bowl')) {
            category = 'bowl';
        } else if (title_lower.includes('leash') || title_lower.includes('walking') || title_lower.includes('lead') || slug_lower.includes('leash')) {
            category = 'leash';
        } else if (title_lower.includes('bed') || title_lower.includes('sleep') || title_lower.includes('comfort') || title_lower.includes('orthopedic') || slug_lower.includes('bed')) {
            category = 'bed';
        } else if (title_lower.includes('treat') || title_lower.includes('snack') || title_lower.includes('food') || slug_lower.includes('treat')) {
            category = 'treat';
        }
        
        return `'''
    
    updated_content = updated_content.replace(old_map_start, new_map_start)
    
    # Close the map function properly
    old_map_end = '    `).join(\'\');'
    new_map_end = '    `;'
    new_map_end += '    }).join(\'\');'
    
    updated_content = updated_content.replace(old_map_end, new_map_end)
    
    with open('site/js/home.js', 'w') as f:
        f.write(updated_content)
    
    print("✅ Updated home.js to add rotation containers to article cards!")

if __name__ == "__main__":
    update_home_js()
