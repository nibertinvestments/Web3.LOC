/**
 * Contract Analyzer for Web3.LOC
 * Provides advanced contract analysis and pattern detection
 */

class ContractAnalyzer {
    constructor() {
        this.patterns = {
            tokens: {
                erc20: ['transfer', 'transferfrom', 'approve', 'balanceof', 'totalsupply'],
                erc721: ['safetransferfrom', 'transferfrom', 'approve', 'ownerof', 'tokenuri'],
                erc1155: ['safetransferfrom', 'safebatchtransferfrom', 'balanceof', 'balanceofbatch']
            },
            defi: {
                uniswap: ['swap', 'addliquidity', 'removeliquidity', 'getamountsout'],
                aave: ['deposit', 'withdraw', 'borrow', 'repay'],
                compound: ['mint', 'redeem', 'borrow', 'repayborrow']
            },
            governance: {
                dao: ['propose', 'vote', 'execute', 'queue'],
                multisig: ['addowner', 'removeowner', 'confirmtransaction', 'executetransaction']
            }
        };

        this.securityPatterns = [
            {
                pattern: /tx\.origin/gi,
                severity: 'high',
                description: 'Uses tx.origin which can be exploited in phishing attacks'
            },
            {
                pattern: /suicide\s*\(|selfdestruct\s*\(/gi,
                severity: 'medium',
                description: 'Contract can be destroyed'
            },
            {
                pattern: /call\.value/gi,
                severity: 'high',
                description: 'Uses call.value which can be vulnerable to reentrancy'
            },
            {
                pattern: /delegatecall/gi,
                severity: 'medium',
                description: 'Uses delegatecall which can be dangerous if not properly secured'
            },
            {
                pattern: /block\.timestamp|now/gi,
                severity: 'low',
                description: 'Relies on block timestamp which can be manipulated by miners'
            },
            {
                pattern: /assert\s*\(/gi,
                severity: 'low',
                description: 'Uses assert() which consumes all gas on failure'
            }
        ];
    }

    /**
     * Analyze a contract comprehensively
     */
    analyzeContract(contractData) {
        const analysis = {
            basic_info: this.extractBasicInfo(contractData),
            token_analysis: this.analyzeTokenStandards(contractData),
            defi_analysis: this.analyzeDeFiPatterns(contractData),
            governance_analysis: this.analyzeGovernancePatterns(contractData),
            security_analysis: this.analyzeSecurityIssues(contractData),
            function_analysis: this.analyzeFunctions(contractData),
            event_analysis: this.analyzeEvents(contractData),
            complexity_metrics: this.calculateComplexityMetrics(contractData),
            gas_analysis: this.analyzeGasUsage(contractData)
        };

        // Generate overall score
        analysis.overall_score = this.calculateOverallScore(analysis);

        return analysis;
    }

    /**
     * Extract basic contract information
     */
    extractBasicInfo(contractData) {
        return {
            name: contractData.name || 'Unknown',
            address: contractData.address,
            chain: contractData.chain,
            verified: contractData.verified,
            compiler_version: contractData.compiler_version,
            optimization_enabled: contractData.optimization,
            optimization_runs: contractData.optimization_runs || 0,
            license: contractData.license_type || 'Unknown',
            is_proxy: contractData.proxy || false,
            source_code_size: contractData.source_code ? contractData.source_code.length : 0
        };
    }

    /**
     * Analyze token standards (ERC-20, ERC-721, ERC-1155)
     */
    analyzeTokenStandards(contractData) {
        const analysis = {
            is_token: false,
            standards: [],
            token_type: null,
            token_features: []
        };

        if (!contractData.abi) {
            return analysis;
        }

        try {
            const abi = typeof contractData.abi === 'string' ? JSON.parse(contractData.abi) : contractData.abi;
            const functionNames = abi
                .filter(item => item.type === 'function')
                .map(func => func.name.toLowerCase());

            // Check ERC-20
            const erc20Functions = this.patterns.tokens.erc20;
            const hasERC20 = erc20Functions.every(func => functionNames.includes(func));
            if (hasERC20) {
                analysis.is_token = true;
                analysis.standards.push('ERC-20');
                analysis.token_type = 'Fungible Token';
            }

            // Check ERC-721
            const erc721Functions = this.patterns.tokens.erc721;
            const hasERC721 = erc721Functions.some(func => functionNames.includes(func));
            if (hasERC721) {
                analysis.is_token = true;
                analysis.standards.push('ERC-721');
                analysis.token_type = 'Non-Fungible Token (NFT)';
            }

            // Check ERC-1155
            const erc1155Functions = this.patterns.tokens.erc1155;
            const hasERC1155 = erc1155Functions.some(func => functionNames.includes(func));
            if (hasERC1155) {
                analysis.is_token = true;
                analysis.standards.push('ERC-1155');
                analysis.token_type = 'Multi-Token';
            }

            // Detect additional token features
            if (functionNames.includes('mint')) {
                analysis.token_features.push('Mintable');
            }
            if (functionNames.includes('burn')) {
                analysis.token_features.push('Burnable');
            }
            if (functionNames.includes('pause')) {
                analysis.token_features.push('Pausable');
            }
            if (functionNames.includes('permit')) {
                analysis.token_features.push('EIP-2612 Permit');
            }

        } catch (error) {
            console.warn('Error analyzing token standards:', error);
        }

        return analysis;
    }

    /**
     * Analyze DeFi patterns
     */
    analyzeDeFiPatterns(contractData) {
        const analysis = {
            is_defi: false,
            protocols: [],
            defi_features: []
        };

        if (!contractData.abi || !contractData.source_code) {
            return analysis;
        }

        try {
            const abi = typeof contractData.abi === 'string' ? JSON.parse(contractData.abi) : contractData.abi;
            const functionNames = abi
                .filter(item => item.type === 'function')
                .map(func => func.name.toLowerCase());
            
            const sourceCodeLower = contractData.source_code.toLowerCase();

            // Check Uniswap patterns
            const uniswapFunctions = this.patterns.defi.uniswap;
            if (uniswapFunctions.some(func => functionNames.includes(func))) {
                analysis.is_defi = true;
                analysis.protocols.push('Uniswap/AMM');
            }

            // Check Aave patterns
            const aaveFunctions = this.patterns.defi.aave;
            if (aaveFunctions.some(func => functionNames.includes(func))) {
                analysis.is_defi = true;
                analysis.protocols.push('Aave/Lending');
            }

            // Check Compound patterns
            const compoundFunctions = this.patterns.defi.compound;
            if (compoundFunctions.some(func => functionNames.includes(func))) {
                analysis.is_defi = true;
                analysis.protocols.push('Compound/Lending');
            }

            // Check for other DeFi features
            if (sourceCodeLower.includes('oracle') || functionNames.includes('getprice')) {
                analysis.defi_features.push('Price Oracle');
            }

            if (functionNames.includes('flashloan') || sourceCodeLower.includes('flashloan')) {
                analysis.defi_features.push('Flash Loans');
            }

            if (functionNames.includes('stake') || functionNames.includes('unstake')) {
                analysis.defi_features.push('Staking');
            }

            if (sourceCodeLower.includes('yield') || sourceCodeLower.includes('farming')) {
                analysis.defi_features.push('Yield Farming');
            }

        } catch (error) {
            console.warn('Error analyzing DeFi patterns:', error);
        }

        return analysis;
    }

    /**
     * Analyze governance patterns
     */
    analyzeGovernancePatterns(contractData) {
        const analysis = {
            is_governance: false,
            governance_type: null,
            governance_features: []
        };

        if (!contractData.abi || !contractData.source_code) {
            return analysis;
        }

        try {
            const abi = typeof contractData.abi === 'string' ? JSON.parse(contractData.abi) : contractData.abi;
            const functionNames = abi
                .filter(item => item.type === 'function')
                .map(func => func.name.toLowerCase());

            const sourceCodeLower = contractData.source_code.toLowerCase();

            // Check DAO patterns
            const daoFunctions = this.patterns.governance.dao;
            if (daoFunctions.some(func => functionNames.includes(func))) {
                analysis.is_governance = true;
                analysis.governance_type = 'DAO';
            }

            // Check Multisig patterns
            const multisigFunctions = this.patterns.governance.multisig;
            if (multisigFunctions.some(func => functionNames.includes(func))) {
                analysis.is_governance = true;
                analysis.governance_type = 'Multisig';
            }

            // Governance features
            if (functionNames.includes('timelock') || sourceCodeLower.includes('timelock')) {
                analysis.governance_features.push('Timelock');
            }

            if (functionNames.includes('delegate') || functionNames.includes('delegation')) {
                analysis.governance_features.push('Vote Delegation');
            }

            if (sourceCodeLower.includes('quorum')) {
                analysis.governance_features.push('Quorum Voting');
            }

        } catch (error) {
            console.warn('Error analyzing governance patterns:', error);
        }

        return analysis;
    }

    /**
     * Analyze security issues
     */
    analyzeSecurityIssues(contractData) {
        const issues = [];

        if (!contractData.source_code) {
            return { issues: [], risk_level: 'unknown' };
        }

        // Check for known security patterns
        this.securityPatterns.forEach(pattern => {
            const matches = contractData.source_code.match(pattern.pattern);
            if (matches) {
                issues.push({
                    severity: pattern.severity,
                    description: pattern.description,
                    occurrences: matches.length,
                    pattern: pattern.pattern.source
                });
            }
        });

        // Calculate overall risk level
        const severityCounts = {
            high: issues.filter(i => i.severity === 'high').length,
            medium: issues.filter(i => i.severity === 'medium').length,
            low: issues.filter(i => i.severity === 'low').length
        };

        let riskLevel = 'low';
        if (severityCounts.high > 0) {
            riskLevel = 'high';
        } else if (severityCounts.medium > 2) {
            riskLevel = 'high';
        } else if (severityCounts.medium > 0) {
            riskLevel = 'medium';
        }

        return {
            issues,
            risk_level: riskLevel,
            severity_counts: severityCounts
        };
    }

    /**
     * Analyze functions
     */
    analyzeFunctions(contractData) {
        const analysis = {
            total_functions: 0,
            public_functions: 0,
            private_functions: 0,
            payable_functions: 0,
            view_functions: 0,
            pure_functions: 0,
            function_details: []
        };

        if (!contractData.abi) {
            return analysis;
        }

        try {
            const abi = typeof contractData.abi === 'string' ? JSON.parse(contractData.abi) : contractData.abi;
            const functions = abi.filter(item => item.type === 'function');

            analysis.total_functions = functions.length;

            functions.forEach(func => {
                // Count by visibility
                const visibility = func.stateMutability || 'nonpayable';
                
                if (func.payable || visibility === 'payable') {
                    analysis.payable_functions++;
                }
                if (visibility === 'view') {
                    analysis.view_functions++;
                }
                if (visibility === 'pure') {
                    analysis.pure_functions++;
                }

                // Add to detailed list
                analysis.function_details.push({
                    name: func.name,
                    inputs: func.inputs?.length || 0,
                    outputs: func.outputs?.length || 0,
                    stateMutability: visibility,
                    payable: func.payable || visibility === 'payable'
                });
            });

        } catch (error) {
            console.warn('Error analyzing functions:', error);
        }

        return analysis;
    }

    /**
     * Analyze events
     */
    analyzeEvents(contractData) {
        const analysis = {
            total_events: 0,
            event_details: []
        };

        if (!contractData.abi) {
            return analysis;
        }

        try {
            const abi = typeof contractData.abi === 'string' ? JSON.parse(contractData.abi) : contractData.abi;
            const events = abi.filter(item => item.type === 'event');

            analysis.total_events = events.length;

            events.forEach(event => {
                analysis.event_details.push({
                    name: event.name,
                    inputs: event.inputs?.length || 0,
                    indexed_inputs: event.inputs?.filter(input => input.indexed).length || 0
                });
            });

        } catch (error) {
            console.warn('Error analyzing events:', error);
        }

        return analysis;
    }

    /**
     * Calculate complexity metrics
     */
    calculateComplexityMetrics(contractData) {
        const metrics = {
            source_lines: 0,
            cyclomatic_complexity: 0,
            function_complexity: 0
        };

        if (contractData.source_code) {
            // Count lines of code
            metrics.source_lines = contractData.source_code.split('\n').length;

            // Simple cyclomatic complexity calculation
            const complexityKeywords = ['if', 'else', 'for', 'while', 'do', 'switch', 'case', '&&', '||', '?'];
            complexityKeywords.forEach(keyword => {
                const regex = new RegExp(`\\b${keyword}\\b`, 'gi');
                const matches = contractData.source_code.match(regex);
                metrics.cyclomatic_complexity += matches ? matches.length : 0;
            });
        }

        if (contractData.abi) {
            try {
                const abi = typeof contractData.abi === 'string' ? JSON.parse(contractData.abi) : contractData.abi;
                const functions = abi.filter(item => item.type === 'function');
                metrics.function_complexity = functions.length;
            } catch (error) {
                console.warn('Error calculating function complexity:', error);
            }
        }

        return metrics;
    }

    /**
     * Analyze gas usage patterns
     */
    analyzeGasUsage(contractData) {
        const analysis = {
            optimization_enabled: contractData.optimization || false,
            optimization_runs: contractData.optimization_runs || 0,
            estimated_deployment_gas: 0,
            gas_efficiency_score: 0
        };

        // Estimate deployment gas based on bytecode size
        if (contractData.contract_creation_code) {
            analysis.estimated_deployment_gas = Math.ceil(contractData.contract_creation_code.length / 2) * 68;
        }

        // Calculate gas efficiency score
        let score = 50; // Base score

        if (analysis.optimization_enabled) {
            score += 20;
        }

        if (analysis.optimization_runs > 200) {
            score += 10;
        }

        // Adjust based on contract size
        const sourceSize = contractData.source_code ? contractData.source_code.length : 0;
        if (sourceSize < 10000) {
            score += 10;
        } else if (sourceSize > 50000) {
            score -= 10;
        }

        analysis.gas_efficiency_score = Math.max(0, Math.min(100, score));

        return analysis;
    }

    /**
     * Calculate overall contract score
     */
    calculateOverallScore(analysis) {
        let score = 50; // Base score

        // Security score impact
        if (analysis.security_analysis.risk_level === 'low') {
            score += 20;
        } else if (analysis.security_analysis.risk_level === 'medium') {
            score += 10;
        } else if (analysis.security_analysis.risk_level === 'high') {
            score -= 20;
        }

        // Optimization impact
        if (analysis.gas_analysis.optimization_enabled) {
            score += 10;
        }

        // Verification impact
        if (analysis.basic_info.verified) {
            score += 20;
        }

        // Token/DeFi bonus
        if (analysis.token_analysis.is_token) {
            score += 5;
        }
        if (analysis.defi_analysis.is_defi) {
            score += 5;
        }

        return Math.max(0, Math.min(100, score));
    }

    /**
     * Generate contract summary
     */
    generateSummary(analysis) {
        const summary = [];

        // Basic info
        summary.push(`Contract: ${analysis.basic_info.name}`);
        summary.push(`Chain: ${analysis.basic_info.chain.charAt(0).toUpperCase() + analysis.basic_info.chain.slice(1)}`);
        summary.push(`Verified: ${analysis.basic_info.verified ? 'Yes' : 'No'}`);

        // Token info
        if (analysis.token_analysis.is_token) {
            summary.push(`Token Type: ${analysis.token_analysis.token_type}`);
            if (analysis.token_analysis.standards.length > 0) {
                summary.push(`Standards: ${analysis.token_analysis.standards.join(', ')}`);
            }
        }

        // DeFi info
        if (analysis.defi_analysis.is_defi) {
            summary.push(`DeFi Protocol: ${analysis.defi_analysis.protocols.join(', ')}`);
        }

        // Security
        const riskLevel = analysis.security_analysis.risk_level;
        summary.push(`Security Risk: ${riskLevel.charAt(0).toUpperCase() + riskLevel.slice(1)}`);

        // Functions
        summary.push(`Functions: ${analysis.function_analysis.total_functions}`);
        summary.push(`Events: ${analysis.event_analysis.total_events}`);

        // Overall score
        summary.push(`Overall Score: ${analysis.overall_score}/100`);

        return summary.join('\n');
    }
}

// Export for use in other modules
window.ContractAnalyzer = ContractAnalyzer;
