#!/usr/bin/env python3
"""
Add ADMIN_TOKEN to existing .env file
"""

import os
import secrets

def add_admin_token():
    """Add ADMIN_TOKEN to existing .env file"""
    
    # Generate a secure admin token
    admin_token = secrets.token_urlsafe(32)
    
    # Read existing .env file
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            content = f.read()
        
        # Check if ADMIN_TOKEN already exists
        if 'ADMIN_TOKEN=' in content:
            print("✅ ADMIN_TOKEN already exists in .env file")
            return
        
        # Add ADMIN_TOKEN to the end of the file
        with open('.env', 'a') as f:
            f.write(f"\n# Admin authentication token\nADMIN_TOKEN={admin_token}\n")
        
        print(f"✅ Added ADMIN_TOKEN to .env file: {admin_token}")
        print("🔐 Save this token! You'll need it to access the admin console.")
        
    else:
        print("❌ .env file not found")

if __name__ == "__main__":
    add_admin_token() 