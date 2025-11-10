# Deployment Guide
## Apartment Maintenance Request System

Complete guide for deploying your application to production.

---

## 🌐 Deployment Overview

We'll deploy:
- **Backend** → Render (or Railway)
- **Frontend** → Vercel (or Netlify)
- **Database** → MongoDB Atlas

Total cost: **$0** (using free tiers)

---

## 📊 Pre-Deployment Checklist

- [ ] Code tested locally
- [ ] Environment variables documented
- [ ] MongoDB Atlas cluster created
- [ ] Git repository created
- [ ] `.gitignore` properly configured
- [ ] No sensitive data in code

---

## 1️⃣ MongoDB Atlas Setup

### Create Production Database

1. Go to https://www.mongodb.com/cloud/atlas
2. Create **new cluster** or use existing
3. Click **"Connect"** → **"Connect your application"**
4. Copy connection string:
   ```
   mongodb+srv://<username>:<password>@<cluster>.mongodb.net/<database>?retryWrites=true&w=majority
   ```
5. Replace `<database>` with `apartment_maintenance`
6. Save this for backend deployment

### Configure Network Access

1. Go to **Network Access**
2. Click **"Add IP Address"**
3. Select **"Allow Access from Anywhere"** (`0.0.0.0/0`)
4. Or add specific IPs from Render/Railway

### Create Database User

1. Go to **Database Access**
2. Click **"Add New Database User"**
3. Set username: `prod_user`
4. Set strong password (save it!)
5. Set role: **Read and write to any database**

---

## 2️⃣ Backend Deployment to Render

### Step 1: Push Code to GitHub

```powershell
# Initialize git (if not already)
cd "apartment-maintenance-system"
git init
git add .
git commit -m "Initial commit - Apartment Maintenance System"

# Create GitHub repo and push
git remote add origin https://github.com/yourusername/apartment-maintenance-system.git
git branch -M main
git push -u origin main
```

### Step 2: Create Render Account

1. Go to https://render.com
2. Sign up with GitHub account
3. Authorize Render to access repositories

### Step 3: Create Web Service

1. Click **"New +"** → **"Web Service"**
2. Connect your repository
3. Configure:

**Basic Settings:**
- Name: `apartment-maintenance-api`
- Root Directory: `backend`
- Environment: `Python 3`
- Region: `Oregon (US West)` (or closest)
- Branch: `main`

**Build & Deploy:**
- Build Command: 
  ```bash
  pip install -r requirements.txt
  ```
- Start Command:
  ```bash
  uvicorn app.main:app --host 0.0.0.0 --port $PORT
  ```

### Step 4: Add Environment Variables

Click **"Environment"** and add:

```
MONGO_URI=mongodb+srv://prod_user:YOUR_PASSWORD@cluster0.xxxxx.mongodb.net/apartment_maintenance?retryWrites=true&w=majority
MONGO_DB_NAME=apartment_maintenance
SECRET_KEY=generate-a-secure-random-key-here-use-python-secrets
API_HOST=0.0.0.0
API_PORT=10000
FRONTEND_URL=https://your-app.vercel.app
ENVIRONMENT=production
```

**Generate SECRET_KEY:**
```python
import secrets
print(secrets.token_urlsafe(32))
```

### Step 5: Deploy

1. Click **"Create Web Service"**
2. Wait for build to complete (3-5 minutes)
3. Your API will be at: `https://apartment-maintenance-api.onrender.com`
4. Test: `https://apartment-maintenance-api.onrender.com/health`

---

## 3️⃣ Frontend Deployment to Vercel

### Step 1: Update API URL

Edit `frontend/.env.production`:
```env
VITE_API_URL=https://apartment-maintenance-api.onrender.com
```

Commit changes:
```powershell
git add frontend/.env.production
git commit -m "Add production API URL"
git push
```

### Step 2: Create Vercel Account

1. Go to https://vercel.com
2. Sign up with GitHub account
3. Import your repository

### Step 3: Configure Project

**Import Settings:**
- Framework Preset: **Vite**
- Root Directory: `frontend`
- Build Command: `npm run build`
- Output Directory: `dist`
- Install Command: `npm install`

**Environment Variables:**
```
VITE_API_URL=https://apartment-maintenance-api.onrender.com
```

### Step 4: Deploy

1. Click **"Deploy"**
2. Wait for build (2-3 minutes)
3. Your app will be at: `https://your-app.vercel.app`

### Step 5: Update CORS Settings

Go back to Render and update backend environment:
```
FRONTEND_URL=https://your-app.vercel.app
```

---

## 4️⃣ Seed Production Database

### Option A: From Local Machine

```powershell
cd scripts

python seed_data.py --mongo "YOUR_PRODUCTION_MONGO_URI"
```

### Option B: From Render Shell

1. Go to Render dashboard
2. Select your service
3. Click **"Shell"**
4. Run:
```bash
cd scripts
python seed_data.py --mongo "$MONGO_URI"
```

---

## 5️⃣ Alternative Platforms

### Railway (Alternative to Render)

1. Go to https://railway.app
2. Connect GitHub repo
3. Select `backend` directory
4. Add environment variables
5. Railway auto-detects Python and deploys

