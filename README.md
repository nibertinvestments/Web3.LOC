<div align="center">

# 🔍 Web3.LOC

**Smart Contract Discovery & Analysis Platform**

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live-brightgreen)](https://nibertinvestments.github.io/Web3.LOC/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)

[🚀 **Live Demo**](https://nibertinvestments.github.io/Web3.LOC/) • [📚 **Documentation**](./docs/) • [🐛 **Report Bug**](https://github.com/nibertinvestments/Web3.LOC/issues) • [💡 **Request Feature**](https://github.com/nibertinvestments/Web3.LOC/issues)

---

*Discover, analyze, and manage smart contracts across multiple blockchain networks with intelligent categorization and comprehensive documentation generation.*

</div>

## 📋 Table of Contents

- [✨ Features](#-features)
- [🚀 Quick Start](#-quick-start)
- [💻 Installation](#-installation)
- [🎯 Usage](#-usage)
- [🏗️ Architecture](#️-architecture)
- [🔧 Configuration](#-configuration)
- [📖 API Reference](#-api-reference)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)
- [💬 Support](#-support)

## ✨ Features

### 🔗 Multi-Chain Support
- **Ethereum** - Full contract discovery and analysis
- **Base** - Complete Base network integration
- **EVM Compatible** - Support for all EVM-based networks

### 🧠 Intelligent Analysis
- **Automatic Categorization** - AI-powered contract classification
- **Security Analysis** - Built-in security pattern detection
- **Bytecode Deduplication** - SHA256-based duplicate prevention
- **Comprehensive Documentation** - Auto-generated README files

### 💾 Flexible Storage
- **Local Database** - SQLite for offline access
- **GitHub Integration** - Cloud storage and collaboration
- **Cross-Device Sync** - Access your data anywhere
- **Export Options** - CSV, JSON, and Solidity formats

### 🌐 Modern Interface
- **Web Application** - Clean, responsive web interface
- **Live Deployment** - GitHub Pages integration
- **Real-time Search** - Instant contract filtering
- **Analytics Dashboard** - Comprehensive statistics

## 🚀 Quick Start

### 🌟 Try the Live Demo

Visit our [**live deployment**](https://nibertinvestments.github.io/Web3.LOC/) to try Web3.LOC without any installation.

### ⚡ Local Setup (5 minutes)

```bash
# 1. Clone the repository
git clone https://github.com/nibertinvestments/Web3.LOC.git
cd Web3.LOC

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure API keys (see Configuration section)
cp .env.example .env
# Edit .env with your API keys

# 4. Launch the application
streamlit run web3_loc_gui.py
```

## 💻 Installation

### Prerequisites

- **Python 3.9+** - [Download Python](https://www.python.org/downloads/)
- **Git** - [Download Git](https://git-scm.com/downloads)
- **API Keys** - Etherscan and Basescan (see [Configuration](#-configuration))

### Method 1: Standard Installation

```bash
git clone https://github.com/nibertinvestments/Web3.LOC.git
cd Web3.LOC
pip install -r requirements.txt
```

### Method 2: Development Installation

```bash
git clone https://github.com/nibertinvestments/Web3.LOC.git
cd Web3.LOC
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Method 3: Docker Installation

```bash
docker-compose up -d
```

## 🎯 Usage

### 🔍 Contract Discovery

**Web Interface:**
```bash
streamlit run web3_loc_gui.py
```

**Command Line:**
```bash
# Discover contracts from blockchain explorers
python contract_discovery/main.py discover --chains ethereum --limit 50

# Discover from GitHub repositories
python contract_discovery/main.py discover-github --limit 100

# Full discovery from all sources
python contract_discovery/main.py discover-all --limit 25 --github-limit 50
```

### 📊 Contract Analysis

The platform automatically:
- ✅ **Categorizes** contracts into 20+ types (ERC-20, NFT, DeFi, etc.)
- ✅ **Analyzes** security patterns and vulnerabilities
- ✅ **Generates** comprehensive documentation
- ✅ **Creates** cross-references between similar contracts

### 💾 Data Management

- **Local Storage**: SQLite database for offline access
- **Cloud Backup**: GitHub repository integration
- **Export Options**: CSV, JSON, and Solidity formats
- **Search & Filter**: Advanced filtering and search capabilities

## 🏗️ Architecture

```
Web3.LOC/
├── 🌐 Frontend
│   ├── docs/                 # GitHub Pages site
│   ├── web3_loc_gui.py      # Streamlit interface
│   └── streamlit_app.py     # Alternative interface
├── 🔧 Backend
│   ├── contract_discovery/   # Core discovery engine
│   ├── github_storage.py    # GitHub integration
│   └── main.py              # Application orchestrator
├── 📊 Data
│   ├── Local SQLite         # Contract database
│   └── GitHub Repository    # Cloud storage
└── 🔧 Configuration
    ├── .env                 # Environment variables
    └── requirements.txt     # Dependencies
```

### Core Components

| Component | Description | Technology |
|-----------|-------------|------------|
| **Discovery Engine** | Multi-chain contract detection | Python, Web3.py |
| **Analysis Module** | Contract categorization & security | Custom algorithms |
| **Storage Layer** | Local & cloud data management | SQLite, GitHub API |
| **Web Interface** | User-friendly frontend | Streamlit, HTML/CSS/JS |
| **Documentation Generator** | Automated README creation | Jinja2 templates |

## 🔧 Configuration

### Required API Keys

1. **Etherscan API Key** (Free)
   - Visit [etherscan.io/apis](https://etherscan.io/apis)
   - Register and create API key
   - Add to `.env` as `ETHERSCAN_API_KEY=your_key_here`

2. **Basescan API Key** (Free)
   - Visit [basescan.org/apis](https://basescan.org/apis)
   - Register and create API key
   - Add to `.env` as `BASESCAN_API_KEY=your_key_here`

### Optional Configuration

3. **GitHub Integration** (For cloud storage)
   - Create [Personal Access Token](https://github.com/settings/personal-access-tokens)
   - Add to `.env` as `GITHUB_TOKEN=your_token_here`
   - Set repository: `GITHUB_REPO=username/repository-name`

### Environment Variables

```env
# Required
ETHERSCAN_API_KEY=your_etherscan_key_here
BASESCAN_API_KEY=your_basescan_key_here

# Optional (for GitHub storage)
GITHUB_TOKEN=your_github_token_here
GITHUB_REPO=username/web3-loc-storage

# Performance tuning
RATE_LIMIT=4
GITHUB_RATE_LIMIT=4000
```

## 📖 API Reference

### Command Line Interface

| Command | Description | Example |
|---------|-------------|---------|
| `discover` | Discover from blockchain | `python main.py discover --chains ethereum --limit 50` |
| `discover-github` | Discover from GitHub | `python main.py discover-github --limit 100` |
| `discover-all` | Full discovery | `python main.py discover-all --update-refs` |
| `reports` | Generate reports | `python main.py reports` |

### Supported Chains

- ✅ **Ethereum** (`ethereum`)
- ✅ **Base** (`base`)
- ✅ **Polygon** (`polygon`)
- ✅ **Arbitrum** (`arbitrum`)
- ✅ **Optimism** (`optimism`)
- ✅ **Avalanche** (`avalanche`)
- ✅ **Fantom** (`fantom`)

### Contract Categories

The system automatically detects and categorizes contracts:

- 🪙 **Tokens**: ERC-20, ERC-721, ERC-1155
- 🏦 **DeFi**: DEX, Lending, Staking, Yield Farming
- 🏛️ **Governance**: DAO, Voting, Proposals
- 🔒 **Security**: Multisig, Timelock, Access Control
- 🏗️ **Infrastructure**: Proxy, Factory, Registry
- 🎮 **Gaming**: NFT Games, Marketplace, Rewards
- *And 20+ more categories...*

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### 🐛 Bug Reports

1. Check [existing issues](https://github.com/nibertinvestments/Web3.LOC/issues)
2. Create a [new issue](https://github.com/nibertinvestments/Web3.LOC/issues/new)
3. Include detailed reproduction steps
4. Attach logs and screenshots

### 💡 Feature Requests

1. Check [existing requests](https://github.com/nibertinvestments/Web3.LOC/issues?q=is%3Aissue+label%3Aenhancement)
2. Create a [feature request](https://github.com/nibertinvestments/Web3.LOC/issues/new)
3. Describe the use case and expected behavior
4. Include mockups or examples if applicable

### 🔧 Development

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Make** your changes
4. **Add** tests for new functionality
5. **Commit** your changes: `git commit -m 'Add amazing feature'`
6. **Push** to your branch: `git push origin feature/amazing-feature`
7. **Open** a Pull Request

### 📝 Documentation

Help improve our documentation:
- Fix typos and grammar
- Add examples and use cases
- Improve API documentation
- Create tutorials and guides

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Third-Party Licenses

- [Streamlit](https://streamlit.io/) - Apache 2.0 License
- [Web3.py](https://web3py.readthedocs.io/) - MIT License
- [Chart.js](https://www.chartjs.org/) - MIT License

## 💬 Support

### 📞 Get Help

- 📖 **Documentation**: Check this README and the [docs/](./docs/) folder
- 🐛 **Bug Reports**: [Create an issue](https://github.com/nibertinvestments/Web3.LOC/issues/new)
- 💡 **Feature Requests**: [Request a feature](https://github.com/nibertinvestments/Web3.LOC/issues/new)
- 📧 **Direct Contact**: Open an issue for assistance

### 🔧 Troubleshooting

**Common Issues:**

- **API Rate Limits**: Reduce `RATE_LIMIT` in `.env`
- **GitHub Authentication**: Verify token permissions
- **Database Errors**: Ensure write permissions in data directory
- **Memory Issues**: Use smaller `--limit` values

### 🚀 Deployment Help

- **GitHub Pages**: See [LIVE_DEPLOYMENT.md](./LIVE_DEPLOYMENT.md)
- **Streamlit Cloud**: See [DEPLOYMENT.md](./DEPLOYMENT.md)
- **Docker**: Use the included `docker-compose.yml`

---

<div align="center">

**⭐ Star this repository if you find it useful!**

**Made with ❤️ for the Web3 community**

[🚀 **Try Live Demo**](https://nibertinvestments.github.io/Web3.LOC/) • [📚 **Read Docs**](./docs/) • [🤝 **Contribute**](https://github.com/nibertinvestments/Web3.LOC/blob/main/CONTRIBUTING.md)

</div>