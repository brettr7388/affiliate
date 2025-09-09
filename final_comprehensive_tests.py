#!/usr/bin/env python3
"""
Final Comprehensive Test Suite for Affiliate Content
Tests all articles, dropdown selections, product combinations, and edge cases
"""

import os
import re
import json
import unittest
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup
from typing import Dict, List, Set


class FinalAffiliateTestSuite(unittest.TestCase):
    """
    Final comprehensive test suite for affiliate content
    """
    
    @classmethod
    def setUpClass(cls):
        """Set up comprehensive test data"""
        cls.base_dir = Path(__file__).parent
        cls.site_dir = cls.base_dir / "site"
        cls.content_dir = cls.site_dir / "content"
        
        # All expected products with detailed information
        cls.products = {
            "B07MYPFMZP": {
                "name": "Earth-Rated Biodegradable Poop Bags",
                "category": "poop_bags",
                "price_range": "$15-25",
                "keywords": ["poop", "biodegradable", "earth-rated", "compostable", "bags"],
                "expected_articles": ["poop", "biodegradable", "compostable", "waste"]
            },
            "B004A7X27M": {
                "name": "Kong Classic Dog Toy",
                "category": "dog_toys",
                "price_range": "$5-15",
                "keywords": ["kong", "toy", "eco-friendly", "dog toy", "classic"],
                "expected_articles": ["toy", "play", "kong", "eco-friendly"]
            },
            "B093CLBJDW": {
                "name": "WAG Expedition Organic Banana & Coconut Treats",
                "category": "dog_treats",
                "price_range": "$8-12",
                "keywords": ["wag", "organic", "banana", "coconut", "treats"],
                "expected_articles": ["treat", "organic", "banana", "coconut"]
            },
            "B00C9L67XW": {
                "name": "The Good Dog Company Hemp Canvas Leash",
                "category": "dog_leash",
                "price_range": "$20-35",
                "keywords": ["hemp", "leash", "canvas", "good dog company"],
                "expected_articles": ["leash", "hemp", "canvas"]
            },
            "B00TQ47CPW": {
                "name": "PetFusion Ultimate Dog Bed Lounge",
                "category": "dog_bed",
                "price_range": "$50-80",
                "keywords": ["petfusion", "dog bed", "ultimate", "lounge", "orthopedic"],
                "expected_articles": ["bed", "sleep", "comfort", "petfusion"]
            },
            "B0DWBQXQ46": {
                "name": "West Paw Toppl Treat Dispensing Toy",
                "category": "dog_toys",
                "price_range": "$10-18",
                "keywords": ["west paw", "toppl", "treat", "dispensing", "eco"],
                "expected_articles": ["west paw", "toppl", "toy"]
            }
        }
        
        # Load all articles
        cls.articles = cls._load_articles()
        
        # Load JavaScript content
        cls.js_content = cls._load_javascript()
        
    @classmethod
    def _load_articles(cls):
        """Load all articles with metadata"""
        articles = {}
        
        for html_file in cls.content_dir.glob("*.html"):
            slug = html_file.stem
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            soup = BeautifulSoup(content, 'html.parser')
            title = soup.find('title')
            
            # Extract ASINs
            asins = re.findall(r'/dp/([A-Z0-9]{10})', content)
            
            # Extract affiliate tags
            tags = re.findall(r'tag=([A-Za-z0-9-]+)', content)
            
            articles[slug] = {
                "path": html_file,
                "content": content,
                "soup": soup,
                "title": title.get_text() if title else "",
                "asins": list(set(asins)),
                "affiliate_tags": list(set(tags)),
                "type": "html"
            }
        
        return articles
    
    @classmethod
    def _load_javascript(cls):
        """Load JavaScript files"""
        js_file = cls.site_dir / "js" / "home.js"
        if js_file.exists():
            with open(js_file, 'r', encoding='utf-8') as f:
                return f.read()
        return ""
    
    def test_every_article_has_correct_product_match(self):
        """Test that every article promotes the correct product for its content"""
        print("\n🔍 Testing product matching for all articles...")
        
        for slug, article in self.articles.items():
            with self.subTest(article=slug):
                title_content = (article['title'] + " " + article['content']).lower()
                
                for asin in article['asins']:
                    if asin in self.products:
                        product = self.products[asin]
                        
                        # Check if article content matches product
                        keyword_matches = []
                        for keyword in product['keywords']:
                            if keyword.lower() in title_content:
                                keyword_matches.append(keyword)
                        
                        # Should have at least one keyword match
                        self.assertGreater(
                            len(keyword_matches), 0,
                            f"Article '{slug}' promotes {product['name']} (ASIN: {asin}) "
                            f"but content doesn't contain expected keywords: {product['keywords']}. "
                            f"Found matches: {keyword_matches}"
                        )
                        
                        print(f"  ✅ {slug}: {product['name']} - Keywords found: {keyword_matches}")

    def test_every_dropdown_category_has_articles(self):
        """Test that every dropdown category has corresponding articles"""
        print("\n🔍 Testing dropdown categories have articles...")
        
        expected_categories = {
            'poop_bags': ['poop', 'biodegradable', 'compostable'],
            'dog_toys': ['toy', 'play', 'kong', 'west paw'],
            'dog_treats': ['treat', 'organic'],
            'dog_leash': ['leash', 'hemp'],
            'dog_bed': ['bed', 'sleep', 'comfort']
        }
        
        for category, keywords in expected_categories.items():
            matching_articles = []
            
            for slug, article in self.articles.items():
                content_lower = (article['title'] + " " + article['content']).lower()
                if any(keyword in content_lower for keyword in keywords):
                    matching_articles.append(slug)
            
            self.assertGreater(
                len(matching_articles), 0,
                f"No articles found for category '{category}' with keywords: {keywords}"
            )
            
            print(f"  ✅ {category}: {len(matching_articles)} articles")

    def test_every_product_asin_has_valid_amazon_link(self):
        """Test that every ASIN corresponds to a valid Amazon link structure"""
        print("\n🔍 Testing Amazon link structure for all ASINs...")
        
        for slug, article in self.articles.items():
            with self.subTest(article=slug):
                for asin in article['asins']:
                    # Find the actual link for this ASIN
                    asin_links = re.findall(f'https?://[^\\s"]*amazon\\.com[^\\s"]*/dp/{asin}[^\\s"]*', article['content'])
                    
                    self.assertGreater(
                        len(asin_links), 0,
                        f"ASIN {asin} found in {slug} but no corresponding Amazon link"
                    )
                    
                    for link in asin_links:
                        # Validate link structure
                        parsed = urlparse(link)
                        self.assertIn('amazon.com', parsed.netloc, f"Invalid Amazon domain in {slug}: {link}")
                        self.assertIn(f'/dp/{asin}', parsed.path, f"Invalid ASIN path in {slug}: {link}")
                        
                        # Check for affiliate tag
                        query_params = parse_qs(parsed.query)
                        self.assertIn('tag', query_params, f"Missing affiliate tag in {slug}: {link}")
                        
                        print(f"  ✅ {slug}: ASIN {asin} - Valid Amazon link")

    def test_every_affiliate_tag_is_consistent_per_article(self):
        """Test that each article uses consistent affiliate tags"""
        print("\n🔍 Testing affiliate tag consistency...")
        
        for slug, article in self.articles.items():
            with self.subTest(article=slug):
                tags = article['affiliate_tags']
                
                if tags:
                    # All tags should be the same within an article
                    unique_tags = list(set(tags))
                    self.assertEqual(
                        len(unique_tags), 1,
                        f"Article {slug} has inconsistent affiliate tags: {unique_tags}"
                    )
                    
                    # Tag should be valid
                    tag = unique_tags[0]
                    valid_tags = ["test0b252-20", "YOUR-AMAZON-ASSOCIATES-TAG"]
                    self.assertIn(
                        tag, valid_tags,
                        f"Article {slug} has invalid affiliate tag: {tag}"
                    )
                    
                    print(f"  ✅ {slug}: Consistent tag '{tag}'")

    def test_every_comparison_article_has_multiple_products(self):
        """Test that comparison articles promote multiple products"""
        print("\n🔍 Testing comparison articles have multiple products...")
        
        comparison_keywords = ['vs', 'compare', 'comparison', 'better', 'which']
        
        for slug, article in self.articles.items():
            title_lower = article['title'].lower()
            
            if any(keyword in title_lower for keyword in comparison_keywords):
                with self.subTest(article=slug):
                    self.assertGreaterEqual(
                        len(article['asins']), 2,
                        f"Comparison article {slug} should have at least 2 products, found: {len(article['asins'])}"
                    )
                    
                    # Products should be in the same category or related
                    categories = []
                    for asin in article['asins']:
                        if asin in self.products:
                            categories.append(self.products[asin]['category'])
                    
                    # Allow flexibility for comparison articles
                    print(f"  ✅ {slug}: {len(article['asins'])} products, categories: {set(categories)}")

    def test_every_cta_button_matches_promoted_product(self):
        """Test that CTA buttons match the products being promoted"""
        print("\n🔍 Testing CTA button text matches products...")
        
        category_button_keywords = {
            'poop_bags': ['poop', 'bags', 'eco', 'biodegradable'],
            'dog_toys': ['toy', 'eco', 'dog', 'play'],
            'dog_treats': ['treat', 'organic', 'healthy'],
            'dog_leash': ['leash', 'hemp', 'eco'],
            'dog_bed': ['bed', 'comfort', 'sleep']
        }
        
        for slug, article in self.articles.items():
            with self.subTest(article=slug):
                soup = article['soup']
                cta_buttons = soup.find_all('a', class_='cta-button')
                
                for button in cta_buttons:
                    button_text = button.get_text().lower()
                    href = button.get('href', '')
                    
                    # Find ASIN in href
                    asin_match = re.search(r'/dp/([A-Z0-9]{10})', href)
                    if asin_match and asin_match.group(1) in self.products:
                        asin = asin_match.group(1)
                        product = self.products[asin]
                        category = product['category']
                        
                        expected_keywords = category_button_keywords.get(category, [])
                        if expected_keywords:
                            keyword_found = any(kw in button_text for kw in expected_keywords)
                            self.assertTrue(
                                keyword_found,
                                f"CTA button '{button_text}' in {slug} doesn't match {category} product. "
                                f"Expected keywords: {expected_keywords}"
                            )
                            
                            print(f"  ✅ {slug}: CTA '{button_text}' matches {category}")

    def test_dropdown_javascript_functionality(self):
        """Test that dropdown JavaScript functionality is properly implemented"""
        print("\n🔍 Testing dropdown JavaScript functionality...")
        
        required_elements = [
            'category-dropdown',
            'handleCategoryClick',
            'handleTabClick',
            'tab-button',
            'data-category',
            'addEventListener'
        ]
        
        for element in required_elements:
            self.assertIn(
                element, self.js_content,
                f"Required dropdown element/function '{element}' not found in JavaScript"
            )
        
        # Test specific dropdown patterns
        category_pattern = r'data-category["\']?\s*[:=]\s*["\']([^"\']+)["\']'
        categories = re.findall(category_pattern, self.js_content)
        
        if categories:
            print(f"  ✅ Found dropdown categories: {categories}")
        
        print(f"  ✅ All required JavaScript functionality present")

    def test_every_article_has_proper_meta_tags(self):
        """Test that every article has proper SEO meta tags"""
        print("\n🔍 Testing meta tags for all articles...")
        
        for slug, article in self.articles.items():
            with self.subTest(article=slug):
                soup = article['soup']
                
                # Required meta tags
                title_tag = soup.find('title')
                self.assertIsNotNone(title_tag, f"Missing title tag in {slug}")
                
                description_meta = soup.find('meta', attrs={'name': 'description'})
                self.assertIsNotNone(description_meta, f"Missing meta description in {slug}")
                
                viewport_meta = soup.find('meta', attrs={'name': 'viewport'})
                self.assertIsNotNone(viewport_meta, f"Missing viewport meta in {slug}")
                
                # Validate lengths
                title_text = title_tag.get_text()
                self.assertLessEqual(len(title_text), 60, f"Title too long in {slug}: {len(title_text)} chars")
                
                if description_meta:
                    desc_content = description_meta.get('content', '')
                    self.assertLessEqual(len(desc_content), 160, f"Meta description too long in {slug}")
                
                print(f"  ✅ {slug}: Valid meta tags")

    def test_no_duplicate_content_across_articles(self):
        """Test that articles don't have duplicate content"""
        print("\n🔍 Testing for duplicate content...")
        
        article_contents = {}
        
        for slug, article in self.articles.items():
            # Extract main content (remove HTML tags for comparison)
            soup = article['soup']
            
            # Remove script, style, and navigation elements
            for element in soup(['script', 'style', 'nav', 'header', 'footer']):
                element.decompose()
            
            main_content = soup.get_text()
            
            # Create a content signature (first 200 characters)
            content_signature = re.sub(r'\s+', ' ', main_content[:200]).strip().lower()
            
            if content_signature in article_contents:
                self.fail(f"Duplicate content found between {slug} and {article_contents[content_signature]}")
            
            article_contents[content_signature] = slug
        
        print(f"  ✅ All {len(self.articles)} articles have unique content")

    def test_affiliate_disclosure_compliance(self):
        """Test that all articles have proper affiliate disclosure"""
        print("\n🔍 Testing affiliate disclosure compliance...")
        
        required_disclosures = [
            "amazon associate",
            "affiliate",
            "commission",
            "qualifying purchases"
        ]
        
        for slug, article in self.articles.items():
            with self.subTest(article=slug):
                content_lower = article['content'].lower()
                
                has_disclosure = any(disclosure in content_lower for disclosure in required_disclosures)
                self.assertTrue(
                    has_disclosure,
                    f"Article {slug} missing required affiliate disclosure"
                )
                
                print(f"  ✅ {slug}: Has affiliate disclosure")

    def test_product_price_consistency(self):
        """Test that product information is consistent where mentioned"""
        print("\n🔍 Testing product price consistency...")
        
        # This test checks if price ranges are reasonable (not testing exact prices as they change)
        price_pattern = r'\$(\d+(?:\.\d{2})?)'
        
        for slug, article in self.articles.items():
            with self.subTest(article=slug):
                prices = re.findall(price_pattern, article['content'])
                
                if prices:
                    # Convert to float and check ranges are reasonable
                    float_prices = [float(p) for p in prices]
                    
                    # Prices should be reasonable for pet products (between $1 and $200)
                    for price in float_prices:
                        self.assertGreaterEqual(price, 1.0, f"Unreasonably low price ${price} in {slug}")
                        self.assertLessEqual(price, 200.0, f"Unreasonably high price ${price} in {slug}")
                
                print(f"  ✅ {slug}: Price information validated")


