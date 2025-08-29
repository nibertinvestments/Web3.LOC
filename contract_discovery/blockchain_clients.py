"""
Simplified blockchain client for Ethereum and Base chains only.
Handles API connections with proper rate limiting (4 scans per second per API).
"""

import aiohttp
import logging
import os
from typing import Dict, List, Optional, Any
from datetime import datetime
from asyncio_throttle.throttler import Throttler
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class SimplifiedBlockchainClient:
    """Simplified blockchain client for Ethereum and Base only."""
    
    def __init__(self, chain_name: str):
        """Initialize client for specific chain (ethereum or base)."""
        self.chain_name = chain_name.lower()
        
        # Set up chain-specific configuration
        if self.chain_name == 'ethereum':
            self.api_key = os.getenv('ETHERSCAN_API_KEY')
            self.api_url = 'https://api.etherscan.io/api'
            self.chain_id = 1
        elif self.chain_name == 'base':
            self.api_key = os.getenv('BASESCAN_API_KEY')
            self.api_url = 'https://api.basescan.org/api'
            self.chain_id = 8453
        else:
            raise ValueError(f"Unsupported chain: {chain_name}. Only 'ethereum' and 'base' are supported.")
        
        if not self.api_key:
            raise ValueError(f"No API key found for {self.chain_name}")
            
        self.session: Optional[aiohttp.ClientSession] = None
        
        # Rate limiting: 4 scans per second per API
        self.throttler = Throttler(rate_limit=4, period=1.0)
        
        logger.info(f"Initialized {self.chain_name} client (Chain ID: {self.chain_id})")
        logger.info(f"API URL: {self.api_url}")
        logger.info(f"API Key: {self.api_key[:10]}...{self.api_key[-4:]}")
        
    async def initialize(self) -> None:
        """Initialize the HTTP session."""
        connector = aiohttp.TCPConnector(limit=10, limit_per_host=5)
        timeout = aiohttp.ClientTimeout(total=30)
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers={'User-Agent': 'Web3.LOC-ContractDiscovery/2.0'}
        )
        
    async def cleanup(self) -> None:
        """Cleanup resources."""
        if self.session:
            await self.session.close()
            
    async def _make_request(self, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Make throttled API request."""
        if not self.session:
            await self.initialize()
            
        # Add API key
        params['apikey'] = self.api_key
            
        async with self.throttler:
            try:
                # Ensure session exists
                if not self.session:
                    raise RuntimeError("Session not initialized")
                    
                async with self.session.get(self.api_url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get('status') == '1':
                            return data
                        else:
                            error_msg = data.get('message', 'Unknown error')
                            logger.warning(f"API error for {self.chain_name}: {error_msg}")
                            return None
                    else:
                        logger.error(f"HTTP error {response.status} for {self.chain_name}")
                        return None
            except Exception as e:
                logger.error(f"Request error for {self.chain_name}: {str(e)}")
                return None
                
    async def test_connection(self) -> bool:
        """Test API connection."""
        try:
            params = {
                'module': 'stats',
                'action': 'ethsupply'
            }
                
            result = await self._make_request(params)
            success = result is not None
            
            if success:
                logger.info(f"✅ {self.chain_name.upper()}: Connected successfully")
            else:
                logger.warning(f"❌ {self.chain_name.upper()}: Connection failed")
                
            return success
        except Exception as e:
            logger.error(f"Connection test failed for {self.chain_name}: {str(e)}")
            return False
            
    async def get_verified_contracts(self, limit: int = 100, start_block: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get verified contracts from the blockchain using a different approach."""
        contracts: List[Dict[str, Any]] = []
        
        logger.info(f"Fetching verified contracts from {self.chain_name} (limit: {limit})")
        
        # Use a list of known verified contract addresses for testing
        # In production, you would get these from various sources
        test_addresses = [
            "0xA0b86a33E6441c35d55E8BaBf441A9E3A7b1b9B8",  # Example contract 1
            "0xdAC17F958D2ee523a2206206994597C13D831ec7",  # USDT
            "0x6B175474E89094C44Da98b954EedeAC495271d0F",  # DAI
            "0xA0b86a33E6441c35d55E8BaBf441A9E3A7b1b9B8",  # Another example
            "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984",  # UNI
        ]
        
        # For Base chain, use different test addresses
        if self.chain_name == 'base':
            test_addresses = [
                "0x4200000000000000000000000000000000000006",  # WETH on Base
                "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",  # USDC on Base
                "0x50c5725949A6F0c72E6C4a641F24049A917DB0Cb",  # DAI on Base
            ]
        
        for address in test_addresses[:limit]:
            try:
                # Get contract source code to verify it's a verified contract
                source_data = await self.get_contract_source(address)
                if source_data and source_data.get('SourceCode'):
                    contract_data: Dict[str, Any] = {
                        'address': address,
                        'name': source_data.get('ContractName', 'Unknown'),
                        'source_code': source_data.get('SourceCode', ''),
                        'compiler_version': source_data.get('CompilerVersion', ''),
                        'optimization': source_data.get('OptimizationUsed', '0') == '1',
                        'runs': int(source_data.get('Runs', 0)),
                        'constructor_arguments': source_data.get('ConstructorArguments', ''),
                        'abi': source_data.get('ABI', ''),
                        'creation_txhash': '',  # Not available in this method
                        'block_number': 0,      # Not available in this method
                        'chain': self.chain_name,
                        'chain_id': self.chain_id,
                        'verified_date': datetime.now().isoformat()
                    }
                    contracts.append(contract_data)
                    logger.info(f"Added verified contract: {address} ({source_data.get('ContractName', 'Unknown')})")
                else:
                    logger.debug(f"Contract {address} is not verified or has no source code")
                    
            except Exception as e:
                logger.error(f"Error processing contract {address}: {str(e)}")
                continue
            
        logger.info(f"Retrieved {len(contracts)} verified contracts from {self.chain_name}")
        return contracts
        
    async def get_contract_source(self, address: str) -> Optional[Dict[str, Any]]:
        """Get contract source code."""
        params = {
            'module': 'contract',
            'action': 'getsourcecode',
            'address': address
        }
        
        response = await self._make_request(params)
        if response and 'result' in response and response['result']:
            result = response['result'][0]
            # Only return if contract is verified (has source code)
            if result.get('SourceCode'):
                return result
                
        return None
        
    async def get_contract_abi(self, address: str) -> Optional[str]:
        """Get contract ABI."""
        params = {
            'module': 'contract',
            'action': 'getabi',
            'address': address
        }
        
        response = await self._make_request(params)
        if response and 'result' in response:
            return response['result']
            
        return None


class BlockchainClientManager:
    """Simplified blockchain client manager for Ethereum and Base only."""
    
    def __init__(self):
        """Initialize the client manager."""
        self.clients: Dict[str, SimplifiedBlockchainClient] = {}
        self._initialized = False
        
    async def initialize(self) -> None:
        """Initialize clients for Ethereum and Base."""
        if self._initialized:
            return
            
        supported_chains = ['ethereum', 'base']
        
        logger.info(f"Initializing clients for chains: {supported_chains}")
        
        # Initialize clients for each supported chain
        for chain_name in supported_chains:
            try:
                client = SimplifiedBlockchainClient(chain_name)
                await client.initialize()
                
                # Test connection
                if await client.test_connection():
                    self.clients[chain_name] = client
                    logger.info(f"✅ {chain_name.upper()}: Client initialized successfully")
                else:
                    logger.warning(f"❌ {chain_name.upper()}: Failed connection test")
                    await client.cleanup()
                    
            except Exception as e:
                logger.error(f"Failed to initialize {chain_name} client: {str(e)}")
                
        self._initialized = True
        logger.info(f"🎉 Initialized {len(self.clients)} blockchain clients: {list(self.clients.keys())}")
        
    async def get_client(self, chain_name: str) -> Optional[SimplifiedBlockchainClient]:
        """Get client for specific chain."""
        if not self._initialized:
            await self.initialize()
            
        return self.clients.get(chain_name.lower())
        
    def get_available_chains(self) -> List[str]:
        """Get list of available chain names."""
        return list(self.clients.keys())
        
    async def get_all_verified_contracts(self, limit_per_chain: int = 50) -> List[Dict[str, Any]]:
        """Get verified contracts from all available chains."""
        all_contracts: List[Dict[str, Any]] = []
        
        for chain_name, client in self.clients.items():
            try:
                logger.info(f"Fetching contracts from {chain_name}...")
                contracts = await client.get_verified_contracts(limit=limit_per_chain)
                all_contracts.extend(contracts)
                logger.info(f"Got {len(contracts)} contracts from {chain_name}")
            except Exception as e:
                logger.error(f"Error fetching contracts from {chain_name}: {str(e)}")
                
        logger.info(f"Total contracts collected: {len(all_contracts)}")
        return all_contracts
        
    async def cleanup(self) -> None:
        """Cleanup all clients."""
        for client in self.clients.values():
            await client.cleanup()
        self.clients.clear()
        self._initialized = False


# Legacy compatibility aliases
EtherscanV2Client = SimplifiedBlockchainClient
BaseBlockchainClient = SimplifiedBlockchainClient
EtherscanClient = SimplifiedBlockchainClient
