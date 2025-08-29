"""
GitHub Storage Manager for Web3.LOC
Stores contract data in GitHub repository as JSON files for live deployment.
"""

import os
import json
import base64
import hashlib
import aiohttp
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class GitHubStorageManager:
    """Manages contract storage in GitHub repository."""
    
    def __init__(self) -> None:
        """Initialize GitHub storage manager."""
        self.github_token: Optional[str] = os.getenv('GITHUB_TOKEN')
        self.github_repo: str = os.getenv('GITHUB_REPO', 'joshm1211/web3-loc-contracts')
        self.branch: str = 'main'
        self.base_url: str = 'https://api.github.com'
        self.session: Optional[aiohttp.ClientSession] = None
        
        if not self.github_token:
            logger.warning("No GitHub token found. GitHub storage will not be available.")
            
    async def initialize(self) -> None:
        """Initialize the HTTP session."""
        if not self.github_token:
            return
            
        self.session = aiohttp.ClientSession(
            headers={
                'Authorization': f'token {self.github_token}',
                'Accept': 'application/vnd.github.v3+json',
                'User-Agent': 'Web3.LOC-Storage/1.0'
            },
            timeout=aiohttp.ClientTimeout(total=30)
        )
        
        # Ensure repository structure exists
        await self._ensure_repo_structure()
        
    async def cleanup(self) -> None:
        """Cleanup resources."""
        if self.session:
            await self.session.close()
            
    async def _ensure_repo_structure(self) -> None:
        """Ensure required directories exist in repository."""
        directories = [
            'contracts/ethereum',
            'contracts/base',
            'metadata',
            'indexes'
        ]
        
        for directory in directories:
            await self._create_directory_if_not_exists(directory)
            
    async def _create_directory_if_not_exists(self, path: str) -> None:
        """Create directory in repository if it doesn't exist."""
        if not self.session:
            return
            
        try:
            # Check if directory exists by trying to get its contents
            url = f"{self.base_url}/repos/{self.github_repo}/contents/{path}"
            async with self.session.get(url) as response:
                if response.status == 404:
                    # Directory doesn't exist, create it with a .gitkeep file
                    await self._create_file(f"{path}/.gitkeep", "", f"Create {path} directory")
                    logger.info(f"Created directory: {path}")
        except Exception as e:
            logger.error(f"Error creating directory {path}: {str(e)}")
            
    async def _get_file_sha(self, file_path: str) -> Optional[str]:
        """Get SHA of existing file."""
        if not self.session:
            return None
            
        try:
            url = f"{self.base_url}/repos/{self.github_repo}/contents/{file_path}"
            async with self.session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('sha')
        except Exception:
            pass
        return None
        
    async def _create_file(self, file_path: str, content: str, commit_message: str) -> bool:
        """Create or update file in repository."""
        if not self.session:
            return False
            
        try:
            url = f"{self.base_url}/repos/{self.github_repo}/contents/{file_path}"
            
            # Get existing file SHA if it exists
            existing_sha = await self._get_file_sha(file_path)
            
            # Encode content
            encoded_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')
            
            data: Dict[str, Any] = {
                'message': commit_message,
                'content': encoded_content,
                'branch': self.branch
            }
            
            if existing_sha:
                data['sha'] = existing_sha
                
            async with self.session.put(url, json=data) as response:
                if response.status in [200, 201]:
                    logger.debug(f"Successfully created/updated file: {file_path}")
                    return True
                else:
                    error_data = await response.json()
                    logger.error(f"Failed to create file {file_path}: {error_data}")
                    return False
                    
        except Exception as e:
            logger.error(f"Error creating file {file_path}: {str(e)}")
            return False
            
    async def _get_file_content(self, file_path: str) -> Optional[str]:
        """Get file content from repository."""
        if not self.session:
            return None
            
        try:
            url = f"{self.base_url}/repos/{self.github_repo}/contents/{file_path}"
            async with self.session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    content = base64.b64decode(data['content']).decode('utf-8')
                    return content
        except Exception as e:
            logger.error(f"Error getting file {file_path}: {str(e)}")
        return None
        
    def _generate_contract_id(self, contract_data: Dict[str, Any]) -> str:
        """Generate unique ID for contract."""
        # Use address + chain as unique identifier
        identifier = f"{contract_data['address']}_{contract_data['chain']}"
        return hashlib.sha256(identifier.encode()).hexdigest()[:16]
        
    async def store_contract(self, contract_data: Dict[str, Any]) -> bool:
        """Store contract data in GitHub repository."""
        if not self.session:
            logger.warning("GitHub storage not initialized")
            return False
            
        try:
            contract_id = self._generate_contract_id(contract_data)
            chain = contract_data.get('chain', 'unknown')
            
            # Add metadata
            contract_data['stored_at'] = datetime.now().isoformat()
            contract_data['contract_id'] = contract_id
            
            # Store contract data
            file_path = f"contracts/{chain}/{contract_id}.json"
            content = json.dumps(contract_data, indent=2)
            commit_message = f"Add contract {contract_data.get('name', 'Unknown')} ({contract_data['address']})"
            
            success = await self._create_file(file_path, content, commit_message)
            
            if success:
                # Update index
                await self._update_contract_index(contract_data)
                logger.info(f"Stored contract {contract_data['address']} in GitHub")
                
            return success
            
        except Exception as e:
            logger.error(f"Error storing contract: {str(e)}")
            return False
            
    async def _update_contract_index(self, contract_data: Dict[str, Any]) -> None:
        """Update contract index for efficient searching."""
        try:
            chain = contract_data.get('chain', 'unknown')
            index_path = f"indexes/{chain}_index.json"
            
            # Get existing index
            existing_content = await self._get_file_content(index_path)
            if existing_content:
                index_data: Dict[str, Any] = json.loads(existing_content)
            else:
                index_data = {'contracts': [], 'last_updated': None}
                
            # Add contract to index
            contract_entry: Dict[str, Any] = {
                'contract_id': contract_data['contract_id'],
                'address': contract_data['address'],
                'name': contract_data.get('name', 'Unknown'),
                'chain': contract_data['chain'],
                'verified_date': contract_data.get('verified_date'),
                'stored_at': contract_data['stored_at']
            }
            
            # Remove existing entry if it exists
            index_data['contracts'] = [
                c for c in index_data['contracts'] 
                if c['address'].lower() != contract_data['address'].lower()
            ]
            
            # Add new entry
            index_data['contracts'].append(contract_entry)
            index_data['last_updated'] = datetime.now().isoformat()
            
            # Store updated index
            content = json.dumps(index_data, indent=2)
            await self._create_file(index_path, content, f"Update {chain} contract index")
            
        except Exception as e:
            logger.error(f"Error updating contract index: {str(e)}")
            
    async def get_contract(self, contract_id: str, chain: str) -> Optional[Dict[str, Any]]:
        """Get contract data by ID."""
        try:
            file_path = f"contracts/{chain}/{contract_id}.json"
            content = await self._get_file_content(file_path)
            
            if content:
                return json.loads(content)
                
        except Exception as e:
            logger.error(f"Error getting contract {contract_id}: {str(e)}")
            
        return None
        
    async def search_contracts(self, 
                             chain: Optional[str] = None,
                             name_filter: Optional[str] = None,
                             address_filter: Optional[str] = None,
                             limit: int = 100) -> List[Dict[str, Any]]:
        """Search contracts with filters."""
        try:
            contracts: List[Dict[str, Any]] = []
            chains_to_search = [chain] if chain else ['ethereum', 'base']
            
            for search_chain in chains_to_search:
                index_path = f"indexes/{search_chain}_index.json"
                content = await self._get_file_content(index_path)
                
                if content:
                    index_data: Dict[str, Any] = json.loads(content)
                    
                    for contract_entry in index_data.get('contracts', []):
                        # Apply filters
                        if name_filter and name_filter.lower() not in contract_entry.get('name', '').lower():
                            continue
                            
                        if address_filter and address_filter.lower() not in contract_entry.get('address', '').lower():
                            continue
                            
                        contracts.append(contract_entry)
                        
                        if len(contracts) >= limit:
                            break
                            
            return contracts[:limit]
            
        except Exception as e:
            logger.error(f"Error searching contracts: {str(e)}")
            return []
            
    async def get_contract_statistics(self) -> Dict[str, Any]:
        """Get storage statistics."""
        try:
            stats: Dict[str, Any] = {
                'total_contracts': 0,
                'chains': {},
                'last_updated': None
            }
            
            for chain in ['ethereum', 'base']:
                index_path = f"indexes/{chain}_index.json"
                content = await self._get_file_content(index_path)
                
                if content:
                    index_data: Dict[str, Any] = json.loads(content)
                    contract_count = len(index_data.get('contracts', []))
                    stats['chains'][chain] = contract_count
                    stats['total_contracts'] += contract_count
                    
                    if index_data.get('last_updated'):
                        if not stats['last_updated'] or index_data['last_updated'] > stats['last_updated']:
                            stats['last_updated'] = index_data['last_updated']
                            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting statistics: {str(e)}")
            return {'total_contracts': 0, 'chains': {}, 'last_updated': None}
            
    async def bulk_store_contracts(self, contracts: List[Dict[str, Any]]) -> int:
        """Store multiple contracts efficiently."""
        if not contracts:
            return 0
            
        stored_count = 0
        
        for contract_data in contracts:
            try:
                if await self.store_contract(contract_data):
                    stored_count += 1
            except Exception as e:
                logger.error(f"Error storing contract {contract_data.get('address', 'unknown')}: {str(e)}")
                
        logger.info(f"Stored {stored_count}/{len(contracts)} contracts in GitHub")
        return stored_count
        
    def is_available(self) -> bool:
        """Check if GitHub storage is available."""
        return bool(self.github_token and self.session)