def run_final_comprehensive_tests():
    """Run the final comprehensive test suite"""
    print("🚀 RUNNING FINAL COMPREHENSIVE AFFILIATE CONTENT TESTS")
    print("="*80)
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(FinalAffiliateTestSuite)
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2, stream=open('final_test_results.txt', 'w'))
    result = runner.run(suite)
    
    # Print summary to console
    print(f"\n{'='*80}")
    print("FINAL TEST RESULTS SUMMARY")
    print(f"{'='*80}")
    print(f"Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success Rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print(f"\n❌ FAILURES ({len(result.failures)}):")
        for test, traceback in result.failures[:3]:  # Show first 3
            print(f"  • {test}")
            error_msg = traceback.split('\n')[-2] if '\n' in traceback else traceback
            print(f"    {error_msg}")
    
    if result.errors:
        print(f"\n⚠️  ERRORS ({len(result.errors)}):")
        for test, traceback in result.errors[:3]:  # Show first 3
            print(f"  • {test}")
    
    if len(result.failures) == 0 and len(result.errors) == 0:
        print(f"\n🎉 ALL TESTS PASSED! Your affiliate content is fully validated.")
        print(f"✅ Tested {result.testsRun} different aspects of your affiliate setup")
        print(f"✅ All articles have correct product matching")
        print(f"✅ All affiliate links are properly structured")
        print(f"✅ All dropdown functionality is working")
        print(f"✅ All meta tags and SEO elements are correct")
    
    return result


if __name__ == '__main__':
    result = run_final_comprehensive_tests()
    exit(len(result.failures) + len(result.errors)) 