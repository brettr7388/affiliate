#!/usr/bin/env python3
"""
Demo Setup Script for Eco Pet Guide
Prepares the application with sample data for demo recording
"""

import os
import sys
import sqlite3
import datetime as dt
from pathlib import Path

def setup_demo_environment():
    """Set up the demo environment with sample data"""
    print("🎬 Setting up demo environment...")
    
    # Check if we're in the right directory
    if not os.path.exists('app.py'):
        print("❌ Error: Please run this script from the affiliate project root directory")
        sys.exit(1)
    
    # Initialize database
    setup_database()
    
    # Create sample routes
    create_sample_routes()
    
    # Generate sample content
    create_sample_content()
    
    # Set up demo configuration
    setup_demo_config()
    
    print("✅ Demo environment ready!")
    print("\n🚀 To start the demo:")
    print("   python start_admin.py")
    print("   Open: http://127.0.0.1:8088")
    print("   Admin: http://127.0.0.1:8088/admin")

def setup_database():
    """Initialize database with demo data"""
    print("📊 Setting up database...")
    
    # Connect to database
    conn = sqlite3.connect('affiliate.db')
    cursor = conn.cursor()
    
    # Create tables if they don't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clicks(
            id TEXT PRIMARY KEY,
            created_at TEXT,
            offer TEXT,
            variant TEXT,
            dest_url TEXT,
            ip TEXT,
            ua TEXT,
            referrer TEXT,
            utm_source TEXT,
            utm_medium TEXT,
            utm_campaign TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS routes(
            slug TEXT PRIMARY KEY,
            offer TEXT,
            variant TEXT,
            dest_url TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS newsletter_subscribers(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            subscribed_at TEXT NOT NULL,
            ip_address TEXT,
            user_agent TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def create_sample_routes():
    """Create sample affiliate routes for demo"""
    print("🔗 Creating sample routes...")
    
    sample_routes = [
        {
            'slug': 'eco-dog-toys-2025',
            'offer': 'Best Eco-Friendly Dog Toys 2025',
            'dest_url': 'https://amazon.com/dp/B08N5WRWNW?tag=YOUR-AMAZON-ASSOCIATES-TAG'
        },
        {
            'slug': 'biodegradable-poop-bags',
            'offer': 'Biodegradable Dog Poop Bags',
            'dest_url': 'https://amazon.com/dp/B07XYZ123?tag=YOUR-AMAZON-ASSOCIATES-TAG'
        },
        {
            'slug': 'hemp-dog-leash',
            'offer': 'Hemp Dog Leash - Sustainable Walking',
            'dest_url': 'https://amazon.com/dp/B06ABC789?tag=YOUR-AMAZON-ASSOCIATES-TAG'
        },
        {
            'slug': 'organic-dog-treats',
            'offer': 'Organic Dog Treats - All Natural',
            'dest_url': 'https://amazon.com/dp/B09DEF456?tag=YOUR-AMAZON-ASSOCIATES-TAG'
        },
        {
            'slug': 'recycled-dog-bed',
            'offer': 'Recycled Dog Bed - Eco Comfort',
            'dest_url': 'https://amazon.com/dp/B12GHI789?tag=YOUR-AMAZON-ASSOCIATES-TAG'
        },
        {
            'slug': 'sustainable-dog-bowls',
            'offer': 'Sustainable Dog Bowls - Bamboo & Stainless',
            'dest_url': 'https://amazon.com/dp/B15JKL012?tag=YOUR-AMAZON-ASSOCIATES-TAG'
        }
    ]
    
    conn = sqlite3.connect('affiliate.db')
    cursor = conn.cursor()
    
    for route in sample_routes:
        cursor.execute('''
            INSERT OR REPLACE INTO routes (slug, offer, variant, dest_url)
            VALUES (?, ?, 'A', ?)
        ''', (route['slug'], route['offer'], route['dest_url']))
    
    conn.commit()
    conn.close()

def create_sample_content():
    """Create sample articles and content for demo"""
    print("📝 Creating sample content...")
    
    # Ensure content directory exists
    content_dir = Path('site/content')
    content_dir.mkdir(exist_ok=True)
    
    # Sample articles
    sample_articles = [
        {
            'slug': 'best-eco-friendly-dog-toys-2025',
            'title': 'Best Eco-Friendly Dog Toys 2025: Sustainable Play for Your Pup',
            'content': '''# Best Eco-Friendly Dog Toys 2025: Sustainable Play for Your Pup

When it comes to choosing toys for our furry friends, sustainability should be a top priority. Eco-friendly dog toys are not only better for the environment, but they're often safer and more durable than their plastic counterparts.

## Why Choose Eco-Friendly Dog Toys?

Eco-friendly dog toys are made from sustainable materials like:
- Recycled rubber
- Hemp fiber
- Bamboo
- Natural cotton

These materials are biodegradable, non-toxic, and safe for your dog to play with.

## Our Top Picks for 2025

### 1. West Paw Zogoflex Toys
Made from recycled materials and fully recyclable at end of life.

### 2. Kong Classic
The original eco-friendly rubber toy that's been trusted for decades.

### 3. Planet Dog Orbee-Tuff
Made from recycled plastic and designed to last.

## How to Choose the Right Eco Toy

Consider your dog's:
- Size and chewing strength
- Play style
- Environmental impact preferences

## Conclusion

Choosing eco-friendly dog toys is a simple way to reduce your pet's environmental pawprint while keeping them happy and healthy.

*As an Amazon Associate, I earn from qualifying purchases.*
'''
        },
        {
            'slug': 'biodegradable-dog-poop-bags-guide',
            'title': 'The Complete Guide to Biodegradable Dog Poop Bags',
            'content': '''# The Complete Guide to Biodegradable Dog Poop Bags

Dog poop bags are a necessity for responsible pet ownership, but traditional plastic bags can take hundreds of years to decompose. Biodegradable poop bags offer a more sustainable solution.

## What Makes a Bag Biodegradable?

True biodegradable bags are made from:
- Cornstarch
- Vegetable-based materials
- PLA (polylactic acid)

These materials break down naturally in composting conditions.

## Best Biodegradable Poop Bag Brands

### 1. Earth Rated Poop Bags
- Made from recycled plastic
- Scented with lavender
- Extra thick and leak-proof

### 2. BioBag Compostable Bags
- Certified compostable
- Made from renewable resources
- Strong and reliable

### 3. Pooch Paper
- Made from recycled newspaper
- Completely biodegradable
- Lightweight and compact

## How to Use Biodegradable Bags

1. Store in a dry place
2. Use within the expiration date
3. Dispose properly in compost or trash

## Environmental Impact

Switching to biodegradable bags can significantly reduce your dog's environmental impact and help keep our planet clean for future generations.

*As an Amazon Associate, I earn from qualifying purchases.*
'''
        }
    ]
    
    for article in sample_articles:
        # Create markdown file
        md_file = content_dir / f"{article['slug']}.md"
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(article['content'])
        
        # Create HTML file
        html_file = content_dir / f"{article['slug']}.html"
        html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{article['title']}</title>
    <meta name="description" content="Learn about {article['title'].lower()}">
</head>
<body>
    <h1>{article['title']}</h1>
    <div class="content">
        {article['content'].replace('# ', '<h2>').replace(chr(10) + '# ', '</h2>' + chr(10) + '<h2>')}
    </div>
</body>
</html>'''
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

def setup_demo_config():
    """Set up demo configuration"""
    print("⚙️ Setting up demo configuration...")
    
    # Create demo environment file
    env_content = '''# Demo Environment Configuration
ADMIN_TOKEN=demo-admin-token-2025
DATABASE_URL=sqlite:///./affiliate.db
ENV=demo
AFFILIATE_DISCLOSURE="As an Amazon Associate I earn from qualifying purchases."
OPENAI_API_KEY=your-openai-api-key-here
GEMINI_API_KEY=your-gemini-api-key-here
'''
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("📋 Demo configuration created!")
    print("   - Admin token: demo-admin-token-2025")
    print("   - Database: SQLite (affiliate.db)")
    print("   - Environment: demo")

def add_sample_clicks():
    """Add sample click data for demo analytics"""
    print("📊 Adding sample click data...")
    
    conn = sqlite3.connect('affiliate.db')
    cursor = conn.cursor()
    
    # Add sample clicks over the past week
    import random
    from datetime import timedelta
    
    now = dt.datetime.now()
    routes = ['eco-dog-toys-2025', 'biodegradable-poop-bags', 'hemp-dog-leash']
    
    for i in range(50):  # 50 sample clicks
        # Random time in past week
        click_time = now - timedelta(days=random.randint(0, 7), hours=random.randint(0, 23))
        
        route = random.choice(routes)
        ip = f"192.168.1.{random.randint(1, 255)}"
        user_agent = random.choice([
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15"
        ])
        
        cursor.execute('''
            INSERT INTO clicks (id, created_at, offer, variant, dest_url, ip, ua, referrer)
            VALUES (?, ?, ?, 'A', ?, ?, ?, ?)
        ''', (
            f"demo-click-{i:03d}",
            click_time.isoformat(),
            route,
            f"https://amazon.com/dp/B08N5WRWNW?tag=YOUR-AMAZON-ASSOCIATES-TAG",
            ip,
            user_agent,
            random.choice(["google.com", "facebook.com", "pinterest.com", "direct"])
        ))
    
    conn.commit()
    conn.close()

def add_sample_subscribers():
    """Add sample newsletter subscribers"""
    print("📧 Adding sample subscribers...")
    
    conn = sqlite3.connect('affiliate.db')
    cursor = conn.cursor()
    
    sample_emails = [
        "demo@example.com",
        "petlover@demo.com",
        "ecodog@sample.org",
        "sustainablepets@demo.net"
    ]
    
    for email in sample_emails:
        cursor.execute('''
            INSERT OR IGNORE INTO newsletter_subscribers (email, subscribed_at, ip_address, user_agent)
            VALUES (?, ?, ?, ?)
        ''', (
            email,
            dt.datetime.now().isoformat(),
            "192.168.1.100",
            "Demo Setup"
        ))
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    setup_demo_environment()
    add_sample_clicks()
    add_sample_subscribers()
    print("\n🎉 Demo setup complete!")
    print("\n📝 Next steps:")
    print("1. Run: python start_admin.py")
    print("2. Open: http://127.0.0.1:8088")
    print("3. Admin: http://127.0.0.1:8088/admin")
    print("4. Token: demo-admin-token-2025")
