// XenForo Forum JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all functionality
    initSearch();
    initSmoothScrolling();
    initAnimations();
    initForumInteractions();
    initMobileMenu();
    initNotifications();
});

// Search functionality
function initSearch() {
    const searchInput = document.querySelector('.search-box input');
    const searchButton = document.querySelector('.search-box button');

    if (searchInput && searchButton) {
        searchButton.addEventListener('click', performSearch);
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                performSearch();
            }
        });
    }
}

function performSearch() {
    const searchInput = document.querySelector('.search-box input');
    const query = searchInput.value.trim();
    
    if (query) {
        // Simulate search functionality
        showNotification(`"${query}" için arama yapılıyor...`, 'info');
        
        // In a real application, this would make an API call
        setTimeout(() => {
            showNotification(`"${query}" için ${Math.floor(Math.random() * 50) + 1} sonuç bulundu.`, 'success');
        }, 1000);
    } else {
        showNotification('Lütfen arama yapmak için bir terim girin.', 'warning');
    }
}

// Smooth scrolling for navigation links
function initSmoothScrolling() {
    const navLinks = document.querySelectorAll('nav a[href^="#"]');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                targetSection.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
                
                // Update active navigation
                updateActiveNav(this);
            }
        });
    });
}

function updateActiveNav(activeLink) {
    // Remove active class from all nav links
    document.querySelectorAll('nav a').forEach(link => {
        link.classList.remove('active');
    });
    
    // Add active class to clicked link
    activeLink.classList.add('active');
}

// Scroll animations
function initAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Observe elements for animation
    const animatedElements = document.querySelectorAll('.forum-item, .topic-item, .member-card');
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
}

// Forum interactions
function initForumInteractions() {
    // Forum item hover effects
    const forumItems = document.querySelectorAll('.forum-item');
    forumItems.forEach(item => {
        item.addEventListener('mouseenter', function() {
            this.style.transform = 'translateX(10px) scale(1.02)';
        });
        
        item.addEventListener('mouseleave', function() {
            this.style.transform = 'translateX(0) scale(1)';
        });
    });
    
    // Topic item interactions
    const topicItems = document.querySelectorAll('.topic-item');
    topicItems.forEach(item => {
        item.addEventListener('click', function(e) {
            if (!e.target.closest('a')) {
                const topicLink = this.querySelector('h4 a');
                if (topicLink) {
                    showNotification(`"${topicLink.textContent}" konusu açılıyor...`, 'info');
                }
            }
        });
    });
    
    // Member card interactions
    const memberCards = document.querySelectorAll('.member-card');
    memberCards.forEach(card => {
        card.addEventListener('click', function() {
            const memberName = this.querySelector('h4').textContent;
            showNotification(`${memberName} profilini görüntülüyorsunuz.`, 'info');
        });
    });
}

// Mobile menu functionality
function initMobileMenu() {
    // Create mobile menu button
    const header = document.querySelector('.header-container');
    const nav = document.querySelector('.nav');
    
    if (header && nav) {
        const mobileMenuBtn = document.createElement('button');
        mobileMenuBtn.className = 'mobile-menu-btn';
        mobileMenuBtn.innerHTML = '<i class="fas fa-bars"></i>';
        mobileMenuBtn.style.display = 'none';
        
        mobileMenuBtn.addEventListener('click', function() {
            nav.classList.toggle('mobile-active');
            this.innerHTML = nav.classList.contains('mobile-active') ? 
                '<i class="fas fa-times"></i>' : '<i class="fas fa-bars"></i>';
        });
        
        header.appendChild(mobileMenuBtn);
        
        // Show/hide mobile menu button based on screen size
        function checkMobileMenu() {
            if (window.innerWidth <= 768) {
                mobileMenuBtn.style.display = 'block';
                nav.classList.add('mobile-nav');
            } else {
                mobileMenuBtn.style.display = 'none';
                nav.classList.remove('mobile-nav', 'mobile-active');
            }
        }
        
        checkMobileMenu();
        window.addEventListener('resize', checkMobileMenu);
    }
}

// Notification system
function initNotifications() {
    // Create notification container
    const notificationContainer = document.createElement('div');
    notificationContainer.className = 'notification-container';
    notificationContainer.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 10000;
        max-width: 300px;
    `;
    document.body.appendChild(notificationContainer);
}

function showNotification(message, type = 'info') {
    const notificationContainer = document.querySelector('.notification-container');
    
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.style.cssText = `
        background: ${getNotificationColor(type)};
        color: white;
        padding: 15px 20px;
        border-radius: 8px;
        margin-bottom: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        transform: translateX(100%);
        transition: transform 0.3s ease;
        position: relative;
        overflow: hidden;
    `;
    
    notification.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span>${message}</span>
            <button onclick="this.parentElement.parentElement.remove()" 
                    style="background: none; border: none; color: white; cursor: pointer; font-size: 18px;">
                ×
            </button>
        </div>
    `;
    
    notificationContainer.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => {
                if (notification.parentElement) {
                    notification.remove();
                }
            }, 300);
        }
    }, 5000);
}

