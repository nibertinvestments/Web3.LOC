"""
Secure environment variable loader for Web3.LOC project.
Handles API keys and sensitive configuration data.
"""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

class SecretsLoader:
    """Centralized secrets and configuration management."""
    
    def __init__(self):
        """Initialize the secrets loader."""
        self._load_environment()
        
    def _load_environment(self):
        """Load environment variables from .env file."""
        env_path = Path(__file__).parent.parent / '.env'
        if env_path.exists():
            load_dotenv(env_path)
        else:
            print(f"Warning: .env file not found at {env_path}")
            print("Please copy .env.example to .env and fill in your API keys")
    
    def get_api_key(self, service: str) -> Optional[str]:
        """Get API key for a specific service."""
        key_mapping = {
            'etherscan': 'ETHERSCAN_API_KEY',
            'bscscan': 'BSC_API_KEY',
            'polygonscan': 'POLYGON_API_KEY',
            'arbiscan': 'ARBITRUM_API_KEY',
            'optimism': 'OPTIMISM_API_KEY',
            'snowtrace': 'AVALANCHE_API_KEY',
            'ftmscan': 'FANTOM_API_KEY',
            'github': 'GITHUB_TOKEN'
        }
        
        env_var = key_mapping.get(service.lower())
        if not env_var:
            raise ValueError(f"Unknown service: {service}")
            
        key = os.getenv(env_var)
        if not key or key.startswith('your_'):
            print(f"Warning: {env_var} not set or using placeholder value")
            return None
            
        return key
    
    def get_config(self, key: str, default=None):
        """Get configuration value."""
        return os.getenv(key, default)
    
    def get_rate_limit(self) -> int:
        """Get rate limit for API calls."""
        return int(os.getenv('RATE_LIMIT', 5))
    
    def get_contracts_dir(self) -> Path:
        """Get contracts output directory."""
        contracts_dir = os.getenv('CONTRACTS_DIR', './contracts_library')
        return Path(contracts_dir)
    
    def get_min_contract_age_days(self) -> int:
        """Get minimum contract age in days."""
        return int(os.getenv('MIN_CONTRACT_AGE_DAYS', 30))
    
    def get_max_contracts_per_run(self) -> int:
        """Get maximum contracts to process per run."""
        return int(os.getenv('MAX_CONTRACTS_PER_RUN', 1000))
    
    def get_github_rate_limit(self) -> int:
        """Get GitHub API rate limit (80% of max)."""
        return int(os.getenv('GITHUB_RATE_LIMIT', 4000))
    
    def get_github_token(self) -> Optional[str]:
        """Get GitHub personal access token."""
        return self.get_api_key('github')

# Global instance
secrets = SecretsLoader()