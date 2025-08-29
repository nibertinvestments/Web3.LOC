/**
 * Blockchain API Manager for Web3.LOC
 * Handles interactions with Etherscan and Basescan APIs
 */

class BlockchainAPI {
    constructor() {
        this.etherscanKey = localStorage.getItem('etherscan_key');
        this.basescanKey = localStorage.getItem('basescan_key');
        
        this.endpoints = {
            ethereum: 'https://api.etherscan.io/api',
            base: 'https://api.basescan.org/api'
        };
    }

    /**
     * Get contract source code and ABI
     */
    async getContractData(address, chain) {
        const apiKey = chain === 'ethereum' ? this.etherscanKey : this.basescanKey;
        const endpoint = this.endpoints[chain];

        if (!apiKey) {
            throw new Error(`${chain} API key not configured`);
        }

        try {
            // Get contract source code
            const sourceResponse = await fetch(
                `${endpoint}?module=contract&action=getsourcecode&address=${address}&apikey=${apiKey}`
            );

            if (!sourceResponse.ok) {
                throw new Error(`API request failed: ${sourceResponse.status}`);
            }

            const sourceData = await sourceResponse.json();

            if (sourceData.status !== '1') {
                throw new Error(`API error: ${sourceData.message || 'Unknown error'}`);
            }

            const contractInfo = sourceData.result[0];

            if (!contractInfo || contractInfo.SourceCode === '') {
                throw new Error('Contract not verified or not found');
            }

            // Get additional contract information
            const [transactionCount, balance] = await Promise.all([
                this.getTransactionCount(address, chain),
                this.getBalance(address, chain)
            ]);

            // Parse and structure the contract data
            const contractData = {
                address: address,
                chain: chain,
                name: contractInfo.ContractName || 'Unknown',
                source_code: contractInfo.SourceCode,
                abi: contractInfo.ABI,
                compiler_version: contractInfo.CompilerVersion,
                optimization: contractInfo.OptimizationUsed === '1',
                optimization_runs: parseInt(contractInfo.Runs) || 0,
                constructor_arguments: contractInfo.ConstructorArguments || '',
                contract_creation_code: contractInfo.ByteCode || '',
                library: contractInfo.Library || '',
                license_type: contractInfo.LicenseType || '',
                proxy: contractInfo.Proxy === '1',
                implementation: contractInfo.Implementation || '',
                swarm_source: contractInfo.SwarmSource || '',
                verified: true,
                verified_date: new Date().toISOString(),
                transaction_count: transactionCount,
                balance: balance,
                stored_at: new Date().toISOString()
            };

            return contractData;
        } catch (error) {
            console.error(`Error fetching contract data for ${address}:`, error);
            throw error;
        }
    }

    /**
     * Get transaction count for an address
     */
    async getTransactionCount(address, chain) {
        const apiKey = chain === 'ethereum' ? this.etherscanKey : this.basescanKey;
        const endpoint = this.endpoints[chain];

        try {
            const response = await fetch(
                `${endpoint}?module=proxy&action=eth_getTransactionCount&address=${address}&tag=latest&apikey=${apiKey}`
            );

            const data = await response.json();
            return parseInt(data.result, 16) || 0;
        } catch (error) {
            console.warn('Failed to get transaction count:', error);
            return 0;
        }
    }

    /**
     * Get balance for an address
     */
    async getBalance(address, chain) {
        const apiKey = chain === 'ethereum' ? this.etherscanKey : this.basescanKey;
        const endpoint = this.endpoints[chain];

        try {
            const response = await fetch(
                `${endpoint}?module=account&action=balance&address=${address}&tag=latest&apikey=${apiKey}`
            );

            const data = await response.json();
            return data.result || '0';
        } catch (error) {
            console.warn('Failed to get balance:', error);
            return '0';
        }
    }

    /**
     * Validate Ethereum address format
     */
    isValidAddress(address) {
        return /^0x[a-fA-F0-9]{40}$/.test(address);
    }

    /**
     * Search for contracts by creator address
     */
    async getContractsCreatedBy(creatorAddress, chain, page = 1, offset = 100) {
        const apiKey = chain === 'ethereum' ? this.etherscanKey : this.basescanKey;
        const endpoint = this.endpoints[chain];

        try {
            const response = await fetch(
                `${endpoint}?module=account&action=txlist&address=${creatorAddress}&startblock=0&endblock=99999999&page=${page}&offset=${offset}&sort=asc&apikey=${apiKey}`
            );

            const data = await response.json();

            if (data.status !== '1') {
                throw new Error(data.message || 'Failed to fetch transactions');
            }

            // Filter for contract creation transactions
            const contractCreations = data.result.filter(tx => 
                tx.to === '' && tx.contractAddress && tx.contractAddress !== ''
            );

            return contractCreations.map(tx => ({
                address: tx.contractAddress,
                creator: tx.from,
                transaction_hash: tx.hash,
                block_number: parseInt(tx.blockNumber),
                timestamp: new Date(parseInt(tx.timeStamp) * 1000).toISOString(),
                gas_used: parseInt(tx.gasUsed),
                gas_price: tx.gasPrice
            }));
        } catch (error) {
            console.error('Error searching for created contracts:', error);
            throw error;
        }
    }

