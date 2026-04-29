# Deploy AskSQL (Free Demo)

Deploy to **Render** (backend + frontend) + **TiDB Cloud** (free MySQL).

## Step 1: Create TiDB Cloud Database (5 min)

1. Go to [tidbcloud.com](https://tidbcloud.com) and sign up (free)
2. Click **Create Cluster** → Select **Serverless** (free tier)
3. Choose a region close to you
4. Wait for cluster to be ready (~2 min)
5. Click **Connect** → **General** → Note these values:
   - Host: `gateway01.us-east-1.prod.aws.tidbcloud.com` (yours will differ)
   - Port: `4000`
   - User: your username
   - Password: click "Generate Password"
6. Create a database:
   - Click **SQL Editor** in TiDB console
   - Run: `CREATE DATABASE asksql_demo;`

### Import Sample Data

In TiDB SQL Editor, run the contents of `scripts/setup_sample_db.sql` (copy-paste and execute).

## Step 2: Push to GitHub

```bash
# Initialize git if needed
git init
git add .
git commit -m "Initial commit"

# Push to GitHub
gh repo create asksql --public --push --source=.
# Or push to existing repo
```

## Step 3: Deploy to Render (5 min)

### Option A: One-Click Deploy (Recommended)

1. Go to [render.com](https://render.com) and sign up (free)
2. Click **New** → **Blueprint**
3. Connect your GitHub repo
4. Render will detect `render.yaml` and create both services
5. Add environment variables when prompted:

| Variable | Value |
|----------|-------|
| `GOOGLE_API_KEY` | Your Gemini API key |
| `MYSQL_HOST` | TiDB host (e.g., `gateway01.us-east-1.prod.aws.tidbcloud.com`) |
| `MYSQL_PORT` | `4000` |
| `MYSQL_USER` | Your TiDB username |
| `MYSQL_PASSWORD` | Your TiDB password |
| `MYSQL_DATABASE` | `asksql_demo` |

6. Click **Apply** and wait for deploy (~5 min)

### Option B: Manual Deploy

**Backend:**
1. New → Web Service → Connect repo
2. Name: `asksql-api`
3. Runtime: Docker
4. Dockerfile Path: `./backend/Dockerfile`
5. Plan: Free
6. Add environment variables (same as above)

**Frontend:**
1. New → Static Site → Connect repo
2. Name: `asksql-frontend`
3. Build Command: `cd frontend && npm install && npm run build`
4. Publish Directory: `frontend/dist`
5. Add rewrite rule: `/api/*` → `https://asksql-api.onrender.com/api/*`

## Step 4: Initialize the App

1. Open your frontend URL: `https://asksql-frontend.onrender.com`
2. Click **"Re-index Schemas"** to index your database tables
3. Start asking questions!

## Troubleshooting

### Cold Starts
Free tier services sleep after 15 min of inactivity. First request takes ~30-50 seconds to wake up.

### CORS Errors
Update `backend/app/main.py` with your actual Render URLs in `allow_origins`.

### TiDB Connection Issues
- Ensure your password doesn't have special characters that need escaping
- TiDB uses port `4000`, not `3306`
- Enable **Allow connections from anywhere** in TiDB security settings

### Check Logs
- Render Dashboard → Your Service → Logs

## URLs After Deploy

- **Frontend**: `https://asksql-frontend.onrender.com`
- **Backend API**: `https://asksql-api.onrender.com`
- **Health Check**: `https://asksql-api.onrender.com/api/health`

## Costs

| Service | Cost |
|---------|------|
| Render (backend) | Free (750 hrs/month) |
| Render (frontend) | Free (100 GB/month) |
| TiDB Cloud | Free (5 GB, 50M requests) |
| **Total** | **$0/month** |
