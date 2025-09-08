"""
Content generation pipeline.

This script reads the site's configuration and uses Jinja2 templates to turn
briefs into Markdown and HTML posts. It automatically appends an FTC
disclosure and a call-to-action block linking to your chosen affiliate offer.

Usage:
    python content_pipeline.py

Set the environment variable `AFFILIATE_DISCLOSURE` to customise the
disclosure copy displayed at the top of each post.
"""

import os
import re
import pathlib
import yaml
import markdown
from dotenv import load_dotenv
from jinja2 import Template

load_dotenv()

# Use an environment variable for the FTC disclosure; fall back to a sensible default
DISCLOSURE = os.getenv(
    "AFFILIATE_DISCLOSURE",
    "We may earn a commission from links on this page.",
)

# Jinja2 template for generating Markdown content. It inserts the disclosure and
# a call-to-action block linking to the chosen offer with appended UTM params.
TEMPLATE = Template(
    """# {{ title }}

> {{ disclosure }}

{{ body_md }}

---

**Try this:** [{{ offer_name }}]({{ offer_url }})
*We might earn a commission at no cost to you.*
"""
)

# HTML page template
HTML_TEMPLATE = Template("""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{{ title }} - Eco Pet Guide</title>
    <meta name="description" content="{{ description }}">
    <link rel="stylesheet" href="../style.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
      body { font-family: 'Inter', system-ui, -apple-system, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 0 20px; }
      .header { background: linear-gradient(135deg, #2d5a27, #4a7c59); color: white; padding: 2rem 0; margin: -20px -20px 2rem -20px; }
      .container { max-width: 800px; margin: 0 auto; padding: 0 20px; }
      .tagline { margin: 0.5rem 0; opacity: 0.9; }
      .disclosure { margin: 0.5rem 0; font-size: 0.9rem; opacity: 0.8; }
      .article-content { margin: 2rem 0; }
      .cta-section { background: linear-gradient(135deg, #ff6b35, #f7931e); padding: 2rem; border-radius: 12px; margin: 2rem 0; text-align: center; box-shadow: 0 8px 25px rgba(255,107,53,0.3); border: 3px solid #ff6b35; }
      .cta-button { background: linear-gradient(135deg, #28a745, #20c997); color: white; padding: 1rem 2rem; text-decoration: none; border-radius: 50px; display: inline-block; margin-top: 1rem; font-weight: bold; font-size: 1.1rem; box-shadow: 0 4px 15px rgba(40,167,69,0.4); transition: all 0.3s ease; text-transform: uppercase; letter-spacing: 1px; }
      .cta-button:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(40,167,69,0.6); background: linear-gradient(135deg, #218838, #1ea080); }
      .cta-text { color: white; font-size: 1.2rem; font-weight: bold; margin-bottom: 0.5rem; }
      .cta-subtext { color: rgba(255,255,255,0.9); font-size: 0.95rem; margin-top: 0.5rem; }
      .footer { background: #f8f9fa; padding: 2rem 0; margin: 2rem -20px 0 -20px; text-align: center; font-size: 0.9rem; }
      table { width: 100%; border-collapse: collapse; margin: 1.5rem 0; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
      th, td { padding: 12px 15px; text-align: left; border-bottom: 1px solid #ddd; }
      th { background: #4a7c59; color: white; font-weight: 600; }
      tr:nth-child(even) { background: #f8f9fa; }
      tr:hover { background: #e8f4f8; }
    </style>
  </head>
  <body>
    <header class="header">
      <div class="container">
        <h1><a href="../" style="color: white; text-decoration: none;">🌱 Eco Pet Guide</a></h1>
        <p class="tagline">Sustainable Products for Conscious Pet Parents</p>
        <p class="disclosure">{{ disclosure }}</p>
      </div>
    </header>

    <main>
      <nav style="background: white; padding: 1rem 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        <div class="container">
          <a href="../" style="color: var(--secondary-color); text-decoration: none; font-weight: 500;">← Back to Home</a>
        </div>
      </nav>

      <article class="article-content">
        {% set enhanced_content = content %}
        
        {# Create inline CTA text based on product type #}
        {% if 'poop bag' in title.lower() or 'biodegradable' in title.lower() or 'poop' in title.lower() or 'compostable' in title.lower() %}
          {% set inline_cta = '<strong><a href="' + offer_url + '" style="color: #28a745; text-decoration: none; font-weight: bold; background: linear-gradient(135deg, #e8f5e9, #c8e6c9); padding: 3px 8px; border-radius: 4px; border-bottom: 2px solid #28a745;">🌱 these eco-friendly poop bags</a></strong>' %}
          {% set inline_cta_2 = '<strong><a href="' + offer_url + '" style="color: #ff6b35; text-decoration: none; font-weight: bold; background: linear-gradient(135deg, #fff3e0, #ffe0b2); padding: 3px 8px; border-radius: 4px; border-bottom: 2px solid #ff6b35;">🛒 grab the top-rated biodegradable bags here</a></strong>' %}
        {% elif 'treat' in title.lower() or 'organic' in title.lower() or 'banana' in title.lower() or 'coconut' in title.lower() or 'snack' in title.lower() %}
          {% set inline_cta = '<strong><a href="' + offer_url + '" style="color: #28a745; text-decoration: none; font-weight: bold; background: linear-gradient(135deg, #e8f5e9, #c8e6c9); padding: 3px 8px; border-radius: 4px; border-bottom: 2px solid #28a745;">🍌 these organic dog treats</a></strong>' %}
          {% set inline_cta_2 = '<strong><a href="' + offer_url + '" style="color: #ff6b35; text-decoration: none; font-weight: bold; background: linear-gradient(135deg, #fff3e0, #ffe0b2); padding: 3px 8px; border-radius: 4px; border-bottom: 2px solid #ff6b35;">🥥 grab these healthy treats now</a></strong>' %}
        {% elif 'leash' in title.lower() or 'hemp' in title.lower() or 'canvas' in title.lower() or 'collar' in title.lower() or 'harness' in title.lower() %}
          {% set inline_cta = '<strong><a href="' + offer_url + '" style="color: #28a745; text-decoration: none; font-weight: bold; background: linear-gradient(135deg, #e8f5e9, #c8e6c9); padding: 3px 8px; border-radius: 4px; border-bottom: 2px solid #28a745;">🦮 this premium hemp dog leash</a></strong>' %}
          {% set inline_cta_2 = '<strong><a href="' + offer_url + '" style="color: #ff6b35; text-decoration: none; font-weight: bold; background: linear-gradient(135deg, #fff3e0, #ffe0b2); padding: 3px 8px; border-radius: 4px; border-bottom: 2px solid #ff6b35;">🌿 get this eco-friendly leash now</a></strong>' %}
        {% elif 'dog toy' in title.lower() or 'toy' in title.lower() or 'bowl' in title.lower() or 'kit' in title.lower() or 'essential' in title.lower() %}
          {% set inline_cta = '<strong><a href="' + offer_url + '" style="color: #28a745; text-decoration: none; font-weight: bold; background: linear-gradient(135deg, #e8f5e9, #c8e6c9); padding: 3px 8px; border-radius: 4px; border-bottom: 2px solid #28a745;">🐕 these eco-friendly dog products</a></strong>' %}
          {% set inline_cta_2 = '<strong><a href="' + offer_url + '" style="color: #ff6b35; text-decoration: none; font-weight: bold; background: linear-gradient(135deg, #fff3e0, #ffe0b2); padding: 3px 8px; border-radius: 4px; border-bottom: 2px solid #ff6b35;">🛒 shop eco dog products now</a></strong>' %}
        {% elif 'dog bed' in title.lower() or 'bed' in title.lower() or 'sleep' in title.lower() %}
          {% set inline_cta = '<strong><a href="' + offer_url + '" style="color: #28a745; text-decoration: none; font-weight: bold; background: linear-gradient(135deg, #e8f5e9, #c8e6c9); padding: 3px 8px; border-radius: 4px; border-bottom: 2px solid #28a745;">🛏️ this premium orthopedic dog bed</a></strong>' %}
          {% set inline_cta_2 = '<strong><a href="' + offer_url + '" style="color: #ff6b35; text-decoration: none; font-weight: bold; background: linear-gradient(135deg, #fff3e0, #ffe0b2); padding: 3px 8px; border-radius: 4px; border-bottom: 2px solid #ff6b35;">🏆 get the ultimate comfort bed here</a></strong>' %}
        {% elif 'west paw' in title.lower() or 'kong' in title.lower() %}
          {% set inline_cta = '<strong><a href="' + offer_url + '" style="color: #28a745; text-decoration: none; font-weight: bold; background: linear-gradient(135deg, #e8f5e9, #c8e6c9); padding: 3px 8px; border-radius: 4px; border-bottom: 2px solid #28a745;">🏆 the winning eco toy</a></strong>' %}
          {% set inline_cta_2 = '<strong><a href="' + offer_url + '" style="color: #ff6b35; text-decoration: none; font-weight: bold; background: linear-gradient(135deg, #fff3e0, #ffe0b2); padding: 3px 8px; border-radius: 4px; border-bottom: 2px solid #ff6b35;">🥇 get the champion toy here</a></strong>' %}
        {% else %}
          {% set inline_cta = '<strong><a href="' + offer_url + '" style="color: #28a745; text-decoration: none; font-weight: bold; background: linear-gradient(135deg, #e8f5e9, #c8e6c9); padding: 3px 8px; border-radius: 4px; border-bottom: 2px solid #28a745;">🌱 these eco-friendly products</a></strong>' %}
          {% set inline_cta_2 = '<strong><a href="' + offer_url + '" style="color: #ff6b35; text-decoration: none; font-weight: bold; background: linear-gradient(135deg, #fff3e0, #ffe0b2); padding: 3px 8px; border-radius: 4px; border-bottom: 2px solid #ff6b35;">🛒 shop eco pet products here</a></strong>' %}
        {% endif %}
        
        {# Split content into paragraphs and strategically insert inline CTAs #}
        {% set content_parts = enhanced_content.split('</p>') %}
        {% if content_parts|length > 3 %}
          {# First paragraph - hook them #}
          {{ content_parts[0] }}</p>
          
          {# Second paragraph with first inline CTA #}
          {% set second_para = content_parts[1] %}
          {% if second_para and second_para|length > 100 %}
            {% set words = second_para.split(' ') %}
            {% if words|length > 15 %}
              {% set mid_point = (words|length * 0.7)|int %}
              {% set first_half = words[:mid_point]|join(' ') %}
              {% set second_half = words[mid_point:]|join(' ') %}
              {{ first_half }} {{ inline_cta }} {{ second_half }}</p>
            {% else %}
              {{ second_para }} Want to try {{ inline_cta }}?</p>
            {% endif %}
          {% else %}
            {{ second_para }}</p>
          {% endif %}
          
          {# Third paragraph - continue content #}
          {{ content_parts[2] }}</p>
          
          {# Fourth paragraph with second inline CTA #}
          {% if content_parts|length > 4 %}
            {% set fourth_para = content_parts[3] %}
            {% if fourth_para and fourth_para|length > 100 %}
              {% set words = fourth_para.split(' ') %}
              {% if words|length > 15 %}
                {% set mid_point = (words|length * 0.6)|int %}
                {% set first_half = words[:mid_point]|join(' ') %}
                {% set second_half = words[mid_point:]|join(' ') %}
                {{ first_half }} You can {{ inline_cta_2 }} {{ second_half }}</p>
              {% else %}
                {{ fourth_para }} Ready to {{ inline_cta_2 }}?</p>
              {% endif %}
            {% else %}
              {{ fourth_para }}</p>
            {% endif %}
          {% endif %}
          
          {# Rest of content #}
          {% for part in content_parts[4:] %}
            {{ part }}{% if not loop.last %}</p>{% endif %}
          {% endfor %}
        {% else %}
          {# Shorter content - just add one inline CTA #}
          {% set first_para = content_parts[0] if content_parts|length > 0 else '' %}
          {% if first_para and first_para|length > 50 %}
            {% set words = first_para.split(' ') %}
            {% if words|length > 10 %}
              {% set mid_point = (words|length * 0.7)|int %}
              {% set first_half = words[:mid_point]|join(' ') %}
              {% set second_half = words[mid_point:]|join(' ') %}
              {{ first_half }} {{ inline_cta }} {{ second_half }}</p>
            {% else %}
              {{ enhanced_content }}
            {% endif %}
          {% else %}
            {{ enhanced_content }}
          {% endif %}
          
          {# Add remaining parts #}
          {% for part in content_parts[1:] %}
            {{ part }}{% if not loop.last %}</p>{% endif %}
          {% endfor %}
        {% endif %}
        
        <div class="cta-section">
          <div class="cta-text">🎯 GET {{ product_cta_title }}!</div>
          <div style="color: white; font-size: 1rem; margin: 0.5rem 0;">{{ product_description }}</div>
          <a href="{{ offer_url }}" class="cta-button">🛒 {{ button_text }} →</a>
          <div class="cta-subtext">⚡ Prime shipping • ⭐ 4.5+ stars • 💚 Planet-friendly</div>
        </div>
      </article>

      <section class="cta-section" style="max-width: 800px; margin: 2rem auto;">
        <div class="container">
          <div class="cta-text">🌟 WANT MORE ECO PET PRODUCTS?</div>
          <div style="color: white; font-size: 1rem; margin: 0.5rem 0;">Discover the best sustainable pet gear & save money!</div>
          <a href="../" class="cta-button">🏠 SHOP MORE ECO PRODUCTS →</a>
          <div class="cta-subtext">📱 TikTok approved • 💰 Best prices • 🌱 Planet-friendly</div>
        </div>
      </section>
    </main>

    <footer class="footer">
      <div class="container">
        <p>
          © <span id="y"></span> Eco Pet Guide ·
          <a href="../disclosure.html">Disclosure</a> ·
          <a href="../privacy.html">Privacy</a>
        </p>
        <p style="margin-top: 1rem; opacity: 0.8;">
          🌱 Making pet parenthood more sustainable, one review at a time
        </p>
      </div>
    </footer>

    <script>document.getElementById('y').textContent=new Date().getFullYear()</script>
  </body>
</html>""")

