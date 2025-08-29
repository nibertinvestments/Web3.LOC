# Web3.LOC - Live Contract Discovery Platform

Web3.LOC is a comprehensive smart contract discovery and analysis platform that works both locally and as a live deployment using GitHub as a storage backend. It enables users to discover, analyze, and manage smart contracts across multiple blockchain networks.

## 🌟 Features

### Core Functionality
- **Multi-Chain Support**: Ethereum and Base blockchain networks
- **Contract Discovery**: Automated contract detection and verification
- **Advanced Search**: Filter contracts by name, address, chain, and more
- **Contract Analysis**: Detailed analysis including ABI extraction and source code review
- **Export Capabilities**: Export contract data in various formats

### Live Deployment Features
- **GitHub Storage Backend**: Store contracts remotely for live deployment
- **Remote Contract Search**: Search and access contracts from GitHub repository
- **Cross-Device Access**: Access your contract database from anywhere
- **Team Collaboration**: Share contract data with team members
- **Automatic Backup**: Contracts are automatically backed up to GitHub

## 🚀 Quick Start

### Local Development Setup

1. **Clone the repository**
```bash
git clone https://github.com/your-username/Web3.LOC.git
cd Web3.LOC
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables**
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your actual values
# Required: ETHERSCAN_API_KEY, BASESCAN_API_KEY
# Optional for live deployment: GITHUB_TOKEN, GITHUB_REPO
```

4. **Run the application**
```bash
streamlit run web3_loc_gui.py
```

### Live Deployment Setup

For live deployment with GitHub storage backend:

1. **Create a GitHub repository** for contract storage
   - Create a new public or private repository
   - Note the repository name in format `username/repo-name`

2. **Generate GitHub Personal Access Token**
   - Go to GitHub Settings → Developer settings → Personal access tokens
   - Generate a new token with `repo` scope
   - Copy the token securely

3. **Configure environment variables**
```bash
# Required for live deployment
GITHUB_TOKEN=your_github_personal_access_token
GITHUB_REPO=your-username/your-repo-name

# Required for contract discovery
ETHERSCAN_API_KEY=your_etherscan_api_key
BASESCAN_API_KEY=your_basescan_api_key
```

4. **Deploy to cloud platform**
   - Deploy to Streamlit Cloud, Heroku, or your preferred platform
   - Ensure environment variables are set in your deployment platform

## 🎯 Usage Guide

### Contract Discovery

1. **Navigate to Discovery tab**
2. **Select blockchain network** (Ethereum or Base)
3. **Enter contract address** or use automated discovery
4. **Review contract details** including source code and ABI
5. **Save to database** for future reference

### Contract Search

#### Local Database Search
- Search contracts stored in your local database
- Filter by name, address, or description
- View detailed contract information

#### Remote Repository Search
- Search contracts stored in GitHub repository
- Filter by chain, name, or address
- Load full contract details on demand
- View repository statistics

### Data Management

- **Export Data**: Export contract data to CSV format
- **Database Statistics**: View local database statistics
- **GitHub Integration**: Sync with remote repository
- **Backup Management**: Automatic backup to GitHub

## 🏗️ Architecture

### Components

1. **Web3.LOC GUI** (`web3_loc_gui.py`)
   - Modern Streamlit interface
   - Tab-based navigation
   - Real-time contract analysis

2. **Blockchain Client Manager** (`enhanced_blockchain_client.py`)
   - Multi-chain support
   - API rate limiting
   - Contract verification

3. **Contract Database** (`contract_database.py`)
   - SQLite local storage
   - Contract analysis
   - Search functionality

4. **GitHub Storage Manager** (`github_storage.py`)
   - Remote storage backend
   - Async operations
   - Contract indexing

5. **Main System** (`main.py`)
   - System coordination
   - Workflow management
   - Error handling

### Data Flow

1. **Contract Discovery**: User inputs contract address
2. **Blockchain Query**: System fetches contract data from blockchain
3. **Analysis**: Contract is analyzed for security and functionality
4. **Storage**: Contract is stored locally and optionally in GitHub
5. **Search**: Users can search both local and remote storage

## 🔧 Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `ETHERSCAN_API_KEY` | Yes | Etherscan API key for Ethereum contract data |
| `BASESCAN_API_KEY` | Yes | Basescan API key for Base contract data |
| `GITHUB_TOKEN` | No* | GitHub personal access token for remote storage |
| `GITHUB_REPO` | No* | GitHub repository in format `owner/repo` |

