// WattWise AI - Main JavaScript File

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });

    // Auto-hide flash messages after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add loading state to forms
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function() {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Processing...';
            }
        });
    });

    // Chart animations
    const charts = document.querySelectorAll('canvas');
    charts.forEach(function(chart) {
        chart.style.opacity = '0';
        setTimeout(function() {
            chart.style.transition = 'opacity 0.5s ease-in';
            chart.style.opacity = '1';
        }, 100);
    });

    // Number formatting for Indian Rupees
    window.formatINR = function(amount) {
        return '₹' + amount.toLocaleString('en-IN', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });
    };

    // Energy consumption formatting
    window.formatEnergy = function(kwh) {
        return kwh.toLocaleString('en-IN', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        }) + ' kWh';
    };

    // Percentage formatting
    window.formatPercentage = function(value) {
        return value.toLocaleString('en-IN', {
            minimumFractionDigits: 1,
            maximumFractionDigits: 1
        }) + '%';
    };

    // Copy to clipboard functionality
    window.copyToClipboard = function(text) {
        navigator.clipboard.writeText(text).then(function() {
            showToast('Copied to clipboard!', 'success');
        }).catch(function(err) {
            console.error('Failed to copy: ', err);
            showToast('Failed to copy to clipboard', 'error');
        });
    };

    // Toast notification system
    window.showToast = function(message, type = 'info') {
        const toastContainer = document.getElementById('toastContainer') || createToastContainer();
        
        const toast = document.createElement('div');
        toast.className = `toast align-items-center text-white bg-${type === 'error' ? 'danger' : type === 'success' ? 'success' : 'primary'} border-0`;
        toast.setAttribute('role', 'alert');
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;
        
        toastContainer.appendChild(toast);
        
        const bsToast = new bootstrap.Toast(toast, {
            autohide: true,
            delay: 3000
        });
        
        bsToast.show();
        
        toast.addEventListener('hidden.bs.toast', function() {
            toast.remove();
        });
    };

    function createToastContainer() {
        const container = document.createElement('div');
        container.id = 'toastContainer';
        container.className = 'toast-container position-fixed top-0 end-0 p-3';
        container.style.zIndex = '1050';
        document.body.appendChild(container);
        return container;
    }

    // Real-time clock for dashboard
    function updateClock() {
        const now = new Date();
        const timeString = now.toLocaleString('en-IN', {
            weekday: 'short',
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        });
        
        const clockElement = document.getElementById('realTimeClock');
        if (clockElement) {
            clockElement.textContent = timeString;
        }
    }

    // Update clock every second
    setInterval(updateClock, 1000);
    updateClock(); // Initial call

    // Energy data refresh simulation
    window.refreshEnergyData = function() {
        const refreshBtn = document.querySelector('[data-action="refresh"]');
        if (refreshBtn) {
            refreshBtn.disabled = true;
            refreshBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Refreshing...';
            
            // Simulate API call
            setTimeout(function() {
                refreshBtn.disabled = false;
                refreshBtn.innerHTML = '<i class="fas fa-sync-alt me-2"></i>Refresh';
                showToast('Energy data refreshed successfully', 'success');
                
                // In a real application, you would fetch new data here
                // and update the charts and tables
            }, 2000);
        }
    };

    // Export data functionality
    window.exportData = function(format = 'csv') {
        showToast(`Exporting data as ${format.toUpperCase()}...`, 'info');
        
        // In a real application, you would make an API call here
        setTimeout(function() {
            showToast('Data exported successfully', 'success');
        }, 1500);
    };

    // Search functionality for insights
    const searchInput = document.getElementById('insightSearch');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const insightCards = document.querySelectorAll('.insight-card');
            
            insightCards.forEach(function(card) {
                const title = card.querySelector('.card-title').textContent.toLowerCase();
                const description = card.querySelector('.card-text').textContent.toLowerCase();
                
                if (title.includes(searchTerm) || description.includes(searchTerm)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    }

    // Filter functionality for insights
    const filterButtons = document.querySelectorAll('[data-filter]');
    filterButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            const filter = this.dataset.filter;
            const insightCards = document.querySelectorAll('.insight-card');
            
            // Update active button
            filterButtons.forEach(function(btn) {
                btn.classList.remove('active', 'btn-primary');
                btn.classList.add('btn-outline-secondary');
            });
            this.classList.remove('btn-outline-secondary');
            this.classList.add('btn-primary', 'active');
            
            // Filter cards
            insightCards.forEach(function(card) {
                if (filter === 'all') {
                    card.style.display = 'block';
                } else {
                    const cardType = card.dataset.type;
                    card.style.display = cardType === filter ? 'block' : 'none';
                }
            });
        });
    });

    // Print functionality
    window.printReport = function() {
        window.print();
    };

    // Keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + P for print
        if ((e.ctrlKey || e.metaKey) && e.key === 'p') {
            e.preventDefault();
            printReport();
        }
        
        // Ctrl/Cmd + R for refresh (prevent default browser refresh)
        if ((e.ctrlKey || e.metaKey) && e.key === 'r') {
            e.preventDefault();
            refreshEnergyData();
        }
    });

    // Performance monitoring
    window.addEventListener('load', function() {
        const loadTime = performance.now();
        console.log(`Page loaded in ${loadTime.toFixed(2)}ms`);
        
        // If load time is slow, show a warning
        if (loadTime > 3000) {
            console.warn('Slow page load detected');
        }
    });

    // Error handling
    window.addEventListener('error', function(e) {
        console.error('JavaScript error:', e.error);
        // In production, you might want to send this to an error tracking service
    });

    // Service Worker registration for PWA capabilities (optional)
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/static/js/sw.js')
            .then(function(registration) {
                console.log('ServiceWorker registration successful');
            })
            .catch(function(err) {
                console.log('ServiceWorker registration failed: ', err);
            });
    }
});

// Utility functions
window.WattWise = {
    // Calculate energy cost based on consumption
    calculateCost: function(kwh, rate = 8.50) {
        return kwh * rate;
    },
    
    // Calculate percentage change
    calculatePercentageChange: function(oldValue, newValue) {
        if (oldValue === 0) return 0;
        return ((newValue - oldValue) / oldValue) * 100;
    },
    
    // Format large numbers with abbreviations
    formatLargeNumber: function(num) {
        if (num >= 1000000) {
            return (num / 1000000).toFixed(1) + 'M';
        } else if (num >= 1000) {
            return (num / 1000).toFixed(1) + 'K';
        }
        return num.toString();
    },
    
    // Generate random color for charts
    generateColor: function() {
        const colors = [
            '#2563eb', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6',
            '#06b6d4', '#84cc16', '#f97316', '#ec4899', '#6366f1'
        ];
        return colors[Math.floor(Math.random() * colors.length)];
    }
};
