#!/usr/bin/env python3
"""
Fix Affiliate Link Issues Script
Automatically fixes identified issues in affiliate content and validates corrections
"""

import os
import re
import json
import glob
from pathlib import Path
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from bs4 import BeautifulSoup
import subprocess


class AffiliateContentFixer:
    """
    Fixes affiliate content issues automatically
    """
    
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.site_dir = self.base_dir / "site"
        self.content_dir = self.site_dir / "content"
        
        # Expected product mappings with correct titles
        self.product_mappings = {
            "B07MYPFMZP": {
                "name": "Earth-Rated Biodegradable Poop Bags",
                "category": "poop_bags",
                "correct_title": "AmazonBiodegradablePoopBags",
                "keywords": ["poop", "biodegradable", "earth-rated", "compostable"]
            },
            "B004A7X27M": {
                "name": "Kong Classic Dog Toy",
                "category": "dog_toys", 
                "correct_title": "AmazonEcoFriendlyDogToys",
                "keywords": ["kong", "toy", "eco-friendly", "dog toy"]
            },
            "B093CLBJDW": {
                "name": "WAG Expedition Organic Banana & Coconut Treats",
                "category": "dog_treats",
                "correct_title": "AmazonOrganicDogTreats",
                "keywords": ["wag", "organic", "banana", "coconut", "treats"]
            },
            "B00C9L67XW": {
                "name": "The Good Dog Company Hemp Canvas Leash",
                "category": "dog_leash",
                "correct_title": "AmazonHempDogLeash",
                "keywords": ["hemp", "leash", "canvas", "good dog company"]
            },
            "B00TQ47CPW": {
                "name": "PetFusion Ultimate Dog Bed Lounge",
                "category": "dog_bed",
                "correct_title": "AmazonEcoFriendlyDogBeds",
                "keywords": ["petfusion", "dog bed", "ultimate", "lounge", "orthopedic"]
            },
            "B0DWBQXQ46": {
                "name": "West Paw Toppl Treat Dispensing Toy",
                "category": "dog_toys",
                "correct_title": "WestPawTopplToy",
                "keywords": ["west paw", "toppl", "treat", "dispensing", "eco"]
            }
        }
        
        self.valid_affiliate_tag = "test0b252-20"
        self.fixes_applied = []
        
    def fix_affiliate_tags_in_markdown(self):
        """Fix affiliate tags with extra characters in markdown files"""
        print("🔧 Fixing affiliate tags in Markdown files...")
        
        for md_file in self.content_dir.glob("*.md"):
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Fix affiliate tags with closing parenthesis
            content = re.sub(r'tag=([A-Za-z0-9-]+)\)', f'tag=\\1', content)
            
            # Fix UTM parameters with closing parenthesis
            content = re.sub(r'utm_campaign=([A-Za-z0-9-]+)\)', f'utm_campaign=\\1', content)
            content = re.sub(r'utm_source=([A-Za-z0-9-]+)\)', f'utm_source=\\1', content)
            
            if content != original_content:
                with open(md_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.fixes_applied.append(f"Fixed affiliate tags in {md_file.name}")
                print(f"  ✓ Fixed {md_file.name}")
    
    def fix_affiliate_tags_in_html(self):
        """Fix affiliate tags with extra characters in HTML files"""
        print("🔧 Fixing affiliate tags in HTML files...")
        
        for html_file in self.content_dir.glob("*.html"):
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Fix affiliate tags with closing parenthesis
            content = re.sub(r'tag=([A-Za-z0-9-]+)\)', f'tag=\\1', content)
            
            # Fix UTM parameters with closing parenthesis  
            content = re.sub(r'utm_campaign=([A-Za-z0-9-]+)\)', f'utm_campaign=\\1', content)
            content = re.sub(r'utm_source=([A-Za-z0-9-]+)\)', f'utm_source=\\1', content)
            
            if content != original_content:
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.fixes_applied.append(f"Fixed affiliate tags in {html_file.name}")
                print(f"  ✓ Fixed {html_file.name}")
    
    def validate_product_title_matching(self):
        """Validate and report product title matching issues"""
        print("🔍 Validating product title matching...")
        
        issues_found = []
        
        for md_file in self.content_dir.glob("*.md"):
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            title_lower = content.lower()
            
            # Find ASINs and their associated titles
            asins = re.findall(r'/dp/([A-Z0-9]{10})', content)
            
            for asin in asins:
                if asin in self.product_mappings:
                    product_info = self.product_mappings[asin]
                    
                    # Check if article content matches product
                    keywords_found = []
                    for keyword in product_info['keywords']:
                        if keyword.lower() in title_lower:
                            keywords_found.append(keyword)
                    
                    if len(keywords_found) == 0:
                        issues_found.append({
                            'file': md_file.name,
                            'asin': asin,
                            'product': product_info['name'],
                            'expected_keywords': product_info['keywords'],
                            'issue': 'Product does not match article content'
                        })
        
        if issues_found:
            print("  ⚠️  Product matching issues found:")
            for issue in issues_found:
                print(f"    • {issue['file']}: {issue['product']} (ASIN: {issue['asin']})")
                print(f"      Expected keywords: {issue['expected_keywords']}")
        else:
            print("  ✅ All products match their article content")
        
        return issues_found
    
    def validate_affiliate_link_consistency(self):
        """Validate affiliate link consistency across files"""
        print("🔍 Validating affiliate link consistency...")
        
        inconsistencies = []
        
        for file_path in list(self.content_dir.glob("*.md")) + list(self.content_dir.glob("*.html")):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find all affiliate tags
            tag_matches = re.findall(r'tag=([A-Za-z0-9-]+)', content)
            
            if tag_matches:
                unique_tags = list(set(tag_matches))
                if len(unique_tags) > 1:
                    inconsistencies.append({
                        'file': file_path.name,
                        'tags': unique_tags,
                        'issue': 'Multiple different affiliate tags in same file'
                    })
                elif unique_tags[0] != self.valid_affiliate_tag and unique_tags[0] != "YOUR-AMAZON-ASSOCIATES-TAG":
                    inconsistencies.append({
                        'file': file_path.name,
                        'tags': unique_tags,
                        'issue': f'Invalid affiliate tag: {unique_tags[0]}'
                    })
        
        if inconsistencies:
            print("  ⚠️  Affiliate link inconsistencies found:")
            for issue in inconsistencies:
                print(f"    • {issue['file']}: {issue['issue']}")
                print(f"      Tags found: {issue['tags']}")
        else:
            print("  ✅ All affiliate links are consistent")
        
        return inconsistencies
    
    def validate_utm_parameters(self):
        """Validate UTM parameter consistency"""
        print("🔍 Validating UTM parameters...")
        
        utm_issues = []
        
        for file_path in list(self.content_dir.glob("*.md")) + list(self.content_dir.glob("*.html")):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find all UTM links
            utm_links = re.findall(r'https?://[^"\s]*amazon\.com[^"\s]*utm_source[^"\s]*', content)
            
            for link in utm_links:
                try:
                    parsed = urlparse(link)
                    query_params = parse_qs(parsed.query)
                    
                    # Check UTM parameters
                    if 'utm_source' in query_params:
                        utm_source = query_params['utm_source'][0]
                        if utm_source != 'site':
                            utm_issues.append({
                                'file': file_path.name,
                                'link': link,
                                'issue': f'Invalid utm_source: {utm_source}'
                            })
                    
                    if 'utm_campaign' in query_params:
                        utm_campaign = query_params['utm_campaign'][0]
                        if utm_campaign != 'content':
                            utm_issues.append({
                                'file': file_path.name,
                                'link': link,
                                'issue': f'Invalid utm_campaign: {utm_campaign}'
                            })
                
                except Exception as e:
                    utm_issues.append({
                        'file': file_path.name,
                        'link': link,
                        'issue': f'URL parsing error: {str(e)}'
                    })
        
        if utm_issues:
            print("  ⚠️  UTM parameter issues found:")
            for issue in utm_issues:
                print(f"    • {issue['file']}: {issue['issue']}")
        else:
            print("  ✅ All UTM parameters are correct")
        
        return utm_issues
    
    def validate_cta_button_text(self):
        """Validate CTA button text matches products"""
        print("🔍 Validating CTA button text...")
        
        cta_issues = []
        
        for html_file in self.content_dir.glob("*.html"):
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            try:
                soup = BeautifulSoup(content, 'html.parser')
                cta_buttons = soup.find_all('a', class_='cta-button')
                
                for button in cta_buttons:
                    button_text = button.get_text().lower()
                    href = button.get('href', '')
                    
                    # Extract ASIN from href
                    asin_match = re.search(r'/dp/([A-Z0-9]{10})', href)
                    if asin_match:
                        asin = asin_match.group(1)
                        if asin in self.product_mappings:
                            product_info = self.product_mappings[asin]
                            
                            # Check if button text matches product category
                            category_keywords = {
                                'poop_bags': ['poop', 'bags', 'eco'],
                                'dog_toys': ['toy', 'eco', 'dog'],
                                'dog_treats': ['treat', 'organic'],
                                'dog_leash': ['leash', 'hemp'],
                                'dog_bed': ['bed', 'comfort']
                            }
                            
                            expected_keywords = category_keywords.get(product_info['category'], [])
                            if expected_keywords:
                                has_relevant_keyword = any(kw in button_text for kw in expected_keywords)
                                if not has_relevant_keyword:
                                    cta_issues.append({
                                        'file': html_file.name,
                                        'button_text': button_text,
                                        'product': product_info['name'],
                                        'expected_keywords': expected_keywords,
                                        'issue': 'CTA button text does not match product category'
                                    })
            
            except Exception as e:
                cta_issues.append({
                    'file': html_file.name,
                    'issue': f'HTML parsing error: {str(e)}'
                })
        
        if cta_issues:
            print("  ⚠️  CTA button text issues found:")
            for issue in cta_issues:
                print(f"    • {issue['file']}: {issue.get('button_text', 'N/A')}")
                if 'expected_keywords' in issue:
                    print(f"      Expected keywords: {issue['expected_keywords']}")
        else:
            print("  ✅ All CTA button text matches products")
        
        return cta_issues
    
    def validate_dropdown_functionality(self):
        """Validate dropdown functionality in JavaScript"""
        print("🔍 Validating dropdown functionality...")
        
        js_file = self.site_dir / "js" / "home.js"
        dropdown_issues = []
        
        if js_file.exists():
            with open(js_file, 'r', encoding='utf-8') as f:
                js_content = f.read()
            
            required_functions = [
                'handleCategoryClick',
                'handleTabClick',
                'category-dropdown'
            ]
            
            for func in required_functions:
                if func not in js_content:
                    dropdown_issues.append({
                        'file': 'home.js',
                        'issue': f'Missing required function/element: {func}'
                    })
            
            # Check for proper event listeners
            if 'addEventListener' not in js_content:
                dropdown_issues.append({
                    'file': 'home.js',
                    'issue': 'Missing event listeners setup'
                })
        else:
            dropdown_issues.append({
                'file': 'home.js',
                'issue': 'JavaScript file not found'
            })
        
        if dropdown_issues:
            print("  ⚠️  Dropdown functionality issues found:")
            for issue in dropdown_issues:
                print(f"    • {issue['file']}: {issue['issue']}")
        else:
            print("  ✅ All dropdown functionality is properly implemented")
        
        return dropdown_issues
    
    def run_comprehensive_validation(self):
        """Run all validation checks"""
        print("🚀 Starting comprehensive affiliate content validation...\n")
        
        # Apply fixes first
        self.fix_affiliate_tags_in_markdown()
        self.fix_affiliate_tags_in_html()
        
        print()
        
        # Run validations
        product_issues = self.validate_product_title_matching()
        affiliate_issues = self.validate_affiliate_link_consistency()
        utm_issues = self.validate_utm_parameters()
        cta_issues = self.validate_cta_button_text()
        dropdown_issues = self.validate_dropdown_functionality()
        
        # Summary
        total_issues = len(product_issues) + len(affiliate_issues) + len(utm_issues) + len(cta_issues) + len(dropdown_issues)
        
        print(f"\n{'='*80}")
        print("COMPREHENSIVE VALIDATION SUMMARY")
        print(f"{'='*80}")
        print(f"Fixes Applied: {len(self.fixes_applied)}")
        print(f"Total Issues Found: {total_issues}")
        print(f"  • Product Matching Issues: {len(product_issues)}")
        print(f"  • Affiliate Link Issues: {len(affiliate_issues)}")
        print(f"  • UTM Parameter Issues: {len(utm_issues)}")
        print(f"  • CTA Button Issues: {len(cta_issues)}")
        print(f"  • Dropdown Issues: {len(dropdown_issues)}")
        
        if self.fixes_applied:
            print(f"\n📝 Applied Fixes:")
            for fix in self.fixes_applied:
                print(f"  • {fix}")
        
        if total_issues == 0:
            print(f"\n🎉 All validation checks passed! Your affiliate content is properly configured.")
        else:
            print(f"\n⚠️  Please review and fix the issues listed above.")
        
        return {
            'fixes_applied': len(self.fixes_applied),
            'total_issues': total_issues,
            'product_issues': product_issues,
            'affiliate_issues': affiliate_issues,
            'utm_issues': utm_issues,
            'cta_issues': cta_issues,
            'dropdown_issues': dropdown_issues
        }
    
    def generate_detailed_report(self, results):
        """Generate a detailed report file"""
        report_path = self.base_dir / "affiliate_validation_report.json"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"\n📊 Detailed report saved to: {report_path}")
        
        # Also create a human-readable report
        txt_report_path = self.base_dir / "affiliate_validation_report.txt"
        with open(txt_report_path, 'w', encoding='utf-8') as f:
            f.write("AFFILIATE CONTENT VALIDATION REPORT\n")
            f.write("="*50 + "\n\n")
            
            f.write(f"Fixes Applied: {results['fixes_applied']}\n")
            f.write(f"Total Issues: {results['total_issues']}\n\n")
            
            for category, issues in results.items():
                if isinstance(issues, list) and issues and category != 'fixes_applied':
                    f.write(f"\n{category.upper().replace('_', ' ')}:\n")
                    f.write("-" * 30 + "\n")
                    for issue in issues:
                        f.write(f"• File: {issue.get('file', 'Unknown')}\n")
                        f.write(f"  Issue: {issue.get('issue', 'Unknown issue')}\n\n")
        
        print(f"📄 Human-readable report saved to: {txt_report_path}")


if __name__ == '__main__':
    fixer = AffiliateContentFixer()
    results = fixer.run_comprehensive_validation()
    fixer.generate_detailed_report(results) 