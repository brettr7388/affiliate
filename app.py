import os
import uuid
import datetime as dt
import re
import glob
import json
import random
import hashlib
from urllib.parse import urlencode, urlparse, urlunparse, parse_qsl
from typing import List, Optional
from pathlib import Path

from fastapi import FastAPI, Request, HTTPException, Query
from fastapi.responses import RedirectResponse, JSONResponse, HTMLResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from image_library import image_library

# Try to import Gemini image generator
try:
    from gemini_image_generator import GeminiImageGenerator
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("⚠️  Gemini image generator not available. Install google-generativeai and set GEMINI_API_KEY to enable automatic image generation.")

# Load environment variables from a .env file if present
load_dotenv()

# Use SQLite by default; override via the DATABASE_URL env var
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./affiliate.db")
engine = create_engine(DATABASE_URL, future=True)

app = FastAPI()

# Admin authentication
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

def require_admin(request: Request):
    """Check if request has valid admin token"""
    token = request.headers.get("X-Admin-Token") or request.query_params.get("token")
    if ADMIN_TOKEN and token != ADMIN_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")

def init_db() -> None:
    """Create required tables if they don't already exist."""
    with engine.begin() as conn:
        conn.execute(
            text(
                """
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
        );
        """
            )
        )
        conn.execute(
            text(
                """
        CREATE TABLE IF NOT EXISTS routes(
          slug TEXT PRIMARY KEY,
          offer TEXT,
          variant TEXT,
          dest_url TEXT
        );
        """
            )
        )
        
        # Create newsletter_subscribers table (auto-detect database type)
        if "postgres" in DATABASE_URL:
            # PostgreSQL/Supabase syntax
            conn.execute(
                text(
                    """
            CREATE TABLE IF NOT EXISTS newsletter_subscribers(
              id SERIAL PRIMARY KEY,
              email VARCHAR(255) UNIQUE NOT NULL,
              subscribed_at TIMESTAMP NOT NULL,
              ip_address VARCHAR(45),
              user_agent TEXT
            );
            """
                )
            )
        else:
            # SQLite syntax
            conn.execute(
                text(
                    """
            CREATE TABLE IF NOT EXISTS newsletter_subscribers(
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              email TEXT UNIQUE NOT NULL,
              subscribed_at TEXT NOT NULL,
              ip_address TEXT,
              user_agent TEXT
            );
            """
                )
            )

init_db()

# Run startup fixes for production database
try:
    from startup_fixes import run_startup_fixes
    run_startup_fixes()
except ImportError:
    print("Startup fixes module not found, skipping...")
except Exception as e:
    print(f"Startup fixes error: {e}")

class Article(BaseModel):
    slug: str
    title: str
    excerpt: str
    heroImage: Optional[str] = None
    tags: List[str] = []
    publishedAt: str
    estimatedReadMin: int = 5

class ArticleResponse(BaseModel):
    items: List[Article]
    total: int

class FeaturedRoute(BaseModel):
    slug: str
    label: str
    dest_url: str
    image: Optional[str] = None

class ClickData(BaseModel):
    slug: str
    href: str
    utm: Optional[dict] = None
    event_type: str = "click"

class ABTestData(BaseModel):
    area: str
    variant: str
    action: str = "impression"  # impression or convert

class NewsletterSubscription(BaseModel):
    email: str

class ProductComparison(BaseModel):
    category: str
    title: str
    description: str
    products: List[dict]
    display_type: str = "table"  # "table" or "cards"


def detect_article_category(title, slug):
    """Detect the main product category from article title and slug"""
    title_lower = title.lower()
    slug_lower = slug.lower()
    
    # Check for specific product categories
    if any(keyword in title_lower for keyword in ['toy', 'play', 'kong', 'west paw']) or 'toy' in slug_lower:
        return 'toy'
    elif any(keyword in title_lower for keyword in ['poop bag', 'biodegradable', 'waste', 'bag']) or 'bag' in slug_lower:
        return 'bag'
    elif any(keyword in title_lower for keyword in ['bowl', 'feeding', 'dish']) or 'bowl' in slug_lower:
        return 'bowl'
    elif any(keyword in title_lower for keyword in ['leash', 'walking', 'lead']) or 'leash' in slug_lower:
        return 'leash'
    elif any(keyword in title_lower for keyword in ['bed', 'sleep', 'comfort', 'orthopedic']) or 'bed' in slug_lower:
        return 'bed'
    elif any(keyword in title_lower for keyword in ['treat', 'snack', 'food']) or 'treat' in slug_lower:
        return 'treat'
    else:
        return 'all'  # Default for general articles

