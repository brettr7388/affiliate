
# Image Rotation Setup Instructions

## Current Status
✅ Image rotation system implemented
✅ All articles updated with rotation code
✅ Directory structure created
✅ Placeholder images generated

## Next Steps

### 1. Replace Placeholder Images
Copy your generated images to the appropriate directories:

```
site/images/rotating/
├── toy/
│   ├── toy1.png  ← Replace with your toy image 1
│   ├── toy2.png  ← Replace with your toy image 2
│   ├── toy3.png  ← Replace with your toy image 3
│   └── toy4.png  ← Replace with your toy image 4
├── bag/
│   ├── bag1.png  ← Replace with your bag image 1
│   ├── bag2.png  ← Replace with your bag image 2
│   └── bag3.png  ← Replace with your bag image 3
├── bowl/
│   ├── bowl1.png ← Replace with your bowl image 1
│   ├── bowl2.png ← Replace with your bowl image 2
│   └── bowl3.png ← Replace with your bowl image 3
├── leash/
│   ├── leash1.png ← Replace with your leash image 1
│   ├── leash2.png ← Replace with your leash image 2
│   └── leash3.png ← Replace with your leash image 3
├── bed/
│   ├── bed1.png  ← Replace with your bed image 1
│   ├── bed2.png  ← Replace with your bed image 2
│   └── bed3.png  ← Replace with your bed image 3
├── treat/
│   ├── treat1.png ← Replace with your treat image 1
│   ├── treat2.png ← Replace with your treat image 2
│   └── treat3.png ← Replace with your treat image 3
└── all/
    ├── all1.png  ← Replace with your general image 1
    ├── all2.png  ← Replace with your general image 2
    └── all3.png  ← Replace with your general image 3
```

### 2. How It Works
- Images rotate automatically on page refresh
- Each category shows the appropriate images
- Same image displays for the entire day (consistent experience)
- Manual refresh button available on each page

### 3. Testing
1. Open any article in your browser
2. Refresh the page to see different images
3. Use the "🔄 Refresh Images" button for manual rotation
4. Check that the correct category images appear

### 4. Categories by Article Type
- **Toy articles**: Show toy1.png, toy2.png, toy3.png, toy4.png
- **Bag articles**: Show bag1.png, bag2.png, bag3.png
- **Bowl articles**: Show bowl1.png, bowl2.png, bowl3.png
- **Leash articles**: Show leash1.png, leash2.png, leash3.png
- **Bed articles**: Show bed1.png, bed2.png, bed3.png
- **Treat articles**: Show treat1.png, treat2.png, treat3.png
- **General articles**: Show all1.png, all2.png, all3.png

## File Naming Convention
Make sure your images follow this exact naming:
- `{category}{number}.png`
- Examples: `toy1.png`, `bag2.png`, `bowl3.png`, etc.
