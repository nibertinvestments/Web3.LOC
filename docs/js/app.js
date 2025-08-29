/**
 * Main Application for Web3.LOC
 * Coordinates all components and handles user interactions
 */

class Web3LOCApp {
    constructor() {
        this.githubStorage = new GitHubStorage();
        this.blockchainAPI = new BlockchainAPI();
        this.contractAnalyzer = new ContractAnalyzer();
        this.chartsManager = new ChartsManager();
        
        this.contracts = [];
        this.currentTab = 'dashboard';
        this.isLoading = false;
        
        this.initialize();
    }

    /**
     * Initialize the application
     */
    async initialize() {
        try {
            // Initialize AOS animations
            if (typeof AOS !== 'undefined') {
                AOS.init({
                    duration: 800,
                    easing: 'ease-in-out',
                    once: true
                });
            }

            // Set up event listeners
            this.setupEventListeners();
            
            // Initialize charts
            this.chartsManager.initializeCharts();
            
            // Load saved settings
            this.loadSettings();
            
            // Test connections
            await this.testConnections();
            
            // Load initial data
            await this.loadDashboardData();
            
            console.log('Web3.LOC application initialized successfully');
        } catch (error) {
            console.error('Error initializing application:', error);
            this.showMessage('Error initializing application', 'error');
        }
    }

