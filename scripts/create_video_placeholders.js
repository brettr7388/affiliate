// Create placeholder files for the 9 Mixkit dog videos
const fs = require('fs');
const path = require('path');

const videos = [
  'mixkit-playfull-border-collie-dog-playing-with-a-toy-ball-50688-hd-ready.mp4',
  'mixkit-a-young-pitbull-dog-bitting-and-playing-with-a-teddy-50676-hd-ready.mp4',
  'mixkit-dog-tied-to-his-leash-on-the-street-19543-hd-ready.mp4',
  'mixkit-husky-sled-dogs-pulling-in-slow-motion-7361-hd-ready.mp4',
  'mixkit-a-dog-resting-on-the-grass-next-to-a-dog-1479-hd-ready.mp4',
  'mixkit-man-with-his-dog-watching-the-sunset-on-the-horizon-4839-hd-ready.mp4',
  'mixkit-dog-sitting-on-log-1550-hd-ready.mp4',
  'mixkit-dog-catches-a-ball-in-a-river-1494-hd-ready.mp4',
  'mixkit-dog-walking-with-its-owner-in-a-park-1476-hd-ready.mp4'
];

const backgroundSourcesDir = path.join(__dirname, '..', 'background_sources');

// Ensure directory exists
if (!fs.existsSync(backgroundSourcesDir)) {
  fs.mkdirSync(backgroundSourcesDir, { recursive: true });
}

console.log('📁 Creating placeholder files for 9 Mixkit dog videos...\n');

videos.forEach((filename, index) => {
  const filePath = path.join(backgroundSourcesDir, filename);
  const placeholderContent = `# Placeholder for ${filename}
# Replace this file with the actual video file
# This file will be served at: https://your-domain.com/backgrounds/${filename}`;
  
  fs.writeFileSync(filePath, placeholderContent);
  console.log(`✅ Created placeholder ${index + 1}/9: ${filename}`);
});

console.log('\n🎉 Placeholder files created!');
console.log('📁 Files created in: background_sources/');
console.log('\n💡 Instructions:');
console.log('1. Replace each placeholder file with the actual video file');
console.log('2. Run "node scripts/setupBackgrounds.js" to make them publicly accessible');
console.log('3. Your videos will be available at: https://your-domain.com/backgrounds/filename.mp4');
