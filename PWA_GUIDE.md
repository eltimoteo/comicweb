# ComicDB PWA Deployment Guide

## What's Been Added

Your ComicDB tracker has been converted into a **Progressive Web App (PWA)**! This means:

✅ **Installable on phones & tablets** - Users can add it to their home screen
✅ **Offline support** - Works without internet (after first load)
✅ **Fast loading** - Cached assets load instantly
✅ **App-like experience** - Runs in standalone mode without browser UI

## Files Created

1. **manifest.json** - PWA configuration (name, icons, theme colors)
2. **sw.js** - Service worker for offline caching
3. **icon-192.png** - App icon (192x192)
4. **icon-512.png** - App icon (512x512)

## Testing Locally

### Option 1: Using Python's HTTP Server
```bash
cd /Users/timothyhuang/Desktop/comicweb
python3 -m http.server 8000
```
Then visit: http://localhost:8000

### Option 2: Using npx serve
```bash
cd /Users/timothyhuang/Desktop/comicweb
npx serve -p 8000
```

## Installing on Mobile

### iOS (iPhone/iPad)
1. Open the website in Safari
2. Tap the Share button (square with arrow)
3. Scroll down and tap "Add to Home Screen"
4. Tap "Add" in the top right
5. The ComicDB icon will appear on your home screen!

### Android
1. Open the website in Chrome
2. Tap the menu (three dots)
3. Tap "Add to Home Screen" or "Install app"
4. Tap "Install" in the popup
5. The ComicDB icon will appear on your home screen!

## Deployment Options

### GitHub Pages (Free)
1. Create a new GitHub repository
2. Push all files to the repository
3. Go to Settings → Pages
4. Select "main" branch as source
5. Your PWA will be live at: `https://yourusername.github.io/comicweb`

### Netlify (Free)
1. Go to https://netlify.com
2. Drag and drop the `comicweb` folder
3. Your PWA will be live instantly!

### Vercel (Free)
1. Install Vercel CLI: `npm i -g vercel`
2. Run: `cd /Users/timothyhuang/Desktop/comicweb && vercel`
3. Follow the prompts
4. Your PWA will be deployed!

## Important Notes

⚠️ **HTTPS Required**: PWAs only work on HTTPS (or localhost). All deployment platforms above provide HTTPS automatically.

⚠️ **Service Worker Caching**: After updating your site, users may need to close and reopen the app to see changes. The service worker version is set to `v2.6.1` in `sw.js`.

## Updating the Cache

When you make changes to the site, update the cache version in `sw.js`:
```javascript
const CACHE_NAME = 'comicdb-v2.6.2'; // Increment this
```

This forces all devices to download fresh assets.

## Features

- 📱 **Mobile Responsive** - Already works great on phones
- 🌐 **Offline Mode** - Service worker caches pages and assets
- 🎨 **VSCode Theme** - Maintained across all platforms
- 📊 **Live Data** - Still pulls from Google Sheets when online
- ⚡ **Fast** - Cached resources load instantly

Enjoy your installable comic tracker! 🚀
