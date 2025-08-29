/**
 * Charts Manager for Web3.LOC
 * Handles all chart visualizations using Chart.js
 */

class ChartsManager {
    constructor() {
        this.charts = {};
        this.defaultColors = [
            '#3B82F6', '#8B5CF6', '#EF4444', '#10B981', '#F59E0B',
            '#EC4899', '#06B6D4', '#84CC16', '#F97316', '#6366F1'
        ];
    }

    /**
     * Initialize all charts
     */
    initializeCharts() {
        this.createDistributionChart();
        this.createTimelineChart();
        this.createCompilerChart();
        this.createOptimizationChart();
    }

    /**
     * Create contract distribution chart
     */
    createDistributionChart() {
        const ctx = document.getElementById('distributionChart');
        if (!ctx) return;

        this.charts.distribution = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Ethereum', 'Base'],
                datasets: [{
                    data: [0, 0],
                    backgroundColor: [this.defaultColors[0], this.defaultColors[1]],
                    borderWidth: 2,
                    borderColor: '#1F2937'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: '#E5E7EB',
                            usePointStyle: true,
                            padding: 20
                        }
                    },
                    tooltip: {
                        backgroundColor: '#1F2937',
                        titleColor: '#E5E7EB',
                        bodyColor: '#E5E7EB',
                        borderColor: '#374151',
                        borderWidth: 1
                    }
                },
                elements: {
                    arc: {
                        borderWidth: 2
                    }
                }
            }
        });
    }

    /**
     * Create timeline chart
     */
    createTimelineChart() {
        const ctx = document.getElementById('timelineChart');
        if (!ctx) return;

        this.charts.timeline = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Contracts Discovered',
                    data: [],
                    borderColor: this.defaultColors[0],
                    backgroundColor: this.defaultColors[0] + '20',
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: this.defaultColors[0],
                    pointBorderColor: '#1F2937',
                    pointBorderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: {
                            color: '#E5E7EB'
                        }
                    },
                    tooltip: {
                        backgroundColor: '#1F2937',
                        titleColor: '#E5E7EB',
                        bodyColor: '#E5E7EB',
                        borderColor: '#374151',
                        borderWidth: 1
                    }
                },
                scales: {
                    x: {
                        ticks: {
                            color: '#9CA3AF'
                        },
                        grid: {
                            color: '#374151'
                        }
                    },
                    y: {
                        ticks: {
                            color: '#9CA3AF'
                        },
                        grid: {
                            color: '#374151'
                        }
                    }
                }
            }
        });
    }

    /**
     * Create compiler version chart
     */
    createCompilerChart() {
        const ctx = document.getElementById('compilerChart');
        if (!ctx) return;

        this.charts.compiler = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: [],
                datasets: [{
                    label: 'Contracts',
                    data: [],
                    backgroundColor: this.defaultColors[2],
                    borderColor: '#1F2937',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: {
                            color: '#E5E7EB'
                        }
                    },
                    tooltip: {
                        backgroundColor: '#1F2937',
                        titleColor: '#E5E7EB',
                        bodyColor: '#E5E7EB',
                        borderColor: '#374151',
                        borderWidth: 1
                    }
                },
                scales: {
                    x: {
                        ticks: {
                            color: '#9CA3AF'
                        },
                        grid: {
                            color: '#374151'
                        }
                    },
                    y: {
                        ticks: {
                            color: '#9CA3AF'
                        },
                        grid: {
                            color: '#374151'
                        }
                    }
                }
            }
        });
    }

    /**
     * Create optimization chart
     */
    createOptimizationChart() {
        const ctx = document.getElementById('optimizationChart');
        if (!ctx) return;

        this.charts.optimization = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: ['Optimized', 'Not Optimized'],
                datasets: [{
                    data: [0, 0],
                    backgroundColor: [this.defaultColors[3], this.defaultColors[4]],
                    borderWidth: 2,
                    borderColor: '#1F2937'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: '#E5E7EB',
                            usePointStyle: true,
                            padding: 20
                        }
                    },
                    tooltip: {
                        backgroundColor: '#1F2937',
                        titleColor: '#E5E7EB',
                        bodyColor: '#E5E7EB',
                        borderColor: '#374151',
                        borderWidth: 1
                    }
                }
            }
        });
    }

    /**
     * Update distribution chart
     */
    updateDistributionChart(data) {
        if (!this.charts.distribution) return;

        this.charts.distribution.data.datasets[0].data = [
            data.ethereum || 0,
            data.base || 0
        ];
        this.charts.distribution.update();
    }

    /**
     * Update timeline chart
     */
    updateTimelineChart(data) {
        if (!this.charts.timeline) return;

        const sortedData = data.sort((a, b) => new Date(a.date) - new Date(b.date));
        
        this.charts.timeline.data.labels = sortedData.map(item => 
            new Date(item.date).toLocaleDateString()
        );
        this.charts.timeline.data.datasets[0].data = sortedData.map(item => item.count);
        
        this.charts.timeline.update();
    }

    /**
     * Update compiler chart
     */
    updateCompilerChart(data) {
        if (!this.charts.compiler) return;

        const compilerVersions = Object.keys(data).slice(0, 10); // Top 10 versions
        const counts = compilerVersions.map(version => data[version]);

        this.charts.compiler.data.labels = compilerVersions.map(version => 
            version.replace('v', '').split('+')[0] // Clean version string
        );
        this.charts.compiler.data.datasets[0].data = counts;
        this.charts.compiler.data.datasets[0].backgroundColor = this.defaultColors.slice(0, compilerVersions.length);
        
        this.charts.compiler.update();
    }

    /**
     * Update optimization chart
     */
    updateOptimizationChart(data) {
        if (!this.charts.optimization) return;

        this.charts.optimization.data.datasets[0].data = [
            data.optimized || 0,
            data.not_optimized || 0
        ];
        this.charts.optimization.update();
    }

    /**
     * Create custom chart for analytics
     */
    createCustomChart(containerId, type, data, options = {}) {
        const ctx = document.getElementById(containerId);
        if (!ctx) return null;

        const defaultOptions = {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: {
                        color: '#E5E7EB'
                    }
                },
                tooltip: {
                    backgroundColor: '#1F2937',
                    titleColor: '#E5E7EB',
                    bodyColor: '#E5E7EB',
                    borderColor: '#374151',
                    borderWidth: 1
                }
            }
        };

        if (type === 'bar' || type === 'line') {
            defaultOptions.scales = {
                x: {
                    ticks: {
                        color: '#9CA3AF'
                    },
                    grid: {
                        color: '#374151'
                    }
                },
                y: {
                    ticks: {
                        color: '#9CA3AF'
                    },
                    grid: {
                        color: '#374151'
                    }
                }
            };
        }

        const mergedOptions = this.mergeDeep(defaultOptions, options);

        return new Chart(ctx, {
            type: type,
            data: data,
            options: mergedOptions
        });
    }

    /**
     * Generate chart data for token analysis
     */
    generateTokenAnalysisData(contracts) {
        const tokenTypes = {};
        const tokenFeatures = {};

        contracts.forEach(contract => {
            if (contract.analysis && contract.analysis.token_analysis) {
                const tokenAnalysis = contract.analysis.token_analysis;
                
                if (tokenAnalysis.is_token) {
                    const type = tokenAnalysis.token_type || 'Unknown';
                    tokenTypes[type] = (tokenTypes[type] || 0) + 1;
                    
                    tokenAnalysis.token_features?.forEach(feature => {
                        tokenFeatures[feature] = (tokenFeatures[feature] || 0) + 1;
                    });
                }
            }
        });

        return { tokenTypes, tokenFeatures };
    }

    /**
     * Generate chart data for DeFi analysis
     */
    generateDeFiAnalysisData(contracts) {
        const protocols = {};
        const features = {};

        contracts.forEach(contract => {
            if (contract.analysis && contract.analysis.defi_analysis) {
                const defiAnalysis = contract.analysis.defi_analysis;
                
                if (defiAnalysis.is_defi) {
                    defiAnalysis.protocols?.forEach(protocol => {
                        protocols[protocol] = (protocols[protocol] || 0) + 1;
                    });
                    
                    defiAnalysis.defi_features?.forEach(feature => {
                        features[feature] = (features[feature] || 0) + 1;
                    });
                }
            }
        });

        return { protocols, features };
    }

    /**
     * Generate chart data for security analysis
     */
    generateSecurityAnalysisData(contracts) {
        const riskLevels = { low: 0, medium: 0, high: 0, unknown: 0 };
        const securityIssues = {};

        contracts.forEach(contract => {
            if (contract.analysis && contract.analysis.security_analysis) {
                const securityAnalysis = contract.analysis.security_analysis;
                
                const riskLevel = securityAnalysis.risk_level || 'unknown';
                riskLevels[riskLevel]++;
                
                securityAnalysis.issues?.forEach(issue => {
                    const key = issue.description.substring(0, 50);
                    securityIssues[key] = (securityIssues[key] || 0) + 1;
                });
            }
        });

        return { riskLevels, securityIssues };
    }

    /**
     * Destroy all charts
     */
    destroyAllCharts() {
        Object.values(this.charts).forEach(chart => {
            if (chart && typeof chart.destroy === 'function') {
                chart.destroy();
            }
        });
        this.charts = {};
    }

    /**
     * Resize all charts
     */
    resizeAllCharts() {
        Object.values(this.charts).forEach(chart => {
            if (chart && typeof chart.resize === 'function') {
                chart.resize();
            }
        });
    }

    /**
     * Deep merge objects
     */
    mergeDeep(target, source) {
        const result = Object.assign({}, target);
        
        if (this.isObject(target) && this.isObject(source)) {
            Object.keys(source).forEach(key => {
                if (this.isObject(source[key])) {
                    if (!(key in target)) {
                        Object.assign(result, { [key]: source[key] });
                    } else {
                        result[key] = this.mergeDeep(target[key], source[key]);
                    }
                } else {
                    Object.assign(result, { [key]: source[key] });
                }
            });
        }
        
        return result;
    }

    /**
     * Check if value is object
     */
    isObject(item) {
        return item && typeof item === 'object' && !Array.isArray(item);
    }
}

// Export for use in other modules
window.ChartsManager = ChartsManager;