*Required for live deployment with GitHub storage

### API Keys Setup

#### Etherscan API Key
1. Visit [etherscan.io](https://etherscan.io/apis)
2. Create account and generate API key
3. Add to `.env` file as `ETHERSCAN_API_KEY=your_key_here`

#### Basescan API Key
1. Visit [basescan.org](https://basescan.org/apis)
2. Create account and generate API key
3. Add to `.env` file as `BASESCAN_API_KEY=your_key_here`

## 🚀 Deployment Options

### Streamlit Cloud
1. Push code to GitHub repository
2. Connect Streamlit Cloud to your repository
3. Configure environment variables in Streamlit Cloud dashboard
4. Deploy with one click

### Heroku
1. Create Heroku app
2. Connect to GitHub repository
3. Configure environment variables in Heroku dashboard
4. Deploy using Heroku CLI or dashboard

### Docker
```dockerfile
FROM python:3.9

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "web3_loc_gui.py"]
```

## 📊 Features in Detail

### Contract Analysis
- **Source Code Review**: Full Solidity source code analysis
- **ABI Extraction**: Automatic ABI extraction and formatting
- **Security Analysis**: Basic security pattern detection
- **Optimization Check**: Compiler optimization detection

### Search Capabilities
- **Fuzzy Search**: Intelligent matching for contract names
- **Multi-Filter Search**: Combine multiple search criteria
- **Real-time Results**: Instant search results as you type
- **Export Results**: Export search results to CSV

### GitHub Integration
- **Automatic Sync**: Contracts automatically stored in GitHub
- **Version Control**: Full version history of contract changes
- **Collaboration**: Share contract database with team members
- **Backup**: Automatic backup and restore capabilities

## 🔍 Troubleshooting

### Common Issues

#### GitHub Authentication Failed
- Verify GitHub token has correct permissions
- Check repository name format (`owner/repo`)
- Ensure token is not expired

#### API Rate Limits
- Upgrade to paid Etherscan/Basescan plans
- Implement request throttling
- Use multiple API keys for load balancing

#### Missing Contract Data
- Verify contract is verified on blockchain explorer
- Check network selection (Ethereum vs Base)
- Ensure contract address is correct

### Performance Optimization
- Use GitHub storage for large contract collections
- Implement local caching for frequently accessed contracts
- Enable database indexing for faster searches

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## � Acknowledgments

- Etherscan and Basescan for providing blockchain data APIs
- Streamlit for the amazing web framework
- GitHub for hosting and storage capabilities
- The Ethereum and Base communities for their continued innovation

## 📞 Support

For support, please open an issue on GitHub or contact the development team.

---

**Made with ❤️ for the Web3 community**

Web3.LOC is a comprehensive smart contract discovery platform that automatically finds, analyzes, and documents verified smart contracts from multiple blockchain networks. The system features advanced bytecode-level deduplication, real-time contract analysis, and a modern web interface for exploration and filtering.

### Key Features

- **🔍 Multi-Chain Discovery**: Supports Ethereum, Base, and other EVM-compatible networks
- **🧬 Bytecode Analysis**: SHA256-based deduplication prevents exact contract duplicates
- **📊 Modern Web GUI**: Streamlit-based interface with filtering, search, and analytics
- **📁 Automated Documentation**: Generates comprehensive README files for each contract
- **💾 Export Capabilities**: CSV export with customizable field selection
- **🛡️ Security Analysis**: Automated security pattern detection and risk assessment
- **⚡ Rate-Limited APIs**: Intelligent throttling to respect API limits

### 🧠 Intelligent Analysis
- **Contract Classification**: Automatically categorizes contracts into 20+ types
- **Dynamic Category Detection**: Automatically creates new categories when novel contract types are discovered
- **Security Analysis**: Identifies potential security patterns and vulnerabilities
- **Code Deduplication**: Uses SHA-256 hashing to prevent duplicate contracts

### 📁 Hierarchical Organization
- **Chain-based Structure**: Organizes contracts by blockchain first, then by type
- **Comprehensive Documentation**: Generates detailed README files for each contract
- **Cross-referencing**: Builds relationships between similar contracts
- **Metadata Storage**: Maintains rich metadata including gas usage, security score, and dependencies

## ⚡ Quick Start

### 1. Setup
```powershell
# Clone the repository
git clone <repository-url>
cd Web3.LOC

# Run automated setup
.\scripts\setup.ps1
```

### 2. Configure API Keys
Edit `.env` file with your API key:
```env
# Your Etherscan API key (works with all EVM chains except BSC)
ETHERSCAN_API_KEY=CCTZK119D6N5GZHC3NCP833TKVN6BP9ED5
RATE_LIMIT=4

# GitHub token for library discovery (optional)
GITHUB_TOKEN=your_github_token_here
GITHUB_RATE_LIMIT=4000
```

### 3. Start Discovery
```bash
# Discover from blockchain explorers only (BSC excluded)
python contract_discovery/main.py discover --chains ethereum polygon arbitrum optimism avalanche fantom --limit 50

# Discover from GitHub only
python contract_discovery/main.py discover-github --limit 100

# Full discovery from both sources
python contract_discovery/main.py discover-all --limit 25 --github-limit 50 --update-refs --generate-reports
```

## 📋 Available Commands

| Command | Description | Example |
|---------|-------------|---------|
| `discover` | Discover from blockchain explorers | `python contract_discovery/main.py discover --chains ethereum --limit 50` |
| `discover-github` | Discover from GitHub repositories | `python contract_discovery/main.py discover-github --limit 100` |
| `discover-all` | Discover from both sources | `python contract_discovery/main.py discover-all --limit 25 --github-limit 50` |
| `update-refs` | Update cross-references between contracts | `python contract_discovery/main.py update-refs` |
| `reports` | Generate summary reports | `python contract_discovery/main.py reports` |

### Command Options
- `--chains`: Specific blockchains to process (ethereum, polygon, arbitrum, optimism, avalanche, fantom)
  - *Note: BSC removed - not supported by unified Etherscan API*
- `--limit`: Maximum contracts per blockchain
- `--github-limit`: Maximum contracts from GitHub
- `--update-refs`: Update cross-references after discovery
- `--generate-reports`: Generate reports after discovery

## 📊 System Output

### Generated Structure
```
contracts/
├── ethereum/
│   ├── ERC20/
│   │   ├── UniswapV2/
│   │   │   ├── contract.sol
│   │   │   ├── README.md
│   │   │   └── metadata.json
│   │   └── ...
│   ├── ERC721/
│   └── DEX/
├── polygon/
├── arbitrum/
├── optimism/
├── avalanche/
├── fantom/
├── github/
│   ├── LIBRARY/
│   ├── ERC20/
│   └── ...
└── reports/
    ├── discovery_summary.html
    ├── contract_statistics.json
    └── cross_references.json
```

### Contract Categories (Auto-detected)
- **Standard Tokens**: ERC20, ERC721, ERC1155
- **DeFi Protocols**: DEX, Lending, Staking, Yield Farming, AMM
- **Governance**: DAO, Voting, Proposal systems
- **Security**: Multisig, Timelock, Access Control
- **Infrastructure**: Proxy, Factory, Registry, Oracle
- **Gaming**: NFT Games, Marketplace, Rewards
- **And 20+ more categories with automatic detection!**

## 🔧 Project Structure

```
Web3.LOC/
├── contract_discovery/           # Main application modules
│   ├── main.py                  # CLI interface and orchestration
│   ├── blockchain_clients.py    # Multi-chain API clients
│   ├── github_client.py         # GitHub API integration  ⭐ NEW
│   ├── contract_analyzer.py     # Contract classification and analysis
│   ├── contract_organizer.py    # File organization and documentation
│   └── database_manager.py      # SQLite database operations
├── secrets/                     # Configuration management
│   └── loader.py               # Environment variable loading
├── scripts/                     # Utility scripts
├── tests/                      # Test files
├── requirements.txt           # Python dependencies
├── .env.example              # Environment template
└── README.md                 # This file
```

## 🛡️ API Rate Limiting

The system respects API rate limits:
- **Etherscan APIs**: Configurable (your key: 4 calls/second) - Works with all EVM chains except BSC
- **GitHub API**: 80% of maximum rate (4000/hour with token)
- **Automatic Throttling**: Built-in rate limiting prevents violations
- **Error Handling**: Graceful handling of rate limit responses

## 🔍 Key Features

### Automatic Category Creation
When discovering new contract types, the system:
1. Analyzes contract code for patterns
2. Creates new category folders automatically
3. Adds contracts to appropriate categories
4. Updates cross-reference system

### Comprehensive Documentation
Each contract gets:
- Detailed README with functionality explanation
- Security analysis and recommendations
- Gas usage patterns
- Cross-references to similar contracts
- Deployment information

### GitHub Integration ⭐ NEW
- Discovers Solidity libraries from GitHub
- Searches popular contracts by type
- Respects API rate limits (80% max usage)
- Validates library quality before inclusion

## 🗄️ Database Schema

SQLite database stores:
```sql
-- Contracts with metadata
CREATE TABLE contracts (
    id INTEGER PRIMARY KEY,
    code_hash TEXT UNIQUE,
    name TEXT,
    chain TEXT,
    address TEXT,
    contract_type TEXT,
    source_code TEXT,
    analysis_data TEXT,
    created_at TIMESTAMP
);

-- Cross-references between contracts
CREATE TABLE cross_references (
    id INTEGER PRIMARY KEY,
    source_contract_id INTEGER,
    target_contract_id INTEGER,
    relationship_type TEXT,
    similarity_score REAL
);
```

## 🐛 Troubleshooting

### Common Issues
1. **API Rate Limit Errors**: Reduce `RATE_LIMIT` in `.env`
2. **GitHub Token Issues**: Generate token with `public_repo` scope
3. **Database Errors**: Ensure `data/` directory is writable
4. **Memory Issues**: Use smaller `--limit` values

### Getting Help
- Check console logs for error details
- Validate config: `python scripts/validate_config.py`
- Review generated reports for system statistics

## 📈 Example Usage Session

```bash
# Full discovery session
python contract_discovery/main.py discover-all \
  --chains ethereum bsc polygon \
  --limit 50 \
  --github-limit 100 \
  --update-refs \
  --generate-reports

# Expected output:
# === Combined Discovery Results ===
# Total contracts discovered: 250
# Total contracts added: 200
# Total contracts skipped: 50
# 
# Blockchain Discovery:
#   Contracts discovered: 150
#   Contracts added: 125
#   Processing time: 45.2 seconds
# 
# GitHub Discovery:
#   Libraries discovered: 75
#   Contracts discovered: 25
#   Total added: 75
#   Processing time: 32.1 seconds
```

## 🚀 Recent Updates

### v2.0 - GitHub Integration
- ✅ Added GitHub API client for library discovery
- ✅ Enhanced contract analyzer with 40+ dynamic patterns
- ✅ Automatic category creation for new contract types
- ✅ Rate limiting at 80% of GitHub API maximum
- ✅ Cross-platform support and automated setup

### v1.0 - Core System
- ✅ Multi-chain blockchain explorer integration
- ✅ Intelligent contract deduplication
- ✅ Hierarchical file organization
- ✅ Comprehensive documentation generation
- ✅ SQLite database with cross-references

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

---

**Ready to explore the Web3 contract universe? Start with:**
```bash
python contract_discovery/main.py discover-all --limit 25 --github-limit 25 --update-refs --generate-reports
```

This repository also contains a data pipeline to surface underserved software problem niches you can build into revenue streams.

### Pipeline Stages
1. Collect Google Autocomplete suggestions (`data_collect/google_autocomplete.py`).
2. Normalize & deduplicate phrases (`processing/normalize.py`).
3. Embed + cluster semantically (`processing/embed_cluster.py`).
4. Simulate demand & supply signals, compute opportunity scores (`processing/scoring.py`).
5. Output CSV + JSON reports (`reports/`).

### Quick Start (Windows PowerShell)
Create & activate a virtual environment, install dependencies, then run the pipeline script.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
powershell -ExecutionPolicy Bypass -File .\scripts\run_pipeline.ps1 -SkipInstall
```

Outputs (after run):
- `data/autocomplete.jsonl`
- `data/queries_clean.jsonl`
- `data/clusters.csv`
- `reports/opportunities_simulated.csv`
- `reports/top10.json`

### Tests
```powershell
pytest -q
```

### Secret Handling & Security
Use a real `.env` file (never committed) for API keys and credentials. This repo omits any sample `.env.example` to avoid accidental production key leakage. Add `.env` to your local `.gitignore` (already present) and supply only actual keys you control. Rotate keys immediately if ever exposed.

### Next Steps
- Replace simulated metrics with real Reddit / StackOverflow / GitHub collectors.
- Add SERP/API based supply measurement.
- Enhance scoring with pain signal extraction.

---

Original scope (Web3 contract library) remains; pipeline lives alongside and can help identify smart-contract tooling gaps.
#   F o r c e   d e p l o y m e n t   t r i g g e r  
 