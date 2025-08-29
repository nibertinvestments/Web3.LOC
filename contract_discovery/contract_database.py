"""
Advanced database manager for Web3.LOC contract storage and analysis.
Supports SQLite with advanced querying, filtering, and export capabilities.
"""

import sqlite3
import csv
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path

from .enhanced_blockchain_client import ContractData

logger = logging.getLogger(__name__)

class ContractDatabase:
    """Advanced contract database with comprehensive features."""
    
    def __init__(self, db_path: str = "./data/contracts.db"):
        """Initialize the database."""
        self.db_path = db_path
        
        # Ensure data directory exists
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        
        self.conn: Optional[sqlite3.Connection] = None
        self._initialize_database()
        
    def _initialize_database(self) -> None:
        """Initialize database tables."""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row  # Enable dict-like access
            
            # Create comprehensive contracts table
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS contracts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    address TEXT NOT NULL,
                    name TEXT NOT NULL,
                    source_code TEXT NOT NULL,
                    bytecode TEXT NOT NULL,
                    compiler_version TEXT,
                    optimization BOOLEAN,
                    runs INTEGER,
                    constructor_arguments TEXT,
                    abi TEXT,
                    creation_txhash TEXT,
                    block_number INTEGER,
                    chain TEXT NOT NULL,
                    chain_id INTEGER,
                    verified_date TEXT,
                    bytecode_hash TEXT UNIQUE,
                    source_hash TEXT UNIQUE,
                    contract_summary TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create indexes for performance
            self.conn.execute("CREATE INDEX IF NOT EXISTS idx_address ON contracts(address)")
            self.conn.execute("CREATE INDEX IF NOT EXISTS idx_chain ON contracts(chain)")
            self.conn.execute("CREATE INDEX IF NOT EXISTS idx_name ON contracts(name)")
            self.conn.execute("CREATE INDEX IF NOT EXISTS idx_bytecode_hash ON contracts(bytecode_hash)")
            self.conn.execute("CREATE INDEX IF NOT EXISTS idx_source_hash ON contracts(source_hash)")
            
            # Create contract tags table for categorization
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS contract_tags (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    contract_id INTEGER,
                    tag TEXT,
                    FOREIGN KEY(contract_id) REFERENCES contracts(id)
                )
            """)
            
            self.conn.commit()
            logger.info("Database initialized successfully")
            
        except Exception as e:
            logger.error(f"Database initialization failed: {str(e)}")
            raise
    
    def insert_contract(self, contract: ContractData, summary: str = "") -> bool:
        """Insert a new contract into the database."""
        try:
            if not self.conn:
                return False
                
            # Check if contract already exists (by bytecode hash or source hash)
            existing = self.conn.execute(
                "SELECT id FROM contracts WHERE bytecode_hash = ? OR source_hash = ?",
                (contract.bytecode_hash, contract.source_hash)
            ).fetchone()
            
            if existing:
                logger.debug(f"Contract {contract.address} already exists in database")
                return False
            
            # Insert new contract
            self.conn.execute("""
                INSERT INTO contracts (
                    address, name, source_code, bytecode, compiler_version,
                    optimization, runs, constructor_arguments, abi, creation_txhash,
                    block_number, chain, chain_id, verified_date, bytecode_hash,
                    source_hash, contract_summary
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                contract.address, contract.name, contract.source_code, contract.bytecode,
                contract.compiler_version, contract.optimization, contract.runs,
                contract.constructor_arguments, contract.abi, contract.creation_txhash,
                contract.block_number, contract.chain, contract.chain_id,
                contract.verified_date, contract.bytecode_hash, contract.source_hash,
                summary
            ))
            
            self.conn.commit()
            logger.info(f"Inserted contract: {contract.name} ({contract.address})")
            return True
            
        except Exception as e:
            logger.error(f"Failed to insert contract {contract.address}: {str(e)}")
            return False
    
    def get_contracts(self, 
                     filters: Optional[Dict[str, Any]] = None,
                     limit: Optional[int] = None,
                     offset: int = 0) -> List[Dict[str, Any]]:
        """Get contracts with optional filtering."""
        try:
            if not self.conn:
                return []
            
            query = "SELECT * FROM contracts WHERE 1=1"
            params: List[Any] = []
            
            # Apply filters
            if filters:
                if 'chain' in filters:
                    query += " AND chain = ?"
                    params.append(filters['chain'])
                    
                if 'name' in filters:
                    query += " AND name LIKE ?"
                    params.append(f"%{filters['name']}%")
                    
                if 'compiler_version' in filters:
                    query += " AND compiler_version LIKE ?"
                    params.append(f"%{filters['compiler_version']}%")
                    
                if 'optimization' in filters:
                    query += " AND optimization = ?"
                    params.append(filters['optimization'])
                    
                if 'address' in filters:
                    query += " AND address = ?"
                    params.append(filters['address'])
            
            # Add ordering and limits
            query += " ORDER BY created_at DESC"
            
            if limit:
                query += " LIMIT ?"
                params.append(limit)
                
            if offset:
                query += " OFFSET ?"
                params.append(offset)
            
            cursor = self.conn.execute(query, params)
            contracts = [dict(row) for row in cursor.fetchall()]
            
            logger.debug(f"Retrieved {len(contracts)} contracts with filters: {filters}")
            return contracts
            
        except Exception as e:
            logger.error(f"Failed to get contracts: {str(e)}")
            return []
    
    def filter_contracts(self, **filters: Any) -> List[Dict[str, Any]]:
        """Filter contracts by various criteria.
        
        Args:
            **filters: Filter criteria
            
        Returns:
            List of matching contracts
        """
        return self.get_contracts(filters=filters)
    
    def get_contract_by_address(self, address: str) -> Optional[Dict[str, Any]]:
        """Get a specific contract by address."""
        try:
            if not self.conn:
                return None
                
            cursor = self.conn.execute(
                "SELECT * FROM contracts WHERE address = ?", (address,)
            )
            row = cursor.fetchone()
            return dict(row) if row else None
            
        except Exception as e:
            logger.error(f"Failed to get contract {address}: {str(e)}")
            return None
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get database statistics."""
        try:
            if not self.conn:
                return {}
            
            stats: Dict[str, Any] = {}
            
            # Total contracts
            cursor = self.conn.execute("SELECT COUNT(*) as total FROM contracts")
            stats['total_contracts'] = cursor.fetchone()['total']
            
            # Contracts by chain
            cursor = self.conn.execute("""
                SELECT chain, COUNT(*) as count 
                FROM contracts 
                GROUP BY chain
            """)
            stats['by_chain'] = {row['chain']: row['count'] for row in cursor.fetchall()}
            
            # Optimization usage
            cursor = self.conn.execute("""
                SELECT optimization, COUNT(*) as count 
                FROM contracts 
                GROUP BY optimization
            """)
            stats['optimization_usage'] = {
                bool(row['optimization']): row['count'] for row in cursor.fetchall()
            }
            
            # Top compiler versions
            cursor = self.conn.execute("""
                SELECT compiler_version, COUNT(*) as count 
                FROM contracts 
                GROUP BY compiler_version 
                ORDER BY count DESC 
                LIMIT 10
            """)
            stats['top_compilers'] = {
                row['compiler_version']: row['count'] for row in cursor.fetchall()
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Failed to get statistics: {str(e)}")
            return {}
    
    def export_to_csv(self, filename: str, filters: Optional[Dict[str, Any]] = None) -> bool:
        """Export contracts to CSV file."""
        try:
            contracts = self.get_contracts(filters)
            
            if not contracts:
                logger.warning("No contracts to export")
                return False
            
            # Ensure exports directory exists
            Path(filename).parent.mkdir(parents=True, exist_ok=True)
            
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = [
                    'address', 'name', 'chain', 'compiler_version', 'optimization',
                    'runs', 'block_number', 'verified_date', 'contract_summary',
                    'bytecode_hash', 'source_hash'
                ]
                
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for contract in contracts:
                    # Select only the fields we want to export
                    export_data = {field: contract.get(field, '') for field in fieldnames}
                    writer.writerow(export_data)
            
            logger.info(f"Exported {len(contracts)} contracts to {filename}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to export to CSV: {str(e)}")
            return False
    
    def search_contracts(self, search_term: str) -> List[Dict[str, Any]]:
        """Search contracts by name, address, or summary."""
        try:
            if not self.conn:
                return []
            
            query = """
                SELECT * FROM contracts 
                WHERE name LIKE ? 
                   OR address LIKE ? 
                   OR contract_summary LIKE ?
                ORDER BY created_at DESC
            """
            
            term = f"%{search_term}%"
            cursor = self.conn.execute(query, (term, term, term))
            contracts = [dict(row) for row in cursor.fetchall()]
            
            logger.debug(f"Search for '{search_term}' returned {len(contracts)} results")
            return contracts
            
        except Exception as e:
            logger.error(f"Search failed: {str(e)}")
            return []
    
    def update_contract_summary(self, address: str, summary: str) -> bool:
        """Update contract summary."""
        try:
            if not self.conn:
                return False
                
            self.conn.execute(
                "UPDATE contracts SET contract_summary = ?, updated_at = CURRENT_TIMESTAMP WHERE address = ?",
                (summary, address)
            )
            self.conn.commit()
            
            logger.info(f"Updated summary for contract {address}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update summary for {address}: {str(e)}")
            return False
    
    def close(self) -> None:
        """Close database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None
            logger.info("Database connection closed")

