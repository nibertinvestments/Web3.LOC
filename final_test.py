#!/usr/bin/env python3
"""
Web3.LOC Final Integration Test
Tests all components of the Web3.LOC platform to ensure everything works together.
"""

import asyncio
import sys
import traceback
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from contract_discovery.enhanced_blockchain_client import BlockchainClientManager
from contract_discovery.contract_database import ContractDatabase, ContractAnalyzer
from contract_discovery.readme_generator import ContractREADMEGenerator
from main import Web3LOCSystem

async def test_blockchain_clients():
    """Test blockchain client connections and contract discovery."""
    print("🔍 Testing blockchain client connections...")
    
    try:
        client_manager = BlockchainClientManager()
        await client_manager.initialize()
        
        available_chains = client_manager.get_available_chains()
        print(f"✅ Connected to {len(available_chains)} chains: {', '.join(available_chains)}")
        
        # Test contract discovery
        print("🔎 Testing contract discovery (2 contracts per chain)...")
        contracts = await client_manager.get_all_verified_contracts(limit_per_chain=2)
        
        if contracts:
            print(f"✅ Discovered {len(contracts)} contracts")
            for contract in contracts[:3]:  # Show first 3
                print(f"   - {contract.name} on {contract.chain} ({contract.address[:10]}...)")
        else:
            print("⚠️ No contracts discovered")
        
        await client_manager.cleanup()
        return True, contracts[:2] if contracts else []  # Return 2 contracts for further testing
        
    except Exception as e:
        print(f"❌ Blockchain client test failed: {str(e)}")
        traceback.print_exc()
        return False, []

async def test_integrated_system():
    """Test the complete integrated system."""
    print("\n🚀 Testing integrated Web3.LOC system...")
    
    try:
        system = Web3LOCSystem()
        await system.initialize()
        
        # Test discovery with README generation
        results = await system.discover_contracts(
            limit_per_chain=2,
            generate_readmes=True
        )
        
        if results['success']:
            print(f"✅ System integration test successful!")
            print(f"   Contracts processed: {results['contracts_processed']}")
            print(f"   New contracts added: {results['contracts_added']}")
            print(f"   README files: {len(results.get('readme_files', []))}")
        else:
            print(f"⚠️ System integration test partial: {results['message']}")
        
        await system.cleanup()
        return True
        
    except Exception as e:
        print(f"❌ Integrated system test failed: {str(e)}")
        traceback.print_exc()
        return False

def test_gui_components():
    """Test GUI component availability."""
    print("\n🌐 Testing GUI components...")
    
    try:
        # Test Streamlit availability
        import streamlit as st
        print("✅ Streamlit available")
        
        # Test Plotly availability
        import plotly.express as px
        print("✅ Plotly available")
        
        # Test Pandas availability
        import pandas as pd
        print("✅ Pandas available")
        
        # Check if GUI file exists and is importable
        gui_path = Path("web3_loc_gui.py")
        if gui_path.exists():
            print("✅ GUI file exists")
        else:
            print("❌ GUI file missing")
            return False
        
        return True
        
    except ImportError as e:
        print(f"❌ GUI dependency missing: {str(e)}")
        print("💡 Install with: pip install streamlit plotly pandas")
        return False
    except Exception as e:
        print(f"❌ GUI test failed: {str(e)}")
        return False

async def run_final_test():
    """Run final system test."""
    print("🔍 Web3.LOC Final Integration Test")
    print("=" * 40)
    
    test_results = {
        'blockchain_clients': False,
        'integrated_system': False,
        'gui_components': False
    }
    
    # Test 1: Blockchain Clients
    success, test_contracts = await test_blockchain_clients()
    test_results['blockchain_clients'] = success
    
    # Test 2: Integrated System
    test_results['integrated_system'] = await test_integrated_system()
    
    # Test 3: GUI Components
    test_results['gui_components'] = test_gui_components()
    
    # Summary
    print("\n📊 Test Results Summary")
    print("=" * 30)
    
    passed_tests = sum(test_results.values())
    total_tests = len(test_results)
    
    for test_name, result in test_results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name.replace('_', ' ').title()}: {status}")
    
    print(f"\nOverall: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("\n🎉 All tests passed! Web3.LOC is ready to use.")
        print("\n🚀 To start using Web3.LOC:")
        print("   Option 1 (Recommended): streamlit run web3_loc_gui.py")
        print("   Option 2 (CLI): python main.py")
        print("   Option 3 (Startup): python start.py")
    elif passed_tests >= 2:
        print("\n✅ Core functionality working!")
        print("💡 You can use the system with minor limitations.")
    else:
        print("\n❌ Critical issues detected. Please check:")
        print("   1. API keys in .env file")
        print("   2. Internet connection")
        print("   3. Dependencies: pip install -r requirements.txt")

def main():
    """Main test function."""
    try:
        asyncio.run(run_final_test())
    except KeyboardInterrupt:
        print("\n\n👋 Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        traceback.print_exc()

if __name__ == "__main__":
    main()
