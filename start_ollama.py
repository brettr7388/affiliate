#!/usr/bin/env python3
"""
Start Ollama and test the integration
"""

import subprocess
import time
import sys

def start_ollama():
    """Start Ollama if it's not running"""
    print("🚀 Starting Ollama...")
    
    try:
        # Test if Ollama is already running
        from ollama_integration import OllamaArticleGenerator
        generator = OllamaArticleGenerator()
        
        if generator.test_connection():
            print("✅ Ollama is already running!")
            return True
        else:
            print("🔄 Ollama not responding, starting it...")
    except ImportError:
        print("❌ Ollama integration module not found")
        return False
    
    try:
        # Start Ollama in the background
        subprocess.Popen(["ollama", "serve"], 
                        stdout=subprocess.DEVNULL, 
                        stderr=subprocess.DEVNULL)
        
        print("⏳ Waiting for Ollama to start...")
        time.sleep(5)  # Wait for Ollama to start
        
        # Test connection again
        generator = OllamaArticleGenerator()
        if generator.test_connection():
            print("✅ Ollama started successfully!")
            return True
        else:
            print("❌ Ollama failed to start")
            return False
            
    except FileNotFoundError:
        print("❌ Ollama not found. Please install Ollama first:")
        print("   Visit: https://ollama.ai/download")
        return False
    except Exception as e:
        print(f"❌ Error starting Ollama: {e}")
        return False

def test_model():
    """Test if the llama3.1:8b model is available"""
    print("\n🧠 Testing model availability...")
    
    try:
        from ollama_integration import OllamaArticleGenerator
        generator = OllamaArticleGenerator()
        
        # Test a simple generation
        test_content = generator.generate_article(
            product_info={
                "offer": "Test Product",
                "dest_url": "https://example.com",
                "slug": "test"
            },
            article_type="review",
            tone="casual",
            keywords="test, example",
            length="short",
            include_comparison="no",
            target_audience="pet-owners",
            seo_focus="general"
        )
        
        if test_content and len(test_content) > 100:
            print("✅ Model test successful! Generated content:")
            print(f"   Length: {len(test_content)} characters")
            print("   First 100 chars:", test_content[:100] + "...")
            return True
        else:
            print("❌ Model test failed - no content generated")
            return False
            
    except Exception as e:
        print(f"❌ Model test error: {e}")
        return False

def main():
    print("🤖 Ollama Integration Test")
    print("=" * 40)
    
    # Start Ollama
    if not start_ollama():
        print("\n❌ Cannot proceed without Ollama")
        return
    
    # Test model
    if test_model():
        print("\n🎉 Everything is working perfectly!")
        print("\n📝 You can now:")
        print("   1. Go to your admin console: http://127.0.0.1:8088/admin")
        print("   2. Use the '🤖 AI Article Generator' section")
        print("   3. Click '🔗 Test Ollama' to verify connection")
        print("   4. Generate AI articles about your products!")
    else:
        print("\n❌ Model test failed. Check Ollama logs for errors.")

if __name__ == "__main__":
    main()
