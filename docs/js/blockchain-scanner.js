/**
 * Blockchain Scanner for Web3.LOC
 * Continuously scans Ethereum and Base networks for new contracts at 4 calls/second
 */

class BlockchainScanner {
    constructor() {
        this.isRunning = false;
        this.scanCount = 0;
        this.lastScanTime = null;
        this.discoveredContracts = 0;
        this.errorCount = 0;
        
        // Rate limiting (4 calls per second total)
        this.requestQueue = [];
        this.isProcessingQueue = false;
        this.lastRequestTime = 0;
        this.requestInterval = 250; // 250ms between requests (4/second)
        
        // Scanning state
        this.currentBlock = {
            ethereum: null,
            base: null
        };
        
        this.scanStrategies = {
            recentBlocks: true,
            popularContracts: true,
            addressPatterns: true
        };
        
        this.init();
    }

    /**
     * Initialize the scanner
     */
    async init() {
        try {
            // Get current block numbers
            await this.updateCurrentBlocks();
            
            // Initialize GitHub storage
            this.storage = new GitHubStorage();
            
            console.log('🚀 Blockchain Scanner initialized');
            
            // Start scanning if enabled
            if (CONFIG.SCANNER.ENABLED) {
                this.start();
            }
        } catch (error) {
            console.error('Failed to initialize scanner:', error);
        }
    }

    /**
     * Start continuous scanning
     */
    start() {
        if (this.isRunning) return;
        
        this.isRunning = true;
        console.log('🔄 Starting continuous blockchain scanning at 4 calls/second');
        
        // Start request processor
        this.startRequestProcessor();
        
        // Start scanning strategies
        this.startRecentBlocksScanning();
        this.startPopularContractsScanning();
        this.startAddressPatternsScanning();
        
        // Update UI
        this.updateScannerStatus();
    }

    /**
     * Stop scanning
     */
    stop() {
        this.isRunning = false;
        console.log('⏹️ Blockchain scanning stopped');
    }

    /**
     * Process request queue with rate limiting
     */
    async startRequestProcessor() {
        this.isProcessingQueue = true;
        
        while (this.isRunning) {
            if (this.requestQueue.length > 0) {
                const now = Date.now();
                
                // Rate limiting check
                if (now - this.lastRequestTime >= this.requestInterval) {
                    const request = this.requestQueue.shift();
                    this.lastRequestTime = now;
                    
                    try {
                        await this.processRequest(request);
                        this.scanCount++;
                        this.lastScanTime = now;
                    } catch (error) {
                        this.errorCount++;
                        console.warn('Request failed:', error.message);
                    }
                }
            }
            
            // Small delay to prevent busy waiting
            await this.sleep(10);
        }
        
        this.isProcessingQueue = false;
    }

    /**
     * Process a single API request
     */
    async processRequest(request) {
        const { network, endpoint, params } = request;
        
        const apiConfig = network === 'ethereum' ? CONFIG.APIS.ETHERSCAN : CONFIG.APIS.BASESCAN;
        const url = new URL(apiConfig.BASE_URL);
        
        // Add parameters
        Object.keys(params).forEach(key => {
            url.searchParams.append(key, params[key]);
        });
        url.searchParams.append('apikey', apiConfig.API_KEY);

        const response = await fetch(url.toString(), {
            timeout: apiConfig.TIMEOUT
        });

        if (!response.ok) {
            throw new Error(`API request failed: ${response.status}`);
        }

        const data = await response.json();
        
        if (data.status === '0' && data.message !== 'No transactions found') {
            throw new Error(data.result || 'API error');
        }

        return data.result;
    }

    /**
     * Scan recent blocks for new contracts
     */
    async startRecentBlocksScanning() {
        while (this.isRunning && CONFIG.SCANNER.STRATEGIES.RECENT_BLOCKS.enabled) {
            try {
                // Queue requests for both networks
                await this.queueRecentBlocksRequests();
                
                // Wait before next scan
                await this.sleep(CONFIG.SCANNER.STRATEGIES.RECENT_BLOCKS.interval);
            } catch (error) {
                console.warn('Recent blocks scanning error:', error);
                await this.sleep(30000); // Wait 30s on error
            }
        }
    }

    /**
     * Queue requests for recent blocks scanning
     */
    async queueRecentBlocksRequests() {
        for (const network of CONFIG.SCANNER.NETWORKS) {
            // Get latest block
            this.requestQueue.push({
                network,
                endpoint: 'eth_blockNumber',
                params: {
                    module: 'proxy',
                    action: 'eth_blockNumber'
                },
                callback: (result) => this.handleNewBlock(network, result)
            });

            // Scan recent blocks for contract creation transactions
            if (this.currentBlock[network]) {
                const fromBlock = Math.max(
                    this.currentBlock[network] - CONFIG.SCANNER.STRATEGIES.RECENT_BLOCKS.lookback,
                    0
                );

                this.requestQueue.push({
                    network,
                    endpoint: 'txlist',
                    params: {
                        module: 'account',
                        action: 'txlist',
                        startblock: fromBlock,
                        endblock: 'latest',
                        sort: 'desc'
                    },
                    callback: (result) => this.handleTransactionList(network, result)
                });
            }
        }
    }

