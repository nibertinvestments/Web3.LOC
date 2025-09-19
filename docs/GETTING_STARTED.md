# 🚀 Getting Started with Web3.LOC

This guide will help you get Web3.LOC up and running quickly.

## 📋 Prerequisites

Before you begin, ensure you have:

- **Python 3.9 or higher** - [Download here](https://www.python.org/downloads/)
- **Git** - [Download here](https://git-scm.com/downloads/)
- **API Keys** - Free accounts from Etherscan and Basescan

## 🌟 Quick Start Options

### Option 1: Try the Live Demo (No Installation)

**🔗 [Visit Web3.LOC Live Demo](https://nibertinvestments.github.io/Web3.LOC/)**

Perfect for:
- First-time users
- Quick contract searches
- Evaluating the platform

### Option 2: Local Installation (Full Features)

Perfect for:
- Development and customization
- Large-scale contract discovery
- Offline usage

## 💻 Local Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/nibertinvestments/Web3.LOC.git
cd Web3.LOC
```

### Step 2: Set Up Python Environment

**Option A: Standard Installation**
```bash
pip install -r requirements.txt
```

**Option B: Virtual Environment (Recommended)**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Configure API Keys

1. **Copy the example environment file:**
   ```bash
   cp .env.example .env
   ```

2. **Get your free API keys:**
   - **Etherscan**: Visit [etherscan.io/apis](https://etherscan.io/apis)
   - **Basescan**: Visit [basescan.org/apis](https://basescan.org/apis)

3. **Edit the .env file:**
   ```env
   # Required API keys
   ETHERSCAN_API_KEY=your_etherscan_key_here
   BASESCAN_API_KEY=your_basescan_key_here
   
   # Optional: GitHub integration
   GITHUB_TOKEN=your_github_token_here
   GITHUB_REPO=username/repository-name
   
   # Performance settings
   RATE_LIMIT=4
   ```

### Step 4: Launch the Application

```bash
streamlit run web3_loc_gui.py
```

Your browser will open to `http://localhost:8501` with the Web3.LOC interface.

## 🎯 First Steps Tutorial

### 1. Discover Your First Contract

1. **Navigate to the Discovery tab**
2. **Select a blockchain** (Ethereum or Base)
3. **Enter a contract address** or use auto-discovery
4. **Click "Discover"** to analyze the contract

**Example contract addresses to try:**
- Ethereum USDC: `0xA0b86a33E6431B7ff34d1A1D49e12B52E0C41AE3`
- Base USDC: `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`

### 2. Explore Contract Details

After discovery, you'll see:
- **Contract category** (ERC-20, NFT, DeFi, etc.)
- **Security analysis** with risk assessment
- **Source code** with syntax highlighting
- **ABI interface** for contract interaction
- **Deployment information** and metadata

### 3. Search and Filter

1. **Go to the Search tab**
2. **Use filters** to narrow results:
   - Contract name or address
   - Blockchain network
   - Contract category
   - Security score range
3. **Export results** to CSV for further analysis

### 4. Manage Your Data

- **Local Database**: All contracts saved automatically
- **GitHub Backup**: Enable for cloud storage
- **Export Options**: CSV, JSON, Solidity files
- **Statistics**: View discovery metrics

## 🔧 Configuration Options

### Basic Configuration

```env
# API Keys (Required)
ETHERSCAN_API_KEY=your_key
BASESCAN_API_KEY=your_key

# Rate Limiting
RATE_LIMIT=4                    # API calls per second
GITHUB_RATE_LIMIT=4000         # GitHub API limit per hour
```

### Advanced Configuration

```env
# Database Settings
DATABASE_PATH=data/contracts.db
BACKUP_ENABLED=true
BACKUP_INTERVAL=3600           # seconds

# Discovery Settings
MAX_CONTRACTS_PER_RUN=1000
AUTO_CATEGORIZE=true
SECURITY_ANALYSIS=true

# GitHub Integration
GITHUB_TOKEN=your_token
GITHUB_REPO=username/repo
AUTO_SYNC=true
SYNC_INTERVAL=1800            # seconds
```

## 🛠️ Command Line Usage

Web3.LOC also provides a powerful command-line interface:

### Basic Discovery

```bash
# Discover from Ethereum
python contract_discovery/main.py discover --chains ethereum --limit 50

# Discover from multiple chains
python contract_discovery/main.py discover --chains ethereum base polygon --limit 25

# Discover from GitHub repositories
python contract_discovery/main.py discover-github --limit 100
```

### Advanced Commands

```bash
# Full discovery with reporting
python contract_discovery/main.py discover-all \
  --limit 50 \
  --github-limit 100 \
  --update-refs \
  --generate-reports

# Update cross-references
python contract_discovery/main.py update-refs

# Generate reports
python contract_discovery/main.py reports
```

## 🐛 Troubleshooting

### Common Issues

**1. "API Key Invalid" Error**
- Verify your API keys are correct
- Check that keys have proper permissions
- Ensure no extra spaces in .env file

**2. "Rate Limit Exceeded"**
- Reduce `RATE_LIMIT` in .env file
- Wait for rate limit reset (usually 1 hour)
- Consider upgrading to paid API plans

**3. "Database Connection Error"**
- Ensure the `data/` directory exists and is writable
- Check disk space availability
- Try deleting and recreating the database

**4. "GitHub Authentication Failed"**
- Verify GitHub token has correct permissions
- Check repository name format (`owner/repo`)
- Ensure token hasn't expired

### Getting Help

- **Documentation**: Check the [main README](./README.md)
- **Issues**: [Report bugs](https://github.com/nibertinvestments/Web3.LOC/issues)
- **Discussions**: [Ask questions](https://github.com/nibertinvestments/Web3.LOC/discussions)

## 📚 Next Steps

Once you're comfortable with the basics:

1. **Explore Advanced Features**:
   - Set up GitHub integration for cloud storage
   - Use the command-line interface for automation
   - Create custom contract categories

2. **Integrate with Your Workflow**:
   - Export data for analysis in other tools
   - Set up automated discovery scripts
   - Share contract databases with your team

3. **Contribute to the Project**:
   - Report bugs and suggest improvements
   - Add support for new blockchain networks
   - Help improve documentation

## 🎉 Welcome to Web3.LOC!

You're now ready to explore the world of smart contracts. Start discovering, analyzing, and organizing contracts across multiple blockchain networks.

**Happy exploring! 🚀**