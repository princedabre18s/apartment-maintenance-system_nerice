# 🚀 Deployment Guide - Render + Netlify

## Overview

- **Backend**: Render.com (FastAPI + PostgreSQL)
- **Frontend**: Netlify (React + Vite)
- **Database**: NEON PostgreSQL (Already set up)

---

## 📋 Backend Deployment on Render

### Step 1: Push Configuration to GitHub

```bash
cd "c:\Users\prInce dabre\Downloads\18s projects\nerice noob\MongoDB\apartment-maintenance-system"
git add .
git commit -m "Add deployment configuration for Render and Netlify"
git push origin main
```

### Step 2: Deploy on Render

1. **Go to**: https://render.com
2. **Sign up/Login** with GitHub
3. **Click**: "New +" → "Web Service"
4. **Connect Repository**: Select `apartment-maintenance-system_nerice`
5. **Configure Service**:
   - **Name**: `apartment-maintenance-backend`
   - **Region**: Oregon (US West) or closest to you
   - **Branch**: `main`
   - **Root Directory**: Leave empty (render.yaml handles this)
   - **Environment**: Python 3
   - **Build Command**: 
     ```bash
     cd backend && pip install -r requirements.txt
     ```
   - **Start Command**: 
     ```bash
     cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
     ```
   - **Plan**: Free

6. **Add Environment Variables** (Click "Advanced" → "Add Environment Variable"):

   ```
   PG_HOST=ep-broad-resonance-ade3fcco-pooler.c-2.us-east-1.aws.neon.tech
   PG_DATABASE=neondb
   PG_USER=neondb_owner
   PG_PASSWORD=npg_SkIJU01uZvKo
   PG_SSLMODE=require
   PG_PORT=5432
   SECRET_KEY=your-secret-key-change-this-in-production-min-32-chars
   API_HOST=0.0.0.0
   ENVIRONMENT=production
   ```

7. **Click**: "Create Web Service"
8. **Wait**: 5-10 minutes for deployment
9. **Copy URL**: `https://apartment-maintenance-backend.onrender.com`

### ⚠️ Important Notes:

- Free tier: App sleeps after 15 min of inactivity (takes 30-60s to wake up)
- Database credentials are from your NEON account
- Backend URL will be: `https://apartment-maintenance-backend.onrender.com`

---

## 🌐 Frontend Deployment on Netlify

### Step 1: Update netlify.toml with Your Backend URL

After backend is deployed, update `netlify.toml`:

```toml
[context.production]
  environment = { VITE_API_URL = "https://YOUR-BACKEND-URL.onrender.com" }
```

Replace `YOUR-BACKEND-URL` with your actual Render backend URL.

### Step 2: Push to GitHub

```bash
git add netlify.toml
git commit -m "Update backend URL for production"
git push origin main
```

### Step 3: Deploy on Netlify

1. **Go to**: https://netlify.com
2. **Sign up/Login** with GitHub
3. **Click**: "Add new site" → "Import an existing project"
4. **Choose**: GitHub
5. **Select Repository**: `apartment-maintenance-system_nerice`
6. **Configure Build Settings**:
   - **Branch**: `main`
   - **Base directory**: `frontend`
   - **Build command**: `npm install && npm run build`
   - **Publish directory**: `frontend/dist`

7. **Environment Variables** (Site settings → Environment variables):
   ```
   VITE_API_URL=https://YOUR-BACKEND-URL.onrender.com
   ```

8. **Click**: "Deploy site"
9. **Wait**: 2-3 minutes for deployment
10. **Your site**: `https://random-name-123.netlify.app`

### Step 4: Custom Domain (Optional)

- Go to: Site settings → Domain management
- Click: "Add custom domain"
- Follow instructions to connect your domain

---

## 🔧 Post-Deployment Configuration

### Update Backend CORS Settings

After frontend is deployed, update backend to allow your Netlify domain:

1. Edit `backend/app/main.py`
2. Find CORS configuration:
   ```python
   app.add_middleware(
       CORSMiddleware,
       allow_origins=[
           "http://localhost:5173",
           "https://YOUR-NETLIFY-SITE.netlify.app"  # Add this
       ],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

3. Or use environment variable:
   ```python
   origins = [
       os.getenv("FRONTEND_URL", "http://localhost:5173"),
   ]
   ```

4. Add `FRONTEND_URL` to Render environment variables:
   ```
   FRONTEND_URL=https://YOUR-NETLIFY-SITE.netlify.app
   ```

---

## ✅ Verification Checklist

### Backend (Render):
- [ ] Service deployed successfully
- [ ] Health check passes: `https://your-backend.onrender.com/docs`
- [ ] Database connected (check logs)
- [ ] API endpoints working
- [ ] CORS configured for frontend domain

### Frontend (Netlify):
- [ ] Site deployed successfully
- [ ] Opens without errors
- [ ] API calls working (check browser console)
- [ ] Dashboard loads with data
- [ ] All pages accessible

---

## 🐛 Troubleshooting

### Backend Issues:

**Problem**: Build failed
- Check Python version (3.12+ required)
- Verify requirements.txt is correct
- Check Render build logs

**Problem**: Database connection error
- Verify environment variables are correct
- Check NEON database is accessible
- Test connection string locally

**Problem**: App crashes on startup
- Check start command is correct
- Verify `$PORT` is used (Render provides this)
- Check logs for errors

### Frontend Issues:

**Problem**: API calls failing
- Verify `VITE_API_URL` is set correctly
- Check backend CORS allows frontend domain
- Open browser console for errors

**Problem**: Build failed
- Check Node.js version (18+ required)
- Verify all dependencies in package.json
- Check Netlify build logs

**Problem**: 404 on page refresh
- Verify `netlify.toml` redirects are configured
- Check publish directory is `frontend/dist`

---

## 📊 Expected Costs

**Render (Backend):**
- Free tier: $0/month
- Limitations: 
  - Sleeps after 15 min inactivity
  - 750 hours/month free
  - 512 MB RAM

**Netlify (Frontend):**
- Free tier: $0/month
- Limitations:
  - 100 GB bandwidth/month
  - 300 build minutes/month
  - Unlimited sites

**NEON (Database):**
- Free tier: Already using
- 0.5 GB storage
- 10 hours compute/month

**Total Cost: $0/month** (using free tiers)

---

## 🚀 Going Live URLs

After deployment, you'll have:

- **Frontend**: `https://your-site.netlify.app`
- **Backend API**: `https://apartment-maintenance-backend.onrender.com`
- **API Docs**: `https://apartment-maintenance-backend.onrender.com/docs`
- **Database**: NEON (already configured)

---

## 🔄 Future Updates

To update your deployed apps:

```bash
# Make changes to code
git add .
git commit -m "Your update message"
git push origin main
```

Both Render and Netlify will automatically redeploy on push to main branch!

---

## 📞 Support

**Render Documentation**: https://render.com/docs  
**Netlify Documentation**: https://docs.netlify.com  
**NEON Documentation**: https://neon.tech/docs

---

**Ready to deploy!** 🎉

Start with Step 1 above to push your deployment configuration to GitHub.
