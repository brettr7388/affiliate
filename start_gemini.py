#!/usr/bin/env python3
"""
Test Google Gemini API integration
"""

import os
import sys
from dotenv import load_dotenv

def test_gemini_setup():
    """Test if Gemini API is properly configured"""
    print("🚀 Testing Gemini API Setup...")
    
    # Load environment variables
    load_dotenv()
    
    # Check if API key is set
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "your-gemini-api-key-here":
        print("❌ GEMINI_API_KEY not found in environment variables!")
        print("   Please:")
        print("   1. Get your API key from: https://aistudio.google.com/app/apikey")
        print("   2. Copy .env.example to .env")
        print("   3. Add your API key to the .env file")
        return False
    
    print("✅ API key found in environment")
    return True

def test_gemini_connection():
    """Test Gemini API connection"""
    print("\n🔗 Testing Gemini API Connection...")
    
    try:
        from gemini_integration import GeminiArticleGenerator
        generator = GeminiArticleGenerator()
        
        if generator.test_connection():
            print("✅ Gemini API connection successful!")
            return True
        else:
            print("❌ Gemini API connection failed")
            return False
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Make sure to install: pip install google-generativeai")
        return False
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

def test_article_generation():
    """Test article generation"""
    print("\n🧠 Testing Article Generation...")
    
    try:
        from gemini_integration import GeminiArticleGenerator
        generator = GeminiArticleGenerator()
        
        # Test a simple generation
        test_content = generator.generate_article(
            product_info={
                "offer": "Test Eco-Friendly Dog Toy",
                "dest_url": "https://example.com",
                "slug": "test"
            },
            article_type="review",
            tone="casual",
            keywords="eco-friendly, sustainable, dog toy",
            length="short",
            include_comparison="no",
            target_audience="pet-owners",
            seo_focus="eco-friendly pet products"
        )
        
        if test_content and len(test_content) > 100:
            print("✅ Article generation successful!")
            print(f"   Generated {len(test_content)} characters")
            print("   First 100 chars:", test_content[:100] + "...")
            return True
        else:
            print("❌ Article generation failed - no content generated")
            return False
            
    except Exception as e:
        print(f"❌ Generation error: {e}")
        return False

def main():
    print("🤖 Google Gemini API Integration Test")
    print("=" * 50)
    
    # Test setup
    if not test_gemini_setup():
        print("\n❌ Setup failed. Please configure your API key first.")
        return
    
    # Test connection
    if not test_gemini_connection():
        print("\n❌ Connection failed. Check your API key and internet connection.")
        return
    
    # Test generation
    if test_article_generation():
        print("\n🎉 Everything is working perfectly!")
        print("\n📝 You can now:")
        print("   1. Start your app: python app.py")
        print("   2. Go to your admin console: http://127.0.0.1:8088/admin")
        print("   3. Use the '🤖 AI Article Generator' section")
        print("   4. Click '🔗 Test Gemini' to verify connection")
        print("   5. Generate AI articles about your products!")
        print("\n💡 Gemini API Pricing Info:")
        print("   - Free tier: 15 requests/min, 1M tokens/min, 1500 requests/day")
        print("   - Very affordable pay-as-you-go rates after free tier")
    else:
        print("\n❌ Article generation test failed.")

if __name__ == "__main__":
    main()