function getNotificationColor(type) {
    const colors = {
        success: '#4CAF50',
        error: '#f44336',
        warning: '#ff9800',
        info: '#2196F3'
    };
    return colors[type] || colors.info;
}

// Statistics counter animation
function animateCounters() {
    const counters = document.querySelectorAll('.stat-number');
    
    counters.forEach(counter => {
        const target = parseInt(counter.textContent.replace(/,/g, ''));
        const increment = target / 100;
        let current = 0;
        
        const updateCounter = () => {
            if (current < target) {
                current += increment;
                counter.textContent = Math.floor(current).toLocaleString();
                requestAnimationFrame(updateCounter);
            } else {
                counter.textContent = target.toLocaleString();
            }
        };
        
        updateCounter();
    });
}

// Initialize counter animation when page loads
window.addEventListener('load', function() {
    setTimeout(animateCounters, 1000);
});

// Add CSS for mobile menu
const mobileMenuCSS = `
    @media (max-width: 768px) {
        .mobile-nav {
            position: absolute;
            top: 100%;
            left: 0;
            right: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            flex-direction: column;
            padding: 1rem;
            transform: translateY(-100%);
            opacity: 0;
            transition: all 0.3s ease;
            z-index: 999;
        }
        
        .mobile-nav.mobile-active {
            transform: translateY(0);
            opacity: 1;
        }
        
        .mobile-nav ul {
            flex-direction: column;
            gap: 1rem;
        }
        
        .mobile-menu-btn {
            background: transparent;
            border: none;
            color: white;
            font-size: 1.5rem;
            cursor: pointer;
            padding: 0.5rem;
        }
    }
`;

// Inject mobile menu CSS
const style = document.createElement('style');
style.textContent = mobileMenuCSS;
document.head.appendChild(style);

// Add loading animation
function showLoading() {
    const loading = document.createElement('div');
    loading.className = 'loading-overlay';
    loading.innerHTML = `
        <div class="loading-spinner">
            <i class="fas fa-spinner fa-spin"></i>
            <p>Yükleniyor...</p>
        </div>
    `;
    loading.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.5);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 10000;
    `;
    
    const spinner = loading.querySelector('.loading-spinner');
    spinner.style.cssText = `
        background: white;
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
    `;
    
    spinner.querySelector('i').style.cssText = `
        font-size: 2rem;
        color: #667eea;
        margin-bottom: 1rem;
    `;
    
    document.body.appendChild(loading);
    
    return loading;
}

function hideLoading(loadingElement) {
    if (loadingElement) {
        loadingElement.remove();
    }
}

// Simulate loading for forum interactions
document.addEventListener('click', function(e) {
    if (e.target.closest('.forum-info h4 a') || e.target.closest('.topic-info h4 a')) {
        const loading = showLoading();
        setTimeout(() => {
            hideLoading(loading);
            showNotification('Forum sayfası yüklendi!', 'success');
        }, 1500);
    }
});

// Add keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + K for search
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        const searchInput = document.querySelector('.search-box input');
        if (searchInput) {
            searchInput.focus();
        }
    }
    
    // Escape to close notifications
    if (e.key === 'Escape') {
        const notifications = document.querySelectorAll('.notification');
        notifications.forEach(notification => notification.remove());
    }
});

// Add tooltips
function addTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');
    
    tooltipElements.forEach(element => {
        element.addEventListener('mouseenter', function() {
            const tooltip = document.createElement('div');
            tooltip.className = 'tooltip';
            tooltip.textContent = this.getAttribute('data-tooltip');
            tooltip.style.cssText = `
                position: absolute;
                background: #333;
                color: white;
                padding: 5px 10px;
                border-radius: 4px;
                font-size: 12px;
                z-index: 1000;
                pointer-events: none;
                white-space: nowrap;
            `;
            
            document.body.appendChild(tooltip);
            
            const rect = this.getBoundingClientRect();
            tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
            tooltip.style.top = rect.top - tooltip.offsetHeight - 5 + 'px';
            
            this.tooltip = tooltip;
        });
        
        element.addEventListener('mouseleave', function() {
            if (this.tooltip) {
                this.tooltip.remove();
                this.tooltip = null;
            }
        });
    });
}

// Initialize tooltips
addTooltips();

console.log('XenForo Forum JavaScript yüklendi! 🚀');