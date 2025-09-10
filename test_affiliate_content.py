#!/usr/bin/env python3
"""
Comprehensive Test Suite for Affiliate Content
Tests all articles, dropdowns, and Amazon affiliate links for correctness
"""

import os
import re
import json
import glob
import unittest
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup
import markdown
from typing import Dict, List, Tuple, Set


class AffiliateContentTestSuite(unittest.TestCase):
    """
    Test suite for validating affiliate content integrity
    """
    
    @classmethod
    def setUpClass(cls):
        """Set up test data and configurations"""
        cls.base_dir = Path(__file__).parent
        cls.site_dir = cls.base_dir / "site"
        cls.content_dir = cls.site_dir / "content"
        
        # Expected product mappings (ASIN -> Product Info)
        cls.expected_products = {
            "B07MYPFMZP": {
                "name": "Earth-Rated Biodegradable Poop Bags",
                "category": "poop_bags",
                "keywords": ["poop", "biodegradable", "earth-rated", "compostable"]
            },
            "B004A7X27M": {
                "name": "Kong Classic Dog Toy",
                "category": "dog_toys", 
                "keywords": ["kong", "toy", "eco-friendly", "dog toy"]
            },
            "B093CLBJDW": {
                "name": "WAG Expedition Organic Banana & Coconut Treats",
                "category": "dog_treats",
                "keywords": ["wag", "organic", "banana", "coconut", "treats"]
            },
            "B00C9L67XW": {
                "name": "The Good Dog Company Hemp Canvas Leash",
                "category": "dog_leash",
                "keywords": ["hemp", "leash", "canvas", "good dog company"]
            },
            "B00TQ47CPW": {
                "name": "PetFusion Ultimate Dog Bed Lounge",
                "category": "dog_bed",
                "keywords": ["petfusion", "dog bed", "ultimate", "lounge", "orthopedic"]
            },
            "B0DWBQXQ46": {
                "name": "West Paw Toppl Treat Dispensing Toy",
                "category": "dog_toys",
                "keywords": ["west paw", "toppl", "treat", "dispensing", "eco"]
            }
        }
        
        # Expected affiliate tags
        cls.valid_affiliate_tags = ["test0b252-20", "YOUR-AMAZON-ASSOCIATES-TAG"]
        
        # Article categories based on content analysis
        cls.article_categories = {
            "poop_bags": ["poop", "biodegradable", "compostable", "waste"],
            "dog_toys": ["toy", "play", "kong", "west paw", "toppl"],
            "dog_treats": ["treat", "organic", "banana", "coconut", "wag"],
            "dog_leash": ["leash", "hemp", "canvas", "collar"],
            "dog_bed": ["bed", "sleep", "comfort", "petfusion"],
            "comparison": ["vs", "compare", "better", "which"]
        }
        
        # Load all articles
        cls.articles = cls._load_all_articles()
        
    @classmethod
    def _load_all_articles(cls) -> Dict[str, Dict]:
        """Load all HTML and MD articles"""
        articles = {}
        
        # Load HTML articles
        for html_file in cls.content_dir.glob("*.html"):
            slug = html_file.stem
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            soup = BeautifulSoup(content, 'html.parser')
            title = soup.find('title')
            title_text = title.get_text() if title else ""
            
            articles[slug] = {
                "type": "html",
                "path": html_file,
                "content": content,
                "soup": soup,
                "title": title_text
            }
        
        # Load Markdown articles
        for md_file in cls.content_dir.glob("*.md"):
            slug = md_file.stem
            if slug + ".html" in [a.split('.')[0] for a in articles.keys()]:
                # Skip if HTML version exists
                continue
                
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract title from markdown
            title_match = re.search(r'^# (.+)', content, re.MULTILINE)
            title = title_match.group(1) if title_match else slug
            
            articles[slug] = {
                "type": "markdown",
                "path": md_file,
                "content": content,
                "title": title
            }
        
        return articles

    def test_all_articles_have_valid_structure(self):
        """Test that all articles have valid HTML/MD structure"""
        for slug, article in self.articles.items():
            with self.subTest(article=slug):
                self.assertIsNotNone(article['content'], f"Article {slug} has no content")
                self.assertGreater(len(article['content']), 100, f"Article {slug} content too short")
                self.assertIsNotNone(article['title'], f"Article {slug} has no title")
                self.assertGreater(len(article['title']), 5, f"Article {slug} title too short")

    def test_all_articles_have_affiliate_disclosure(self):
        """Test that all articles have proper affiliate disclosure"""
        for slug, article in self.articles.items():
            with self.subTest(article=slug):
                content = article['content'].lower()
                
                # Check for affiliate disclosure
                disclosure_patterns = [
                    "amazon associate",
                    "affiliate",
                    "commission",
                    "qualifying purchases"
                ]
                
                has_disclosure = any(pattern in content for pattern in disclosure_patterns)
                self.assertTrue(has_disclosure, f"Article {slug} missing affiliate disclosure")

    def test_amazon_affiliate_links_structure(self):
        """Test that all Amazon affiliate links have correct structure"""
        for slug, article in self.articles.items():
            with self.subTest(article=slug):
                # Find all Amazon links
                amazon_links = re.findall(r'https?://(?:www\.)?amazon\.com/[^\s"\'<>]+', article['content'])
                
                for link in amazon_links:
                    # Parse URL
                    parsed = urlparse(link)
                    query_params = parse_qs(parsed.query)
                    
                    # Check for ASIN in path
                    asin_match = re.search(r'/dp/([A-Z0-9]{10})', parsed.path)
                    self.assertIsNotNone(asin_match, f"Invalid Amazon link structure in {slug}: {link}")
                    
                    asin = asin_match.group(1)
                    
                    # Check for affiliate tag
                    self.assertIn('tag', query_params, f"Missing affiliate tag in {slug}: {link}")
                    tag = query_params['tag'][0]
                    self.assertIn(tag, self.valid_affiliate_tags, f"Invalid affiliate tag in {slug}: {tag}")

    def test_product_title_matching(self):
        """Test that product links match article titles and content"""
        for slug, article in self.articles.items():
            with self.subTest(article=slug):
                title_lower = article['title'].lower()
                content_lower = article['content'].lower()
                
                # Find ASINs in the article
                asins = re.findall(r'/dp/([A-Z0-9]{10})', article['content'])
                
                for asin in asins:
                    if asin in self.expected_products:
                        product_info = self.expected_products[asin]
                        
                        # Check if article content matches product
                        keywords_found = []
                        for keyword in product_info['keywords']:
                            if keyword.lower() in title_lower or keyword.lower() in content_lower:
                                keywords_found.append(keyword)
                        
                        self.assertGreater(
                            len(keywords_found), 0,
                            f"Article {slug} uses ASIN {asin} ({product_info['name']}) but content doesn't match. "
                            f"Expected keywords: {product_info['keywords']}, Found: {keywords_found}"
                        )

    def test_article_category_consistency(self):
        """Test that articles are consistently categorized"""
        for slug, article in self.articles.items():
            with self.subTest(article=slug):
                title_lower = article['title'].lower()
                content_lower = article['content'].lower()
                
                # Determine article category based on content
                detected_categories = []
                for category, keywords in self.article_categories.items():
                    if any(keyword in title_lower or keyword in content_lower for keyword in keywords):
                        detected_categories.append(category)
                
                # Should have at least one category
                self.assertGreater(len(detected_categories), 0, 
                                 f"Article {slug} doesn't fit any category")
                
                # Check ASINs match detected categories
                asins = re.findall(r'/dp/([A-Z0-9]{10})', article['content'])
                for asin in asins:
                    if asin in self.expected_products:
                        product_category = self.expected_products[asin]['category']
                        # Allow some flexibility for comparison articles
                        if 'comparison' not in detected_categories:
                            self.assertIn(product_category, detected_categories,
                                        f"Article {slug} category mismatch: detected {detected_categories}, "
                                        f"but uses {product_category} product (ASIN: {asin})")

    def test_cta_button_text_matches_product(self):
        """Test that CTA button text matches the promoted product"""
        for slug, article in self.articles.items():
            with self.subTest(article=slug):
                if article['type'] == 'html':
                    soup = article['soup']
                    cta_buttons = soup.find_all('a', class_='cta-button')
                    
                    for button in cta_buttons:
                        button_text = button.get_text().lower()
                        href = button.get('href', '')
                        
                        # Extract ASIN from href
                        asin_match = re.search(r'/dp/([A-Z0-9]{10})', href)
                        if asin_match:
                            asin = asin_match.group(1)
                            if asin in self.expected_products:
                                product_info = self.expected_products[asin]
                                
                                # Check if button text is appropriate for product
                                if product_info['category'] == 'poop_bags':
                                    self.assertTrue(
                                        any(word in button_text for word in ['poop', 'bags', 'eco']),
                                        f"CTA button text '{button_text}' doesn't match poop bags product in {slug}"
                                    )
                                elif product_info['category'] == 'dog_toys':
                                    self.assertTrue(
                                        any(word in button_text for word in ['toy', 'eco', 'dog']),
                                        f"CTA button text '{button_text}' doesn't match dog toy product in {slug}"
                                    )
                                elif product_info['category'] == 'dog_treats':
                                    self.assertTrue(
                                        any(word in button_text for word in ['treat', 'organic']),
                                        f"CTA button text '{button_text}' doesn't match treats product in {slug}"
                                    )

    def test_inline_cta_links_match_product(self):
        """Test that inline CTA links match the product being promoted"""
        for slug, article in self.articles.items():
            with self.subTest(article=slug):
                # Find inline CTA links (styled links within content)
                inline_cta_pattern = r'<strong><a href="[^"]*amazon\.com[^"]*"[^>]*>([^<]+)</a></strong>'
                inline_ctas = re.findall(inline_cta_pattern, article['content'])
                
                # Find ASINs in the article
                asins = re.findall(r'/dp/([A-Z0-9]{10})', article['content'])
                
                for cta_text in inline_ctas:
                    cta_lower = cta_text.lower()
                    
                    # Check that CTA text matches at least one product in the article
                    matched_product = False
                    for asin in asins:
                        if asin in self.expected_products:
                            product_info = self.expected_products[asin]
                            if any(keyword.lower() in cta_lower for keyword in product_info['keywords']):
                                matched_product = True
                                break
                    
                    self.assertTrue(matched_product,
                                  f"Inline CTA '{cta_text}' in {slug} doesn't match any promoted product")

    def test_dropdown_functionality_in_homepage(self):
        """Test dropdown selections in homepage JavaScript"""
        js_file = self.site_dir / "js" / "home.js"
        if js_file.exists():
            with open(js_file, 'r', encoding='utf-8') as f:
                js_content = f.read()
            
            # Test category dropdown implementation
            self.assertIn('category-dropdown', js_content, "Category dropdown not implemented")
            self.assertIn('handleCategoryClick', js_content, "Category click handler missing")
            
            # Test tab functionality
            self.assertIn('handleTabClick', js_content, "Tab click handler missing")
            self.assertIn('tab-button', js_content, "Tab button functionality missing")

    def test_product_comparison_structure(self):
        """Test product comparison tables and cards structure"""
        for slug, article in self.articles.items():
            if 'vs' in slug or 'comparison' in slug.lower():
                with self.subTest(article=slug):
                    if article['type'] == 'html':
                        soup = article['soup']
                        
                        # Should have comparison elements
                        has_table = bool(soup.find('table'))
                        has_comparison_cards = bool(soup.find_all('div', class_=re.compile(r'.*card.*')))
                        
                        self.assertTrue(has_table or has_comparison_cards,
                                      f"Comparison article {slug} lacks comparison structure")
                        
                        # Should have multiple products
                        asins = re.findall(r'/dp/([A-Z0-9]{10})', article['content'])
                        unique_asins = list(set(asins))
                        self.assertGreaterEqual(len(unique_asins), 2,
                                              f"Comparison article {slug} should have at least 2 products")

    def test_utm_parameters_consistency(self):
        """Test that UTM parameters are consistently applied"""
        for slug, article in self.articles.items():
            with self.subTest(article=slug):
                # Find all Amazon links with UTM parameters - improved regex
                utm_links = re.findall(r'https?://[^"\s]*amazon\.com[^"\s]*utm_source[^"\s]*', article['content'])
                
                for link in utm_links:
                    parsed = urlparse(link)
                    query_params = parse_qs(parsed.query)
                    
                    # Check for required UTM parameters
                    self.assertIn('utm_source', query_params, f"Missing utm_source in {slug}: {link}")
                    self.assertIn('utm_campaign', query_params, f"Missing utm_campaign in {slug}: {link}")
                    
                    # Validate UTM values
                    utm_source = query_params['utm_source'][0]
                    utm_campaign = query_params['utm_campaign'][0]
                    
                    self.assertEqual(utm_source, 'site', f"Invalid utm_source in {slug}: {utm_source}")
                    self.assertEqual(utm_campaign, 'content', f"Invalid utm_campaign in {slug}: {utm_campaign}")

    def test_article_meta_tags(self):
        """Test that HTML articles have proper meta tags"""
        for slug, article in self.articles.items():
            if article['type'] == 'html':
                with self.subTest(article=slug):
                    soup = article['soup']
                    
                    # Check for required meta tags
                    title_tag = soup.find('title')
                    self.assertIsNotNone(title_tag, f"Missing title tag in {slug}")
                    
                    description_meta = soup.find('meta', attrs={'name': 'description'})
                    self.assertIsNotNone(description_meta, f"Missing meta description in {slug}")
                    
                    viewport_meta = soup.find('meta', attrs={'name': 'viewport'})
                    self.assertIsNotNone(viewport_meta, f"Missing viewport meta in {slug}")
                    
                    # Validate title length
                    title_text = title_tag.get_text()
                    self.assertLessEqual(len(title_text), 60, f"Title too long in {slug}: {len(title_text)} chars")
                    
                    # Validate description length
                    if description_meta:
                        desc_content = description_meta.get('content', '')
                        self.assertLessEqual(len(desc_content), 160, f"Meta description too long in {slug}: {len(desc_content)} chars")

    def test_no_broken_internal_links(self):
        """Test that internal links are not broken"""
        for slug, article in self.articles.items():
            with self.subTest(article=slug):
                # Find internal links
                internal_links = re.findall(r'href="(\.\./[^"]*)"', article['content'])
                
                for link in internal_links:
                    # Convert relative path to absolute
                    if link.startswith('../'):
                        target_path = self.site_dir / link[3:]
                        self.assertTrue(target_path.exists(), 
                                      f"Broken internal link in {slug}: {link}")

    def test_affiliate_tag_consistency(self):
        """Test that affiliate tags are consistent within each article"""
        for slug, article in self.articles.items():
            with self.subTest(article=slug):
                # Find all affiliate tags in the article - improved regex to avoid capturing extra characters
                tag_matches = re.findall(r'tag=([A-Za-z0-9-]+)', article['content'])
                
                if tag_matches:
                    # All tags in an article should be the same
                    unique_tags = list(set(tag_matches))
                    self.assertEqual(len(unique_tags), 1,
                                   f"Inconsistent affiliate tags in {slug}: {unique_tags}")
                    
                    # Should be a valid tag
                    tag = unique_tags[0]
                    self.assertIn(tag, self.valid_affiliate_tags,
                                f"Invalid affiliate tag in {slug}: {tag}")

    def test_product_cta_title_matches_content(self):
        """Test that product CTA titles match the actual content"""
        for slug, article in self.articles.items():
            if article['type'] == 'html':
                with self.subTest(article=slug):
                    soup = article['soup']
                    
                    # Find CTA sections with product titles
                    cta_sections = soup.find_all('div', class_='cta-section')
                    
                    for cta in cta_sections:
                        cta_text_elem = cta.find('div', class_='cta-text')
                        if cta_text_elem:
                            cta_text = cta_text_elem.get_text().lower()
                            
                            # Extract ASINs from links in this CTA
                            cta_links = cta.find_all('a')
                            for link in cta_links:
                                href = link.get('href', '')
                                asin_match = re.search(r'/dp/([A-Z0-9]{10})', href)
                                
                                if asin_match and asin_match.group(1) in self.expected_products:
                                    asin = asin_match.group(1)
                                    product_info = self.expected_products[asin]
                                    
                                    # CTA text should relate to product category
                                    category_keywords = {
                                        'poop_bags': ['poop', 'bags', 'eco'],
                                        'dog_toys': ['toy', 'eco', 'dog'],
                                        'dog_treats': ['treat', 'organic'],
                                        'dog_leash': ['leash', 'hemp'],
                                        'dog_bed': ['bed', 'comfort']
                                    }
                                    
                                    expected_keywords = category_keywords.get(product_info['category'], [])
                                    if expected_keywords:
                                        has_relevant_keyword = any(kw in cta_text for kw in expected_keywords)
                                        self.assertTrue(has_relevant_keyword,
                                                      f"CTA text '{cta_text}' doesn't match {product_info['category']} in {slug}")


