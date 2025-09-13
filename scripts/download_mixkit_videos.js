// Download Mixkit dog videos for background use
const https = require('https');
const fs = require('fs');
const path = require('path');

const videos = [
  {
    filename: 'mixkit-playfull-border-collie-dog-playing-with-a-toy-ball-50688-hd-ready.mp4',
    url: 'https://assets.mixkit.co/videos/preview/mixkit-playfull-border-collie-dog-playing-with-a-toy-ball-50688-hd-ready.mp4'
  },
  {
    filename: 'mixkit-a-young-pitbull-dog-bitting-and-playing-with-a-teddy-50676-hd-ready.mp4',
    url: 'https://assets.mixkit.co/videos/preview/mixkit-a-young-pitbull-dog-bitting-and-playing-with-a-teddy-50676-hd-ready.mp4'
  },
  {
    filename: 'mixkit-dog-tied-to-his-leash-on-the-street-19543-hd-ready.mp4',
    url: 'https://assets.mixkit.co/videos/preview/mixkit-dog-tied-to-his-leash-on-the-street-19543-hd-ready.mp4'
  },
  {
    filename: 'mixkit-husky-sled-dogs-pulling-in-slow-motion-7361-hd-ready.mp4',
    url: 'https://assets.mixkit.co/videos/preview/mixkit-husky-sled-dogs-pulling-in-slow-motion-7361-hd-ready.mp4'
  },
  {
    filename: 'mixkit-a-dog-resting-on-the-grass-next-to-a-dog-1479-hd-ready.mp4',
    url: 'https://assets.mixkit.co/videos/preview/mixkit-a-dog-resting-on-the-grass-next-to-a-dog-1479-hd-ready.mp4'
  },
  {
    filename: 'mixkit-man-with-his-dog-watching-the-sunset-on-the-horizon-4839-hd-ready.mp4',
    url: 'https://assets.mixkit.co/videos/preview/mixkit-man-with-his-dog-watching-the-sunset-on-the-horizon-4839-hd-ready.mp4'
  },
  {
    filename: 'mixkit-dog-sitting-on-log-1550-hd-ready.mp4',
    url: 'https://assets.mixkit.co/videos/preview/mixkit-dog-sitting-on-log-1550-hd-ready.mp4'
  },
  {
    filename: 'mixkit-dog-catches-a-ball-in-a-river-1494-hd-ready.mp4',
    url: 'https://assets.mixkit.co/videos/preview/mixkit-dog-catches-a-ball-in-a-river-1494-hd-ready.mp4'
  },
  {
    filename: 'mixkit-dog-walking-with-its-owner-in-a-park-1476-hd-ready.mp4',
    url: 'https://assets.mixkit.co/videos/preview/mixkit-dog-walking-with-its-owner-in-a-park-1476-hd-ready.mp4'
  }
];

const backgroundSourcesDir = path.join(__dirname, '..', 'background_sources');

// Ensure directory exists
if (!fs.existsSync(backgroundSourcesDir)) {
  fs.mkdirSync(backgroundSourcesDir, { recursive: true });
}

function downloadVideo(video, index) {
  return new Promise((resolve, reject) => {
    const filePath = path.join(backgroundSourcesDir, video.filename);
    const file = fs.createWriteStream(filePath);
    
    console.log(`📥 Downloading ${index + 1}/9: ${video.filename}`);
    
    https.get(video.url, (response) => {
      if (response.statusCode === 200) {
        response.pipe(file);
        file.on('finish', () => {
          file.close();
          console.log(`✅ Downloaded: ${video.filename}`);
          resolve();
        });
      } else {
        console.log(`❌ Failed to download: ${video.filename} (Status: ${response.statusCode})`);
        reject(new Error(`HTTP ${response.statusCode}`));
      }
    }).on('error', (err) => {
      console.log(`❌ Error downloading ${video.filename}: ${err.message}`);
      reject(err);
    });
  });
}

async function downloadAllVideos() {
  console.log('🚀 Starting download of 9 Mixkit dog videos...\n');
  
  for (let i = 0; i < videos.length; i++) {
    try {
      await downloadVideo(videos[i], i);
    } catch (error) {
      console.log(`⚠️  Skipped ${videos[i].filename} due to error`);
    }
  }
  
  console.log('\n🎉 Download complete!');
  console.log('📁 Videos saved to: background_sources/');
  console.log('\n💡 Next step: Run "node scripts/setupBackgrounds.js" to make them publicly accessible');
}

downloadAllVideos().catch(console.error);
