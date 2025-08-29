/**
 * GitHub Storage Manager for Web3.LOC
 * Centralized public storage for smart contract discovery
 */

class GitHubStorage {
    constructor() {
        this.baseUrl = 'https://api.github.com';
        this.repo = 'Web3LOC/contract-storage';
        this.rawBase = 'https://raw.githubusercontent.com/Web3LOC/contract-storage/main';
        this.cache = new Map();
        this.isOnline = false;
    }

    /**
     * Test GitHub connection
     */
    async testConnection() {
        try {
            const response = await fetch(`${this.baseUrl}/repos/${this.repo}`, {
                headers: {
                    'Accept': 'application/vnd.github.v3+json'
                }
            });

            if (!response.ok) {
                throw new Error(`GitHub API error: ${response.status} ${response.statusText}`);
            }

            this.isOnline = true;
            return await response.json();
        } catch (error) {
            this.isOnline = false;
            throw error;
        }
    }

    /**
     * Search contracts in centralized repository
     */
    async searchContracts(filters = {}) {
        try {
            const index = await this.getContractIndex();
            let contracts = index.contracts || [];

            // Apply filters
            if (filters.chain) {
                contracts = contracts.filter(c => c.chain === filters.chain);
            }

            if (filters.name_filter) {
                const searchTerm = filters.name_filter.toLowerCase();
                contracts = contracts.filter(c => 
                    c.name?.toLowerCase().includes(searchTerm) ||
                    c.address?.toLowerCase().includes(searchTerm)
                );
            }

            if (filters.address_filter) {
                const addressFilter = filters.address_filter.toLowerCase();
                contracts = contracts.filter(c => 
                    c.address?.toLowerCase().includes(addressFilter)
                );
            }

            if (filters.type) {
                contracts = contracts.filter(c => c.type === filters.type);
            }

            if (filters.date_range) {
                const now = new Date();
                let cutoffDate;
                
                switch (filters.date_range) {
                    case '24h':
                        cutoffDate = new Date(now.getTime() - 24 * 60 * 60 * 1000);
                        break;
                    case '7d':
                        cutoffDate = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
                        break;
                    case '30d':
                        cutoffDate = new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000);
                        break;
                }
                
                if (cutoffDate) {
                    contracts = contracts.filter(c => 
                        new Date(c.stored_at) >= cutoffDate
                    );
                }
            }

            // Apply limit
            const limit = filters.limit || 50;
            contracts = contracts.slice(0, Math.min(limit, 500));

            return contracts;
        } catch (error) {
            console.error('Error searching contracts:', error);
            return [];
        }
    }

    /**
     * Get a specific contract
     */
    async getContract(contractId, chain) {
        const cacheKey = `${chain}_${contractId}`;
        
        if (this.cache.has(cacheKey)) {
            return this.cache.get(cacheKey);
        }

        try {
            const url = `${this.rawBase}/contracts/${chain}/contract_${contractId}.json`;
            const response = await fetch(url);

            if (!response.ok) {
                return null;
            }

            const contractData = await response.json();
            this.cache.set(cacheKey, contractData);
            return contractData;
        } catch (error) {
            console.error('Error getting contract:', error);
            return null;
        }
    }

    /**
     * Get contract statistics
     */
    async getContractStatistics() {
        try {
            const url = `${this.rawBase}/index/statistics.json`;
            const response = await fetch(url);
            
            if (response.ok) {
                return await response.json();
            } else {
                const index = await this.getContractIndex();
                return index.statistics || {
                    total_contracts: 0,
                    chains: { ethereum: 0, base: 0 },
                    last_updated: null
                };
            }
        } catch (error) {
            return {
                total_contracts: 0,
                chains: { ethereum: 0, base: 0 },
                last_updated: null
            };
        }
    }

    /**
     * Get contract index
     */
    async getContractIndex() {
        try {
            const url = `${this.rawBase}/index/contract_index.json`;
            const response = await fetch(url);

            if (response.ok) {
                return await response.json();
            } else {
                return {
                    contracts: [],
                    statistics: {
                        total_contracts: 0,
                        chains: { ethereum: 0, base: 0 },
                        last_updated: null
                    }
                };
            }
        } catch (error) {
            return {
                contracts: [],
                statistics: {
                    total_contracts: 0,
                    chains: { ethereum: 0, base: 0 },
                    last_updated: null
                }
            };
        }
    }

    /**
     * Get recent contracts
     */
    async getRecentContracts(limit = 10) {
        try {
            const contracts = await this.searchContracts({ limit });
            return contracts
                .sort((a, b) => new Date(b.stored_at) - new Date(a.stored_at))
                .slice(0, limit);
        } catch (error) {
            return [];
        }
    }

    /**
     * Export contracts as CSV
     */
    async exportContractsCSV(filters = {}) {
        try {
            const contracts = await this.searchContracts(filters);
            
            if (contracts.length === 0) {
                throw new Error('No contracts found to export');
            }

            const headers = [
                'Address', 'Chain', 'Name', 'Type', 'Verified', 
                'Compiler', 'Optimized', 'Stored Date'
            ];
            
            const rows = contracts.map(contract => [
                contract.address || '',
                contract.chain || '',
                contract.name || 'Unknown',
                contract.type || 'other',
                contract.verified ? 'Yes' : 'No',
                contract.compiler_version || 'Unknown',
                contract.optimization ? 'Yes' : 'No',
                contract.stored_at ? new Date(contract.stored_at).toLocaleDateString() : ''
            ]);

            const csvContent = [headers, ...rows]
                .map(row => row.map(field => `"${field}"`).join(','))
                .join('\n');

            return csvContent;
        } catch (error) {
            throw error;
        }
    }

    /**
     * Export contract as Solidity file
     */
    async exportContractSol(contractId, chain) {
        try {
            const contract = await this.getContract(contractId, chain);
            
            if (!contract) {
                throw new Error('Contract not found');
            }

            const header = `// SPDX-License-Identifier: MIT
// Contract discovered by Web3.LOC
// Network: ${contract.chain}
// Address: ${contract.address}
// Name: ${contract.name}

`;
            
            return header + contract.source_code;
        } catch (error) {
            throw error;
        }
    }

    /**
     * Export contract as README
     */
    async exportContractReadme(contractId, chain) {
        try {
            const contract = await this.getContract(contractId, chain);
            
            if (!contract) {
                throw new Error('Contract not found');
            }

            const readme = `# ${contract.name}

## Contract Information
- **Address**: ${contract.address}
- **Network**: ${contract.chain.charAt(0).toUpperCase() + contract.chain.slice(1)}
- **Type**: ${contract.type || 'Unknown'}
- **Verified**: ${contract.verified ? 'Yes' : 'No'}
- **Compiler**: ${contract.compiler_version || 'Unknown'}
- **Optimized**: ${contract.optimization ? 'Yes' : 'No'}

## Summary
${contract.summary || 'No summary available'}

## Source Code
\`\`\`solidity
${contract.source_code || 'Source code not available'}
\`\`\`

## ABI
\`\`\`json
${contract.abi || '[]'}
\`\`\`

---
*Generated by Web3.LOC - Smart Contract Discovery Platform*
`;

            return readme;
        } catch (error) {
            throw error;
        }
    }

    /**
     * Download file helper
     */
    downloadFile(content, filename, mimeType = 'text/plain') {
        const blob = new Blob([content], { type: mimeType });
        const url = URL.createObjectURL(blob);
        
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        
        URL.revokeObjectURL(url);
    }

    /**
     * Get analytics data
     */
    async getAnalyticsData() {
        try {
            const index = await this.getContractIndex();
            const contracts = index.contracts || [];

            const analytics = {
                total: contracts.length,
                by_chain: {},
                by_type: {},
                by_date: {},
                verification_rate: 0
            };

            // Count by chain
            contracts.forEach(contract => {
                analytics.by_chain[contract.chain] = (analytics.by_chain[contract.chain] || 0) + 1;
            });

            // Count by type
            contracts.forEach(contract => {
                const type = contract.type || 'other';
                analytics.by_type[type] = (analytics.by_type[type] || 0) + 1;
            });

            // Count by date (last 30 days)
            const last30Days = {};
            const now = new Date();
            
            for (let i = 0; i < 30; i++) {
                const date = new Date(now.getTime() - i * 24 * 60 * 60 * 1000);
                const dateStr = date.toISOString().split('T')[0];
                last30Days[dateStr] = 0;
            }

            contracts.forEach(contract => {
                if (contract.stored_at) {
                    const dateStr = contract.stored_at.split('T')[0];
                    if (last30Days.hasOwnProperty(dateStr)) {
                        last30Days[dateStr]++;
                    }
                }
            });

            analytics.by_date = last30Days;

            // Calculate verification rate
            const verifiedCount = contracts.filter(c => c.verified).length;
            analytics.verification_rate = contracts.length > 0 ? 
                Math.round((verifiedCount / contracts.length) * 100) : 0;

            return analytics;
        } catch (error) {
            return {
                total: 0,
                by_chain: {},
                by_type: {},
                by_date: {},
                verification_rate: 0
            };
        }
    }
}

// Make storage globally available
window.GitHubStorage = GitHubStorage;