def generate_detailed_test_report():
    """Generate a detailed test report with specific issues found"""
    suite = unittest.TestLoader().loadTestsFromTestCase(AffiliateContentTestSuite)
    
    # Create a custom test result to capture more details
    class DetailedTestResult(unittest.TextTestResult):
        def __init__(self, stream, descriptions, verbosity):
            super().__init__(stream, descriptions, verbosity)
            self.detailed_failures = []
            self.detailed_errors = []
            
        def addFailure(self, test, err):
            super().addFailure(test, err)
            self.detailed_failures.append((test, err))
            
        def addError(self, test, err):
            super().addError(test, err)
            self.detailed_errors.append((test, err))
    
    # Run tests with detailed results
    runner = unittest.TextTestRunner(
        verbosity=0, 
        stream=open('test_results_detailed.txt', 'w'),
        resultclass=DetailedTestResult
    )
    result = runner.run(suite)
    
    # Generate summary report
    print(f"\n{'='*80}")
    print("COMPREHENSIVE AFFILIATE CONTENT TEST REPORT")
    print(f"{'='*80}")
    print(f"Total Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success Rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    # Categorize issues
    issues_by_category = {
        'affiliate_tag_issues': [],
        'utm_parameter_issues': [],
        'product_matching_issues': [],
        'structure_issues': [],
        'other_issues': []
    }
    
    for test, traceback in result.failures:
        test_name = test._testMethodName
        article_name = str(test).split('(')[1].split(')')[0].replace('article=', '').replace("'", "")
        
        if 'affiliate_tag' in test_name:
            issues_by_category['affiliate_tag_issues'].append((article_name, test_name, traceback))
        elif 'utm_parameter' in test_name:
            issues_by_category['utm_parameter_issues'].append((article_name, test_name, traceback))
        elif 'product' in test_name or 'matching' in test_name:
            issues_by_category['product_matching_issues'].append((article_name, test_name, traceback))
        elif 'structure' in test_name or 'meta' in test_name:
            issues_by_category['structure_issues'].append((article_name, test_name, traceback))
        else:
            issues_by_category['other_issues'].append((article_name, test_name, traceback))
    
    # Print categorized issues
    for category, issues in issues_by_category.items():
        if issues:
            print(f"\n{'-'*60}")
            print(f"{category.upper().replace('_', ' ')}: {len(issues)} issues")
            print(f"{'-'*60}")
            
            for article, test_name, traceback in issues[:5]:  # Show first 5 issues per category
                print(f"• Article: {article}")
                print(f"  Test: {test_name}")
                # Extract the assertion error message
                error_lines = traceback.split('\n')
                assertion_error = next((line for line in error_lines if 'AssertionError:' in line), '')
                if assertion_error:
                    print(f"  Issue: {assertion_error.split('AssertionError: ')[-1]}")
                print()
            
            if len(issues) > 5:
                print(f"  ... and {len(issues) - 5} more issues in this category")
    
    return result


if __name__ == '__main__':
    # Install required packages if not available
    try:
        import bs4
    except ImportError:
        print("Installing required packages...")
        os.system("pip install beautifulsoup4 markdown")
    
    # Run tests
    result = generate_detailed_test_report()
    
    # Exit with error code if tests failed
    exit_code = len(result.failures) + len(result.errors)
    exit(exit_code) 