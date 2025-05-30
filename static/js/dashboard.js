// Dashboard JavaScript for interactive charts and functionality
class SurveyDashboard {
    constructor() {
        this.charts = {};
        this.init();
    }

    async init() {
        try {
            // Load chart data from API
            const response = await fetch('/api/chart-data');
            if (!response.ok) {
                throw new Error('Failed to load chart data');
            }
            
            const chartData = await response.json();
            
            // Initialize all charts
            this.initIDEChart(chartData.ide_chart);
            this.initSatisfactionChart(chartData.satisfaction_chart);
            this.initFeedbackChart(chartData.feedback_chart);
            
            // Initialize interactions
            this.initInteractions();
            
            // Add fade-in animations
            this.addAnimations();
            
        } catch (error) {
            console.error('Error initializing dashboard:', error);
            this.showError('Failed to load chart data. Please refresh the page.');
        }
    }

    initIDEChart(data) {
        const ctx = document.getElementById('ideChart');
        if (!ctx) return;

        this.charts.ideChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'Desenvolvedores',
                    data: data.data,
                    backgroundColor: data.backgroundColor,
                    borderColor: '#2563EB',
                    borderWidth: 2,
                    borderRadius: 8,
                    borderSkipped: false
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: 'rgba(37, 99, 235, 0.9)',
                        titleColor: '#ffffff',
                        bodyColor: '#ffffff',
                        borderColor: '#2563EB',
                        borderWidth: 1,
                        cornerRadius: 8,
                        callbacks: {
                            label: function(context) {
                                return `${context.parsed.y} desenvolvedores`;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1,
                            color: '#6B7280'
                        },
                        grid: {
                            color: 'rgba(229, 231, 235, 0.5)'
                        }
                    },
                    x: {
                        ticks: {
                            color: '#6B7280',
                            maxRotation: 45
                        },
                        grid: {
                            display: false
                        }
                    }
                },
                animation: {
                    duration: 1500,
                    easing: 'easeOutQuart'
                }
            }
        });
    }

    initSatisfactionChart(data) {
        const ctx = document.getElementById('satisfactionChart');
        if (!ctx) return;

        this.charts.satisfactionChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: data.labels,
                datasets: [{
                    data: data.data,
                    backgroundColor: data.backgroundColor,
                    borderWidth: 3,
                    borderColor: '#ffffff',
                    hoverBorderWidth: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            usePointStyle: true,
                            pointStyle: 'circle',
                            padding: 20,
                            color: '#1F2937',
                            font: {
                                size: 12,
                                family: 'Inter'
                            }
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(37, 99, 235, 0.9)',
                        titleColor: '#ffffff',
                        bodyColor: '#ffffff',
                        borderColor: '#2563EB',
                        borderWidth: 1,
                        cornerRadius: 8,
                        callbacks: {
                            label: function(context) {
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = ((context.parsed / total) * 100).toFixed(1);
                                return `${context.label}: ${context.parsed} (${percentage}%)`;
                            }
                        }
                    }
                },
                cutout: '60%',
                animation: {
                    animateRotate: true,
                    animateScale: true,
                    duration: 1500,
                    easing: 'easeOutQuart'
                }
            }
        });
    }

    initFeedbackChart(chartData) {
        const ctx = document.getElementById('feedbackChart');
        if (!ctx) return;

        // Combine likes and dislikes data
        const likesData = chartData.likes;
        const dislikesData = chartData.dislikes;
        
        // Create a horizontal bar chart showing top feedback themes
        const allLabels = [...likesData.labels, ...dislikesData.labels];
        const allData = [...likesData.data.map(val => val), ...dislikesData.data.map(val => -val)]; // Negative for dislikes
        const colors = [
            ...Array(likesData.data.length).fill('#10B981'), // Green for likes
            ...Array(dislikesData.data.length).fill('#EF4444')  // Red for dislikes
        ];

        this.charts.feedbackChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: allLabels,
                datasets: [{
                    label: 'Feedback',
                    data: allData,
                    backgroundColor: colors,
                    borderColor: colors,
                    borderWidth: 1,
                    borderRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                indexAxis: 'y',
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: 'rgba(37, 99, 235, 0.9)',
                        titleColor: '#ffffff',
                        bodyColor: '#ffffff',
                        borderColor: '#2563EB',
                        borderWidth: 1,
                        cornerRadius: 8,
                        callbacks: {
                            label: function(context) {
                                const value = Math.abs(context.parsed.x);
                                const type = context.parsed.x > 0 ? 'Gostam' : 'Não gostam';
                                return `${type}: ${value} menções`;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return Math.abs(value);
                            },
                            color: '#6B7280'
                        },
                        grid: {
                            color: 'rgba(229, 231, 235, 0.5)'
                        }
                    },
                    y: {
                        ticks: {
                            color: '#6B7280',
                            font: {
                                size: 11
                            }
                        },
                        grid: {
                            display: false
                        }
                    }
                },
                animation: {
                    duration: 1500,
                    easing: 'easeOutQuart'
                }
            }
        });
    }

    initInteractions() {
        // Request data button functionality
        const requestBtn = document.getElementById('requestDataBtn');
        if (requestBtn) {
            requestBtn.addEventListener('click', this.handleDataRequest.bind(this));
        }

        // Add hover effects to charts
        Object.values(this.charts).forEach(chart => {
            if (chart.canvas) {
                chart.canvas.addEventListener('mousemove', this.handleChartHover.bind(this));
            }
        });
    }

    async handleDataRequest() {
        const btn = document.getElementById('requestDataBtn');
        if (!btn) return;

        const originalText = btn.innerHTML;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Enviando...';
        btn.disabled = true;

        try {
            const response = await fetch('/api/request-data', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            if (!response.ok) {
                throw new Error('Failed to submit request');
            }

            const result = await response.json();
            
            // Show success message
            btn.innerHTML = '<i class="fas fa-check"></i> Solicitação Enviada!';
            btn.style.backgroundColor = '#10B981';
            
            setTimeout(() => {
                btn.innerHTML = originalText;
                btn.disabled = false;
                btn.style.backgroundColor = '';
            }, 3000);

        } catch (error) {
            console.error('Error submitting data request:', error);
            btn.innerHTML = '<i class="fas fa-exclamation-triangle"></i> Erro - Tente novamente';
            btn.style.backgroundColor = '#EF4444';
            
            setTimeout(() => {
                btn.innerHTML = originalText;
                btn.disabled = false;
                btn.style.backgroundColor = '';
            }, 3000);
        }
    }

    handleChartHover(event) {
        const chart = Chart.getChart(event.target);
        if (chart) {
            event.target.style.cursor = 'pointer';
        }
    }

    addAnimations() {
        // Add fade-in animations to sections
        const sections = document.querySelectorAll('.section, .chart-container, .insight-card, .quote-card');
        
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('fade-in-up');
                    observer.unobserve(entry.target);
                }
            });
        }, observerOptions);

        sections.forEach(section => {
            observer.observe(section);
        });
    }

    showError(message) {
        const container = document.querySelector('.container');
        if (container) {
            const errorDiv = document.createElement('div');
            errorDiv.className = 'error';
            errorDiv.innerHTML = `<i class="fas fa-exclamation-triangle"></i> ${message}`;
            container.insertBefore(errorDiv, container.firstChild);
        }
    }

    // Utility method to update charts with new data
    updateCharts(newData) {
        if (this.charts.ideChart && newData.ide_chart) {
            this.charts.ideChart.data = newData.ide_chart;
            this.charts.ideChart.update('active');
        }
        
        if (this.charts.satisfactionChart && newData.satisfaction_chart) {
            this.charts.satisfactionChart.data = newData.satisfaction_chart;
            this.charts.satisfactionChart.update('active');
        }
        
        if (this.charts.feedbackChart && newData.feedback_chart) {
            this.charts.feedbackChart.data = newData.feedback_chart;
            this.charts.feedbackChart.update('active');
        }
    }

    // Method to resize charts when window is resized
    handleResize() {
        Object.values(this.charts).forEach(chart => {
            if (chart) {
                chart.resize();
            }
        });
    }
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const dashboard = new SurveyDashboard();
    
    // Handle window resize
    window.addEventListener('resize', () => {
        dashboard.handleResize();
    });
    
    // Make dashboard globally available for debugging
    window.surveyDashboard = dashboard;
});

// Smooth scrolling for anchor links
document.addEventListener('click', (e) => {
    if (e.target.tagName === 'A' && e.target.getAttribute('href').startsWith('#')) {
        e.preventDefault();
        const target = document.querySelector(e.target.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    }
});
