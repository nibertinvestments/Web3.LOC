"""
Web3.LOC GitHub Storage Manager - Python Version
Centralized public storage for smart contract discovery
Compatible with mobile app development using Kivy/BeeWare
"""

import aiohttp
import asyncio
import json
import csv
import io
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import logging

class GitHubStorage:
    """
    Python version of GitHub Storage Manager
    Same parameters and functionality as JavaScript version
    """
    
    def __init__(self):
        self.base_url = 'https://api.github.com'
        self.repo = 'Web3LOC/contract-storage'
        self.raw_base = 'https://raw.githubusercontent.com/Web3LOC/contract-storage/main'
        self.cache = {}
        self.is_online = False
        self.session = None
        
    async def initialize(self):
        """Initialize HTTP session"""
        if not self.session:
            self.session = aiohttp.ClientSession()
    
    async def close(self):
        """Close HTTP session"""
        if self.session:
            await self.session.close()
            self.session = None
    
    async def test_connection(self) -> Dict[str, Any]:
        """Test GitHub connection"""
        try:
            await self.initialize()
            
            async with self.session.get(
                f"{self.base_url}/repos/{self.repo}",
                headers={'Accept': 'application/vnd.github.v3+json'}
            ) as response:
                
                if not response.ok:
                    raise Exception(f"GitHub API error: {response.status} {response.reason}")
                
                self.is_online = True
                return await response.json()
                
        except Exception as error:
            self.is_online = False
            logging.error(f"Connection test failed: {error}")
            raise error
    
    async def search_contracts(self, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Search contracts in centralized repository
        Same parameters as JavaScript version
        """
        if filters is None:
            filters = {}
            
        try:
            index = await self.get_contract_index()
            contracts = index.get('contracts', [])
            
            # Apply chain filter
            if filters.get('chain'):
                contracts = [c for c in contracts if c.get('chain') == filters['chain']]
            
            # Apply name filter
            if filters.get('name_filter'):
                search_term = filters['name_filter'].lower()
                contracts = [
                    c for c in contracts 
                    if search_term in str(c.get('name', '')).lower() 
                    or search_term in str(c.get('address', '')).lower()
                ]
            
            # Apply address filter
            if filters.get('address_filter'):
                address_filter = filters['address_filter'].lower()
                contracts = [
                    c for c in contracts 
                    if address_filter in str(c.get('address', '')).lower()
                ]
            
            # Apply type filter
            if filters.get('type'):
                contracts = [c for c in contracts if c.get('type') == filters['type']]
            
            # Apply date range filter
            if filters.get('date_range'):
                now = datetime.now()
                cutoff_date = None
                
                if filters['date_range'] == '24h':
                    cutoff_date = now - timedelta(hours=24)
                elif filters['date_range'] == '7d':
                    cutoff_date = now - timedelta(days=7)
                elif filters['date_range'] == '30d':
                    cutoff_date = now - timedelta(days=30)
                
                if cutoff_date:
                    contracts = [
                        c for c in contracts 
                        if c.get('stored_at') and 
                        datetime.fromisoformat(c['stored_at'].replace('Z', '+00:00')) >= cutoff_date
                    ]
            
            # Apply limit
            limit = min(filters.get('limit', 50), 500)
            contracts = contracts[:limit]
            
            return contracts
            
        except Exception as error:
            logging.error(f"Error searching contracts: {error}")
            return []
    
    async def get_contract(self, contract_id: str, chain: str) -> Optional[Dict[str, Any]]:
        """Get a specific contract"""
        cache_key = f"{chain}_{contract_id}"
        
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        try:
            await self.initialize()
            
            url = f"{self.raw_base}/contracts/{chain}/contract_{contract_id}.json"
            async with self.session.get(url) as response:
                
                if not response.ok:
                    return None
                
                contract_data = await response.json()
                self.cache[cache_key] = contract_data
                return contract_data
                
        except Exception as error:
            logging.error(f"Error getting contract: {error}")
            return None
    
    async def get_contract_statistics(self) -> Dict[str, Any]:
        """Get contract statistics"""
        try:
            await self.initialize()
            
            url = f"{self.raw_base}/index/statistics.json"
            async with self.session.get(url) as response:
                
                if response.ok:
                    return await response.json()
                else:
                    index = await self.get_contract_index()
                    return index.get('statistics', {
                        'total_contracts': 0,
                        'chains': {'ethereum': 0, 'base': 0},
                        'last_updated': None
                    })
                    
        except Exception:
            return {
                'total_contracts': 0,
                'chains': {'ethereum': 0, 'base': 0},
                'last_updated': None
            }
    
    async def get_contract_index(self) -> Dict[str, Any]:
        """Get contract index"""
        try:
            await self.initialize()
            
            url = f"{self.raw_base}/index/contract_index.json"
            async with self.session.get(url) as response:
                
                if response.ok:
                    return await response.json()
                else:
                    return {
                        'contracts': [],
                        'statistics': {
                            'total_contracts': 0,
                            'chains': {'ethereum': 0, 'base': 0},
                            'last_updated': None
                        }
                    }
                    
        except Exception:
            return {
                'contracts': [],
                'statistics': {
                    'total_contracts': 0,
                    'chains': {'ethereum': 0, 'base': 0},
                    'last_updated': None
                }
            }
    
    async def get_recent_contracts(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent contracts"""
        try:
            contracts = await self.search_contracts({'limit': limit})
            
            # Sort by stored_at date
            contracts.sort(
                key=lambda x: datetime.fromisoformat(x.get('stored_at', '1970-01-01T00:00:00Z').replace('Z', '+00:00')),
                reverse=True
            )
            
            return contracts[:limit]
            
        except Exception:
            return []
    
    async def export_contracts_csv(self, filters: Optional[Dict[str, Any]] = None) -> str:
        """Export contracts as CSV string"""
        if filters is None:
            filters = {}
            
        try:
            contracts = await self.search_contracts(filters)
            
            if not contracts:
                raise Exception('No contracts found to export')
            
            # Create CSV content
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Headers
            headers = [
                'Address', 'Chain', 'Name', 'Type', 'Verified',
                'Compiler', 'Optimized', 'Stored Date'
            ]
            writer.writerow(headers)
            
            # Data rows
            for contract in contracts:
                row = [
                    contract.get('address', ''),
                    contract.get('chain', ''),
                    contract.get('name', 'Unknown'),
                    contract.get('type', 'other'),
                    'Yes' if contract.get('verified') else 'No',
                    contract.get('compiler_version', 'Unknown'),
                    'Yes' if contract.get('optimization') else 'No',
                    datetime.fromisoformat(contract.get('stored_at', '1970-01-01T00:00:00Z').replace('Z', '+00:00')).strftime('%Y-%m-%d') if contract.get('stored_at') else ''
                ]
                writer.writerow(row)
            
            return output.getvalue()
            
        except Exception as error:
            raise error
    
    async def export_contract_sol(self, contract_id: str, chain: str) -> str:
        """Export contract as Solidity file"""
        try:
            contract = await self.get_contract(contract_id, chain)
            
            if not contract:
                raise Exception('Contract not found')
            
            header = f"""// SPDX-License-Identifier: MIT
// Contract discovered by Web3.LOC
// Network: {contract.get('chain', 'Unknown')}
// Address: {contract.get('address', 'Unknown')}
// Name: {contract.get('name', 'Unknown')}

"""
            
            return header + contract.get('source_code', '')
            
        except Exception as error:
            raise error
    
    async def export_contract_readme(self, contract_id: str, chain: str) -> str:
        """Export contract as README file"""
        try:
            contract = await self.get_contract(contract_id, chain)
            
            if not contract:
                raise Exception('Contract not found')
            
            chain_name = contract.get('chain', 'unknown').capitalize()
            name = contract.get('name', 'Unknown')
            address = contract.get('address', 'Unknown')
            contract_type = contract.get('type', 'Unknown')
            verified = 'Yes' if contract.get('verified') else 'No'
            compiler = contract.get('compiler_version', 'Unknown')
            optimized = 'Yes' if contract.get('optimization') else 'No'
            summary = contract.get('summary', 'No summary available')
            source_code = contract.get('source_code', 'Source code not available')
            abi = contract.get('abi', '[]')
            
            readme = f"""# {name}

## Contract Information
- **Address**: {address}
- **Network**: {chain_name}
- **Type**: {contract_type}
- **Verified**: {verified}
- **Compiler**: {compiler}
- **Optimized**: {optimized}

## Summary
{summary}

## Source Code
```solidity
{source_code}
```

## ABI
```json
{abi}
```

---
*Generated by Web3.LOC - Smart Contract Discovery Platform*
"""
            
            return readme
            
        except Exception as error:
            raise error
    
    def save_file(self, content: str, filename: str, file_path: str = './'):
        """Save content to file"""
        full_path = f"{file_path}{filename}"
        
        try:
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return full_path
        except Exception as error:
            logging.error(f"Error saving file: {error}")
            raise error
    
    async def get_analytics_data(self) -> Dict[str, Any]:
        """Get analytics data"""
        try:
            index = await self.get_contract_index()
            contracts = index.get('contracts', [])
            
            analytics = {
                'total': len(contracts),
                'by_chain': {},
                'by_type': {},
                'by_date': {},
                'verification_rate': 0
            }
            
            # Count by chain
            for contract in contracts:
                chain = contract.get('chain', 'unknown')
                analytics['by_chain'][chain] = analytics['by_chain'].get(chain, 0) + 1
            
            # Count by type
            for contract in contracts:
                contract_type = contract.get('type', 'other')
                analytics['by_type'][contract_type] = analytics['by_type'].get(contract_type, 0) + 1
            
            # Count by date (last 30 days)
            now = datetime.now()
            last_30_days = {}
            
            for i in range(30):
                date = now - timedelta(days=i)
                date_str = date.strftime('%Y-%m-%d')
                last_30_days[date_str] = 0
            
            for contract in contracts:
                if contract.get('stored_at'):
                    try:
                        stored_date = datetime.fromisoformat(contract['stored_at'].replace('Z', '+00:00'))
                        date_str = stored_date.strftime('%Y-%m-%d')
                        if date_str in last_30_days:
                            last_30_days[date_str] += 1
                    except:
                        pass
            
            analytics['by_date'] = last_30_days
            
            # Calculate verification rate
            verified_count = sum(1 for c in contracts if c.get('verified'))
            analytics['verification_rate'] = round((verified_count / len(contracts)) * 100) if contracts else 0
            
            return analytics
            
        except Exception:
            return {
                'total': 0,
                'by_chain': {},
                'by_type': {},
                'by_date': {},
                'verification_rate': 0
            }


# Example usage for mobile apps
async def main():
    """Example usage of the Python GitHub Storage"""
    storage = GitHubStorage()
    
    try:
        # Test connection
        print("Testing connection...")
        repo_info = await storage.test_connection()
        print(f"Connected to: {repo_info.get('full_name')}")
        
        # Search contracts
        print("\nSearching contracts...")
        contracts = await storage.search_contracts({
            'chain': 'ethereum',
            'limit': 5
        })
        print(f"Found {len(contracts)} contracts")
        
        # Get statistics
        print("\nGetting statistics...")
        stats = await storage.get_contract_statistics()
        print(f"Total contracts: {stats.get('total_contracts', 0)}")
        
        # Export CSV (first 10 contracts)
        print("\nExporting CSV...")
        csv_content = await storage.export_contracts_csv({'limit': 10})
        storage.save_file(csv_content, 'contracts_export.csv')
        print("CSV exported successfully")
        
        # Get specific contract and export as .sol
        if contracts:
            contract = contracts[0]
            contract_id = contract['address']
            chain = contract['chain']
            
            print(f"\nExporting contract {contract_id} as .sol file...")
            sol_content = await storage.export_contract_sol(contract_id, chain)
            storage.save_file(sol_content, f'{contract_id}.sol')
            print("Solidity file exported successfully")
        
    finally:
        await storage.close()


if __name__ == '__main__':
    asyncio.run(main())