    /**
     * Handle new block discovery
     */
    async handleNewBlock(network, blockHex) {
        const blockNumber = parseInt(blockHex, 16);
        
        if (!this.currentBlock[network] || blockNumber > this.currentBlock[network]) {
            this.currentBlock[network] = blockNumber;
            console.log(`📦 New ${network} block: ${blockNumber}`);
        }
    }

    /**
     * Handle transaction list and extract contract creations
     */
    async handleTransactionList(network, transactions) {
        if (!Array.isArray(transactions)) return;

        for (const tx of transactions) {
            // Contract creation transactions have empty 'to' field
            if (!tx.to && tx.contractAddress) {
                await this.discoverContract(network, tx.contractAddress, tx);
            }
        }
    }

    /**
     * Scan popular/known contracts
     */
    async startPopularContractsScanning() {
        // List of popular contract addresses to check
        const popularContracts = {
            ethereum: [
                '0xA0b86a33E6441E95C1B7b4de35D65dd8C55c3F2e', // USDT
                '0xA0b86a33E6441E95C1B7b4de35D65dd8C55c3F2e', // USDC
                '0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984', // UNI
                '0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9'  // AAVE
            ],
            base: [
                '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913', // USDC on Base
                '0x4200000000000000000000000000000000000006'  // WETH on Base
            ]
        };

        while (this.isRunning && CONFIG.SCANNER.STRATEGIES.POPULAR_CONTRACTS.enabled) {
            try {
                for (const network of CONFIG.SCANNER.NETWORKS) {
                    const contracts = popularContracts[network] || [];
                    
                    for (const address of contracts) {
                        // Queue contract source code request
                        this.requestQueue.push({
                            network,
                            endpoint: 'getsourcecode',
                            params: {
                                module: 'contract',
                                action: 'getsourcecode',
                                address: address
                            },
                            callback: (result) => this.handleContractSource(network, address, result)
                        });
                    }
                }
                
                await this.sleep(CONFIG.SCANNER.STRATEGIES.POPULAR_CONTRACTS.interval);
            } catch (error) {
                console.warn('Popular contracts scanning error:', error);
                await this.sleep(60000);
            }
        }
    }

    /**
     * Scan contracts by address patterns
     */
    async startAddressPatternsScanning() {
        while (this.isRunning && CONFIG.SCANNER.STRATEGIES.ADDRESS_PATTERNS.enabled) {
            try {
                for (const network of CONFIG.SCANNER.NETWORKS) {
                    for (const pattern of CONFIG.SCANNER.STRATEGIES.ADDRESS_PATTERNS.patterns) {
                        // Generate addresses with the pattern
                        const addresses = this.generateAddressesWithPattern(pattern);
                        
                        for (const address of addresses.slice(0, 5)) { // Limit to 5 per pattern
                            this.requestQueue.push({
                                network,
                                endpoint: 'getsourcecode',
                                params: {
                                    module: 'contract',
                                    action: 'getsourcecode',
                                    address: address
                                },
                                callback: (result) => this.handleContractSource(network, address, result)
                            });
                        }
                    }
                }
                
                await this.sleep(CONFIG.SCANNER.STRATEGIES.ADDRESS_PATTERNS.interval);
            } catch (error) {
                console.warn('Address patterns scanning error:', error);
                await this.sleep(120000);
            }
        }
    }

    /**
     * Generate random addresses with a specific pattern
     */
    generateAddressesWithPattern(pattern) {
        const addresses = [];
        
        for (let i = 0; i < 10; i++) {
            let address = '0x' + pattern.substring(2);
            
            // Fill remaining characters with random hex
            while (address.length < 42) {
                address += Math.floor(Math.random() * 16).toString(16);
            }
            
            addresses.push(address);
        }
        
        return addresses;
    }

    /**
     * Handle contract source code response
     */
    async handleContractSource(network, address, result) {
        if (!Array.isArray(result) || result.length === 0) return;
        
        const contractData = result[0];
        
        // Skip if not verified or no source code
        if (!contractData.SourceCode || contractData.SourceCode === '') return;
        
        await this.discoverContract(network, address, null, contractData);
    }

