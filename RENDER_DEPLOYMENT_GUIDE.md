# 🚀 Eco Pet Guide - Render Deployment Guide

## 🎯 Why Render Over Netlify?

Your affiliate site has complex backend requirements that make Render the perfect choice:

- ✅ **FastAPI Backend** - Dynamic API endpoints
- ✅ **Database Integration** - SQLite/PostgreSQL support  
- ✅ **Admin Portal** - Dynamic content generation
- ✅ **Affiliate Tracking** - Click tracking & analytics
- ✅ **Newsletter System** - Email subscriptions
- ✅ **Auto-scaling** - Handle TikTok traffic spikes

## 🛠️ Pre-Deployment Checklist

- [x] Site stats removed from footer
- [x] AI generated images excluded via .gitignore
- [x] render.yaml configuration created
- [x] Procfile for compatibility
- [x] Requirements.txt updated
- [x] Environment variables identified

## 🚀 Deployment Steps

### Step 1: Push to GitHub

```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### Step 2: Create Render Account

1. Go to [render.com](https://render.com)
2. Sign up with GitHub (recommended)
3. Authorize Render to access your repositories

### Step 3: Create Web Service

1. Click "New +" → "Web Service"
2. Connect your `affiliate` repository
3. Configure settings:

**Basic Settings:**
- **Name:** `eco-pet-guide`
- **Branch:** `main`
- **Runtime:** `Python 3`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn app:app --host 0.0.0.0 --port $PORT`

**Advanced Settings:**
- **Auto-Deploy:** Yes
- **Health Check Path:** `/`

### Step 4: Configure Environment Variables

In Render dashboard, add these environment variables:

**Required Variables:**
```
DATABASE_URL=postgresql://user:pass@host:port/dbname
ADMIN_TOKEN=your-secure-admin-token-here
```

**Optional Variables:**
```
GEMINI_API_KEY=your-gemini-api-key (for image generation)
```

### Step 5: Set Up Database

**Option A: Render PostgreSQL (Recommended)**
1. Create new PostgreSQL database in Render
2. Copy the DATABASE_URL to your web service environment variables

**Option B: External Database**
- Use your existing database URL
- Ensure it's accessible from Render's IP ranges

## 🌐 Domain Setup

### Custom Domain Configuration

1. In Render dashboard → Settings → Custom Domains
2. Add your domain: `ecopetguide.com`
3. Update your DNS records:
   ```
   Type: CNAME
   Name: @
   Value: eco-pet-guide.onrender.com
   ```

### SSL Certificate
- Render provides automatic SSL certificates
- No additional configuration needed

## 🔧 Post-Deployment Configuration

### 1. Test Your Deployment

Visit your Render URL to verify:
- [x] Homepage loads correctly
- [x] Articles display properly  
- [x] Admin portal accessible
- [x] Database connections work
- [x] Image uploads function

### 2. Update Admin Portal

Your admin portal will now work at:
`https://your-app.onrender.com/admin`

### 3. TikTok Link Updates

Update your TikTok bio link to:
`https://your-custom-domain.com` or `https://eco-pet-guide.onrender.com`

## 🎛️ Managing Your Deployment

### Automatic Deployments

- Every push to `main` branch triggers auto-deployment
- Check deployment logs in Render dashboard
- Typical deploy time: 2-5 minutes

### Manual Deployments

1. Go to Render dashboard
2. Select your service
3. Click "Manual Deploy" → "Deploy latest commit"

### Monitoring

- **Logs:** Available in real-time via dashboard
- **Metrics:** CPU, Memory, Response times
- **Health Checks:** Automatic monitoring

## 🚨 Troubleshooting

### Common Issues

**Port Binding Error:**
```bash
# If you see port binding errors, ensure start command is:
uvicorn app:app --host 0.0.0.0 --port $PORT
```

**Database Connection Issues:**
- Verify DATABASE_URL format
- Check database is accessible
- Ensure database exists and tables are created

**Static Files Not Loading:**
- Verify file paths in your app
- Check that images exist in repository
- Ensure proper CORS configuration

### Debug Commands

```bash
# Check environment variables
echo $DATABASE_URL

# Test database connection
python -c "from app import engine; print(engine)"

# Check port binding
echo $PORT
```

## 💰 Pricing

**Free Tier Limits:**
- 750 hours/month (enough for always-on)
- 512MB RAM
- Shared CPU
- Perfect for getting started

**Paid Plans Start at $7/month:**
- Dedicated resources
- Custom domains included
- Priority support

## 🎯 Next Steps After Deployment

1. **Test Everything:**
   - All article links work
   - Admin portal functions
   - Newsletter signups
   - Affiliate tracking

2. **Update TikTok:**
   - Change bio link to new domain
   - Test traffic flow from TikTok → Site

3. **Monitor Performance:**
   - Check response times
   - Monitor error rates
   - Watch resource usage

4. **Scale as Needed:**
   - Upgrade plan if traffic increases
   - Add custom domain
   - Optimize database queries

## 🔗 Important URLs

- **Production Site:** `https://eco-pet-guide.onrender.com`
- **Admin Portal:** `https://eco-pet-guide.onrender.com/admin`
- **API Docs:** `https://eco-pet-guide.onrender.com/docs`

## 🆘 Need Help?

- **Render Docs:** [render.com/docs](https://render.com/docs)
- **FastAPI Deployment:** [render.com/docs/deploy-fastapi](https://render.com/docs/deploy-fastapi)
- **Support:** Available via Render dashboard

---

**Ready to deploy? Follow the steps above and your eco-friendly pet guide will be live in minutes!** 🌱🐕 