#!/usr/bin/env python3
"""
Add static file serving to FastAPI app
"""

def add_static_files():
    with open('app.py', 'r') as f:
        content = f.read()
    
    # Add StaticFiles import
    import_line = 'from fastapi import FastAPI, Request, HTTPException, Query\nfrom fastapi.responses import RedirectResponse, JSONResponse, HTMLResponse, Response\nfrom fastapi.middleware.cors import CORSMiddleware'
    
    new_import_line = 'from fastapi import FastAPI, Request, HTTPException, Query\nfrom fastapi.responses import RedirectResponse, JSONResponse, HTMLResponse, Response\nfrom fastapi.middleware.cors import CORSMiddleware\nfrom fastapi.staticfiles import StaticFiles'
    
    content = content.replace(import_line, new_import_line)
    
    # Add static file mounting after CORS middleware
    cors_section = '''app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)'''
    
    new_cors_section = '''app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

# Mount static files
app.mount("/images", StaticFiles(directory="site/images"), name="images")
app.mount("/css", StaticFiles(directory="site/css"), name="css")
app.mount("/js", StaticFiles(directory="site/js"), name="js")'''
    
    content = content.replace(cors_section, new_cors_section)
    
    with open('app.py', 'w') as f:
        f.write(content)
    
    print("✅ Added static file serving to FastAPI app!")

if __name__ == "__main__":
    add_static_files()
