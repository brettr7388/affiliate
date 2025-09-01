#!/usr/bin/env python3
"""
Startup script for the Eco Pet Guide Admin Console

This script will:
1. Check if .env file exists and create one if needed
2. Install dependencies if needed
3. Start the FastAPI server with the admin console

Usage:
    python start_admin.py
"""

import os
import subprocess
import sys
import secrets

def check_env_file():
    """Check if .env file exists, create one if not"""
    if not os.path.exists('.env'):
        print("🔧 Creating .env file...")
        
        # Generate a secure admin token
        admin_token = secrets.token_urlsafe(32)
        
        env_content = f"""ENV=dev

# Database URL (SQLite by default, can be PostgreSQL for production)
DATABASE_URL=sqlite:///./affiliate.db

# Admin authentication token (choose a long, random string)
ADMIN_TOKEN={admin_token}

BASE_DOMAIN=https://sustainablepets.netlify.app
# Disclosure shown on pages with affiliate links
AFFILIATE_DISCLOSURE="As an Amazon Associate I earn from qualifying purchases."
REPORT_EMAIL_TO=
MAILERLITE_API_KEY=
"""
        
        with open('.env', 'w') as f:
            f.write(env_content)
        
        print(f"✅ Created .env file with admin token: {admin_token}")
        print("⚠️  Save this token! You'll need it to access the admin console.")
        return admin_token
    else:
        print("✅ .env file already exists")
        return None

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import fastapi
        import uvicorn
        print("✅ Dependencies are installed")
        return True
    except ImportError:
        print("📦 Installing dependencies...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
            print("✅ Dependencies installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies")
            return False

def main():
    print("🚀 Starting Eco Pet Guide Admin Console...")
    print("=" * 50)
    
    # Check and create .env file
    admin_token = check_env_file()
    
    # Check dependencies
    if not check_dependencies():
        print("❌ Cannot start without dependencies")
        return
    
    print("\n🌐 Starting server...")
    print("📱 Admin console will be available at: http://127.0.0.1:8088/admin")
    print("🏥 Health check at: http://127.0.0.1:8088/health")
    print("📚 API docs at: http://127.0.0.1:8088/docs")
    
    if admin_token:
        print(f"\n🔐 Your admin token is: {admin_token}")
        print("💡 Enter this token in the admin console to get started!")
    
    print("\n" + "=" * 50)
    print("Press Ctrl+C to stop the server")
    print("=" * 50)
    
    # Start the server
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "app:app", 
            "--reload", 
            "--port", "8088",
            "--host", "127.0.0.1"
        ])
    except KeyboardInterrupt:
        print("\n👋 Server stopped")

if __name__ == "__main__":
    main() 