**Pros**: Faster deployments, better free tier
**Cons**: Credit card required (even for free tier)

### Netlify (Alternative to Vercel)

1. Go to https://netlify.com
2. Connect GitHub repo
3. Build settings:
   - Base directory: `frontend`
   - Build command: `npm run build`
   - Publish directory: `frontend/dist`
4. Add environment variables
5. Deploy

**Pros**: Great for static sites, easy rollbacks
**Cons**: Similar to Vercel

---

## 🔒 Security Best Practices

### 1. Environment Variables
- ✅ Never commit `.env` files
- ✅ Use different credentials for dev/prod
- ✅ Rotate secrets regularly
- ✅ Use strong passwords (16+ characters)

### 2. MongoDB Security
- ✅ Enable authentication
- ✅ Use least privilege access
- ✅ Regularly backup data
- ✅ Monitor access logs

### 3. API Security
- ✅ Enable CORS only for your frontend domain
- ✅ Use HTTPS only in production
- ✅ Implement rate limiting (future)
- ✅ Validate all inputs

### 4. Frontend Security
- ✅ Don't expose sensitive data
- ✅ Sanitize user inputs
- ✅ Use environment variables
- ✅ Enable CSP headers

---

## 📊 Monitoring & Maintenance

### Health Checks

**Backend Health:**
```bash
curl https://apartment-maintenance-api.onrender.com/health
```

**Expected Response:**
```json
{"status": "healthy"}
```

### Render Logs

View logs in Render dashboard:
1. Select your service
2. Click **"Logs"** tab
3. Monitor for errors

### Vercel Analytics

Enable analytics in Vercel:
1. Go to project settings
2. Click **"Analytics"**
3. View traffic and performance

---

## 🔄 Continuous Deployment

### Auto-Deploy on Git Push

Both Render and Vercel support automatic deployments:

```powershell
# Make changes
git add .
git commit -m "Update feature X"
git push

# Automatically triggers:
# 1. Backend rebuild on Render
# 2. Frontend rebuild on Vercel
```

### Branch Deployments

Create preview environments:

```powershell
# Create feature branch
git checkout -b feature/new-dashboard
git push -u origin feature/new-dashboard

# Vercel creates preview URL:
# https://your-app-git-feature-new-dashboard.vercel.app
```

---

## 💰 Cost Estimates

### Free Tier Limits

**MongoDB Atlas Free (M0):**
- Storage: 512 MB
- RAM: Shared
- Good for: ~10,000 documents
- Cost: $0

**Render Free:**
- 750 hours/month
- Sleeps after 15 min inactivity
- 100 GB bandwidth
- Cost: $0

**Vercel Free:**
- 100 GB bandwidth
- Unlimited requests
- 100 deployments/day
- Cost: $0

### When to Upgrade

Upgrade when you hit:
- MongoDB: >500MB data or need backups
- Render: Need 24/7 uptime or >750hrs
- Vercel: >100GB bandwidth

---

## 🚨 Troubleshooting

### Backend Not Responding
```bash
# Check logs on Render
# Common issues:
# 1. Wrong MONGO_URI
# 2. Missing environment variables
# 3. Build errors
```

### Frontend API Errors
```javascript
// Check browser console (F12)
// Common issues:
// 1. Wrong VITE_API_URL
// 2. CORS errors (check backend FRONTEND_URL)
// 3. Network issues
```

### Database Connection Issues
```bash
# Test MongoDB connection
mongosh "mongodb+srv://user:pass@cluster.mongodb.net"

# Check:
# 1. Credentials correct
# 2. IP whitelisted
# 3. Database user exists
```

---

## 📱 Custom Domain (Optional)

### Add Custom Domain to Vercel

1. Go to project **Settings**
2. Click **"Domains"**
3. Add your domain (e.g., `maintenance.yourdomain.com`)
4. Update DNS records as instructed
5. SSL auto-configured

### Add Custom Domain to Render

1. Go to service **Settings**
2. Click **"Custom Domains"**
3. Add your domain
4. Update DNS CNAME record
5. SSL auto-configured

---

## ✅ Post-Deployment Checklist

- [ ] Backend API responding at `/health`
- [ ] Frontend loads without errors
- [ ] Can create new request
- [ ] Dashboard shows metrics
- [ ] Data persists in MongoDB
- [ ] CORS working correctly
- [ ] All environment variables set
- [ ] Logs show no errors

---

## 🎉 Success!

Your application is now live!

**Share your deployment:**
- Backend API: `https://your-api.onrender.com`
- Frontend App: `https://your-app.vercel.app`

**Monitor regularly:**
- Check logs for errors
- Monitor MongoDB usage
- Review analytics
- Update dependencies

---

**Need Help?** 
- Render Support: https://render.com/docs
- Vercel Support: https://vercel.com/docs
- MongoDB Support: https://docs.mongodb.com/

**Project Contacts:**
- Email: nerodr@iu.edu, rdharani@iu.edu
- Course: PA55 - Applied Database Technologies

---

**Last Updated**: November 7, 2025
