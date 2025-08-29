"""
Contract README Generator - Automated Documentation for Smart Contracts
Generates comprehensive README files for each discovered contract with analysis and summaries.
"""

import os
import re
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass
from pathlib import Path

from contract_discovery.enhanced_blockchain_client import ContractData
from contract_discovery.contract_database import ContractAnalyzer

@dataclass
class ContractDocumentation:
    """Documentation data for a smart contract."""
    contract_name: str
    address: str
    chain: str
    compiler_version: str
    optimization: bool
    runs: Optional[int]
    block_number: int
    verified_date: str
    summary: str
    category: str
    features: List[str]
    security_analysis: Dict[str, Any]
    complexity_score: int
    function_count: int
    event_count: int
    inheritance_info: Dict[str, Any]
    dependencies: List[str]

class ContractREADMEGenerator:
    """Generates comprehensive README files for smart contracts."""
    
    def __init__(self, output_dir: str = "./contract_readmes"):
        """Initialize the README generator.
        
        Args:
            output_dir: Directory to save README files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def generate_readme(self, contract: ContractData, contract_summary: str) -> str:
        """Generate a comprehensive README for a contract.
        
        Args:
            contract: ContractData object
            contract_summary: Generated summary from ContractAnalyzer
            
        Returns:
            Path to the generated README file
        """
        # Analyze the contract for documentation
        doc_data = self._analyze_contract_for_docs(contract, contract_summary)
        
        # Generate README content
        readme_content = self._generate_readme_content(doc_data)
        
        # Save README file
        filename = f"{contract.chain}_{contract.address}_README.md"
        readme_path = self.output_dir / filename
        
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        return str(readme_path)
    
    def _analyze_contract_for_docs(self, contract: ContractData, summary: str) -> ContractDocumentation:
        """Analyze contract for documentation generation.
        
        Args:
            contract: ContractData object
            summary: Contract summary
            
        Returns:
            ContractDocumentation object
        """
        # Parse ABI for function and event information
        abi_data = self._parse_abi(contract.abi)
        
        # Analyze source code
        source_analysis = self._analyze_source_code(contract.source_code)
        
        # Determine contract category and features
        category, features = self._categorize_contract(contract.source_code, abi_data)
        
        # Security analysis
        security_analysis = self._perform_security_analysis(contract.source_code)
        
        # Calculate complexity score
        complexity_score = self._calculate_complexity_score(source_analysis)
        
        return ContractDocumentation(
            contract_name=contract.name,
            address=contract.address,
            chain=contract.chain,
            compiler_version=contract.compiler_version,
            optimization=contract.optimization,
            runs=contract.runs,
            block_number=contract.block_number,
            verified_date=contract.verified_date,
            summary=summary,
            category=category,
            features=features,
            security_analysis=security_analysis,
            complexity_score=complexity_score,
            function_count=abi_data['function_count'],
            event_count=abi_data['event_count'],
            inheritance_info=source_analysis['inheritance'],
            dependencies=source_analysis['dependencies']
        )
    
    def _parse_abi(self, abi_json: str) -> Dict[str, Any]:
        """Parse ABI JSON and extract information.
        
        Args:
            abi_json: ABI in JSON format
            
        Returns:
            Parsed ABI information
        """
        try:
            abi = json.loads(abi_json) if isinstance(abi_json, str) else abi_json
            
            functions = [item for item in abi if item.get('type') == 'function']
            events = [item for item in abi if item.get('type') == 'event']
            constructors = [item for item in abi if item.get('type') == 'constructor']
            
            # Categorize functions
            view_functions = [f for f in functions if f.get('stateMutability') in ['view', 'pure']]
            payable_functions = [f for f in functions if f.get('stateMutability') == 'payable']
            nonpayable_functions = [f for f in functions if f.get('stateMutability') == 'nonpayable']
            
            return {
                'total_items': len(abi),
                'function_count': len(functions),
                'event_count': len(events),
                'constructor_count': len(constructors),
                'view_functions': len(view_functions),
                'payable_functions': len(payable_functions),
                'nonpayable_functions': len(nonpayable_functions),
                'functions': functions,
                'events': events,
                'constructors': constructors
            }
        except Exception as e:
            return {
                'error': str(e),
                'function_count': 0,
                'event_count': 0,
                'functions': [],
                'events': [],
                'constructors': []
            }
    
    def _analyze_source_code(self, source_code: str) -> Dict[str, Any]:
        """Analyze source code for patterns and structure.
        
        Args:
            source_code: Solidity source code
            
        Returns:
            Source code analysis results
        """
        # Find imports
        imports = re.findall(r'import\s+["\']([^"\']+)["\']', source_code)
        
        # Find contract inheritance
        contract_matches = re.findall(r'contract\s+(\w+)(?:\s+is\s+([^{]+))?', source_code)
        inheritance = {}
        for name, parents in contract_matches:
            if parents:
                parent_list = [p.strip() for p in parents.split(',')]
                inheritance[name] = parent_list
            else:
                inheritance[name] = []
        
        # Find modifiers
        modifiers = re.findall(r'modifier\s+(\w+)', source_code)
        
        # Find custom errors
        errors = re.findall(r'error\s+(\w+)', source_code)
        
        # Count lines and complexity indicators
        lines = source_code.split('\n')
        total_lines = len(lines)
        code_lines = len([line for line in lines if line.strip() and not line.strip().startswith('//')])
        
        # Find security patterns
        security_patterns = {
            'reentrancy_guard': 'ReentrancyGuard' in source_code or 'nonReentrant' in source_code,
            'access_control': any(pattern in source_code for pattern in ['onlyOwner', 'AccessControl', 'Ownable']),
            'pause_mechanism': 'Pausable' in source_code or 'whenNotPaused' in source_code,
            'safe_math': 'SafeMath' in source_code or 'using SafeMath' in source_code,
            'checks_effects_interactions': self._check_cei_pattern(source_code)
        }
        
        return {
            'total_lines': total_lines,
            'code_lines': code_lines,
            'imports': imports,
            'inheritance': inheritance,
            'modifiers': modifiers,
            'custom_errors': errors,
            'security_patterns': security_patterns,
            'dependencies': self._extract_dependencies(imports)
        }
    
    def _categorize_contract(self, source_code: str, abi_data: Dict[str, Any]) -> tuple[str, List[str]]:
        """Categorize contract and identify features.
        
        Args:
            source_code: Contract source code
            abi_data: Parsed ABI data
            
        Returns:
            Tuple of (category, features_list)
        """
        category = "Unknown"
        features: List[str] = []
        
        # Check for token contracts
        if self._is_erc20_token(source_code, abi_data):
            category = "ERC-20 Token"
            features.extend(["Fungible Token", "Transfer", "Allowance"])
            
        elif self._is_erc721_token(source_code, abi_data):
            category = "ERC-721 NFT"
            features.extend(["Non-Fungible Token", "Minting", "Metadata"])
            
        elif self._is_erc1155_token(source_code, abi_data):
            category = "ERC-1155 Multi-Token"
            features.extend(["Multi-Token", "Batch Operations"])
        
        # Check for DeFi contracts
        elif self._is_defi_contract(source_code):
            if "swap" in source_code.lower() or "exchange" in source_code.lower():
                category = "DEX/AMM"
                features.extend(["Decentralized Exchange", "Swapping"])
            elif "stake" in source_code.lower() or "yield" in source_code.lower():
                category = "Staking/Yield"
                features.extend(["Staking", "Rewards"])
            elif "lend" in source_code.lower() or "borrow" in source_code.lower():
                category = "Lending Protocol"
                features.extend(["Lending", "Borrowing"])
            else:
                category = "DeFi Protocol"
                features.append("DeFi")
        
        # Check for governance
        elif self._is_governance_contract(source_code):
            category = "Governance"
            features.extend(["Voting", "Proposals", "Timelock"])
        
        # Check for proxy/upgradeable
        elif self._is_proxy_contract(source_code):
            category = "Proxy Contract"
            features.extend(["Upgradeable", "Proxy Pattern"])
        
        # Additional features
        if "multisig" in source_code.lower() or "MultiSig" in source_code:
            features.append("Multi-Signature")
        
        if "oracle" in source_code.lower():
            features.append("Price Oracle")
        
        if "timelock" in source_code.lower() or "TimeLock" in source_code:
            features.append("Time Lock")
        
        if "pausable" in source_code.lower() or "Pausable" in source_code:
            features.append("Pausable")
        
        if "ownable" in source_code.lower() or "Ownable" in source_code:
            features.append("Ownable")
        
        return category, features
    
    def _perform_security_analysis(self, source_code: str) -> Dict[str, Any]:
        """Perform basic security analysis of the contract.
        
        Args:
            source_code: Contract source code
            
        Returns:
            Security analysis results
        """
        analysis = {
            'security_score': 0,
            'issues': [],
            'good_practices': [],
            'recommendations': []
        }
        
        # Check for common security patterns
        if 'ReentrancyGuard' in source_code or 'nonReentrant' in source_code:
            analysis['good_practices'].append("Uses reentrancy protection")
            analysis['security_score'] += 20
        else:
            analysis['issues'].append("No explicit reentrancy protection found")
            analysis['recommendations'].append("Consider implementing reentrancy guards")
        
        if any(pattern in source_code for pattern in ['onlyOwner', 'AccessControl', 'require(msg.sender']):
            analysis['good_practices'].append("Implements access control")
            analysis['security_score'] += 15
        else:
            analysis['issues'].append("Limited access control mechanisms")
        
        if 'SafeMath' in source_code or 'unchecked' in source_code:
            analysis['good_practices'].append("Handles arithmetic operations safely")
            analysis['security_score'] += 10
        
        if '.call(' in source_code and 'require(' not in source_code:
            analysis['issues'].append("Low-level calls without proper checks")
            analysis['recommendations'].append("Check return values of low-level calls")
        
        # Cap the security score
        analysis['security_score'] = min(analysis['security_score'], 100)
        
        return analysis
    
    def _calculate_complexity_score(self, source_analysis: Dict[str, Any]) -> int:
        """Calculate complexity score based on source analysis.
        
        Args:
            source_analysis: Source code analysis results
            
        Returns:
            Complexity score (0-100)
        """
        score = 0
        
        # Base complexity from lines of code
        code_lines = source_analysis.get('code_lines', 0)
        if code_lines > 500:
            score += 30
        elif code_lines > 200:
            score += 20
        elif code_lines > 100:
            score += 10
        
        # Inheritance complexity
        inheritance = source_analysis.get('inheritance', {})
        total_inheritance = sum(len(parents) for parents in inheritance.values())
        score += min(total_inheritance * 5, 20)
        
        # Dependencies complexity
        dependencies = source_analysis.get('dependencies', [])
        score += min(len(dependencies) * 3, 15)
        
        # Modifiers complexity
        modifiers = source_analysis.get('modifiers', [])
        score += min(len(modifiers) * 2, 10)
        
        return min(score, 100)
    
    def _generate_readme_content(self, doc_data: ContractDocumentation) -> str:
        """Generate README content from documentation data.
        
        Args:
            doc_data: Contract documentation data
            
        Returns:
            README content as markdown string
        """
        content = f"""# {doc_data.contract_name}

