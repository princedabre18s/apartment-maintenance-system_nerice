# 🚀 Quick Deployment Checklist

## ✅ Step 1: Deploy Backend on Render (10 minutes)

### 1.1 Go to Render
Visit: https://render.com and sign up/login with GitHub

### 1.2 Create New Web Service
- Click "New +" → "Web Service"
- Connect repository: `apartment-maintenance-system_nerice`
- Click "Connect"

### 1.3 Configure Service
Fill in these settings:

**Basic Settings:**
```
Name: apartment-maintenance-backend
Region: Oregon (US West)
Branch: main
Root Directory: (leave empty)
Environment: Python 3
```

**Build Settings:**
```
Build Command: cd backend && pip install -r requirements.txt
Start Command: cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

**Instance Type:**
```
Free
```

### 1.4 Add Environment Variables
Click "Advanced" → Add these environment variables:

```
PG_HOST=ep-broad-resonance-ade3fcco-pooler.c-2.us-east-1.aws.neon.tech
PG_DATABASE=neondb
PG_USER=neondb_owner
PG_PASSWORD=npg_SkIJU01uZvKo
PG_SSLMODE=require
PG_PORT=5432
SECRET_KEY=change-this-to-a-very-long-random-string-min-32-chars
API_HOST=0.0.0.0
ENVIRONMENT=production
FRONTEND_URL=http://localhost:5173
```

(We'll update FRONTEND_URL later with your Netlify URL)

### 1.5 Deploy
- Click "Create Web Service"
- Wait 5-10 minutes for deployment
- **COPY YOUR BACKEND URL**: `https://apartment-maintenance-backend.onrender.com`
- Test it: Visit `https://your-backend-url.onrender.com/docs`

---

## ✅ Step 2: Deploy Frontend on Netlify (5 minutes)

### 2.1 Go to Netlify
Visit: https://netlify.com and sign up/login with GitHub

### 2.2 Create New Site
- Click "Add new site" → "Import an existing project"
- Choose "GitHub"
- Select repository: `apartment-maintenance-system_nerice`
- Click "Deploy"

### 2.3 Configure Build Settings

**Build settings:**
```
Base directory: frontend
Build command: npm install && npm run build
Publish directory: frontend/dist
```

### 2.4 Add Environment Variable
- Go to: Site settings → Environment variables → Add a variable
```
Key: VITE_API_URL
Value: https://YOUR-RENDER-BACKEND-URL.onrender.com
```
(Use the URL you copied from Render in Step 1.5)

### 2.5 Deploy
- Click "Deploy site"
- Wait 2-3 minutes
- **COPY YOUR FRONTEND URL**: `https://random-name.netlify.app`

---

## ✅ Step 3: Connect Frontend and Backend (5 minutes)

### 3.1 Update Backend CORS
Go back to Render:
- Open your backend service
- Go to "Environment"
- Update `FRONTEND_URL` variable:
```
FRONTEND_URL=https://your-netlify-site.netlify.app
```
(Use the URL you copied from Netlify in Step 2.5)

- Click "Save Changes"
- Backend will automatically redeploy (2-3 minutes)

### 3.2 Update Netlify Configuration (Optional)
This ensures future deployments use correct backend URL:

1. Edit `netlify.toml` on your computer:
```toml
[context.production]
  environment = { VITE_API_URL = "https://your-render-backend.onrender.com" }
```

2. Push to GitHub:
```bash
git add netlify.toml
git commit -m "Update production backend URL"
git push origin main
```

---

## ✅ Step 4: Test Your Deployment

### 4.1 Test Backend
Visit: `https://your-backend.onrender.com/docs`
- Should see API documentation
- Try a GET request to `/health` - should return `{"status":"healthy"}`

### 4.2 Test Frontend
Visit: `https://your-site.netlify.app`
- Dashboard should load
- Check browser console (F12) - no errors
- Navigate to Buildings, Units, Tenants pages
- Verify data loads correctly

---

## 🎉 You're Live!

Your application is now hosted and accessible worldwide!

**URLs:**
- Frontend: `https://your-site.netlify.app`
- Backend API: `https://your-backend.onrender.com`
- API Docs: `https://your-backend.onrender.com/docs`

---

## 🔄 Future Updates

To update your deployed application:

```bash
# Make changes to your code
git add .
git commit -m "Your update description"
git push origin main
```

Both Render and Netlify will automatically redeploy!

---

## ⚠️ Important Notes

**Free Tier Limitations:**
- **Render**: Backend sleeps after 15 minutes of inactivity (takes 30-60s to wake up on first request)
- **Netlify**: 100GB bandwidth/month, 300 build minutes/month
- **NEON**: Database is already configured and working

**First Load May Be Slow:**
- If backend is asleep, first request takes 30-60 seconds
- Subsequent requests are fast
- Keep backend awake by pinging it every 10 minutes (optional)

---

## 🐛 Troubleshooting

**Problem: Backend build fails**
- Check Render logs for errors
- Verify Python version is 3.12
- Check requirements.txt has all packages

**Problem: Frontend can't connect to backend**
- Verify `VITE_API_URL` is set correctly in Netlify
- Check `FRONTEND_URL` is set correctly in Render
- Check browser console for CORS errors

**Problem: Database connection fails**
- Verify all PG_* environment variables are correct in Render
- Test database connection from local machine
- Check NEON database is active

---

**Need more help?** See `HOSTING_GUIDE.md` for detailed instructions!
