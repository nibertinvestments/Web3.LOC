# 🚀 Web3.LOC Live Deployment Guide

This guide will help you deploy Web3.LOC as a live application using GitHub storage backend.

## ✅ Prerequisites

1. **GitHub Account**: You'll need a GitHub account to store contracts remotely
2. **API Keys**: Etherscan and Basescan API keys for blockchain data
3. **Deployment Platform**: Choose from Streamlit Cloud, Heroku, or other platforms

## 🔧 Step 1: GitHub Setup

### Create Storage Repository

1. **Create a new GitHub repository** for storing contracts:
   ```
   Repository name: web3-loc-storage (or any name you prefer)
   Visibility: Public or Private (both work)
   ```

2. **Generate Personal Access Token**:
   - Go to GitHub Settings → Developer settings → Personal access tokens
   - Click "Generate new token (classic)"
   - Select scopes: `repo` (Full control of private repositories)
   - Copy the token securely (you won't see it again)

### Repository Structure
Your storage repository will automatically organize contracts like this:
```
web3-loc-storage/
├── contracts/
│   ├── ethereum/
│   │   ├── contract_0x123...abc.json
│   │   └── contract_0x456...def.json
│   └── base/
│       ├── contract_0x789...ghi.json
│       └── contract_0xabc...123.json
└── index/
    ├── contract_index.json
    └── chain_statistics.json
```

## 🔑 Step 2: API Keys Setup

### Etherscan API Key
1. Visit [etherscan.io/apis](https://etherscan.io/apis)
2. Create account if needed
3. Navigate to "API Keys" section
4. Create new API key
5. Copy the key

### Basescan API Key
1. Visit [basescan.org/apis](https://basescan.org/apis)
2. Create account if needed
3. Navigate to "API Keys" section
4. Create new API key
5. Copy the key

## ☁️ Step 3: Streamlit Cloud Deployment (Recommended)

### Setup

1. **Fork this repository** to your GitHub account

2. **Visit [share.streamlit.io](https://share.streamlit.io)**

3. **Create new app**:
   - Repository: `your-username/Web3.LOC`
   - Branch: `main`
   - Main file path: `web3_loc_gui.py`

4. **Configure environment variables** in Advanced settings:
   ```
   ETHERSCAN_API_KEY=your_etherscan_api_key_here
   BASESCAN_API_KEY=your_basescan_api_key_here
   GITHUB_TOKEN=your_github_personal_access_token
   GITHUB_REPO=your-username/web3-loc-storage
   ```

5. **Deploy**: Click "Deploy!" button

### Benefits of Streamlit Cloud
- ✅ Free hosting
- ✅ Automatic deployments from GitHub
- ✅ Easy environment variable management
- ✅ HTTPS by default
- ✅ Custom domains available

## 🐳 Step 4: Alternative - Docker Deployment

### Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run the application
CMD ["streamlit", "run", "web3_loc_gui.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Docker Compose
```yaml
version: '3.8'

services:
  web3-loc:
    build: .
    ports:
      - "8501:8501"
    environment:
      - ETHERSCAN_API_KEY=${ETHERSCAN_API_KEY}
      - BASESCAN_API_KEY=${BASESCAN_API_KEY}
      - GITHUB_TOKEN=${GITHUB_TOKEN}
      - GITHUB_REPO=${GITHUB_REPO}
    restart: unless-stopped
```

### Deploy with Docker
```bash
# Build and run
docker-compose up -d

# Or with direct docker run
docker build -t web3-loc .
docker run -d \
  -p 8501:8501 \
  -e ETHERSCAN_API_KEY=your_key \
  -e BASESCAN_API_KEY=your_key \
  -e GITHUB_TOKEN=your_token \
  -e GITHUB_REPO=your-username/web3-loc-storage \
  --name web3-loc \
  web3-loc
```

## 🌐 Step 5: Heroku Deployment

### Setup

1. **Install Heroku CLI** and login:
   ```bash
   heroku login
   ```

2. **Create Heroku app**:
   ```bash
   heroku create your-web3-loc-app
   ```

3. **Set environment variables**:
   ```bash
   heroku config:set ETHERSCAN_API_KEY=your_etherscan_key
   heroku config:set BASESCAN_API_KEY=your_basescan_key
   heroku config:set GITHUB_TOKEN=your_github_token
   heroku config:set GITHUB_REPO=your-username/web3-loc-storage
   ```

4. **Create Procfile**:
   ```
   web: sh setup.sh && streamlit run web3_loc_gui.py --server.port=$PORT --server.address=0.0.0.0
   ```

5. **Deploy**:
   ```bash
   git push heroku main
   ```

## 🔒 Step 6: Security Best Practices

### Environment Variables
- ❌ Never commit API keys or tokens to git
- ✅ Use environment variables for all secrets
- ✅ Rotate API keys regularly
- ✅ Use different keys for development and production

### GitHub Token Security
- ✅ Create tokens with minimal required permissions
- ✅ Set expiration dates on tokens
- ✅ Monitor token usage in GitHub settings
- ✅ Revoke unused or compromised tokens

### Repository Access
- ✅ Use private repositories for sensitive data
- ✅ Limit collaborator access
- ✅ Enable branch protection rules
- ✅ Monitor repository access logs

## 🧪 Step 7: Testing Your Deployment

### Functionality Tests

1. **Basic Functionality**:
   - ✅ Application loads without errors
   - ✅ Navigation between tabs works
   - ✅ Settings page shows GitHub status

2. **GitHub Integration**:
   - ✅ GitHub connection test passes
   - ✅ Repository statistics load
   - ✅ Remote search works

3. **Contract Discovery**:
   - ✅ Can input contract addresses
   - ✅ Contract data fetches successfully
   - ✅ Contracts save to GitHub storage

4. **Search Functionality**:
   - ✅ Local search works
   - ✅ Remote search returns results
   - ✅ Filtering works correctly

### Performance Tests
- Monitor response times for contract discovery
- Check GitHub API rate limits
- Verify large contract handling

## 📊 Step 8: Monitoring and Maintenance

### Application Monitoring
- Monitor application uptime
- Track GitHub API usage
- Monitor error rates and logs

### GitHub Storage Management
- Monitor repository size
- Archive old contracts if needed
- Backup repository regularly

### API Key Management
- Monitor API usage quotas
- Upgrade to paid plans if needed
- Rotate keys periodically

## 🆘 Troubleshooting

### Common Issues

**GitHub Authentication Failed**
```
Error: GitHub storage not configured
Solution: Verify GITHUB_TOKEN and GITHUB_REPO environment variables
```

**API Rate Limits Exceeded**
```
Error: Rate limit exceeded
Solution: Upgrade to paid API plans or implement request throttling
```

**Contract Not Found**
```
Error: Contract verification failed
Solution: Ensure contract is verified on blockchain explorer
```

**Streamlit Deployment Failed**
```
Error: Application failed to start
Solution: Check requirements.txt and Python version compatibility
```

### Debug Steps
1. Check application logs
2. Verify environment variables
3. Test API keys independently
4. Check network connectivity
5. Validate GitHub repository access

## 🎉 Success!

Your Web3.LOC application is now live and ready for use! You can:

- 🔍 Discover contracts on Ethereum and Base
- 💾 Store contracts in GitHub for remote access
- 🔎 Search both local and remote contract databases
- 📊 Analyze contract data and export results
- 🌐 Access your data from anywhere
- 👥 Share contract data with team members

## 📞 Need Help?

- 📖 Check the main README.md for detailed documentation
- 🐛 Open an issue on GitHub for bugs
- 💡 Submit feature requests via GitHub issues
- 📧 Contact support for deployment assistance

---

**Congratulations on deploying Web3.LOC live! 🚀**