> **Category:** {doc_data.category}  
> **Chain:** {doc_data.chain.title()}  
> **Address:** `{doc_data.address}`

## Overview

{doc_data.summary}

## Contract Information

| Property | Value |
|----------|-------|
| **Name** | {doc_data.contract_name} |
| **Address** | `{doc_data.address}` |
| **Blockchain** | {doc_data.chain.title()} |
| **Compiler Version** | {doc_data.compiler_version} |
| **Optimization** | {'Enabled' if doc_data.optimization else 'Disabled'} |
| **Optimization Runs** | {doc_data.runs if doc_data.runs else 'N/A'} |
| **Block Number** | {doc_data.block_number:,} |
| **Verified Date** | {doc_data.verified_date[:10]} |

## Features

{self._format_features_list(doc_data.features)}

## Architecture Analysis

### Complexity Score: {doc_data.complexity_score}/100

- **Functions:** {doc_data.function_count}
- **Events:** {doc_data.event_count}
- **Dependencies:** {len(doc_data.dependencies)}

### Inheritance Structure

{self._format_inheritance(doc_data.inheritance_info)}

### External Dependencies

{self._format_dependencies(doc_data.dependencies)}

## Security Analysis

### Security Score: {doc_data.security_analysis.get('security_score', 0)}/100