    /**
     * Get recent verified contracts
     */
    async getRecentVerifiedContracts(chain, limit = 20) {
        const apiKey = chain === 'ethereum' ? this.etherscanKey : this.basescanKey;
        const endpoint = this.endpoints[chain];

        try {
            // Note: This is a simplified approach - real implementation might need
            // more sophisticated contract discovery methods
            const response = await fetch(
                `${endpoint}?module=contract&action=getcontractcreation&contractaddresses=&apikey=${apiKey}`
            );

            if (!response.ok) {
                throw new Error('Failed to fetch recent contracts');
            }

            const data = await response.json();
            return data.result || [];
        } catch (error) {
            console.warn('Failed to get recent verified contracts:', error);
            return [];
        }
    }

    /**
     * Analyze contract for common patterns
     */
    analyzeContract(sourceCode, abi) {
        const analysis = {
            is_token: false,
            is_nft: false,
            is_proxy: false,
            is_multisig: false,
            has_pausable: false,
            has_ownable: false,
            has_upgradeable: false,
            functions: [],
            events: [],
            security_issues: []
        };

        if (!sourceCode || !abi) {
            return analysis;
        }

        try {
            const parsedABI = typeof abi === 'string' ? JSON.parse(abi) : abi;
            
            // Extract functions and events
            analysis.functions = parsedABI
                .filter(item => item.type === 'function')
                .map(func => ({
                    name: func.name,
                    inputs: func.inputs?.length || 0,
                    outputs: func.outputs?.length || 0,
                    stateMutability: func.stateMutability,
                    payable: func.payable
                }));

            analysis.events = parsedABI
                .filter(item => item.type === 'event')
                .map(event => ({
                    name: event.name,
                    inputs: event.inputs?.length || 0
                }));

            // Check for common patterns
            const functionNames = analysis.functions.map(f => f.name.toLowerCase());
            const sourceCodeLower = sourceCode.toLowerCase();

            // Token detection
            analysis.is_token = functionNames.includes('transfer') && 
                               functionNames.includes('balanceof') &&
                               functionNames.includes('totalsupply');

            // NFT detection
            analysis.is_nft = functionNames.includes('safetransferfrom') ||
                             functionNames.includes('tokenuri') ||
                             sourceCodeLower.includes('erc721');

            // Proxy detection
            analysis.is_proxy = sourceCodeLower.includes('delegatecall') ||
                               sourceCodeLower.includes('proxy') ||
                               functionNames.includes('implementation');

            // Multisig detection
            analysis.is_multisig = functionNames.includes('addowner') ||
                                  functionNames.includes('confirmtransaction') ||
                                  sourceCodeLower.includes('multisig');

            // Pausable detection
            analysis.has_pausable = functionNames.includes('pause') ||
                                   functionNames.includes('unpause') ||
                                   sourceCodeLower.includes('pausable');

            // Ownable detection
            analysis.has_ownable = functionNames.includes('transferownership') ||
                                  functionNames.includes('owner') ||
                                  sourceCodeLower.includes('ownable');

            // Upgradeable detection
            analysis.has_upgradeable = functionNames.includes('upgrade') ||
                                      sourceCodeLower.includes('upgradeable') ||
                                      sourceCodeLower.includes('initializable');

            // Basic security issue detection
            if (sourceCodeLower.includes('tx.origin')) {
                analysis.security_issues.push('Uses tx.origin (potential security risk)');
            }

            if (sourceCodeLower.includes('suicide') || sourceCodeLower.includes('selfdestruct')) {
                analysis.security_issues.push('Contains selfdestruct');
            }

            if (sourceCodeLower.includes('call.value')) {
                analysis.security_issues.push('Uses call.value (potential reentrancy risk)');
            }

        } catch (error) {
            console.warn('Error analyzing contract:', error);
        }

        return analysis;
    }

    /**
     * Format Wei to Ether
     */
    weiToEther(wei) {
        try {
            const ether = parseFloat(wei) / 1e18;
            return ether.toFixed(6);
        } catch (error) {
            return '0';
        }
    }

    /**
     * Test API connection
     */
    async testConnection(chain) {
        const apiKey = chain === 'ethereum' ? this.etherscanKey : this.basescanKey;
        const endpoint = this.endpoints[chain];

        if (!apiKey) {
            throw new Error(`${chain} API key not configured`);
        }

        try {
            const response = await fetch(
                `${endpoint}?module=stats&action=ethsupply&apikey=${apiKey}`
            );

            if (!response.ok) {
                throw new Error(`API request failed: ${response.status}`);
            }

            const data = await response.json();
            return data.status === '1';
        } catch (error) {
            console.error(`Error testing ${chain} API:`, error);
            return false;
        }
    }
}

// Export for use in other modules
window.BlockchainAPI = BlockchainAPI;