    /**
     * Discover and process a new contract
     */
    async discoverContract(network, address, transactionData = null, contractData = null) {
        try {
            // Check if contract already exists
            const existingContract = await this.storage.getContract(address, network);
            if (existingContract) {
                return; // Skip duplicates
            }

            // If we don't have contract data, fetch it
            if (!contractData) {
                this.requestQueue.push({
                    network,
                    endpoint: 'getsourcecode',
                    params: {
                        module: 'contract',
                        action: 'getsourcecode',
                        address: address
                    },
                    callback: (result) => this.handleContractSource(network, address, result)
                });
                return;
            }

            // Process the contract
            const processedContract = await this.processContract(network, address, contractData, transactionData);
            
            if (processedContract) {
                // Store in GitHub
                await this.storage.storeContract(processedContract);
                
                this.discoveredContracts++;
                console.log(`✅ New contract discovered: ${address} on ${network}`);
                
                // Update UI
                this.updateRecentContracts(processedContract);
            }
        } catch (error) {
            console.warn(`Failed to process contract ${address}:`, error);
        }
    }

    /**
     * Process contract data into standard format
     */
    async processContract(network, address, contractData, transactionData) {
        if (!contractData.SourceCode || contractData.SourceCode === '') {
            return null; // Skip unverified contracts
        }

        const contract = {
            address: address.toLowerCase(),
            chain: network,
            name: contractData.ContractName || 'Unknown',
            source_code: contractData.SourceCode,
            abi: contractData.ABI || '[]',
            compiler_version: contractData.CompilerVersion || 'Unknown',
            optimization: contractData.OptimizationUsed === '1',
            verified: true,
            verified_date: new Date().toISOString(),
            stored_at: new Date().toISOString(),
            
            // Additional metadata
            metadata: {
                constructor_arguments: contractData.ConstructorArguments || '',
                evm_version: contractData.EVMVersion || '',
                library: contractData.Library || '',
                license_type: contractData.LicenseType || '',
                proxy: contractData.Proxy === '1',
                implementation: contractData.Implementation || ''
            }
        };

        // Add transaction data if available
        if (transactionData) {
            contract.creation_transaction = {
                hash: transactionData.hash,
                block_number: parseInt(transactionData.blockNumber),
                gas_used: parseInt(transactionData.gasUsed || 0),
                gas_price: transactionData.gasPrice || '0'
            };
        }

        // Detect contract type
        contract.type = this.detectContractType(contract.source_code, contract.name);
        
        // Generate summary
        contract.summary = this.generateContractSummary(contract);

        return contract;
    }

    /**
     * Detect contract type based on source code and name
     */
    detectContractType(sourceCode, name) {
        const source = sourceCode.toLowerCase();
        const contractName = name.toLowerCase();

        for (const [type, patterns] of Object.entries(CONFIG.CONTRACT_PATTERNS)) {
            for (const pattern of patterns) {
                if (source.includes(pattern.toLowerCase()) || contractName.includes(pattern.toLowerCase())) {
                    return type;
                }
            }
        }

        return 'other';
    }

    /**
     * Generate contract summary
     */
    generateContractSummary(contract) {
        const type = contract.type.charAt(0).toUpperCase() + contract.type.slice(1);
        return `${type} contract ${contract.name} deployed on ${contract.chain} network. Verified and optimized: ${contract.optimization ? 'Yes' : 'No'}.`;
    }

    /**
     * Update current block numbers
     */
    async updateCurrentBlocks() {
        for (const network of CONFIG.SCANNER.NETWORKS) {
            try {
                const apiConfig = network === 'ethereum' ? CONFIG.APIS.ETHERSCAN : CONFIG.APIS.BASESCAN;
                const response = await fetch(`${apiConfig.BASE_URL}?module=proxy&action=eth_blockNumber&apikey=${apiConfig.API_KEY}`);
                const data = await response.json();
                
                if (data.result) {
                    this.currentBlock[network] = parseInt(data.result, 16);
                }
            } catch (error) {
                console.warn(`Failed to get current block for ${network}:`, error);
            }
        }
    }

    /**
     * Update scanner status in UI
     */
    updateScannerStatus() {
        if (typeof updateScannerUI === 'function') {
            updateScannerUI({
                isRunning: this.isRunning,
                scanCount: this.scanCount,
                lastScanTime: this.lastScanTime,
                discoveredContracts: this.discoveredContracts,
                errorCount: this.errorCount,
                queueSize: this.requestQueue.length
            });
        }
    }

    /**
     * Update recent contracts in UI
     */
    updateRecentContracts(contract) {
        if (typeof addRecentContract === 'function') {
            addRecentContract(contract);
        }
    }

    /**
     * Get scanner statistics
     */
    getStats() {
        return {
            isRunning: this.isRunning,
            scanCount: this.scanCount,
            lastScanTime: this.lastScanTime,
            discoveredContracts: this.discoveredContracts,
            errorCount: this.errorCount,
            queueSize: this.requestQueue.length,
            currentBlocks: { ...this.currentBlock }
        };
    }

    /**
     * Utility function for delays
     */
    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

// Make scanner globally available
window.BlockchainScanner = BlockchainScanner;