{self._format_security_analysis(doc_data.security_analysis)}

## Contract Functions

{self._format_contract_category_description(doc_data.category)}

## Usage Guidelines

{self._generate_usage_guidelines(doc_data.category, doc_data.features)}

## Risk Assessment

{self._generate_risk_assessment(doc_data)}

## Links & Resources

- **Blockchain Explorer:** {self._get_explorer_link(doc_data.chain, doc_data.address)}
- **Compiler Version:** [Solidity {doc_data.compiler_version}](https://github.com/ethereum/solidity/releases)

---

*This README was automatically generated by Web3.LOC Contract Analyzer on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} UTC*

## Disclaimer

This analysis is automated and should not be considered as financial or security advice. Always conduct your own research and security audits before interacting with smart contracts.
"""
        return content
    
    def _format_features_list(self, features: List[str]) -> str:
        """Format features list as markdown."""
        if not features:
            return "- No specific features identified"
        return "\n".join(f"- {feature}" for feature in features)
    
    def _format_inheritance(self, inheritance: Dict[str, Any]) -> str:
        """Format inheritance information."""
        if not inheritance:
            return "- No inheritance detected"
        
        result = []
        for contract, parents in inheritance.items():
            if parents:
                result.append(f"- **{contract}** inherits from: {', '.join(parents)}")
            else:
                result.append(f"- **{contract}** (base contract)")
        
        return "\n".join(result)
    
    def _format_dependencies(self, dependencies: List[str]) -> str:
        """Format dependencies list."""
        if not dependencies:
            return "- No external dependencies"
        return "\n".join(f"- {dep}" for dep in dependencies)
    
    def _format_security_analysis(self, security: Dict[str, Any]) -> str:
        """Format security analysis."""
        content = []
        
        if security.get('good_practices'):
            content.append("#### ✅ Good Practices")
            for practice in security['good_practices']:
                content.append(f"- {practice}")
            content.append("")
        
        if security.get('issues'):
            content.append("#### ⚠️ Potential Issues")
            for issue in security['issues']:
                content.append(f"- {issue}")
            content.append("")
        
        if security.get('recommendations'):
            content.append("#### 💡 Recommendations")
            for rec in security['recommendations']:
                content.append(f"- {rec}")
        
        return "\n".join(content)
    
    def _format_contract_category_description(self, category: str) -> str:
        """Generate description based on contract category."""
        descriptions = {
            "ERC-20 Token": "This is a standard fungible token contract implementing the ERC-20 interface. It allows for the transfer of tokens between addresses and includes allowance mechanisms.",
            "ERC-721 NFT": "This is a non-fungible token (NFT) contract implementing the ERC-721 standard. Each token is unique and can represent ownership of digital or physical assets.",
            "ERC-1155 Multi-Token": "This is a multi-token contract that can handle both fungible and non-fungible tokens in a single contract, providing gas efficiency for batch operations.",
            "DEX/AMM": "This is a decentralized exchange or automated market maker contract that facilitates token swapping without intermediaries.",
            "Staking/Yield": "This contract handles staking mechanisms where users can lock tokens to earn rewards or yield.",
            "Lending Protocol": "This contract facilitates lending and borrowing of digital assets in a decentralized manner.",
            "Governance": "This contract handles governance mechanisms including voting, proposals, and decision-making processes.",
            "Proxy Contract": "This is a proxy contract that enables upgradeability by delegating calls to implementation contracts.",
            "DeFi Protocol": "This is a decentralized finance protocol that provides various financial services on the blockchain."
        }
        
        return descriptions.get(category, "This contract provides specific blockchain functionality. Review the code and ABI for detailed function descriptions.")
    
    def _generate_usage_guidelines(self, category: str, features: List[str]) -> str:
        """Generate usage guidelines based on contract type."""
        guidelines = {
            "ERC-20 Token": "- Use standard token interfaces for transfers\n- Check allowances before transferFrom\n- Monitor balance changes after operations",
            "ERC-721 NFT": "- Verify token ownership before operations\n- Handle metadata URIs properly\n- Use safe transfer methods",
            "DEX/AMM": "- Calculate slippage tolerance\n- Check price impact before large trades\n- Monitor liquidity levels",
            "Governance": "- Understand voting mechanisms\n- Check proposal requirements\n- Respect timelock delays"
        }
        
        base_guideline = guidelines.get(category, "- Read contract documentation carefully\n- Test with small amounts first\n- Verify contract addresses")
        
        if "Pausable" in features:
            base_guideline += "\n- Check if contract is paused before operations"
        
        if "Multi-Signature" in features:
            base_guideline += "\n- Ensure required signatures for operations"
        
        return base_guideline
    
    def _generate_risk_assessment(self, doc_data: ContractDocumentation) -> str:
        """Generate risk assessment."""
        risk_level = "Low"
        factors = []
        
        if doc_data.complexity_score > 70:
            risk_level = "High"
            factors.append("High complexity score")
        elif doc_data.complexity_score > 40:
            risk_level = "Medium"
            factors.append("Moderate complexity")
        
        if doc_data.security_analysis.get('security_score', 0) < 50:
            risk_level = "High"
            factors.append("Low security score")
        
        if len(doc_data.security_analysis.get('issues', [])) > 2:
            risk_level = "Medium" if risk_level == "Low" else "High"
            factors.append("Multiple security concerns")
        
        if not doc_data.optimization:
            factors.append("No optimization enabled")
        
        risk_content = f"**Risk Level:** {risk_level}\n\n"
        
        if factors:
            risk_content += "**Risk Factors:**\n"
            risk_content += "\n".join(f"- {factor}" for factor in factors)
        else:
            risk_content += "No significant risk factors identified."
        
        return risk_content
    
    def _get_explorer_link(self, chain: str, address: str) -> str:
        """Get blockchain explorer link."""
        explorers = {
            "ethereum": f"https://etherscan.io/address/{address}",
            "base": f"https://basescan.org/address/{address}"
        }
        return explorers.get(chain, f"https://etherscan.io/address/{address}")
    
    # Helper methods for contract categorization
    def _is_erc20_token(self, source_code: str, abi_data: Dict[str, Any]) -> bool:
        """Check if contract is ERC-20 token."""
        erc20_functions = ['transfer', 'transferFrom', 'approve', 'balanceOf', 'allowance']
        function_names = [f.get('name', '') for f in abi_data.get('functions', [])]
        return all(func in function_names for func in erc20_functions[:3])  # Check main functions
    
    def _is_erc721_token(self, source_code: str, abi_data: Dict[str, Any]) -> bool:
        """Check if contract is ERC-721 NFT."""
        erc721_functions = ['safeTransferFrom', 'ownerOf', 'approve', 'tokenURI']
        function_names = [f.get('name', '') for f in abi_data.get('functions', [])]
        return any(func in function_names for func in erc721_functions[:2])
    
    def _is_erc1155_token(self, source_code: str, abi_data: Dict[str, Any]) -> bool:
        """Check if contract is ERC-1155."""
        erc1155_functions = ['safeTransferFrom', 'safeBatchTransferFrom', 'balanceOf', 'balanceOfBatch']
        function_names = [f.get('name', '') for f in abi_data.get('functions', [])]
        return any(func in function_names for func in erc1155_functions[:2])
    
    def _is_defi_contract(self, source_code: str) -> bool:
        """Check if contract is DeFi-related."""
        defi_keywords = ['swap', 'liquidity', 'stake', 'yield', 'farm', 'pool', 'vault', 'lend', 'borrow']
        source_lower = source_code.lower()
        return any(keyword in source_lower for keyword in defi_keywords)
    
    def _is_governance_contract(self, source_code: str) -> bool:
        """Check if contract is governance-related."""
        governance_keywords = ['vote', 'proposal', 'governance', 'timelock', 'quorum']
        source_lower = source_code.lower()
        return any(keyword in source_lower for keyword in governance_keywords)
    
    def _is_proxy_contract(self, source_code: str) -> bool:
        """Check if contract is a proxy."""
        proxy_keywords = ['proxy', 'implementation', 'upgrade', 'delegate', 'fallback']
        source_lower = source_code.lower()
        return any(keyword in source_lower for keyword in proxy_keywords)
    
    def _check_cei_pattern(self, source_code: str) -> bool:
        """Check for Checks-Effects-Interactions pattern."""
        # Simplified check for CEI pattern
        return 'require(' in source_code and '.call(' in source_code
    
    def _extract_dependencies(self, imports: List[str]) -> List[str]:
        """Extract dependencies from imports."""
        dependencies = []
        for imp in imports:
            # Extract library/framework names
            if '@openzeppelin' in imp:
                dependencies.append('OpenZeppelin')
            elif '@chainlink' in imp:
                dependencies.append('Chainlink')
            elif 'hardhat' in imp:
                dependencies.append('Hardhat')
            elif imp.startswith('./') or imp.startswith('../'):
                dependencies.append('Local Dependencies')
        
        return list(set(dependencies))  # Remove duplicates
