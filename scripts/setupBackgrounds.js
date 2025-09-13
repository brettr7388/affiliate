// scripts/setupBackgrounds.js
// Run this script once to create a /site/backgrounds folder
// and copy your background files there.
//
// Usage: node scripts/setupBackgrounds.js

const fs = require('fs');
const path = require('path');

// change these paths as needed
const sourceDir = path.join(__dirname, '..', 'background_sources');
const destDir   = path.join(__dirname, '..', 'site', 'backgrounds');

// Ensure destination directory exists
if (!fs.existsSync(destDir)) {
  fs.mkdirSync(destDir, { recursive: true });
  console.log(`Created ${destDir}`);
}

// Check if source directory exists
if (!fs.existsSync(sourceDir)) {
  console.log(`⚠️  Source directory ${sourceDir} does not exist.`);
  console.log('Please create it and add your background files there.');
  process.exit(1);
}

// Copy all files from sourceDir to destDir
const files = fs.readdirSync(sourceDir);
if (files.length === 0) {
  console.log(`⚠️  No files found in ${sourceDir}`);
  console.log('Please add your background files (MP4, JPG, PNG, etc.) to the background_sources folder.');
  process.exit(1);
}

files.forEach(file => {
  const src = path.join(sourceDir, file);
  const dest = path.join(destDir, file);
  
  // Check if it's a file (not a directory)
  if (fs.statSync(src).isFile()) {
    fs.copyFileSync(src, dest);
    console.log(`✅ Copied ${file} to ${dest}`);
  }
});

console.log(`\n🎉 Background setup complete! Copied ${files.length} files.`);
console.log(`\n📁 Your backgrounds are now available at:`);
console.log(`   https://your-domain.com/backgrounds/<filename>`);
console.log(`\n💡 Add your background files to: ${sourceDir}`);
console.log(`   Then run this script again to update the backgrounds.`);
