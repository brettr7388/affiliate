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

    # Pick the first offer for the CTA
    offer = cfg["offers"][0]
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

    # Write Markdown and HTML
    (out_dir / f"{slug}.md").write_text(md, encoding="utf-8")
    html = markdown.markdown(md)
    (out_dir / f"{slug}.html").write_text(html, encoding="utf-8")

    return slug


if __name__ == "__main__":
    # Example usage for quick debugging. Replace body_md with actual content.
    example_body = (
        "Practical tips for choosing eco-friendly pet products, pros/cons of different materials, "
        "and how to evaluate products based on sustainability certifications."
    )
    print("Generated:", generate_post(body_md=example_body))