class ContractAnalyzer:
    """Analyzes contracts and generates summaries."""
    
    @staticmethod
    def analyze_contract(contract_data: ContractData) -> str:
        """Analyze contract and generate a summary."""
        try:
            source_code = contract_data.source_code.lower()
            name = contract_data.name
            
            # Basic analysis based on common patterns
            analysis_parts: List[str] = []
            
            # Contract type detection
            if 'erc20' in source_code or 'transfer' in source_code and 'balanceof' in source_code:
                analysis_parts.append("ERC-20 Token Contract")
            elif 'erc721' in source_code or 'nft' in source_code:
                analysis_parts.append("ERC-721 NFT Contract")
            elif 'erc1155' in source_code:
                analysis_parts.append("ERC-1155 Multi-Token Contract")
            elif 'proxy' in source_code or 'implementation' in source_code:
                analysis_parts.append("Proxy Contract")
            elif 'multisig' in source_code or 'multisignature' in source_code:
                analysis_parts.append("Multi-Signature Wallet")
            elif 'swap' in source_code or 'uniswap' in source_code or 'dex' in source_code:
                analysis_parts.append("DEX/Swap Contract")
            elif 'staking' in source_code or 'reward' in source_code:
                analysis_parts.append("Staking/Rewards Contract")
            elif 'governance' in source_code or 'voting' in source_code:
                analysis_parts.append("Governance Contract")
            else:
                analysis_parts.append("Smart Contract")
            
            # Security features
            security_features: List[str] = []
            if 'onlyowner' in source_code or 'owner' in source_code:
                security_features.append("owner-restricted functions")
            if 'pause' in source_code:
                security_features.append("pausable functionality")
            if 'reentrancy' in source_code or 'nonreentrant' in source_code:
                security_features.append("reentrancy protection")
            if 'timelock' in source_code:
                security_features.append("timelock mechanisms")
            
            if security_features:
                analysis_parts.append(f"Security features: {', '.join(security_features)}")
            
            # Technical details
            tech_details: List[str] = []
            if contract_data.optimization:
                tech_details.append(f"optimized with {contract_data.runs} runs")
            
            tech_details.append(f"deployed on {contract_data.chain}")
            tech_details.append(f"compiled with {contract_data.compiler_version}")
            
            analysis_parts.append(f"Technical: {', '.join(tech_details)}")
            
            # Function count estimation
            func_count = source_code.count('function ')
            if func_count > 0:
                analysis_parts.append(f"Contains ~{func_count} functions")
            
            summary = f"{name}: {'. '.join(analysis_parts)}."
            
            return summary[:500]  # Limit summary length
            
        except Exception as e:
            logger.error(f"Contract analysis failed: {str(e)}")
            return f"{contract_data.name}: Smart contract deployed on {contract_data.chain}"