def slugify(title: str) -> str:
    """Make safe, dash-only, ASCII slugs (no punctuation/special hyphens)."""
    s = title.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)      # keep letters/digits; replace others with -
    return re.sub(r"-+", "-", s).strip("-") # collapse repeats; trim ends

def build_affiliate_url(
    base_url: str,
    affiliate_param: str,
    affiliate_id: str,
    utm: dict,
) -> str:
    """Construct a full affiliate URL with tracking and UTM parameters."""
    from urllib.parse import urlparse, urlencode, urlunparse, parse_qsl

    u = urlparse(base_url)
    q = dict(parse_qsl(u.query))
    # Append the affiliate id using the specified parameter name
    q[affiliate_param] = affiliate_id
    # Merge in UTM params (utm_source, utm_campaign, etc.)
    q |= utm
    return urlunparse((u.scheme, u.netloc, u.path, u.params, urlencode(q), u.fragment))

def generate_post(
    config_path: str = "config.yaml",
    title: str = "Best Eco-Friendly Dog Toys (2025)",
    body_md: str = "... write your guide here ...",
) -> str:
    """
    Generate a Markdown and HTML post from the given title and body.

    The first offer defined in config.yaml is used for the CTA block.
    The generated files are saved into `site/content/` relative to the project root.

    Returns the slug for the generated post.
    """
    cfg = yaml.safe_load(open(config_path, "r", encoding="utf-8"))

    # Smart offer selection based on article title
    def select_best_offer(title, offers):
        """Select the most appropriate offer based on article title"""
        title_lower = title.lower()
        
        # Priority matching for specific products
        if any(keyword in title_lower for keyword in ['bed', 'sleep', 'comfort', 'orthopedic']):
            # Look for dog bed offer
            for offer in offers:
                if 'bed' in offer.get('name', '').lower() or 'B00TQ47CPW' in offer.get('base_url', ''):
                    return offer
        
        elif any(keyword in title_lower for keyword in ['poop bag', 'biodegradable', 'waste', 'poop', 'compostable']):
            # Look for poop bags offer
            for offer in offers:
                if 'poop' in offer.get('name', '').lower() or 'bag' in offer.get('name', '').lower():
                    return offer
        
        elif any(keyword in title_lower for keyword in ['treat', 'organic', 'banana', 'coconut', 'snack']):
            # Look for dog treats offer
            for offer in offers:
                if 'treat' in offer.get('name', '').lower() or 'B093CLBJDW' in offer.get('base_url', ''):
                    return offer
        
        elif any(keyword in title_lower for keyword in ['leash', 'hemp', 'canvas', 'collar', 'harness']):
            # Look for dog leash offer
            for offer in offers:
                if 'leash' in offer.get('name', '').lower() or 'B00C9L67XW' in offer.get('base_url', ''):
                    return offer
        
        elif any(keyword in title_lower for keyword in ['toy', 'play', 'kong', 'west paw', 'bowl', 'kit', 'essential']):
            # Look for dog toys offer (default for accessories)
            for offer in offers:
                if 'toy' in offer.get('name', '').lower() or 'B004A7X27M' in offer.get('base_url', ''):
                    return offer
        
        # Default to first offer if no specific match
        return offers[0]
    
    # Select the best offer for this article
    offer = select_best_offer(title, cfg["offers"])
    url = build_affiliate_url(
        offer["base_url"],
        offer["affiliate_param"],
        offer["affiliate_id"],
        {"utm_source": "site", "utm_campaign": "content"},
    )

    md = TEMPLATE.render(
        title=title,
        body_md=body_md,
        disclosure=DISCLOSURE,
        offer_name=offer["name"],
        offer_url=url,
    )

    # Ensure output directory exists
    out_dir = pathlib.Path("site/content")
    out_dir.mkdir(parents=True, exist_ok=True)

    # Create a safe slug
    slug = slugify(title)

    # Write Markdown
    (out_dir / f"{slug}.md").write_text(md, encoding="utf-8")
    
    # Generate HTML content from markdown with table support
    # Include the title as an H1 in the content
    full_content_md = f"# {title}\n\n{body_md}"
    content_html = markdown.markdown(full_content_md, extensions=['tables'])
    
    # Create description from first 150 chars of content
    description = body_md[:150].replace('\n', ' ') + "..." if len(body_md) > 150 else body_md
    
    # Create smart product-specific CTA text based on article title
    def get_product_cta_info(article_title):
        title_lower = article_title.lower()
        
        if any(keyword in title_lower for keyword in ['poop bag', 'biodegradable', 'poop', 'compostable', 'waste']):
            return {
                'cta_title': 'THE BEST ECO POOP BAGS',
                'description': 'Top-rated biodegradable bags that actually work!',
                'button_text': 'BUY ECO POOP BAGS NOW'
            }
        elif any(keyword in title_lower for keyword in ['treat', 'organic', 'banana', 'coconut', 'snack']):
            return {
                'cta_title': 'THESE ORGANIC DOG TREATS',
                'description': 'Healthy, natural treats your dog will absolutely love!',
                'button_text': 'BUY ORGANIC TREATS NOW'
            }
        elif any(keyword in title_lower for keyword in ['leash', 'hemp', 'canvas', 'collar', 'harness']):
            return {
                'cta_title': 'THIS PREMIUM HEMP DOG LEASH',
                'description': 'Durable, eco-friendly leash made from sustainable hemp!',
                'button_text': 'GET THE HEMP LEASH NOW'
            }
        elif any(keyword in title_lower for keyword in ['dog toy', 'toy', 'bowl', 'kit', 'essential']):
            return {
                'cta_title': 'THESE ECO DOG PRODUCTS',
                'description': 'Safe, durable & planet-friendly products your dog will love!',
                'button_text': 'SHOP ECO DOG PRODUCTS NOW'
            }
        elif 'west paw' in title_lower or 'kong' in title_lower:
            return {
                'cta_title': 'THE WINNING DOG TOY',
                'description': 'Get the eco-friendly toy that beats the competition!',
                'button_text': 'BUY THE BEST TOY NOW'
            }
        elif 'bed' in title_lower or 'sleep' in title_lower or 'comfort' in title_lower:
            return {
                'cta_title': 'THE ULTIMATE DOG BED',
                'description': 'Premium orthopedic memory foam for maximum comfort!',
                'button_text': 'BUY THE BEST BED NOW'
            }
        elif 'starter kit' in title_lower or 'essentials' in title_lower:
            return {
                'cta_title': 'THE COMPLETE ECO KIT',
                'description': 'Everything you need for sustainable pet parenting!',
                'button_text': 'GET THE STARTER KIT'
            }
        else:
            return {
                'cta_title': 'THESE ECO PET PRODUCTS',
                'description': 'Top-rated sustainable products for conscious pet parents!',
                'button_text': 'SHOP ECO PRODUCTS NOW'
            }
    
    cta_info = get_product_cta_info(title)
    
    # Generate complete HTML page
    full_html = HTML_TEMPLATE.render(
        title=title,
        description=description,
        disclosure=DISCLOSURE,
        content=content_html,
        offer_name=offer["name"],
        offer_url=url,
        product_cta_title=cta_info['cta_title'],
        product_description=cta_info['description'],
        button_text=cta_info['button_text']
    )
    
    (out_dir / f"{slug}.html").write_text(full_html, encoding="utf-8")

    return slug

if __name__ == "__main__":
    # Example usage for quick debugging. Replace body_md with actual content.
    example_body = (
        "Practical tips for choosing eco-friendly pet products, pros/cons of different materials, "
        "and how to evaluate products based on sustainability certifications."
    )
    print("Generated:", generate_post(body_md=example_body))
