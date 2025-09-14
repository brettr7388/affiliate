#!/usr/bin/env python3
"""
Update featured routes to use rotating images
"""

def fix_featured_routes():
    with open('app.py', 'r') as f:
        content = f.read()
    
    # Find and replace the get_featured_routes function
    old_function = '''def get_featured_routes(limit: int = 6):
    """Get featured affiliate routes"""
    # Map of route slugs to new image names
    image_mapping = {
        "biodegradable-poop-bags": "bag.jpg",
        "hemp-dog-leash": "leash.jpg", 
        "organic-dog-treats": "treats.jpg",
        "recycled-dog-bed": "bed.jpg",
        "sustainable-dog-bowls": "bowl.jpg",
        "eco-dog-toys-2025": "toy.jpg"
    }
    
    with engine.begin() as conn:
        rows = conn.execute(text("""
            SELECT slug, offer, dest_url 
            FROM routes 
            ORDER BY slug 
            LIMIT :limit
        """), {"limit": limit}).all()
    
    return [
        FeaturedRoute(
            slug=slug,
            label=offer,
            dest_url=f"/r/{slug}",
            image=f"/images/library/{image_mapping.get(slug, f'card-{slug}.jpg')}"
        )
        for slug, offer, dest_url in rows
    ]'''
    
    new_function = '''def get_featured_routes(limit: int = 6):
    """Get featured affiliate routes"""
    # Map of route slugs to categories for rotating images
    category_mapping = {
        "biodegradable-poop-bags": "bag",
        "hemp-dog-leash": "leash", 
        "organic-dog-treats": "treat",
        "recycled-dog-bed": "bed",
        "sustainable-dog-bowls": "bowl",
        "eco-dog-toys-2025": "toy"
    }
    
    with engine.begin() as conn:
        rows = conn.execute(text("""
            SELECT slug, offer, dest_url 
            FROM routes 
            ORDER BY slug 
            LIMIT :limit
        """), {"limit": limit}).all()
    
    return [
        FeaturedRoute(
            slug=slug,
            label=offer,
            dest_url=f"/r/{slug}",
            image=f"/images/rotating/{category_mapping.get(slug, 'all')}/{get_random_image_for_category(category_mapping.get(slug, 'all'))}"
        )
        for slug, offer, dest_url in rows
    ]'''
    
    updated_content = content.replace(old_function, new_function)
    
    with open('app.py', 'w') as f:
        f.write(updated_content)
    
    print("✅ Updated featured routes to use rotating images!")

if __name__ == "__main__":
    fix_featured_routes()
