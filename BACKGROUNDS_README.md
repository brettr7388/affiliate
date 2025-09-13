# Hidden Backgrounds for Social Media Videos

This setup allows you to store background files for your social media videos that are publicly accessible via URL but hidden from your website visitors.

## Setup Instructions

### 1. Add Your Background Files
Place your background files (MP4, JPG, PNG, etc.) in the `background_sources/` folder:
```
background_sources/
├── nature_bg_1.mp4
├── nature_bg_2.jpg
├── pet_playground.mp4
└── eco_theme.png
```

### 2. Run the Setup Script
```bash
node scripts/setupBackgrounds.js
```

This will copy all files from `background_sources/` to `site/backgrounds/` where they can be served by your FastAPI app.

### 3. Access Your Backgrounds
Your backgrounds will be available at:
```
https://your-domain.com/backgrounds/filename.mp4
https://your-domain.com/backgrounds/filename.jpg
```

## For n8n and HeyGen Integration

Use these URLs in your n8n workflows and HeyGen video creation:
- **Background Video**: `https://your-domain.com/backgrounds/nature_bg_1.mp4`
- **Background Image**: `https://your-domain.com/backgrounds/eco_theme.png`

## Important Notes

- ✅ Backgrounds are publicly accessible via URL
- ✅ Not linked anywhere on your website (hidden from visitors)
- ✅ Perfect for social media video automation
- ✅ Source files are excluded from git (keeps repo clean)
- ✅ Easy to update - just add new files and run the script

## Updating Backgrounds

1. Add new files to `background_sources/`
2. Run `node scripts/setupBackgrounds.js`
3. Deploy your changes

## File Structure

```
affiliate/
├── background_sources/          # Your source files (excluded from git)
├── site/backgrounds/            # Publicly served files
├── scripts/setupBackgrounds.js  # Setup script
└── app.py                       # FastAPI route added
```

The `backgrounds/` folder will be served by your FastAPI app but won't appear in any website navigation or sitemaps.
