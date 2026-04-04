# 🎬 FlickHive — Movie Watch Site

Simple, fast, no-login movie streaming site built with Django.

---

## Quick Start

```bash
pip install -r requirements.txt
python manage.py migrate
python seed.py
python manage.py runserver
```

→ http://127.0.0.1:8000  
→ Admin: http://127.0.0.1:8000/admin/ (admin / admin123)

---

## Pages

| URL | Page |
|-----|------|
| `/` | Home |
| `/movies/` | All movies (search + filter) |
| `/movies/<slug>/` | Movie detail |
| `/watch/<slug>/` | Video player |
| `/categories/` | All genres |
| `/category/<slug>/` | Genre movies |
| `/about/` | About |
| `/contact/` | Contact form |

---

## 🖼️ Cloudinary Setup (Images)

### 1. Create a free account
→ https://cloudinary.com/users/register/free  
Free tier: **25 GB storage, 25 GB bandwidth/month** — plenty for posters.

### 2. Get your credentials
Dashboard → Settings → API Keys  
Copy: **Cloud Name**, **API Key**, **API Secret**

### 3. Set environment variables
Create a `.env` file (never commit this):
```
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=123456789012345
CLOUDINARY_API_SECRET=your_api_secret_here
OG_DEFAULT_IMAGE=https://res.cloudinary.com/your_cloud_name/image/upload/v1/flickhive-og.jpg
SITE_URL=https://yoursite.com
```

Load it before running:
```bash
export $(cat .env | xargs)
python manage.py runserver
```

Or use `python-dotenv` (see below).

### 4. Upload your OG default image
- Go to Cloudinary Media Library
- Upload a 1200×630px image called `flickhive-og`
- Copy its URL → paste into `.env` as `OG_DEFAULT_IMAGE`

### 5. How it works
When you upload a poster in Django Admin → it automatically goes to Cloudinary.  
The URL returned is used in `<img>` tags and OG meta tags throughout the site.

---

## 🎥 Free Video Streaming Options

> FlickHive uses **iframe embeds** — no video is stored on your server.

### Option A: YouTube (easiest, but ads)
1. Upload your video to YouTube (set to Public or Unlisted)
2. Copy the embed URL: `https://www.youtube.com/embed/VIDEO_ID`
3. Paste into **Video Embed URL** in Admin

✅ Free, reliable, global CDN  
⚠️ YouTube ads may show; YouTube can remove content

### Option B: Vimeo (no ads on basic)
1. Create free account → https://vimeo.com
2. Upload video (free: 5GB storage)
3. Embed URL: `https://player.vimeo.com/video/VIDEO_ID`
4. In Vimeo settings → **Privacy** → "Only on sites I choose" → add your domain ✅

✅ No ads, domain-lock available  
⚠️ Free tier: 5 GB total

### Option C: Bunny.net Stream ⭐ Recommended
Best balance of free/cheap + security:
1. Sign up → https://bunny.net (pay-as-you-go, ~$0.005/GB served)
2. Create a Stream Library
3. Upload videos
4. Enable **DRM** (Widevine + FairPlay) in library settings
5. Enable **Domain Restriction** → add your domain only
6. Embed URL: `https://iframe.mediadelivery.net/embed/LIBRARY_ID/VIDEO_ID`

✅ Domain-locked, DRM-protected, no ads, fast CDN  
💰 ~$0.005/GB — 100GB = $0.50 (extremely cheap)

### Option D: Cloudflare Stream
1. → https://dash.cloudflare.com → Stream
2. Upload video
3. Enable **Signed URLs** (blocks direct access)
4. Embed: `https://iframe.cloudflarestream.com/VIDEO_ID`

✅ Very secure, signed tokens  
💰 $5/month base + $1 per 1000 minutes

### Option E: Archive.org (public domain films only)
1. → https://archive.org/upload
2. Upload Public Domain films
3. Get embed URL from the "Embed" button

✅ Completely free, no limits for public domain  
⚠️ Public domain only (pre-1928 films, Creative Commons)

