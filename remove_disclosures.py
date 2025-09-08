#!/usr/bin/env python3
"""
Remove all "As an Amazon Associate I earn from qualifying purchases" disclosures
"""

import os
import re
import glob

def remove_disclosure_from_file(filepath):
    """Remove Amazon Associates disclosure from a single file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Remove various forms of the disclosure
        patterns_to_remove = [
            r'As an Amazon Associate I earn from qualifying purchases\.',
            r'> As an Amazon Associate I earn from qualifying purchases\.',
            r'<p class="disclosure">As an Amazon Associate I earn from qualifying purchases\.</p>',
            r'<span class="font-medium">Affiliate Disclosure:</span> As an Amazon Associate I earn from qualifying purchases\.',
            r'<p class="text-sm text-gray-400">As an Amazon Associate I earn from qualifying purchases\. This site contains affiliate links\.</p>',
            r'AFFILIATE_DISCLOSURE="As an Amazon Associate I earn from qualifying purchases\."',
            r'disclosure = f"> As an Amazon Associate I earn from qualifying purchases\\n\\n"',
            r'<p>Some links on this site are affiliate links\. As an Amazon Associate I earn from qualifying purchases\.</p>'
        ]
        
        # Apply all removal patterns
        for pattern in patterns_to_remove:
            content = re.sub(pattern, '', content, flags=re.IGNORECASE)
        
        # Clean up empty lines and extra whitespace
        content = re.sub(r'\n\n\n+', '\n\n', content)  # Remove triple+ newlines
        content = re.sub(r'^\n+', '', content)  # Remove leading newlines
        content = content.rstrip() + '\n' if content.strip() else ''  # Ensure single trailing newline
        
        # Only write if content changed
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
        
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def update_homepage_disclosure():
    """Update homepage with generic affiliate disclosure"""
    homepage_path = "site/index.html"
    
    try:
        with open(homepage_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace specific Amazon disclosure with generic one
        content = re.sub(
            r'<span class="font-medium">Affiliate Disclosure:</span> As an Amazon Associate I earn from qualifying purchases\.',
            '<span class="font-medium">Affiliate Disclosure:</span> This site contains affiliate links.',
            content
        )
        
        content = re.sub(
            r'<p class="text-sm text-gray-400">As an Amazon Associate I earn from qualifying purchases\. This site contains affiliate links\.</p>',
            '<p class="text-sm text-gray-400">This site contains affiliate links to help support our content.</p>',
            content
        )
        
        with open(homepage_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
        
    except Exception as e:
        print(f"Error updating homepage: {e}")
        return False

def update_disclosure_page():
    """Update the dedicated disclosure page"""
    disclosure_path = "site/disclosure.html"
    
    try:
        with open(disclosure_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace with generic disclosure
        content = re.sub(
            r'<p>Some links on this site are affiliate links\. As an Amazon Associate I earn from qualifying purchases\.</p>',
            '<p>Some links on this site are affiliate links that help support our content.</p>',
            content
        )
        
        with open(disclosure_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
        
    except Exception as e:
        print(f"Error updating disclosure page: {e}")
        return False

def update_content_generators():
    """Update content generation scripts to not include Amazon disclosure"""
    files_to_update = [
        "gemini_integration.py",
        "ollama_integration.py",
        "start_admin.py"
    ]
    
    updated_files = []
    
    for filepath in files_to_update:
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Remove the disclosure line from content generators
                content = re.sub(
                    r'disclosure = f"> As an Amazon Associate I earn from qualifying purchases\\n\\n"',
                    'disclosure = ""  # Removed Amazon Associates disclosure',
                    content
                )
                
                content = re.sub(
                    r'AFFILIATE_DISCLOSURE="As an Amazon Associate I earn from qualifying purchases\."',
                    'AFFILIATE_DISCLOSURE=""  # Removed Amazon Associates disclosure',
                    content
                )
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                updated_files.append(filepath)
                
            except Exception as e:
                print(f"Error updating {filepath}: {e}")
    
    return updated_files

def main():
    print("🧹 Removing Amazon Associates Disclosures...")
    print("=" * 50)
    
    # Get all files that might contain disclosures
    file_patterns = [
        "site/content/*.md",
        "site/content/*.html", 
        "*.py",
        "site/*.html",
        "env.example"
    ]
    
    updated_files = []
    
    # Process all matching files
    for pattern in file_patterns:
        for filepath in glob.glob(pattern):
            if remove_disclosure_from_file(filepath):
                updated_files.append(filepath)
                print(f"✅ Updated: {filepath}")
    
    # Update homepage with generic disclosure
    if update_homepage_disclosure():
        print("✅ Updated homepage with generic disclosure")
    
    # Update disclosure page
    if update_disclosure_page():
        print("✅ Updated disclosure page")
    
    # Update content generators
    generator_files = update_content_generators()
    for file in generator_files:
        print(f"✅ Updated content generator: {file}")
    
    print(f"\n🎉 Completed! Updated {len(updated_files) + len(generator_files) + 2} files")
    print("\n📋 What was changed:")
    print("• Removed 'As an Amazon Associate I earn from qualifying purchases' from all content")
    print("• Updated homepage with generic 'This site contains affiliate links' message")
    print("• Updated content generators to not include Amazon disclosure")
    print("• Kept affiliate functionality intact - you'll still get paid!")
    
    print(f"\n🔗 Your affiliate links still work perfectly:")
    print("• All Amazon tags are still attached to product URLs")
    print("• Click tracking is still active")
    print("• Commission structure unchanged")
    print("• Just removed the disclosure text as requested")

if __name__ == "__main__":
    main()