    /**
     * Set up event listeners
     */
    setupEventListeners() {
        // Navigation
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const tabId = link.getAttribute('data-tab');
                this.switchTab(tabId);
            });
        });

        // Settings modal
        const settingsBtn = document.getElementById('settings-btn');
        const settingsModal = document.getElementById('settings-modal');
        const closeSettings = document.getElementById('close-settings');
        
        if (settingsBtn) {
            settingsBtn.addEventListener('click', () => {
                settingsModal.classList.add('show');
            });
        }
        
        if (closeSettings) {
            closeSettings.addEventListener('click', () => {
                settingsModal.classList.remove('show');
            });
        }

        // Settings form
        const saveSettings = document.getElementById('save-settings');
        const testConnection = document.getElementById('test-connection');
        
        if (saveSettings) {
            saveSettings.addEventListener('click', () => this.saveSettings());
        }
        
        if (testConnection) {
            testConnection.addEventListener('click', () => this.testConnections());
        }

        // Discovery form
        const discoverBtn = document.getElementById('discover-btn');
        const contractAddress = document.getElementById('contract-address');
        
        if (discoverBtn) {
            discoverBtn.addEventListener('click', () => this.discoverContract());
        }
        
        if (contractAddress) {
            contractAddress.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.discoverContract();
                }
            });
        }

        // Search form
        const searchBtn = document.getElementById('search-btn');
        if (searchBtn) {
            searchBtn.addEventListener('click', () => this.searchContracts());
        }

        // Export buttons
        const exportCSV = document.getElementById('export-csv');
        const exportJSON = document.getElementById('export-json');
        
        if (exportCSV) {
            exportCSV.addEventListener('click', () => this.exportData('csv'));
        }
        
        if (exportJSON) {
            exportJSON.addEventListener('click', () => this.exportData('json'));
        }

        // Close modal when clicking outside
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('modal')) {
                e.target.classList.remove('show');
            }
        });

        // Window resize
        window.addEventListener('resize', () => {
            this.chartsManager.resizeAllCharts();
        });
    }

    /**
     * Switch between tabs
     */
    switchTab(tabId) {
        // Update navigation
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.remove('active');
        });
        document.querySelector(`[data-tab="${tabId}"]`).classList.add('active');

        // Update content
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });
        document.getElementById(tabId).classList.add('active');

        this.currentTab = tabId;

        // Load tab-specific data
        this.loadTabData(tabId);
    }

    /**
     * Load tab-specific data
     */
    async loadTabData(tabId) {
        try {
            switch (tabId) {
                case 'dashboard':
                    await this.loadDashboardData();
                    break;
                case 'analytics':
                    await this.loadAnalyticsData();
                    break;
                case 'search':
                    // Search is loaded on demand
                    break;
            }
        } catch (error) {
            console.error(`Error loading ${tabId} data:`, error);
        }
    }

    /**
     * Load dashboard data
     */
    async loadDashboardData() {
        try {
            this.showLoading(true);

            // Load contracts from GitHub storage
            if (this.githubStorage.isOnline) {
                this.contracts = await this.githubStorage.searchContracts();
                
                // Update statistics
                const stats = await this.githubStorage.getContractStatistics();
                this.updateDashboardStats(stats);
                
                // Update charts
                this.updateDashboardCharts();
                
                // Update recent contracts
                this.updateRecentContracts();
            } else {
                this.showMessage('GitHub storage not available. Please configure your settings.', 'warning');
            }
        } catch (error) {
            console.error('Error loading dashboard data:', error);
            this.showMessage('Failed to load dashboard data', 'error');
        } finally {
            this.showLoading(false);
        }
    }

    /**
     * Update dashboard statistics
     */
    updateDashboardStats(stats) {
        const totalElement = document.getElementById('total-contracts');
        const ethereumElement = document.getElementById('ethereum-contracts');
        const baseElement = document.getElementById('base-contracts');
        const lastUpdatedElement = document.getElementById('last-updated');

        if (totalElement) totalElement.textContent = stats.total_contracts || 0;
        if (ethereumElement) ethereumElement.textContent = stats.chains?.ethereum || 0;
        if (baseElement) baseElement.textContent = stats.chains?.base || 0;
        
        if (lastUpdatedElement && stats.last_updated) {
            const date = new Date(stats.last_updated);
            lastUpdatedElement.textContent = date.toLocaleDateString();
        }
    }

    /**
     * Update dashboard charts
     */
    updateDashboardCharts() {
        if (this.contracts.length === 0) return;

        // Distribution chart
        const chainCounts = this.contracts.reduce((acc, contract) => {
            acc[contract.chain] = (acc[contract.chain] || 0) + 1;
            return acc;
        }, {});
        
        this.chartsManager.updateDistributionChart(chainCounts);

        // Timeline chart (simplified - by day)
        const timelineData = this.generateTimelineData();
        this.chartsManager.updateTimelineChart(timelineData);
    }

    /**
     * Generate timeline data
     */
    generateTimelineData() {
        const timeline = {};
        
        this.contracts.forEach(contract => {
            const date = contract.stored_at ? contract.stored_at.split('T')[0] : new Date().toISOString().split('T')[0];
            timeline[date] = (timeline[date] || 0) + 1;
        });

        return Object.entries(timeline).map(([date, count]) => ({ date, count }));
    }

    /**
     * Update recent contracts
     */
    updateRecentContracts() {
        const container = document.getElementById('recent-contracts');
        if (!container) return;

        const recent = this.contracts
            .sort((a, b) => new Date(b.stored_at || 0) - new Date(a.stored_at || 0))
            .slice(0, 5);

        if (recent.length === 0) {
            container.innerHTML = '<p class="text-gray-400">No contracts found</p>';
            return;
        }

        container.innerHTML = recent.map(contract => `
            <div class="contract-card">
                <div class="flex justify-between items-start">
                    <div class="flex-1">
                        <h4 class="font-semibold text-lg">${contract.name || 'Unknown'}</h4>
                        <p class="text-gray-400 text-sm">${contract.address}</p>
                        <p class="text-gray-300 text-sm mt-1">
                            <span class="capitalize">${contract.chain}</span> • 
                            ${contract.verified ? 'Verified' : 'Unverified'}
                        </p>
                    </div>
                    <div class="text-right">
                        <span class="inline-block px-2 py-1 text-xs rounded-full ${
                            contract.chain === 'ethereum' ? 'bg-purple-500' : 'bg-blue-500'
                        } text-white">
                            ${contract.chain === 'ethereum' ? 'ETH' : 'BASE'}
                        </span>
                    </div>
                </div>
            </div>
        `).join('');
    }

    /**
     * Discover a new contract
     */
    async discoverContract() {
        const addressInput = document.getElementById('contract-address');
        const networkSelect = document.getElementById('network-select');
        const resultsContainer = document.getElementById('discovery-results');

        if (!addressInput || !networkSelect) return;

        const address = addressInput.value.trim();
        const network = networkSelect.value;

        if (!address) {
            this.showMessage('Please enter a contract address', 'warning');
            return;
        }

        if (!this.blockchainAPI.isValidAddress(address)) {
            this.showMessage('Please enter a valid Ethereum address', 'error');
            return;
        }

        try {
            this.showLoading(true);
            resultsContainer.innerHTML = '<p class="text-gray-400">Discovering contract...</p>';
            resultsContainer.classList.remove('hidden');

            // Fetch contract data
            const contractData = await this.blockchainAPI.getContractData(address, network);
            
            // Analyze contract
            const analysis = this.contractAnalyzer.analyzeContract(contractData);
            contractData.analysis = analysis;

            // Store in GitHub
            if (this.githubStorage.isOnline) {
                await this.githubStorage.storeContract(contractData);
                this.showMessage('Contract discovered and stored successfully!', 'success');
            }

            // Add to local contracts array
            this.contracts.push(contractData);

            // Display results
            this.displayDiscoveryResults(contractData, analysis);

            // Refresh dashboard
            await this.loadDashboardData();

            // Clear form
            addressInput.value = '';

        } catch (error) {
            console.error('Error discovering contract:', error);
            this.showMessage(`Discovery failed: ${error.message}`, 'error');
            resultsContainer.innerHTML = `<p class="text-red-400">Error: ${error.message}</p>`;
        } finally {
            this.showLoading(false);
        }
    }

    /**
     * Display discovery results
     */
    displayDiscoveryResults(contractData, analysis) {
        const container = document.getElementById('discovery-results');
        
        const summary = this.contractAnalyzer.generateSummary(analysis);
        
        container.innerHTML = `
            <div class="contract-card">
                <h3 class="text-xl font-bold mb-4">Discovery Results</h3>
                
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                        <h4 class="font-semibold mb-2">Basic Information</h4>
                        <div class="space-y-2 text-sm">
                            <p><strong>Name:</strong> ${contractData.name}</p>
                            <p><strong>Address:</strong> <span class="font-mono">${contractData.address}</span></p>
                            <p><strong>Chain:</strong> <span class="capitalize">${contractData.chain}</span></p>
                            <p><strong>Verified:</strong> ${contractData.verified ? 'Yes' : 'No'}</p>
                            <p><strong>Compiler:</strong> ${contractData.compiler_version}</p>
                        </div>
                    </div>
                    
                    <div>
                        <h4 class="font-semibold mb-2">Analysis Summary</h4>
                        <div class="space-y-2 text-sm">
                            <p><strong>Overall Score:</strong> ${analysis.overall_score}/100</p>
                            <p><strong>Security Risk:</strong> 
                                <span class="capitalize ${this.getRiskColorClass(analysis.security_analysis.risk_level)}">
                                    ${analysis.security_analysis.risk_level}
                                </span>
                            </p>
                            <p><strong>Functions:</strong> ${analysis.function_analysis.total_functions}</p>
                            <p><strong>Events:</strong> ${analysis.event_analysis.total_events}</p>
                        </div>
                    </div>
                </div>
                
                ${analysis.token_analysis.is_token ? `
                    <div class="mt-4 p-4 bg-blue-500 bg-opacity-20 rounded-lg">
                        <h4 class="font-semibold text-blue-300">Token Detected</h4>
                        <p class="text-sm">Type: ${analysis.token_analysis.token_type}</p>
                        <p class="text-sm">Standards: ${analysis.token_analysis.standards.join(', ')}</p>
                    </div>
                ` : ''}
                
                ${analysis.defi_analysis.is_defi ? `
                    <div class="mt-4 p-4 bg-green-500 bg-opacity-20 rounded-lg">
                        <h4 class="font-semibold text-green-300">DeFi Protocol Detected</h4>
                        <p class="text-sm">Protocols: ${analysis.defi_analysis.protocols.join(', ')}</p>
                    </div>
                ` : ''}
                
                <div class="mt-4">
                    <button onclick="this.parentElement.parentElement.classList.add('hidden')" 
                            class="btn-secondary">
                        Close
                    </button>
                </div>
            </div>
        `;
    }

    /**
     * Search contracts
     */
    async searchContracts() {
        const searchTerm = document.getElementById('search-term')?.value.trim();
        const searchNetwork = document.getElementById('search-network')?.value;
        const searchVerified = document.getElementById('search-verified')?.value;
        const resultsContainer = document.getElementById('search-results');

        if (!resultsContainer) return;

        try {
            this.showLoading(true);

            const filters = {};
            if (searchNetwork) filters.chain = searchNetwork;
            if (searchVerified !== '') filters.verified = searchVerified === 'true';
            if (searchTerm) {
                filters.name_filter = searchTerm;
                filters.address_filter = searchTerm;
            }

            let results = [];
            if (this.githubStorage.isOnline) {
                results = await this.githubStorage.searchContracts(filters);
            } else {
                // Filter local contracts
                results = this.contracts.filter(contract => {
                    if (filters.chain && contract.chain !== filters.chain) return false;
                    if (filters.verified !== undefined && contract.verified !== filters.verified) return false;
                    if (searchTerm) {
                        const term = searchTerm.toLowerCase();
                        return contract.name?.toLowerCase().includes(term) ||
                               contract.address?.toLowerCase().includes(term);
                    }
                    return true;
                });
            }

            this.displaySearchResults(results);

        } catch (error) {
            console.error('Error searching contracts:', error);
            this.showMessage('Search failed', 'error');
        } finally {
            this.showLoading(false);
        }
    }

    /**
     * Display search results
     */
    displaySearchResults(results) {
        const container = document.getElementById('search-results');
        
        if (results.length === 0) {
            container.innerHTML = '<p class="text-gray-400">No contracts found matching your criteria</p>';
            return;
        }

        container.innerHTML = results.map(contract => `
            <div class="contract-card">
                <div class="flex justify-between items-start">
                    <div class="flex-1">
                        <h4 class="font-semibold text-lg">${contract.name || 'Unknown'}</h4>
                        <p class="text-gray-400 text-sm font-mono">${contract.address}</p>
                        <div class="flex items-center space-x-4 mt-2 text-sm">
                            <span class="capitalize">${contract.chain}</span>
                            <span class="${contract.verified ? 'text-green-400' : 'text-red-400'}">
                                ${contract.verified ? 'Verified' : 'Unverified'}
                            </span>
                            ${contract.stored_at ? `
                                <span class="text-gray-400">
                                    ${new Date(contract.stored_at).toLocaleDateString()}
                                </span>
                            ` : ''}
                        </div>
                    </div>
                    <div class="text-right">
                        <span class="inline-block px-2 py-1 text-xs rounded-full ${
                            contract.chain === 'ethereum' ? 'bg-purple-500' : 'bg-blue-500'
                        } text-white">
                            ${contract.chain === 'ethereum' ? 'ETH' : 'BASE'}
                        </span>
                        <button onclick="window.app.viewContractDetails('${contract.address}', '${contract.chain}')" 
                                class="block mt-2 text-blue-400 hover:text-blue-300 text-sm">
                            View Details
                        </button>
                    </div>
                </div>
            </div>
        `).join('');
    }

    /**
     * View contract details
     */
    async viewContractDetails(address, chain) {
        try {
            this.showLoading(true);
            
            let contract = this.contracts.find(c => c.address === address && c.chain === chain);
            
            if (!contract && this.githubStorage.isOnline) {
                contract = await this.githubStorage.getContract(address, chain);
            }

            if (!contract) {
                this.showMessage('Contract not found', 'error');
                return;
            }

            // Create and show modal with contract details
            this.showContractDetailsModal(contract);

        } catch (error) {
            console.error('Error loading contract details:', error);
            this.showMessage('Failed to load contract details', 'error');
        } finally {
            this.showLoading(false);
        }
    }

    /**
     * Show contract details modal
     */
    showContractDetailsModal(contract) {
        const modalHTML = `
            <div class="modal show" id="contract-details-modal">
                <div class="modal-content" style="max-width: 4xl;">
                    <div class="flex justify-between items-center mb-6">
                        <h3 class="text-2xl font-bold">${contract.name || 'Contract Details'}</h3>
                        <button onclick="document.getElementById('contract-details-modal').remove()" 
                                class="text-gray-400 hover:text-white">
                            <i class="fas fa-times text-xl"></i>
                        </button>
                    </div>
                    
                    <div class="space-y-6">
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div>
                                <h4 class="font-semibold mb-2">Contract Information</h4>
                                <div class="space-y-1 text-sm">
                                    <p><strong>Address:</strong> <span class="font-mono">${contract.address}</span></p>
                                    <p><strong>Chain:</strong> <span class="capitalize">${contract.chain}</span></p>
                                    <p><strong>Verified:</strong> ${contract.verified ? 'Yes' : 'No'}</p>
                                    <p><strong>Compiler:</strong> ${contract.compiler_version || 'Unknown'}</p>
                                </div>
                            </div>
                            <div>
                                <h4 class="font-semibold mb-2">Analysis</h4>
                                <div class="space-y-1 text-sm">
                                    ${contract.analysis ? `
                                        <p><strong>Overall Score:</strong> ${contract.analysis.overall_score}/100</p>
                                        <p><strong>Security Risk:</strong> 
                                            <span class="capitalize ${this.getRiskColorClass(contract.analysis.security_analysis.risk_level)}">
                                                ${contract.analysis.security_analysis.risk_level}
                                            </span>
                                        </p>
                                        <p><strong>Functions:</strong> ${contract.analysis.function_analysis.total_functions}</p>
                                        <p><strong>Events:</strong> ${contract.analysis.event_analysis.total_events}</p>
                                    ` : '<p>No analysis available</p>'}
                                </div>
                            </div>
                        </div>
                        
                        ${contract.source_code ? `
                            <div>
                                <h4 class="font-semibold mb-2">Source Code (Preview)</h4>
                                <div class="code-block max-h-64 overflow-y-auto">
                                    <pre><code>${contract.source_code.substring(0, 2000)}${contract.source_code.length > 2000 ? '...' : ''}</code></pre>
                                </div>
                            </div>
                        ` : ''}
                        
                        ${contract.abi ? `
                            <div>
                                <h4 class="font-semibold mb-2">ABI (Preview)</h4>
                                <div class="code-block max-h-64 overflow-y-auto">
                                    <pre><code>${JSON.stringify(JSON.parse(contract.abi), null, 2).substring(0, 1000)}...</code></pre>
                                </div>
                            </div>
                        ` : ''}
                    </div>
                </div>
            </div>
        `;

        document.body.insertAdjacentHTML('beforeend', modalHTML);
    }

    /**
     * Load analytics data
     */
    async loadAnalyticsData() {
        try {
            this.showLoading(true);

            if (this.contracts.length === 0) {
                this.showMessage('No contracts available for analysis', 'info');
                return;
            }

            // Update compiler versions chart
            const compilerVersions = this.contracts.reduce((acc, contract) => {
                const version = contract.compiler_version || 'Unknown';
                acc[version] = (acc[version] || 0) + 1;
                return acc;
            }, {});

            this.chartsManager.updateCompilerChart(compilerVersions);

            // Update optimization chart
            const optimization = this.contracts.reduce((acc, contract) => {
                if (contract.optimization) {
                    acc.optimized++;
                } else {
                    acc.not_optimized++;
                }
                return acc;
            }, { optimized: 0, not_optimized: 0 });

            this.chartsManager.updateOptimizationChart(optimization);

        } catch (error) {
            console.error('Error loading analytics data:', error);
            this.showMessage('Failed to load analytics data', 'error');
        } finally {
            this.showLoading(false);
        }
    }

    /**
     * Export data
     */
    async exportData(format) {
        try {
            this.showLoading(true);

            let data;
            let filename;
            let mimeType;

            if (format === 'csv') {
                data = await this.githubStorage.exportContractsCSV();
                filename = `web3-loc-contracts-${new Date().toISOString().split('T')[0]}.csv`;
                mimeType = 'text/csv';
            } else if (format === 'json') {
                data = await this.githubStorage.exportContractsJSON();
                filename = `web3-loc-contracts-${new Date().toISOString().split('T')[0]}.json`;
                mimeType = 'application/json';
            }

            // Create and download file
            const blob = new Blob([data], { type: mimeType });
            const url = URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.download = filename;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            URL.revokeObjectURL(url);

            this.showMessage(`Data exported successfully as ${filename}`, 'success');

        } catch (error) {
            console.error('Error exporting data:', error);
            this.showMessage('Export failed', 'error');
        } finally {
            this.showLoading(false);
        }
    }

    /**
     * Save settings
     */
    saveSettings() {
        const etherscanKey = document.getElementById('etherscan-key')?.value;
        const basescanKey = document.getElementById('basescan-key')?.value;
        const githubRepo = document.getElementById('github-repo')?.value;
        const githubToken = document.getElementById('github-token')?.value;

        if (etherscanKey) {
            localStorage.setItem('etherscan_key', etherscanKey);
            this.blockchainAPI.etherscanKey = etherscanKey;
        }
        
        if (basescanKey) {
            localStorage.setItem('basescan_key', basescanKey);
            this.blockchainAPI.basescanKey = basescanKey;
        }
        
        if (githubRepo) {
            localStorage.setItem('github_repo', githubRepo);
            this.githubStorage.repo = githubRepo;
        }
        
        if (githubToken) {
            localStorage.setItem('github_token', githubToken);
            this.githubStorage.token = githubToken;
        }

        this.showMessage('Settings saved successfully', 'success');
        document.getElementById('settings-modal').classList.remove('show');
    }

    /**
     * Load settings
     */
    loadSettings() {
        const etherscanKey = localStorage.getItem('etherscan_key');
        const basescanKey = localStorage.getItem('basescan_key');
        const githubRepo = localStorage.getItem('github_repo');
        const githubToken = localStorage.getItem('github_token');

        if (etherscanKey) {
            this.blockchainAPI.etherscanKey = etherscanKey;
            const input = document.getElementById('etherscan-key');
            if (input) input.value = etherscanKey;
        }
        
        if (basescanKey) {
            this.blockchainAPI.basescanKey = basescanKey;
            const input = document.getElementById('basescan-key');
            if (input) input.value = basescanKey;
        }
        
        if (githubRepo) {
            this.githubStorage.repo = githubRepo;
            const input = document.getElementById('github-repo');
            if (input) input.value = githubRepo;
        }
        
        if (githubToken) {
            this.githubStorage.token = githubToken;
            const input = document.getElementById('github-token');
            if (input) input.value = githubToken;
        }
    }

    /**
     * Test connections
     */
    async testConnections() {
        const statusElement = document.getElementById('connection-status');
        
        if (statusElement) {
            statusElement.innerHTML = `
                <div class="status-connecting"></div>
                <span class="text-sm">Testing connections...</span>
            `;
        }

        try {
            // Test GitHub connection
            if (this.githubStorage.token && this.githubStorage.repo) {
                await this.githubStorage.testConnection();
                console.log('GitHub connection successful');
            }

            // Test blockchain APIs
            let ethereumOk = false;
            let baseOk = false;

            if (this.blockchainAPI.etherscanKey) {
                ethereumOk = await this.blockchainAPI.testConnection('ethereum');
            }

            if (this.blockchainAPI.basescanKey) {
                baseOk = await this.blockchainAPI.testConnection('base');
            }

            // Update status
            const isOnline = this.githubStorage.isOnline && (ethereumOk || baseOk);
            
            if (statusElement) {
                statusElement.innerHTML = `
                    <div class="${isOnline ? 'status-online' : 'status-offline'}"></div>
                    <span class="text-sm">${isOnline ? 'Connected' : 'Offline'}</span>
                `;
            }

            if (isOnline) {
                this.showMessage('All connections successful', 'success');
            } else {
                this.showMessage('Some connections failed. Check your settings.', 'warning');
            }

        } catch (error) {
            console.error('Connection test failed:', error);
            
            if (statusElement) {
                statusElement.innerHTML = `
                    <div class="status-offline"></div>
                    <span class="text-sm">Connection failed</span>
                `;
            }
            
            this.showMessage('Connection test failed', 'error');
        }
    }

    /**
     * Show loading overlay
     */
    showLoading(show) {
        const overlay = document.getElementById('loading-overlay');
        if (overlay) {
            if (show) {
                overlay.classList.remove('hidden');
            } else {
                overlay.classList.add('hidden');
            }
        }
        this.isLoading = show;
    }

    /**
     * Show message to user
     */
    showMessage(message, type = 'info') {
        const messageHTML = `
            <div class="message-${type} fixed top-20 right-4 z-50 max-w-sm" style="animation: slideIn 0.3s ease-out;">
                <div class="flex items-center">
                    <i class="fas fa-${this.getMessageIcon(type)} mr-2"></i>
                    <span>${message}</span>
                    <button onclick="this.parentElement.parentElement.remove()" class="ml-auto text-current opacity-70 hover:opacity-100">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
            </div>
        `;

        document.body.insertAdjacentHTML('beforeend', messageHTML);

        // Auto-remove after 5 seconds
        setTimeout(() => {
            const messageElement = document.body.lastElementChild;
            if (messageElement && messageElement.classList.contains(`message-${type}`)) {
                messageElement.remove();
            }
        }, 5000);
    }

    /**
     * Get message icon
     */
    getMessageIcon(type) {
        const icons = {
            success: 'check-circle',
            error: 'exclamation-circle',
            warning: 'exclamation-triangle',
            info: 'info-circle'
        };
        return icons[type] || 'info-circle';
    }

    /**
     * Get risk color class
     */
    getRiskColorClass(riskLevel) {
        const colors = {
            low: 'text-green-400',
            medium: 'text-yellow-400',
            high: 'text-red-400'
        };
        return colors[riskLevel] || 'text-gray-400';
    }
}

// Initialize application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.app = new Web3LOCApp();
});

// Add slide-in animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
`;
document.head.appendChild(style);