---

## 🔒 Video Security — What's Protected & What's Not

### ✅ What FlickHive blocks:
| Attack | Protection |
|--------|-----------|
| Right-click → Save | `oncontextmenu=false` on player page |
| Ctrl+S / Cmd+S | Keyboard event listener |
| Ctrl+P (print) | `beforeprint` event blocked |
| Browser cache save | `Cache-Control: no-store` on `/watch/` |
| Direct video URL loading | `media-src 'none'` in CSP |
| Embedding our site elsewhere | `X-Frame-Options: DENY` |
| Long-press save (mobile) | Transparent guard layer over iframe |
| MIME sniffing | `X-Content-Type-Options: nosniff` |

### ⚠️ What can't be fully blocked (client-side limits):
| Attack | Real Solution |
|--------|--------------|
| Screen recording | **Bunny.net / Cloudflare DRM** (Widevine blocks capture on desktop) |
| Screenshot | OS-level, only DRM helps |
| Browser extensions | DRM only |
| DevTools → Network tab → video URL | **Signed/expiring tokens** (Bunny.net / Cloudflare) |

### 🛡️ Maximum security setup:
Use **Bunny.net** with:
- Domain restriction (only your domain can load the player)
- Signed embed tokens (URLs expire after X minutes)
- DRM enabled (Widevine blocks screen recording on Chrome/Firefox)

---

## 🚀 Deployment Guide

### Option A: Railway (recommended — free tier available)
```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login and deploy
railway login
railway init
railway up

# 3. Set environment variables in Railway dashboard:
#    SECRET_KEY, DEBUG=False, ALLOWED_HOSTS=yoursite.railway.app
#    CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET
#    OG_DEFAULT_IMAGE, SITE_URL
```

### Option B: Render (free tier)
1. Push to GitHub
2. → https://render.com → New Web Service → connect repo
3. Build command: `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput`
4. Start command: `gunicorn config.wsgi`
5. Add env vars in Render dashboard

### Option C: PythonAnywhere (free)
1. → https://www.pythonanywhere.com
2. Upload your project
3. Configure WSGI to point to `config.wsgi`
4. Set env vars in the web app config

### Pre-deploy checklist:
```bash
# 1. Collect static files
python manage.py collectstatic

# 2. Set in environment:
DEBUG=False
SECRET_KEY=<generate a real one: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())">
ALLOWED_HOSTS=yourdomain.com

# 3. Add to requirements.txt if using PostgreSQL:
# psycopg2-binary

# 4. Update DATABASES in settings.py for PostgreSQL:
# import dj_database_url
# DATABASES = {'default': dj_database_url.config()}
```

---

## Environment Variables Reference

| Variable | Required | Example |
|----------|----------|---------|
| `SECRET_KEY` | Yes (prod) | `django-abc123...` |
| `DEBUG` | No | `False` |
| `ALLOWED_HOSTS` | Yes (prod) | `flickhive.com,www.flickhive.com` |
| `SITE_URL` | Yes | `https://flickhive.com` |
| `CLOUDINARY_CLOUD_NAME` | Yes | `mycloud` |
| `CLOUDINARY_API_KEY` | Yes | `123456789` |
| `CLOUDINARY_API_SECRET` | Yes | `abc123xyz` |
| `OG_DEFAULT_IMAGE` | Yes | `https://res.cloudinary.com/...` |

---

## Adding Movies via Admin

1. Go to `/admin/` → Movies → Add Movie
2. Fill in all fields
3. **Poster** → upload image (auto-goes to Cloudinary)
4. **Video Embed URL** → paste embed URL from your video host
5. **OG Image URL** → leave blank (uses poster) or paste a specific Cloudinary URL
6. **Is Featured** → tick for one movie to show as homepage hero
7. Save ✅

---

## requirements.txt

```
django>=5.0
pillow>=10.0
cloudinary
django-cloudinary-storage
whitenoise
gunicorn
```
