# 🔧 WattWise AI - Deployment Troubleshooting Guide

## Issue: "Internal Server Error" After 4 Days

### What Happened?
Your app was working fine initially, but after 4 days of inactivity, you're seeing an "Internal Server Error" when trying to register.

### Why This Happens on Render Free Tier:
1. **Service Spin Down**: Free tier services spin down after 15 minutes of inactivity
2. **Database Issues**: PostgreSQL database may lose connection or tables may not be recreated
3. **Cold Start Problems**: Service may not initialize properly when waking up

---

## 🚨 Immediate Actions

### Step 1: Check Render Logs (MOST IMPORTANT!)

1. Go to **https://dashboard.render.com/**
2. Click on your **wattwise-ai-1** service
3. Click on the **"Logs"** tab
4. Look for error messages (search for "ERROR" or "Exception")

**Common errors you might see:**

#### Error A: Database Table Missing
```
sqlalchemy.exc.OperationalError: (psycopg2.errors.UndefinedTable) 
relation "user" does not exist
```

**Solution:** Database tables weren't created. See Step 2 below.

#### Error B: Database Connection Failed
```
sqlalchemy.exc.OperationalError: could not connect to server
```

**Solution:** Database connection issue. Check DATABASE_URL environment variable.

#### Error C: Missing Environment Variables
```
KeyError: 'SECRET_KEY'
```

**Solution:** Environment variables not set. Check Render environment settings.

---

### Step 2: Verify Environment Variables

1. In Render Dashboard → **wattwise-ai-1** → **Environment** tab
2. Verify these variables exist:
   - ✅ `SECRET_KEY` (should be auto-generated)
   - ✅ `DATABASE_URL` (should be auto-populated from database)
   - ✅ `FLASK_DEBUG` = `false`
   - ✅ `GEMINI_API_KEY` (your API key)

**If any are missing:**
- Click **"Add Environment Variable"**
- Add the missing variable
- Click **"Save Changes"**
- Service will automatically redeploy

---

### Step 3: Check Database Connection

1. In Render Dashboard → **Databases** section
2. Find **wattwise-db**
3. Check status: Should be **"Available"** (green)

**If database is suspended or unavailable:**
- Free tier databases may be deleted after inactivity
- You may need to create a new database
- Update `DATABASE_URL` in your web service

---

### Step 4: Manual Redeploy

1. In Render Dashboard → **wattwise-ai-1**
2. Click **"Manual Deploy"** button (top right)
3. Select **"Deploy latest commit"**
4. Wait for deployment to complete (2-5 minutes)
5. Check logs for any errors

---

## 🔍 What I Fixed in the Latest Update

I just pushed fixes that will help diagnose and prevent this issue:

### 1. Enhanced Logging
- ✅ Detailed startup logs showing each initialization step
- ✅ Error logging with specific error messages
- ✅ Database table verification on startup

**You'll now see logs like:**
```
🚀 Starting WattWise AI
📊 Database: postgresql://...
✅ Extensions initialized successfully
✅ Upload folder created: uploads
✅ Blueprints registered successfully
🔧 Creating database tables...
✅ Database tables created: user, energy_data, energy_insight, ai_recommendation
🎉 WattWise AI initialized successfully
```

### 2. Better Error Handling
- ✅ Custom 500 error page (user-friendly)
- ✅ Custom 404 error page
- ✅ Try-catch blocks around critical operations
- ✅ Database session rollback on errors

### 3. Database Initialization Script
- ✅ Created `init_db.py` for manual database setup
- ✅ Automatic table creation with verification
- ✅ Better error messages if tables can't be created

---

## 🛠️ Manual Database Fix (If Needed)

If the database tables are missing, you can manually create them:

### Option A: Via Render Shell (Recommended)

1. In Render Dashboard → **wattwise-ai-1**
2. Click **"Shell"** tab
3. Run these commands:
```bash
python init_db.py
```

This will create all necessary database tables.

### Option B: Via Local Connection

1. Get your DATABASE_URL from Render environment variables
2. On your local machine:
```bash
# Set the database URL
export DATABASE_URL="postgresql://..."  # Copy from Render

# Run initialization
python init_db.py
```

---

## 🎯 Testing After Fix

### 1. Wait for Deployment
After pushing the fix, wait for Render to redeploy (you'll see this in the Events tab).

### 2. Check New Logs
Look for the new emoji-based logs:
- 🚀 Starting WattWise AI
- ✅ Extensions initialized
- ✅ Database tables created

### 3. Test Registration
1. Go to **https://wattwise-ai-1.onrender.com**
2. Click **"Register"**
3. Fill in the form
4. Submit

**If it still fails:**
- Copy the FULL error from Render logs
- Send it to me for further diagnosis

---

## 🚀 Preventing Future Issues

### 1. Keep Service Alive
Free tier services spin down after 15 minutes of inactivity. To keep it alive:

**Option A: Use a Ping Service**
- Use **UptimeRobot** (free): https://uptimerobot.com/
- Add your URL: `https://wattwise-ai-1.onrender.com`
- Set ping interval: Every 5 minutes

**Option B: Upgrade to Paid Plan**
- Render's paid plans don't spin down
- Starting at $7/month

### 2. Database Backups
- Render free tier databases are NOT backed up
- Consider upgrading database to paid tier ($7/month) for backups
- Or export data regularly

### 3. Monitor Your App
- Set up UptimeRobot to get alerts when your app goes down
- Check Render dashboard weekly for any issues

---

## 📊 Current Status

After the latest push:
- ✅ Enhanced error handling deployed
- ✅ Better logging enabled
- ✅ Database initialization improved
- ✅ Custom error pages created

**Next Steps:**
1. Wait for Render to finish deploying (check Events tab)
2. Check the new logs for detailed startup information
3. Test registration again
4. If it still fails, check logs and send me the error

---

## 🆘 Quick Reference

### Render Dashboard URLs
- **Main Dashboard**: https://dashboard.render.com/
- **Your Service**: https://dashboard.render.com/ → wattwise-ai-1
- **Logs**: Service → Logs tab
- **Environment**: Service → Environment tab
- **Shell**: Service → Shell tab

### Important Files
- `app/__init__.py` - Main app initialization (now with logging)
- `init_db.py` - Manual database setup script
- `app/templates/errors/500.html` - Custom error page
- `render.yaml` - Deployment configuration

### Useful Commands
```bash
# Check logs locally
python run.py

# Initialize database manually
python init_db.py

# Test locally
python run.py
# Then visit http://localhost:5000
```

---

## 📞 Still Having Issues?

If the problem persists after following this guide:

1. **Collect Information:**
   - Full error message from Render logs
   - Screenshot of the error page
   - Time when the error occurred

2. **Check These:**
   - [ ] Database status (Available?)
   - [ ] Environment variables (All set?)
   - [ ] Latest deployment (Successful?)
   - [ ] Logs (Any errors?)

3. **Send Me:**
   - The full error from logs
   - What you tried from this guide
   - Any other relevant details

---

**Last Updated:** February 13, 2026
**Status:** Fixes deployed, waiting for Render to redeploy
