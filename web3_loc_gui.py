"""
Web3.LOC - Modern Web Interface for Contract Discovery and Analysis
A comprehensive GUI for exploring, filtering, and analyzing smart contracts.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Any
import os

# Import our modules
from contract_discovery.enhanced_blockchain_client import BlockchainClientManager
from contract_discovery.contract_database import ContractDatabase, ContractAnalyzer
from contract_discovery.github_storage import GitHubStorageManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure Streamlit page
st.set_page_config(
    page_title="Web3.LOC - Contract Discovery Platform",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    
    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

class Web3LOCApp:
    """Main application class for Web3.LOC interface."""
    
    def __init__(self):
        """Initialize the application."""
        self.db = ContractDatabase()
        self.client_manager = None
        self.github_storage = GitHubStorageManager()
        
    def run(self):
        """Run the main application."""
        st.markdown('<h1 class="main-header">🔍 Web3.LOC</h1>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Smart Contract Discovery & Analysis Platform</p>', unsafe_allow_html=True)
        
        # Sidebar navigation
        st.sidebar.title("Navigation")
        page = st.sidebar.radio(
            "Select Page",
            ["🏠 Dashboard", "🔍 Discovery", "📊 Analytics", "🔎 Search", "⚙️ Settings"]
        )
        
        # Route to appropriate page
        if page == "🏠 Dashboard":
            self.show_dashboard()
        elif page == "🔍 Discovery":
            self.show_discovery()
        elif page == "📊 Analytics":
            self.show_analytics()
        elif page == "🔎 Search":
            self.show_search()
        elif page == "⚙️ Settings":
            self.show_settings()
    
    def show_dashboard(self):
        """Show main dashboard with statistics and recent contracts."""
        st.header("📊 Dashboard")
        
        # Get database statistics
        stats = self.db.get_statistics()
        
        if not stats:
            st.warning("No contract data available. Use the Discovery page to scan for contracts.")
            return
        
        # Display key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Total Contracts",
                value=stats.get('total_contracts', 0),
                delta=None
            )
        
        with col2:
            chain_count = len(stats.get('by_chain', {}))
            st.metric(
                label="Active Chains",
                value=chain_count,
                delta=None
            )
        
        with col3:
            optimized_count = stats.get('optimization_usage', {}).get(True, 0)
            total_count = stats.get('total_contracts', 0)
            optimization_rate = f"{(optimized_count/total_count*100):.1f}%" if total_count > 0 else "0%"
            st.metric(
                label="Optimization Rate",
                value=optimization_rate,
                delta=None
            )
        
        with col4:
            compiler_count = len(stats.get('top_compilers', {}))
            st.metric(
                label="Compiler Versions",
                value=compiler_count,
                delta=None
            )
        
        # Charts section
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Contracts by Chain")
            if stats.get('by_chain'):
                chain_data = stats['by_chain']
                fig = px.pie(
                    values=list(chain_data.values()),
                    names=list(chain_data.keys()),
                    title="Distribution of Contracts by Blockchain"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Top Compiler Versions")
            if stats.get('top_compilers'):
                compiler_data = stats['top_compilers']
                fig = px.bar(
                    x=list(compiler_data.values()),
                    y=list(compiler_data.keys()),
                    orientation='h',
                    title="Most Used Solidity Compilers"
                )
                fig.update_layout(yaxis={'categoryorder':'total ascending'})
                st.plotly_chart(fig, use_container_width=True)
        
        # Recent contracts
        st.subheader("Recent Contracts")
        recent_contracts = self.db.get_contracts(limit=10)
        
        if recent_contracts:
            df = pd.DataFrame(recent_contracts)
            display_columns = ['name', 'chain', 'address', 'compiler_version', 'verified_date']
            df_display = df[display_columns].copy()
            df_display['address'] = df_display['address'].apply(lambda x: f"{x[:10]}...{x[-8:]}" if isinstance(x, str) else str(x))
            df_display['verified_date'] = pd.to_datetime(df_display['verified_date']).dt.strftime('%Y-%m-%d %H:%M')
            
            st.dataframe(df_display, use_container_width=True)
        else:
            st.info("No contracts found. Start discovering contracts to see them here.")
    
    def show_discovery(self):
        """Show contract discovery interface."""
        st.header("🔍 Contract Discovery")
        
        st.markdown("""
        Discover and analyze new smart contracts from supported blockchains.
        The system will automatically deduplicate contracts based on bytecode and source code.
        """)
        
        # Discovery configuration
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Discovery Settings")
            
            # Chain selection
            available_chains = ["ethereum", "base"]
            selected_chains = st.multiselect(
                "Select Chains",
                available_chains,
                default=available_chains,
                help="Choose which blockchains to scan for contracts"
            )
            
            # Contracts per chain
            contracts_per_chain = st.slider(
                "Contracts per Chain",
                min_value=1,
                max_value=50,
                value=10,
                help="Number of contracts to discover from each chain"
            )
        
        with col2:
            st.subheader("Current Status")
            
            # Check API connectivity
            if st.button("Test API Connections"):
                with st.spinner("Testing connections..."):
                    status = self._test_api_connections()
                    if status['success']:
                        st.success(f"✅ Connected to {status['connected_chains']} chains")
                    else:
                        st.error(f"❌ Connection issues: {status['error']}")
        
        # Discovery action
        st.subheader("Start Discovery")
        
        if st.button("🚀 Discover Contracts", type="primary"):
            if not selected_chains:
                st.error("Please select at least one chain.")
                return
            
            with st.spinner("Discovering contracts..."):
                success_count, error_count = self._run_discovery(selected_chains, contracts_per_chain)
                
                if success_count > 0:
                    st.success(f"✅ Successfully discovered and analyzed {success_count} new contracts!")
                    if error_count > 0:
                        st.warning(f"⚠️ {error_count} contracts encountered errors during processing.")
                else:
                    st.error("❌ No new contracts were discovered. They may already exist in the database.")
    
    def show_analytics(self):
        """Show analytics and insights about discovered contracts."""
        st.header("📊 Contract Analytics")
        
        # Get all contracts for analysis
        contracts = self.db.get_contracts()
        
        if not contracts:
            st.warning("No contract data available for analysis.")
            return
        
        df = pd.DataFrame(contracts)
        
        # Filter controls
        st.subheader("Filters")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            chain_filter = st.selectbox(
                "Chain",
                options=["All"] + list(df['chain'].unique()),
                index=0
            )
        
        with col2:
            optimization_filter = st.selectbox(
                "Optimization",
                options=["All", "Optimized", "Not Optimized"],
                index=0
            )
        
        with col3:
            compiler_filter = st.selectbox(
                "Compiler Version",
                options=["All"] + list(df['compiler_version'].unique()),
                index=0
            )
        
        # Apply filters
        filtered_df = df.copy()
        
        if chain_filter != "All":
            filtered_df = filtered_df[filtered_df['chain'] == chain_filter]
        
        if optimization_filter == "Optimized":
            filtered_df = filtered_df[filtered_df['optimization'] == True]
        elif optimization_filter == "Not Optimized":
            filtered_df = filtered_df[filtered_df['optimization'] == False]
        
        if compiler_filter != "All":
            filtered_df = filtered_df[filtered_df['compiler_version'] == compiler_filter]
        
        # Display filtered results
        st.subheader(f"Analysis Results ({len(filtered_df)} contracts)")
        
        # Analytics charts
        if len(filtered_df) > 0:
            col1, col2 = st.columns(2)
            
            with col1:
                # Optimization distribution
                opt_counts = filtered_df['optimization'].value_counts()
                fig = px.pie(
                    values=opt_counts.values,
                    names=['Optimized' if x else 'Not Optimized' for x in opt_counts.index],
                    title="Optimization Distribution"
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Optimization runs distribution
                if 'runs' in filtered_df.columns:
                    fig = px.histogram(
                        filtered_df[filtered_df['optimization'] == True],
                        x='runs',
                        title="Optimization Runs Distribution",
                        nbins=20
                    )
                    st.plotly_chart(fig, use_container_width=True)
        
        # Contract table with export option
        st.subheader("Contract Details")
        
        # Export button
        if st.button("📥 Export to CSV"):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"./exports/contracts_{timestamp}.csv"
            
            if self.db.export_to_csv(filename):
                st.success(f"✅ Contracts exported to {filename}")
            else:
                st.error("❌ Export failed")
        
        # Display table
        display_columns = ['name', 'address', 'chain', 'compiler_version', 'optimization', 'runs', 'contract_summary']
        if len(filtered_df) > 0:
            st.dataframe(
                filtered_df[display_columns],
                use_container_width=True,
                hide_index=True
            )
    
    def show_search(self):
        """Show search interface for contracts."""
        st.header("🔎 Search Contracts")
        
        # Search tabs
        tab1, tab2 = st.tabs(["📊 Local Database", "☁️ Remote Repository"])
        
        with tab1:
            st.subheader("Search Local Database")
            # Search input
            search_term = st.text_input(
                "Search contracts by name, address, or description",
                placeholder="e.g., USDT, 0x123..., token contract",
                key="local_search"
            )
            
            if search_term:
                results = self.db.search_contracts(search_term)
                
                st.subheader(f"Local Results ({len(results)} found)")
                
                if results:
                    for contract in results:
                        with st.expander(f"{contract['name']} on {contract['chain'].title()}"):
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.write(f"**Address:** `{contract['address']}`")
                                st.write(f"**Chain:** {contract['chain'].title()}")
                                st.write(f"**Compiler:** {contract['compiler_version']}")
                                st.write(f"**Optimized:** {'Yes' if contract['optimization'] else 'No'}")
                            
                            with col2:
                                st.write(f"**Block Number:** {contract['block_number']}")
                                st.write(f"**Verified:** {contract['verified_date'][:10]}")
                                st.write(f"**Bytecode Hash:** `{contract['bytecode_hash'][:16]}...`")
                            
                            if contract['contract_summary']:
                                st.write("**Summary:**")
                                st.write(contract['contract_summary'])
                            
                            # Action buttons
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.button(f"View Source", key=f"source_{contract['id']}"):
                                    st.code(contract['source_code'][:1000] + "...", language='solidity')
                            
                            with col2:
                                if st.button(f"View ABI", key=f"abi_{contract['id']}"):
                                    st.code(contract['abi'][:1000] + "...", language='json')
                else:
                    st.info("No contracts found matching your search.")
        
        with tab2:
            st.subheader("Search Remote Repository")
            
            if not self.github_storage.is_available():
                st.warning("⚠️ GitHub storage not configured. Please set GITHUB_TOKEN environment variable.")
                return
            
            # Search filters
            col1, col2, col3 = st.columns(3)
            
            with col1:
                chain_filter = st.selectbox(
                    "Chain",
                    ["All", "ethereum", "base"],
                    key="remote_chain"
                )
            
            with col2:
                name_filter = st.text_input(
                    "Contract Name",
                    placeholder="e.g., USDT, UniswapV2",
                    key="remote_name"
                )
            
            with col3:
                address_filter = st.text_input(
                    "Address",
                    placeholder="0x123...",
                    key="remote_address"
                )
            
            limit = st.slider("Max Results", 10, 100, 50, key="remote_limit")
            
            if st.button("🔍 Search Remote Repository", key="search_remote"):
                with st.spinner("Searching remote repository..."):
                    try:
                        # Initialize GitHub storage if needed
                        if not hasattr(self.github_storage, 'session') or not self.github_storage.session:
                            asyncio.run(self.github_storage.initialize())
                        
                        # Search parameters
                        search_params = {
                            'chain': None if chain_filter == "All" else chain_filter,
                            'name_filter': name_filter if name_filter else None,
                            'address_filter': address_filter if address_filter else None,
                            'limit': limit
                        }
                        
                        # Perform async search
                        remote_results = asyncio.run(self.github_storage.search_contracts(**search_params))
                        
                        st.subheader(f"Remote Results ({len(remote_results)} found)")
                        
                        if remote_results:
                            for contract in remote_results:
                                with st.expander(f"{contract['name']} on {contract['chain'].title()}"):
                                    col1, col2 = st.columns(2)
                                    
                                    with col1:
                                        st.write(f"**Address:** `{contract['address']}`")
                                        st.write(f"**Chain:** {contract['chain'].title()}")
                                        st.write(f"**Contract ID:** `{contract['contract_id']}`")
                                    
                                    with col2:
                                        if contract.get('verified_date'):
                                            st.write(f"**Verified:** {contract['verified_date'][:10]}")
                                        if contract.get('stored_at'):
                                            st.write(f"**Stored:** {contract['stored_at'][:10]}")
                                    
                                    # Button to load full contract details
                                    if st.button(f"Load Full Details", key=f"load_{contract['contract_id']}"):
                                        with st.spinner("Loading contract details..."):
                                            full_contract = asyncio.run(
                                                self.github_storage.get_contract(
                                                    contract['contract_id'], 
                                                    contract['chain']
                                                )
                                            )
                                            
                                            if full_contract:
                                                st.success("✅ Contract details loaded!")
                                                
                                                if full_contract.get('summary'):
                                                    st.write("**Summary:**")
                                                    st.write(full_contract['summary'])
                                                
                                                if full_contract.get('source_code'):
                                                    with st.expander("View Source Code"):
                                                        st.code(full_contract['source_code'], language='solidity')
                                                
                                                if full_contract.get('abi'):
                                                    with st.expander("View ABI"):
                                                        st.code(full_contract['abi'], language='json')
                                            else:
                                                st.error("Failed to load contract details")
                        else:
                            st.info("No contracts found in remote repository matching your criteria.")
                            
                    except Exception as e:
                        st.error(f"Error searching remote repository: {str(e)}")
                        logger.error(f"Remote search error: {str(e)}")
            
            # Show repository statistics
            with st.expander("📊 Repository Statistics"):
                try:
                    if not hasattr(self.github_storage, 'session') or not self.github_storage.session:
                        asyncio.run(self.github_storage.initialize())
                    
                    stats = asyncio.run(self.github_storage.get_contract_statistics())
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Total Contracts", stats.get('total_contracts', 0))
                    
                    with col2:
                        ethereum_count = stats.get('chains', {}).get('ethereum', 0)
                        st.metric("Ethereum Contracts", ethereum_count)
                    
                    with col3:
                        base_count = stats.get('chains', {}).get('base', 0)
                        st.metric("Base Contracts", base_count)
                    
                    if stats.get('last_updated'):
                        st.write(f"**Last Updated:** {stats['last_updated'][:19].replace('T', ' ')}")
                        
                except Exception as e:
                    st.error(f"Error loading repository statistics: {str(e)}")
                    logger.error(f"Stats error: {str(e)}")
    
    def show_settings(self):
        """Show application settings."""
        st.header("⚙️ Settings")
        
        # GitHub Configuration
        st.subheader("☁️ GitHub Storage Configuration")
        
        github_available = self.github_storage.is_available()
        
        if github_available:
            st.success("✅ GitHub storage is configured and available")
            
            # Show current repository
            github_repo = os.getenv('GITHUB_REPO', 'Not set')
            st.write(f"**Repository:** {github_repo}")
            
            # Test connection button
            if st.button("🧪 Test GitHub Connection"):
                with st.spinner("Testing GitHub connection..."):
                    try:
                        if not hasattr(self.github_storage, 'session') or not self.github_storage.session:
                            asyncio.run(self.github_storage.initialize())
                        
                        stats = asyncio.run(self.github_storage.get_contract_statistics())
                        st.success(f"✅ Connection successful! Found {stats.get('total_contracts', 0)} contracts in repository.")
                    except Exception as e:
                        st.error(f"❌ Connection failed: {str(e)}")
            
            # Repository statistics
            with st.expander("📊 Repository Statistics"):
                try:
                    if not hasattr(self.github_storage, 'session') or not self.github_storage.session:
                        asyncio.run(self.github_storage.initialize())
                    
                    stats = asyncio.run(self.github_storage.get_contract_statistics())
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Total Contracts", stats.get('total_contracts', 0))
                    
                    with col2:
                        ethereum_count = stats.get('chains', {}).get('ethereum', 0)
                        st.metric("Ethereum Contracts", ethereum_count)
                    
                    with col3:
                        base_count = stats.get('chains', {}).get('base', 0)
                        st.metric("Base Contracts", base_count)
                    
                    if stats.get('last_updated'):
                        st.write(f"**Last Updated:** {stats['last_updated'][:19].replace('T', ' ')}")
                        
                except Exception as e:
                    st.error(f"Error loading repository statistics: {str(e)}")
        else:
            st.warning("⚠️ GitHub storage is not configured")
            st.info("""
            To enable GitHub storage, set the following environment variables:
            - **GITHUB_TOKEN**: Your GitHub personal access token
            - **GITHUB_REPO**: Repository in format 'owner/repo-name'
            
            GitHub storage allows you to:
            - Store contracts remotely for live deployment
            - Access contracts from multiple devices
            - Share contract data with team members
            - Backup contract data automatically
            """)
        
        # API Configuration
        st.subheader("🔑 API Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            etherscan_key = os.getenv('ETHERSCAN_API_KEY', '')
            st.text_input(
                "Etherscan API Key",
                value=etherscan_key[:10] + "..." if etherscan_key else "Not configured",
                disabled=True,
                help="Configure in .env file"
            )
        
        with col2:
            basescan_key = os.getenv('BASESCAN_API_KEY', '')
            st.text_input(
                "Basescan API Key",
                value=basescan_key[:10] + "..." if basescan_key else "Not configured",
                disabled=True,
                help="Configure in .env file"
            )
        
        # Database Management
        st.subheader("Database Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🗑️ Clear Database", type="secondary"):
                if st.checkbox("I understand this will delete all contract data"):
                    # Would implement database clearing logic here
                    st.warning("Database clearing functionality would be implemented here.")
        
        with col2:
            if st.button("📊 Database Statistics"):
                stats = self.db.get_statistics()
                st.json(stats)
        
        # Export/Import
        st.subheader("Data Management")
        
        if st.button("📥 Export All Data"):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"./exports/full_export_{timestamp}.csv"
            
            if self.db.export_to_csv(filename):
                st.success(f"✅ Data exported to {filename}")
            else:
                st.error("❌ Export failed")
    
    def _test_api_connections(self) -> Dict[str, Any]:
        """Test API connections."""
        loop = None
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            self.client_manager = BlockchainClientManager()
            loop.run_until_complete(self.client_manager.initialize())
            
            connected_chains = self.client_manager.get_available_chains()
            
            return {
                'success': len(connected_chains) > 0,
                'connected_chains': len(connected_chains),
                'chains': connected_chains,
                'error': None
            }
            
        except Exception as e:
            return {
                'success': False,
                'connected_chains': 0,
                'chains': [],
                'error': str(e)
            }
        finally:
            if self.client_manager and loop:
                loop.run_until_complete(self.client_manager.cleanup())
    
    def _run_discovery(self, chains: List[str], limit: int) -> tuple[int, int]:
        """Run contract discovery process."""
        loop = None
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            self.client_manager = BlockchainClientManager()
            loop.run_until_complete(self.client_manager.initialize())
            
            all_contracts = loop.run_until_complete(
                self.client_manager.get_all_verified_contracts(limit_per_chain=limit)
            )
            
            success_count = 0
            error_count = 0
            
            for contract in all_contracts:
                try:
                    # Generate contract summary
                    summary = ContractAnalyzer.analyze_contract(contract)
                    
                    # Insert into database
                    if self.db.insert_contract(contract, summary):
                        success_count += 1
                    else:
                        error_count += 1
                        
                except Exception as e:
                    logger.error(f"Error processing contract {contract.address}: {str(e)}")
                    error_count += 1
            
            return success_count, error_count
            
        except Exception as e:
            logger.error(f"Discovery failed: {str(e)}")
            return 0, 1
        finally:
            if self.client_manager and loop:
                loop.run_until_complete(self.client_manager.cleanup())

def main():
    """Main entry point for the Streamlit app."""
    app = Web3LOCApp()
    app.run()

if __name__ == "__main__":
    main()
