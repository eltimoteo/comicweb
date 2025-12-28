# GitHub Pages Deployment Fix

## What Was Fixed

✅ Changed `manifest.json` start_url from `/index.html` to `./` (relative path)
✅ Updated `sw.js` to dynamically detect the base path
✅ Changed service worker registration from `/sw.js` to `./sw.js`

These changes make the PWA work on **both**:
- Root domains: `yoursite.com`
- GitHub Pages subdirectories: `username.github.io/comicweb/`

## Verify GitHub Pages is Enabled

1. Go to your GitHub repository
2. Click **Settings**
3. Scroll to **Pages** in the left sidebar
4. Under **Source**, select:
   - Branch: `main` (or `master`)
   - Folder: `/ (root)`
5. Click **Save**
6. Wait 1-2 minutes for deployment
7. Your site should be at: `https://YOUR_USERNAME.github.io/REPO_NAME/`

## Clear the Cache on Mobile

After updating the files, you need to clear the old cached version:

### iOS
1. Delete the installed PWA from home screen
2. Open Safari
3. Go to Settings → Safari → Advanced → Website Data
4. Find your site and swipe left to delete
5. Visit the new URL and reinstall

### Android
1. Uninstall the PWA (long press → uninstall)
2. Open Chrome
3. Go to Settings → Privacy → Clear Browsing Data
4. Select "Cached images and files"
5. Visit the new URL and reinstall

## Test the Deployment

1. Visit your GitHub Pages URL in a browser
2. Open DevTools Console (F12)
3. Check for "ServiceWorker registered" message
4. Go to Application tab → Service Workers
5. Verify the service worker is active
6. Try the install prompt

## Common Issues

### Still seeing 404?
- **Check the URL**: Make sure you're using `https://username.github.io/repo-name/`
- **Wait a minute**: GitHub Pages takes 1-2 minutes to deploy
- **Check branch**: Ensure the correct branch is selected in Settings → Pages
- **Check files**: Ensure all files (index.html, sw.js, manifest.json, icons) are pushed

### Can't reinstall on phone?
- **Clear everything**: Settings → Safari/Chrome → Clear all data for the site
- **Force refresh**: On desktop, do Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)
- **New incognito tab**: Test in private/incognito mode first

### Service worker not registering?
- **HTTPS required**: GitHub Pages provides this automatically
- **Check console**: Look for error messages in DevTools
- **Try desktop first**: Easier to debug on desktop before mobile

## Redeployment Steps

After making these fixes:

```bash
cd /Users/timothyhuang/Desktop/comicweb
git add .
git commit -m "Fix PWA paths for GitHub Pages compatibility"
git push origin main
```

Wait 1-2 minutes, then test at your GitHub Pages URL.

## Alternative: Test Locally First

Before deploying, test the relative paths work locally:

```bash
# Stop current server (Ctrl+C)
# Start new server
python3 -m http.server 8080
```

Visit http://localhost:8080 and verify service worker registers correctly.

---

**Updated:** The paths are now relative and will work on any deployment platform! 🎉