def parse_markdown_file(filepath: str) -> Optional[Article]:
    """Parse a markdown file and extract article metadata"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract title from first # heading
        title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else os.path.basename(filepath).replace('.md', '').replace('-', ' ').title()
        
        # Create slug from filename
        slug = os.path.basename(filepath).replace('.md', '')
        
        # Extract excerpt (first paragraph after title)
        lines = content.split('\n')
        excerpt = ""
        for line in lines[2:]:  # Skip title and empty line
            line = line.strip()
            if line and not line.startswith('#') and not line.startswith('>'):
                excerpt = line[:150] + "..." if len(line) > 150 else line
                break
        
        # Extract tags from filename patterns
        tags = []
        if 'poop-bag' in slug:
            tags.append("Poop Bags")
        if 'toy' in slug:
            tags.append("Toys")
        if 'guide' in slug:
            tags.append("Guides")
        if 'comparison' in slug or 'vs' in slug:
            tags.append("Comparisons")
        
        # Get file modification time as published date
        mtime = os.path.getmtime(filepath)
        published_at = dt.datetime.fromtimestamp(mtime).isoformat() + 'Z'
        
        # Estimate read time based on content length
        word_count = len(content.split())
        read_min = max(1, word_count // 200)  # Assume 200 words per minute
        
        # Determine article category for rotating images
        article_category = detect_article_category(title, slug)
        
        return Article(
            slug=slug,
            title=title,
            excerpt=excerpt,
            heroImage=f"/images/rotating/{article_category}/{article_category}1.png",  # Rotating image system
            tags=tags,
            publishedAt=published_at,
            estimatedReadMin=read_min
        )
    except Exception as e:
        print(f"Error parsing {filepath}: {e}")
        return None

def get_all_articles(shuffle_seed: Optional[str] = None) -> List[Article]:
    """Get all articles from the content directory with smart shuffling"""
    articles = []
    content_dir = "site/content"
    
    if os.path.exists(content_dir):
        for md_file in glob.glob(os.path.join(content_dir, "*.md")):
            article = parse_markdown_file(md_file)
            if article:
                articles.append(article)
    
    if shuffle_seed:
        # Use deterministic shuffling based on seed for consistent results per session
        random.seed(shuffle_seed)
        
        # Separate articles into quality tiers for smart shuffling
        high_quality = []
        regular = []
        
        for article in articles:
            # High quality indicators
            is_high_quality = (
                len(article.title) > 30 and  # Detailed titles
                any(keyword in article.title.lower() for keyword in [
                    'best', 'top', 'guide', 'review', 'vs', 'comparison', '2025'
                ]) or
                any(tag in article.tags for tag in ['Guides', 'Reviews', 'Comparisons'])
            )
            
            if is_high_quality:
                high_quality.append(article)
            else:
                regular.append(article)
        
        # Shuffle each tier separately
        random.shuffle(high_quality)
        random.shuffle(regular)
        
        # Interleave high quality articles throughout the list
        shuffled_articles = []
        regular_iter = iter(regular)
        
        for i, hq_article in enumerate(high_quality):
            # Add high quality article
            shuffled_articles.append(hq_article)
            
            # Add 2-3 regular articles after each high quality one
            for _ in range(random.randint(2, 3)):
                try:
                    shuffled_articles.append(next(regular_iter))
                except StopIteration:
                    break
        
        # Add any remaining regular articles
        shuffled_articles.extend(list(regular_iter))
        
        return shuffled_articles
    else:
        # Default: Sort by published date, newest first
        articles.sort(key=lambda x: x.publishedAt, reverse=True)
        return articles

def generate_article_hero_image(article_title: str, article_slug: str) -> bool:
    """Generate a hero image for an article using Gemini"""
    if not GEMINI_AVAILABLE:
        return False
    
    try:
        generator = GeminiImageGenerator()
        
        # Determine article type from title
        article_type = 'general_article'
        title_lower = article_title.lower()
        
        if 'vs' in title_lower or 'comparison' in title_lower:
            article_type = 'comparison'
        elif 'how to' in title_lower or 'guide' in title_lower:
            article_type = 'how_to_guide'
        elif any(num in title_lower for num in ['5', '10', '15', '20']) and ('best' in title_lower or 'top' in title_lower):
            article_type = 'roundup'
        elif 'review' in title_lower or 'product' in title_lower:
            article_type = 'product_review'
        
        filepath = generator.generate_article_image(article_title, article_slug, article_type)
        return filepath is not None
        
    except Exception as e:
        print(f"Error generating Gemini image for {article_slug}: {e}")
        return False

def create_product_card_image(slug: str, product_name: str) -> bool:
    """Create a product card image with appropriate emoji/icon"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # Create image with eco-friendly gradient background
        img = Image.new('RGB', (400, 300), (240, 248, 255))
        draw = ImageDraw.Draw(img)
        
        # Add gradient effect
        for y in range(300):
            color_ratio = y / 300
            r = int(240 + (220 - 240) * color_ratio)
            g = int(248 + (255 - 248) * color_ratio)
            b = int(255 + (240 - 255) * color_ratio)
            draw.line([(0, y), (400, y)], fill=(r, g, b))
        
        # Determine icon text based on product type (using simple text instead of emojis for better compatibility)
        icon_text = 'DOG'  # default
        product_lower = product_name.lower()
        if 'poop' in product_lower or 'bag' in product_lower:
            icon_text = 'BAGS'
        elif 'toy' in product_lower:
            icon_text = 'TOYS'
        elif 'bowl' in product_lower or 'food' in product_lower:
            icon_text = 'BOWLS'
        elif 'leash' in product_lower:
            icon_text = 'LEASH'
        elif 'treat' in product_lower:
            icon_text = 'TREATS'
        elif 'bed' in product_lower:
            icon_text = 'BED'
        elif 'eco' in product_lower or 'green' in product_lower:
            icon_text = 'ECO'
        
        # Try to use system fonts
        try:
            font_large = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 48)
            font_small = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 16)
        except:
            try:
                font_large = ImageFont.truetype('/System/Library/Fonts/Arial.ttf', 48)
                font_small = ImageFont.truetype('/System/Library/Fonts/Arial.ttf', 16)
            except:
                font_large = ImageFont.load_default()
                font_small = ImageFont.load_default()
        
        # Draw icon text in center
        icon_bbox = draw.textbbox((0, 0), icon_text, font=font_large)
        icon_width = icon_bbox[2] - icon_bbox[0]
        icon_height = icon_bbox[3] - icon_bbox[1]
        icon_x = (400 - icon_width) // 2
        icon_y = (300 - icon_height) // 2 - 20
        
        draw.text((icon_x, icon_y), icon_text, font=font_large, fill=(22, 163, 74))
        
        # Draw product name at bottom
        words = product_name.split()
        if len(words) > 3:
            # Split into two lines
            mid = len(words) // 2
            line1 = ' '.join(words[:mid])
            line2 = ' '.join(words[mid:])
            
            line1_bbox = draw.textbbox((0, 0), line1, font=font_small)
            line2_bbox = draw.textbbox((0, 0), line2, font=font_small)
            
            line1_width = line1_bbox[2] - line1_bbox[0]
            line2_width = line2_bbox[2] - line2_bbox[0]
            
            draw.text(((400 - line1_width) // 2, 250), line1, font=font_small, fill=(55, 65, 81))
            draw.text(((400 - line2_width) // 2, 270), line2, font=font_small, fill=(55, 65, 81))
        else:
            text_bbox = draw.textbbox((0, 0), product_name, font=font_small)
            text_width = text_bbox[2] - text_bbox[0]
            draw.text(((400 - text_width) // 2, 260), product_name, font=font_small, fill=(55, 65, 81))
        
        # Ensure directory exists
        os.makedirs("site/images/library", exist_ok=True)
        
        # Save image
        filename = f'site/images/library/card-{slug}.jpg'
        img.save(filename)
        print(f'Created product image: {filename}')
        return True
        
    except Exception as e:
        print(f'Error creating product image for {slug}: {e}')
        return False

class Route(BaseModel):
    slug: str
    offer: str
    variant: str = "A"
    dest_url: str

# Public API endpoints for homepage
@app.get("/api/articles", response_model=ArticleResponse)
def get_articles(
    limit: int = Query(24, ge=1, le=100),
    offset: int = Query(0, ge=0),
    tag: Optional[str] = Query(None),
    sort: str = Query("new", pattern="^(new|popular|shuffled)$"),
    request: Request = None
):
    """Get articles with pagination and filtering"""
    
    # Generate a shuffle seed based on user session for consistent ordering per session
    shuffle_seed = None
    if sort == "shuffled":
        # Create seed from IP + User-Agent + current hour for session consistency
        user_ip = request.client.host if request else "unknown"
        user_agent = request.headers.get("user-agent", "") if request else ""
        current_hour = dt.datetime.now().strftime("%Y%m%d%H")  # Changes every hour
        
        # Create deterministic seed that changes hourly but is consistent per user per hour
        seed_string = f"{user_ip}_{user_agent}_{current_hour}"
        shuffle_seed = hashlib.md5(seed_string.encode()).hexdigest()[:8]
    
    articles = get_all_articles(shuffle_seed=shuffle_seed)
    
    # Filter by tag if specified
    if tag:
        articles = [a for a in articles if tag in a.tags]
    
    # Handle different sort types
    if sort == "popular":
        # For now, just return newest since we don't have view counts
        # In production, you'd join with click data
        articles.sort(key=lambda x: x.publishedAt, reverse=True)
    elif sort == "new":
        # Explicit newest first sorting
        articles.sort(key=lambda x: x.publishedAt, reverse=True)
    # shuffled is already handled by get_all_articles with shuffle_seed
    
    # Apply pagination
    total = len(articles)
    paginated_articles = articles[offset:offset + limit]
    
    return ArticleResponse(items=paginated_articles, total=total)

@app.get("/api/stats/top")
def get_top_articles(window: str = "7d", limit: int = 6):
    """Get top articles by clicks in the specified time window"""
    try:
        # Parse window (7d, 30d, etc.)
        days = int(window.replace('d', ''))
        since = (dt.datetime.utcnow() - dt.timedelta(days=days)).isoformat()
        
        with engine.begin() as conn:
            # Get top clicked offers (these map to article slugs)
            rows = conn.execute(text("""
                SELECT offer, COUNT(*) as clicks
                FROM clicks 
                WHERE created_at >= :since
                GROUP BY offer
                ORDER BY clicks DESC
                LIMIT :limit
            """), {"since": since, "limit": limit}).all()
        
        # Return just the slugs for now
        return [{"slug": offer, "clicks": clicks} for offer, clicks in rows]
    except Exception as e:
        # Fallback to recent articles if no click data
        articles = get_all_articles()
        return [{"slug": a.slug, "clicks": 0} for a in articles[:limit]]

@app.get("/api/routes/featured")
def get_featured_routes(limit: int = 6):
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
    ]

@app.post("/api/clicks")
async def track_click(click_data: ClickData, request: Request):
    """Track clicks for analytics"""
    try:
        click_id = str(uuid.uuid4())
        utm = click_data.utm or {}
        
        with engine.begin() as conn:
            conn.execute(
                text("""
                INSERT INTO clicks(
                    id, created_at, offer, variant, dest_url, ip, ua, referrer,
                    utm_source, utm_medium, utm_campaign
                )
                VALUES(:id, :ts, :offer, :variant, :dest, :ip, :ua, :ref, :us, :um, :uc)
                """),
                {
                    "id": click_id,
                    "ts": dt.datetime.utcnow().isoformat(),
                    "offer": click_data.slug,
                    "variant": "A",  # Default variant
                    "dest": click_data.href,
                    "ip": request.client.host if request.client else None,
                    "ua": request.headers.get("User-Agent"),
                    "ref": request.headers.get("Referer"),
                    "us": utm.get("utm_source"),
                    "um": utm.get("utm_medium"),
                    "uc": utm.get("utm_campaign"),
                }
            )
        
        return {"ok": True}
    except Exception as e:
        # Don't fail the request if tracking fails
        print(f"Click tracking error: {e}")
        return {"ok": False, "error": str(e)}

@app.post("/api/ab/impression")
async def track_ab_impression(ab_data: ABTestData, request: Request):
    """Track A/B test impressions"""
    # For now, just log to console. In production, store in database
    print(f"A/B Test Impression: {ab_data.area} - {ab_data.variant}")
    return {"ok": True}

@app.post("/api/ab/convert")  
async def track_ab_conversion(ab_data: ABTestData, request: Request):
    """Track A/B test conversions"""
    # For now, just log to console. In production, store in database
    print(f"A/B Test Conversion: {ab_data.area} - {ab_data.variant}")
    return {"ok": True}

@app.post("/api/newsletter/subscribe")
async def subscribe_newsletter(subscription: NewsletterSubscription, request: Request):
    """Subscribe to newsletter"""
    try:
        # Get user info
        user_ip = request.client.host
        user_agent = request.headers.get("user-agent", "")
        
        with engine.begin() as conn:
            # Try to insert new subscriber
            # Use appropriate timestamp format for database type
            if "postgres" in DATABASE_URL:
                timestamp = dt.datetime.now()  # PostgreSQL handles datetime objects
            else:
                timestamp = dt.datetime.now().isoformat()  # SQLite prefers ISO strings
                
            conn.execute(text("""
                INSERT INTO newsletter_subscribers (email, subscribed_at, ip_address, user_agent)
                VALUES (:email, :subscribed_at, :ip_address, :user_agent)
            """), {
                "email": subscription.email,
                "subscribed_at": timestamp,
                "ip_address": user_ip,
                "user_agent": user_agent
            })
            
        return {"ok": True, "message": "Successfully subscribed!"}
        
    except Exception as e:
        # Handle duplicate email (unique constraint)
        if "UNIQUE constraint failed" in str(e):
            return {"ok": True, "message": "Already subscribed!"}
        else:
            print(f"Newsletter subscription error: {e}")
            raise HTTPException(status_code=500, detail="Subscription failed")

@app.get("/api/newsletter/subscribers")
def get_newsletter_subscribers(request: Request):
    """Get newsletter subscribers for admin"""
    require_admin(request)
    
    with engine.begin() as conn:
        result = conn.execute(text("""
            SELECT email, subscribed_at, ip_address 
            FROM newsletter_subscribers 
            ORDER BY subscribed_at DESC
        """)).fetchall()
        
        subscribers = [
            {
                "email": row[0],
                "subscribed_at": row[1],
                "ip_address": row[2]
            }
            for row in result
        ]
        
    return {"subscribers": subscribers, "total": len(subscribers)}

@app.get("/api/product-comparisons")
def get_product_comparisons():
    """Get dynamic product comparisons from config.yaml"""
    try:
        import yaml
        
        # Load config.yaml
        with open('config.yaml', 'r') as f:
            config = yaml.safe_load(f)
        
        # Get routes from database for dynamic links
        with engine.begin() as conn:
            routes_result = conn.execute(text("SELECT slug, offer, dest_url FROM routes"))
            routes = {row.slug: {"offer": row.offer, "dest_url": row.dest_url} for row in routes_result}
        
        # Get product comparisons from config (nested under content)
        content_config = config.get('content', {})
        config_comparisons = content_config.get('product_comparisons', [])
        comparisons = []
        
        for comparison in config_comparisons:
            # Check if we have routes for this category
            category = comparison['category']
            category_keywords = [
                category,
                category.replace('-', ''),
                category.replace('-', ' '),
                *category.split('-')  # Split on dashes to get individual words
            ]
            
            category_routes = []
            for slug in routes.keys():
                if any(keyword in slug for keyword in category_keywords):
                    category_routes.append(slug)
            
            # Also check if any product has a specific route_slug that exists
            product_routes = []
            for product in comparison.get('products', []):
                route_slug = product.get('route_slug')
                if route_slug and route_slug in routes:
                    product_routes.append(route_slug)
            
            # Show comparison if we have category routes, product routes, or always_show is set
            if category_routes or product_routes or comparison.get('always_show', False):
                # Process products and add dynamic links
                processed_products = []
                for product in comparison.get('products', []):
                    processed_product = product.copy()
                    
                    # Use route_slug from config, or find matching route
                    route_slug = product.get('route_slug')
                    if route_slug and route_slug in routes:
                        processed_product['link'] = f"/r/{route_slug}"
                    elif product_routes:
                        # Use first product route
                        processed_product['link'] = f"/r/{product_routes[0]}"
                    elif category_routes:
                        # Use first matching category route
                        processed_product['link'] = f"/r/{category_routes[0]}"
                    else:
                        # Fallback link
                        processed_product['link'] = f"/r/{comparison['category']}"
                    
                    processed_products.append(processed_product)
                
                # Add processed comparison
                processed_comparison = comparison.copy()
                processed_comparison['products'] = processed_products
                comparisons.append(processed_comparison)
        
        return {"comparisons": comparisons}
        
    except FileNotFoundError:
        print("Config.yaml not found, using fallback comparisons")
        return {"comparisons": []}
    except Exception as e:
        print(f"Error fetching product comparisons: {e}")
        return {"comparisons": []}

@app.get("/api/stats/summary")
def get_stats_summary():
    """Get summary statistics for the footer"""
    with engine.begin() as conn:
        total_clicks = conn.execute(text("SELECT COUNT(*) FROM clicks")).scalar() or 0
        today_clicks = conn.execute(text("""
            SELECT COUNT(*) FROM clicks 
            WHERE date(created_at) = date('now')
        """)).scalar() or 0
        
    return {
        "total_clicks": total_clicks,
        "today_clicks": today_clicks,
        "active_routes": len(get_featured_routes())
    }

@app.post("/admin/route")
def create_route(r: Route, request: Request):
    require_admin(request)
    # Works on Postgres and modern SQLite
    upsert = text("""
        INSERT INTO routes(slug, offer, variant, dest_url)
        VALUES (:s, :o, :v, :d)
        ON CONFLICT (slug) DO UPDATE
        SET offer   = EXCLUDED.offer,
            variant = EXCLUDED.variant,
            dest_url= EXCLUDED.dest_url
    """)
    with engine.begin() as conn:
        conn.execute(upsert, {"s": r.slug, "o": r.offer, "v": r.variant, "d": r.dest_url})
    
    # Automatically generate product card image
    try:
        create_product_card_image(r.slug, r.offer)
    except Exception as e:
        print(f"Warning: Could not create product image for {r.slug}: {e}")
    
    return {"ok": True}

@app.get("/r/{slug}")
def redirect(slug: str, request: Request, v: str | None = None) -> RedirectResponse:
    """Redirect to the destination URL, logging click data.

    An optional query parameter `v` allows overriding the variant (e.g. v=B).
    """
    with engine.begin() as conn:
        row = conn.execute(
            text("SELECT offer,variant,dest_url FROM routes WHERE slug=:s"),
            {"s": slug},
        ).fetchone()
    if not row:
        raise HTTPException(404, "Unknown route")
    offer, variant, dest = row
    # allow explicit variant override via query parameter
    if v in ("A", "B"):
        variant = v
    # capture UTM params from the incoming request
    q = dict(parse_qsl(urlparse(str(request.url)).query))
    utm_source = q.get("utm_source")
    utm_medium = q.get("utm_medium")
    utm_campaign = q.get("utm_campaign")

    click_id = str(uuid.uuid4())
    with engine.begin() as conn:
        conn.execute(
            text(
                """
            INSERT INTO clicks(
                id,created_at,offer,variant,dest_url,ip,ua,referrer,utm_source,utm_medium,utm_campaign
            )
            VALUES(:id,:ts,:offer,:variant,:dest,:ip,:ua,:ref,:us,:um,:uc)
            """
            ),
            {
                "id": click_id,
                "ts": dt.datetime.utcnow().isoformat(),
                "offer": offer,
                "variant": variant,
                "dest": dest,
                "ip": request.client.host if request.client else None,
                "ua": request.headers.get("User-Agent"),
                "ref": request.headers.get("Referer"),
                "us": utm_source,
                "um": utm_medium,
                "uc": utm_campaign,
            },
        )
    return RedirectResponse(dest, status_code=302)

@app.get("/health")
def health() -> dict[str, object]:
    """Basic health check endpoint exposing the number of logged clicks."""
    with engine.begin() as conn:
        total = conn.execute(text("SELECT COUNT(*) FROM clicks")).scalar()
    return {"status": "ok", "clicks": total}

@app.get("/", response_class=HTMLResponse)
def root():
    """Serve the main website"""
    try:
        with open("site/index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="""<pre>Eco Pet Guide Affiliate System
See: /health  /docs  /admin
</pre>""")

@app.get("/admin", response_class=HTMLResponse)
def admin_page():
    """Main admin console with full UI"""
    try:
        with open("admin_template.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="""<h1>Admin Console</h1><p>Template file not found. <a href="/test-admin">Use test admin</a></p>""")

# List routes
@app.get("/admin/routes")
def list_routes(request: Request):
    require_admin(request)
    with engine.begin() as conn:
        rows = conn.execute(text("SELECT slug, offer, variant, dest_url FROM routes ORDER BY slug")).all()
    return JSONResponse([{"slug": s, "offer": o, "variant": v, "dest_url": d} for s, o, v, d in rows])

# Click aggregates
@app.get("/admin/clicks")
def clicks(request: Request, days: int = 7):
    require_admin(request)
    with engine.begin() as conn:
        rows = conn.execute(text("""
            SELECT offer, variant, COUNT(*) AS clicks
            FROM clicks
            WHERE created_at >= :since
            GROUP BY 1,2 ORDER BY clicks DESC
        """), {"since": (dt.datetime.utcnow() - dt.timedelta(days=days)).isoformat()}).all()
    return JSONResponse([{"offer": o, "variant": v, "clicks": c} for o, v, c in rows])

# Content generation endpoint
@app.post("/admin/generate")
async def admin_generate(request: Request):
    require_admin(request)
    try:
        body = await request.json()
        title = body.get("title", "")
        body_md = body.get("body_md", "Draft content")
        
        if not title:
            raise HTTPException(status_code=400, detail="Title is required")
            
        from content_pipeline import generate_post
        slug = generate_post(title=title, body_md=body_md)
        
        # Update the index.html file to include the new article
        try:
            import subprocess
            subprocess.run(["python3", "update_index.py"], check=True, capture_output=True)
        except Exception as e:
            print(f"Warning: Could not update index.html: {e}")
        
        return {"ok": True, "slug": slug}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Weekly report generation
@app.post("/admin/weekly")
def admin_weekly(request: Request):
    require_admin(request)
    try:
        import subprocess
        result = subprocess.run(["python3", "generate_report.py"], check=True, capture_output=True, text=True)
        return {"ok": True, "message": "Weekly report generated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Scheduler run
@app.post("/admin/scheduler")
def admin_scheduler(request: Request):
    require_admin(request)
    try:
        import subprocess
        # Run content generation
        subprocess.run(["python3", "content_pipeline.py"], check=True, capture_output=True)
        return {"ok": True, "message": "Content generation completed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Sitemap ping
@app.post("/admin/ping")
def admin_ping(request: Request):
    require_admin(request)
    try:
        # Simulate sitemap ping (in production, you'd ping actual search engines)
        return {"ok": True, "message": "Search engines notified of new content"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Update website index
@app.post("/admin/update-index")
def admin_update_index(request: Request):
    require_admin(request)
    try:
        import subprocess
        result = subprocess.run(["python3", "update_index.py"], check=True, capture_output=True, text=True)
        return {"ok": True, "message": "Website index updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# AI Article Generation with Google Gemini
@app.post("/admin/generate-ai-article")
async def admin_generate_ai_article(request: Request):
    require_admin(request)
    try:
        body = await request.json()
        product = body.get("product", "")
        article_type = body.get("articleType", "review")
        tone = body.get("tone", "professional")
        keywords = body.get("keywords", "")
        length = body.get("length", "medium")
        include_comparison = body.get("includeComparison", "no")
        target_audience = body.get("targetAudience", "pet-owners")
        seo_focus = body.get("seoFocus", "general")
        
        if not product:
            raise HTTPException(status_code=400, detail="Product is required")
        
        # Get product details from database
        with engine.begin() as conn:
            route = conn.execute(
                text("SELECT offer, dest_url FROM routes WHERE slug=:s"),
                {"s": product},
            ).fetchone()
        
        if not route:
            raise HTTPException(status_code=404, detail="Product not found")
        
        offer, dest_url = route
        
        # Prepare product info for Gemini
        product_info = {
            "offer": offer,
            "dest_url": dest_url,
            "slug": product
        }
        
        try:
            # Import and use Gemini generator
            from gemini_integration import GeminiArticleGenerator
            
            # Test Gemini connection first
            generator = GeminiArticleGenerator()
            if not generator.test_connection():
                raise Exception("Gemini API is not accessible. Please check your API key.")
            
            # Generate article using Gemini
            article_content = generator.generate_article(
                product_info=product_info,
                article_type=article_type,
                tone=tone,
                keywords=keywords,
                length=length,
                include_comparison=include_comparison,
                target_audience=target_audience,
                seo_focus=seo_focus
            )
            
            # Extract title from the generated content
            title_match = re.search(r'^# (.+)$', article_content, re.MULTILINE)
            if title_match:
                title = title_match.group(1)
            else:
                title = f"{offer} - {article_type.title()}"
            
        except ImportError:
            raise Exception("Gemini integration module not found")
        except Exception as e:
            raise Exception(f"Gemini API error: {str(e)}")
        
        # Generate the article using the existing pipeline
        from content_pipeline import generate_post
        slug = generate_post(title=title, body_md=article_content)
        
        # Update the website index
        try:
            import subprocess
            subprocess.run(["python3", "update_index.py"], check=True, capture_output=True)
        except Exception as e:
            print(f"Warning: Could not update index.html: {e}")
        
        return {"ok": True, "slug": slug, "message": "AI article generated successfully using Google Gemini!"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Test Gemini API connection
@app.post("/admin/test-gemini")
async def admin_test_gemini(request: Request):
    require_admin(request)
    try:
        from gemini_integration import GeminiArticleGenerator
        
        generator = GeminiArticleGenerator()
        if generator.test_connection():
            return {"ok": True, "message": "Gemini API is working and accessible"}
        else:
            raise Exception("Gemini API is not responding")
            
    except ImportError:
        raise HTTPException(status_code=500, detail="Gemini integration module not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini API connection failed: {str(e)}")

# Test Image Generator connection
@app.post("/admin/test-image-generator")
async def admin_test_image_generator(request: Request):
    require_admin(request)
    try:
        from image_generator import SlideshowImageGenerator
        
        generator = SlideshowImageGenerator()
        if generator.test_connection():
            return {"ok": True, "message": "Image generator is available"}
        else:
            raise Exception("Image generator not available")
            
    except ImportError:
        raise HTTPException(status_code=500, detail="Image generator module not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image generator test failed: {str(e)}")

# Generate Images with Progress
@app.post("/admin/generate-images")
async def admin_generate_images(request: Request):
    require_admin(request)
    try:
        body = await request.json()
        product = body.get("product", "")
        style = body.get("style", "simple")
        count = int(body.get("count", 3))
        
        if not product:
            raise HTTPException(status_code=400, detail="Product is required")
        
        # Get product details from database
        with engine.begin() as conn:
            route = conn.execute(
                text("SELECT offer, dest_url FROM routes WHERE slug=:s"),
                {"s": product},
            ).fetchone()
        
        if not route:
            raise HTTPException(status_code=404, detail="Product not found")
        
        offer, dest_url = route
        
        # Import image generator
        from image_generator import SlideshowImageGenerator
        generator = SlideshowImageGenerator()
        
        # Generate images
        images = generator.generate_product_slideshow_images(
            product_name=offer,
            article_title=f"Article about {offer}",
            style=style,
            count=count
        )
        
        return {"ok": True, "images": images, "message": f"Generated {len(images)} images successfully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Serve static content files
@app.get("/content/{filename}")
def serve_content(filename: str):
    """Serve content files from site/content/"""
    try:
        with open(f"site/content/{filename}", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Content not found")

@app.get("/disclosure.html")
def serve_disclosure():
    """Serve disclosure page"""
    try:
        with open("site/disclosure.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Disclosure not found")

@app.get("/privacy.html")
def serve_privacy():
    """Serve privacy page"""
    try:
        with open("site/privacy.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Privacy not found")

@app.get("/admin.js")
def serve_admin_js():
    """Serve admin JavaScript file"""
    try:
        with open("site/admin.js", "r", encoding="utf-8") as f:
            return Response(content=f.read(), media_type="application/javascript")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Admin JS not found")

@app.get("/js/home.js")
def serve_home_js():
    """Serve homepage JavaScript file"""
    try:
        with open("site/js/home.js", "r", encoding="utf-8") as f:
            return Response(content=f.read(), media_type="application/javascript")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Home JS not found")

@app.get("/css/custom.css")
def serve_custom_css():
    """Serve custom CSS file"""
    try:
        with open("site/css/custom.css", "r", encoding="utf-8") as f:
            return Response(content=f.read(), media_type="text/css")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Custom CSS not found")

@app.get("/images/slideshows/{filename}")
@app.head("/images/slideshows/{filename}")
def serve_slideshow_image(filename: str):
    """Serve generated slideshow images"""
    try:
        from fastapi.responses import FileResponse
        filepath = f"site/images/slideshows/{filename}"
        if os.path.exists(filepath):
            return FileResponse(filepath)
        else:
            raise HTTPException(status_code=404, detail="Image not found")
    except Exception as e:
        raise HTTPException(status_code=404, detail="Image not found")

@app.get("/images/library/{filename}")
@app.head("/images/library/{filename}")
def serve_library_image(filename: str):
    """Serve images from the library"""
    try:
        from fastapi.responses import FileResponse
        filepath = f"site/images/library/{filename}"
        if os.path.exists(filepath):
            return FileResponse(filepath)
        else:
            raise HTTPException(status_code=404, detail="Library image not found")
    except Exception as e:
        raise HTTPException(status_code=404, detail="Library image not found")


@app.get("/backgrounds/{filename}")
@app.head("/backgrounds/{filename}")
def serve_background(filename: str):
    """Serve background files for social media videos (hidden from website)"""
    try:
        from fastapi.responses import FileResponse
        filepath = f"site/backgrounds/{filename}"
        if os.path.exists(filepath):
            return FileResponse(filepath)
        else:
            raise HTTPException(status_code=404, detail="Background not found")
    except Exception as e:
        raise HTTPException(status_code=404, detail="Background not found")
@app.get("/admin/library")
def get_image_library(request: Request, query: str = "", product: str = "", style: str = "", limit: int = 50):
    """Get images from the library with optional filtering"""
    require_admin(request)
    try:
        results = image_library.search_images(query=query, product=product, style=style, limit=limit)
        return {"ok": True, "images": results}
    except Exception as e:
        return {"ok": False, "detail": str(e)}

@app.get("/admin/library/stats")
def get_library_stats(request: Request):
    """Get library statistics"""
    require_admin(request)
    try:
        stats = image_library.get_image_stats()
        return {"ok": True, "stats": stats}
    except Exception as e:
        return {"ok": False, "detail": str(e)}

@app.post("/admin/library/organize")
def organize_library(request: Request):
    """Organize existing images into the library"""
    require_admin(request)
    try:
        result = image_library.organize_existing_images()
        return {"ok": True, "result": result}
    except Exception as e:
        return {"ok": False, "detail": str(e)}

@app.delete("/admin/library/{generation_id}")
def delete_library_generation(request: Request, generation_id: str):
    """Delete a generation and its images from the library"""
    require_admin(request)
    try:
        success = image_library.delete_generation(generation_id)
        if success:
            return {"ok": True, "message": f"Deleted generation {generation_id}"}
        else:
            return {"ok": False, "detail": "Generation not found"}
    except Exception as e:
        return {"ok": False, "detail": str(e)}

# Article Management Endpoints
@app.get("/admin/articles")
def get_all_articles_admin(request: Request, limit: int = 50, offset: int = 0, sort: str = "newest"):
    """Get all articles for admin management"""
    require_admin(request)
    
    try:
        content_dir = "site/content"
        articles = []
        
        if os.path.exists(content_dir):
            # Get all markdown files
            for md_file in glob.glob(os.path.join(content_dir, "*.md")):
                article = parse_markdown_file(md_file)
                if article:
                    # Get file stats
                    file_path = Path(md_file)
                    stat = file_path.stat()
                    
                    # Check if HTML version exists
                    html_file = md_file.replace('.md', '.html')
                    has_html = os.path.exists(html_file)
                    
                    # Get file size
                    file_size = stat.st_size
                    
                    articles.append({
                        "slug": article.slug,
                        "title": article.title,
                        "excerpt": article.excerpt,
                        "tags": article.tags,
                        "publishedAt": article.publishedAt,
                        "estimatedReadMin": article.estimatedReadMin,
                        "file_size": file_size,
                        "has_html": has_html,
                        "created_at": dt.datetime.fromtimestamp(stat.st_ctime).isoformat(),
                        "modified_at": dt.datetime.fromtimestamp(stat.st_mtime).isoformat()
                    })
        
        # Sort articles
        if sort == "newest":
            articles.sort(key=lambda x: x["publishedAt"], reverse=True)
        elif sort == "oldest":
            articles.sort(key=lambda x: x["publishedAt"])
        elif sort == "title":
            articles.sort(key=lambda x: x["title"].lower())
        elif sort == "size":
            articles.sort(key=lambda x: x["file_size"], reverse=True)
        
        # Apply pagination
        total = len(articles)
        paginated_articles = articles[offset:offset + limit]
        
        return {
            "articles": paginated_articles,
            "total": total,
            "offset": offset,
            "limit": limit
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/admin/articles/{slug}")
def get_article_content(request: Request, slug: str):
    """Get full content of a specific article"""
    require_admin(request)
    
    try:
        md_file = f"site/content/{slug}.md"
        html_file = f"site/content/{slug}.html"
        
        result = {"slug": slug}
        
        # Read markdown content
        if os.path.exists(md_file):
            with open(md_file, 'r', encoding='utf-8') as f:
                result["markdown_content"] = f.read()
        
        # Read HTML content
        if os.path.exists(html_file):
            with open(html_file, 'r', encoding='utf-8') as f:
                result["html_content"] = f.read()
        
        if not result.get("markdown_content") and not result.get("html_content"):
            raise HTTPException(status_code=404, detail="Article not found")
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/admin/articles/{slug}")
def delete_article(request: Request, slug: str):
    """Delete an article (both .md and .html files)"""
    require_admin(request)
    
    try:
        deleted_files = []
        
        # Delete markdown file
        md_file = f"site/content/{slug}.md"
        if os.path.exists(md_file):
            os.remove(md_file)
            deleted_files.append(f"{slug}.md")
        
        # Delete HTML file
        html_file = f"site/content/{slug}.html"
        if os.path.exists(html_file):
            os.remove(html_file)
            deleted_files.append(f"{slug}.html")
        
        if not deleted_files:
            raise HTTPException(status_code=404, detail="Article not found")
        
        # Update the website index after deletion
        try:
            import subprocess
            subprocess.run(["python3", "update_index.py"], check=True, capture_output=True)
        except Exception as e:
            print(f"Warning: Could not update index.html after deletion: {e}")
        
        return {
            "ok": True, 
            "message": f"Article '{slug}' deleted successfully",
            "deleted_files": deleted_files
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

