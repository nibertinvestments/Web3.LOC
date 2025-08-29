"""
Web3.LOC Main Application - Complete Contract Discovery and Analysis System
Integrates all components for a production-ready blockchain contract discovery platform.
"""

import asyncio
import logging
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from contract_discovery.enhanced_blockchain_client import BlockchainClientManager, ContractData
from contract_discovery.contract_database import ContractDatabase, ContractAnalyzer
from contract_discovery.readme_generator import ContractREADMEGenerator
from contract_discovery.github_storage import GitHubStorageManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('web3_loc.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class Web3LOCSystem:
    """Main system coordinator for Web3.LOC contract discovery platform."""
    
    def __init__(self):
        """Initialize the Web3.LOC system."""
        self.client_manager = None
        self.database = ContractDatabase()
        self.readme_generator = ContractREADMEGenerator()
        self.github_storage = GitHubStorageManager()
        self.is_initialized = False
        
        # Create necessary directories
        self._setup_directories()
    
    def _setup_directories(self):
        """Create necessary directories for the system."""
        directories = [
            './exports',
            './contract_readmes',
            './logs'
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
    
    async def initialize(self):
        """Initialize the system components."""
        try:
            logger.info("Initializing Web3.LOC system...")
            
            # Initialize blockchain client manager
            self.client_manager = BlockchainClientManager()
            await self.client_manager.initialize()
            
            # Initialize GitHub storage
            await self.github_storage.initialize()
            
            # Verify database connection
            self.database.get_statistics()
            
            self.is_initialized = True
            logger.info("Web3.LOC system initialized successfully")
            
            # Log system status
            self._log_system_status()
            
        except Exception as e:
            logger.error(f"Failed to initialize Web3.LOC system: {str(e)}")
            raise
    
    async def discover_contracts(self, 
                               chains: Optional[List[str]] = None,
                               limit_per_chain: int = 20,
                               generate_readmes: bool = True) -> Dict[str, Any]:
        """Discover contracts from specified chains.
        
        Args:
            chains: List of chain names to scan (None for all available)
            limit_per_chain: Number of contracts to discover per chain
            generate_readmes: Whether to generate README files for contracts
            
        Returns:
            Discovery results summary
        """
        if not self.is_initialized:
            await self.initialize()
        
        logger.info(f"Starting contract discovery: {limit_per_chain} contracts per chain")
        
        try:
            # Get contracts from blockchain clients
            if not self.client_manager:
                raise Exception("Client manager not initialized")
                
            contracts = await self.client_manager.get_all_verified_contracts(
                limit_per_chain=limit_per_chain
            )
            
            if not contracts:
                logger.warning("No contracts discovered")
                return {
                    'success': False,
                    'message': 'No contracts found',
                    'contracts_processed': 0,
                    'contracts_added': 0,
                    'duplicates_found': 0,
                    'errors': 0
                }
            
            # Process and store contracts
            results = await self._process_contracts(contracts, generate_readmes)
            
            logger.info(f"Discovery completed: {results['contracts_added']} new contracts added")
            return results
            
        except Exception as e:
            logger.error(f"Contract discovery failed: {str(e)}")
            return {
                'success': False,
                'message': f'Discovery failed: {str(e)}',
                'contracts_processed': 0,
                'contracts_added': 0,
                'duplicates_found': 0,
                'errors': 1
            }
    
    async def _process_contracts(self, 
                               contracts: List[ContractData], 
                               generate_readmes: bool) -> Dict[str, Any]:
        """Process discovered contracts and store them in database.
        
        Args:
            contracts: List of discovered contracts
            generate_readmes: Whether to generate README files
            
        Returns:
            Processing results
        """
        results: Dict[str, Any] = {
            'success': True,
            'contracts_processed': len(contracts),
            'contracts_added': 0,
            'duplicates_found': 0,
            'errors': 0,
            'readme_files': []
        }
        
        for contract in contracts:
            try:
                # Generate contract analysis and summary
                summary = ContractAnalyzer.analyze_contract(contract)
                
                # Try to insert into database
                if self.database.insert_contract(contract, summary):
                    results['contracts_added'] += 1
                    logger.info(f"Added contract: {contract.name} ({contract.address[:10]}...)")
                    
                    # Store in GitHub if available
                    if self.github_storage.is_available():
                        try:
                            contract_data = contract.to_dict()
                            contract_data['summary'] = summary
                            await self.github_storage.store_contract(contract_data)
                            logger.info(f"Stored contract {contract.name} in GitHub")
                        except Exception as e:
                            logger.error(f"Failed to store contract {contract.name} in GitHub: {str(e)}")
                    
                    # Generate README if requested
                    if generate_readmes:
                        try:
                            readme_path = self.readme_generator.generate_readme(contract, summary)
                            results['readme_files'].append(readme_path)
                            logger.info(f"Generated README: {readme_path}")
                        except Exception as e:
                            logger.error(f"Failed to generate README for {contract.name}: {str(e)}")
                else:
                    results['duplicates_found'] += 1
                    logger.info(f"Duplicate contract skipped: {contract.name} ({contract.address[:10]}...)")
                    
            except Exception as e:
                results['errors'] += 1
                logger.error(f"Error processing contract {contract.address}: {str(e)}")
        
        return results
    
    def search_contracts(self, 
                        query: str, 
                        filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Search contracts in the database.
        
        Args:
            query: Search query string
            filters: Optional filters to apply
            
        Returns:
            List of matching contracts
        """
        if not filters:
            return self.database.search_contracts(query)
        else:
            return self.database.filter_contracts(**filters)
    
    def export_contracts(self, 
                        filename: Optional[str] = None,
                        filters: Optional[Dict[str, Any]] = None) -> str:
        """Export contracts to CSV file.
        
        Args:
            filename: Output filename (auto-generated if None)
            filters: Optional filters to apply
            
        Returns:
            Path to exported file
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"./exports/contracts_export_{timestamp}.csv"
        
        # Apply filters if provided
        if filters:
            # This would require extending the database export method
            # For now, export all contracts
            pass
        
        if self.database.export_to_csv(filename):
            logger.info(f"Contracts exported to: {filename}")
            return filename
        else:
            raise Exception("Export failed")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get comprehensive system statistics.
        
        Returns:
            System statistics
        """
        stats = self.database.get_statistics()
        
        # Add system-specific stats
        if self.client_manager:
            stats['available_chains'] = self.client_manager.get_available_chains()
            stats['client_status'] = len(self.client_manager.clients)
        
        stats['system_initialized'] = self.is_initialized
        stats['last_updated'] = datetime.now().isoformat()
        
        return stats
    
    def _log_system_status(self):
        """Log current system status."""
        if self.client_manager:
            chains = self.client_manager.get_available_chains()
            logger.info(f"Connected to {len(chains)} blockchain clients: {', '.join(chains)}")
        
        stats = self.database.get_statistics()
        total_contracts = stats.get('total_contracts', 0)
        logger.info(f"Database contains {total_contracts} contracts")
    
    async def cleanup(self):
        """Clean up system resources."""
        if self.client_manager:
            await self.client_manager.cleanup()
        if self.github_storage:
            await self.github_storage.cleanup()
        logger.info("Web3.LOC system cleaned up")

class Web3LOCCLIInterface:
    """Command-line interface for Web3.LOC system."""
    
    def __init__(self):
        """Initialize CLI interface."""
        self.system = Web3LOCSystem()
    
    async def run_interactive(self):
        """Run interactive CLI mode."""
        print("🔍 Web3.LOC - Smart Contract Discovery Platform")
        print("=" * 50)
        
        try:
            await self.system.initialize()
            print("✅ System initialized successfully")
            
            while True:
                print("\nAvailable commands:")
                print("1. Discover contracts")
                print("2. Search contracts")
                print("3. Export contracts")
                print("4. Show statistics")
                print("5. Exit")
                
                choice = input("\nEnter your choice (1-5): ").strip()
                
                if choice == "1":
                    await self._handle_discovery()
                elif choice == "2":
                    await self._handle_search()
                elif choice == "3":
                    await self._handle_export()
                elif choice == "4":
                    await self._handle_statistics()
                elif choice == "5":
                    print("Goodbye! 👋")
                    break
                else:
                    print("Invalid choice. Please try again.")
                    
        except KeyboardInterrupt:
            print("\n\nShutting down...")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        finally:
            await self.system.cleanup()
    
    async def _handle_discovery(self):
        """Handle contract discovery command."""
        print("\n🔍 Contract Discovery")
        
        try:
            # Get discovery parameters
            limit = input("Contracts per chain (default: 10): ").strip()
            if not limit:
                limit = 10
            else:
                limit = int(limit)
            
            generate_readmes = input("Generate README files? (y/n, default: y): ").strip().lower()
            generate_readmes = generate_readmes != 'n'
            
            print(f"\nDiscovering {limit} contracts per chain...")
            print("This may take a few minutes...")
            
            results = await self.system.discover_contracts(
                limit_per_chain=limit,
                generate_readmes=generate_readmes
            )
            
            if results['success']:
                print(f"✅ Discovery completed!")
                print(f"   Contracts processed: {results['contracts_processed']}")
                print(f"   New contracts added: {results['contracts_added']}")
                print(f"   Duplicates found: {results['duplicates_found']}")
                print(f"   Errors: {results['errors']}")
                
                if generate_readmes and results.get('readme_files'):
                    print(f"   README files generated: {len(results['readme_files'])}")
            else:
                print(f"❌ Discovery failed: {results['message']}")
                
        except ValueError:
            print("❌ Invalid number format")
        except Exception as e:
            print(f"❌ Discovery error: {str(e)}")
    
    async def _handle_search(self):
        """Handle contract search command."""
        print("\n🔎 Search Contracts")
        
        query = input("Enter search query: ").strip()
        if not query:
            print("❌ Search query cannot be empty")
            return
        
        try:
            results = self.system.search_contracts(query)
            
            if results:
                print(f"\n✅ Found {len(results)} contracts:")
                for i, contract in enumerate(results[:10], 1):  # Show first 10
                    print(f"{i}. {contract['name']} on {contract['chain']} ({contract['address'][:10]}...)")
                
                if len(results) > 10:
                    print(f"... and {len(results) - 10} more")
            else:
                print("❌ No contracts found matching your query")
                
        except Exception as e:
            print(f"❌ Search error: {str(e)}")
    
    async def _handle_export(self):
        """Handle contract export command."""
        print("\n📥 Export Contracts")
        
        try:
            filename = self.system.export_contracts()
            print(f"✅ Contracts exported to: {filename}")
            
        except Exception as e:
            print(f"❌ Export error: {str(e)}")
    
    async def _handle_statistics(self):
        """Handle statistics display command."""
        print("\n📊 System Statistics")
        
        try:
            stats = self.system.get_statistics()
            
            print(f"Total contracts: {stats.get('total_contracts', 0)}")
            print(f"Available chains: {len(stats.get('available_chains', []))}")
            
            if stats.get('by_chain'):
                print("\nContracts by chain:")
                for chain, count in stats['by_chain'].items():
                    print(f"  {chain}: {count}")
            
            if stats.get('top_compilers'):
                print("\nTop compiler versions:")
                for compiler, count in list(stats['top_compilers'].items())[:5]:
                    print(f"  {compiler}: {count}")
                    
        except Exception as e:
            print(f"❌ Statistics error: {str(e)}")

async def main():
    """Main entry point for the application."""
    if len(sys.argv) > 1:
        # Command-line mode with arguments
        command = sys.argv[1].lower()
        
        system = Web3LOCSystem()
        
        try:
            if command == "discover":
                limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
                results = await system.discover_contracts(limit_per_chain=limit)
                print(f"Discovery completed: {results['contracts_added']} new contracts")
                
            elif command == "export":
                filename = sys.argv[2] if len(sys.argv) > 2 else None
                exported_file = system.export_contracts(filename)
                print(f"Exported to: {exported_file}")
                
            elif command == "stats":
                stats = system.get_statistics()
                print(f"Total contracts: {stats.get('total_contracts', 0)}")
                
            else:
                print("Unknown command. Use: discover, export, or stats")
                
        except Exception as e:
            print(f"Error: {str(e)}")
        finally:
            await system.cleanup()
    else:
        # Interactive mode
        cli = Web3LOCCLIInterface()
        await cli.run_interactive()

if __name__ == "__main__":
    # Run the application
    asyncio.run(main())
