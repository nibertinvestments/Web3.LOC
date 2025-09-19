# 📖 Web3.LOC API Reference

This document provides comprehensive documentation for Web3.LOC's APIs and interfaces.

## 📋 Table of Contents

- [Command Line Interface](#command-line-interface)
- [Python API](#python-api)
- [REST API](#rest-api)
- [Configuration](#configuration)
- [Examples](#examples)

## Command Line Interface

### Main Commands

#### `discover`
Discover contracts from blockchain explorers.

```bash
python contract_discovery/main.py discover [OPTIONS]
```

**Options:**
- `--chains TEXT`: Blockchain networks to scan (ethereum, base, polygon, etc.)
- `--limit INTEGER`: Maximum contracts per blockchain (default: 100)
- `--start-block INTEGER`: Starting block number
- `--end-block INTEGER`: Ending block number
- `--address TEXT`: Specific contract address to analyze
- `--category TEXT`: Filter by contract category

**Examples:**
```bash
# Discover 50 contracts from Ethereum
python contract_discovery/main.py discover --chains ethereum --limit 50

# Discover from multiple chains
python contract_discovery/main.py discover --chains ethereum,base,polygon --limit 25

# Analyze specific contract
python contract_discovery/main.py discover --address 0x123... --chains ethereum
```

#### `discover-github`
Discover contracts from GitHub repositories.

```bash
python contract_discovery/main.py discover-github [OPTIONS]
```

**Options:**
- `--limit INTEGER`: Maximum repositories to scan (default: 100)
- `--language TEXT`: Programming language filter (default: Solidity)
- `--min-stars INTEGER`: Minimum GitHub stars (default: 10)
- `--query TEXT`: Custom search query

**Examples:**
```bash
# Discover popular Solidity contracts
python contract_discovery/main.py discover-github --limit 100 --min-stars 50

# Search specific topics
python contract_discovery/main.py discover-github --query "defi erc20" --limit 50
```

#### `discover-all`
Combined discovery from all sources.

```bash
python contract_discovery/main.py discover-all [OPTIONS]
```

**Options:**
- `--limit INTEGER`: Blockchain discovery limit
- `--github-limit INTEGER`: GitHub discovery limit
- `--update-refs`: Update cross-references after discovery
- `--generate-reports`: Generate analysis reports
- `--parallel`: Enable parallel processing

**Examples:**
```bash
# Full discovery with all features
python contract_discovery/main.py discover-all \
  --limit 50 \
  --github-limit 100 \
  --update-refs \
  --generate-reports \
  --parallel
```

#### `update-refs`
Update cross-references between contracts.

```bash
python contract_discovery/main.py update-refs [OPTIONS]
```

**Options:**
- `--threshold FLOAT`: Similarity threshold (0.0-1.0, default: 0.8)
- `--method TEXT`: Comparison method (bytecode, abi, source)

#### `reports`
Generate analysis reports.

```bash
python contract_discovery/main.py reports [OPTIONS]
```

**Options:**
- `--format TEXT`: Output format (html, json, csv)
- `--output TEXT`: Output directory path

### Supported Chains

| Chain | Identifier | API Provider |
|-------|------------|--------------|
| Ethereum | `ethereum` | Etherscan |
| Base | `base` | Basescan |
| Polygon | `polygon` | Polygonscan |
| Arbitrum | `arbitrum` | Arbiscan |
| Optimism | `optimism` | Optimistic Etherscan |
| Avalanche | `avalanche` | Snowtrace |
| Fantom | `fantom` | FTMScan |

## Python API

### Core Classes

#### `ContractAnalyzer`

Main class for contract analysis and categorization.

```python
from contract_discovery.contract_analyzer import ContractAnalyzer

analyzer = ContractAnalyzer()
```

**Methods:**

##### `analyze_contract(address: str, chain: str) -> Dict[str, Any]`

Analyze a smart contract and return detailed information.

```python
result = analyzer.analyze_contract(
    address="0x123...",
    chain="ethereum"
)

# Returns:
{
    "address": "0x123...",
    "chain": "ethereum",
    "category": "ERC-20 Token",
    "security_score": 85,
    "features": ["Pausable", "Mintable"],
    "abi": [...],
    "source_code": "...",
    "compilation_info": {...}
}
```

##### `categorize_contract(source_code: str, abi: List[Dict]) -> str`

Categorize a contract based on source code and ABI.

```python
category = analyzer.categorize_contract(
    source_code="contract Token { ... }",
    abi=[{"name": "transfer", ...}]
)
# Returns: "ERC-20 Token"
```

#### `BlockchainClient`

Client for interacting with blockchain APIs.

```python
from contract_discovery.blockchain_clients import BlockchainClient

client = BlockchainClient(
    api_key="your_api_key",
    chain="ethereum",
    rate_limit=4
)
```

**Methods:**

##### `get_contract_source(address: str) -> Dict[str, Any]`

Retrieve contract source code and metadata.

```python
source_data = client.get_contract_source("0x123...")

# Returns:
{
    "source_code": "contract Token { ... }",
    "abi": [...],
    "compiler_version": "0.8.19",
    "optimization": True,
    "optimization_runs": 200
}
```

##### `get_recent_contracts(limit: int = 100) -> List[str]`

Get recently verified contracts.

```python
contracts = client.get_recent_contracts(limit=50)
# Returns: ["0x123...", "0x456...", ...]
```

#### `GitHubClient`

Client for GitHub repository discovery.

```python
from contract_discovery.github_client import GitHubClient

client = GitHubClient(
    token="your_github_token",
    rate_limit=4000
)
```

**Methods:**

##### `search_repositories(query: str, limit: int = 100) -> List[Dict]`

Search GitHub repositories for smart contracts.

```python
repos = client.search_repositories(
    query="solidity erc20",
    limit=50
)

# Returns list of repository metadata
```

##### `get_solidity_files(repo: str) -> List[Dict]`

Extract Solidity files from a repository.

```python
files = client.get_solidity_files("owner/repo")

# Returns:
[
    {
        "path": "contracts/Token.sol",
        "content": "contract Token { ... }",
        "size": 1024
    }
]
```

#### `ContractDatabase`

Database interface for contract storage and retrieval.

```python
from contract_discovery.contract_database import ContractDatabase

db = ContractDatabase("data/contracts.db")
```

**Methods:**

##### `save_contract(contract_data: Dict) -> int`

Save contract to database.

```python
contract_id = db.save_contract({
    "address": "0x123...",
    "chain": "ethereum",
    "category": "ERC-20 Token",
    "source_code": "...",
    "abi": [...]
})
```

##### `search_contracts(query: str, filters: Dict = None) -> List[Dict]`

Search contracts in database.

```python
results = db.search_contracts(
    query="USDC",
    filters={
        "chain": "ethereum",
        "category": "ERC-20 Token"
    }
)
```

## REST API

Web3.LOC provides a REST API for integration with external applications.

### Base URL

```
http://localhost:8501/api/v1
```

### Authentication

Include your API key in the header:

```http
Authorization: Bearer your_api_key
```

### Endpoints

#### `GET /contracts`

List contracts with filtering and pagination.

**Parameters:**
- `chain` (string): Filter by blockchain
- `category` (string): Filter by contract category
- `limit` (integer): Number of results (max 1000)
- `offset` (integer): Pagination offset
- `search` (string): Search query

**Example:**
```http
GET /api/v1/contracts?chain=ethereum&category=ERC-20&limit=50
```

**Response:**
```json
{
    "contracts": [
        {
            "id": 1,
            "address": "0x123...",
            "chain": "ethereum",
            "category": "ERC-20 Token",
            "name": "USD Coin",
            "security_score": 95,
            "created_at": "2024-01-15T10:30:00Z"
        }
    ],
    "total": 1250,
    "limit": 50,
    "offset": 0
}
```

#### `GET /contracts/{id}`

Get detailed contract information.

**Example:**
```http
GET /api/v1/contracts/123
```

**Response:**
```json
{
    "id": 123,
    "address": "0x123...",
    "chain": "ethereum",
    "category": "ERC-20 Token",
    "source_code": "contract Token { ... }",
    "abi": [...],
    "security_analysis": {...},
    "features": ["Pausable", "Mintable"]
}
```

#### `POST /contracts/analyze`

Analyze a contract by address.

**Request Body:**
```json
{
    "address": "0x123...",
    "chain": "ethereum"
}
```

**Response:**
```json
{
    "analysis": {
        "category": "ERC-20 Token",
        "security_score": 85,
        "features": ["Pausable"],
        "recommendations": [...]
    }
}
```

#### `GET /stats`

Get platform statistics.

**Response:**
```json
{
    "total_contracts": 15420,
    "chains": {
        "ethereum": 8500,
        "base": 3200,
        "polygon": 2100
    },
    "categories": {
        "ERC-20 Token": 5200,
        "ERC-721 NFT": 3100,
        "DeFi": 2800
    }
}
```

## Configuration

### Environment Variables

#### Required

```env
ETHERSCAN_API_KEY=your_etherscan_key
BASESCAN_API_KEY=your_basescan_key
```

#### Optional

```env
# GitHub Integration
GITHUB_TOKEN=your_github_token
GITHUB_REPO=username/repository

# Performance
RATE_LIMIT=4
GITHUB_RATE_LIMIT=4000
MAX_WORKERS=4

# Database
DATABASE_PATH=data/contracts.db
BACKUP_ENABLED=true

# API Server
API_HOST=localhost
API_PORT=8501
API_KEY=your_api_key
```

### Configuration File

You can also use a YAML configuration file:

```yaml
# config.yaml
api_keys:
  etherscan: "your_key"
  basescan: "your_key"
  
discovery:
  rate_limit: 4
  max_contracts: 1000
  auto_categorize: true
  
github:
  token: "your_token"
  rate_limit: 4000
  
database:
  path: "data/contracts.db"
  backup_enabled: true
  
server:
  host: "localhost"
  port: 8501
```

Load configuration:

```python
from contract_discovery.config import load_config

config = load_config("config.yaml")
```

## Examples

### Basic Contract Analysis

```python
from contract_discovery import ContractAnalyzer, BlockchainClient

# Initialize components
client = BlockchainClient(api_key="your_key", chain="ethereum")
analyzer = ContractAnalyzer()

# Get contract data
contract_data = client.get_contract_source("0x123...")

# Analyze contract
analysis = analyzer.analyze_contract(
    address="0x123...",
    chain="ethereum"
)

print(f"Category: {analysis['category']}")
print(f"Security Score: {analysis['security_score']}")
print(f"Features: {', '.join(analysis['features'])}")
```

### Batch Contract Discovery

```python
from contract_discovery import ContractDatabase, BlockchainClient

db = ContractDatabase()
client = BlockchainClient(api_key="your_key", chain="ethereum")

# Get recent contracts
recent_contracts = client.get_recent_contracts(limit=100)

# Process each contract
for address in recent_contracts:
    try:
        # Get contract data
        contract_data = client.get_contract_source(address)
        
        # Save to database
        db.save_contract({
            "address": address,
            "chain": "ethereum",
            **contract_data
        })
        
        print(f"Processed: {address}")
        
    except Exception as e:
        print(f"Error processing {address}: {e}")
```

### GitHub Repository Analysis

```python
from contract_discovery import GitHubClient, ContractAnalyzer

github = GitHubClient(token="your_token")
analyzer = ContractAnalyzer()

# Search repositories
repos = github.search_repositories("defi solidity", limit=50)

for repo in repos:
    # Get Solidity files
    sol_files = github.get_solidity_files(repo["full_name"])
    
    for file in sol_files:
        # Analyze contract
        try:
            category = analyzer.categorize_contract(
                source_code=file["content"],
                abi=[]  # ABI not available from source
            )
            
            print(f"Found {category} in {repo['full_name']}/{file['path']}")
            
        except Exception as e:
            print(f"Error analyzing {file['path']}: {e}")
```

### Custom Contract Search

```python
from contract_discovery import ContractDatabase

db = ContractDatabase()

# Complex search with multiple filters
results = db.search_contracts(
    query="token",
    filters={
        "chain": ["ethereum", "base"],
        "category": ["ERC-20 Token", "ERC-721 NFT"],
        "security_score_min": 80,
        "has_features": ["Pausable", "Upgradeable"]
    }
)

for contract in results:
    print(f"{contract['name']} ({contract['address']})")
    print(f"  Category: {contract['category']}")
    print(f"  Security: {contract['security_score']}/100")
    print(f"  Features: {', '.join(contract['features'])}")
    print()
```

## Error Handling

### Common Error Codes

| Code | Description | Solution |
|------|-------------|----------|
| `API_KEY_INVALID` | Invalid API key | Check key validity and permissions |
| `RATE_LIMIT_EXCEEDED` | API rate limit exceeded | Reduce rate limit or wait |
| `CONTRACT_NOT_FOUND` | Contract not found on blockchain | Verify address and network |
| `NETWORK_ERROR` | Network connectivity issue | Check internet connection |
| `DATABASE_ERROR` | Database operation failed | Check database permissions |

### Error Response Format

```json
{
    "error": {
        "code": "RATE_LIMIT_EXCEEDED",
        "message": "API rate limit exceeded. Try again in 3600 seconds.",
        "details": {
            "retry_after": 3600,
            "limit": 5,
            "reset_time": "2024-01-15T11:30:00Z"
        }
    }
}
```

---

## Support

For API support and questions:
- 📖 [Documentation](../README.md)
- 🐛 [Report Issues](https://github.com/nibertinvestments/Web3.LOC/issues)
- 💬 [Discussions](https://github.com/nibertinvestments/Web3.LOC/discussions)