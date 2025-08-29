# Web3.LOC - Live Streamlit App

## 🚀 Live Python Web App Deployment

This creates a live, web-accessible version of the Web3.LOC Python application using Streamlit Cloud.

### Quick Deploy Links:

**Streamlit Cloud:** https://share.streamlit.io/

**Railway:** https://railway.app/

**Render:** https://render.com/

**Heroku:** https://heroku.com/

### Files Ready for Live Deployment:

1. `streamlit_app.py` - Main app file (Streamlit Cloud looks for this)
2. `requirements.txt` - Dependencies 
3. `.env.example` - Environment variables template
4. `packages.txt` - System dependencies (if needed)

### How to Deploy Live:

#### Option 1: Streamlit Cloud (Easiest)
1. Go to https://share.streamlit.io/
2. Connect your GitHub account
3. Select repository: `nibertinvestments/Web3.LOC`
4. Main file path: `streamlit_app.py`
5. Click "Deploy"

#### Option 2: Railway
1. Go to https://railway.app/
2. "Deploy from GitHub repo"
3. Select `nibertinvestments/Web3.LOC`
4. Set start command: `streamlit run streamlit_app.py --server.port $PORT`

#### Option 3: Render
1. Go to https://render.com/
2. "New Web Service"
3. Connect GitHub repo
4. Build command: `pip install -r requirements.txt`
5. Start command: `streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0`

### Environment Variables Needed:
- `ETHERSCAN_API_KEY`
- `BASESCAN_API_KEY`
- `GITHUB_TOKEN` (optional)

Your live Python app will be accessible at a public URL!
